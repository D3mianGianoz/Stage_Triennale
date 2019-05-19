from TypicalMember import *
from itertools import *
from Scenario import *

'''
Questo modulo fornisce una serie di metodi utilizzati per calcolare le probabilità da associare ad ogni TypicalMember,
generare tutti gli scenari possibili e associare ad ogni scenario la probabilità opportuna.
'''


def compute_probability_for_typical_members(ontology_manager):
    ontology_manager.typical_facts_list.sort(key=lambda x: x.t_class_identifier.name)
    ontology_manager.a_box_members_list.sort(key=lambda x: x.class_identifier.name)
    length = len(ontology_manager.typical_facts_list) - 1
    i = 0
    probability_to_assign_to_typical_member = 1.0
    while i <= length:
        while i < length and ontology_manager.typical_facts_list[i].t_class_identifier.name == \
                ontology_manager.typical_facts_list[i + 1].t_class_identifier.name:

            probability_to_assign_to_typical_member = float(probability_to_assign_to_typical_member *
                                                            ontology_manager.typical_facts_list[i].probability)
            i = i + 1
        probability_to_assign_to_typical_member = \
            float(probability_to_assign_to_typical_member * ontology_manager.typical_facts_list[i].probability)
        __set_probability(
            probability_to_assign_to_typical_member,
            ontology_manager,
            ontology_manager.typical_facts_list[i].t_class_identifier)
        i = i + 1
        # Reset della probabilita
        probability_to_assign_to_typical_member = 1.0


def __set_probability(probability_to_assign_to_typical_member, ontology_manager, t_class_identifier):
    for abm in ontology_manager.a_box_members_list:
        if abm.class_identifier.name == t_class_identifier.name:
            ontology_manager.typical_members_list.append(TypicalMember(
                abm.class_identifier,
                abm.member_name,
                probability_to_assign_to_typical_member
            ))


def generate_scenarios(ontology_manager):
    return chain(*map(lambda x: combinations(
        ontology_manager.typical_members_list, x), range(0, len(ontology_manager.typical_members_list) + 1))
                 )


def set_probability_for_each_scenario(scenarios, ontology_manager):
    for scenario in scenarios:
        scenario = list(scenario)
        probability_to_assign_to_each_scenario = 1
        for tm in scenario:
            probability_to_assign_to_each_scenario = probability_to_assign_to_each_scenario * tm.probability
        diff = __difference(scenario, ontology_manager.typical_members_list)
        for key in diff:
            typical_member = __get_typical_member(key, ontology_manager)
            probability_to_assign_to_each_scenario = probability_to_assign_to_each_scenario * \
                                                     (1 - typical_member.probability)
        ontology_manager.scenarios_list.append(Scenario(scenario,
                                                        probability_to_assign_to_each_scenario))


def __difference(scenario, typical_members_list):
    scenario_keys = list()
    typical_members_keys = list()
    for s in scenario:
        scenario_keys.append(s.key)
    for tm in typical_members_list:
        typical_members_keys.append(tm.key)
    li_diff = [key for key in scenario_keys + typical_members_keys
               if key not in scenario_keys or key not in typical_members_keys]
    return li_diff


def __get_typical_member(key, ontology_manager):
    for tm in ontology_manager.typical_members_list:
        if key == tm.key:
            return tm
