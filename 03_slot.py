#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
03_slot.py - LUCKY 7s SLOT MACHINE
Insert a coin -> reels spin -> lock left to right -> match 3 on the
payline to win.  7-7-7 hits the MEGA JACKPOT.
Run:  python3 03_slot.py           Quit: Ctrl+C
"""
import random, time, sys
from coinlib import (wait_for_coin, flush_coins, status, header,
                     cab_line, cab_mid, cab_bottom, cab_center_raw,
                     CLEAR, HIDE, SHOW, RESET, DIM, GOLD, GREEN, WHITE, FRAME)

W = 28          # cabinet inner width
GRID = 13       # reel grid visible width

SYMBOLS = ['7', '$', '@', '#', '&', '*']
ANSI = {'7':'\033[1;33m','$':'\033[1;32m','@':'\033[1;36m',
        '#':'\033[1;35m','&':'\033[1;34m','*':'\033[1;31m'}

def _bright(s): return f"{ANSI[s]}{s}{RESET}"
def _dim(s):    return f"{DIM}{s}{RESET}"

def _grid_border(s):
    cab_center_raw(f"{DIM}{s}{RESET}", s, W)

def _sym_line(cols, row, bright):
    cells = [f" {(_bright(c[row]) if bright else _dim(c[row]))} " for c in cols]
    grid = f"{DIM}│{RESET}" + f"{DIM}│{RESET}".join(cells) + f"{DIM}│{RESET}"
    plain = "│" + "│".join(f" {c[row]} " for c in cols) + "│"
    if bright:
        colored = f"{GOLD}>{RESET} " + grid + f" {GOLD}<{RESET}"
        plain = "> " + plain + " <"
        cab_center_raw(colored, plain, W)
    else:
        cab_center_raw(grid, plain, W)

def draw(cols, message, mcolor, coins, wins):
    print(CLEAR, end="")
    header("L U C K Y   7 s", W)
    _grid_border("┌───┬───┬───┐")
    _sym_line(cols, 0, False)
    _sym_line(cols, 1, True)          # payline
    _sym_line(cols, 2, False)
    _grid_border("└───┴───┴───┘")
    cab_mid(W)
    cab_line(f"CREDITS  {coins}     WINS  {wins}", W, WHITE)
    cab_mid(W)
    cab_line(message, W, mcolor)
    cab_bottom(W)
    status()

def evaluate(pay):
    a, b, c = pay
    if a == b == c == '7': return ('MEGA', "** 7-7-7 JACKPOT! **", GOLD)
    if a == b == c:        return ('JACKPOT', ">>  JACKPOT!  <<", GOLD)
    if a == b or b == c or a == c: return ('WIN', "-  WINNER  -", GREEN)
    return ('NONE', "TRY AGAIN", DIM)

def _rand_col():  return [random.choice(SYMBOLS) for _ in range(3)]
def _rand_cols(): return [_rand_col() for _ in range(3)]

def spin(coins, wins):
    pay = [random.choice(SYMBOLS) for _ in range(3)]
    wintype, msg, mcolor = evaluate(pay)
    finals = [[random.choice(SYMBOLS), pay[i], random.choice(SYMBOLS)] for i in range(3)]
    dwins = wins + (1 if wintype != 'NONE' else 0)

    draw(_rand_cols(), "GOOD LUCK!", GREEN, coins, wins); time.sleep(0.45)
    for _ in range(11):
        draw(_rand_cols(), "SPINNING", WHITE, coins, wins); time.sleep(0.07)
    for _ in range(6):
        draw([finals[0], _rand_col(), _rand_col()], "SPINNING .", WHITE, coins, wins); time.sleep(0.09)
    for _ in range(6):
        draw([finals[0], finals[1], _rand_col()], "SPINNING . .", WHITE, coins, wins); time.sleep(0.11)
    for i in range(6):
        draw(finals, msg if i % 2 == 0 else "", mcolor, coins, dwins); time.sleep(0.18)
    draw(finals, msg, mcolor, coins, dwins)
    return wintype

def attract(coins, wins):
    cols = [['$','7','&'], ['@','7','*'], ['#','7','$']]
    draw(cols, "INSERT COIN TO PLAY", GOLD, coins, wins)

def main():
    coins, wins = 0, 0
    print(HIDE, end="")
    attract(coins, wins)
    try:
        while True:
            wait_for_coin()
            coins += 1
            if spin(coins, wins) != 'NONE':
                wins += 1
            flush_coins()
    except KeyboardInterrupt:
        print(SHOW + f"\n\n  {GOLD}GAME OVER  -  Coins: {coins}   Wins: {wins}{RESET}\n")
        sys.exit(0)

if __name__ == "__main__":
    main()
