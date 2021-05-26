#!/usr/bin/env python

from dungeon import Generator
from bot import Bot

if __name__ == '__main__':
  gen = Generator()
  gen.gen_level()
  gen.gen_tiles_level()
  gen.print_dungen()
  dungeon = gen.get_dungen_array()
  bot = Bot(dungeon)

  # probab

