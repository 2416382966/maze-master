#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Jolly_Son
# 功能：迷宫绘制
from PIL import Image, ImageTk
import tkinter as tk

x_offset = 0  # 顶部距离设为0
y_offset = 0  # 左侧距离设为0

BGC = '#ffffff'  # 白色
FGC = '#000000'  # 黑色
WKC = '#00fc0f'  # 湖蓝
VSC = '#000000'  # 黑色
RRR = '#ff0000'  # 红色
GGG = '#00ff00'  # 绿色
BBB = '#0000ff'  # 蓝色
XXX = '#000000'  # 黑色
LGB = '#8080ff'  # 浅蓝

ROOM_HEIGHT_IN_PIX = 35
ROOM_WIDTH_IN_PIX = 35

U_WALL = 1
R_WALL = 2
D_WALL = 4
L_WALL = 8


class MazeGraphics(object):
    DEBUG = 0
    roomheight = ROOM_HEIGHT_IN_PIX
    roomwidth = ROOM_WIDTH_IN_PIX
    walker = (0, 0)
    mz = []
    trail_colors = ['#000fff', '#3080ff', '#60b0ff', '#90d0ff', '#c0f0ff']

    class Room(object):
        def __init__(self, field, loc, width, height, parent):
            self.field = field
            self.parent = parent  # 保存对 MazeGraphics 实例的引用
            x0, y0 = loc
            self.loc = loc
            self.ld = (x0 + width, y0)
            self.ru = (x0, y0 + height)
            self.rd = (x0 + width, y0 + height)
            self.center = (x0 + width // 2, y0 + height // 2)

            self.uw = field.create_line(y0, x0, y0 + height, x0, fill=FGC)
            self.rw = field.create_line(y0 + height, x0, y0 + height, x0 + width, fill=FGC)
            self.dw = field.create_line(y0 + height, x0 + width, y0, x0 + width, fill=FGC)
            self.lw = field.create_line(y0, x0 + width, y0, x0, fill=FGC)

            x0 += 2
            y0 += 2
            x2 = x0 + width - 4
            y2 = y0 + height - 4
            self.wlk = field.create_oval(y0, x0, y2, x2, fill=BGC, outline=BBB)
            self.trail = []
            self.trail_step = 0

        def add_trail(self):
            if len(self.trail) >= 5:
                old = self.trail.pop(0)
                self.field.delete(old)
            x0, y0 = self.loc
            x0 += 2 + self.trail_step * 2
            y0 += 2 + self.trail_step * 2
            # 通过 parent 直接访问 MazeGraphics 的属性
            roomwidth = self.parent.roomwidth
            roomheight = self.parent.roomheight
            x2 = x0 + roomwidth - 4 - self.trail_step * 4
            y2 = y0 + roomheight - 4 - self.trail_step * 4
            trail = self.field.create_oval(
                y0, x0, y2, x2,
                fill=self.parent.trail_colors[self.trail_step],
                outline="",
                tags="trail"
            )
            self.trail.append(trail)
            self.trail_step = (self.trail_step + 1) % 5

        def clear(self):
            self.field.itemconfigure(self.uw, fill=FGC)
            self.field.itemconfigure(self.rw, fill=FGC)
            self.field.itemconfigure(self.dw, fill=FGC)
            self.field.itemconfigure(self.lw, fill=FGC)
            self.field.itemconfigure(self.wlk, fill=BGC)

        def setWalker(self):
            self.field.itemconfigure(self.wlk, fill=BBB)

        def setWalkerAnswer(self):
            self.field.itemconfigure(self.wlk, fill=GGG)

        def clearWalker(self):
            self.field.itemconfigure(self.wlk, fill=BGC)

        def markWalker(self):
            self.field.itemconfigure(self.wlk, fill=LGB)

        def markWalkerAnswer(self):
            self.field.itemconfigure(self.wlk, fill=GGG)

        def markVisited(self):
            self.field.itemconfigure(self.wlk, fill=VSC)

        def breakWall(self, wall):
            if wall == U_WALL:
                self.field.itemconfigure(self.uw, fill=BGC)
            elif wall == R_WALL:
                self.field.itemconfigure(self.rw, fill=BGC)
            elif wall == D_WALL:
                self.field.itemconfigure(self.dw, fill=BGC)
            elif wall == L_WALL:
                self.field.itemconfigure(self.lw, fill=BGC)

        def markCell(self, color):
            self.field.itemconfigure(self.wlk, fill=color)

    def __init__(self, field, x, y, bg_image_path=None):
        bg_width = y * self.roomwidth
        bg_height = x * self.roomheight
        if bg_image_path:
            try:
                self.bg_image = Image.open(bg_image_path)
                self.bg_photo = ImageTk.PhotoImage(
                    self.bg_image.resize((bg_width, bg_height), Image.Resampling.LANCZOS)
                )
                field.create_image(0, 0, image=self.bg_photo, anchor="nw", tags="bg")
            except Exception as e:
                print(f"Failed to load background image: {e}")
        self.field = field
        self.width = y
        self.height = x
        self.mz = []

        for i in range(x):
            self.mz.append([])
            for j in range(y):
                loc = (i * self.roomheight, j * self.roomwidth)
                # 传入 self 作为 parent 参数
                rm = self.Room(field, loc, self.roomwidth, self.roomheight, self)
                self.mz[i].append(rm)

    def clear(self):
        x, y = self.walker
        self.mz[x][y].clearWalker()
        self.walker = (0, 0)
        for i in range(self.height):
            for j in range(self.width):
                self.mz[i][j].clear()

    def breakWall(self, x, y, w):
        if w == 'U':
            self.mz[x][y].breakWall(U_WALL)
        else:
            self.mz[x][y].breakWall(D_WALL)

    def connectRooms(self, x, y, x1, y1):
        if x == x1:
            if y < y1:
                self.mz[x][y].breakWall(R_WALL)
                self.mz[x1][y1].breakWall(L_WALL)
            else:
                self.mz[x][y].breakWall(L_WALL)
                self.mz[x1][y1].breakWall(R_WALL)
        else:
            if x < x1:
                self.mz[x][y].breakWall(D_WALL)
                self.mz[x1][y1].breakWall(U_WALL)
            else:
                self.mz[x][y].breakWall(U_WALL)
                self.mz[x1][y1].breakWall(D_WALL)

    def clearWalker(self, i, j):
        self.mz[i][j].clearWalker()

    def setGoal(self, i, j):
        self.mz[i][j].markCell(RRR)

    def setWalker(self, i, j):
        x, y = self.walker
        self.mz[x][y].clearWalker()
        self.mz[i][j].setWalker()
        self.walker = (i, j)

    def moveWalker(self, i, j):
        x, y = self.walker
        self.mz[x][y].add_trail()
        self.mz[x][y].markWalker()
        self.mz[i][j].setWalker()
        self.walker = (i, j)

    def moveWalkerAnswer(self, i, j):
        x, y = self.walker
        self.mz[x][y].add_trail()
        self.mz[x][y].markWalkerAnswer()
        self.mz[i][j].setWalkerAnswer()
        self.walker = (i, j)
