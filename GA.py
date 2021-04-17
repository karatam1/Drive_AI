class Genetic_Alg:


    def __init__(self, n, gen_board):

        self.n = n
        self.gen_board = gen_board
        self.curr = [n-1,0]

    def move(self, gen_board):
        #Important step, always make sure local gen_board is updated to the latest gen_board
        self.gen_board = gen_board

        i,j = self.curr[0], self.curr[1]

        if i >= 0:
            if self.gen_board[i-1][j] == 1: 
                self.gen_board[i][j] = 1
                i-=1
        

        self.gen_board[i][j] = 9
        self.curr = [i, j]

        return self.gen_board