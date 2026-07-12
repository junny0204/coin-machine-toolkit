#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
coinlib.py - shared core for the Sintron ST-001 Coin Machine Toolkit
====================================================================

COIN SOURCE (the single swap point)
-----------------------------------
Every tool in this toolkit gets its coins from the two functions below.

* On a Raspberry Pi with a Sintron ST-001 coin acceptor (serial mode)
  wired to the UART, this library opens /dev/serial0 @ 115200
  automatically and every REAL coin triggers the tools.
  The ST-001 sends one line per coin:

      value:30,frequency:213\r\n

  We parse the "value" (the value you programmed into the acceptor)
  and ignore "frequency" (the raw coil reading).

* Anywhere else (your Mac / PC), it falls back to DEMO MODE:
  press Enter = insert one coin, or type a value (e.g. 5) then Enter.

MODE options:
  "auto"     - try the ST-001 first, fall back to keyboard demo (default)
  "serial"   - require the ST-001 (exit if the port cannot be opened)
  "keyboard" - force demo mode
"""

import sys
import select
import re

MODE = "auto"
SERIAL_PORT = "/dev/serial0"
BAUD = 115200

# ---- ANSI colors --------------------------------------------------
RESET = "\033[0m";   DIM   = "\033[1;30m"; WHITE = "\033[1;37m"
RED   = "\033[1;31m"; GREEN = "\033[1;32m"; GOLD  = "\033[1;33m"
BLUE  = "\033[1;34m"; PURP  = "\033[1;35m"; CYAN  = "\033[1;36m"
CLEAR = "\033[2J\033[H"; HIDE = "\033[?25l"; SHOW = "\033[?25h"

FRAME = CYAN                      # cabinet frame color for all tools
BRAND = "powered by Sintron ST-001"

# ---- coin source ---------------------------------------------------
_coin_re = re.compile(rb"value:(\d+)")
_ser = None
if MODE in ("auto", "serial"):
    try:
        import serial as _pyserial
        _ser = _pyserial.Serial(SERIAL_PORT, BAUD, timeout=1)
        _ser.reset_input_buffer()
    except Exception as _e:
        _ser = None
        if MODE == "serial":
            sys.exit(f"Could not open {SERIAL_PORT}: {_e}")

SOURCE_DESC = (f"{SERIAL_PORT} @ {BAUD}" if _ser
               else "DEMO: Enter = coin")

def wait_for_coin(default=1.0):
    """Block until one coin arrives. Returns the coin value (float)."""
    if _ser:
        while True:
            m = _coin_re.search(_ser.readline())
            if m:
                return float(m.group(1))
    raw = input().strip()
    if raw == "":
        return default
    try:
        return float(raw)
    except ValueError:
        return default

def poll_coin(timeout=1.0, default=1.0):
    """Wait up to `timeout` seconds; return a coin value or None.
    For tools that count down while still accepting coins."""
    if _ser:
        _ser.timeout = timeout
        m = _coin_re.search(_ser.readline())
        return float(m.group(1)) if m else None
    r, _, _ = select.select([sys.stdin], [], [], timeout)
    if not r:
        return None
    raw = sys.stdin.readline().strip()
    if raw == "":
        return default
    try:
        return float(raw)
    except ValueError:
        return default

def flush_coins():
    """Drop coins that queued up while the tool was busy animating."""
    if _ser:
        _ser.reset_input_buffer()

# ---- number formatting ---------------------------------------------
def fmt(v):
    """30 -> '30', 0.25 -> '0.25'"""
    return f"{v:g}"

def money(v):
    return f"$ {v:,.2f}"

# ---- shared cabinet UI ----------------------------------------------
def cab_top(w):    print(f"  {FRAME}╔{'═'*w}╗{RESET}")
def cab_mid(w):    print(f"  {FRAME}╠{'═'*w}╣{RESET}")
def cab_bottom(w): print(f"  {FRAME}╚{'═'*w}╝{RESET}")

def cab_line(text, w, color=WHITE):
    """Centered single-color row."""
    print(f"  {FRAME}║{RESET}{color}{text.center(w)}{RESET}{FRAME}║{RESET}")

def cab_row(left, right, w, lcolor=WHITE, rcolor=GREEN):
    """Left label, right-aligned value."""
    gap = max(w - 4 - len(left) - len(right), 1)
    print(f"  {FRAME}║{RESET}  {lcolor}{left}{RESET}{' '*gap}"
          f"{rcolor}{right}{RESET}  {FRAME}║{RESET}")

def cab_center_raw(colored, plain, w):
    """Centered row whose content already contains ANSI colors.
    `plain` is the same content without colors (for width math)."""
    pad = max(w - len(plain), 0); l = pad // 2
    print(f"  {FRAME}║{RESET}{' '*l}{colored}{' '*(pad-l)}{FRAME}║{RESET}")

def cab_left_raw(colored, plain, w):
    """Left-aligned colored row."""
    pad = max(w - 2 - len(plain), 0)
    print(f"  {FRAME}║{RESET}  {colored}{' '*pad}{FRAME}║{RESET}")

def header(title, w):
    """Cabinet top: title marquee + Sintron ST-001 brand line."""
    cab_top(w)
    cab_line(f"*  {title}  *", w, GOLD)
    cab_line(BRAND, w, CYAN)
    cab_mid(w)

def status(extra=""):
    """Bottom status lines under the cabinet (one item per line, white)."""
    parts = [SOURCE_DESC]
    if extra:
        parts.append(extra)
    print(f"\n  {WHITE}Sintron ST-001 Coin Acceptor |{RESET}")
    for p in parts:
        print(f"  {WHITE}{p} |{RESET}")
    print(f"  {WHITE}Ctrl+C to quit{RESET}")
