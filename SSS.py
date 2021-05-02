class State_Space_Search:

    def __init__(self, n, gen_board):
        self.n = n
        self.gen_board = gen_board
        self.curr = [n-1,0]
        self.goal = [0,n-1]

 
    def move(self, gen_board):
        #Important step, always make sure local gen_board is updated to the latest gen_board
        self.gen_board = gen_board

        if (self.curr[0] != self.goal[0]) or self.curr[1] != self.goal[1]:
            i,j = self.curr[0], self.curr[1]
            self.gen_board[i][j] = 1
            prev = (i, j) # In case we need to go back

            # moving vehicle
            dir = self.min_cost()
            if dir == "u":
                i = self.go_up(self.curr)
                #print("Going up")
            elif dir == "r":
                j = self.go_right(self.curr)
                #print("Going right")
            elif dir == "l":
                j = self.go_left(self.curr)
                #print("Going left")
            else:
               pass

            #important - flip position
            # if coords have 1, flip position, else if we hit an obstacle, revert to prev coords
            if gen_board[i][j] == 1:
                self.gen_board[i][j] = 9
            else:
                i, j = prev[0], prev[1]
                self.gen_board[i][j] = 9
            #important - update curr after finalizing move
            self.curr = [i, j]

        return self.gen_board, self.curr


    def go_right(self, curr):
        i, j = curr[0], curr[1]
        if j < self.n-1:
            j += 1
        return j

    def go_left(self, curr):
        i, j = curr[0], curr[1]
        if j > 0:
            j -= 1
        return j

    def go_up(self, curr):
        i, j = curr[0], curr[1]
        if i > 0:
            i -= 1
        return i

    # Strategy Prioritizes Moving the the Right Direction
    # SSS calculates the costs of movement based on different views of the agent, two positions in advance
    def min_cost(self):
        r = self.right_cost()
        l = self.left_cost()
        u = self.up_cost()

        #print("r : " + str(r) + ",l : " + str(l) + ",u : " + str(u))

        m = min([r, l, u])

        if m == u:
            return "u"
        elif m == r:
            return "r"
        elif m == l:
            return "l"
        elif r == l:
            return "r"
        else:
            return "stay"

    def right_cost(self):
        cost = 0
        i, j = self.curr[0], self.curr[1]
        if j+1 > self.n-1:
            return 100

        # right 1
        if j + 1 < self.n :
            if self.gen_board[i][j+1] == 2:
                cost += 2
            elif self.gen_board[i][j+1] == 0:
                cost += 1
            else:
                pass

        # right 2
        if j+2 < self.n :
            if self.gen_board[i][j+2] == 2:
                cost += 2
            elif self.gen_board[i][j+2] == 0:
                cost += 1
            else:
                pass

        # up 1 right 1
        if j + 1 < self.n and i - 1 >= 0:
            if self.gen_board[i-1][j + 1] == 2:
                cost += 2
            elif self.gen_board[i - 1][j + 1] == 0:
                cost += 1
            else:
                pass

        # up 2 right 1
        if j + 1 < self.n and i - 2 >= 0:
            if self.gen_board[i - 2][j + 1] == 2:
                cost += 2
            elif self.gen_board[i - 2][j + 1] == 0:
                cost += 1
            else:
                pass

        # up 2 right 2
        if j + 2 < self.n and i - 2 >= 0:
            if self.gen_board[i - 2][j + 2] == 2:
                cost += 2
            elif self.gen_board[i - 2][j + 2] == 0:
                cost += 1
            else:
                pass

        return cost - 2

    def left_cost(self):
        cost = 0
        i, j = self.curr[0], self.curr[1]

        # reach edge
        if j - 1 < 0:
            return 100

        # left 1
        if self.gen_board[i][j - 1] == 2:
            cost += 2
        elif self.gen_board[i][j - 1] == 0:
            cost += 1
        else:
            pass

        # left 2
        if self.gen_board[i][j - 2] == 2:
            cost += 2
        elif self.gen_board[i][j - 2] == 0:
            cost += 1
        else:
            pass

        # up 1 left 1
        if self.gen_board[i - 1][j - 1] == 2:
            cost += 2
        elif self.gen_board[i - 1][j - 1] == 0:
            cost += 1
        else:
            pass

        # up 2 left 1
        if self.gen_board[i - 2][j - 1] == 2:
            cost += 2
        elif self.gen_board[i - 2][j - 1] == 0:
            cost += 1
        else:
            pass

        # up 2 left 2
        if self.gen_board[i - 2][j - 2] == 2:
            cost += 2
        elif self.gen_board[i - 2][j - 2] == 0:
            cost += 1
        else:
            pass

        return cost

    def up_cost(self):
        cost = 0
        i, j = self.curr[0], self.curr[1]

        if i - 1 < 0:
            return 100

        if self.gen_board[i - 1][j] == 0:
            return 100

        # up 1
        if i - 1 >= 0:
            if self.gen_board[i - 1][j] == 2:
                cost += 2
            elif self.gen_board[i - 1][j] == 0:
                cost += 1
            else:
                pass

        # up 2
        if i - 2 >= 0:
            if self.gen_board[i - 2][j] == 2:
                cost += 2
            elif self.gen_board[i - 2][j] == 0:
                cost += 1
            else:
                pass

        # up 2 left 1
        if i - 2 >= 0 and j - 1 >= 0:
            if self.gen_board[i - 2][j - 1] == 2:
                cost += 2
            elif self.gen_board[i - 2][j - 1] == 0:
                cost += 1
            else:
                pass

        # up 2 left 2
        if i - 2 >= 0 and j - 2 >= 0:
            if self.gen_board[i - 2][j - 2] == 2:
                cost += 2
            elif self.gen_board[i - 2][j - 2] == 0:
                cost += 1
            else:
                pass

        # up 2 right 1
        if i - 2 >= 0 and j + 1 < self.n:
            if self.gen_board[i - 2][j + 1] == 2:
                cost += 2
            elif self.gen_board[i - 2][j + 1] == 0:
                cost += 1
            else:
                pass

        # up 2 right 2
        if i - 2 >= 0 and j + 2 < self.n:
            if self.gen_board[i - 2][j + 2] == 2:
                cost += 2
            elif self.gen_board[i - 2][j + 2] == 0:
                cost += 1
            else:
                pass

        # up 1 left 1
        if i - 1 >= 0 and j - 1 >= 0:
            if self.gen_board[i - 1][j - 1] == 2:
                cost += 2
            elif self.gen_board[i - 1][j - 1] == 0:
                cost += 1
            else:
                pass

        # up 1 left 2
        if i - 1 >= 0 and j - 2 >= 0:
            if self.gen_board[i - 1][j - 2] == 2:
                cost += 2
            elif self.gen_board[i - 1][j - 2] == 0:
                cost += 1
            else:
                pass

        # up 1 right 1
        if i - 1 >= 0 and j + 1 < self.n:
            if self.gen_board[i - 1][j + 1] == 2:
                cost += 2
            elif self.gen_board[i - 1][j + 1] == 0:
                cost += 1
            else:
                pass

        # up 1 right 2
        if i - 1 >= 0 and j + 2 < self.n:
            if self.gen_board[i - 1][j + 2] == 2:
                cost += 2
            elif self.gen_board[i - 1][j + 2] == 0:
                cost += 1
            else:
                pass

        return cost - 2
        