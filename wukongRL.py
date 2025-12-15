#!/bin/python3
import curses, time, sys

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 24
MAP_WIDTH = SCREEN_WIDTH
MAP_HEIGHT = SCREEN_HEIGHT-1

class Tile:
  def __init__(self, blocked, block_sight=None):
    self.blocked = blocked
    if block_sight is None:  block_sight = blocked
    self.block_sight = block_sight

class GameObject:
  def __init__(self, x, y, ch, scr):
    self.x = x
    self.y = y
    self.ch = ch
    self.scr = scr
    
  def move(self, dx, dy):
    if not map[self.x + dx][self.y + dy].blocked:
      self.x += dx
      self.y += dy
    
  def draw(self):
    self.scr.addch(self.y, self.x, self.ch)

  def clear(self):
    self.scr.addch(self.y, self.x, ' ')

def make_map():
  global map
  map = [[Tile(False) for y in range(MAP_HEIGHT)] for x in range(MAP_WIDTH)]
  map[30][11].blocked = True
  map[30][11].block_sight = True
  map[40][11].blocked = True
  map[40][11].block_sight = True

def render_all(scr, objects):
  for y in range(MAP_HEIGHT):
    for x in range(MAP_WIDTH):
      wall = map[x][y].block_sight
      if wall: scr.addch(y, x, '#')
      else: scr.addch(y, x, '.')
  for object in objects: object.draw()
  curses.curs_set(0)
  player = objects[0]
  scr.move(player.y, player.x)
  curses.curs_set(1)
  scr.refresh()

def handle_command(scr, player):
  ch = scr.getch()
  if ch == ord('Q'): sys.exit(0)
  elif ch == ord('h'): player.move(-1, 0)
  elif ch == ord('j'): player.move(0, 1)
  elif ch == ord('k'): player.move(0, -1)
  elif ch == ord('l'): player.move(1, 0)
  
def main(scr):
  rows, cols = scr.getmaxyx()
  if (rows < SCREEN_HEIGHT or cols < SCREEN_WIDTH):
    raise RuntimeError('Set your terminal to at least 80x24')
  scr.nodelay(1)
  curses.noecho()
  curses.raw()
  scr.keypad(1)
  curses.use_default_colors()
  player = GameObject(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, '@', scr)
  monster = GameObject(SCREEN_WIDTH//2-5, SCREEN_HEIGHT//2, 'M', scr)
  objects = [player, monster]
  make_map()
  while True:
    render_all(scr, objects)
    handle_command(scr, player)
    for object in objects: object.clear()

try: curses.wrapper(main)
except RuntimeError as e: print(e)
