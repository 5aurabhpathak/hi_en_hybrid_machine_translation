#!/bin/env python3
#Author: Saurabh Pathak
''' Word based suffix tree for corpus using Ukkonen's algorithm.
    Will be used to create a suffix array in linear time.
    Based on an explanation of the algorithm from here: http://stackoverflow.com/questions/9452701/ukkonens-suffix-tree-algorithm-in-plain-english
'''
main = __name__ == '__main__'

class _Pointer:
    '''Creates a pointer object to a corpus position'''
    def __init__(self, p): self.value = p.value if isinstance(p, _Pointer) else p

    if main:
        def __str__(self): return str(self.value)

class _Edge:
    '''Represents an edge of the suffix tree'''
    def __init__(self, beg, end, to_vertex=None):
        assert isinstance(beg, _Pointer) and isinstance(end, _Pointer), 'not a pointer while defining an edge'
        assert to_vertex is None or isinstance(to_vertex, _Node), 'to_vertex not None or _Node'
        self.beg, self.end, self.to_vertex = beg, end, to_vertex

class _Node:
    '''Represents a node of the suffix tree'''
    def __init__(self, parent=None, suffix=None, edges=None):
        assert parent is None or isinstance(parent, _Node), 'parent is not null or a _Node'
        if edges is None: edges = {}
        self.edges, self.parent, self.suffix = edges, parent, suffix
        if main: self.handle, self.edgehandles = pydot.Node(str(id(self))), {}

    def add_edge(self, word, end, beg=None, to_vertex=None):
        if beg is None: beg = _Pointer(end)
        self.edges.update({word : _Edge(beg,end,to_vertex)})
        if main: self.edgehandles.update({self.edges[word] : pydot.Edge(self.handle, pydot.Node(str(id(self.edges.get(word)))) if to_vertex is None else to_vertex.handle, label=word)})

class SuffixTree:
    def __init__(self, string):
        '''constructs a word based suffix tree out of string'''
        temp = string.split()
        assert not main or len(temp) == 1, 'tests are character based for better visualization. Dont use spaces.'
        self.__string = string if main else temp # <-- actually, a list
        self.__cur, self.__nodes, self.__remainder = _Pointer(-1), [_Node()], 0
        self.__active_node, self.__active_edge, self.__active_length = self.__nodes[0], None, 0
        if main:
            self.__graph = pydot.Dot(graph_type='digraph')
            self.__graph.set_node_defaults(label='', height=.1, width=.1)
            self.__graph.set_edge_defaults(arrowsize=.5)
            self.__graph.set_graph_defaults(rankdir='LR')
        self.__construct_tree()

    def __construct_tree(self):
        for word in self.__string:
            self.__cur.value += 1
            self.__remainder += 1
            if main:
                for node in self.__nodes:
                    for edge, edgehandle in node.edgehandles.items():
                        if edge.to_vertex is None: edgehandle.set_label(edgehandle.get_attributes()['label']+word)
            stop, self.__prev_node = False, None
            while not stop and self.__remainder > 0:
                edge = self.__active_node.edges.get(self.__active_edge)
                if self.__insertable(word, edge):
                    if self.__remainder == 1 and self.__active_length == 0:
                        self.__active_node.add_edge(word, self.__cur)
                        self.__remainder = 0
                        self.__active_edge = None
                        if main: self.__graph.add_edge(self.__active_node.edgehandles[self.__active_node.edges[word]])
                    else: self.__split_insert(word, edge)
                else:
                    if main: print(word, 'skipped')
                    stop = True
                    if self.__active_length == 0:
                        self.__active_edge = word
                        edge = self.__active_node.edges.get(word)
                    self.__active_length += 1
                    if edge.to_vertex is not None: self.__adjust_active_point(edge)
                if main:
                    print(self.__show_active_point())
                    self.__graph.write_png('%s%s%d.png' %(self.__cur, word, self.__remainder))

    def __insertable(self, word, edge):
        '''checks if current word is insertable or should be skipped'''
        if self.__active_node.edges.get(word) is None: return True
        return edge is not None and self.__string[edge.beg.value + self.__active_length] != word

    def __split_insert(self, word, edge):
        '''splits an edge at the active length and then inserts the suffix'''
        newnode = _Node(self.__active_node)
        self.__nodes += newnode,
        newnode.add_edge(word, self.__cur)
        begpos = edge.beg.value + self.__active_length
        newnode.add_edge(self.__string[begpos], edge.end, _Pointer(begpos), edge.to_vertex)
        if main: seglabel = self.__string[begpos:edge.end.value+1]
        edge.end, edge.to_vertex = _Pointer(edge.beg.value + self.__active_length - 1), newnode
        self.__remainder -= 1
        if main:
            oldedge = self.__active_node.edgehandles[edge]
            self.__graph.del_edge(oldedge.get_source(), oldedge.get_destination())
            newedge = self.__active_node.edgehandles[edge] = pydot.Edge(self.__active_node.handle, newnode.handle, label=oldedge.get_attributes()['label'][:self.__active_length])
            del oldedge
            self.__graph.add_edge(newedge)
            self.__graph.add_edge(newnode.edgehandles[newnode.edges[word]])
            newedge = newnode.edgehandles[newnode.edges[self.__string[begpos]]]
            newedge.set_label(seglabel)
            self.__graph.add_edge(newedge)
        #apply applicable rules
        #rule 1
        if self.__active_node.parent is None:
            self.__active_edge = self.__string[self.__cur.value - self.__remainder + 1]
            if self.__active_length > 0: self.__active_length -= 1
            if main: print('rule 1 applied', self.__show_active_point())
        #rule 3 (not a typo)
        else:
            if self.__active_node.suffix is not None: self.__active_node = self.__active_node.suffix
            else: self.__active_node = self.__nodes[0]
            self.__adjust_active_point(edge)
            if main: print('rule 3 applied', self.__show_active_point())
        #rule 2
        if self.__prev_node is not None:
            self.__prev_node.suffix = newnode
            if main:
                self.__graph.add_edge(pydot.Edge(self.__prev_node.handle, newnode.handle, style='dotted'))
                print('rule 2 applied', self.__show_active_point())
        self.__prev_node = newnode

    def __adjust_active_point(self, oldedge):
        edge = self.__active_node.edges.get(self.__active_edge)
        while edge.beg.value + self.__active_length > edge.end.value + 1:
            self.__active_node = oldedge.to_vertex
            self.__active_edge = self.__string[edge.end.value + 1]
            self.__active_length -= edge.end.value - edge.beg.value + 1
            oldedge, edge = edge, self.__active_node.edges.get(self.__active_edge)

    if main:
        def __show_active_point(self): return '(%s, %s , %d)' %(self.__active_node, 'None' if self.__active_edge is None else self.__active_edge, self.__active_length)

if main:
    import pydot
    SuffixTree(input())
