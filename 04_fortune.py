#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
04_fortune.py - COIN ORACLE (Zoltar style)
Insert a coin, the crystal ball glows, your fortune is revealed.
Run:  python3 04_fortune.py        Quit: Ctrl+C
"""
import random, time, sys, textwrap
from coinlib import (wait_for_coin, flush_coins, status, header,
                     cab_line, cab_bottom, CLEAR, HIDE, SHOW,
                     RESET, DIM, GOLD, PURP, CYAN, WHITE)

W = 36

FORTUNES = [
    "A perfect parry awaits you today.",
    "Your next coin brings unexpected luck.",
    "Patience now, EX meter later.",
    "The crystal sees a comeback victory.",
    "Beware the overhead. Block high.",
    "Fortune favors the frame-perfect.",
    "A worthy rival approaches from afar.",
    "Today, the RNG smiles upon you.",
    "Great rewards follow great risk.",
    "Trust your reads. Confirm your hits.",
    "An old friend returns with good news.",
    "The wheel turns; your moment is near.",
]

BALL = [
    "      .-\"\"\"\"\"-.",
    "    /  .  .  .  \\",
    "   |  .   *   .  |",
    "   |   .     .   |",
    "    \\  .  .  .  /",
    "      '-.....-'",
]

def frame(lines, color=PURP):
    print(CLEAR, end="")
    header("COIN ORACLE", W)
    for ln in lines:
        cab_line(ln, W, color)
    cab_bottom(W)
    status("1 coin = 1 fortune")

def show_ball(color):
    frame(["", *BALL, ""], color)

def main():
    print(HIDE, end="")
    show_ball(CYAN)
    try:
        while True:
            wait_for_coin()
            for col in [PURP, CYAN, WHITE, PURP, CYAN, WHITE, PURP]:
                show_ball(col); time.sleep(0.18)
            fortune = random.choice(FORTUNES)
            body = ["", "*   *   *", ""] + textwrap.wrap(fortune, W-6) + ["", "*   *   *", ""]
            frame(body, GOLD)
            flush_coins()
    except KeyboardInterrupt:
        print(SHOW + f"\n  {GOLD}The crystal sleeps.{RESET}\n")
        sys.exit(0)

if __name__ == "__main__":
    main()
