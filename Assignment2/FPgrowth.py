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




def main():
    data = Database(file_name)
    global min_sup
    min_sup = int(data.size * sup_percent) #amount of items * sup_percent -> MST

    # JO: testing the changes I made
    fp_tree = FPtree()
    fp_tree.build_table(data, min_sup) # must do this before the build_tree call
    fp_tree.build_tree(data)
    print(fp_tree) # this is to test if things are working, also depends on if I overrode __str__ properly

    tree_root = Node("Root", 0, True)
    for key in reversed(fp_tree.header_table):
        print("Building projected tree for itemset " + str(set(key)))
        link = fp_tree.header_table[key][1]
        tree_header = fp_tree.build_projected_table(link)
        print("    Header table is " + str(tree_header))
      #  proj_tree = FPtree(tree_root, tree_header) # MO i dont need this because the projected tree method is changed

        proj_tree = fp_tree.build_projected_tree(link, min_sup) # MO: since the projected tree makes a new tree instea dof passing it through main now i chnaged the aprameters
        print(proj_tree)
    
    # When I run this, nothing is printed, but no errors. Might have made a mistake in overriding __str__, 
    # could just check by adding print statements in build_table and build_tree, but I am busy for tonight
    # so I'll have to leave it to you guys.


    #in all honesty, I am unclear in how we are supposed to find which items are connected to other items without making more scans of the database
    # JO: We can do it by following the header table hyperlinks, to build the smaller trees, then we just need to store
    # the frequent patterns, and find a way to do it recursively.

if __name__ == "__main__":
    main()