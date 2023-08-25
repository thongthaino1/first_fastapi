#
#
#
# global board_glo
# board_glo =  [["5","3",".",".","7",".",".",".","."],
#                      ["6",".",".","1","9","5",".",".","."],
#                      [".","9","8",".",".",".",".","6","."],
#                      ["8",".",".",".","6",".",".",".","3"],
#                      ["4",".",".","8",".","3",".",".","1"],
#                      ["7",".",".",".","2",".",".",".","6"],
#                      [".","6",".",".",".",".","2","8","."],
#                      [".",".",".","4","1","9",".",".","5"],
#                      [".",".",".",".","8",".",".","7","9"]]
#
#
# class Solution:
#     def solveSudoku(self, board: list[list[str]] = board_glo ) -> None:
#         """
#         Do not return anything, modify board in-place instead.
#         """
#         # board_glo = board
#         self.solve()
#         # board_glo[0][0] = 1
#         print(board_glo)
#     def possible(self,y,x,n:str) :
#         for i in range(9) :
#         # print(board_glo[4][5] == 3)
#             if board_glo[y][i] == n :
#                 return False
#             if board_glo[i][x] == n :
#                 # print(123)
#                 # print(board_glo[y][i],board_glo[i][x])
#                 return False
#         x0 = (x // 3)  * 3
#         y0 = (y // 3)  * 3
#         for i in range(3) :
#             for j in range(3) :
#                 if board_glo[y0+i][x0+j] == n :
#                     return False
#         return True
#     def solve(self) :
#         # board_glo[i][j] =
#         for i in range(9) :
#             for j in range(9) :
#                 # board_glo[i][j] = 1
#                 if board_glo[i][j] == "." :
#                     for n in range (1,10) :
#                         if self.possible(i,j,n) :
#                             board_glo[i][j] = n
#                             self.solve()
#                             board_glo[i][j] = "."
#                     return
#
#
# c =Solution ()
# c.solveSudoku()
#
a = "a"
print(str("dfgdgffdg"))