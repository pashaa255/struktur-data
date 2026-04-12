maze = [
    ["S", " ", "*", " "],
    ["*", " ", "*", " "],
    [" ", " ", " ", "E"]
]

stack = [(0,0)]  
visited = set()

while stack:
    r, c = stack[-1]

    if maze[r][c] == "E":
        print("KETEMU JALAN!")
        break

    visited.add((r,c))

    for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
        nr, nc = r+dr, c+dc

        if (0 <= nr < 3 and 0 <= nc < 4 and
            maze[nr][nc] != "*" and
            (nr,nc) not in visited):

            stack.append((nr,nc))
            break
    else:
        stack.pop()
"======================================="

import random

class Maze:
    WALL = "*"
    PATH = "x"
    TRIED = "o"
    EMPTY = " "

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = self.generate_maze()
        self.start = (0, 0)
        self.exit = (rows - 1, cols - 1)

        self.grid[0][0] = "S"
        self.grid[rows - 1][cols - 1] = "E"

    def generate_maze(self):
        maze = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                if random.random() < 0.3:
                    row.append(self.WALL)
                else:
                    row.append(self.EMPTY)
            maze.append(row)
        return maze

    def print_maze(self):
        for row in self.grid:
            print(" ".join(row))
        print()

    def valid_move(self, r, c):
        return (0 <= r < self.rows and
                0 <= c < self.cols and
                self.grid[r][c] in [self.EMPTY, "E"])

    def solve(self):
        stack = []
        stack.append(self.start)

        while stack:
            r, c = stack[-1]

            if (r, c) == self.exit:
                return True

            # cek 4 arah
            moved = False
            for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
                nr, nc = r + dr, c + dc

                if self.valid_move(nr, nc):
                    if self.grid[nr][nc] != "E":
                        self.grid[nr][nc] = self.PATH
                    stack.append((nr, nc))
                    moved = True
                    break

            if not moved:
                # jalan buntu → mundur
                if self.grid[r][c] not in ["S", "E"]:
                    self.grid[r][c] = self.TRIED
                stack.pop()

        return False


# ===== MAIN PROGRAM =====
rows = int(input("Masukkan jumlah baris: "))
cols = int(input("Masukkan jumlah kolom: "))

maze = Maze(rows, cols)

print("\nLabirin Awal:")
maze.print_maze()

if maze.solve():
    print("Jalur ditemukan!\n")
else:
    print("Tidak ada jalur!\n")

print("Labirin Setelah Diselesaikan:")
maze.print_maze()
