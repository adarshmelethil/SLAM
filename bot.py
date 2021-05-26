#!/usr/bin/env python

import random
import math
import matplotlib.pyplot as plt
import numpy as np

from dungeon import Generator


class Bot():
  def __init__(self, dungeon):
    self.set_dungeon(dungeon)
    plt.ion()

  def set_dungeon(self, dungeon):
    self.dungeon = dungeon

    self.open_tiles = []
    for row_num, row in enumerate(self.dungeon):
      for col_num, cell in enumerate(row):
        if cell == 1:
          self.open_tiles.append([row_num, col_num])

    self.position = random.choice(self.open_tiles)

  def display(self, laser_data=None):
    plt.clf()

    # Walls
    wall_xs = []
    wall_ys = []
    for row_num, row in enumerate(self.dungeon):
      for col_num, cell in enumerate(row):
        if cell == 2:
          wall_xs.append(row_num)
          wall_ys.append(col_num)
        if cell == 0:
          wall_xs.append(row_num)
          wall_ys.append(col_num)
    plt.plot(wall_xs, wall_ys, "*k")
    
    # Bot position
    plt.plot([self.position[0]], [self.position[1]], "ob")

    if laser_data:
      laser_x = []
      laser_y = []
      num_of_points = len(laser_data)
      for i, laser in enumerate(laser_data):
        angle = i * (360/num_of_points)
        laser_vec = self.distToWorldPoint(laser, angle)

        laser_x.append(laser_vec[0])
        laser_y.append(laser_vec[1])

      plt.plot(laser_x, laser_y, "xr")
    # plt.plot(xs, ys, ".k")
    plt.draw()
    plt.pause(0.0001)

  def distToWorldPoint(self, dist, angle):
    pos = np.array(self.position)
    up_vec = np.array([0, 1])
    return pos + self.rotate(up_vec, -angle) * dist

  def rotate(self, vector, degree):
    theta = np.radians(degree)
    c, s = np.cos(theta), np.sin(theta)
    R = np.array(((c,-s), (s, c)))
    return np.matmul(R, vector)

  def move(self, direction):
    if direction == "up":
      if self.dungeon[self.position[0]][self.position[1]+1] != 1:
        return False
      self.position[1] += 1
    elif direction == "down":
      if self.dungeon[self.position[0]][self.position[1]-1] != 1:
        return False
      self.position[1] -= 1
    elif direction == "right":
      if self.dungeon[self.position[0]+1][self.position[1]] != 1:
        return False
      self.position[0] += 1
    elif direction == "left":
      if self.dungeon[self.position[0]-1][self.position[1]] != 1:
        return False
      self.position[0] -= 1
    return True

  def laser(self, laser_direc):
    cur_pos = np.array(self.position)
    laser = np.copy(laser_direc)
    laser_cell = cur_pos + laser
    while self.dungeon[int(laser_cell[0])][int(laser_cell[1])] == 1:
      laser += laser_direc
      laser_cell = cur_pos + laser
    return np.linalg.norm(laser)

  def lidar(self):
    num_of_lasers = 8

    laser_data = []
    up_vec = np.array([0, 1])
    # starting up, then rotating by 45° right 
    for i, angle in enumerate([-i*(360/num_of_lasers) for i in range(num_of_lasers)]):
      laser_direc = self.rotate(up_vec, angle)
      if i % 2:
        laser_direc *= math.sqrt(2) # diagonal unit is more than 1
      laser_data.append(self.laser(laser_direc))
    return laser_data

if __name__ == '__main__':
  gen = Generator(
    width=64, height=64,
    max_rooms=32, min_room_xy=5,
    max_room_xy=10, rooms_overlap=True, random_connections=2,
    random_spurs=3
  )

  gen.gen_level()
  gen.gen_tiles_level()
  gen.print_dungen()
  dungeon = gen.get_dungen_array()

  bot = Bot(dungeon)
  while True:
    laser_data = bot.lidar()
    print("forward laser", laser_data[0])
    # self.dungeon[self.position[0]][self.position[1]]

    bot.display(laser_data=laser_data)
    d = input()
    if d == "":
      break

    print(bot.move(d))


