
import copy
from collections import deque


size = 15
max = 150

empty = "."
WALL = "#"
health = "H"
AMMO = "A"

DIRECTIONS = {
    "UP": (-1, 0),
    "DOWN": (1, 0),
    "LEFT": (0, -1),
    "RIGHT": (0, 1),
}
def makeboard():
    powerups = {
        (2, 12): health, (10, 2): health,
        (5, 5): AMMO, (9, 10): AMMO,
    }

    board = [[empty for _ in range(15)] for _ in range(15)]

    walls = [
        (3, 3), (5, 12), (3, 5), (2, 4), (1, 7), (8, 5),
        (11, 9), (10, 10), (11, 8), (7, 1), (7, 2), (7, 3),
        (7, 11), (7, 12), (7, 13), (6, 7), (6, 8), (6, 9),
    ]
    for row, col in walls:
        board[row][col] = WALL

    for (row, col), item in powerups.items():
        board[row][col] = item

    return board


def maketanks():
    return {
        1: {"hp": 100, "ammo": 10, "pos": (0, 0)},
        2: {"hp": 100, "ammo": 10, "pos": (14, 14)},
    }


def printb(board, tanks):
    display = [row[:] for row in board]

    for tank_id, tank in tanks.items():
        if tank["hp"] > 0:
            row, col = tank["pos"]
            display[row][col] = str(tank_id)

    print()
    for row in display:
        print(" ".join(row))

    print(
        f" tank 1   POS={tanks[1]['pos']} | "
        f"tank 2  POS={tanks[2]['pos']}"
    )


def intheboard(pos):
    row, col = pos
    return 0 <= row < 15 and 0 <= col < 15


def opponent(tank_id):
    return 2 if tank_id == 1 else 1


def blocked(board, tanks, pos):
    if not intheboard(pos):
        return True

    row, col = pos
    if board[row][col] == WALL:
        return True

    return any(tank["hp"] > 0 and tank["pos"] == pos for tank in tanks.values())


def fix(action):
    if not isinstance(action, tuple) or not action:
        return ("PASS",)

    action_type = action[0]
    if action_type == "MOVE" and len(action) == 2 and action[1] in DIRECTIONS:
        return action

    if action_type == "SHOOT" and len(action) == 2 and action[1] in DIRECTIONS:
        return action

    if action_type == "PASS":
        return ("PASS",)
    

def checkmoves(tank, action): #extra validation
    action = fix(action)

    if tank["hp"] == 0: #dead tanks dont start to move

        return ("PASS",)

    if action[0] == "SHOOT" and tank["ammo"] == 0:
        return ("PASS",)

    return action


def usepowerup(board, tank):
    row, col = tank["pos"]
    item = board[row][col]

    if item == health:
        tank["hp"] = min(100, tank["hp"] + 30)
        board[row][col] = empty
    elif item == AMMO:
        tank["ammo"] += 5
        board[row][col] = empty


def adv_tank(board, tanks, tank_id, direction):
    tank = tanks[tank_id]
    row, col = tank["pos"]
    row_change, col_change = DIRECTIONS[direction]
    new_pos = (row + row_change, col + col_change)

    if blocked(board, tanks, new_pos):
        return

    tank["pos"] = new_pos
    usepowerup(board, tank)


def followbullet(board, tanks, attacker, direction):
    shooter = tanks[attacker]
    enemy_id = opponent(attacker)
    enemy = tanks[enemy_id]

    row_change, col_change = DIRECTIONS[direction] 
    row, col = shooter["pos"]
    row += row_change
    col += col_change

    while intheboard((row, col)):
        if board[row][col] == WALL:
            return None

        if enemy["pos"] == (row, col):
            return enemy_id

        row += row_change
        col += col_change

    return None


def shoot(board, tanks, attacker, direction):  
    shooter = tanks[attacker]
    enemy_id = opponent(attacker)
    enemy = tanks[enemy_id]

    if shooter["ammo"] <= 0 or enemy["hp"] <= 0:
        return

    shooter["ammo"] -= 1

    opponentid = followbullet(board, tanks, attacker, direction)

    if opponentid is not None:
        tanks[opponentid]["hp"] -= 25


def performactin(board, tanks, tank_id, action):
    action = checkmoves(tanks[tank_id], action)

    if action[0] == "MOVE":
        adv_tank(board, tanks, tank_id, action[1])

    elif action[0] == "SHOOT":
        shoot(board, tanks, tank_id, action[1])


