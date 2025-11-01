# This is the object class used to store the transaction database
# information in a workable format.

class Database:

    # Initializes the database object to have 2 variables, size and a transaction list.
    # Requires a filepath on initialization.
    def __init__(self, file_path):
        try:
            with open (file_path, 'r') as file: 
                self.size = int(file.readline())
                self.transactions = [None] * self.size
                for line in file:
                    line = line.strip()
                    components = line.split("	") # gets an array of the line, split on tab characters
                    index = int(components[0])-1 #components[0] is the index, but subtract 1 from it so we are 0 indexing
                    self.transactions[index]:frozenset = frozenset(components[2].split(" ")) # this splits on spaces for the transactions
                    # this leaves the list set up like an array, 0 indexed, where each entry is 
                    # another list, containing the transactions. 
        except FileNotFoundError:
            print(f"Error: The file '{file_path}' was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
