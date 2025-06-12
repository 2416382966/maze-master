#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Jolly_Son
from tkinter import messagebox
import random
import time
import maze_room
import maze_graphics


class MazeGame(object):
    DEBUG = 0
    mz = []
    visited = []  # 机器路径
    visited2 = []  # 手动路径
    start = 0
    end = 0
    is_timeout = False  # 新增标志位，用于判断是否超时

    class RoomSet(object):
        def __init__(self):
            self.coll = []

        def add(self, item):
            if item not in self.coll:
                self.coll.append(item)

        def pop(self):
            rnd = random.randint(0, len(self.coll) - 1)
            return self.coll.pop(rnd)

        def len(self):
            return len(self.coll)

        def clear(self):
            self.coll.clear()

    def __init__(self, field, x, y, difficulty="普通"):
        self.field_height = x  # 直接使用传入的x/y作为迷宫尺寸
        self.field_width = y
        self.walker = (0, 0)
        self.Walker = (0, 0)
        self.field = field
        self.difficulty = difficulty
        for i in range(x):
            self.mz.append([])
            for j in range(y):
                self.mz[i].append(maze_room.MazeRoom())
        self.disp = maze_graphics.MazeGraphics(field, x, y)

    def clearGame(self):
        self.start = 0
        self.end = 0
        self.walker = (0, 0)
        self.disp.setWalker(0, 0)
        self.disp.clear()
        self.is_timeout = False  # 重置超时标志位
        self.visited = []  # 重置机器路径
        self.visited2 = []  # 重置手动路径
        for i in range(self.field_height):
            for j in range(self.field_width):
                self.mz[i][j].clear()

    def addToFront(self, front, room):
        r, c = room
        if r > 0 and not self.mz[r - 1][c].visited():
            front.add((r - 1, c))
        if r < self.field_height - 1 and not self.mz[r + 1][c].visited():
            front.add((r + 1, c))
        if c > 0 and not self.mz[r][c - 1].visited():
            front.add((r, c - 1))
        if c < self.field_width - 1 and not self.mz[r][c + 1].visited():
            front.add((r, c + 1))
        return front

    def breakWall(self, r, c):
        breakable = self.RoomSet()
        if r > 0 and self.mz[r - 1][c].visited():
            breakable.add((r - 1, c))
        if r < self.field_height - 1 and self.mz[r + 1][c].visited():
            breakable.add((r + 1, c))
        if c > 0 and self.mz[r][c - 1].visited():
            breakable.add((r, c - 1))
        if c < self.field_width - 1 and self.mz[r][c + 1].visited():
            breakable.add((r, c + 1))

        if breakable.len() > 0:
            r1, c1 = breakable.pop()
            if r1 == r:
                if c1 < c:
                    self.mz[r][c].breakWall(maze_room.L_WALL)
                    self.mz[r1][c1].breakWall(maze_room.R_WALL)
                else:
                    self.mz[r][c].breakWall(maze_room.R_WALL)
                    self.mz[r1][c1].breakWall(maze_room.L_WALL)
            else:
                if r1 < r:
                    self.mz[r][c].breakWall(maze_room.U_WALL)
                    self.mz[r1][c1].breakWall(maze_room.D_WALL)
                else:
                    self.mz[r][c].breakWall(maze_room.D_WALL)
                    self.mz[r1][c1].breakWall(maze_room.U_WALL)
            self.disp.connectRooms(r, c, r1, c1)

    def drawGame(self):
        row = random.randint(0, self.field_height - 1)
        col = random.randint(0, self.field_width - 1)
        self.mz[row][col].visit()
        front = self.RoomSet()
        front = self.addToFront(front, (row, col))

        while front.len() > 0:
            row, col = front.pop()
            self.mz[row][col].visit()
            self.breakWall(row, col)
            front = self.addToFront(front, (row, col))

        # 入口：底部随机位置（无需偏移）
        row = self.field_height - 1
        col = random.randint(0, self.field_width - 1)
        self.disp.breakWall(row, col, 'D')
        self.walker = (row, col)
        self.disp.setWalker(row, col)

        # 出口：顶部随机位置
        row = 0
        col = random.randint(0, self.field_width - 1)
        self.mz[row][col].breakWall(maze_room.U_WALL)
        self.disp.breakWall(row, col, 'U')
        self.exit = (row, col)
        self.disp.setGoal(row, col)

    def move(self, mv):
        if self.is_timeout:  # 如果已经超时，直接返回
            return False
        if self.start == 0:
            self.start = time.time()
        self.end = time.time()

        # 根据难度调整超时时间
        timeout = 30  # 默认普通难度
        if self.difficulty == "简单":
            timeout = 30
        elif self.difficulty == "困难":
            timeout = 30

        if self.end - self.start >= timeout:
            messagebox.showerror("超时！", "已超时，可点击查看答案")
            self.is_timeout = True  # 设置超时标志位
            return False  # 超时后返回False，避免弹出成功通关提示

        r, c = self.walker
        self.visited2.append((r, c))

        # 边界检查和移动逻辑
        if mv == 'U':
            if r == 0 or self.mz[r][c].hasWall(maze_room.U_WALL):
                messagebox.showerror("撞墙！", "请重新选择方向")
            else:
                self.walker = (r - 1, c)
                self.disp.moveWalker(r - 1, c)
                if (r - 1, c) == self.exit and not self.is_timeout:
                    return True
        elif mv == 'D':
            if r == self.field_height - 1 or self.mz[r][c].hasWall(maze_room.D_WALL):
                messagebox.showerror("撞墙！", "请重新选择方向")
            else:
                self.walker = (r + 1, c)
                self.disp.moveWalker(r + 1, c)
        elif mv == 'L':
            if c == 0 or self.mz[r][c].hasWall(maze_room.L_WALL):
                messagebox.showerror("撞墙！", "请重新选择方向")
            else:
                self.walker = (r, c - 1)
                self.disp.moveWalker(r, c - 1)
        elif mv == 'R':
            if c == self.field_width - 1 or self.mz[r][c].hasWall(maze_room.R_WALL):
                messagebox.showerror("撞墙！", "请重新选择方向")
            else:
                self.walker = (r, c + 1)
                self.disp.moveWalker(r, c + 1)

        return False

    def auto(self, x, y):
        r, c = self.walker
        xx, yy = self.exit
        self.answer(r, c, x, y)

    def answer(self, i, j, x, y):
        x1, y1 = self.walker
        xx, yy = self.exit
        if (x1, y1) == (xx, yy):
            messagebox.showwarning("提示", "查看答案后游戏将退出")
            time.sleep(1)
            return

        directions = []
        if i > 0 and self.mz[i - 1][j].noWall(maze_room.U_WALL) and (i - 1, j) not in self.visited:
            directions.append(('U', i - 1, j))
        if i < x - 1 and self.mz[i + 1][j].noWall(maze_room.D_WALL) and (i + 1, j) not in self.visited:
            directions.append(('D', i + 1, j))
        if j > 0 and self.mz[i][j - 1].noWall(maze_room.L_WALL) and (i, j - 1) not in self.visited:
            directions.append(('L', i, j - 1))
        if j < y - 1 and self.mz[i][j + 1].noWall(maze_room.R_WALL) and (i, j + 1) not in self.visited:
            directions.append(('R', i, j + 1))

        for d in directions:
            mv, ni, nj = d
            self.visited.append((i, j))
            self.visited2.append((i, j))
            self.walker = (ni, nj)
            self.disp.moveWalkerAnswer(ni, nj)
            self.answer(ni, nj, x, y)
            if (ni, nj) == (xx, yy):
                return
