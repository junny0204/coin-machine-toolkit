#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
06_fundraiser.py - FUNDRAISER GOAL
Every coin pushes the progress bar toward the goal.
Hit the goal and the machine celebrates.
Run:  python3 06_fundraiser.py     Quit: Ctrl+C
Custom goal:  python3 06_fundraiser.py 50
"""
import time, sys
from coinlib import (wait_for_coin, flush_coins, status, header, cab_line,
                     cab_mid, cab_bottom, cab_row, cab_center_raw,
                     CLEAR, HIDE, SHOW, RESET, DIM, GOLD, GREEN, CYAN, WHITE, money)

GOAL = float(sys.argv[1]) if len(sys.argv) > 1 else 20.0
W = 36
BARW = 28

def render(total, celebrate=False):
    pct = min(total / GOAL, 1.0)
    filled = int(pct * BARW)
    bar_plain = "[" + "█"*filled + "░"*(BARW-filled) + "]"
    bar = f"{DIM}[{RESET}{GREEN}{'█'*filled}{RESET}{DIM}{'░'*(BARW-filled)}]{RESET}"
    print(CLEAR, end="")
    header("FUNDRAISER GOAL", W)
    cab_row("GOAL",   money(GOAL),  W, WHITE, WHITE)
    cab_row("RAISED", f"{money(total)}  ({pct*100:.0f}%)", W, WHITE, GREEN)
    cab_line("", W)
    cab_center_raw(bar, bar_plain, W)
    cab_line("", W)
    cab_mid(W)
    if celebrate:
        cab_line("*  G O A L   R E A C H E D  *", W, GOLD)
        cab_line("THANK YOU!", W, CYAN)
    else:
        cab_line(f"{money(max(GOAL-total,0))} TO GO", W, DIM)
        cab_line("EVERY COIN COUNTS", W, DIM)
    cab_bottom(W)
    status()

def main():
    total, reached = 0.0, False
    print(HIDE, end="")
    render(total)
    try:
        while True:
            v = wait_for_coin()
            total += v
            if total >= GOAL and not reached:
                reached = True
                for i in range(6):
                    render(total, celebrate=(i % 2 == 0)); time.sleep(0.25)
                render(total, celebrate=True)
            else:
                render(total, celebrate=reached)
            flush_coins()
    except KeyboardInterrupt:
        print(SHOW + f"\n  {GOLD}RAISED {money(total)} / {money(GOAL)}{RESET}\n")
        sys.exit(0)

if __name__ == "__main__":
    main()
