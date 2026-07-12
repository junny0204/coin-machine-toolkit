#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
01_dashboard.py - LIVE COIN DASHBOARD
Every coin updates: total collected, coin count, last coin value,
coins per minute, uptime.
Run:  python3 01_dashboard.py      Quit: Ctrl+C
"""
import time, sys
from coinlib import (wait_for_coin, flush_coins, status, header,
                     cab_row, cab_bottom, CLEAR, HIDE, SHOW,
                     RESET, DIM, GOLD, GREEN, CYAN, WHITE, money, fmt)

W = 34

def render(total, count, last, start):
    mins = (time.time() - start) / 60
    cpm = count / mins if mins > 0.01 else 0
    print(CLEAR, end="")
    header("COIN DASHBOARD", W)
    cab_row("TOTAL COLLECTED", money(total), W, WHITE, GREEN)
    cab_row("COINS INSERTED",  str(count),   W, WHITE, WHITE)
    cab_row("LAST COIN VALUE", fmt(last) if count else "-", W, WHITE, GOLD)
    cab_row("COINS / MIN",     f"{cpm:.1f}", W, WHITE, CYAN)
    cab_row("UPTIME",          f"{mins:.1f} min", W, WHITE, DIM)
    cab_bottom(W)
    status()

def main():
    total, count, last = 0.0, 0, 0.0
    start = time.time()
    print(HIDE, end="")
    render(total, count, last, start)
    try:
        while True:
            v = wait_for_coin()
            total += v; count += 1; last = v
            render(total, count, last, start)
            flush_coins()
    except KeyboardInterrupt:
        print(SHOW + f"\n\n  {GOLD}SESSION TOTAL: {count} coins  ·  {money(total)}{RESET}\n")
        sys.exit(0)

if __name__ == "__main__":
    main()
