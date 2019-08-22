"""
Classe che assieme alla classe TypicalMember costituisce la Tbox dell'ontologia
"""


class TypicalFact:

    def __init__(self, t_class_identifier, class_identifier, probability):
        self.t_class_identifier = t_class_identifier
        self.class_identifier = class_identifier
        self.probability = probability
        self.typical_fact_name = "T"+t_class_identifier.name+"_"+class_identifier.name

    def __str__(self):
        return self.t_class_identifier.name + " | " + self.class_identifier.name + " | " + str(self.probability) \
               + " | " + self.typical_fact_name

