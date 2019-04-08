"""
Classe che assieme alla classe TypicalFact costituisce la Tbox dell'ontologia
"""


class TypicalMember:
    counter = 0

    def __init__(self, t_class_identifier, member_name, probability):
        self.t_class_identifier = t_class_identifier
        self.member_name = member_name
        self.probability = probability
        self.key = TypicalMember.counter
        TypicalMember.counter += 1


