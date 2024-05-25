from copy import deepcopy
import pygame
import random
from random import randint, shuffle


def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None


def valid(board, pos, num):
    row, col = pos
    # Check row and column
    if any(board[row][j] == num for j in range(9)) or any(board[i][col] == num for i in range(9)):
        return False
    # Check 3x3 box
    start_i, start_j = row - row % 3, col - col % 3
    return not any(board[start_i + i][start_j + j] == num for i in range(3) for j in range(3))


def solve(board):
    empty = find_empty(board)
    if not empty:
        return True

    for num in range(1, 10):
        if valid(board, empty, num):
            board[empty[0]][empty[1]] = num
            if solve(board):
                return True
            board[empty[0]][empty[1]] = 0
    return False


def generate_board():
    board = [[0 for _ in range(9)] for _ in range(9)]
    for i in range(0, 9, 3):
        nums = list(range(1, 10))
        shuffle(nums)
        for row in range(3):
            for col in range(3):
                board[i + row][i + col] = nums.pop()

    def fill_cells(board, row, col):
        if row == 9:
            return True
        if col == 9:
            return fill_cells(board, row + 1, 0)
        if board[row][col] != 0:
            return fill_cells(board, row, col + 1)

        for num in range(1, 10):
            if valid(board, (row, col), num):
                board[row][col] = num
                if fill_cells(board, row, col + 1):
                    return True
        board[row][col] = 0
        return False

    fill_cells(board, 0, 0)
    for _ in range(randint(55, 65)):
        board[randint(0, 8)][randint(0, 8)] = 0

    return board


pygame.init()


