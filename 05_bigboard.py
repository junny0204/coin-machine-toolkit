#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
05_bigboard.py - GIANT TOTAL BOARD
Casino-style giant digits show the running total. Flashes green
on every coin.
Run:  python3 05_bigboard.py       Quit: Ctrl+C
"""
import time, sys
from coinlib import (wait_for_coin, flush_coins, status, header, cab_line,
                     cab_mid, cab_bottom, CLEAR, HIDE, SHOW,
                     RESET, DIM, GOLD, GREEN, WHITE, money)

BIG = {
    '0':["###","# #","# #","# #","###"], '1':[" # ","## "," # "," # ","###"],
    '2':["###","  #","###","#  ","###"], '3':["###","  #","###","  #","###"],
    '4':["# #","# #","###","  #","  #"], '5':["###","#  ","###","  #","###"],
    '6':["###","#  ","###","# #","###"], '7':["###","  #","  #","  #","  #"],
    '8':["###","# #","###","# #","###"], '9':["###","# #","###","  #","###"],
    '.':["   ","   ","   ","   "," # "], ',':["   ","   ","   ","  #"," # "],
}
BIG = {k:[r.replace('#','█') for r in v] for k,v in BIG.items()}

def big_lines(text):
    return ["  ".join(BIG.get(ch, ["   "]*5)[r] for ch in text) for r in range(5)]

def render(total, count, flash=False):
    s = f"{total:,.2f}"
    rows = big_lines(s)
    W = max(34, len(rows[0]) + 4)
    color = GREEN if flash else GOLD
    print(CLEAR, end="")
    header("TOTAL COLLECTED", W)
    cab_line("", W)
    for r in rows:
        cab_line(r, W, color)
    cab_line("", W)
    cab_mid(W)
    cab_line(f"{money(total)}   ·   {count} COINS", W, WHITE)
    cab_bottom(W)
    status()

def main():
    total, count = 0.0, 0
    print(HIDE, end="")
    render(total, count)
    try:
        while True:
            v = wait_for_coin()
            total += v; count += 1
            render(total, count, flash=True); time.sleep(0.12)
            render(total, count, flash=False)
            flush_coins()
    except KeyboardInterrupt:
        print(SHOW + f"\n  {GOLD}SESSION TOTAL: {money(total)}{RESET}\n")
        sys.exit(0)

if __name__ == "__main__":
    main()
