# Tic-Tac-Toe 2 (Ultimate Tic-Tac-Toe) for the TI-84 Evo
# 9 small boards inside 1 big board. Where you play in a small board
# decides which small board the other player must use next.
# Keys: arrows = move, enter = place, clear = quit
import random
from ti_draw import clear, set_color, draw_text
from ti_draw import fill_rect as ti_fill_rect
try:
    from ti_draw import get_screen_dim
    SW, SH = get_screen_dim()
except:
    SW, SH = 319, 209

# Keep every box inside the screen and never stop the game over one box.
# The Evo draws boxes 1 pixel too small, so we ask for 1 pixel more.
def fill_rect(x, y, w, h):
    if x < 0:
        w, x = w + x, 0
    if y < 0:
        h, y = h + y, 0
    w, h = min(w, SW - x), min(h, SH - y)
    if w > 0 and h > 0:
        try:
            ti_fill_rect(x, y, w + 1, h + 1)
        except:
            pass
# Draw in a hidden buffer and show the finished picture at once: no flicker
try:
    from ti_draw import use_buffer, paint_buffer
    use_buffer()
except:
    paint_buffer = None
try:
    from ti_system import get_key as read_key
except:
    from ti_system import getKey as read_key
# On the Evo get_key wants one number. Find out once at the start.
try:
    read_key()
    key = read_key
except TypeError:
    def key():
        return read_key(0)
try:
    from ti_system import store_list, recall_list
except:
    store_list = recall_list = None
try:
    from time import sleep
except:
    from ti_system import sleep

# Key numbers (the Evo uses the second number in each pair)
LEFT = (2, 24)
RIGHT = (1, 26)
UP = (3, 25)
DOWN = (4, 34)
OK = (5, 105)                 # enter
QUIT = (9, 45)                # clear

C = 20                        # small square size in pixels
GAP = 8                       # extra space between the small boards
X0 = 4
Y0 = (SH - (9 * C + 2 * GAP)) // 2
TX = X0 + 9 * C + 2 * GAP + 4  # text panel on the right (black, so text is fine)

LIGHT = (210, 210, 210)       # squares
GREEN = (40, 255, 40)         # frame around the boards you may play in
XCOL = (220, 0, 0)
OCOL = (0, 60, 230)
XTINT = (255, 190, 190)       # small board won by X
OTINT = (190, 205, 255)       # small board won by O
FULL = (60, 60, 60)           # small board full, nobody won
YELLOW = (255, 220, 0)

# X and O as 5 x 5 block pictures (we draw them; text would sit too high)
SHAPES = {1: ["#...#", ".#.#.", "..#..", ".#.#.", "#...#"],
          2: [".###.", "#...#", "#...#", "#...#", ".###."]}
LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8),
         (0, 4, 8), (2, 4, 6)]

boards = [[0] * 9 for b in range(9)]   # 0 empty, 1 X, 2 O
won = [0] * 9                         # 0 open, 1 X, 2 O, 3 full
active = [-1]                         # board you must play in, -1 = any

def paint():
    if paint_buffer:
        paint_buffer()

def shape(p, x, y, size):
    for r in range(5):
        row = SHAPES[p][r]
        c = 0
        while c < 5:                   # draw each run of blocks as one box
            if row[c] == "#":
                e = c
                while e < 5 and row[e] == "#":
                    e += 1
                fill_rect(x + c * size, y + r * size, (e - c) * size, size)
                c = e
            else:
                c += 1

