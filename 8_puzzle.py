import copy

"""Implementation of 8 puzzle using DFS."""
__author__      = "Bethel Panashe Choto"

def welcome_msg():
    print('__        _______ _     ____ ___  __  __ _____ _  ')
    print('\ \      / / ____| |   / ___/ _ \|  \/  | ____| | ')
    print(' \ \ /\ / /|  _| | |  | |  | | | | |\/| |  _| | | ')
    print('  \ V  V / | |___| |__| |__| |_| | |  | | |___|_| ')
    print('   \_/\_/  |_____|_____\____\___/|_|  |_|_____(_) ')
    
    print(                    ' _         ')
    print(                    '| |_ ___   ')
    print(                    '| __/ _ \  ')
    print(                    '| || (_) | ')
    print(                     ' \__\___/ ')                                                

    print(' _____ ___ ____ _   _ _____   ____  _   _ ___________     _____  ')
    print('| ____|_ _/ ___| | | |_   _| |  _ \| | | |__  /__  / |   | ____| ')
    print('|  _|  | | |  _| |_| | | |   | |_) | | | | / /  / /| |   |  _|   ')
    print('| |___ | | |_| |  _  | | |   |  __/| |_| |/ /_ / /_| |___| |___  ')
    print('|_____|___\____|_| |_| |_|   |_|    \___//____/____|_____|_____| ')
    print('-----------------------------------------------------------------------\n')
    print('------------------------------------------------------------------------\n')

#take input from the user
def take_input():
    print("Enter a start node row wise (e.g 1 2 3 0 4 5 8 6 7)")
    user_in=[int(i) for i in input().split()]
    return user_in

class Problem:
    """ This class represents a generic Problem to be solved by search."""

    def __init__(self, init_state, goal_state):#start goal1
	    self.init_state = init_state
	    self.goal_state = goal_state

    def __str__(self):
        return (type(self).__name__ + ": Init state=" + str(self.init_state) +
                ", goal state=" + str(self.goal_state))
    
    def goal_test(self, state):
        return False

    def actions(self, state):
        return None, None

class Puzzle(Problem):
    """ This class represents the prolem of having a robot navigate
        in a 2D world with obstacles.
    """
    def __init__(self, init_state, goal_state):
        super().__init__(init_state,goal_state)
    
    #looping through the numbers to find the location of the blank space
    def BlankSpaceLoc(self, numbers):
    	for i in range(9):
    		if numbers[i] == 0:
    			return i

    def actions(self, numbers):
        position = self.BlankSpaceLoc(numbers)
        actions = []
        succ_states = []

        #move the blank position upwards
        U = copy.deepcopy(numbers)
        if position>2:
            U[position] = U[position - 3] #swap the numbers
            U[position - 3] = 0
            actions.append("U")
            succ_states.append(U)

        #move the blank position to the right 
        R = copy.deepcopy(numbers)
        if position != 2 and position != 5 and position != 8:
            R[position] = R[position+1] #swap the numbers
            R[position + 1] = 0
            actions.append("R")
            succ_states.append(R)

        #move the blank position to the left 
        L = copy.deepcopy(numbers)
        if position != 0 and position != 3 and position != 6:
            L[position] = L[position - 1] #swap the numbers
            L[position - 1] = 0
            actions.append("L")
            succ_states.append(L)

        #move the blank position downwards
        D = copy.deepcopy(numbers)
        if position<6:
            D[position] = D[position+3] #swap the numbers
            D[position + 3] = 0
            actions.append("D")
            succ_states.append(D)
        return actions, succ_states

    def goal_test(self,state):
        return (state == goal)

class Node:
    """ This class represents a node in the search tree"""

    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

    def __str__(self):    #which we will be using to as a key in comparing elements in the explored set
        mystr = "Node with state=" + str(self.state);
        if (self.parent != None):
            mystr += (", parent=" + str(self.parent.state) +
                    ", action=" + str(self.action) +
                    ", path_cost=" + str(self.path_cost))
        return mystr

    # The purpose of this method is to enable two nodes  on the
    # frontier to be considered equal to each other if they represent
    # the same state (regardless of if they have different parent nodes)
    def __eq__(self, other):
        return (isinstance(other,Node) and 
                self.state == other.state)

    def solution_path(self):
        # to do: implement this to generate the solution path
        # leading to this node
        actions_path = []
        overral_path_cost = 0
        sequence_of_actions = []
        
        while (self.parent is not None):
            actions_path.append(self.state)
            overral_path_cost += 1
            sequence_of_actions.append(self.action)
            self = self.parent
        sequence_of_actions.reverse()
        for i in range(len(sequence_of_actions)):
            print("Action", i+1 , sequence_of_actions[i],"\n")
            print_grid(actions_path[i])
            print('-----------\n')

def dfs(problem):
    #print("About to do DFS on problem: ", problem)
    node = Node(problem.init_state)
    #check if the given problem is solvable or not
    solv = 0
    for i in range(8):
    	for j in range(i,9):
    		if(node.state[i] > node.state[j] and node.state[j] !=0):
    			solv = solv + 1
    if(solv%2 == 0):
    	print("Solution Exist For This Problem!")
    	print("It might take a while to find the solution please be patient!!",'\n',"Solving...")
    else:
    	print(" solution does not exists for this initial state",'\n')
			
    
    if problem.goal_test(node.state):
        return node.solution_path()
    
    frontier = [node]
    explored = []
    nodes_processed = 0
    maxLength = 0

    while(len(frontier) > 0):
        maxLength = max(maxLength, len(frontier))
        node = frontier.pop() 
        nodes_processed += 1
        explored.append(node.state)
        actions, successors = problem.actions(node.state)
        for i in range(len(actions)):
            child = Node(successors[i], node, actions[i],
                         node.path_cost+1)
            if (child.state not in explored and
                child not in frontier):
                if (problem.goal_test(child.state)):
                    return child.solution_path()
                frontier.append(child)    
    return None

def print_grid(grid):
    i = 0
    for row in [0, 1, 2]:
        for col in [0, 1, 2]:
            print(grid[i],end = " | ")
            i = i + 1
        print()

def game_over():
        print('  ____                         ___                 _  ')
        print(' / ___| __ _ _ __ ___   ___   / _ \__   _____ _ __| | ')
        print('| |  _ / _` |  _ ` _ \ / _ \ | | | \ \ / / _ \  __| | ')
        print('| |_| | (_| | | | | | |  __/ | |_| |\ V /  __/ |  |_| ')
        print(' \____|\__,_|_| |_| |_|\___|  \___/  \_/ \___|_|  (_) ') 
        print('---------------------------------------------------------------------\n')
        print('----------------------------------------------------------------------\n')

if __name__ == "__main__":
  welcome_msg()
  goal = [1,2,3,4,5,6,7,8,0]
  dfs(Puzzle(take_input(),goal))
  game_over()

