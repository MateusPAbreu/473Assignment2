class Nodes:
    
    def __init__(self):
        self._root_value = None
        self._root_name = "Root"


    def set_parent(self, parent):   
        self._parent = parent
    
    def get_parent(self):
        return self._parent
    
    def set_child(self, child):
        self._child = child

    def get_child(self): #this one is confusing me, cause we will need to be able to have a parent node that can hold many children... gonna think more about it
        return self._child
    
    def set_value(self, value):
        self._value = value

    def get_value(self):
        return self._value
    
    def set_name(self, name):
        self._name = name

    def get_name(self):
        return self._name
    
    def set_linkIn(self, link_in):
        self._link_in = link_in

    def get_linkIn(self):
        return self._link_in
    
    def set_linkOut(self, link_out):
        self._link_out = link_out

    def get_linkOut(self):
        return self._link_out
    
    def buildTree():
        return None #just to have something and not break the file
        #some sort of loop is necessary
