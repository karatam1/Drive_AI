import time
import copy
import random
import numpy as np

class Sim:

    def __init__(self, gen_board):
        self.gen_board = gen_board
        self.n = len(gen_board)
        #sets the agent's initial positions
        self.curr = [self.n-1,0]
        self.orient = 'R'

        self.hit_target = []


    def move2(self, population, main_frame, bc, color_board, rules):
        ################# THIS IS ONLY FOR TESTING PURPOSES #############
        #sets the agent's initial positions
        i, j = self.curr[0], self.curr[1]
        for k in range(20):
            if k % 5 == 0:
                #generates new blocks every 5 iterations
                self.gen_board = bc.blocks_gen(self.gen_board, len(self.gen_board))
            self.gen_board = bc.traffic_move(self.gen_board, rules)
            self.gen_board[i][j] = 1
            if i > 1:
                i-=1
            self.gen_board[i][j] = 9
            self.curr = [i, j]
            bc.re_color_board(self.gen_board, color_board, self.n)
            main_frame.update() #updates/refresh the main_frame
            time.sleep(0.3)
        ##########################################################################
            


    def move(self, i, j, orient, action):
        
        #agent moves up
        if action == 'Up':
            if orient == 'U':
                return [i-1, j, 'U']
            if orient == 'L':
                return [i, j-1, 'L']
            if orient == 'D':
                return [i+1, j, 'D'] 
            if orient == 'R':
                return [i, j+1, 'R']

        #agent moves to the left
        elif action == 'Le':
            if orient == 'U':
                return [i, j-1, 'L']
            if orient == 'L':
                return [i+1, j, 'D']
            if orient == 'D':
                return [i, j+1, 'R'] 
            if orient == 'R':
                return [i-1, j, 'U']


        #agent moves to the right
        elif action == 'Ri':
            if orient == 'U':
                return [i, j+1, 'R']
            if orient == 'L':
                return [i-1, j, 'U']
            if orient == 'D':
                return [i, j-1, 'L'] 
            if orient == 'R':
                return [i+1, j, 'D']

        #agent must wait at current location
        else:
            #action = 'Wi':
            return [i, j, orient]
        


    def simulator(self, gen_board, rls, bc, chromosome, main_frame, color_board):
        #the below lines ensure that the simulator sees the same board with the same traffic positions everytime 
        self.gen_board = gen_board
        board = copy.deepcopy(self.gen_board)
        t_rules = copy.deepcopy(rls) #not to get confused with rules in chromosome, this rule variable is for traffic
        positions = copy.deepcopy(bc.positions)
        curr = copy.copy(self.curr)
        orient = np.copy(self.orient)
        i, j = curr[0], curr[1]
        

        steps = 0
        #runs through a max run-time of n**2 positions (essentially the maximum time it can take to itertate through all positions of the board)
        for v in range(self.n**2):
            
            #returns the field (in bits) as viewed from the current location 
            field = self.FOV(i, j, orient, board)

            #print("field looks like ", field)
            #the first matching rule with field is returned from rule_find()
            first_rule = self.rule_find(field, chromosome)
            
            #checks if no rule found
            if first_rule == []:
                #take random action among [up, left, right, wait]
                act = random.sample(['Up', 'Le', 'Ri', 'Wi'], 1)[0]

            #rule was found
            else:
                act = self.rule_act(list(first_rule[-2:]))

            #gets the next position of the agent 
            #print("the act is ", act)
            movements = self.move(i, j, orient, act)

            new_i, new_j, orient = movements[0], movements[1], movements[2]

            #print(new_i, new_j, orient)

            #checks if it hits the target
            if new_i == 0 and new_j == self.n-1:
                return steps, 1

            #makes sure the new_i and new_j are not going out of bounds
            if new_i < 0 or new_i > self.n-1 or new_j < 0 or new_j > self.n-1:
                new_i, new_j = max(0, new_i), max(0, new_j) 
                new_i, new_j = min(new_i, self.n-1), min(new_j, self.n-1)

                #penalizes due to the out of bounds issues
                steps-=1

            else:
                #checks if the new spot is empty (based on new_i, new_j)
                if board[new_i][new_j] == 1:
                    steps +=1
                    board[i][j] = 1 #resets the agents old position to 1 (road)
                    board[new_i][new_j] = 9 #sets the agents new position in the direction of action

                    i, j = new_i, new_j
                    #code to re-color board goes here
                
            if v % 10 == 0:
                #generates new blocks every 10 iterations
                board = bc.blocks_gen(board, self.n)
            #moves the traffic
            board = bc.traffic_move(board, t_rules)

        
            #bc.re_color_board(board, color_board, self.n)
            #main_frame.update() #updates/refresh the main_frame
            #time.sleep(0.3)
            #print(steps)
        return steps, 0




    def FOV(self, i, j, orient, board):

        #agent is not at the edge
        if 1 <= i < self.n-1 and 1 <= j < self.n-1:
            if orient == 'U':
                return self.field_conv([board[i][j-1], board[i-1][j-1], board[i-1][j], board[i-1][j+1], board[i][j+1]])

            elif orient == 'L':
                return self.field_conv([board[i+1][j], board[i+1][j-1], board[i][j-1], board[i-1][j-1], board[i-1][j]])

            elif orient == 'R':
                return self.field_conv([board[i-1][j], board[i-1][j+1], board[i][j+1], board[i+1][j+1], board[i+1][j]])

            elif orient == 'D':
                return self.field_conv([board[i][j+1], board[i+1][j+1], board[i+1][j], board[i+1][j-1], board[i][j-1]])
            
        #checks if the agent is at the edge/boundary of the board
        else:
            return self.field_conv([9,9,9,9,9])


    def field_conv(self, field):

        ret = []
        for r in field:
            if r == 0: # it is land
                ret+=[0, 0, 0]
            elif r == 1: # it is a road
                ret+=[0, 0, 1]
            elif r == 2: # it is a traffic piece
                ret+=[0, 1, 0]
            elif r < 0: # it is some sort of traffic block
                ret+=[0, 1, 1]
            else:
                ret+=[2, 2, 2] #it is at an edge
        return ret


    def rule_find(self, field, chromosome):

        if field == []:
            return field

        for i in range(0, len(chromosome), 17):
            same = field == list(chromosome[i:i+15])
            if same:
                return chromosome[i:i+17]
        return []


    def rule_act(self, action):

        if action == [0, 0]:
            return 'Up'
        elif action == [0, 1]:
            return 'Le'
        elif action == [1, 0]:
            return 'Ri'
        elif action == [1, 1]:
            return 'Wi'        
        else:
            return random.sample(['Up', 'Le', 'Ri', 'Wi'], 1)
