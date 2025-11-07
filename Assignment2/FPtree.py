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

    def connect_hyperlinks(self, node: Node):
        item = node.name
        if self.header_table[item][1] is None: # no hyperlink
            self.header_table[item] = (self.header_table[item][0], node)
        else:
            # There are already hyperlinks, so we need to traverse to the end and add it
            current_node = self.header_table[item][1]
            print(str(current_node))
            print(str(current_node.get_linkOut()))
            while current_node.get_linkOut() is not None: # Loop runs while currentNode is not the last hyperlink
                current_node = current_node.get_linkOut()
            current_node.set_linkOut(node)
            node.set_linkIn(current_node)

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
                        new_node.parent=current_root
                        current_root.set_child(new_node)
                       # bugbugbug self.header_table[item] = (self.header_table[item][0], new_node) if this happens befor connect_hyperlinks the condition will fail in the method
                        self.connect_hyperlinks(new_node)
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
                            new_node.parent=current_root
                            current_root.set_child(new_node)
                            current_root = new_node
                            self.connect_hyperlinks(new_node)
                    
        # This is pretty nested and yucky, if you can think of a nicer way to refactor, go for it.
        # Could break it into helper methods, like I was gonna with addToTree, but then you have to pass around
        # information and it just feels worse.

        return self.root
    

    # JO: Made more sense to have the header table creation inside the FPtree class. This does basically
    # the same thing as the previous assignment, then just changes the structure to fit the header table.
    def build_table(self, database: Database, min_sup: int):
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
        
    # This method doesn't work perfectly yet, it is highly couple with the build_projected_tree method
    # to accomplish any work. This is because it doesn't do any pruning in this method, it just grabs
    # every single count of all seen items and adds them to a header table. Pruning shouuuuld happen in this
    # method, then the build_projected_tree method should be refactored. 
    def build_projected_table(self,node:Node):
        current_link = node
        itemset_headertable: dict[frozenset, tuple[int, Node]] = {}
        # Make a little header table for each itemset
        while current_link is not None:
            current_node = current_link
            base_count= current_node.get_value() # this is the actual support amount of the item we are making the projected tree for
            while not current_node.parent.isRoot:
                current_node = current_node.parent
                print("-working with " + str(current_node))
                # i changed this part because when traversing up the tree for a given itemset proj. tree we need to count the basecount of the item not "1"
                if (current_node.name not in itemset_headertable):
                    itemset_headertable[current_node.name] = (base_count, None)
                else:
                    itemset_headertable[current_node.name] = ((itemset_headertable[current_node.name][0] + base_count), None) # I also added the base count here
            print("  Current link is "+ str(current_link) + ", link out is " + str(current_link.link_out) + ", link in is " + str(current_link.link_in))
            current_link = current_link.link_out

        return itemset_headertable
    

    # This method should be refactored to make use of the connect_hyperlinks method, in the exact same way
    #MO that is what i am trying to do now
    # that build tree does.
    def build_projected_tree(self, node: Node, min_sup: int):
        # Step 1: Get the items from the node you are checking till the root  it has a format :{'1': (3, None), '2': (5, None), '4': (3, None)}

        conditional_header = self.build_projected_table(node)
        
        # Step 2: I am pruning things here
        filtered_header = {}
        # i am pattern matching the contents of the headertable and discarding the link because it will be None
        for item, (count, _) in conditional_header.items():
            if count >= min_sup:
                filtered_header[item] = (count, None)
        
        # Step 3: Sort by count
        sorted_items = sorted(filtered_header.keys(), 
                            key=lambda x: filtered_header[x][0], # i wanted to use a method but goggle suggested a lambda expression
                            reverse=True) # this makes it organized form highest to lowest, i think itw as used above to vonver to header table
        
        sorted_header= {item: filtered_header[item] for item in sorted_items}
        
        # Step 4: Create empty projected tree (just to make it easier to think about it, i dont want to mxi it with something)
        new_root = Node("Root", 0, True)
        new_tree = FPtree(new_root, sorted_header)
        
        # Step 5: Process each occurrence of target item
        current_link = node
        while current_link is not None:
            # Get the count for this path till the root
            path_count = current_link.get_value()
            
            # Collect p items (bottom-up)
            p = []
            parent = current_link.parent
            while not parent.isRoot:
                if parent.name in sorted_header:  # if it is a frequent node 
                    p.append(parent.name) # put it in the list
                parent = parent.parent
            
            # Reverse to get top-down order
            p.reverse()
            
            # Insert this prefix path into new tree
            self._insert_path(new_tree, p, path_count)
            
            # Move to next hyperlinked node
            current_link = current_link.get_linkOut()
        
        return new_tree

    # def sort_key(x):
    #  return filtered_header[x][0]

    def _insert_path(self, tree: FPtree, path: list, count: int):
    
        current = tree.root
        
        for item in path:
            # Check if item already exists as child
            found = False
            for child in current.get_children():
                if child.get_name() == item:
                    # Item exists - add count
                    child.set_value(child.get_value() + count)
                    current = child
                    found = True
                    break # sorry terry
            
            # Item not found  so create new node
            if not found:
                new_node = Node(item, count)
                new_node.parent = current
                current.set_child(new_node)
                tree.connect_hyperlinks(new_node)
                current = new_node

    def mining(self, stuff:frozenset, min_sup)  :
        # this method will happen recursively wehere a projected tree will be made
        patterns=[] # this list will fill the patterns of the frequent itemsets.
        stuff= frozenset()
        #stuff is the pattern that we are checking to see if it is a frequent, everytime we make a projected tree for it, if it has not reached the base case of length 0-1 tree we make a new pattern and try again
         
        for item in (list(self.header_table.keys())).reverse : # this is a revered list of the header table
         new_pattern= item.union(stuff)
         #---> Here i want to add the new pattern to the patterns list because the previosu pattern did not reach the base case and we are checkign the next , perhaps append. ....
        sup= self.header_table[item][0]

        new_tree=  self.build_projected_tree(self.header_table[item][1],min_sup) # this is building the tree for
        # if not len(new_tree.header_table.items)  <= 1:  
        #     # if so the cnew tree should be mined with the new pattern as  the stuff
        #     # # whatever you result should be added to the lsit of patterns
        #     # # i hope these kind of help🤔
        # else: