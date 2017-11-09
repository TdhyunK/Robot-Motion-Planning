class search_node:
    # each search node except the root has a parent node
    # and all search nodes wrap a state object
    def __init__(self, state, cost=0, children=None, parent=None):
        self.state = state
        self.children = children
        self.parent = parent
        self.color = "w"
        self.cost = cost


    def __str__(self):
        return "state: " + str(self.state) + "\n" + "children: " + str(self.children) + \
            "\n" + "parent: " + str(self.parent) + "\n"        
    def __lt__(self, other):
        return self.cost < other.cost


    #Returns the state of SearchNode
    def get_state(self):
        return self.state

    #Returns list of children in SearchNode
    def get_children(self):
        return self.children

    #Returns parent node of SearchNode
    def get_parent(self):
        return self.parent

    #Sets the children of the SearchNode
    def set_children(self, children):
        self.children = children

    #Sets the parent of the SearchNode
    def set_parent(self, parent):
        self.parent = parent

