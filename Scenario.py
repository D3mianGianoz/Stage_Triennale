"""
Classe che rappresenta lo scenario da aggiungere all'ontologia per l'interrogazione
Ha due parametri, la lista dei membri tipici e la probabilità complessiva dello scenario
"""


class Scenario:

    def __init__(self, list_of_typical_members=None, probability=None):
        if list_of_typical_members is None:
            list_of_typical_members = []
        self.list_of_typical_members = list_of_typical_members
        self.probability = probability

    def __str__(self):
        result: str = ""
        for member in self.list_of_typical_members:
            result += member.__str__()
        return "Lista membri tipici: " + result + "probabilita': " + str(self.probability) 

    def __repr__(self):
        result: str = ""
        for member in self.list_of_typical_members:
            result += member.__str__() + "\n"
        return "Lista membri tipici: " + result + "probabilita': " + str(self.probability)

