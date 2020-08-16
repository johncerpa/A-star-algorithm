from collections import deque,defaultdict

class Graph:
    def __init__(self, adjacency_list):
        self.adjacency_list = adjacency_list
        self.heuristic = self.create_heuristic()

    def get_neighbors(self, v):
        return self.adjacency_list[v]

    def create_heuristic(self):
        heuristic = defaultdict(int)
        for i in self.adjacency_list:
            minor = 9999999999        
            for (n, w) in self.adjacency_list[i]:
                if w < minor:
                    minor = w
            heuristic[i] = minor
        return heuristic
        
    def h(self, n):
        return self.heuristic[n]

    def a_star_algorithm(self, start_node, stop_node):
        open_list = set([start_node])
        closed_list = set([])

        g = {}
        g[start_node] = 0

        parents = {}
        parents[start_node] = start_node

        while len(open_list) > 0:
            n = None

            for v in open_list:
                if n == None or g[v] + self.h(v) < g[n] + self.h(n):
                    n = v

            print('Current node', n)
            print('g(n) =', g[n], ' h(n) =', self.h(n), ' f(n) =', g[n] + self.h(n))

            if n == None:
                return None

            if n == stop_node:
                path_found = []

                while parents[n] != n:
                    path_found.append(n)
                    n = parents[n]

                path_found.append(start_node)
                path_found.reverse()

                return path_found

            
            for (m, weight) in self.get_neighbors(n):                
                if m not in open_list and m not in closed_list:
                    open_list.add(m)
                    parents[m] = n
                    g[m] = g[n] + weight
                else:
                    if g[m] > g[n] + weight:
                        g[m] = g[n] + weight
                        parents[m] = n

                        if m in closed_list:
                            closed_list.remove(m)
                            open_list.add(m)

            open_list.remove(n)
            closed_list.add(n)

        return None
