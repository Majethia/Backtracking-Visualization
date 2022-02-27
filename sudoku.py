import sys
import pygame

RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (156, 156, 156)
LBLUE = (153, 255, 255)
TEXTC = (51, 51, 255)
GREEN = (90, 255, 0)


WINDOW_HEIGHT = 640
WINDOW_WIDTH = 640
FPS = 250

pygame.init()
pygame.font.init()
font = pygame.font.SysFont('Calibri', 40)


SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
CLOCK = pygame.time.Clock()
SCREEN.fill(WHITE)


class Node():
    def __init__(self, x, y, val: int = 0):
        self.val = val
        self.x = x
        self.y = y
        self.color = WHITE
        self.txtclr = TEXTC

    def draw(self, SCREEN):
        x = self.x * WINDOW_HEIGHT / 9
        y = self.y * WINDOW_HEIGHT / 9
        rectangle = pygame.Rect(x, y, WINDOW_HEIGHT / 9, WINDOW_HEIGHT / 9)
        rectangle1 = pygame.Rect(x+2, y+2, WINDOW_HEIGHT / 9 - 4, WINDOW_HEIGHT / 9 - 4)

        pygame.draw.rect(SCREEN, BLACK, rectangle)
        pygame.draw.rect(SCREEN, self.color, rectangle1)
        if self.val != 0:
            textsurface = font.render(str(self.val), False, self.txtclr)
            SCREEN.blit(textsurface,(x + 27, y + 17))

def find_empty(bo):
    for i in range (9):
        for j in range (9):
            if bo[i][j] == 0:
                return i,j

def valid(bo, num, pos):
    for i in range(9):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False
    
    for i in range(9):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y * 3, box_y*3 + 2):
        for j in range(box_x * 3, box_x*3 + 2):
            if bo[i][j] == num and pos != (i,j):
                return False
    
    return True

def convert_input(input_from_window):
    d = []
    for i in range(81):
        d.append(int(input_from_window[i]))

    return [d[0:9], d[9:18], d[18:27], d[27:36], d[36:45], d[45:54], d[54:63], d[63:72], d[72:81]]

def draw_grid(b, b1, cursor, clr):
    for i in range(9):
        for j in range(9):
            n = Node(i, j)
            n.val = b[i][j]
            if b[i][j] == b1[i][j]:
                n.txtclr = BLACK
            else:
                n.txtclr = clr
            box_x = i // 3
            box_y = j // 3
            if (box_x, box_y) in ((0, 0), (0, 2), (1, 1), (2, 0), (2, 2)):
                n.color = LBLUE
            if cursor[0] != 10:
                if [i, j] == [cursor[0], cursor[1]]:
                    n.color = GREY
                    if b1[i][j] == 0 and cursor[2] != 0:
                        if b[i][j] == cursor[2]:
                            b[i][j] = 0
                            cursor[2] = 0
                        else:
                            b[i][j] = cursor[2]
                            cursor[2] = 0
            n.draw(SCREEN)

def main():
    run = True
    input_board = '100904082052680300864200910010049806498300701607010093086035209509002130030497008'
    b = convert_input(input_board)
    b1 = convert_input(input_board)
    cursor = [0, 0, 0]

    while run:
        draw_grid(b, b1, cursor, BLACK)    
        pygame.display.update()   

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    run = False
                elif event.key == pygame.K_DOWN:
                    if cursor[1] < 9:
                        cursor[1] += 1
                        cursor[2] = 0
                elif event.key == pygame.K_UP:
                    if cursor[1] > 0:
                        cursor[1] -= 1
                        cursor[2] = 0
                elif event.key == pygame.K_RIGHT:
                    if cursor[0] < 9:
                        cursor[0] += 1
                        cursor[2] = 0
                elif event.key == pygame.K_LEFT:
                    if cursor[0] > 0:
                        cursor[0] -= 1
                        cursor[2] = 0
                elif event.key == pygame.K_KP0:
                    cursor[2] = 0
                elif event.key == pygame.K_KP1:
                    cursor[2] = 1
                elif event.key == pygame.K_KP2:
                    cursor[2] = 2
                elif event.key == pygame.K_KP3:
                    cursor[2] = 3
                elif event.key == pygame.K_KP4:
                    cursor[2] = 4
                elif event.key == pygame.K_KP5:
                    cursor[2] = 5
                elif event.key == pygame.K_KP6:
                    cursor[2] = 6
                elif event.key == pygame.K_KP7:
                    cursor[2] = 7
                elif event.key == pygame.K_KP8:
                    cursor[2] = 8
                elif event.key == pygame.K_KP9: 
                    cursor[2] = 9
    
    s = True

    while s:

        draw_grid(b, b1, cursor, GREEN)    
        pygame.display.update()

        def solve(b):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            find = find_empty(b)
            if find == None:
                return True
            else:
                row, col = find

            for i in range(1,10):
                n = Node(row, col, i)
                if not valid(b, n.val, (row, col)):
                    n.txtclr = RED
                box_x = row // 3
                box_y = col // 3
                if (box_x, box_y) in ((0, 0), (0, 2), (1, 1), (2, 0), (2, 2)):
                    n.color = LBLUE
                n.draw(SCREEN)
                CLOCK.tick(FPS)
                pygame.display.update()
                if valid(b, i, (row, col)):
                    b[row][col] = i

                    if solve(b):
                        return True
                    else:
                        b[row][col] = 0
                        n = Node(row, col, 0)
                        box_x = row // 3
                        box_y = col // 3
                        if (box_x, box_y) in ((0, 0), (0, 2), (1, 1), (2, 0), (2, 2)):
                            n.color = LBLUE
                        n.draw(SCREEN)
                        CLOCK.tick(FPS)
                        pygame.display.update()
            n.val = 0
            box_x = row // 3
            box_y = col // 3
            if (box_x, box_y) in ((0, 0), (0, 2), (1, 1), (2, 0), (2, 2)):
                n.color = LBLUE
            n.draw(SCREEN)
            CLOCK.tick(FPS)
            pygame.display.update()
            return False

        solve(b)

if __name__ == "__main__":
    main()

