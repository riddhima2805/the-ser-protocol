from engine import (opponent, inlineofsight, nextstep,
                    search_cell, availabel_nearby, blocked,
                    DIRECTIONS, health, AMMO)


def my_bot(board, tanks, tank_id):
    tank = tanks[tank_id]
    enemy_id = opponent(tank_id)
    enemy = tanks[enemy_id]

    my_row, my_col = tank["pos"]
    his_row, his_col = enemy["pos"]

    shot_vector = inlineofsight(board, tank["pos"], enemy["pos"])
    if shot_vector and tank["ammo"] > 0:
        return ("SHOOT", shot_vector)


    if tank["hp"] < 25:
        health_step = nextstep(
            board, tanks, tank_id, search_cell(board, health)
        )
        if health_step:
            return ("MOVE", health_step)

    if tank["ammo"] == 0:
        ammo_step = nextstep(
            board, tanks, tank_id, search_cell(board, AMMO)
        )
        if ammo_step:
            return ("MOVE", ammo_step)

    if my_row == his_row:
        new_pos = (my_row + 1, my_col)
        if not blocked(board, tanks, new_pos):
            return ("MOVE", "DOWN")

    if my_col == his_col:
        new_pos = (my_row, my_col + 1)
        if not blocked(board, tanks, new_pos):
            return ("MOVE", "RIGHT")

    
    chase_step = nextstep(
        board, tanks, tank_id, availabel_nearby(board, enemy["pos"])
    )
    if chase_step:
        return ("MOVE", chase_step)

    return ("PASS",)