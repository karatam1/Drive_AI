
import random


class nGA:


    def __init__(self, n, main_board, gen_board, epoch, psize, p_mutation, p_crossover):

        self.n = n
        self.gen_board = gen_board
        self.epoch = epoch
        self.psize = psize
        self.p_mutation = p_mutation
        self.p_crossover = p_crossover

        self.curr = [n-1, 0]
    

    def start(self, board):
        
        self.gen_board = board
        #generate initial rule-board
        rule_board = []
        
        for j in range(self.n):
            t = []
            for i in range(self.n):
                n = random.randint(1,4)
                t.append(n)
            rule_board.append(t)



        for i in range(self.epoch):
            #call fitness function 

            #rework is an array that contains the co-ordinates the led made the agent wait
            #re_act is an array that contains the corresponding action of that co-ordinate
            fitness, rework, re_act = self.fitness(rule_board)

            #convert the action to it's binary form, create a massive string with these concatenated binary strings
            #function call

            #apply tournament on re_act
            #function call on the tournament (if odd size then do up to len(re_act)-1)
            
                #apply cross-over on the new children

                #add them to the new string

            #perform mutation on the new complete string

            #decode the string to individual actions

            #hard-set the new-actions with their respective co-ordinates for the rule-board

            #add the fitness to an array

            





    def fitness(self, rule_board):
        
        i, j = self.curr[0], self.curr[1]

        for i in range(self.n**2):

            #check what rule the agent has to take based on the action in gen_board
            act = rule_board[i][j]

            #call rule-act
            new_i, new_j = self.rule_act(act, rule_board)

            #check new positions
               


    def rule_act(self, act, rule_board, board):
        # go up
        if act == 0:
            #check if it can
            if self.check_pos(i-1, j):
                
            else:
                

        #go right
        elif act == 1:

        #go left
        elif act == 2:        


    def check_pos(self, i, j):
        if 0 <= i < self.n-1 and 0 <= j < self.n-1:
            return True
        return False



#up
#right
#left
#wait

        














