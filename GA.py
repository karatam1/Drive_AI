import Sim
import numpy as np

class Genetic_Alg:

    def __init__(self, n, gen_board, ga_data):

        self.n = n
        self.gen_board = gen_board

        #generations, string_length (17*20 rules), population size, p_mutation, p_crossover
        self.epoch = ga_data[0]
        self.str_len = ga_data[1]
        self.psize = ga_data[2]
        self.p_mutation = ga_data[3]
        self.p_crossover = ga_data[4]

        #----------------basic facts of the setup
        #each square on the grid can be one of [land:0, road:1, traffic: 2, block: -1]
        #the agent has at most 5 Field Of Views at any given time
        #will be using 20 rules, each rule will be represented by a 17-bit string
        #the string can be broken into 15-bits: F.O.V + 2-bits: Action


        #initialize the first generation of the population
        self.population = np.random.rand(self.psize, self.str_len)
        self.population = np.where(self.population < 0.5, 1, 0)

        #keeps track of min_steps and its corresponding chromosome
        self.min_steps = n**2
        self.min_chromosome = []

        #the most optimal path that the agent takes
        self.min_path = []
        

    def start(self, main_frame, gen_board, bc, traffic):
        #Important step, always make sure local gen_board is updated to the latest gen_board
        self.gen_board = gen_board
        
        #runs for specified no. of generations 
        for g in range(self.epoch):
            
            #fit_arr contains the fitness of each population,   len(fit_arr) == pop_size
            fit_arr = self.fitness(main_frame, bc, traffic)
            

            #REMOVE BREAK AFTER EVERYTHING IS READY
            break
            #######################################


            #create a new empty population, this will under-go repopulation based on the fitness of the old population
            new_population = np.zeros((self.psize, self.str_len), dtype = 'int64')

            #run tournament on old population
            for i in range(0, self.psize, 2):
                
                tup = self.tournament(fit_arr,self.psize)
                #extracts the index location of the new chromosomes to add
                n1, n2 = tup[0], tup[1]             
                
                #save the 2 indexed population to separate variables
                off1, off2 = self.population[n1], self.population[n2]
                
                #run cross-over on the candidates
                chr1, chr2 = self.cross_over(off1, off2)

                #populate the new_population
                new_population[i], new_population[i+1] = chr1, chr2       


            #mutuate the new population
            new_population = self.mutate_population(new_population)

            #update the global population variable with the new population variable
            self.population = new_population

            #calculate fitness of new population
            fit_arr = self.fitness(main_frame, bc, traffic)

            #update the global min_steps and corresponding chromosomes
            for i in range(len(fit_arr)):
                if fit_arr[i] < self.min_steps:
                    self.min_steps = fit_arr[i]
                    self.min_chromosome = self.population[i]
            
            #update the color_board data row with the new min_steps




    def fitness(self, main_frame, bc, traffic):
        
        #extract the color_board and rules
        color_board, rules = traffic[0], traffic[1]
        
        #creates the simulator object
        sim = Sim.Sim(self.gen_board)

        #calls the simulator  (this is the only link between the Sim.py and GA.py file)
        #steps = sim.move2(self.population, main_frame, bc, color_board, rules) #should be sim.simulator
        #####

        #intializes the return array
        vals = np.zeros(self.psize)
        target = 0
        target_arr = []

        #go through each chromosome in population
        for i in range(self.psize):
            
            #print(self.population[i])
            steps, hit = sim.simulator(self.gen_board, rules, bc, self.population[i], main_frame, color_board)
            target+=hit
            vals[i] = steps
            if hit == 1:
                target_arr.append(steps)

        print(vals)
        print(max(vals), min(vals))
        print("Hit target ",target, target_arr)

        return vals


    def tournament(self,fitness,popsize):
        # select first parent par1
        cand1 = np.random.randint(popsize)      # candidate 1, 1st tourn., int
        cand2 = cand1                           # candidate 2, 1st tourn., int
        while cand2 == cand1:                   # until cand2 differs
            cand2 = np.random.randint(popsize)   #   identify a second candidate
        if fitness[cand1] > fitness[cand2]:     # if cand1 more fit than cand2 
            par1 = cand1                         #   then first parent is cand1
        else:                                   #   else first parent is cand2
            par1 = cand2
        # select second parent par2
        cand1 = np.random.randint(popsize)      # candidate 1, 2nd tourn., int
        cand2 = cand1                           # candidate 2, 2nd tourn., int
        while cand2 == cand1:                   # until cand2 differs
            cand2 = np.random.randint(popsize)   #   identify a second candidate
        if fitness[cand1] > fitness[cand2]:     # if cand1 more fit than cand2 
            par2 = cand1                         #   then 2nd parent par2 is cand1
        else:                                   #   else 2nd parent par2 is cand2
            par2 = cand2
        return par1,par2

    def cross_over(self, child1,child2):
        # single point crossover
        # cut locn to right of position (hence subtract 1)
        locn = np.random.randint(0,self.str_len - 1)
        tmp = np.copy(child1)       # save child1 copy, then do crossover
        child1[locn+1:self.str_len] = child2[locn+1:self.str_len]
        child2[locn+1:self.str_len] = tmp[locn+1:self.str_len]
        return child1,child2
        

    def mutate_population(self, pop):
        whereMutate = np.random.rand(np.shape(pop)[0],np.shape(pop)[1])
        whereMutate = np.where(whereMutate < self.p_mutation)
        pop[whereMutate] = 1 - pop[whereMutate]
        return pop
