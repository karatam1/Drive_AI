import tkinter as tk
import random
import SSS as st
import GA as ga
import Board_Creator as bc
import time

# GUI initializer
main_frame = tk.Tk()
main_frame.geometry("7000x7000")
main_frame.title("Drive_AI UI")
main_frame.configure(bg = "SteelBlue1")


def run_alg_sss(new_board, n, alg, epoch, color_board):
        
    rules = bc.traffic_rules_gen(new_board)

    for i in range(epoch):
        
        if i % 5 == 0:
            #generates new blocks every 5 iterations
            new_board = bc.blocks_gen(new_board, n)

        new_board = bc.traffic_move(new_board, rules)
        
        new_board = alg.move(new_board)
        
        bc.re_color_board(new_board, color_board, n)
        main_frame.update() #updates/refresh the main_frame
        time.sleep(0.3)
        

def run_alg_ga(new_board, n, alg, color_board):

    #make the function call to the main GA_function that runs the entire operation
    #pass in bc board creator object
    #re_color board and traffics move, block generation, time.sleep() will occur over there instead
    #display every 10th epoch
    #either in the ga files or in main, print the epoch vs min_steps graph
    rules = bc.traffic_rules_gen(new_board)
    traffic = [color_board, rules]


    alg.start(main_frame, new_board, bc, traffic)



#processing functions
def control():
    n, density, ai_method = size.get(), traf_dens.get(), alg.get()
    color_frame = tk.Frame(main_frame, width = "7000", height = "4000", bg = "SteelBlue1")
    color_frame.grid(row = 4)
    color_board = tk.Canvas(color_frame, borderwidth = 1, width = 7000, height = 4000, bg = "SteelBlue1")
    color_board.grid(row = 0, column = 1)
    #creates the initial color_board

    color_board = bc.board_init(n, color_board)
    #resets the traffic positions incase of re-submits
    bc.positions = []
    bc.blocks = {}
    #------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    #creates new_board based on functions from Board_Creator
    new_board = bc.board_gen(n, density)   
    #prints debug board
    #for x in new_board:
    #    print(x)

    #re-colors board based on the new_board specifications for the initial board preview
    bc.re_color_board(new_board, color_board, n)
    main_frame.update()
    time.sleep(0.7)


    #holds ga initialization data: generations, string_length (17*20 rules), population size, p_mutation, p_crossover
    ga_data = [100, 850, 60, 0.001, 0.5]

    s1 = st.State_Space_Search(n, new_board)

    g1 = ga.Genetic_Alg(n, new_board, ga_data)

    #run sss
    if ai_method == 1:
        #epoch = 25
        epoch = n**2
        run_alg_sss(new_board, n, s1, epoch, color_board)
    
    #run ga
    elif ai_method == 2:
        run_alg_ga(new_board, n, g1, color_board)
    else:
        copy_board = new_board[:]

        run_alg_sss(new_board, n, s1, epoch, color_board)
        run_alg_ga(copy_board, n, g1, color_board)





###################################################################################################################################################################
#grid allocations
head_frame = tk.Frame(main_frame, width = "7000", height = "50", bg = "SteelBlue1")
input_frame = tk.Frame(main_frame, width = "7000", height = "200")
info_frame = tk.Frame(main_frame, width = "7000", height = "25")

head_frame.grid(row = 0, sticky = "nw")
input_frame.grid(row = 1, sticky = "nw")
info_frame.grid(row = 3, sticky = "nw")


#labels 
l1 = tk.Label(head_frame, text = "Choose the settings from the given options", bg = "SteelBlue1")
l2 = tk.Label(input_frame, text = "Grid Size:")
l3 = tk.Label(input_frame, text = "Density:")
l4 = tk.Label(info_frame, text = "Epoch #")
l5 = tk.Label(info_frame, text = "Min_steps:")


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
l4.grid(row = 0, column = 0, columnspan = 4)#line 3 left
l5.grid(row = 0, column = 7)#line 3 left

main_frame.mainloop()