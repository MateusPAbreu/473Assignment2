from database import Database
from node import Node

class FPtree:

    def __init__(self, headerTable = None):
        self.root = None
        # JO: Header table is here, Hyperlinks are in the nodes through link_in and link_out
        # The reason header table is optional is because the little trees we recursively build
        # won't need it.
        self.headerTable:dict[frozenset, tuple[int, Node]] = headerTable if headerTable is not None else {}
        # JO: The structure of header table is like the l_tables from the previous assignment,
        # with the difference being it contains the hyperlink information (The Node that is the
        # first of that item in the tree) bundled with the count in a tuple. 
        # Ex: to get item a's count, you do headerTable[frozenset(['a'])][0]. This is ugly though,
        # so we are more likely to iterate through header table items. Probably using for each.


    def buildTree(self, database: Database, minsup):
        self.root = Node("Root", 0, True)
        # Root is empty, then we check database.
        # For each element in our header table, we check if it is in the transaction, if it is
        # we then add it to the tree as needed. This looks like checking the children of root,
        # if the item is there, increment its count, if not add it as a new child with count 1.
        # then the next item you add is added as a child of the previous element added, until the
        # transaction is done.
        for transaction in database.transactions:
            for item in self.headerTable:
                if item.issubset(transaction): 
                    for child in self.root.get_children():
                        if child.get_name() == item:
                            child.set_value(child.get_value() + 1)
                            break # don't need to keep looking
                        else:
                            newNode = Node(item, 1)
                            self.root.set_child(newNode)
                            # Now we need to update the header table to add this new node's hyperlink
                            if self.headerTable[item][1] is None: # no hyperlink
                                self.headerTable[item] = (self.headerTable[item][0], newNode)
                            else:
                                # There are already hyperlinks, so we need to traverse to the end and add it
                                currentNode = self.headerTable[item][1]
                                while currentNode.get_linkOut() is not None: # Loop runs while currentNode is not the last hyperlink
                                    currentNode = currentNode.get_linkOut()
                                currentNode.set_linkOut(newNode)
                                newNode.set_linkIn(currentNode)
        # This is pretty nested and yucky, if you can think of a nicer way to refactor, go for it.
        # Could break it into helper methods, like I was gonna with addToTree, but then you have to pass around
        # information and it just feels worse.

        return self.root
    