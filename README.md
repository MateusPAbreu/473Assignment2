# CPSC473_a2_Mojoma_Rockets
This is a repository to track code changes for the FP-Growth Algorithm for frequent pattern mining on a transaction databases. It identifies frequent itemsets that meet a user indicated minimum support threshold. 

#Course #: CPSC 473- Introduction to Data Mining\
#School#: University Of Northern British Columbia(UNBC)\
#Semester# : Fall 2025\
#Assignment 2#

### Team Members
1. **Josh Holuboch**
2. **Mateus de Abreu**
3. **Muhammad Olaniyan**


### **If you wish to run the code** :
1. Navigate to the directory of the "CPSC473_a2_Mojoma_Rockets"
2. Insert the command py FPgrowth.py "data file name" "minimum support threshold percent"

        ex:

        a. py FPgrowth.py connect.txt 99

        b. py FPgrowth.py data.txt 50

        c. py FPgrowth.py 1k5L.txt 60

        d. py FPgrowth.py t25i10d10k.txt 60

3. The output should appear shortly afterwards with the corresponding output file created/updated 


### **Algorithm Overview**:

1. Scan Database to get support for each item.
2. Generate frequent 1 items or L1.
3. Build a header table from this L1 table, that contains the items in sorted order and a hyperlink.
4. Using this header table and the database, build the first general FP-tree and connect the hyperlinks. 
5. Recursively iterate from the bottom of the header table:
   i. for each item, create a specific FP-tree (this represents size 2 itemsets)
   ii. on this Fp-tree, further recurse to build any possible trees
6. Collect all the information from the trees and report the frequent patterns.
