#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
07_challenge.py - COIN RUSH: 60 SECOND CHALLENGE
Insert the first coin to start the clock, then feed coins as fast
as you can.  Final score is graded S / A / B / C.
Run:  python3 07_challenge.py      Quit: Ctrl+C
Custom duration:  python3 07_challenge.py 30
"""
import time, sys
from coinlib import (wait_for_coin, poll_coin, flush_coins, status, header,
                     cab_line, cab_mid, cab_bottom, cab_row, cab_center_raw,
                     CLEAR, HIDE, SHOW, RESET, DIM, GOLD, GREEN, RED, CYAN, WHITE)

DURATION = float(sys.argv[1]) if len(sys.argv) > 1 else 60.0
W = 36
BARW = 28

def _bar(remaining):
    pct = max(remaining / DURATION, 0)
    filled = int(pct * BARW)
    col = GREEN if pct > 0.5 else (GOLD if pct > 0.2 else RED)
    plain = "[" + "█"*filled + "░"*(BARW-filled) + "]"
    colored = f"{DIM}[{RESET}{col}{'█'*filled}{RESET}{DIM}{'░'*(BARW-filled)}]{RESET}"
    return colored, plain

def render_play(remaining, coins):
    elapsed = DURATION - remaining
    rate = coins / elapsed if elapsed > 0.5 else 0.0
    colored, plain = _bar(remaining)
    print(CLEAR, end="")
    header("C O I N   R U S H", W)
    cab_row("TIME LEFT", f"{remaining:4.1f} s", W, WHITE, CYAN)
    cab_center_raw(colored, plain, W)
    cab_mid(W)
    cab_row("COINS", str(coins), W, WHITE, GOLD)
    cab_row("RATE",  f"{rate:.1f} / sec", W, WHITE, DIM)
    cab_mid(W)
    cab_line("FEED THE MACHINE !!", W, GREEN)
    cab_bottom(W)
    status()

def render_result(coins):
    rate = coins / DURATION
    if coins >= 30:   grade, gcol = "S   LEGENDARY !", GOLD
    elif coins >= 20: grade, gcol = "A   GREAT RUN",   GREEN
    elif coins >= 10: grade, gcol = "B   NOT BAD",     CYAN
    else:             grade, gcol = "C   WARM-UP LAP", WHITE
    print(CLEAR, end="")
    header("C O I N   R U S H", W)
    cab_line("", W)
    cab_line("=====  TIME'S UP  =====", W, GOLD)
    cab_line("", W)
    cab_row("TOTAL COINS", str(coins), W, WHITE, GOLD)
    cab_row("AVG RATE", f"{rate:.2f} / sec", W, WHITE, CYAN)
    cab_row("GRADE", grade, W, WHITE, gcol)
    cab_line("", W)
    cab_line("insert coin to play again", W, DIM)
    cab_bottom(W)
    status()

def render_ready():
    print(CLEAR, end="")
    header("C O I N   R U S H", W)
    cab_line("", W)
    cab_line(f"{int(DURATION)} SECONDS ON THE CLOCK", W, WHITE)
    cab_line("HOW MANY COINS CAN YOU FEED?", W, WHITE)
    cab_line("", W)
    cab_line("INSERT COIN TO START", W, GOLD)
    cab_line("", W)
    cab_bottom(W)
    status()

def run_once():
    render_ready()
    wait_for_coin()               # first coin starts the clock (not scored)
    coins = 0
    end = time.time() + DURATION
    while True:
        remaining = end - time.time()
        if remaining <= 0:
            break
        if poll_coin(timeout=min(0.15, remaining)) is not None:
            coins += 1
        render_play(max(remaining, 0), coins)
    render_result(coins)
    flush_coins()

def main():
    print(HIDE, end="")
    try:
        while True:
            run_once()
            wait_for_coin()       # coin = play again
    except KeyboardInterrupt:
        print(SHOW + f"\n  {GOLD}THANKS FOR PLAYING{RESET}\n")
        sys.exit(0)

if __name__ == "__main__":
    main()