def pos(g):                            # pixel of square 0..8 across or down
    return g * C + (g // 3) * GAP

def playable(b):
    return won[b] == 0 and (active[0] == -1 or active[0] == b)

def draw_cell(gx, gy):
    b, c = (gy // 3) * 3 + gx // 3, (gy % 3) * 3 + gx % 3
    x, y = X0 + pos(gx), Y0 + pos(gy)
    set_color(*LIGHT)
    fill_rect(x, y, C - 1, C - 1)
    v = boards[b][c]
    if v:
        set_color(*(XCOL if v == 1 else OCOL))
        shape(v, x + 2, y + 2, 3)

# Green frame around a board you may play in (black = not now).
# Much faster than recolouring all 9 squares of a board.
def frame(b, on):
    x, y = X0 + pos((b % 3) * 3) - 4, Y0 + pos((b // 3) * 3) - 4
    n = 3 * C + 7                      # outside size: 3 px frame, 1 px gap
    set_color(*(GREEN if on else (0, 0, 0)))
    fill_rect(x, y, n, 3)
    fill_rect(x, y + n - 3, n, 3)
    fill_rect(x, y, 3, n)
    fill_rect(x + n - 3, y, 3, n)

def draw_board(b):
    bx, by = b % 3, b // 3
    if won[b]:
        x, y = X0 + pos(bx * 3), Y0 + pos(by * 3)
        set_color(*{1: XTINT, 2: OTINT, 3: FULL}[won[b]])
        fill_rect(x, y, 3 * C - 1, 3 * C - 1)
        if won[b] < 3:
            set_color(*(XCOL if won[b] == 1 else OCOL))
            shape(won[b], x + 4, y + 4, 10)
    else:
        for cy in range(3):
            for cx in range(3):
                draw_cell(bx * 3 + cx, by * 3 + cy)

def draw_at(gx, gy):                   # one square, or its whole won board
    b = (gy // 3) * 3 + gx // 3
    if won[b]:
        draw_board(b)
    else:
        draw_cell(gx, gy)

def cursor(gx, gy):                    # thick yellow frame
    x, y = X0 + pos(gx), Y0 + pos(gy)
    set_color(*YELLOW)
    fill_rect(x, y, C - 1, 3)
    fill_rect(x, y + C - 4, C - 1, 3)
    fill_rect(x, y, 3, C - 1)
    fill_rect(x + C - 4, y, 3, C - 1)

# Text panel on the right: row 0..6, each 30 px high. Wipe the whole row.
def text(row, s, col=(255, 255, 255)):
    set_color(0, 0, 0)
    fill_rect(TX, row * 30, SW - TX, 29)
    set_color(*col)
    write(TX, row * 30 + 22, s)

def write(x, y, s):                    # text that can never stop the game
    try:
        draw_text(x, y, s)
    except:
        pass

def winner(cells):
    for a, b, c in LINES:
        if cells[a] in (1, 2) and cells[a] == cells[b] == cells[c]:
            return cells[a]
    return 0 if 0 in cells else 3

def big_winner():                      # 1 X, 2 O, 3 draw, 0 not over
    return winner(won)

def wait_for(keys):
    paint()
    while True:
        k = key()
        if k in keys:
            return k
        sleep(0.05)

# Wins are saved in the calculator list TICT2: [X wins, O wins, draws]
def load_stats():
    try:
        l = recall_list("TICT2")
        return [int(l[0]), int(l[1]), int(l[2])]
    except:
        return [0, 0, 0]

def save_stats(s):
    try:
        store_list("TICT2", s)
    except:
        pass

# ---------- computer player ----------
# It looks 2 moves ahead: its own move, then every answer you could give.
# Positions get points: + is good for X, - is good for O.
WEIGHT = [1.2, 1, 1.2, 1, 1.5, 1, 1.2, 1, 1.2]   # middle and corners matter more
TWO = (0, 0.5, 3, 0)                              # 0, 1 or 2 marks in an open line
BIG = (0, 4, 25, 1000)                            # 0..3 won boards in a big line
score = [0] * 9                                   # points of each small board

def board_points(b):
    w = won[b]
    if w:
        return (0, 10, -10, 0)[w] * WEIGHT[b]
    cells, s = boards[b], 0
    for a, m, c in LINES:
        x = (cells[a] == 1) + (cells[m] == 1) + (cells[c] == 1)
        o = (cells[a] == 2) + (cells[m] == 2) + (cells[c] == 2)
        if o == 0:
            s += TWO[x]
        if x == 0:
            s -= TWO[o]
    return s * WEIGHT[b]

def points():                                     # whole position
    s = sum(score)
    for a, m, c in LINES:
        v = (won[a], won[m], won[c])
        if 3 in v:
            continue                              # a full board blocks the line
        x, o = v.count(1), v.count(2)
        if o == 0:
            s += BIG[x]
        if x == 0:
            s -= BIG[o]
    return s

def moves():
    return [(b, c) for b in range(9) if playable(b)
            for c in range(9) if boards[b][c] == 0]

def do(b, c, p):                                  # play a move, keep the undo info
    undo = (won[b], active[0], score[b])
    boards[b][c] = p
    won[b] = winner(boards[b])
    active[0] = -1 if won[c] else c
    score[b] = board_points(b)
    return undo

def undo_move(b, c, u):
    boards[b][c] = 0
    won[b], active[0], score[b] = u

WIN = 10000
KEEP = {3: 6, 2: 8}                               # best moves to look at, per depth

def ordered(me, depth):                           # moves, best-looking first
    sign = 1 if me == 1 else -1
    ms = moves()
    if depth in KEEP and len(ms) > KEEP[depth]:
        rated = []
        for b, c in ms:
            u = do(b, c, me)
            rated.append((sign * points(), b, c))
            undo_move(b, c, u)
        rated.sort(reverse=True)
        ms = [(b, c) for q, b, c in rated[:KEEP[depth]]]
    return ms

# Best value for player me, looking depth moves ahead (alpha-beta search)
def search(me, depth, alpha, beta):
    if depth == 0:
        return (1 if me == 1 else -1) * points()
    ms = ordered(me, depth)
    if not ms:
        return 0                                  # nothing left: draw
    best = -WIN * 2
    for b, c in ms:
        u = do(b, c, me)
        w = winner(won)
        if w == me:
            v = WIN + depth                       # winning sooner is better
        elif w == 3:
            v = 0
        else:
            v = -search(3 - me, depth - 1, -beta, -alpha)
        undo_move(b, c, u)
        if v > best:
            best = v
        if best > alpha:
            alpha = best
        if alpha >= beta:
            break                                 # the other player won't allow this
    return best

# level 1 = easy, 2 = medium, 3 = hard (= how many moves it looks ahead)
def ai_move(me, level):
    for b in range(9):
        score[b] = board_points(b)
    ms = moves()
    if level == 1 and random.random() < 0.3:
        return random.choice(ms)                  # easy: sometimes just random
    best, move = -WIN * 3, ms[0]
    for b, c in ordered(me, level):
        u = do(b, c, me)
        w = winner(won)
        if w == me:
            undo_move(b, c, u)
            return (b, c)                         # wins the game now
        v = 0 if w == 3 else -search(3 - me, level - 1, -WIN * 3, WIN * 3)
        undo_move(b, c, u)
        v += random.random() * (4 if level == 1 else 0.5)   # a little variety
        if v > best:
            best, move = v, (b, c)
    return move

# A menu on the start screen. Returns the chosen number, or -1 for clear.
def menu(options, choice, hint):
    x = SW // 2 - 80
    set_color(0, 0, 0)
    fill_rect(0, 64, SW, SH - 64)                 # wipe the old menu
    set_color(255, 255, 255)
    write(x, 202, hint)
    while True:
        for i in range(len(options)):
            set_color(0, 0, 0)
            fill_rect(x - 20, 64 + i * 28, 200, 27)
            set_color(*(YELLOW if i == choice else (150, 150, 150)))
            write(x, 90 + i * 28, ("> " if i == choice else "  ") + options[i])
        k = wait_for(UP + DOWN + OK + QUIT)
        if k in QUIT:
            return -1
        if k in OK:
            return choice
        if k in UP:
            choice = (choice - 1) % len(options)
        if k in DOWN:
            choice = (choice + 1) % len(options)

# Returns 0-2 = computer level (Easy, Medium, Hard), 3 = 2 players, -1 = quit
def start_screen(stats):
    clear()
    set_color(0, 0, 0)
    fill_rect(0, 0, SW, SH)
    x = SW // 2 - 80
    set_color(*XCOL)
    write(x, 25, "TIC TAC TOE 2")
    set_color(255, 255, 255)
    write(x, 55, "X " + str(stats[0]) + "  O " + str(stats[1]) + "  Draw " + str(stats[2]))
    while True:
        p = menu(["1 player", "2 players"], 0, "UP/DOWN + ENTER")
        if p < 0:
            return -1
        if p == 1:
            return 3
        level = menu(["Easy", "Medium", "Hard"], 1, "CLEAR: back")
        if level >= 0:
            return level

def game(mode):                        # mode 0-2 = computer level, 3 = 2 players
    for b in range(9):
        boards[b] = [0] * 9
        won[b] = 0
    active[0] = -1
    clear()
    set_color(0, 0, 0)
    fill_rect(0, 0, SW, SH)
    for b in range(9):
        draw_board(b)
        frame(b, True)
    gx, gy, turn = 4, 4, 1
    text(0, "TIC TAC 2")
    text(5, "ENTER:place")
    text(6, "CLEAR:quit")
    while True:
        computer = mode < 3 and turn == 2
        text(2, ("X" if turn == 1 else "O") + (": CPU" if computer else "'s turn"),
             XCOL if turn == 1 else OCOL)
        if computer:
            paint()
            sleep(0.2)
            b, c = ai_move(2, mode + 1)
        else:
            cursor(gx, gy)
            paint()
            while True:
                k = key()
                if not k:
                    sleep(0.03)
                    continue
                if k in QUIT:
                    return 0
                ox, oy = gx, gy
                if k in LEFT:
                    gx = max(0, gx - 1)
                elif k in RIGHT:
                    gx = min(8, gx + 1)
                elif k in UP:
                    gy = max(0, gy - 1)
                elif k in DOWN:
                    gy = min(8, gy + 1)
                elif k in OK:
                    b, c = (gy // 3) * 3 + gx // 3, (gy % 3) * 3 + gx % 3
                    if playable(b) and boards[b][c] == 0:
                        break
                draw_at(ox, oy)
                cursor(gx, gy)
                paint()
        # place the mark and work out the next board
        was = [playable(i) for i in range(9)]
        boards[b][c] = turn
        won[b] = winner(boards[b])
        active[0] = -1 if won[c] else c
        if won[b]:
            draw_board(b)              # big X or O over the whole board
        else:
            draw_cell((b % 3) * 3 + c % 3, (b // 3) * 3 + c // 3)
        for i in range(9):             # only change frames that changed
            if was[i] != playable(i):
                frame(i, playable(i))
        w = big_winner()
        if w:
            return w
        turn = 3 - turn
        if active[0] != -1:            # jump to the middle of the next board
            gx, gy = (active[0] % 3) * 3 + 1, (active[0] // 3) * 3 + 1

# --- start ---
stats = load_stats()
mode = start_screen(stats)
while mode >= 0:
    w = game(mode)
    if w == 0:
        break
    stats[w - 1] += 1
    save_stats(stats)
    text(2, {1: "X wins!", 2: "O wins!", 3: "Draw!"}[w], {1: XCOL, 2: OCOL, 3: (255, 255, 255)}[w])
    text(5, "ENTER:again")
    if wait_for(OK + QUIT) in QUIT:
        break
paint()
