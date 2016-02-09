#Lnook for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the warehouse domain.

'''
rushhour STATESPACE
'''
#   You may add only standard python imports---i.e., ones that are automatically
#   available on CDF.
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files
import copy

from search import *
from random import randint

##################################################
# The search space class 'rushhour'             #
# This class is a sub-class of 'StateSpace'      #
##################################################


class rushhour(StateSpace):
    def __init__(self, action, gval, statevar, parent = None):
        """Initialize a rushhour search state object."""
        StateSpace.__init__(self, action, gval, parent)
        self.statevar = statevar

    def successors(self):
        '''Return list of rushhour objects that are the successors of the current object'''
        # Successors are valid movements of a vehicle
        successor_states = list() 

        for vidx, veh in enumerate(self.statevar["myVehicles"]):
            # Check forward and back for empty spaces
            vloc_x = veh["location"][0]
            vloc_y = veh["location"][1]
            vlen = veh["length"]
            m = self.statevar["board_size"][0]
            n = self.statevar["board_size"][1]

            if veh["is_horizontal"]:
                vneg = ((vloc_x-1) % n, vloc_y)
                vpos = ((vloc_x+vlen) % n, vloc_y)

                ### MOVE WEST
                if vneg in self.statevar["blank_spaces"]:
                    nxt_state = copy.deepcopy(self.statevar)
                    nxt_state["myVehicles"][vidx]["location"] = vneg # make changes
                    ## change occupado status
                    nxt_state["blank_spaces"].remove(vneg)
                    freed_space = ((vloc_x-1+vlen) % n, vloc_y)
                    nxt_state["blank_spaces"].append(freed_space)
                    nxt_state["blank_spaces"].sort()

                    ### Add to list
                    successor_states.append(rushhour('move_vehicle({},W)'.format(veh["name"]), self.gval+1, nxt_state))

                nxt_state = []

                ### MOVE EAST
                if vpos in self.statevar["blank_spaces"]:
                    nxt_state = copy.deepcopy(self.statevar)
                    # make changes
                    nxt_state["myVehicles"][vidx]["location"] = ((vloc_x+1) % n, vloc_y) 
                    ## change occupado status
                    nxt_state["blank_spaces"].remove(vpos)
                    freed_space = (vloc_x, vloc_y)
                    nxt_state["blank_spaces"].append(freed_space)
                    nxt_state["blank_spaces"].sort()

                    ### Add to list
                    successor_states.append(rushhour('move_vehicle({},E)'.format(veh["name"]), self.gval+1, nxt_state))

                ### SELF-BLOCKING
                if veh["length"] == n:
                    nxt_state_E = copy.deepcopy(self.statevar)
                    nxt_state_W = copy.deepcopy(self.statevar)
                    # make changes
                    nxt_state_E["myVehicles"][vidx]["location"] = ((vloc_x+1) % n, vloc_y) 
                    nxt_state_W["myVehicles"][vidx]["location"] = vneg
                    nxt_state_E["blank_spaces"].sort()
                    nxt_state_W["blank_spaces"].sort()

                    ### Add to list
                    successor_states.append(rushhour('move_vehicle({},E)'.format(veh["name"]), self.gval+1, nxt_state_E))
                    successor_states.append(rushhour('move_vehicle({},W)'.format(veh["name"]), self.gval+1, nxt_state_W))
            else:
                vneg = (vloc_x, (vloc_y-1) % m)
                vpos = (vloc_x, (vloc_y+vlen) % m)

                ### MOVE NORTH
                if vneg in self.statevar["blank_spaces"]:
                    nxt_state = copy.deepcopy(self.statevar)
                    nxt_state["myVehicles"][vidx]["location"] = vneg # make changes
                    ## change occupado status
                    nxt_state["blank_spaces"].remove(vneg)
                    freed_space = (vloc_x, (vloc_y-1+vlen) % m)
                    nxt_state["blank_spaces"].append(freed_space)
                    nxt_state["blank_spaces"].sort()

                    ### Add to list
                    successor_states.append(rushhour('move_vehicle({},N)'.format(veh["name"]), self.gval+1, nxt_state))

                nxt_state = []

                ### MOVE SOUTH
                if vpos in self.statevar["blank_spaces"]:
                    nxt_state = copy.deepcopy(self.statevar)
                    # make changes
                    nxt_state["myVehicles"][vidx]["location"] = (vloc_x, (vloc_y+1) % m) 
                    ## change occupado status
                    nxt_state["blank_spaces"].remove(vpos)
                    freed_space = (vloc_x, vloc_y)
                    nxt_state["blank_spaces"].append(freed_space)
                    nxt_state["blank_spaces"].sort()

                    ### Add to list
                    successor_states.append(rushhour('move_vehicle({},S)'.format(veh["name"]), self.gval+1, nxt_state, self))

                ### SELF-BLOCKING
                if veh["length"] == n:
                    nxt_state_N = copy.deepcopy(self.statevar)
                    nxt_state_S = copy.deepcopy(self.statevar)
                    # make changes
                    nxt_state_N["myVehicles"][vidx]["location"] = vneg # make changes
                    nxt_state_S["myVehicles"][vidx]["location"] = (vloc_x, (vloc_y+1) % m) 
                    nxt_state_N["blank_spaces"].sort()
                    nxt_state_S["blank_spaces"].sort()

                    ### Add to list
                    successor_states.append(rushhour('move_vehicle({},N)'.format(veh["name"]), self.gval+1, nxt_state_N))
                    successor_states.append(rushhour('move_vehicle({},S)'.format(veh["name"]), self.gval+1, nxt_state_S))
        
       #for ss in successor_states:
       #    print("----------")
       #    board = get_board(ss.get_vehicle_statuses(), ss.get_board_properties())
       #    for bl in board:
       #        print("{}".format(''.join(bl)))
       #print("##########")

        return successor_states

    def hashable_state(self):
        '''Return a data item that can be used as a dictionary key to UNIQUELY represent the state.'''
        myhash = self.make_hash(self.statevar)
        # print("HASH: {}\n".format(myhash))
        return myhash

    def make_hash(self, nested_obj):
        if isinstance(nested_obj, (set, tuple, list)):
            return tuple([self.make_hash(e) for e in nested_obj])
        elif not isinstance(nested_obj, (dict)):
            return hash(nested_obj)

        new_obj = copy.deepcopy(nested_obj)
        for k, v in new_obj.items():
            new_obj[k] = self.make_hash(v)

        return hash(tuple(frozenset(sorted(new_obj.items()))))

    def print_state(self):
        #DO NOT CHANGE THIS FUNCTION---it will be used in auto marking
        #and in generating sample trace output.
        #Note that if you implement the "get" routines
        #(rushhour.get_vehicle_statuses() and rushhour.get_board_size())
        #properly, this function should work irrespective of how you represent
        #your state.

        if self.parent:
            print("Action= \"{}\", S{}, g-value = {}, (From S{})".format(self.action, self.index, self.gval, self.parent.index))
        else:
            print("Action= \"{}\", S{}, g-value = {}, (Initial State)".format(self.action, self.index, self.gval))

        print("Vehicle Statuses")
        for vs in sorted(self.get_vehicle_statuses()):
            print("    {} is at ({}, {})".format(vs[0], vs[1][0], vs[1][1]), end="")
        board = get_board(self.get_vehicle_statuses(), self.get_board_properties())
        print('\n')
        print('\n'.join([''.join(board[i]) for i in range(len(board))]))

