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
    visited = []  # 记录机器走迷宫的路径
    visited2 = []  # 记录手动走迷宫的路径
    start = 0      # 记录游戏开始的时间戳
    end = 0       # 记录游戏结束的时间戳

    # 小蓝点对象
    class RoomSet(object):
        # A helper - 'ordered' set with random pop
        def __init__(self):
            self.coll = []
        
        def add(self, item):
            if item not in self.coll:
                self.coll.append(item)

        def pop(self):
            #print(self.coll)
            rnd = random.randint(0, len(self.coll) - 1)
            #item = self.coll[rnd]
            item = self.coll.pop(rnd)
            return item
        
        def len(self):
            return len(self.coll)
        
        def clear(self):
            # 移除所有的元素
            self.coll.clear()

    def __init__(self, field, x, y):
        self.field_height = x
        self.field_width = y
        self.walker = (0,0)
        self.Walker = (0,0)
        self.field = field

        # 建立迷宫 - 数组的方格
        for i in range(0, x):
            self.mz.append([]) # 增加一行
            for j in range(0, y):
                rm = maze_room.MazeRoom()
                self.mz[i].append(rm) # 一行增加一个方格（列的方格）
        # 创建迷宫的表示
        self.disp = maze_graphics.MazeGraphics(field, x, y)

    def clearGame(self):
        # 清除计时
        self.start = 0
        self.end = 0
        # 清除游戏
        self.walker = (0,0)
        self.disp.setWalker(0, 0)
        self.disp.clear()
        for i in range(0, self.field_height):
            for j in range(0, self.field_width):
                self.mz[i][j].clear()

    # 格子的迷宫边框和路径形成的算法
    def addToFront(self, front, room):
        # Adds the neighbouring non-visited rooms to the front set
        r, c = room
        if r != 0:
            if self.mz[r - 1][c].visited() == False:
                front.add((r - 1, c))
        if r != self.field_height - 1:
            if self.mz[r + 1][c].visited() == False:
                front.add((r + 1, c))
        if c != 0:
            if self.mz[r][c - 1].visited() == False:
                front.add((r, c - 1))
        if c != self.field_width - 1:
            if self.mz[r][c + 1].visited() == False:
                front.add((r, c + 1))
        return front

    # 打破一条可以走通的路径
    def breakWall(self, r, c):
        # 从两条边之间选择一个可能出去的地方并且打破它
        # 创建一个可能的墙然后去打破它
        # 一堵墙吸住了两个分离的走过的格子
        breakable = self.RoomSet()
        if r != 0:
            if self.mz[r - 1][c].visited():
                breakable.add((r - 1, c))
        if r != self.field_height - 1:
            if self.mz[r + 1][c].visited():
                breakable.add((r + 1, c))
        if c != 0:
            if self.mz[r][c - 1].visited():
                breakable.add((r, c - 1))
        if c != self.field_width - 1:
            if self.mz[r][c + 1].visited():
                breakable.add((r, c + 1))

        # 随机选择一个可能的方格子
        r1, c1 = breakable.pop()
        # 打破这墙从方格里分离
        if r1 == r:
            if c1 < c:
                # 这墙是前面方格的
                self.mz[r][c].breakWall(maze_room.L_WALL)
                # 这相同的墙是已经访问过的
                self.mz[r1][c1].breakWall(maze_room.R_WALL)
                # 更新显示
                self.disp.connectRooms(r, c, r1, c1)
            else:
                self.mz[r][c].breakWall(maze_room.R_WALL)
                self.mz[r1][c1].breakWall(maze_room.L_WALL)
                self.disp.connectRooms(r, c, r1, c1)
        else:
            if r1 < r:
                self.mz[r][c].breakWall(maze_room.U_WALL)
                self.mz[r1][c1].breakWall(maze_room.D_WALL)
                self.disp.connectRooms(r, c, r1, c1)
            else:
                self.mz[r][c].breakWall(maze_room.D_WALL)
                self.mz[r1][c1].breakWall(maze_room.U_WALL)
                self.disp.connectRooms(r, c, r1, c1)
        if self.DEBUG >= 1:
            print("Clear breakable: size = ", breakable.len())

    # 绘制迷宫
    def drawGame(self):
        # 选择一个开始点并且标记为已经访问过
        col = random.randint(0, self.field_width - 1)
        row = random.randint(0, self.field_height - 1)
        self.mz[row][col].visit()
        # print("Starting point: ", (row, col))

        # 设置在前面
        front = self.RoomSet()
        front = self.addToFront(front, (row, col))

        # 该算法被称为 传播算法
        # 改进的随机整数规划算法
        while front.len() > 0: # 房间在前面
            # 选择一个作为下一个访问格子
            row, col = front.pop()
            self.mz[row][col].visit()
            # 添加到这个迷宫
            self.breakWall(row, col)
            # 添加这个没有被访问的新的邻居格子
            # 对于前面的设置
            front = self.addToFront(front, (row, col))
            if self.DEBUG >= 1:
                print("front size = ", front.len())
            
            if self.DEBUG > 1:
                messagebox.showinfo("Break", "continue")
        if self.DEBUG >= 1:
            print("Generated: count = ", count)
            input("press any key")

        # 选择一个入口位置 (从底边)
        row = self.field_height - 1
        col = random.randint(0, self.field_width - 1)
        # 小蓝点不能打破那个逻辑墙
        # 只能走在迷宫的逻辑墙外面
        # 尽管显示了入口位置
        # 也不能执行这句self.mz[row][col].breakWall(maze_room.D_WALL)
        # 这句会使蓝点走出迷宫入口
        self.disp.breakWall(row, col, 'D')
        # And put the walker there
        self.walker = (row, col)
        self.disp.setWalker(row, col)

        # 选择一个出口位置 (向上的那一边)
        row = 0
        col = random.randint(0, self.field_width - 1)
        # 允许移动出结束的迷宫边
        # 这走迷宫从不退出, 通过...
        self.mz[row][col].breakWall(maze_room.U_WALL)
        self.disp.breakWall(row, col, 'U')
        self.exit = (row, col)
        # 显示小红色的终点
        self.disp.setGoal(row, col)

    # 手动走迷宫的函数
    def move(self, mv):
        # 游戏开始只要走动小点，视为游戏开始并存入开始时间
        if self.start == 0:
            self.start = time.time()

        # 判断大于等于30s为超时
        if (self.end - self.start) >= 30:
            messagebox.showerror("超时！", "对不起，您已经超时了！别气馁，下次继续努力！可以点击窗口下方\"悄悄看答案\"哦。")

        self.end = time.time() # 每次走动刷新一次结束计时

        # 移动小蓝点
        r, c = self.walker # from where
        # print("room ",r,c," = ", hex(self.mz[r][c].getRoom()))
        # 根据玩家的命令尝试移动到任何地方
        self.visited2.append(self.walker)
        if mv == 'U': # 向上移动
            if self.mz[r][c].hasWall(maze_room.U_WALL):
                messagebox.showerror("你撞墙了！", "你是不撞北墙不回头？")
                # 不能移动，这里有墙
            else:
                x, y = self.exit # 如果我们在这个出口的前面
                if (x == r) and (y == c):
                    # 不能移动，但是会通知你你已经走出迷宫...
                    messagebox.showinfo("恭喜你！", "您已经成功走出迷宫！")
                    return False # 并且等待游戏

                # 或者，移动作为命令
                self.walker = (r - 1, c)
                self.disp.moveWalker(r - 1, c)

        elif mv == 'D': # 向下移动
            if self.mz[r][c].hasWall(maze_room.D_WALL):
                messagebox.showerror("你撞墙了！","你是不撞南墙不回头？")
            else:
                self.walker = (r + 1, c)
                self.disp.moveWalker(r + 1, c)

        elif mv == 'L': # 向左移动
            if self.mz[r][c].hasWall(maze_room.L_WALL):
                messagebox.showerror("你撞墙了！", "你是不撞西墙不回头？")
            else:
                self.walker = (r, c - 1)
                self.disp.moveWalker(r, c - 1)

        elif mv == 'R': # 向右移动
            if self.mz[r][c].hasWall(maze_room.R_WALL):
                messagebox.showerror("你撞墙了！", "你是不撞东墙不回头？")
            else:
                self.walker = (r, c + 1)
                self.disp.moveWalker(r, c + 1)

        return False # 寻求迷宫出口仍在继续

    # 自动走迷宫
    def auto(self,x,y):
        r, c = self.walker  # 开始的位置
        xx, yy = self.exit
        print('起点坐标 x、y:',r,c,'终点坐标x、y:',xx,yy)
        # exit()
        self.answer(r, c, x, y)

    # 自动走迷宫得到答案的具体递归代码
    # 递归的“核心”代码
    def answer(self,i,j,x,y):
        x1, y1 = self.walker #当前点所在位置 (0,7)
        xx, yy = self.exit  # 结束的出口前面(9,3)
        found = None

        # 走到结束出口（小蓝点位置与出口位置相同），找到的标志位 found = True
        if (xx == x1) and (yy == y1):
            found = True
            print("您的操作路径：",self.visited)
            print("机器继续完成的路径：",self.visited2)

        if found == True:
            messagebox.showwarning("小提示","您只有一次看答案的机会，单击\"确定\"游戏将退出！")
            time.sleep(1)
            return

        up = self.mz[x1][y1].noWall(maze_room.U_WALL)  # 向上走没有墙 noWall
        down = self.mz[x1][y1].noWall(maze_room.D_WALL) # 向下走没有墙
        left = self.mz[x1][y1].noWall(maze_room.L_WALL)  # 向左走没有墙
        right = self.mz[x1][y1].noWall(maze_room.R_WALL)  # 向右走没有墙

        if (not found):
            self.visited.append(self.walker)
            self.visited2.append(self.walker)

        if (not found) and (i - 1 >= 0) and (up) and ((i - 1, j) not in self.visited):
            print('往上走')
            self.walker = (i - 1, j)    #  格子代码走了一步
            self.disp.moveWalkerAnswer(i - 1, j)   #  格子在界面上的显示走了一步
            self.answer(i - 1, j, x, y)  # 又递归调用一次代码，直到走出去的时候标志位为True时结束

        if (not found) and (i + 1 <= x+1) and (down) and ((i + 1, j) not in self.visited):
            print('往下走')
            self.walker = (i + 1, j)
            self.disp.moveWalkerAnswer(i + 1, j)
            self.answer(i + 1, j, x, y)

        if (not found) and (j - 1 >= 0) and (left) and ((i, j - 1) not in self.visited):
            print('往左走')
            self.walker = (i, j - 1)
            self.disp.moveWalkerAnswer(i, j - 1)
            self.answer(i, j- 1, x, y)

        if (not found) and (j + 1 <= y+1) and (right) and ((i, j + 1) not in self.visited):
            print('往右走')
            self.walker = (i ,j + 1)
            self.disp.moveWalkerAnswer(i, j + 1)
            self.answer(i, j + 1, x, y)

        return found