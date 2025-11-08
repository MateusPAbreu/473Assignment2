import sys
from database import Database
from FPtree import FPtree
import time

file_name = sys.argv[1]
sup = int(sys.argv[2])
sup_percent = sup / 100

def main():
    data = Database(file_name)
    min_sup = int(data.size * sup_percent)
    
    start_time = time.time()
    
    # Build FP-tree
    fp_tree = FPtree()
    fp_tree.build_table(data, min_sup)
    fp_tree.build_tree(data)
    
    # Mine patterns
    result = fp_tree.mining(frozenset(), min_sup)
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    
    print(f"minsup = {sup}% = {min_sup}")
    print(f"|FPs| = {len(result)}")
    print(f"Total Runtime: {elapsed_time:.3f} sec")
    
   
    output_file = f"MiningResult_{file_name}"
    with open(output_file, "w") as file:
        file.write(f"|FPs| = {len(result)}\n")
        for pattern, support in result:
            file.write(f"{set(pattern)} : {support}\n")

if __name__ == "__main__":
    main()