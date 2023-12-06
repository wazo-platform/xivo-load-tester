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



import argparse
import logging
import os.path
from loadtester.config import ScenarioConfig
from loadtester.runner import ScenarioRunner
from loadtester.scenario import Scenario

_CONFIG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../etc'))
_CONFIG_FILE = os.path.join(_CONFIG_DIR, 'conf.py')


def main():
    _init_logging()

    parsed_args = _parse_args()

    if parsed_args.verbose:
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

    scenario = Scenario(parsed_args.scenario_dir, parsed_args.run_dir)

    scenario_config = ScenarioConfig.new_from_filename(parsed_args.conf)
    if parsed_args.background:
        scenario_config.set_option('sipp_background', True)

    scenario_runner = ScenarioRunner()
    scenario_runner.start_scenario(scenario, scenario_config)


def _init_logging():
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
    logger.addHandler(handler)
    logger.setLevel(logging.WARNING)


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--background', action='store_true',
                        help='run sipp in background')
    parser.add_argument('-c', '--conf', default=_CONFIG_FILE,
                        help='path to the config file')
    parser.add_argument('-d', '--run-dir',
                        help='run scenario in this directory')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='increase verbosity')
    parser.add_argument('scenario_dir',
                        help='path to the scenario directory')
    return parser.parse_args()


if __name__ == '__main__':
    main()
