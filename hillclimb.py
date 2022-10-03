
import random

# ENTER INPUT FILE PATH HERE
input_name = '/Users/soumenmohanty/Documents/Fall-2022/Artificial-Intelligence/Programming-Assignment-1/input.txt'
input_file = open(input_name, 'r' )

# parsing input file
line1 = input_file.readline().strip().split(' ')

budget = int(line1[0])
output_type = line1[1]
num_restarts = int(line1[2])

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

# random restart function that returns a random set of nodes with each node having a 50% chance of being in the set
def random_restart():
    set = []
    for i in nodes_list.keys():
        if random.choices(range(2)) == [1]:
            set.append(i)
    print(f" Randomly chosen start state {set}")
    return set

# helper function that returns the cost and error of a given set
def error_function(set):
    cost = 0
    unused_edges_cost = 0

    for i in set:
        cost += nodes_list[i].cost
        
    unused_edges = check_unused_edges(set)
    for i in unused_edges:
        unused_edges_cost += min(nodes_list[i[0]].cost, nodes_list[i[1]].cost)
    
    ret_value = max(0, cost - budget) + unused_edges_cost
    return cost, ret_value

# function that prints the neighbors of a given set, it also returns the best neighbor
def findneighbors(set):
    best_cost, best_error = error_function(set)
    next_set = []
    if output_type == 'V':
        print(" Neighbors:")
    for i in nodes_list.keys():
        set_copy = set.copy()

        if i in set:
            set_copy.remove(i)
            cost, error = error_function(set_copy)
            if error <= best_error:
                if error == best_error and cost < best_cost:
                    best_cost = cost
                    next_set = set_copy.copy()
                elif error < best_error:    
                    best_cost = cost
                    best_error = error
                    next_set = set_copy.copy()
            if output_type == 'V':
                print(f" {set_copy} Cost = {cost}. Error = {error}")
        
        elif i not in set:
            set_copy.append(i)
            set_copy.sort()
            cost, error = error_function(set_copy)   
            if error <= best_error:
                if error == best_error and cost < best_cost:
                    best_cost = cost
                    next_set = set_copy.copy()
                elif error < best_error:    
                    best_cost = cost
                    best_error = error
                    next_set = set_copy.copy()
            if output_type == 'V':
                print(f" {set_copy} Cost = {cost}. Error = {error}")
    
    if next_set == [] and set_copy != []:
        return 0, set
    else:
        return 1, next_set

# function that checks if a given set is a solution
def issolution(set):
    cost, error = error_function(set)
    unused_edges = check_unused_edges(set)
    if cost < budget and unused_edges == []:
        return True
    else:
        return False


# hill climb function that returns the best solution using hill climb algorithm
def hillClimbing():
    solution_set = []
    for i in range(num_restarts):
        doneflag = False
        solution_set = random_restart()

        cost, error = error_function(solution_set)
        if output_type == 'V':
            print(f"Cost = {cost}. Error = {error}")

        done, solution_set = findneighbors(solution_set)
        if done == 0:
            if issolution(solution_set):
                print(f"\n Solution is {solution_set} \n")
            else:
                print(f"\n Search failed \n")
            doneflag = True
        while not doneflag:
            if output_type == 'V':
                print(f"\n Move to {solution_set}")
            done, solution_set = findneighbors(solution_set)
            if done == 0:
                if issolution(solution_set):
                    print(f"\n Solution is {solution_set} \n")
                else:
                    print(f"\n Search failed \n")
                doneflag = True

def main():
    hillClimbing()

if __name__ == "__main__":
    main()










