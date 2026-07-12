#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
08_chart.py - COIN RATE MONITOR
Logs every coin to coins_log.csv (timestamp, value) and draws a live
bar chart of coins per 10-second bucket.  Analyze the CSV later with
pandas / Excel.
Run:  python3 08_chart.py          Quit: Ctrl+C
"""
import time, sys, csv, os
from datetime import datetime
from collections import defaultdict
from coinlib import (wait_for_coin, flush_coins, status, header, cab_line,
                     cab_mid, cab_bottom, cab_row, cab_left_raw,
                     CLEAR, HIDE, SHOW, RESET, DIM, GOLD, GREEN, CYAN, WHITE, money)

CSV_PATH = "coins_log.csv"
BUCKET = 10
BAR_MAX = 22
SHOW_BUCKETS = 7
W = 40

def ensure_csv():
    if not os.path.exists(CSV_PATH):
        with open(CSV_PATH, "w", newline="") as f:
            csv.writer(f).writerow(["timestamp", "value"])

def log_coin(value):
    with open(CSV_PATH, "a", newline="") as f:
        csv.writer(f).writerow([datetime.now().isoformat(timespec="seconds"), value])

def render(buckets, total_count, total_value, start):
    print(CLEAR, end="")
    header("COIN RATE MONITOR", W)
    cab_line(f"coins per {BUCKET}-second bucket", W, DIM)
    cab_mid(W)
    if not buckets:
        cab_line("", W)
        cab_line("waiting for the first coin...", W, DIM)
        cab_line("", W)
    else:
        keys = sorted(buckets.keys())[-SHOW_BUCKETS:]
        peak = max(buckets[k] for k in keys) or 1
        for k in keys:
            n = buckets[k]
            length = max(int(n / peak * BAR_MAX), 1)
            label = time.strftime("%H:%M:%S", time.localtime(k))
            plain = f"{label} {'█'*length} {n}"
            colored = f"{DIM}{label}{RESET} {CYAN}{'█'*length}{RESET} {WHITE}{n}{RESET}"
            cab_left_raw(colored, plain, W)
    cab_mid(W)
    mins = (time.time() - start) / 60
    cab_row("TOTAL", f"{total_count} coins  ·  {money(total_value)}", W, WHITE, GREEN)
    cab_row("LOG FILE", CSV_PATH, W, WHITE, DIM)
    cab_bottom(W)
    status(f"{mins:.1f} min")

def main():
    ensure_csv()
    buckets = defaultdict(int)
    total_count, total_value = 0, 0.0
    start = time.time()
    print(HIDE, end="")
    render(buckets, total_count, total_value, start)
    try:
        while True:
            v = wait_for_coin()
            key = int(time.time() // BUCKET * BUCKET)
            buckets[key] += 1
            total_count += 1; total_value += v
            log_coin(v)
            render(buckets, total_count, total_value, start)
            flush_coins()
    except KeyboardInterrupt:
        print(SHOW + f"\n  {GOLD}{total_count} coins saved to {CSV_PATH}{RESET}")
        print(f"  {DIM}pandas:  pd.read_csv('{CSV_PATH}', parse_dates=['timestamp']){RESET}\n")
        sys.exit(0)

if __name__ == "__main__":
    main()
