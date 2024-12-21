import pandas as pd
import numpy as np


class Transaction:

    def __init__(self, next, distance):
        self.next = next
        self.distance = distance

class Node:

    def __init__(self, name, straight_line_distance):
        self.name = name
        self.straight_line_distance = straight_line_distance
        self.transactions = list()


class CitiesTree:

    def __init__(self, start_node_name):
        self.start_node_name = start_node_name
        self.start = None

    def createTree(self, city_data, nodes):
        for node in nodes:
            line = np.array(city_data.loc[city_data["City Name"] == node.name])
            destinations_dict = dict({})
            for i in range(2,6):
                str = line[0,i]
                if str != "null":
                    name, distance = str.split('-')
                    destinations_dict[name] = distance
                else: continue
            for temp_node in nodes:
                if temp_node.name in destinations_dict.keys():
                    node.transactions.append(Transaction(temp_node,destinations_dict[temp_node.name]))

        for node in nodes:
            if node.name.strip() == self.start_node_name:
                self.start = node
                break

    def printTree(self):
        visited_list = list()
        self.print_node(self.start, visited_list)

    def print_node(self, node, visited_list):
        if node in visited_list:
            return
        print(f"{node.name}: {node.straight_line_distance}")
        visited_list.append(node)
        for transaction in node.transactions:
            if transaction is not None:
                self.print_node(transaction.next, visited_list)

    def A_star_find_path(self, end_node):
        fringe = dict({self.start: 366})
        g_n = {self.start: 0}
        ptr = self.start
        while 1 == 1:
            for transaction in ptr.transactions:
                next_node = transaction.next
                distance = int(transaction.distance)

                # f(n) = g(n) + h(n) hesapla
                tentative_g_n = g_n[ptr] + distance
                f_n = tentative_g_n + int(next_node.straight_line_distance)

                if next_node not in g_n or tentative_g_n < g_n[next_node]:
                    g_n[next_node] = tentative_g_n
                    fringe[next_node] = f_n

            del fringe[ptr]

            if not fringe:
                print("Yol bulunamadı!")
                return None

            ptr = min(fringe, key=fringe.get)
            if ptr == end_node:
                break
        print(f"Optimal yol maliyeti: {g_n[end_node]}")
        return g_n[end_node]

def read_from_file(filename):
    dataFrame = pd.read_excel(filename)
    df_lower = dataFrame.map(lambda x: x.lower() if isinstance(x, str) else x)
    df_lower_columns = df_lower.columns
    df_cities = df_lower[[df_lower_columns[0], df_lower_columns[1]]]
    return df_cities, df_lower

def create_cities_node_list(cities):
    node_list = list()
    np_cities = np.array(cities)
    for city in np_cities:
        node_list.append(Node(city[0], city[1]))
    return node_list

def main():
    cities, data = read_from_file("Cities.xlsx")
    nodes = create_cities_node_list(cities)
    tree = CitiesTree("arad")
    tree.createTree(data, nodes)
    tree.A_star_find_path(nodes[1])

if __name__ == "__main__":
    main()