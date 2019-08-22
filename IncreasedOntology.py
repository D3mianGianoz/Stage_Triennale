from TypicalMember import *
from itertools import combinations,chain
from Scenario import *

'''
Questo modulo fornisce una serie di metodi utilizzati per calcolare le probabilità da associare ad ogni TypicalMember,
generare tutti gli scenari possibili e associare ad ogni scenario la probabilità opportuna.

Elemento chiave per la diagnosi:
1 La generazione di scenari quando deve avvenire ?
2 Come dedurre quali fatti vanno negli scenari ?
'''


def compute_probability_for_typical_members(onto_manager):
    facts_list = onto_manager.typical_facts_list
    abox_members_list = onto_manager.a_box_members_list
    facts_list.sort(key=lambda x: x.t_class_identifier.name)
    abox_members_list.sort(key=lambda x: x.class_identifier.name)
    length = len(facts_list) - 1
    i = 0
    cnsec: int = 0
    prob_to_assign_to_typical_member = 1.0
    while i <= length:
        while i < length and facts_list[i].t_class_identifier.name == facts_list[i + 1].t_class_identifier.name:
            prob_to_assign_to_typical_member = float(prob_to_assign_to_typical_member *
                                                            facts_list[i].probability)
            i = i + 1
            cnsec += 1
        prob_to_assign_to_typical_member = float(prob_to_assign_to_typical_member * facts_list[i].probability)
        # Casi consecutivi
        while cnsec > 0:
            __set_probability(
                prob_to_assign_to_typical_member,onto_manager,facts_list[i - cnsec].t_class_identifier,
                facts_list[i - cnsec].class_identifier)
            cnsec -= 1
        # casi "normali"
        __set_probability(
            prob_to_assign_to_typical_member,onto_manager,facts_list[i].t_class_identifier,
            facts_list[i].class_identifier)
        i = i + 1
        prob_to_assign_to_typical_member = 1.0
        cnsec = 0

#      if aboxMember.class_identifier.name == t_class_identifier.name:

def __set_probability(probability_to_assign_to_typical_member, ontology_manager, t_class_identifier , class_id):
    for aboxMember in ontology_manager.a_box_members_list:
        if aboxMember.isSymptom is True and aboxMember.class_identifier.name == class_id.name:
            #print("Abox M class ID: ", aboxMember.class_identifier.name, " name", aboxMember.member_name, "prob", probability_to_assign_to_typical_member)
            ontology_manager.typical_members_list.append(TypicalMember(
                    t_class_identifier,
                    aboxMember.member_name,
                    probability_to_assign_to_typical_member
                ))


def generate_scenarios(ontology_manager):
    return chain(*map(lambda x: combinations(
        ontology_manager.typical_members_list, x), range(0, len(ontology_manager.typical_members_list) + 1))
                 )


def set_probability_for_each_scenario(scenarios, ontology_manager):
    #TODO trovare un modo migliore per gestire lo scenario vuoto
    scenarios.__next__()
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