def sametime(board, tanks, actions):
    clean_actions = {
        tank_id: checkmoves(tanks[tank_id], action)
        for tank_id, action in actions.items()
    }

    performactin(board, tanks, 1, clean_actions[1])
    performactin(board, tanks, 2, clean_actions[2])


def determine_win(tanks, turn):
    if tanks[1]["hp"] <= 0 and tanks[2]["hp"] <= 0:
        return "tie"
    if tanks[1]["hp"] <= 0:
        return 2
    if tanks[2]["hp"] <= 0:
        return 1

    if turn >= 150:
        if tanks[1]["hp"] > tanks[2]["hp"]:
            return 1
        if tanks[2]["hp"] > tanks[1]["hp"]:
            return 2
        return "tie"

    return None


def botsmove(bot, board, tanks, tank_id):
    try:
        safe_board = copy.deepcopy(board)
        safe_tanks = copy.deepcopy(tanks)
        return bot(safe_board, safe_tanks, tank_id)
    except Exception as error:
        print(f"Bot {tank_id} error: {error}. Passing turn.")
        return ("PASS",)


def run_game(bot1, bot2, show_board=False):
    board = makeboard()
    tanks = maketanks()
    winner = None
    turn = 0

    if show_board:
        printb(board, tanks)

    while winner is None:
        turn += 1

        action1 = botsmove(bot1, board, tanks, 1)
        action2 = botsmove(bot2, board, tanks, 2)

        sametime(board, tanks, {
            1: action1,
            2: action2,
        })

        if show_board:
            print(f"\nTURN {turn}")
            print(f"Bot 1 action: {action1}")
            print(f"Bot 2 action: {action2}")
            printb(board, tanks)

        winner = determine_win(tanks, turn)

    print(f"\nWinner: {winner}")
    return winner


def inlineofsight(board, start, target):
    start_row, start_col = start
    target_row, target_col = target

    if start_row == target_row:
        direction = "RIGHT" if target_col > start_col else "LEFT"
    elif start_col == target_col:
        direction = "DOWN" if target_row > start_row else "UP"
    else:
        return None

    row_change, col_change = DIRECTIONS[direction]
    row = start_row + row_change
    col = start_col + col_change

    while (row, col) != target:
        if board[row][col] == WALL:
            return None
        row += row_change
        col += col_change

    return direction


def nextstep(board, tanks, tank_id, targets):
    start = tanks[tank_id]["pos"]
    enemy_id = opponent(tank_id)
    enemy_pos = tanks[enemy_id]["pos"]
    target_set = set(targets)
    queue = deque([(start, None)])
    visited = {start}

    while queue:
        pos, first_step = queue.popleft()

        if pos in target_set and pos != start:
            return first_step
        #if first direction explored is right then first step is right, then every future node in that path 
        # becomes right stored. and when the target is first found , it knows the first move to take. 

        row, col = pos
        for direction, (row_change, col_change) in DIRECTIONS.items():
            next_pos = (row + row_change, col + col_change)

            if next_pos in visited:
                continue
            if not intheboard(next_pos):
                continue
            next_row, next_col = next_pos
            if board[next_row][next_col] == WALL:
                continue
            if next_pos == enemy_pos:
                continue

            visited.add(next_pos)
            queue.append((next_pos, first_step or direction))

    return None


def search_cell(board, item):
    cells = []
    for row, board_row in enumerate(board):
        for col, value in enumerate(board_row):
            if value == item:
                cells.append((row, col))
    return cells


def availabel_nearby(board, pos):
    row, col = pos
    cells = []

    for row_change, col_change in DIRECTIONS.values():
        next_pos = (row + row_change, col + col_change)
        if not intheboard(next_pos):
            continue
        next_row, next_col = next_pos
        if board[next_row][next_col] != WALL:
            cells.append(next_pos)

    return cells


def aggressive_bot(board, tanks, tank_id):
    tank = tanks[tank_id]
    enemy_id = opponent(tank_id)
    enemy = tanks[enemy_id]

    shot_vector = inlineofsight(board, tank["pos"], enemy["pos"])
    if shot_vector and tank["ammo"] > 0:
        return ("SHOOT", shot_vector)

    if tank["ammo"] == 0:
        ammo_step = nextstep(board, tanks, tank_id, search_cell(board, AMMO))
        if ammo_step:
            return ("MOVE", ammo_step)

    chase_step = nextstep(
        board, tanks, tank_id, availabel_nearby(board, enemy["pos"])
    )
    if chase_step:
        return ("MOVE", chase_step)

    return ("PASS",)