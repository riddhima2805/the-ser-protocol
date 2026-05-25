from engine import *


def colison():
    board = makeboard()
    tanks = maketanks()
    tanks[1]["pos"] = (3, 4)

    adv_tank(board, tanks, 1, "LEFT")

    assert tanks[1]["pos"] == (3, 4)
    print(" as position stayed same WALL collision test passed")


def sdam():
    board = makeboard()
    tanks = maketanks()


    tanks[1]["pos"] = (5, 5)
    tanks[2]["pos"] = (5, 8)
    shoot(board, tanks, 1, "RIGHT")
    assert tanks[2]["hp"] == 75
    print("shooting damage test passed")


def bulletsblocked():
    tanks = maketanks()
    board = makeboard()
    
    board[5][6] = WALL

    tanks[1]["pos"] = (5, 5)
    tanks[2]["pos"] = (5, 8)

    shoot(board, tanks, 1, "RIGHT") 

    assert tanks[2]["hp"] == 100
    print("hp stayed same as bullet was blocked by WALL test passed :)")


def hpack():
    board = makeboard()
    tanks = maketanks()

    tanks[1]["hp"] = 50
    tanks[1]["pos"] = (2, 12)

    usepowerup(board, tanks[1])

    assert tanks[1]["hp"] == 80
    assert board[2][12] == empty
    print("health pack working as hp became 80 :)")


def apack():
    
    tanks = maketanks()
    board = makeboard()

    tanks[1]["ammo"] = 1
    tanks[1]["pos"] = (5, 5)

    usepowerup(board, tanks[1])

    assert tanks[1]["ammo"] == 6 
    assert board[5][5] == empty
    print("ammo pack working as ammo became 6 - test passed :)")


def copytest():
    board = makeboard()
    tanks = maketanks()

    def bad_bot(bot_board, bot_tanks, tank_id):
        bot_board[1][1] = WALL
        bot_tanks[2]["hp"] = 0
        return ("PASS",)

    action = botsmove(bad_bot, board, tanks, 1)

    assert action == ("PASS",)
    assert board[1][1] != WALL
    assert tanks[2]["hp"] == 100
    print("bot gets copy test passed :)")


def tietest():
    tanks = maketanks()
    board = makeboard()
    tanks[1]["hp"] = 25
    tanks[2]["hp"] = 25
    tanks[1]["pos"] = (5, 5)
    tanks[2]["pos"] = (5, 8)

    sametime(board, tanks, {
        1: ("SHOOT", "RIGHT"),
        2: ("SHOOT", "LEFT"),
    }
    )
    assert tanks[1]["hp"] == 25
    assert tanks[2]["hp"] == 0
    assert determine_win(tanks, 1) == 1
    print("sequential shooting test passed :)")


def sameposition():
    board = makeboard()
    tanks = maketanks()

    tanks[1]["pos"] = (5, 5)
    tanks[2]["pos"] = (5, 7)
    sametime(board, tanks, {
        1: ("MOVE", "RIGHT"),
        2: ("MOVE", "LEFT"),
    }
    )

    assert tanks[1]["pos"] == (5, 6) 
    assert tanks[2]["pos"] == (5, 7)  
    print("same square move collision test passed :)")


def collision():
    board = makeboard()
    tanks = maketanks()

    tanks[1]["pos"] = (5, 5)
    tanks[2]["pos"] = (5, 6)

    sametime(board, tanks, {
        1: ("MOVE", "RIGHT"),
        2: ("MOVE", "LEFT"),
    })

    assert tanks[1]["pos"] == (5, 5)
    assert tanks[2]["pos"] == (5, 6)
    print("as tanks try to move into each others positions they collide and test passed")


def run_tests():
    tests = [
        colison,
        sdam,
        bulletsblocked,
        hpack,
        apack,
        copytest,
        tietest,
        sameposition,
        collision,
    ]
    for test in tests:
        test()

    print(f"\n{len(tests)} tests passed")


if __name__ == "__main__":
    run_tests()