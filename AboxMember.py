"""
Classe che rappresenta l'Abox dell'ontologia.
Possiede un id della classe (malattia), il nome del paziente e se fa parte o meno dei sintomi
"""


class AboxMember:

    def __init__(self, class_identifier, member_name, symp: bool = False):
        self.class_identifier = class_identifier
        self.member_name = member_name
        self.isSymptom = symp

    def __str__(self):
        return "AboxM | id: " + self.class_identifier.name + " | member name: " + self.member_name + \
                " | è un sintomo?: " + self.isSymptom.__str__()


