# -*- coding: UTF-8 -*-


class ScenarioRunner(object):

    def start_scenario(self, scenario, scenario_config):
        context = scenario_config.get_context_for_scenario(scenario.name)
        scenario.prepare_run(context)
        scenario.run()
