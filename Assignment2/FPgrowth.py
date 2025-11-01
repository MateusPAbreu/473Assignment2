import sys
from database import Database #unclear why database import is not working


file_name = sys.argv[1] #this is the file path we will be opening
sup = int(sys.argv[2]) #minimum support
sup_percent = sup/100
min_sup = 0
data:Database

def table():
    # initializes the C0 table 
    c_table:dict[frozenset, int] = {}
    for transaction in data.transactions:
        for item in transaction:
            key = frozenset([item])
            c_table[key] = c_table.get(key, 0) + 1
    #print(f"Initial C0 table is: \n{c_table}")
    l_table: dict[frozenset, int] = {}
    l_table = make_l_table(c_table, {}) # initialize the first l table
    print(l_table)
    #up to here we should be able to get the first l table, and from there it would be possible to start the tree

#we need at least the l1 table, so that's the purpose of this whole thing 
def make_l_table(c_table:dict[frozenset, int], previous_l_table:dict[frozenset, int]):
    l_table: dict[frozenset, int] = {}
    for item in c_table:
        if (c_table[item] >= min_sup):
            l_table[item] = c_table[item]
    #print(f"l table is \n{l_table}")

#I don't think we need the next two commented blocks of code for this algorithm, since we just need the first table
    # if (len(previous_l_table) > 1):
    #     l_table = validate_items(l_table, previous_l_table)

    # global frequent_patterns
    # frequent_patterns.update(l_table)

    return l_table

def main():
    data = Database(file_name)
    global min_sup
    min_sup = int(data.size * sup_percent) #amount of items * sup_percent -> MST

    #in all honesty, I am unclear in how we are supposed to find which items are connected to other items without making more scans of the database