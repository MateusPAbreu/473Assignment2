import sys
from database import Database #unclear why database import is not working
# JO: on my end this import works fine
from FPtree import FPtree
from node import Node

file_name = sys.argv[1] #this is the file path we will be opening
sup = int(sys.argv[2]) #minimum support
sup_percent = sup/100
min_sup = 0
data:Database

def build_projected_table(node:Node):
    current_link = node
    itemset_headertable: dict[frozenset, tuple[int, Node]] = {}
    # Make a little header table for each itemset
    while current_link is not None:
        current_node = current_link
        while not current_node.parent.isRoot:
            current_node = current_node.parent
            print("-working with " + str(current_node))
            if (current_node.name not in itemset_headertable):
                itemset_headertable[current_node.name] = (1, None)
            else:
                itemset_headertable[current_node.name] = ((itemset_headertable[current_node.name][0] + 1), None)
        print("  Current link is "+ str(current_link) + ", link out is " + str(current_link.link_out) + ", link in is " + str(current_link.link_in))
        current_link = current_link.link_out

    return itemset_headertable

def build_projected_tree(tree:FPtree, node:Node):
    temp_stack = []
    itemset_headertable = tree.header_table

    current_link = node
    while current_link is not None:
        current_node = current_link
        while not current_node.parent.isRoot:
            temp_node = current_node.parent
            temp_node.set_value(current_node.get_value())
            current_node = temp_node
            if (itemset_headertable[current_node.name][0] > min_sup):
                temp_stack.append(current_node)
        current_link = current_link.link_out

    # Add all of our stack items to a new projected tree
    current_root = tree.root
    while(len(temp_stack) > 0):
        print("adding item " + str(item))
        item = temp_stack.pop()
        child_found = False
        if(current_root.get_children() == []): # no children yet
            current_root.set_child(item)
            itemset_headertable[item] = (itemset_headertable[item][0], item)
            current_root = item
        else:
            for child in current_root.get_children():
                if child.get_name() == item.get_name():
                    current_root = child 
                    child_found = True
                    child.set_value(child.get_value() + item.get_value())

        if (not child_found):
            current_root.set_child(item)
            itemset_headertable[item] = (itemset_headertable[item][0], item)
            current_root = item

        if itemset_headertable[item][1] is None: # no hyperlink
            itemset_headertable[item] = (itemset_headertable[item][0], item)
        else:
            # There are already hyperlinks, so we need to traverse to the end and add it
            current_node = itemset_headertable[item][1]
            while current_node.get_linkOut() is not None: # Loop runs while currentNode is not the last hyperlink
                current_node = current_node.get_linkOut()
            current_node.set_linkOut(item)
            item.set_linkIn(current_node)

    return FPtree(tree.root, itemset_headertable)


def main():
    data = Database(file_name)
    global min_sup
    min_sup = int(data.size * sup_percent) #amount of items * sup_percent -> MST

    # JO: testing the changes I made
    fp_tree = FPtree()
    fp_tree.make_header_table(data, min_sup) # must do this before the build_tree call
    fp_tree.build_tree(data)
    print(fp_tree) # this is to test if things are working, also depends on if I overrode __str__ properly

    tree_root = Node("Root", 0, True)
    for key in reversed(fp_tree.header_table):
        print("Building projected tree for itemset " + str(set(key)))
        link = fp_tree.header_table[key][1]
        tree_header = build_projected_table(link)
        print("    Header table is " + str(tree_header))
        proj_tree = FPtree(tree_root, tree_header)

        proj_tree = build_projected_tree(proj_tree, link)
        print(proj_tree)
    
    # When I run this, nothing is printed, but no errors. Might have made a mistake in overriding __str__, 
    # could just check by adding print statements in make_header_table and build_tree, but I am busy for tonight
    # so I'll have to leave it to you guys.


    #in all honesty, I am unclear in how we are supposed to find which items are connected to other items without making more scans of the database
    # JO: We can do it by following the header table hyperlinks, to build the smaller trees, then we just need to store
    # the frequent patterns, and find a way to do it recursively.

if __name__ == "__main__":
    main()