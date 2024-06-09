import glib

v1 = glib.vertex('A')
v2 = glib.vertex('B')

e1 = glib.edge(v1, v2, directed = True)
e2 = glib.edge(v2, v1, directed = True)

print(e1 == e2)

g1 = [
    [0, 0, 1, 1],
    [0, 0, 1, 1],
    [1, 1, 0, 1],
    [1, 1, 1, 0],
]

g = glib.graph()
g.import_adj_matrix(g1)

print(g)

print(g.get_vertex(0))

g.print_adj_matrix()

print(g.get_edge(0, 3) == g.get_edge(3, 0))

print('\n\n Adding a vertex\n\n')
g.add_vertex()
g.add_edge(0, 4)

print(g)

g.print_adj_matrix()

print('\n\nGetting NBHD\n\n')

print(g.nbhd(0))
print(g.nbhd(0, closed=True))

print('\n\nRemoving vertex 4\n\n')
g.remove_vertex(4)

g.print_adj_matrix()


h1 = glib.graph()
h1_graph = [
    [0, 1, 1, 1, 1],
    [1, 0, 0, 0, 0],
    [1, 0, 0, 0, 0],
    [1, 0, 0, 0, 0],
    [1, 0, 0, 0, 0],
]

h1.import_adj_matrix(h1_graph)

print('#_____________________________________________')

filename = 'g0g1.mat'
graphs = glib.load_mat_file(filename)

g = graphs[0]
g.print_adj_matrix()