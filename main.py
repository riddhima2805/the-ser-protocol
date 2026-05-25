from engine import run_game, aggressive_bot
from my_bot import my_bot


if __name__ == "__main__":
    result = run_game(my_bot, aggressive_bot)
    print(f"Final result: {result}")