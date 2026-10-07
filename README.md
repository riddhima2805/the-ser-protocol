# The Ser Protocol

A turn-based, two-player tank battle game engine written in pure Python (standard library only). Two bots share a grid map, take one action per turn, and fight until one tank is eliminated or the turn limit is reached.

The repo contains the game engine, a sample bot, a runner script, a test suite and a written strategy document.

---

## Game Rules

### Actions

On each turn, a bot picks exactly **one** action:

| Action | Description | Condition |
| --- | --- | --- |
| **Move** | Move one step up, down, left or right | Destination must be empty (not a wall or the other tank) |
| **Shoot** | Fire a bullet up, down, left or right | Costs 1 ammo |
| **Pass** | Do nothing this turn | Always valid |

- **Powerups:** moving onto an `H` or `A` tile automatically collects the powerup.
- **Invalid actions:** an invalid action (for example, moving into a wall or shooting with 0 ammo) is treated as `PASS` for that turn.

### Shooting

- A bullet travels in the given direction, one tile per tick, until it hits a **wall** or the **enemy tank**.
- A hit deals **25 HP** of damage.
- Bullets do **not** pass through walls.
- Both bots shoot from their *current* position. Bullets are resolved **after** both bots have submitted their actions for the turn.

### Winning

- A tank at **0 HP or below** is eliminated and the opponent wins.
- If **150 turns** pass with no winner, the tank with **more HP** wins.
- If HP is tied at turn 150, the match is a **draw**.

---

## Repository Structure

| File | Purpose |
| --- | --- |
| `engine.py` | The game engine: holds game state, validates actions, advances the game turn by turn and produces a result |
| `my_bot.py` | My bot, which reacts to the game state with a non-random strategy |
| `main.py` | Imports the engine and runs a sample match between two bots, printing the outcome |
| `tests.py` | Test cases for rules and edge cases, written as plain Python assertions |
| `strategy.md` | Explanation of my bot's strategy, including strengths and known weaknesses |

---

## Engine Overview

The engine is responsible for:

1. Initializing a game from a given map
2. Checking whether an action is valid for a given player in the current state
3. Taking both players' actions and producing the next state
4. Generating the state snapshot passed to each bot
5. Running a full match from start to finish given two bot functions
6. Printing a human-readable ASCII view of the board at any point

---

