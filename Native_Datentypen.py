list = [1, 2, 3, 4, 5] # Listen sind veränderlich
print("Das ist eine Liste: ", list)
list.append(6)
print("Liste nach dem Hinzufügen einer 6: ", list)

tuple = (1, 2, 3, 4, 5) # Tuples sind unveränderlich
print("Das ist ein Tuple: ", tuple)


dict = {"eins": 1, "zwei": 2, "drei": 3} # Dictionaries sind key-value Paare
print("Das ist ein Dictionary: ", dict)
dict["vier"] = 4
print("Dictionary nach dem Hinzufügen von 'vier': ", dict)

set = {1, 2, 3, 4, 5} # Sets sind ungeordnet und enthalten keine Duplikate
print("Das ist ein Set: ", set)
