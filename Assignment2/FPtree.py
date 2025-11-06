from database import Database
from node import Node

class FPtree:
    def __init__(self, root = None, headerTable = None):
        self.root = root if root is not None else None
        # JO: Header table is here, Hyperlinks are in the nodes through link_in and link_out
        # The reason header table is optional is because the little trees we recursively build
        # won't need it.
        self.header_table:dict[frozenset, tuple[int, Node]] = headerTable if headerTable is not None else {}
        # JO: The structure of header table is like the l_tables from the previous assignment,
        # with the difference being it contains the hyperlink information (The Node that is the
        # first of that item in the tree) bundled with the count in a tuple. 
        # Ex: to get item a's count, you do headerTable[frozenset(['a'])][0]. This is ugly though,
        # so we are more likely to iterate through header table items. Probably using for each.

    def str_helper(self, node:Node , children_string:str):
        if (not node.get_children() == []):
            for child in node.get_children():
                children_string += str(child) + "  " 
            children_string += "\n"
            for child in node.get_children():
                children_string = self.str_helper(child, children_string)

        return children_string

    def __str__ (self):
        header_table_string = "Header table: \n" + "\n".join([str(set(item)) +"| "+str(self.header_table[item][0]) for item in self.header_table])
        children_string = "\n[ROOT] \n" 
        children_string = self.str_helper(self.root, children_string)
        return header_table_string + children_string

    # JO: I built this with constructing the first FP tree in mind, it probably isn't gonna work to build
    # all the little trees recursively. We could modify it to make the database optional and then do checks
    # inside to see if we are building the main tree or a conditional tree, or we could just make a new
    # method for building the smaller trees (this is what I suggest).
    def build_tree(self, database: Database):
        self.root = Node("Root", 0, True)
        # Root is empty, then we check database.
        # For each element in our header table, we check if it is in the transaction, if it is
        # we then add it to the tree as needed. This looks like checking the children of root,
        # if the item is there, increment its count, if not add it as a new child with count 1.
        # then the next item you add is added as a child of the previous element added, until the
        # transaction is done.
        for transaction in database.transactions:
            current_root = self.root # JO: I think the issue is this update needs to go somewhere else
            for item in self.header_table:
                if item.issubset(transaction): 
                    if(current_root.get_children() == []): # no children yet
                        new_node = Node(item, 1)
                        current_root.set_child(new_node)
                        self.header_table[item] = (self.header_table[item][0], new_node)
                        current_root = new_node
                    else:
                        child_found = False
                        for child in current_root.get_children():
                            if not child_found:
                                if child.get_name() == item:
                                    current_root = child 
                                    child_found = True
                                    child.set_value(child.get_value() + 1)

                        if not child_found:
                            new_node = Node(item, 1)
                            current_root.set_child(new_node)
                            current_root = new_node
                            # Now we need to update the header table to add this new node's hyperlink
                            if self.header_table[item][1] is None: # no hyperlink
                                self.header_table[item] = (self.header_table[item][0], new_node)
                            else:
                                # There are already hyperlinks, so we need to traverse to the end and add it
                                current_node = self.header_table[item][1]
                                while current_node.get_linkOut() is not None: # Loop runs while currentNode is not the last hyperlink
                                    current_node = current_node.get_linkOut()
                                current_node.set_linkOut(new_node)
                                new_node.set_linkIn(current_node)
        # This is pretty nested and yucky, if you can think of a nicer way to refactor, go for it.
        # Could break it into helper methods, like I was gonna with addToTree, but then you have to pass around
        # information and it just feels worse.

        return self.root
    

    # JO: Made more sense to have the header table creation inside the FPtree class. This does basically
    # the same thing as the previous assignment, then just changes the structure to fit the header table.
    def make_header_table(self, database: Database, min_sup: int):
        # Code from last assignment, makes a c table
        c_table:dict[frozenset, int] = {}
        for transaction in database.transactions:
            for item in transaction:
                key = frozenset([item])
                c_table[key] = c_table.get(key, 0) + 1

        # Code from last assignment, makes l table from c table
        l_table: dict[frozenset, int] = {}
        for item in c_table:
            if (c_table[item] >= min_sup):
                l_table[item] = c_table[item]

        # Now we need to convert l_table to header table
        l_table = dict(sorted(l_table.items(), key=lambda x: x[1], reverse=True)) # I've used this in other assignments,
            # but it basically just sorts l table in reverse order based on the count (which is specified through the key)
        
        for item in l_table:
            self.header_table[item] = (l_table[item], None) # None is placeholder for hyperlink Node
        
    