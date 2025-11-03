import sys
from database import Database #unclear why database import is not working
# JO: on my end this import works fine
from FPtree import FPtree

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
    fp_tree.make_header_table(data, min_sup) # must do this before the build_tree call
    fp_tree.build_tree(data)
    print(fp_tree) # this is to test if things are working, also depends on if I overrode __str__ properly
    # When I run this, nothing is printed, but no errors. Might have made a mistake in overriding __str__, 
    # could just check by adding print statements in make_header_table and build_tree, but I am busy for tonight
    # so I'll have to leave it to you guys.


    #in all honesty, I am unclear in how we are supposed to find which items are connected to other items without making more scans of the database
    # JO: We can do it by following the header table hyperlinks, to build the smaller trees, then we just need to store
    # the frequent patterns, and find a way to do it recursively.