#Data accessor routines.

    def get_vehicle_statuses(self):
        '''Return list containing the status of each vehicle
           This list has to be in the format: [vs_1, vs_2, ..., vs_k]
           with one status list for each vehicle in the state.
           Each vehicle status item vs_i is itself a list in the format:
                 [<name>, <loc>, <length>, <is_horizontal>, <is_goal>]
           Where <name> is the name of the vehicle (a string)
                 <loc> is a location (a pair (x,y)) indicating the front of the vehicle,
                       i.e., its length is counted in the positive x- or y-direction
                       from this point
                 <length> is the length of that vehicle
                 <is_horizontal> is true iff the vehicle is oriented horizontally
                 <is_goal> is true iff the vehicle is a goal vehicle
        '''
        # Convert dicts back into list
        out_list = list()
        for veh in self.statevar["myVehicles"]:
           out_list.append(
                   [
                        veh["name"],
                        veh["location"],
                        veh["length"],
                        veh["is_horizontal"],
                        veh["is_goal"]
                   ]) 

        return out_list

    def get_board_properties(self):
        '''Return (board_size, goal_entrance, goal_direction)
           where board_size = (m, n) is the dimensions of the board (m rows, n columns)
                 goal_entrance = (x, y) is the location of the goal
                 goal_direction is one of 'N', 'E', 'S' or 'W' indicating
                                the orientation of the goal
        '''
        return (
                self.statevar["board_size"], 
                self.statevar["goal_entrance"], 
                self.statevar["goal_direction"]
            )

