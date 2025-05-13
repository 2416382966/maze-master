#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Jolly_Son
# 功能：主程序，包括按键处理等

from tkinter import *
import tkinter as tk
import time
import maze_game
import maze_graphics

# 这个是设置迷宫规模
x = 10
y = 10


class Application(tk.Frame):
    def __init__(self, master=None):
        # 构造函数
        print("初始化应用程序...")
        tk.Frame.__init__(self, master)
        self.x = x
        self.y = y
        self.grid()
        self.field = self.createWidgets(x, y)
        print(f"计时器标签类型: {type(self.timer_label)}")
        self.game = maze_game.MazeGame(self.field, self.x - 2, self.y - 2)
        self.start_time = None  # 开始时间
        self.timer_id = None  # 计时器ID
        self.playGame()

    def createWidgets(self, x, y):
        print("创建游戏界面组件...")
        # 创建图形化界面的一部分
        # 设置迷宫宽高
        yy = y * maze_graphics.ROOM_WIDTH_IN_PIX
        xx = x * maze_graphics.ROOM_HEIGHT_IN_PIX

        # 先设置整个 窗口 为白色背景 maze_graphics.BGC
        field = tk.Canvas(self, width=yy, height=xx, background=maze_graphics.BGC)
        field.grid()

        # 迷宫界面中间的 “游戏规则” 标签 Label
        self.textLabel1 = tk.Label(self, font=("微软雅黑", 11), fg='blue',
                                   text="游戏规则：１．蓝点是入口，红点是出口处　　　　 ")
        self.textLabel1.grid()
        self.textLabel2 = tk.Label(self, font=("微软雅黑", 11), fg='blue',
                                   text="         ２．使用'↑' '↓' '←' '→'进行游戏　　")
        self.textLabel2.grid()
        self.textLabel3 = tk.Label(self, font=("微软雅黑", 11), fg='blue', text="　　　　　３．请尽快找到出口　　　　　　　　")
        self.textLabel3.grid()
        self.textLabel4 = tk.Label(self, font=("微软雅黑", 11), fg='blue',
                                   text="　　　　４．您只拥有一次看答案的机会      　　")
        self.textLabel4.grid()
        self.textLabel5 = tk.Label(self, text=" ")
        self.textLabel5.grid()

        # 新增：计时器标签
        print("创建计时器标签...")
        self.timer_label = tk.Label(self, font=("微软雅黑", 14, "bold"), fg='red', text="用时: 00:00")
        self.timer_label.grid()
        print(f"创建的计时器标签: {self.timer_label}")

        # 下方的四个功能按钮 Button
        fm = Frame(height=30, width=180)
        fm1 = Frame(fm, height=30, width=60)
        fm2 = Frame(fm, height=30, width=60)
        fm3 = Frame(fm, height=30, width=60)
        fm4 = Frame(fm, height=30, width=60)
        fm.grid(row=2)
        fm1.pack(side='left')
        fm2.pack(side='left')
        fm3.pack(side='left')
        fm4.pack(side='right')
        Button(fm1, text="悄悄看答案", width=10, command=self.answer).pack(side='left')
        Button(fm2, text="开始游戏", width=10, command=self.startGame).pack(side='left')
        Button(fm3, text="再来一次", width=10, command=self.playGame).pack(side='left')
        Button(fm4, text="退出游戏", width=10, command=self.stopGame).pack(side='right')
        return field

    def addHandler(self, field):
        # 添加一个按键处理
        seq = '<Any-KeyPress>'
        field.bind_all(sequence=seq, func=self.handleKey, add=None)

    def initGame(self):
        print("初始化游戏...")
        # 设置游戏初始化
        self.game.clearGame()
        self.game.drawGame()
        self.updateTimer(0)  # 重置计时器显示

    def answer(self):
        #  “悄悄看答案”部分
        self.game.auto(x, y)
        self.stopTimer()

    def stopGame(self):
        # 杀死这个应用
        self.stopTimer()
        self.done = True
        app.destroy()
        self.quit()

    def handleKey(self, event):
        # 按键处理程序，获取键盘上的上下左右按键
        if False:
            print("handleKey: ", event.keysym, event.keycode, event.keysym_num)
        mv = None
        if event.keycode == 104:  # Down
            mv = 'D'
        elif event.keycode == 100:  # Left
            mv = 'L'
        elif event.keycode == 102:  # Right
            mv = 'R'
        elif event.keycode == 98:  # Up
            mv = 'U'
        elif event.keycode == 88:  # KP_Down
            mv = 'D'
        elif event.keycode == 80:  # KP_Up
            mv = 'U'
        elif event.keycode == 83:  # KP_Left
            mv = 'L'
        elif event.keycode == 85:  # KP_Right
            mv = 'R'
        elif event.keysym == 'Down':  # ??_Down
            mv = 'D'
        elif event.keysym == 'Up':  # ??_Up
            mv = 'U'
        elif event.keysym == 'Left':  # ??_Left
            mv = 'L'
        elif event.keysym == 'Right':  # ??_Right
            mv = 'R'
        else:
            return

        # 如果计时器未启动，先启动计时器
        if self.start_time is None:
            print("启动计时器...")
            self.startTimer()

        # Player's move
        if self.game.move(mv):
            # Solved - exit the program
            self.stopTimer()
            self.showCompletionTime()
            self.stopGame()

    def playGame(self):
        print("开始游戏...")
        # 开始游戏
        self.initGame()
        self.addHandler(self.field)
        # 重置计时器状态
        self.start_time = None
        self.updateTimer(0)

    def startGame(self):
        print("通过按钮启动游戏...")
        # 专门用于启动游戏和计时器的方法
        self.playGame()
        self.startTimer()

    def startTimer(self):
        print("计时器启动中...")
        # 启动计时器
        if self.start_time is None:
            self.start_time = time.time()
            print(f"开始时间: {self.start_time}")
            self.updateTimer()

    def stopTimer(self):
        # 停止计时器
        if self.timer_id:
            print("停止计时器...")
            self.after_cancel(self.timer_id)
            self.timer_id = None

    def updateTimer(self, seconds=None):
        # 更新计时器显示
        if self.timer_label is None:
            print("警告: 计时器标签未正确初始化!")
            return

        print(f"更新计时器: {self.timer_label}")

        if seconds is None:
            if self.start_time:
                elapsed = int(time.time() - self.start_time)
            else:
                elapsed = 0
        else:
            elapsed = seconds

        minutes, secs = divmod(elapsed, 60)
        time_str = f"用时: {minutes:02d}:{secs:02d}"
        self.timer_label.config(text=time_str)

        # 继续计时
        if self.start_time:
            self.timer_id = self.after(1000, self.updateTimer)
            print(f"下一次更新将在1秒后进行 (ID: {self.timer_id})")

    def showCompletionTime(self):
        # 显示完成时间
        if self.start_time:
            elapsed = int(time.time() - self.start_time)
            minutes, secs = divmod(elapsed, 60)
            tk.messagebox.showinfo("恭喜！", f"你成功走出了迷宫！\n用时: {minutes}分{secs}秒")

    def protocol(self, param, closeWindow):
        # 添加此函数跳到一个空函数（closeWindow）后解决关闭窗口报错问题
        pass


