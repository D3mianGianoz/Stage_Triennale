from OntologyManager import OntologyManager
from owlready2 import Not

'''
Il seguente metodo prendendo in input un oggetto di tipo OntologyManager
ha il compito di costruire l'ontologia leggendo i dati forniti dal file
"OntologyInput"
'''


def build_ontology(onto_manager: OntologyManager):
    file_object = open("OntologyInput.txt", "r")
    for line in file_object:
        if line[:-1] == "Classes:":
            line = file_object.readline().rstrip("\n")
            class_names_list = line.split()
            for class_name in class_names_list:
                if class_name.startswith("Not"):
                    class_name = strip_not(class_name)
                    onto_manager.create_class(class_name)
                    test = onto_manager.create_class("Not(" + class_name + ")")
                    test.equivalent_to = [
                        onto_manager.create_complementary_class(onto_manager.get_class(class_name))]
                else:
                    onto_manager.create_class(class_name)
        if line[:-1] == "Set_as_sub_class:":
            line = file_object.readline().rstrip("\n")
            if line is not "":
                sub_class_list = line.split()
                for classes_couple in sub_class_list:
                    split_classes_couple = classes_couple.split(",")
                    sub_class = onto_manager.get_class(split_classes_couple[0])
                    super_class = onto_manager.get_class(split_classes_couple[1])
                    onto_manager.add_sub_class(sub_class, super_class)
        if line[:-1] == "Add_members_to_class:":
            line = file_object.readline().rstrip("\n")
            list_couple_member_classes = line.split(" | ")
            for couple_member_classes in list_couple_member_classes:
                couple_splitted = couple_member_classes.split(";")
                member_name = couple_splitted[0]
                classes = couple_splitted[1].split(",")
                member_identifier = onto_manager.add_member_to_class(member_name,
                                                                     onto_manager.get_class(classes[0]))
                i = 1
                while i < len(classes):
                    onto_manager.add_member_to_multiple_classes(member_identifier,
                                                                [onto_manager.get_class(classes[i])])
                    i += 1
        if line[:-1] == "Set_typical_facts:":
            fact = file_object.readline().rstrip("\n")
            while fact != "$$$\n":
                splitted_fact = fact.split(",")
                splitted_fact[0] = strip_typical(splitted_fact[0])

                # Crea la classe complementare negata
                if splitted_fact[1].startswith("Not"):
                    splitted_fact[1] = strip_not(splitted_fact[1])
                    splitted_fact_1_identifier = onto_manager.create_class("Not(" + splitted_fact[1] + ")")
                    splitted_fact_1_identifier.equivalent_to = [
                        onto_manager.create_complementary_class(onto_manager.get_class(splitted_fact[1]))]
                    onto_manager.add_typical_fact(onto_manager.get_class(splitted_fact[0]),
                                                  splitted_fact_1_identifier,
                                                  float(splitted_fact[2]))
                else:
                    onto_manager.add_typical_fact(onto_manager.get_class(splitted_fact[0]),
                                                  onto_manager.get_class(splitted_fact[1]),
                                                  float(splitted_fact[2]))
                # leggo la prossima riga
                fact = file_object.readline()
        if line[:-1] == "Set_cost_of:":
            temp = dict()
            cost_list: list = file_object.read().splitlines()
            for cost in cost_list:
                splitted = cost.split(": ")
                temp[splitted[0]] = int(splitted[1])
            # Salvo il dict
            onto_manager.cost_dict = temp
    onto_manager.save_base_world()
    file_object.close()


def read_symptoms(ontology_manager, result: bool = False):
    file_object = open("PatientSetOfSymptoms.txt", "r")
    line = file_object.readline().rstrip("\n")
    list_couple_patient_class = line.split(" | ")
    symptoms_for_plot: str = ""
    for couple in list_couple_patient_class:
        patient_str: str
        couple_member_class = couple.split(";")
        test: bool = couple_member_class[1].startswith("Not")
        couple_member_class[1] = strip_not(couple_member_class[1])
        class_c = ontology_manager.create_class(couple_member_class[1])
        not_class_c = ontology_manager.create_class("Not(" + couple_member_class[1] + ")")
        class_c.equivalent_to = [Not(not_class_c)]
        print_msg: str = "Sintomo aggiunto: " + couple_member_class[0]
        if not test:
            patient_str = class_c.name
            ontology_manager.add_member_to_class(couple_member_class[0], class_c, symp=True)
            ontology_manager.store_for_reasoning(couple_member_class[0], class_c)
        else:
            patient_str = not_class_c.name
            ontology_manager.add_member_to_class(couple_member_class[0], not_class_c, symp=True)
            ontology_manager.store_for_reasoning(couple_member_class[0], not_class_c)
        print(print_msg + " " + patient_str)
        symptoms_for_plot += "#" + patient_str + " "
    file_object.close()

    if result:
        return symptoms_for_plot


def strip_not(string_to_strip: str):
    return string_to_strip.replace("Not", "", 1).replace("(", "").replace(")", "")


def strip_typical(string_to_strip: str):
    return string_to_strip.replace("Typical", "", 1).replace("(", "").replace(")", "")
