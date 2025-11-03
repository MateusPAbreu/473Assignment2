class Node:

    def __init__(self, name:frozenset, value = None, isRoot = False): # JO: added default values
        self.name = name
        self.value = value
        self.isRoot = isRoot
        self.parent = None
        self.link_in: Node = None
        self.link_out: Node = None

        self.children: list[Node] = []

    def __str__(self):
        return "Node(" + str(self.name) + ", " + str(self.value) + ")"

    def set_root(self, state):
       self.isRoot = state

    def set_parent(self, parent):   
        self.parent = parent
    
    def get_parent(self):
        return self.parent
    
    def set_child(self, child: "Node"): # JO: weird looking, python allows 'type hinting' to reference the same class.
        child.set_parent(self)
        self.children.append(child)

    def get_children(self): #this one is confusing me, cause we will need to be able to have a parent node that can hold many children... gonna think more about it
        # MO: i think i fixed it, the root will have many children in alist while a child will only have one
        # JO: each child might also have many children, so they should return a list too.
        return self.children
    
    def set_value(self, value:int):
        self.value = value

    def get_value(self):
        return self.value
    
    def set_name(self, name:frozenset):
        self.name = name

    def get_name(self):
        return self.name
    
    def set_linkIn(self, link_in):
        self.link_in = link_in

    def get_linkIn(self):
        return self.link_in
    
    def set_linkOut(self, link_out):
        self.link_out = link_out

    def get_linkOut(self):
        return self.link_out
    