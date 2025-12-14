#!/bin/python3
import curses, time, sys

WIDTH = 80
HEIGHT = 24

px = WIDTH // 2
py = HEIGHT // 2

def render_screen(scr):
  for row in range(HEIGHT):
    for col in range(WIDTH):
      try:
        if row == py and col == px: scr.addch(row, col, '@')
        else: scr.addch(row, col, ' ')
      except: pass
  scr.move(py, px)
  scr.refresh()

def handle_command(scr):
  global px, py
  ch = scr.getch()
  if ch == ord('Q'): sys.exit(0)
  elif ch == ord('h'): px -= 1
  elif ch == ord('j'): py += 1
  elif ch == ord('k'): py -= 1
  elif ch == ord('l'): px += 1
  
def main(stdscr):
  scr = curses.initscr()
  curses.noecho()
  curses.cbreak()
  scr.keypad(1)
  ROWS, COLS = scr.getmaxyx()
  if (ROWS < HEIGHT or COLS < WIDTH): raise RuntimeError('Set your terminal to at least 80x24')
  curses.use_default_colors()
  while True:
    render_screen(scr)
    handle_command(scr)

try: curses.wrapper(main)
except RuntimeError as e: print(e)
