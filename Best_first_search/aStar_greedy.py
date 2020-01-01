from queue import PriorityQueue

class Node:
    def __init__(self, city, visited, distance):
        self.city = city
        self.visited = visited
        self.distance = distance

def get_neighbour_cities(city, distances):
    cities = []
    for cityA, cityB in distances:
        if cityA == city:
            cities.append((cityB, distances[cityA, cityB]))
        elif cityB == city:
            cities.append((cityA, distances[cityA, cityB]))

    return cities

def find_path_greedy(start: str, distances, sld):
    pq = PriorityQueue()
    pq.put((sld[start], Node(start, [start], 0)))  # Initial state

    while not pq.empty():
        parent_node = pq.get()[1]   # get highest priority node (lowest sld)

        if parent_node.city == 'Valladolid':
            return parent_node

        for city, dist in get_neighbour_cities(parent_node.city, distances):
            if city not in parent_node.visited:
                new_visited = list(parent_node.visited)
                new_visited.append(city)

                node = Node(city,
                            new_visited,
                            parent_node.distance + dist)

                pq.put((sld[city], node))
    
    # No solution found
    return None

def find_path_aStar(start: str, distances, sld):
    pq = PriorityQueue()
    pq.put((sld[start], Node(start, [start], 0)))  # Initial state

    while not pq.empty():
        parent_node = pq.get()[1] # get highest priority node (lowest estimated total cost from n to goal)
        
        if parent_node.city == 'Valladolid':
            return parent_node

        for city, dist in get_neighbour_cities(parent_node.city, distances):
            if city not in parent_node.visited:
                new_visited = list(parent_node.visited)
                new_visited.append(city)

                node = Node(city,
                            new_visited,
                            parent_node.distance + dist)

                # g(n) = node.distance, h(n) = sld(node.city)
                pq.put((node.distance + sld[node.city], node))

    # No solution found
    return None

def read_file(file_path, distances, straight_line_distances):
    file = open(file_path, 'r')
    lines = file.readlines()

    for line in lines[5:82]:
        a, b, dist = line.split(' ')
        distances[(a, b)] = int(dist)

    for line in lines[85:134]:
        city, dist = line.split(' ')
        straight_line_distances[city] = int(dist)

def main():
    distances = {}                  # distance between cities
    straight_line_distances = {}    # Straight line distances to Valladolid

    read_file('cities_map', distances, straight_line_distances)

    # Greedy Best-first
    path = find_path_greedy('Malaga', distances, straight_line_distances)
    if path:
        print('Greedy Best-first:\n{}\nDistance traveled: {}\n'.format(path.visited, path.distance))
    else:
        print('Greedy Best-first: No solution found\n')

    # A*
    path = find_path_aStar('Malaga', distances, straight_line_distances)
    if path:
        print('A*:\n{}\nDistance traveled: {}\n'.format(path.visited, path.distance))
    else:
        print('A*: No solution found\n')

if __name__ == '__main__':
   main()