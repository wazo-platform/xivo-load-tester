# -*- coding: utf-8 -*-

# Copyright (C) 2013 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

import errno
import os
import shutil
import subprocess
from jinja2 import Environment, FileSystemLoader, StrictUndefined


class Scenario(object):

    def __init__(self, directory, run_directory=None):
        if run_directory is None:
            run_directory = directory

        self.directory = directory
        self._run_directory = run_directory
        self.name = self._extract_scenario_name()

    def _extract_scenario_name(self):
        return os.path.basename(self.directory.rstrip("/"))

    def prepare_run(self, context):
        if self.directory != self._run_directory:
            self._create_run_directory()
            self._copy_files_into_run_directory()
        self._generate_templates(context)

    def _create_run_directory(self):
        try:
            os.mkdir(self._run_directory)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    def _copy_files_into_run_directory(self):
        for filename in os.listdir(self.directory):
            if filename.endswith('.csv'):
                continue

            src_filename = os.path.join(self.directory, filename)
            dst_filename = os.path.join(self._run_directory, filename)
            shutil.copyfile(src_filename, dst_filename)

    def _generate_templates(self, context):
        tpl_processor = _TemplatesProcessor(self._run_directory, context)
        tpl_processor.generate_files()

    def run(self):
        process = subprocess.Popen(['sh', 'start.sh'], cwd=self._run_directory)
        process.communicate()


class _TemplatesProcessor(object):

    _TEMPLATE_SUFFIX = '.tpl'
    _TEMPLATE_SUFFIX_LENGTH = len(_TEMPLATE_SUFFIX)

    def __init__(self, directory, context):
        self._directory = directory
        self._context = context
        self._environment = self._new_environment(directory)

    def _new_environment(self, directory):
        env = Environment(loader=FileSystemLoader(directory),
                          undefined=StrictUndefined)
        env.filters['sipp_pause'] = _sipp_pause_filter
        env.filters['sipp_rtp'] = _sipp_rtp_filter
        return env

    def generate_files(self):
        for tpl_filename in self._list_template_filenames():
            self._generate_file_from_template(tpl_filename)

    def _list_template_filenames(self):
        for filename in os.listdir(self._directory):
            if self._is_template_filename(filename):
                yield filename

    def _is_template_filename(self, filename):
        return filename.endswith(self._TEMPLATE_SUFFIX)

    def _generate_file_from_template(self, tpl_filename):
        filename = self._get_template_destination(tpl_filename)
        template = self._environment.get_template(tpl_filename)
        template.stream(self._context).dump(filename)

    def _get_template_destination(self, tpl_filename):
        filename = tpl_filename[:-self._TEMPLATE_SUFFIX_LENGTH]
        return os.path.join(self._directory, filename)


def _sipp_pause_filter(pause_dict):
    attributes = ' '.join('%s="%s"' % item for item in pause_dict.iteritems())
    return '<pause %s />' % attributes


def _sipp_rtp_filter(filename, codec):
    if not filename:
        return ''

    filename = os.path.abspath(os.path.join('audio', '%s.%s' % (filename, codec['name'])))
    return '<nop><action><exec rtp_stream="%s,1,%s"/></action></nop>' % (filename, codec['pt'])
