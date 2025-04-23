# -*- coding: utf-8 -*-

# Copyright 2013-2023 The Wazo Authors  (see the AUTHORS file)
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

import logging
import time

logger = logging.getLogger(__name__)


class ScenarioConfig(object):

    def __init__(self, config_content):
        self._config = {}
        self._scenarios = _ScenariosObject()
        self._read_config(config_content)

    def _read_config(self, config_content):
        self._config['scenarios'] = self._scenarios
        exec(config_content, self._config)
        del self._config['scenarios']
        del self._config['__builtins__']

    def set_option(self, key, value):
        self._config[key] = value

    def get_context_for_scenario(self, scenario_name):
        context = dict(self._config)
        attribute_name = scenario_name.replace('-', '_')
        scenario_dict = getattr(self._scenarios, attribute_name, {})
        context.update(scenario_dict)
        context['sipp_std_options'] = self._compute_sipp_std_options(context)
        self._emit_deprecation_warning(context)
        return context

    _SIPP_STD_OPTIONS = [
        # ('sipp_local_ip', '-i'),
        ('sipp_call_rate', '-r'),
        ('sipp_pause_in_ms', '-d'),
        ('sipp_rate_period_in_ms', '-rp'),
        ('sipp_max_simult_calls', '-l'),
        ('sipp_nb_of_calls_before_exit', '-m'),
    ]

    _SIPP_STD_FLAGS = [
        ('sipp_auto_answer', '-aa'),
        ('sipp_background', '-bg'),
        ('sipp_enable_trace_calldebug', '-trace_calldebug'),
        ('sipp_enable_trace_err', '-trace_err'),
        ('sipp_enable_trace_shortmsg', '-trace_shortmsg'),
        ('sipp_enable_trace_stat', '-trace_stat'),
    ]

    def _compute_sipp_std_options(self, context):
        sipp_std_options_list = []
        for key, option_flag in self._SIPP_STD_OPTIONS:
            if key in context:
                sipp_std_options_list.extend([option_flag, str(context[key])])
        for key, option_flag in self._SIPP_STD_FLAGS:
            if context.get(key, False):
                sipp_std_options_list.extend([option_flag])
        return ' '.join(sipp_std_options_list)

    def _emit_deprecation_warning(self, context):
        if 'sipp_pause_in_ms' in context:
            logger.warning('deprecated config key "sipp_pause_in_ms": please use "pause"')
            time.sleep(3)

    @classmethod
    def new_from_filename(cls, filename):
        with open(filename) as fobj:
            config_content = fobj.read()
        return cls(config_content)


class _ScenariosObject(object):
    pass