def generateMaze():
    # 产生迷宫
    global x, y
    # 修复：使用 == 比较字符串值
    if width.get() == '' or height.get() == '':  # 规模框里不输入任何东西则执行默认规模10*10
        y, x = 12, 12
    else:
        y = int(width.get()) + 2
        x = int(height.get()) + 2
    print(f"生成迷宫: 宽度={y - 2}, 高度={x - 2}")
    window.destroy()  # 产生完成迷宫窗口后关闭 第一个设置迷宫规模的窗口window 对象


# 设置规模时 使输入框只能输入“数字”的模块相关的
def test(content):  # 如果你不加上==""的话，你就会发现删不完。总会剩下一个数字
    if content.isdigit() or (content == ""):
        return True
    else:
        return False


# 设置规模窗口的部分
window = tk.Tk()
window.title('DIY 我的迷宫！')
window.geometry('450x255')
v1 = StringVar()  # 调用函数，使用户可以调整游戏窗口大小
v2 = StringVar()
v1.set('10')
v2.set('10')
testCMD = window.register(test)  # 包装函数
widthLabel = tk.Label(text="设置迷宫高:").pack()
width = tk.Entry(window, show=None, textvariable=v1,
                 validate='key',  # 发生任何变动的时候，就会调用validatecommand
                 validatecommand=(testCMD, '%P')
                 )  # %P代表输入框的实时内容
# 当validate为key的时候，获取输入框内容就不可以用get（）
width.pack()
heightLabel = tk.Label(text="设置迷宫宽:").pack()
# 因为只有当validatecommand判断正确后，返回true。才会改变.get()返回的值.所以要用%P
height = tk.Entry(window, show=None, textvariable=v2, validate='key', validatecommand=(testCMD, '%P'))
height.pack()
tk.Label(text="  ").pack()
# 绑定generateMaze函数，触发迷宫生成流程
generate = tk.Button(window, text='生 成 迷 宫', width=11, height=1, command=generateMaze).pack()
tk.Label(text="  ").pack()
tk.Label(fg='blue', font=("微软雅黑", 10), text="推荐迷宫 10*10 ").pack()
tk.Label(fg='blue', font=("微软雅黑", 10), text="最大宽高最好不要超过12以免显示超出显示屏  ").pack()
window.mainloop()


def closeWindow():  # 正式运行整个迷宫窗口的部分
    return


print("创建应用程序实例...")
app = Application()  # 实例化主游戏应用，继承tk.Frame实现迷宫核心逻辑
app.master.title('Maze-迷宫小游戏 v1.0')
app.protocol('WM_DELETE_WINDOW', closeWindow)  # 添加此句跳到一个空函数（closeWindow）后解决关闭窗口报错问题
print("启动主事件循环...")
app.mainloop()
