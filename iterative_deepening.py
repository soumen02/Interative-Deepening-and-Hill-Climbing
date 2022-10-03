import random

# ENTER INPUT FILE PATH HERE
input_name = '/Users/soumenmohanty/Documents/Fall-2022/Artificial-Intelligence/Programming-Assignment-1/input.txt'
input_file = open(input_name, 'r' )

# parsing input file
line1 = input_file.readline().strip().split(' ')

budget = int(line1[0])
output_type = line1[1]

# putting file in a list
nodes_edges = input_file.read().split('\n\n')
string_nodes = nodes_edges[0].split('\n')
string_edges = nodes_edges[1].split('\n')

EDGES = []

# appending edges to a list
for i in string_edges:
    temp = i.split(' ')
    EDGES.append(temp)

# creating a dictionary of nodes where each element is a node object
nodes_list = {}

class Node:
    def __init__(self, name, cost):
        self.name = name
        self.cost = cost
        self.edges = []

# iterating through list and creating node objects
for i in string_nodes:
    node_value = i.split(' ')
    new_node = Node(node_value[0], int(node_value[1]))
    nodes_list[node_value[0]] = new_node

# iterating through list and creating edges for the node objects
for i in string_edges:
    temp_edges = i.split(' ')

    nodes_list[temp_edges[0]].edges.append(nodes_list[temp_edges[1]])
    nodes_list[temp_edges[1]].edges.append(nodes_list[temp_edges[0]])

# helper function that returns the unused edges
def  check_unused_edges(check_set):
    edges_copy = EDGES.copy()
    remove_list = []

    for i in check_set:
        for j in edges_copy:
            if i in j:
                remove_list.append(j)

    for j in remove_list:
        if j in edges_copy:
            edges_copy.remove(j)
    return edges_copy

# helper funciotn that returns the cost of a set
def cost_function(set):
    cost = 0
    for i in set:
        cost += nodes_list[i].cost
    return cost

# function that checks if a set is a solution
def issolution(set):
    cost  = cost_function(set)
    unused_edges = check_unused_edges(set)
    if cost < budget and unused_edges == []:
        return True
    else:
        return False

state_store = []
# function that performs depth limited search 
def depth_limited_search(state, depth):
    if (issolution(state)):
        print(f" Found solution at {state}")
        return "break"
    if (depth == 0):
        return "temp"
    for i in nodes_list.keys():
        if state == [] or (ord(i) > ord(state[-1]) and budget >= cost_function(state)+nodes_list[i].cost and check_unused_edges(state+[i]) != check_unused_edges(state)):
            state.append(i)
            state_store.append(state)
            if output_type == "V":
                print(f" {state}     Cost = {cost_function(state)}")
            stop = depth_limited_search(state, depth-1)
            if stop == "break":
                return "break"
            state.pop()

# function that performs iterative deepening search algorithm
def iterative_deepening():
    prev_state = []
    state = []
    depth = 0
    notdone = True
    while(notdone):
        depth += 1
        if output_type == "V":
            print(f"\n Depth = {depth}")
        stop = depth_limited_search(state, depth)
        if stop == "break":
            break

        # checks if the states is the same as the previous states, if it is then it prints no solution is found
        prev_state.clear()
        prev_state = state_store.copy()
        state_store.clear()
        if prev_state == state_store:
            notdone = False
            print(" No solution found! ")

def main():
    iterative_deepening()

if __name__ == "__main__":
    main()





