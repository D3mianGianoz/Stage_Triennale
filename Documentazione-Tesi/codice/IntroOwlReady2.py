from owlready2 import *

# Caricare un ontologia da una repostiory locale o da Internet:
onto = get_ontology("http://www.lesfleursdunormal.fr/.. .../pizza_onto.owl")
onto.load()

# Creare nuove classi nell'ontologia
# mischiando costrutti OWL e metodi Python:
class NonVegeterianPizza(onto.Pizza):
    equivalent_to = [onto.Pizza & 
    (onto.has_topping.some(onto.MeatTopping) | 
    onto.has_topping.some(onto.FishTopping)
    )]

    def eat(self) : print ("Yuuum! So good!")

with onto:
    class Pizza (Thing):
        def eat(self) : print ("I love pizza !")
    pass

# Accedere le classi dell'ontologia e creare nuovi Individui/instanze:
test_pizza = onto.Pizza("test_pizza_owl_identifier")
test_pizza.has_topping = [onto.CheeseTopping(),onto.TomatoTopping()]
print(test_pizza.has_topping) 
''' [pizza_onto.cheesetopping1, pizza_onto.tomatotopping1] '''

# In questo pacchetto quasi ogni lista può essere modificata sul posto, 
# per esempio aggiungendo/rimuovendo elementi dalla lista.
# Owlready2 aggiornerà in automatico il quadstore RDF.
test_pizza.has_topping.append(onto.MeatTopping()) 
print(test_pizza.has_topping) 
''' [pizza_onto.cheesetopping1, pizza_onto.tomatotopping1, 
	pizza_onto.meattopping1]'''
test_pizza.eat() ''' I love pizza ! '''

# Effeturare "reasoning" e classificare le istanze e le classi
print(test_pizza.__class__) ''' pizza_onto.Pizza '''
sync_reasoner()
print(test_pizza.__class__) ''' pizza_onto.NonVegeterianPizza '''
test_pizza.eat()            ''' Yuuum! So good! '''

# Esportare l'ontologia in un file .owl
onto.save("Demo")