#############################################
# heuristics                                #
#############################################


def heur_zero(state):
    '''Zero Heuristic use to make A* search perform uniform cost search'''
    return 0


def heur_min_moves(state):
    '''rushhour heuristic'''
    #We want an admissible heuristic. Getting to the goal requires
    #one move for each tile of distance.
    #Since the board wraps around, there are two different
    #directions that lead to the goal.
    #NOTE that we want an estimate of the number of ADDITIONAL
    #     moves required from our current state
    #1. Proceeding in the first direction, let MOVES1 =
    #   number of moves required to get to the goal if it were unobstructed
    #2. Proceeding in the second direction, let MOVES2 =
    #   number of moves required to get to the goal if it were unobstructed
    #
    #Our heuristic value is the minimum of MOVES1 and MOVES2 over all goal vehicles.
    #You should implement this heuristic function exactly, even if it is
    #tempting to improve it.

    m = state.statevar["board_size"][0]
    n = state.statevar["board_size"][1]

    ## Isolate goal vehicles
    moves = [float('inf')]
    for veh in state.statevar["myVehicles"]:
        if veh["goal_square"] == -1:
            continue
        
        move1 = float('inf')
        move2 = float('inf')

        if veh["is_horizontal"]:
            gsy = veh["goal_square"][0]
            vly = veh["location"][0]

            if vly > gsy:
                move1 = vly - gsy
                move2 = (gsy+n) - vly
            else:
                move1 = gsy - vly
                move2 = vly - (gsy-n)
        else:
            gsx = veh["goal_square"][1]
            vlx = veh["location"][1]

            if vlx > gsx:
                move1 = vlx - gsx
                move2 = (gsx+m) - vlx
            else:
                move1 = gsx - vlx
                move2 = vlx - (gsx-m)
        
        moves.append(min(move1,move2))
    return min(moves)

def rushhour_goal_fn(state):
    '''Have we reached a goal state'''
    ## Isolate goal vehicles
    for veh in state.statevar["myVehicles"]:
        if veh["goal_square"] == -1:
            continue
        elif veh["location"] == veh["goal_square"]:
            return True
    return False

def make_init_state(board_size, vehicle_list, goal_entrance, goal_direction):
    '''Input the following items which specify a state and return a rushhour object
       representing this initial state.
         The state's its g-value is zero
         The state's parent is None
         The state's action is the dummy action "START"
       board_size = (m, n)
          m is the number of rows in the board
          n is the number of columns in the board
       vehicle_list = [v1, v2, ..., vk]
          a list of vehicles. Each vehicle vi is itself a list
          vi = [vehicle_name, (x, y), length, is_horizontal, is_goal] where
              vehicle_name is the name of the vehicle (string)
              (x,y) is the location of that vehicle (int, int)
              length is the length of that vehicle (int)
              is_horizontal is whether the vehicle is horizontal (Boolean)
              is_goal is whether the vehicle is a goal vehicle (Boolean)
      goal_entrance is the coordinates of the entrance tile to the goal and
      goal_direction is the orientation of the goal ('N', 'E', 'S', 'W')

   NOTE: for simplicity you may assume that
         (a) no vehicle name is repeated
         (b) all locations are integer pairs (x,y) where 0<=x<=n-1 and 0<=y<=m-1
         (c) vehicle lengths are positive integers
    '''
    # Need way to identify empty spaces, use matrix; tailored for sparse empty spaces

    ### Identify empty spaces on board
    board = get_board(vehicle_list, [board_size, goal_entrance, goal_direction])

    blank_spaces = list()
    for r,row_w_blank in enumerate(board):
        if "." in row_w_blank:
            for k,cell in enumerate(row_w_blank):
                if cell == ".":
                    blank_spaces.append((k,r))

    # Sort so hashing won't get messed up
    blank_spaces.sort()

    ge_x = goal_entrance[0]
    ge_y = goal_entrance[1]
    m = board_size[0]
    n = board_size[1]

    ### Use own vehicle objects (list of dictionaries)
    myVehicles = list()
    for vehicle in vehicle_list:
        goal_square = -1 # Initialize

        v_dic = {
                    "name": vehicle[0],
                    "location": vehicle[1],
                    "length": vehicle[2],
                    "is_horizontal": vehicle[3],
                    "is_goal": vehicle[4],
            }
                    
        vlen = v_dic["length"]
        if v_dic["is_goal"]:
            # Vehicle is horz, goal is horz, goal row == vehicle row
            if v_dic["is_horizontal"] and goal_direction in ['W','E'] and ge_y == v_dic["location"][1]:
                if goal_direction == 'E': # East facing goals
                    goal_square = ((ge_x-vlen+1) % n, ge_y)
                else:
                    goal_square = (ge_x, ge_y)
            # Vehicle is vert, goal is vert, goal col == vehicle col
            elif goal_direction in ['N','S'] and ge_x == v_dic["location"][0]: 
                if goal_direction == 'S': # South facing goals
                    goal_square = (ge_x, (ge_y-vlen+1) % m) 
                else: # North facing goals
                    goal_square = (ge_x, ge_y)

        v_dic["goal_square"] = goal_square
        myVehicles.append(v_dic)
    
    statevar = {
            "board_size": board_size, 
            "myVehicles": myVehicles, 
            "goal_entrance": goal_entrance, 
            "goal_direction": goal_direction,
            "blank_spaces": blank_spaces
        }

   #for bl in board:
   #    print("{}".format(''.join(bl)))

    return rushhour("START", 0, statevar)

