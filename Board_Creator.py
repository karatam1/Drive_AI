import random

positions = []
blocks = {}

def board_init(ns, color_board):
    #--- Creates the initial colored board ---------------------------------------------------------------------------------------------------------------------
    d1, d2 = 60, 32

    if ns > 20:
        d1, d2 = 45, 24

    k1, k2 = ns, 1
    x1, y1 = d1,0
    x2, y2 = d1*2, d2
    for i in range(d2, d2*(ns+1), d2):
        #color_board.create_text(0, y1, 30, y2, fill = 'white')
        color_board.create_text(d2-2, y1+14, fill = 'black', text = 'y'+str(k1))
        k1-=1
        for j in range(d1*2, d1*(ns+2), d1):
            color_board.create_rectangle(x1, y1, j, i, fill = 'grey')

            x1+=d1
        y1+=d2
        x1 = d1
        x2 = d1*2
        y2+=d2

    #create numbered cols
    for t in range(d1, d1*(ns+1), d1):
        color_board.create_text(t+16, y1+7, fill = 'black', text = 'x'+str(k2))
        k2+=1

    return color_board


def blocks_gen(gen_board, n):

    bl = n / 5
    v = 0
    events = [-2,-3,-4,-5]


    while v < bl:
        a = random.randint(0, n-1)
        b = random.randint(0, n-1)

        if gen_board[a][b] == 1:
            z = random.sample(events, 1)
            gen_board[a][b] == z[0]

            blocks[gen_board[a][b]] = random.randint(8, 20)
            v+=1

    return gen_board



def traffic_gen(n, density, gen_board):
    
    #to find find remaining open positions
    rv = float(density)/10
    cap = (n**2)/4
    cap = float(cap*rv)
    v = 0

    while v < cap:
        a = random.randint(0, n-1) 
        b = random.randint(0, n-1)

        if gen_board[a][b] == 1:
            gen_board[a][b] = 2
            v+=1
            positions.append([a,b])
    return gen_board

def traffic_rules_gen(gen_board):

    rem = []
    rules = []
    #remove traffic overlapped by land
    for p in positions:
        i, j = p[0], p[1]

        if gen_board[i][j] != 2:
            rem.append(p)
    for r in rem:
        positions.remove(r)

    #The traffic has now been finalized
    #provide randomly generated rules for each position
    rset = [[-1, 0], [0, -1], [0, 1]]
    for i in range(len(positions)):
        random.shuffle(rset)
        rules.append(rset[:])
    return rules


def traffic_move(gen_board, rules):

    ln = len(gen_board)-1
    for p in range(len(positions)):
        i, j = positions[p][0], positions[p][1]

        if gen_board[i][j] in blocks:
            blocks[gen_board[i][j]] -=1

            if blocks[gen_board[i][j]] == 0:
                del blocks[gen_board[i][j]]
        else:    
            for f in range(3):
                a,b = i+rules[p][f][0], j+rules[p][f][1]
                
                if a >= 0 and a <= ln and b >= 0 and b <= ln:
                    
                    #detects empty position
                    if gen_board[a][b] == 1:
                        #resets the current position of the board to a road
                        gen_board[i][j] = 1
                        #updates the position
                        positions[p] = [a, b]
                        #changes the traffic position on the board
                        gen_board[a][b] = 2
                        break
                    #detects crashes
                    elif gen_board[a][b] == 2 and f == 2:
                        #resets the current position of the board to a road
                        gen_board[i][j] = 1
                        #updates the position
                        positions[p] = [a,b]
                        gen_board[a][b] = -1
                        blocks[gen_board[a][b]] = 15
                        break

                    #if its not a road or a car, then its either land or a road block and it has to avoid it

                #the traffic is set to go off the board, need to regenerate a position for it
                #helps in de-cluttering the board
                else:
                    u1, u2 = 0,0
                    while gen_board[u1][u2] != 1:
                        u1 = random.randint(0, len(gen_board)-1)
                        u2 = random.randint(0, len(gen_board)-1)

                    gen_board[i][j] = 1
                    positions[p] = [u1, u2]
                    gen_board[u1][u2] = 2
                    i, j = u1, u2
              

    return gen_board


def board_gen(n, density):
    # 0 represents land
    # 1 represents road
    # 2 represents traffic
    # 9 is curr location

    #generates the board
    gen_board = [([1]*n) for x in range(n)]


    #generates the random cars
    #generate random number between 0 and n twice (one for row and one for col)
    #do this in a while loop as long as it does not generate on a land cell or current location cell
    gen_board = traffic_gen(n, density, gen_board)
    
    #adds the land to the board
    gen_board = add_land(gen_board, n)

    #sets the initial position
    gen_board[n-1][0] = 9

    return gen_board



def add_land(gen_board, n):

    land = 4
    #sets the island size
    if 0 < n < 10:
        land = 2
    elif 10 <= n <= 20:
        land = 2

    #adds the land blocks to the board
    i, j = 1,0
    while i < n-land and j < n-land:
        
        for z in range(land):
            for k in range(land): 
                gen_board[i+z][j+k] = 0
        j += (land+1)
        if j >= n-land-1:
            j = 0
            i+=(land+1)

    return gen_board



def re_color_board(gen_board, color_board, n):

    d1, d2 = 60, 32

    if n > 20:
        d1, d2 = 45, 24

    x1, y1 = d1,0
    x2, y2 = 2*d1, d2
    r, c = 0,0
    for i in range(d2, d2*(n+1), d2):
        for j in range(2*d1, d1*(n+2), d1):
            if gen_board[r][c] == 0:
                color_board.create_rectangle(x1, y1, j, i, fill = 'green4')

            elif gen_board[r][c] == 9:
                color_board.create_rectangle(x1, y1, j, i, fill = 'red3')
            
            elif gen_board[r][c] == 2:
                color_board.create_rectangle(x1, y1, j, i, fill = 'royal blue')

            elif gen_board[r][c] < 0:
                color_board.create_rectangle(x1, y1, j, i, fill = 'DarkOrange1')
            
            else:
                color_board.create_rectangle(x1, y1, j, i, fill = 'grey')
            x1+=d1
            c+=1
        y1+=d2
        x1 = d1
        x2 = d1*2
        c = 0
        r+=1


