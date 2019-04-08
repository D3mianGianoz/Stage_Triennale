"""
Classe che rappresenta lo scenario da aggiungere all'ontologia per l'interrogazione
"""


class Scenario:

    def __init__(self, list_of_typical_members=None, probability=None):
        if list_of_typical_members is None:
            list_of_typical_members = []
        self.list_of_typical_members = list_of_typical_members
        self.probability = probability