########################################################
#   Functions provided so that you can more easily     #
#   Test your implementation                           #
########################################################


def get_board(vehicle_statuses, board_properties):
    #DO NOT CHANGE THIS FUNCTION---it will be used in auto marking
    #and in generating sample trace output.
    #Note that if you implement the "get" routines
    #(rushhour.get_vehicle_statuses() and rushhour.get_board_size())
    #properly, this function should work irrespective of how you represent
    #your state.
    (m, n) = board_properties[0]
    board = [list(['.'] * n) for i in range(m)]
    for vs in vehicle_statuses:
        for i in range(vs[2]):  # vehicle length
            if vs[3]:
                # vehicle is horizontal
                board[vs[1][1]][(vs[1][0] + i) % n] = vs[0][0]
                # represent vehicle as first character of its name
            else:
                # vehicle is vertical
                board[(vs[1][1] + i) % m][vs[1][0]] = vs[0][0]
                # represent vehicle as first character of its name
    # print goal
    board[board_properties[1][1]][board_properties[1][0]] = board_properties[2]
    return board


def make_rand_init_state(nvehicles, board_size):
    '''Generate a random initial state containing
       nvehicles = number of vehicles
       board_size = (m,n) size of board
       Warning: may take a long time if the vehicles nearly
       fill the entire board. May run forever if finding
       a configuration is infeasible. Also will not work any
       vehicle name starts with a period.

       You may want to expand this function to create test cases.
    '''

    (m, n) = board_size
    vehicle_list = []
    board_properties = [board_size, None, None]
    for i in range(nvehicles):
        if i == 0:
            # make the goal vehicle and goal
            x = randint(0, n - 1)
            y = randint(0, m - 1)
            is_horizontal = True if randint(0, 1) else False
            vehicle_list.append(['gv', (x, y), 2, is_horizontal, True])
            if is_horizontal:
                board_properties[1] = ((x + n // 2 + 1) % n, y)
                board_properties[2] = 'W' if randint(0, 1) else 'E'
            else:
                board_properties[1] = (x, (y + m // 2 + 1) % m)
                board_properties[2] = 'N' if randint(0, 1) else 'S'
        else:
            board = get_board(vehicle_list, board_properties)
            conflict = True
            while conflict:
                x = randint(0, n - 1)
                y = randint(0, m - 1)
                is_horizontal = True if randint(0, 1) else False
                length = randint(2, 3)
                conflict = False
                for j in range(length):  # vehicle length
                    if is_horizontal:
                        if board[y][(x + j) % n] != '.':
                            conflict = True
                            break
                    else:
                        if board[(y + j) % m][x] != '.':
                            conflict = True
                            break
            vehicle_list.append([str(i), (x, y), length, is_horizontal, False])

    return make_init_state(board_size, vehicle_list, board_properties[1], board_properties[2])


def test(nvehicles, board_size):
    s0 = make_rand_init_state(nvehicles, board_size)
    se = SearchEngine('astar', 'full')
    #se.trace_on(2)
    final = se.search(s0, rushhour_goal_fn, heur_min_moves)
