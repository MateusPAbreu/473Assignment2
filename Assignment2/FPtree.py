from database import Database
from node import Node

class FPtree:

    def __init__(self, headerTable = None):
        self.root = None
        # JO: Header table is here, Hyperlinks are in the nodes through link_in and link_out
        # The reason header table is optional is because the little trees we recursively build
        # won't need it.
        self.headerTable:dict[frozenset, int, Node] = headerTable if headerTable is not None else {}
        # JO: The structure of header table is like the l_tables from the previous assignment,
        # with the difference being it contains the hyperlink information (The Node that is the
        # first of that item in the tree)


    def buildTree(self, database: Database, minsup):
        self.root = Node("Root", 0, True)
        # Root is empty, then we check database.
        # For each element in our header table, we check if it is in the transaction, if it is
        # we then add it to the tree as needed. I will make this a seperate method probably.
        for transaction in database.transactions:
            for item in self.headerTable:
                if item.issubset(transaction): # JO: I think this works with frozensets
                    self.addToTree(item)

        return self.root
    
    def addToTree(self, item:frozenset):