class Board:
    def __init__(self, window):
        self.board = generate_board()
        self.solvedBoard = deepcopy(self.board)
        solve(self.solvedBoard)
        self.tiles = [
            [Tile(self.board[i][j], window, i * 60, j * 60) for j in range(9)]
            for i in range(9)
        ]
        self.window = window

    def draw_board(self):
        for i in range(9):
            for j in range(9):
                if j % 3 == 0 and j != 0:
                    pygame.draw.line(self.window, (0, 0, 0), (j // 3 * 180, 0), (j // 3 * 180, 540), 4)
                if i % 3 == 0 and i != 0:
                    pygame.draw.line(self.window, (0, 0, 0), (0, i // 3 * 180), (540, i // 3 * 180), 4)
                self.tiles[i][j].draw((0, 0, 0), 1)
                if self.tiles[i][j].value != 0:
                    self.tiles[i][j].display(self.tiles[i][j].value, (21 + j * 60, 16 + i * 60), (0, 0, 0))
        pygame.draw.line(self.window, (0, 0, 0), (0, 540), (540, 540), 4)

    def deselect(self, tile):
        for row in self.tiles:
            for t in row:
                if t != tile:
                    t.selected = False

    def redraw(self, keys, wrong):
        self.window.fill((255, 255, 255))
        self.draw_board()
        for row in self.tiles:
            for t in row:
                if t.selected:
                    t.draw((50, 205, 50), 4)
                elif t.correct:
                    t.draw((34, 139, 34), 4)
                elif t.incorrect:
                    t.draw((255, 0, 0), 4)

        for value in keys:
            self.tiles[value[0]][value[1]].display(keys[value], (21 + value[0] * 60, 16 + value[1] * 60), (128, 128, 128))

        if wrong > 0:
            font = pygame.font.SysFont("Bauhaus 93", 30)
            text = font.render("X", True, (255, 0, 0))
            self.window.blit(text, (10, 554))

            font = pygame.font.SysFont("Bahnschrift", 40)
            text = font.render(str(wrong), True, (0, 0, 0))
            self.window.blit(text, (32, 542))

        pygame.display.flip()

    def visualSolve(self, wrong):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        empty = find_empty(self.board)
        if not empty:
            return True

        for num in range(1, 10):
            if valid(self.board, empty, num):
                self.board[empty[0]][empty[1]] = num
                self.tiles[empty[0]][empty[1]].value = num
                self.tiles[empty[0]][empty[1]].correct = True
                self.redraw({}, wrong)

                if self.visualSolve(wrong):
                    return True

                self.board[empty[0]][empty[1]] = 0
                self.tiles[empty[0]][empty[1]].value = 0
                self.tiles[empty[0]][empty[1]].incorrect = True
                self.tiles[empty[0]][empty[1]].correct = False
                pygame.time.delay(63)
                self.redraw({}, wrong)

    def hint(self, keys):
        while True:
            i, j = randint(0, 8), randint(0, 8)
            if self.board[i][j] == 0:
                if (j, i) in keys:
                    del keys[(j, i)]
                self.board[i][j] = self.solvedBoard[i][j]
                self.tiles[i][j].value = self.solvedBoard[i][j]
                return True
            elif self.board == self.solvedBoard:
                return False


class Tile:
    def __init__(self, value, window, x, y):
        self.value = value
        self.window = window
        self.rect = pygame.Rect(x, y, 60, 60)
        self.selected = False
        self.correct = False
        self.incorrect = False

    def draw(self, color, thickness):
        pygame.draw.rect(self.window, color, self.rect, thickness)

    def display(self, value, position, color):
        font = pygame.font.SysFont("lato", 45)
        text = font.render(str(value), True, color)
        self.window.blit(text, position)

    def clicked(self, mousePos):
        if self.rect.collidepoint(mousePos):
            self.selected = True
        return self.selected


def main():
    screen = pygame.display.set_mode((540, 590))
    screen.fill((255, 255, 255))
    pygame.display.set_caption("Sudoku Solver")

    font = pygame.font.SysFont("Bahnschrift", 40)
    text = font.render("Generating", True, (0, 0, 0))
    screen.blit(text, (175, 245))

    text = font.render("Random Grid", True, (0, 0, 0))
    screen.blit(text, (156, 290))
    pygame.display.flip()

    wrong = 0
    board = Board(screen)
    selected = (-1, -1)
    keyDict = {}
    solved = False

    keysToValues = {
        pygame.K_1: 1,
        pygame.K_2: 2,
        pygame.K_3: 3,
        pygame.K_4: 4,
        pygame.K_5: 5,
        pygame.K_6: 6,
        pygame.K_7: 7,
        pygame.K_8: 8,
        pygame.K_9: 9,
    }

    while not solved:
        if board.board == board.solvedBoard:
            solved = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                mousePos = pygame.mouse.get_pos()
                for i in range(9):
                    for j in range(9):
                        if board.tiles[i][j].clicked(mousePos):
                            selected = (i, j)
                            board.deselect(board.tiles[i][j])
            elif event.type == pygame.KEYDOWN:
                if board.board[selected[1]][selected[0]] == 0 and selected != (-1, -1):
                    if event.key in keysToValues:
                        keyDict[selected] = keysToValues[event.key]
                    elif event.key == pygame.K_BACKSPACE and selected in keyDict:
                        board.tiles[selected[0]][selected[1]].value = 0
                        del keyDict[selected]
                    elif event.key == pygame.K_RETURN and selected in keyDict:
                        row, col = selected[1], selected[0]
                        if keyDict[selected] != board.solvedBoard[row][col]:
                            wrong += 1
                            board.tiles[col][row].incorrect = True
                            pygame.time.delay(130)
                        else:
                            board.tiles[col][row].value = keyDict[selected]
                            board.tiles[col][row].correct = True
                            board.board[row][col] = keyDict[selected]
                        del keyDict[selected]
                    elif event.key == pygame.K_h:
                        board.hint(keyDict)
                    elif event.key == pygame.K_SPACE:
                        board.visualSolve(wrong)
        board.redraw(keyDict, wrong)

    # font = pygame.font.SysFont("Bahnschrift", 40)
    # text = font.render("You Won!", True, (0, 0, 0))
    # screen.blit(text, (225, 550))
    # pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()


if __name__ == "__main__":
    main()
