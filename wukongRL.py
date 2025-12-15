#!/bin/python3
import curses, time, sys
from random import randint

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 24
MAP_WIDTH = SCREEN_WIDTH
MAP_HEIGHT = SCREEN_HEIGHT-1
ROOM_MAX_SIZE = 12
ROOM_MIN_SIZE = 6
MAX_ROOMS = 30

class Rect:
  def __init__(self, x, y, w, h):
    self.x1 = x
    self.y1 = y
    self.x2 = x + w
    self.y2 = y + h

  def center(self):
    center_x = (self.x1 + self.x2) // 2
    center_y = (self.y1 + self.y2) // 2
    return (center_x, center_y)
    
  def intersect(self, other):
    return (self.x1 <= other.x2 and self.x2 >= other.x1 and
            self.y1 <= other.y2 and self.y2 >= other.y1)

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

def create_room(room):
  global map
  for x in range(room.x1 + 1, room.x2):
    for y in range(room.y1 + 1, room.y2):
      map[x][y].blocked = False
      map[x][y].block_sight = False

def create_h_tunnel(x1, x2, y):
  global map
  for x in range(min(x1, x2), max(x1, x2) + 1):
    map[x][y].blocked = False
    map[x][y].block_sight = False

def create_v_tunnel(y1, y2, x):
  global map
  for y in range(min(y1, y2), max(y1, y2) + 1):
    map[x][y].blocked = False
    map[x][y].block_sight = False

def make_map(player):
  global map
  map = [[Tile(True) for y in range(MAP_HEIGHT)] for x in range(MAP_WIDTH)]
  rooms = []
  num_rooms = 0
  for r in range(MAX_ROOMS):
    w = randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
    h = randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
    x = randint(0, MAP_WIDTH-w-1)
    y = randint(0, MAP_HEIGHT-h-1)
    new_room = Rect(x, y, w, h)
    failed = False
    for other_room in rooms:
      if new_room.intersect(other_room):
        failed = True
        break
    if not failed:
      create_room(new_room)
      (new_x, new_y) = new_room.center()
      if num_rooms == 0:
        player.x = new_x
        player.y = new_y
      else:
        (prev_x, prev_y) = rooms[num_rooms-1].center()
        if randint(0, 1):
          create_h_tunnel(prev_x, new_x, prev_y)
          create_v_tunnel(prev_y, new_y, new_x)
        else:
          create_v_tunnel(prev_y, new_y, prev_x)
          create_h_tunnel(prev_x, new_x, new_y)
      rooms.append(new_room)
      num_rooms += 1
  
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
  player = GameObject(0, 0, '@', scr)
  monster = GameObject(0, 0, 'M', scr)
  objects = [player]
  make_map(player)
  while True:
    render_all(scr, objects)
    handle_command(scr, player)
    #for object in objects: object.clear()

try: curses.wrapper(main)
except RuntimeError as e: print(e)
