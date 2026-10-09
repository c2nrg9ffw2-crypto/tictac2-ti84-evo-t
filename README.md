# Tic-Tac-Toe 2 for the TI-84 Evo-T

**Ultimate Tic-Tac-Toe** for the **TI-84 Evo-T** graphing calculator, written in Python:
one big Tic-Tac-Toe board made of 9 small boards.

> **Made with AI:** this game and this README were created with the help of AI (Claude by Anthropic).
> Everything was tested on a real TI-84 Evo-T.

## Features

- **1 player** against the calculator, with 3 levels: **Easy**, **Medium** and **Hard**
- **2 players** on one calculator
- A **green frame** shows where you may play
- Won small boards get a big X or O
- Wins and draws stay saved after you quit
- No flicker

## What you need

- A **TI-84 Evo-T** calculator
- A USB cable to connect it to your computer
- **Google Chrome** or **Microsoft Edge** (Safari and Firefox do not work with the TI tool)
- The file [`tictac2.py`](tictac2.py) from this repo

## Setup

1. Download [`tictac2.py`](tictac2.py) to your computer.
2. Connect the calculator to your computer with the USB cable.
   Leave the calculator on the **home screen**.
3. Open **https://connectevo.ti.com** in **Chrome** or **Edge**.
4. Connect to your calculator in the page and allow access when the browser asks.
5. Drag `tictac2.py` onto the page to send it to the calculator.
6. **Choose RAM** to play right away.
   The Python app on the Evo-T only shows files that are in RAM.
   (Want to keep the game safe? See [Don't lose the game](#dont-lose-the-game).)

> **Already sent it to Archive?** On the **home screen** (not in the Python app) press **2nd → mem → Mem Management**,
> find **TICTAC2** and press **enter**. The `*` in front of the name disappears, which means
> it is now in RAM.

## Start the game

1. Open the **Python** app on the calculator.
2. Choose **TICTAC2** and run it.
3. Choose **1 player** or **2 players** with ▲ ▼ and press **enter**.
4. For 1 player, choose **Easy**, **Medium** or **Hard** (or **clear** to go back).

## Don't lose the game

The Evo-T **deletes RAM** when it stays turned off for a while.
A normal turn-off is fine, but after some time the game is gone.

**Best way:**

1. Keep the game in **Archive**. Archive is never deleted.
2. Go to the **home screen**. If you are in the Python app, leave it with **2nd → quit**
   (quit is above the **mode** key). In the Python app, **2nd → mem** does nothing.
3. Press **2nd → mem** (mem is above the **+** key) and choose **2: Mem Management**.
4. Choose the list with Python programs (or **All**).
5. Find **TICTAC2** and press **enter**. The `*` disappears, which means the game is now in RAM.
6. Open the **Python** app and play.

Programs can't move files between Archive and RAM by themselves, so this step can't be automatic.
The wins list **TICT2** is in RAM too, so it can be deleted the same way.

## Keys

| Key | What it does |
|---|---|
| ◀ ▶ ▲ ▼ | Move the yellow frame |
| enter | Place your X or O |
| clear | Quit |

## Rules

- The big board has 9 small boards. **X** starts.
- **Where** you play inside a small board decides **which small board** the other player must use next.
  For example: play in the top-right square of a small board, and the other player must play in
  the top-right small board.
- The board you must play in has a **green frame**.
- If that board is already won or full, the other player may play in **any** open board.
- Get 3 in a row in a small board to **win** it. It then shows a big X or O.
- Win **3 small boards in a row** to win the game.

## Levels

| Level | How the calculator plays |
|---|---|
| Easy | Looks only at its own move, and sometimes plays a random move |
| Medium | Looks 2 moves ahead |
| Hard | Looks 3 moves ahead (thinks a little longer) |

## Wins

Wins and draws are saved in a calculator list called **TICT2**, so they stay after you quit.

- To reset them, delete the list **TICT2** in **2nd → mem → Mem Management** (on the home screen).
- A calculator reset (RAM clear) also resets them.

## Good to know

- Keep `tictac2.py` on your computer too, so you can always send it again.
- Made for the TI-84 Evo-T. Other TI-84 models are not tested.
