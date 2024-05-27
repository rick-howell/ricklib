# A class for graph theory operations

class vertex:

    def __init__(self, name, value = None):
        self.name = name
        self.value = value

    def __str__(self):
        if self.value == None:
            return f"{self.name}"
        else:
            return f"{self.name} ({self.value})"
        
    def __eq__(self, other):
        if other == None:
            return False

        if isinstance(other, vertex):
            return self.name == other.name
        else:
            return self.name == other


class edge:

    def __init__(self, v1: vertex, v2: vertex, weight = None, directed = False):
        # If the edge is directed, v1 is the source and v2 is the destination

        self.v1 = v1
        self.v2 = v2
        self.weight = weight
        self.directed = directed

    def get_vertices(self):
        return (self.v1, self.v2)
    
    def get_weight(self):
        return self.weight
    
    def set_weight(self, weight):
        self.weight = weight

    def __str__(self):
        connector = '->' if self.directed else '--'
        if self.weight == None:
            return f"{self.v1.name} {connector} {self.v2.name}"
        else:
            return f"{self.v1.name} {connector} {self.v2.name} ({self.weight})"
    
    def __eq__(self, other):
        if self.directed:
            return self.v1 == other.v1 and self.v2 == other.v2
        else:
            return (self.v1 == other.v1 and self.v2 == other.v2) or (self.v1 == other.v1 and self.v2 == other.v2)

class graph:

    def __init__(self):
        self.V = []
        self.E = []

    def sort_vertices(self):
        self.V.sort(key = lambda x: x.name)

    def sort_edges(self):
        self.E.sort(key = lambda x: (x.v1.name, x.v2.name))

    def add_vertex(self, name = None, value = None):
        # Add a vertex the graph with the given name and value

        if name == None:
            name = str(len(self.V))
        else:
            for v in self.V:
                if v.name == name:
                    raise ValueError(f"Vertex {name} already exists in graph")
        self.V.append(vertex(name, value))
        self.sort_vertices()

    def insert_vertex(self, v: vertex):
        # add a vertex object to the graph

        if v not in self.V:
            self.V.append(v)
            self.sort_vertices()

    def get_vertex(self, v):
        if type(v) == vertex:
            if v in self.V:
                return v
        else:
            v = str(v)
            for vert in self.V:
                if vert.name == v:
                    return vert
            
        raise ValueError(f"Vertex {v} not found in graph")
    
    def remove_vertex(self, name):
        v = self.get_vertex(name)
        if v == None:
            return
        
        self.V.remove(v)
        self.E = [e for e in self.E if e.u != v and e.v != v]
        self.sort_edges()
    
    def contains_edge(self, e):
        for edge in self.E:
            if edge == e:
                return True

    def add_edge(self, v1, v2, weight = None, directed = False):
        v1 = self.get_vertex(v1)
        v2 = self.get_vertex(v2)

        if v1 == None or v2== None:
            raise ValueError("Vertex not found in graph")
        
        e = edge(v1, v2, weight, directed)

        if self.contains_edge(e):
            return
        else:
            self.E.append(e)

        self.sort_edges()

    def get_edge(self, v1, v2):
        v1 = self.get_vertex(v1)
        v2 = self.get_vertex(v2)

        if v1 == None or v2 == None:
            raise ValueError("Vertex not found in graph")

        e1 = edge(v1, v2)

        for e in self.E:
            if e == e1:
                return e
        
        print(f"Edge {v1.name} -> {v2.name} not found in graph")
        return None
    
    def remove_edge(self, v1, v2):
        e = self.get_edge(v1, v2)
        if e == None:
            return
        
        self.E.remove(e)
        self.sort_edges()
    
    def adj_matrix(self):
        n = len(self.V)
        adj = [[0 for _ in range(n)] for _ in range(n)]

        for e in self.E:
            i = self.V.index(e.v1)
            j = self.V.index(e.v2)

            val = 1 if e.weight == None else e.weight
            if e.directed:
                adj[i][j] = val
            else:
                adj[i][j] = val
                adj[j][i] = val
        
        return adj
    
    def print_adj_matrix(self):
        adj = self.adj_matrix()
        for row in adj:
            print(row)
    
    def import_adj_matrix(self, adj, weighted = False):
        '''adj should be a square 2D list'''
        n = len(adj)
        self.V = [vertex(str(i)) for i in range(n)]
        self.E = []

        for i in range(n):
            for j in range(n):
                if adj[i][j] != 0:
                    if weighted:
                        self.add_edge(self.V[i], self.V[j], adj[i][j])
                    else:
                        self.add_edge(self.V[i], self.V[j])

    def nbhd(self, v, closed = False):
        v = self.get_vertex(v)
        if v == None:
            return None
        
        print(f"Neighborhood of {v.name}:")

        g = graph()
        if closed:
            g.insert_vertex(v)
        
        for e in self.E:
            v1, v2 = e.get_vertices()
            if v1 == v:
                g.insert_vertex(v2)
            elif v2 == v:
                g.insert_vertex(v1)

        for e in self.E:
            v1, v2 = e.get_vertices()
            if v1 in g.V and v2 in g.V:
                g.add_edge(v1, v2, e.get_weight(), e.directed)
            
        return g


    def det(self):
        # Return the determinant of the adjacency matrix of the graph
        
        adj = self.adj_matrix()
        n = len(adj)
        

    def __str__(self):
        s = f'Graph with {len(self.V)} vertices and {len(self.E)} edges\n\n'

        s += "Vertices:\n"
        for v in self.V:
            s += f"{v}\n"
        
        s += "\nEdges:\n"
        for e in self.E:
            s += f"{e}\n"
        
        return s
    

