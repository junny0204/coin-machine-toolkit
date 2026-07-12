#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
02_timer.py - COIN-OP TIMER
Insert a coin to add time. Big digits count down to TIME UP.
More coins = more time (they stack).
Run:  python3 02_timer.py          Quit: Ctrl+C
Custom seconds per coin:  python3 02_timer.py 600
"""
import time, sys
from coinlib import (poll_coin, status, header, cab_line, cab_mid, cab_bottom,
                     CLEAR, HIDE, SHOW, RESET, DIM, GOLD, GREEN, RED, CYAN, WHITE)

SEC_PER_COIN = float(sys.argv[1]) if len(sys.argv) > 1 else 60.0
W = 34

BIG = {
    '0':["###","# #","# #","# #","###"], '1':[" # ","## "," # "," # ","###"],
    '2':["###","  #","###","#  ","###"], '3':["###","  #","###","  #","###"],
    '4':["# #","# #","###","  #","  #"], '5':["###","#  ","###","  #","###"],
    '6':["###","#  ","###","# #","###"], '7':["###","  #","  #","  #","  #"],
    '8':["###","# #","###","# #","###"], '9':["###","# #","###","  #","###"],
    ':':["   "," # ","   "," # ","   "],
}
BIG = {k:[r.replace('#','█') for r in v] for k,v in BIG.items()}

def big_lines(text):
    return ["  ".join(BIG.get(ch, ["   "]*5)[r] for ch in text) for r in range(5)]

def render(remaining, started):
    m, s = divmod(int(remaining + 0.999), 60)
    clock = f"{m:02d}:{s:02d}"
    up = started and remaining <= 0
    color = RED if up else (GOLD if remaining > 10 else CYAN)
    print(CLEAR, end="")
    header("COIN-OP TIMER", W)
    cab_line("", W)
    for row in big_lines(clock):
        cab_line(row, W, color)
    cab_line("", W)
    cab_mid(W)
    if up:
        cab_line("*  T I M E   U P  *", W, RED)
        cab_line("insert coin to restart", W, DIM)
    elif started:
        cab_line("RUNNING", W, GREEN)
        cab_line(f"1 COIN = {int(SEC_PER_COIN)} SEC", W, DIM)
    else:
        cab_line("INSERT COIN TO START", W, GOLD)
        cab_line(f"1 COIN = {int(SEC_PER_COIN)} SEC", W, DIM)
    cab_bottom(W)
    status()

def main():
    remaining, started = 0.0, False
    last = time.time()
    print(HIDE, end="")
    render(remaining, started)
    try:
        while True:
            coin = poll_coin(timeout=0.25)
            now = time.time(); dt = now - last; last = now
            if coin is not None:
                # each coin adds SEC_PER_COIN (1 coin = 1 credit)
                remaining += SEC_PER_COIN
                started = True
            if remaining > 0:
                remaining = max(0.0, remaining - dt)
            render(remaining, started)
    except KeyboardInterrupt:
        print(SHOW + f"\n  {GOLD}TIMER OFF{RESET}\n")
        sys.exit(0)

if __name__ == "__main__":
    main()
