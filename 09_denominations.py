#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
09_denominations.py - MULTI-COIN RECOGNITION
The Sintron ST-001 can be trained to recognize different coins, each
reporting its own programmed value.  This tool tallies every value
live: count and subtotal per coin type, plus the grand total.

DEMO MODE: type a value (e.g. 5, 10, 30) then Enter to simulate
different coin types.  Plain Enter = value 1.
Run:  python3 09_denominations.py  Quit: Ctrl+C
"""
import sys
from collections import defaultdict
from coinlib import (wait_for_coin, flush_coins, status, header, cab_line,
                     cab_mid, cab_bottom, cab_row, cab_center_raw,
                     CLEAR, HIDE, SHOW, RESET, DIM, GOLD, GREEN, CYAN, WHITE, fmt, money)

W = 34
C1, C2, C3 = 9, 8, 13          # column widths (plain chars)

def _row(a, b, c, color=WHITE):
    plain = f"{a.center(C1)}│{b.center(C2)}│{c.center(C3)}"
    colored = (f"{color}{a.center(C1)}{RESET}{DIM}│{RESET}"
               f"{color}{b.center(C2)}{RESET}{DIM}│{RESET}"
               f"{color}{c.center(C3)}{RESET}")
    cab_center_raw(colored, plain, W)

def _rule():
    plain = "─"*C1 + "┼" + "─"*C2 + "┼" + "─"*C3
    cab_center_raw(f"{DIM}{plain}{RESET}", plain, W)

def render(counts, last=None):
    total_count = sum(counts.values())
    total_value = sum(v * n for v, n in counts.items())
    print(CLEAR, end="")
    header("MULTI-COIN RECOGNITION", W)
    _row("VALUE", "COUNT", "SUBTOTAL", WHITE)
    _rule()
    if not counts:
        cab_line("", W)
        cab_line("waiting for coins...", W, DIM)
        cab_line("", W)
    else:
        for v in sorted(counts.keys()):
            n = counts[v]
            hi = GREEN if (last is not None and abs(v - last) < 1e-9) else WHITE
            _row(fmt(v), str(n), fmt(v * n), hi)
    cab_mid(W)
    cab_row("TOTAL", f"{total_count} coins   {money(total_value)}", W, WHITE, GREEN)
    cab_bottom(W)
    status("each coin type reports its own value")

def main():
    counts = defaultdict(int)
    print(HIDE, end="")
    render(counts)
    try:
        while True:
            v = wait_for_coin(default=1.0)
            counts[v] += 1
            render(counts, last=v)
            flush_coins()
    except KeyboardInterrupt:
        tv = sum(v * n for v, n in counts.items())
        print(SHOW + f"\n  {GOLD}{sum(counts.values())} coins  ·  {money(tv)}{RESET}\n")
        sys.exit(0)

if __name__ == "__main__":
    main()
