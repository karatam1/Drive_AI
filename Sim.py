import time
import copy
import random
import math
import numpy as np

class Sim:

    def __init__(self, gen_board):
        self.gen_board = gen_board
        self.n = len(gen_board)
        #sets the agent's initial positions
        self.curr = [self.n-1,0]
        self.orient = 'R'

        self.hit_target = []



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
        


    def simulator(self, gen_board, rls, bc, chromosome, main_frame, color_board, show):
        #the below lines ensure that the simulator sees the same board with the same traffic positions everytime 
        self.gen_board = gen_board
        board = copy.deepcopy(self.gen_board)
        t_rules = copy.deepcopy(rls) #not to get confused with rules in chromosome, this rule variable is for traffic

        positions = copy.deepcopy(bc.positions)
        curr = copy.copy(self.curr)
        orient = np.copy(self.orient)
        i, j = curr[0], curr[1]
        
        visited = []    
        match = 0
        steps, cost = 0,0
        #runs through a max run-time of n**2 positions (essentially the maximum time it can take to itertate through all positions of the board)
        for v in range(self.n**2):
            
            new_i, new_j = 0, 0
            #returns the field (in bits) as viewed from the current location 
            field = self.FOV(i, j, orient, board)


            #the first matching rule with field is returned from rule_find()
            first_rule = self.rule_find(field, list(chromosome))
            

            #checks if no rule found
            if first_rule == []:
                #take random action among [up, left, right, wait]
                #orient = 'U'
                orient = random.sample(['U', 'L', 'R', 'D'], 1)[0]
                act = random.sample(['Up', 'Ri', 'Le' 'Wi'], 1)[0]
                #checks if up is available

                # if 0 <= i <= self.n-1 and 0 <= j+1 <= self.n-1:
                #     if board[i][j+1] == 1:
                #         act = 'Ri'

                # if 0 <= i-1 <= self.n-1 and 0 <= j <= self.n-1:
                #     if board[i-1][j] == 1:
                #         act = 'Up'

            #rule was found
            else:
                #print("rule matched")
                match+=1

                act = self.rule_act(list(first_rule[-2:]), i , j)
                
                #steps+=1
            #gets the next position of the agent 
            movements = self.move(i, j, orient, act)
            new_i, new_j, orient = movements[0], movements[1], movements[2]

            steps+=1

            #checks if it hits the target
            if new_i == 0 and new_j == self.n-1:

                #resets the traffic positions to the original after the simulation
                bc.positions = positions
                
                fit = self.fitCalc(new_i, new_j, steps, 50)

                return fit, 1, match


            #makes sure the new_i and new_j are not going out of bounds
            if new_i < 0 or new_i > self.n-1 or new_j < 0 or new_j > self.n-1:
                new_i, new_j = max(0, new_i), max(0, new_j) 
                new_i, new_j = min(new_i, self.n-1), min(new_j, self.n-1)

            else:
                #checks if the new spot is empty (based on new_i, new_j)
                if board[new_i][new_j] == 1:

                    #steps +=1
                    board[i][j] = 1 #resets the agents old position to 1 (road)
                    board[new_i][new_j] = 9 #sets the agents new position in the direction of action

                    i, j = new_i, new_j
                

            if v % 10 == 0:
                #generates new blocks every 10 iterations
                board = bc.blocks_gen(board, self.n)
            #moves the traffic
            board = bc.traffic_move(board, t_rules)


            #checks if it has to color the board
            if show:
                bc.re_color_board(board, color_board, self.n)
                main_frame.update() #updates/refresh the main_frame
                time.sleep(0.01)
                

        #resets the traffic positions to the original after the simulation
        bc.positions = positions

        #fitness function here
        fit = self.fitCalc(i, j, steps, 0)

        return fit, 0, match







    def fitCalc(self, i, j, steps, cost):#############################################################################

        i = self.n - i
        
        #euc_dist = (((n-i)^2) + ((n-j)^2))^((1/2))
        euc_dist = math.sqrt(math.pow((self.n-i), 2) + math.pow((self.n-j), 2))

        #euc_dist/= math.sqrt((self.n**2) + (self.n**2))
        max_dist = math.sqrt(math.pow((self.n-0), 2) + math.pow((self.n-0), 2))

        #(n^2 - steps) / n^2
        max_diff = math.pow(self.n,2) - steps
        
        return round(((max_dist - euc_dist) + max_diff), 2)

        #######################################################################################################        



    def FOV(self, i, j, orient, board):

        ret = []
        # #agent is not at the edge
        # if 1 <= i < self.n-1 and 1 <= j < self.n-1:
        #     if orient == 'U':
        #         return self.field_conv([board[i][j-1], board[i-1][j-1], board[i-1][j], board[i-1][j+1], board[i][j+1]])

        #     elif orient == 'L':
        #         return self.field_conv([board[i+1][j], board[i+1][j-1], board[i][j-1], board[i-1][j-1], board[i-1][j]])

        #     elif orient == 'R':
        #         return self.field_conv([board[i-1][j], board[i-1][j+1], board[i][j+1], board[i+1][j+1], board[i+1][j]])

        #     elif orient == 'D':
        #         return self.field_conv([board[i][j+1], board[i+1][j+1], board[i+1][j], board[i+1][j-1], board[i][j-1]])
        
        #else: #agent is at an edge
        arr = []
        if orient == 'U':
            arr = [[0, -1], [-1, -1], [-1, 0], [-1, 1], [0,1]]
        elif orient == 'L':
            arr = [[1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0]]
        elif orient == 'R':
            arr = [[-1,0], [-1, 1], [0, 1], [1, 1], [1, 0]]
        elif orient == 'D':
            arr = [[0, 1], [1,1], [1,0], [1, -1], [0, -1]]

        for x in arr:
            #checks if the position is in the board      
            if 0 <= i+x[0] <= self.n-1 and 0 <= j+x[1] <= self.n-1:
                ret.append(board[i+x[0]][j+x[1]])
            else:# it is not in board
                ret.append(5)
        return self.field_conv(ret)



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
            elif r == 5: # it is a wall
                #print("matched a wall")
                ret+=[1, 0, 0]
        return ret


    def rule_find(self, field, chromosome):

        for i in range(0, len(chromosome), 17):
            if field == (chromosome[i:i+15]):
                #print("rule matched")
                return chromosome[i:i+17]
        return []


    def rule_act(self, action, i , j):

        if action == [0,0]:
            return 'Up'
        elif action == [0,1]:
            return 'Le'
        elif action == [1,0]:
            return 'Ri'
        elif action == [1,1]:
            return 'Wi'    
        else:
            return random.sample(['Up', 'Le', 'Ri', 'Wi'], 1)[0]
