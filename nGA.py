
import random
import time
import numpy


class nGA:


    def __init__(self, n, gen_board, epoch, psize, p_mutation, p_crossover):

        self.n = n
        self.gen_board = gen_board
        self.epoch = epoch
        self.psize = psize
        self.p_mutation = p_mutation
        self.p_crossover = p_crossover

        self.curr = [n-1, 0]
    

    def start(self, main_frame, info_frame, board, bc, traffic):
        
        self.gen_board = board
        #generate initial rule-board
        rule_board = []
        
        for j in range(self.n):
            t = []
            for i in range(self.n):
                n = random.randint(0,2)
                t.append(n)
            rule_board.append(t)

        for x in rule_board:
            print(x)


        for i in range(self.epoch):
            #call fitness function 

            #rework is an array that contains the co-ordinates the led made the agent wait
            #re_act is an array that contains the corresponding action of that co-ordinate
            
            fitness, rework, re_act = self.fitness(rule_board, board, bc, main_frame, traffic)

            fit_arr = []
            #convert the action to it's binary form, create a massive string with these concatenated binary strings
            bin_act = self.conv_act(re_act)

            #do something with bin_act to get some useful operation
            
            #decode the string to individual actions

            #hard-set the new-actions with their respective co-ordinates for the rule-board

            #add the fitness to an array
            fit_arr.append(fitness)
            #update the global rule_board variable to the new rule_board
            board = self.gen_board      




    def conv_act(self, re_act):

        ret = []
        for x in re_act:
            if x == 0:
                ret=[0,0]
            elif x == 1:
                ret+=[0,1]
            elif x == 2:
                ret+=[1,0]
            else:
                ret+=[1,1]
        return ret


    def fitness(self, rule_board, board, bc, main_frame, traffic):
        
        i, j = self.curr[0], self.curr[1]
        steps = 0
        color_board, t_rules = traffic[0], traffic[1]
        rework, re_act = [], []

        for i in range(self.n**2):
            #check what rule the agent has to take based on the action in gen_board
            act = rule_board[i][j]

            #call rule_act
            new_i, new_j, rework, re_act = self.rule_act(i, j, act, board, rework, re_act)

            #change the position on the board
            board[i][j] = 1
            board[new_i][new_j] = 9
            i, j = new_i, new_j

            if i == 0 and j == self.n-1:
                return steps, rework, re_act

            #call traffic move

            steps+=1

            #color the board
            bc.re_color_board(board, color_board, self.n)
            main_frame.update() #updates/refresh the main_frame
            time.sleep(0.05)

        return steps, rework, re_act





    def rule_act(self, i, j, act, board, rework, re_act):
          
        while True:

            # go up
            if act == 0:
                #check if the position is valid
                if self.check_pos(i-1, j):
                    #if the position is valid but there is no traffic in the next position
                    if self.check_traffic(i-1, j, board):
                        return i-1, j, rework, re_act
                    #position is valid but traffic in the next position
                    else:
                        return i, j, rework, re_act

            #go right
            elif act == 1:
                #check if the position is valid
                if self.check_pos(i, j+1):
                    #if the position is valid but there is no traffic in the next position
                    if self.check_traffic(i, j+1, board):
                        return i, j+1, rework, re_act
                    #position is valid but traffic in the next position
                    else:
                        return i, j+1, rework, re_act

            #go left
            elif act == 2:        
                #check if the position is valid
                if self.check_pos(i, j-1):
                    #if the position is valid but there is no traffic in the next position
                    if self.check_traffic(i, j-1, board):
                        return i, j-1, rework, re_act
                    #position is valid but traffic in the next position
                    else:
                        return i, j-1, rework, re_act

            #set act to random action
            print("stuck in the while loop")
            act = random.randint(0,2)
            rework.append([i, j])
            re_act.append(act)



    def check_pos(self, i, j):
        if 0 <= i < self.n-1 and 0 <= j < self.n-1:
            return True
        return False


    def check_traffic(self, i, j, board):
        if board[i][j] == 1:
            return True
        return False
