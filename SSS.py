class State_Space_Search:

    def __init__(self, n, gen_board):
        self.n = n
        self.gen_board = gen_board
        self.curr = [n-1,0]

    #DO NOT MODIFTY MOVE METHOD SIGNATURE AND RETURN STATEMENT
    def move(self, gen_board):
        #Important step, always make sure local gen_board is updated to the latest gen_board
        self.gen_board = gen_board

        i,j = self.curr[0], self.curr[1]
        self.gen_board[i][j] = 1
        if j < self.n-1:
            j+=1
        #important - flip position
        self.gen_board[i][j] = 9
        #important - update curr after finalizing move
        self.curr = [i, j]

        return self.gen_board