import pygame as pg

# intialize pygame
pg.init()

# constants
SCRW = 700
SCRH = 550
BOARD_SIZE = 306
BOARD_SX = SCRW//2 - BOARD_SIZE//2
BOARD_SY = SCRH//2 - BOARD_SIZE//2
CELL_SIZE = BOARD_SIZE // 3
ST_BTN_W = 300
ST_BTN_H = 75
ST_BTN_GAP = 30
ST_BTN_X = SCRW//2 - ST_BTN_W//2
ST_BTN_Y = SCRH//2 - ST_BTN_H - ST_BTN_GAP
PLAYERS_FONT_SIZE = 100
START_FONT_SIZE = 48
SCORE_FONT_SIZE = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FPS = 15
DELAY = 50
# variables
screen = pg.display.set_mode((SCRW, SCRH))
clock = pg.time.Clock()
players_font = pg.font.SysFont('Comic Sans', PLAYERS_FONT_SIZE)
start_font = pg.font.SysFont('Comic Sans', START_FONT_SIZE)
score_font = pg.font.SysFont('Comic Sans', SCORE_FONT_SIZE)

# functions
def get_indices():
    mx, my = pg.mouse.get_pos()
    return (mx-BOARD_SX) // CELL_SIZE, (my-BOARD_SY) // CELL_SIZE


def detect_win(board):
    # rows
    for row in board:
        if len(set(row)) == 1:
            return row[0]
    # coulmns
    for i in range(3):
        col = [board[0][i], board[1][i], board[2][i]]
        if len(set(col)) == 1:
            return col[0]
    # diagonals
    diag1 = [board[0][0], board[1][1], board[2][2]]
    if len(set(diag1)) == 1:
        return diag1[0]
    diag2 = [board[0][2], board[1][1], board[2][0]]
    if len(set(diag2)) == 1:
        return diag2[0]


def handle_start_screen():
    mx, my = pg.mouse.get_pos()
    if mx in range(ST_BTN_X, ST_BTN_X + ST_BTN_W)\
            and my in range(ST_BTN_Y, ST_BTN_Y + ST_BTN_H):
                return 1
    y = ST_BTN_Y + ST_BTN_H + ST_BTN_GAP
    if mx in range(ST_BTN_X, ST_BTN_X + ST_BTN_W)\
            and my in range(y, y + ST_BTN_H):
                return 2
    return 0


def full_board(board):
    for row in board:
        for val in row:
            if val is None:
                return False
    return True


def draw_score(scores):
    i = 0
    for k, v in scores.items():
        text = score_font.render(f'{k}: {v}', True, WHITE)
        screen.blit(text, [25 + i*100, 25])
        i += 1


def draw_board():
    for i in range(1, 3):
        # horizontal lines
        hx = BOARD_SX
        hy = BOARD_SY + CELL_SIZE*i
        pg.draw.line(screen, WHITE, (hx, hy), (hx + BOARD_SIZE, hy))
        # vertical lines
        vx = BOARD_SX + CELL_SIZE*i
        vy = BOARD_SY
        pg.draw.line(screen, WHITE, (vx, vy), (vx, vy + BOARD_SIZE))


def draw_players(board):
    for r in range(3):
        for c in range(3):
            if board[r][c] is not None:
                text = players_font.render(board[r][c], True, WHITE)
                tw = text.get_width()
                th = text.get_height()
                x = c*CELL_SIZE + BOARD_SX + CELL_SIZE//2 - tw//2
                y = r*CELL_SIZE + BOARD_SY + CELL_SIZE//2 - th//2
                screen.blit(text, (x, y))


def draw_start_screen():
    for i in range(2):
        y = ST_BTN_Y + i*(ST_BTN_GAP+ST_BTN_H)
        pg.draw.rect(screen, WHITE, (ST_BTN_X, y, ST_BTN_W, ST_BTN_H), 1)
        text = start_font.render(f'{i + 1} PLAYER{"S"*i}', True, WHITE)
        tx = ST_BTN_X + ST_BTN_W//2 - text.get_width()//2
        ty = y + ST_BTN_H//2 - text.get_height()//2
        screen.blit(text, (tx, ty))


def draw(board, start_screen, score):
    screen.fill(BLACK)

    if start_screen:
        draw_start_screen()
    else:
        draw_score(score)
        draw_board()
        draw_players(board)

    pg.display.update()

# main function
if __name__ == '__main__':
    run = True
    start_screen = True
    ai = False
    board = [[None for _ in range(3)] for _ in range(3)]
    turn = 'X'
    score = {'X': 0, 'O': 0}

    while run:
        draw(board, start_screen ,score)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if start_screen:
                    ssv = handle_start_screen()
                    if ssv:
                        start_screen = False
                    if ssv == 1:
                        ai = True
                    continue

                if ai:
                    continue

                c, r = get_indices()
                if c in range(3) and r in range(3):
                    if board[r][c] is None:
                        board[r][c] = turn
                        win = detect_win(board)
                        if win is not None or full_board(board):
                            if win is not None:
                                score[win] += 1
                            board = [[None for _ in range(3)] for _ in range(3)]
                            turn = 'X'
                            continue

                        turn = 'O' if turn == 'X' else 'X'

        clock.tick(FPS)
        pg.time.delay(DELAY)

    quit()
