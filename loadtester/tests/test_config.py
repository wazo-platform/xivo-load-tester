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

import os.path
import unittest
from loadtester.config import ScenarioConfig


class TestScenarioConfig(unittest.TestCase):

    def test_simple_config(self):
        config_content = "a = 'a'\n"

        config = ScenarioConfig(config_content)

        expected_context = self._new_context({'a': 'a'})
        self.assertEqual(expected_context, config.get_context_for_scenario('s1'))

    def _new_context(self, context=None):
        base_context = {'sipp_std_options': ''}
        if context is not None:
            base_context.update(context)
        return base_context

    def test_config_with_undefined_name_raise_exception(self):
        config_content = "a = b\n"

        self.assertRaises(Exception, ScenarioConfig, config_content)

    def test_config_with_bad_syntax_raise_exception(self):
        config_content = "!a\n"

        self.assertRaises(Exception, ScenarioConfig, config_content)

    def test_new_from_filename(self):
        config_filename = os.path.join(os.path.dirname(__file__), 'config', 'example1')

        config = ScenarioConfig.new_from_filename(config_filename)

        expected_context = self._new_context({'a': 'a'})
        self.assertEqual(expected_context, config.get_context_for_scenario('s1'))

    def test_config_using_scenarios_variable(self):
        config_content = """\
scenarios.s1 = dict(a='s1.a')
"""

        config = ScenarioConfig(config_content)

        expected_context = self._new_context({'a': 's1.a'})
        self.assertEqual(expected_context, config.get_context_for_scenario('s1'))

    def test_global_variables_doesnt_override_scenario_variable(self):
        config_content = """\
scenarios.s1 = dict(a='s1.a')
a = 'a'
"""

        config = ScenarioConfig(config_content)

        expected_context = self._new_context({'a': 's1.a'})
        self.assertEqual(expected_context, config.get_context_for_scenario('s1'))

    def test_hyphen_are_converted_to_underscore(self):
        config_content = "scenarios.s_1 = dict(a='s_1.a')\n"

        config = ScenarioConfig(config_content)

        expected_context = self._new_context({'a': 's_1.a'})
        self.assertEqual(expected_context, config.get_context_for_scenario('s-1'))

    def test_sipp_std_options_is_built(self):
        config_content = """\
sipp_local_ip = 'local_ip'
sipp_call_rate = 1.0
sipp_rate_period_in_ms = 1000
sipp_max_simult_calls = 3
sipp_background = True
sipp_enable_trace_calldebug = True
sipp_enable_trace_err = True
sipp_enable_trace_shortmsg = True
sipp_enable_trace_stat = True
sipp_nb_of_calls_before_exit = 4
"""

        config = ScenarioConfig(config_content)

        sipp_std_options = config.get_context_for_scenario('s1')['sipp_std_options']
        self.assertEqual('-i local_ip -r 1.0 -rp 1000 -l 3 -m 4 -bg -trace_calldebug -trace_err -trace_shortmsg -trace_stat',
                         sipp_std_options)

    def test_sipp_std_option_when_sipp_enable_traces_are_false(self):
        config_content = """\
sipp_enable_trace_calldebug = False
sipp_enable_trace_err = False
sipp_enable_trace_shortmsg = False
sipp_enable_trace_stat = False
"""

        config = ScenarioConfig(config_content)

        sipp_std_options = config.get_context_for_scenario('s1')['sipp_std_options']
        self.assertEqual('', sipp_std_options)

    def test_set_option_when_set(self):
        config = ScenarioConfig('')

        config.set_option('sipp_background', True)

        context = config.get_context_for_scenario('s1')
        self.assertTrue(context['sipp_background'])

    def test_set_option_when_not_set(self):
        config = ScenarioConfig('')

        context = config.get_context_for_scenario('s1')
        self.assertFalse('sipp_background' in context)
