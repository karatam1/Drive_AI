import tkinter as tk
import random
import SSS as st
import GA as ga
import nGA as na 
import Board_Creator as bc
import time
import matplotlib.pyplot as mp

# GUI initializer
main_frame = tk.Tk()
main_frame.geometry("7000x7000")
main_frame.title("Drive_AI UI")
main_frame.configure(bg = "White")


def run_alg_sss(new_board, n, alg, epoch, color_board):
    
    #creates text file
    fds = open('sss_data.txt', 'a')

    rules = bc.traffic_rules_gen(new_board)
    taken, v = [], 0

    l5 = tk.Label(info_frame, text = "              Steps: ")
    l5.grid(row = 0, column = 2)

    for j in range(epoch):
        steps, v = 0, 0
        #resets the agent position in the grid
        alg.curr = [n-1, 0]
        while v < n**2:
            if v % 10 == 0:
                #generates new blocks every 5 iterations
                new_board = bc.blocks_gen(new_board, n)
            #moves the traffic
            new_board = bc.traffic_move(new_board, rules)
            #moves the agent
            new_board, curr = alg.move(new_board)
         
            #updates steps and check if it hit target
            steps+=1
            if curr[0] == 0 and curr[1] == n-1:
                v = n**2

            #decides when to color the board
            if j in [0, epoch/2, epoch-1]: 
                bc.re_color_board(new_board, color_board, n)
                main_frame.update() #updates/refresh the main_frame
                time.sleep(0.05)
            v+=1

        #stores the steps taken data
        taken.append(steps)
        
        #resets the agents position
        new_board[n-1][0] = 9
        new_board[0][n-1] = 1

        #updates the display values in the GUI
        l8 = tk.Label(info_frame, text = str(j+1))
        l9 = tk.Label(info_frame, text = str(steps))
        l8.grid(row = 0, column = 1)
        l9.grid(row = 0, column = 3, columnspan = 4)
        info_frame.update()

        #writes the data to the file
        fds.write("Epoch " + str(j+1) + " Steps: " + str(steps) + "\n")
    
    #displays the plot at the end
    #x array for plot
    gen_arr = [h for h in range(1, epoch+1)]

    fds.write("Min Steps: " + str(min(taken)) + " Max Steps: " + str(max(taken)) + " Avg Steps: " + str(sum(taken)/len(taken)) + "\n")
    fds.write("\n")
    fds.close()

    #plots epochs vs max-fitness
    mp.plot(gen_arr, taken) #epochs vs steps taken
    mp.ylabel("Steps")
    mp.xlabel("Epochs (generation)")
    mp.title("Steps vs Epoch Plot")
    mp.show()
    

def run_alg_ga(new_board, n, alg, color_board):

    #make the function call to the main GA_function that runs the entire operation
    #pass in bc board creator object
    #re_color board and traffics move, block generation, time.sleep() will occur over there instead
    #display every 10th epoch
    #either in the ga files or in main, print the epoch vs min_steps graph
    rules = bc.traffic_rules_gen(new_board)
    traffic = [color_board, rules]
    

    alg.start(main_frame, info_frame, new_board, bc, traffic)



#processing functions
def control():
    n, density, ai_method = size.get(), traf_dens.get(), alg.get()
    color_frame = tk.Frame(main_frame, width = "7000", height = "4000", bg = "White")
    color_frame.grid(row = 4)
    color_board = tk.Canvas(color_frame, borderwidth = 1, width = 7000, height = 4000, bg = "White")
    color_board.grid(row = 0, column = 1)
    #creates the initial color_board

    color_board = bc.board_init(n, color_board)
    #resets the traffic positions incase of re-submits
    bc.positions = []
    bc.blocks = {}
    #------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    #creates new_board based on functions from Board_Creator
    new_board = bc.board_gen(n, density)   
 

    #re-colors board based on the new_board specifications for the initial board preview
    bc.re_color_board(new_board, color_board, n)
    main_frame.update()
    time.sleep(0.7)


    #holds ga initialization data: generations, string_length (17*20 rules), population size, p_mutation, p_crossover
    ga_data = [100, 3400, 100, 0.01, 0.4]

    s1 = st.State_Space_Search(n, new_board)

    g1 = ga.Genetic_Alg(n, new_board, ga_data)




    #run sss
    if ai_method == 1:
        #epoch = 25
        run_alg_sss(new_board, n, s1, 100, color_board)
    
    #run ga
    elif ai_method == 2:
        run_alg_ga(new_board, n, g1, color_board)

    else:
        copy_board = new_board[:]

        run_alg_sss(new_board, n, s1, epoch, color_board)
        run_alg_ga(copy_board, n, g1, color_board)





###################################################################################################################################################################
#grid allocations
head_frame = tk.Frame(main_frame, width = "7000", height = "50", bg = "White")
input_frame = tk.Frame(main_frame, width = "7000", height = "200")
info_frame = tk.Frame(main_frame, width = "7000", height = "25")

head_frame.grid(row = 0, sticky = "nw")
input_frame.grid(row = 1, sticky = "nw")
info_frame.grid(row = 3, sticky = "nw")


#labels 
l1 = tk.Label(head_frame, text = "Choose the settings from the given options", bg = "White")
l2 = tk.Label(input_frame, text = "Grid Size:")
l3 = tk.Label(input_frame, text = "Density:")
l4 = tk.Label(info_frame, text = "Epoch # ")
l5 = tk.Label(info_frame, text = "Max-Fitness: ")
l6 = tk.Label(info_frame, text = "0")
l7 = tk.Label(info_frame, text = "0.0")


#variables
size = tk.IntVar()
traf_dens = tk.IntVar()
alg = tk.IntVar()


#Data Entries and Buttons
i1 = tk.Entry(input_frame, textvariable = size )
submit_button = tk.Button(input_frame, text = "Enter", command = control)
slider = tk.Scale(input_frame, from_=0, to = 10, variable = traf_dens, orient = tk.HORIZONTAL)
r1 = tk.Radiobutton(input_frame, text = "State Space Search", variable = alg, value = 1)
r2 = tk.Radiobutton(input_frame, text = "Genetic Algorithm", variable = alg, value = 2)
r3 = tk.Radiobutton(input_frame, text = "Both", variable = alg, value = 3)



l1.grid(row = 0, columnspan = 5)
l2.grid(row = 0, column = 0)#line 2 left
i1.grid(row = 0, column = 1)#line 2 left
l3.grid(row = 0, column = 2)#line 2 left
slider.grid(row = 0, column = 3)#line 2 left
r1.grid(row = 0, column = 4)# line 2 left
r2.grid(row = 0, column = 5)#line 2 left
r3.grid(row = 0, column = 6)#line 2 left
submit_button.grid(row = 0, column = 7)#line 2 left
l4.grid(row = 0, column = 0)#line 3 left
l6.grid(row = 0, column = 1)
l5.grid(row = 0, column = 2)#line 3 left
l7.grid(row = 0, column = 3)

main_frame.mainloop()