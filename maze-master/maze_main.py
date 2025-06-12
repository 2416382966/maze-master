#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Jolly_Son
# 功能：主程序，包括按键处理等
from tkinter import *
import tkinter as tk
from tkinter import filedialog
import time
import maze_game
import maze_graphics
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.font_manager as fm

# 设置matplotlib支持中文显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'WenQuanYi Micro Hei', 'Heiti TC']  # 用于显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用于正常显示负号

# 全局变量
x = 10  # 初始迷宫尺寸
y = 10
bg_image_path = None
data = []  # 用于存储游戏数据



class Application(tk.Frame):
    def __init__(self, master=None, width=10, height=10, bg_path=None, difficulty="普通"):
        super().__init__(master)
        self.master = master
        self.bg_image_path = bg_path
        self.difficulty = difficulty

        # 根据难度设置迷宫尺寸
        if self.difficulty == "简单":
            self.x, self.y = 10, 10
        elif self.difficulty == "普通":
            self.x, self.y = 15, 15
        elif self.difficulty == "困难":
            self.x, self.y = 15, 20

        self.start_time = None
        self.grid()
        self.field = self.createWidgets(self.x, self.y)
        # 传递难度参数
        self.game = maze_game.MazeGame(self.field, self.x, self.y, self.difficulty)
        self.playGame()
        if self.master:
            self.addHandler(self.master)
            # 绑定Enter键到startGame方法
            self.master.bind("<Return>", lambda event: self.startGame())

    def change_difficulty(self):
        # 更新难度并重新开始游戏
        self.difficulty = self.difficulty_var.get()

        # 根据难度设置迷宫尺寸
        if self.difficulty == "简单":
            self.x, self.y = 10, 10
        elif self.difficulty == "普通":
            self.x, self.y = 15, 15
        elif self.difficulty == "困难":
            self.x, self.y = 15, 20

        self.difficulty_label.config(text=f"当前难度: {self.difficulty}")

        # 根据难度调整超时时间
        timeout = 30  # 默认普通难度
        if self.difficulty == "简单":
            timeout = 30
        elif self.difficulty == "困难":
            timeout = 30

        # 重置游戏
        # 重新创建画布以适应新的迷宫尺寸
        self.field.destroy()
        self.field = self.createWidgets(self.x, self.y)
        # 传递难度参数
        self.game = maze_game.MazeGame(self.field, self.x, self.y, self.difficulty)
        self.playGame()

    def createWidgets(self, x, y):
        # 计算真实迷宫尺寸
        room_width = maze_graphics.ROOM_WIDTH_IN_PIX
        room_height = maze_graphics.ROOM_HEIGHT_IN_PIX
        canvas_width = y * room_width
        canvas_height = x * room_height

        # 创建带滚动条的Canvas
        frame = Frame(self)
        frame.grid(row=0, column=0, sticky="nsew")
        canvas = tk.Canvas(frame, width=canvas_width, height=canvas_height,
                           scrollregion=(0, 0, canvas_width, canvas_height),
                           background=maze_graphics.BGC)
        hbar = Scrollbar(frame, orient=HORIZONTAL)
        hbar.pack(side=BOTTOM, fill=X)
        hbar.config(command=canvas.xview)
        vbar = Scrollbar(frame, orient=VERTICAL)
        vbar.pack(side=RIGHT, fill=Y)
        vbar.config(command=canvas.yview)
        canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        canvas.pack(side=LEFT, expand=True, fill=BOTH)

        # 游戏规则标签
        self.textLabel1 = tk.Label(self, font=("微软雅黑", 11), fg='blue',
                                   text="游戏规则：１．蓝点是入口，红点是出口")
        self.textLabel1.grid(row=1, sticky=W, padx=5)
        self.textLabel2 = tk.Label(self, font=("微软雅黑", 11), fg='blue',
                                   text="         ２．使用'↑' '↓' '←' '→'键移动")
        self.textLabel2.grid(row=2, sticky=W, padx=5)
        self.textLabel3 = tk.Label(self, font=("微软雅黑", 11), fg='blue',
                                   text=f"　　　　３．限时{self.get_timeout()}秒，超时失败")
        self.textLabel3.grid(row=3, sticky=W, padx=5)
        self.textLabel4 = tk.Label(self, font=("微软雅黑", 11), fg='blue',
                                   text="　　　　４．按Enter键开始游戏")
        self.textLabel4.grid(row=4, sticky=W, padx=5)
        self.textLabel5 = tk.Label(self, text=" ")
        self.textLabel5.grid(row=5)

        # 计时器标签
        self.timer_label = tk.Label(self, font=("微软雅黑", 14, "bold"), fg='red', text="按Enter键开始计时")
        self.timer_label.grid(row=6, pady=5)

        # 当前难度显示
        self.difficulty_label = tk.Label(self, font=("微软雅黑", 12), text=f"当前难度: {self.difficulty}")
        self.difficulty_label.grid(row=7, pady=2)

        # 难度选择框架
        difficulty_frame = Frame(self)
        difficulty_frame.grid(row=8, pady=5)

        self.difficulty_var = StringVar(value=self.difficulty)

        Label(difficulty_frame, text="选择难度:").grid(row=0, column=0, padx=5)
        easy_radio = Radiobutton(difficulty_frame, text="简单", variable=self.difficulty_var,
                                 value="简单", command=self.change_difficulty)
        easy_radio.grid(row=0, column=1, padx=5)
        medium_radio = Radiobutton(difficulty_frame, text="普通", variable=self.difficulty_var,
                                   value="普通", command=self.change_difficulty)
        medium_radio.grid(row=0, column=2, padx=5)
        hard_radio = Radiobutton(difficulty_frame, text="困难", variable=self.difficulty_var,
                                 value="困难", command=self.change_difficulty)
        hard_radio.grid(row=0, column=3, padx=5)

        # 功能按钮
        fm = Frame(self)
        fm.grid(row=9, pady=5, sticky="ew")

        # 保留所有按钮但调整提示
        Button(fm, text="悄悄看答案", width=10, command=self.answer).grid(row=0, column=0, padx=5)
        Button(fm, text="开始游戏", width=10, command=self.startGame).grid(row=0, column=1, padx=5)
        Button(fm, text="再来一次", width=10, command=self.playGame).grid(row=0, column=2, padx=5)
        Button(fm, text="退出游戏", width=10, command=self.stopGame).grid(row=0, column=3, padx=5)
        Button(fm, text="选择背景", width=10, command=self.select_background).grid(row=0, column=4, padx=5)
        Button(fm, text="调整大小", width=10, command=self.adjust_maze_size).grid(row=0, column=5, padx=5)
        Button(fm, text="查看数据分析", width=10, command=self.show_data_analysis).grid(row=0, column=6, padx=5)

        return canvas

    def get_timeout(self):
        # 根据难度返回超时时间
        if self.difficulty == "简单":
            return 30
        elif self.difficulty == "普通":
            return 30
        elif self.difficulty == "困难":
            return 30
        return 30

    def addHandler(self, master):
        # 绑定方向键到主窗口
        master.bind('<Up>', lambda e: self.handleKey(e, 'U'))
        master.bind('<Down>', lambda e: self.handleKey(e, 'D'))
        master.bind('<Left>', lambda e: self.handleKey(e, 'L'))
        master.bind('<Right>', lambda e: self.handleKey(e, 'R'))

    def initGame(self):
        self.game.clearGame()
        self.disp = maze_graphics.MazeGraphics(self.field, self.x, self.y, self.bg_image_path)
        self.game.disp = self.disp
        self.game.drawGame()
        self.updateTimer(0)

    def answer(self):
        self.game.auto(self.x, self.y)
        self.stopTimer()

    def stopGame(self):
        self.stopTimer()
        if self.master:
            self.master.destroy()

    def handleKey(self, event, mv):
        # 简化按键处理，直接使用传入的mv方向
        if self.start_time is None:
            self.startTimer()
        if self.game.move(mv):
            self.stopTimer()
            self.showCompletionTime()
            self.collect_data()  # 收集数据
            tk.messagebox.showinfo("成功！", "恭喜走出迷宫！")  # 显示到达终点提示
            # 不再调用 stopGame，让玩家可以继续查看结果
            # self.stopGame()

    def playGame(self):
        self.initGame()
        if self.master:
            self.addHandler(self.master)
        self.start_time = None
        self.timer_label.config(text="按Enter键开始计时")  # 更新计时器标签提示
        # 重置游戏的开始时间、结束时间和超时标志位
        self.game.start = 0
        self.game.end = 0
        self.game.is_timeout = False

    def startGame(self):
        # 如果游戏已经开始，不再重复启动
        if self.start_time is not None:
            return

        if self.start_time is None:
            self.start_time = time.time()
            self.updateTimer()

    def startTimer(self):
        if self.start_time is None:
            self.start_time = time.time()
            self.updateTimer()

    def stopTimer(self):
        if hasattr(self, 'timer_id') and self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None

    def updateTimer(self, seconds=None):
        if not hasattr(self, 'timer_label') or not self.timer_label:
            return
        if seconds is None:
            elapsed = int(time.time() - self.start_time) if self.start_time else 0
        else:
            elapsed = seconds

        # 根据难度调整超时时间
        timeout = self.get_timeout()

        minutes, secs = divmod(elapsed, 60)
        time_str = f"用时: {minutes:02d}:{secs:02d}"

        # 超时处理
        if elapsed >= timeout:
            time_str += " (已超时)"
            self.timer_label.config(text=time_str, fg='red')
            self.stopTimer()
            tk.messagebox.showinfo("提示", "游戏超时！请重新开始。")
            self.playGame()
        else:
            self.timer_label.config(text=time_str)

        if self.start_time:
            self.timer_id = self.after(1000, self.updateTimer)

    def showCompletionTime(self):
        if self.start_time:
            elapsed = int(time.time() - self.start_time)
            minutes, secs = divmod(elapsed, 60)
            tk.messagebox.showinfo("恭喜！", f"成功走出迷宫！\n用时: {minutes}分{secs}秒")

    def protocol(self, param, closeWindow):
        pass  # 处理窗口关闭事件

    def select_background(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.bg_image_path = file_path
            self.playGame()

    def adjust_maze_size(self):
        # 创建调整迷宫大小的窗口
        size_window = tk.Toplevel(self.master)
        size_window.title('调整迷宫大小')
        size_window.geometry('200x120')
        size_window.resizable(False, False)

        v1 = StringVar(value=str(self.x))
        v2 = StringVar(value=str(self.y))

        testCMD = size_window.register(lambda c: c.isdigit() or c == "")

        Label(size_window, text="宽度:").pack(pady=5)
        width = Entry(size_window, textvariable=v1, validate='key', validatecommand=(testCMD, '%P'))
        width.pack(pady=2)

        Label(size_window, text="高度:").pack(pady=5)
        height = Entry(size_window, textvariable=v2, validate='key', validatecommand=(testCMD, '%P'))
        height.pack(pady=2)

        def apply_size():
            width_val = width.get() or '10'
            height_val = height.get() or '10'
            if not width_val.isdigit() or not height_val.isdigit():
                tk.messagebox.showerror("错误", "请输入数字！")
                return
            new_width = int(width_val)
            new_height = int(height_val)

            # 重新创建游戏实例
            self.master.destroy()
            new_root = tk.Tk()
            new_root.title('Maze-迷宫小游戏 v1.0')
            app = Application(master=new_root, width=new_height, height=new_width,
                              bg_path=self.bg_image_path, difficulty=self.difficulty)
            app.mainloop()
            size_window.destroy()

        Button(size_window, text="应用", width=10, command=apply_size).pack(pady=10)

    def collect_data(self):
        if self.start_time:
            elapsed = int(time.time() - self.start_time)
            data.append({
                "width": self.x,
                "height": self.y,
                "difficulty": self.difficulty,
                "time": elapsed
            })

    def show_data_analysis(self):
        if not data:
            tk.messagebox.showinfo("提示", "暂无游戏数据，请先进行游戏。")
            return

        df = pd.DataFrame(data)

        # 创建一个新窗口显示图表
        analysis_window = tk.Toplevel(self.master)
        analysis_window.title("数据分析")

        # 柱状图：不同难度的平均完成时间
        fig1 = plt.Figure(figsize=(6, 4), dpi=100)
        ax1 = fig1.add_subplot(111)
        avg_time_by_difficulty = df.groupby('difficulty')['time'].mean()
        avg_time_by_difficulty.plot(kind='bar', ax=ax1)
        ax1.set_title('不同难度的平均完成时间')
        ax1.set_xlabel('难度')
        ax1.set_ylabel('平均完成时间（秒）')
        canvas1 = FigureCanvasTkAgg(fig1, master=analysis_window)
        canvas1.draw()
        canvas1.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # 饼状图：不同难度的游戏占比
        fig2 = plt.Figure(figsize=(6, 4), dpi=100)
        ax2 = fig2.add_subplot(111)
        difficulty_counts = df['difficulty'].value_counts()
        difficulty_counts.plot(kind='pie', ax=ax2, autopct='%1.1f%%')
        ax2.set_title('不同难度的游戏占比')
        canvas2 = FigureCanvasTkAgg(fig2, master=analysis_window)
        canvas2.draw()
        canvas2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # 折线图：完成时间随游戏次数的变化
        fig3 = plt.Figure(figsize=(6, 4), dpi=100)
        ax3 = fig3.add_subplot(111)
        df['game_number'] = range(1, len(df) + 1)
        df.plot(x='game_number', y='time', ax=ax3)
        ax3.set_title('完成时间随游戏次数的变化')
        ax3.set_xlabel('游戏次数')
        ax3.set_ylabel('完成时间（秒）')
        canvas3 = FigureCanvasTkAgg(fig3, master=analysis_window)
        canvas3.draw()
        canvas3.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # 雷达图：不同难度下的平均宽度、高度和完成时间
        fig4 = plt.Figure(figsize=(6, 4), dpi=100)
        ax4 = fig4.add_subplot(111, polar=True)

        # 确保有足够的数据点用于雷达图
        stats = df.groupby('difficulty').mean()
        if len(stats) < 2:
            tk.messagebox.showinfo("提示", "数据不足，无法绘制雷达图。请至少完成两个不同难度的游戏。")
            canvas4 = FigureCanvasTkAgg(fig4, master=analysis_window)
            canvas4.draw()
            canvas4.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            return
        labels = stats.index.tolist()
        num_vars = len(labels)
        # 计算雷达图的角度
        angles = [n / float(num_vars) * 2 * 3.14159 for n in range(num_vars)]
        angles += angles[:1]  # 闭合雷达图
        # 提取需要在雷达图上显示的指标
        metrics = ['width', 'height', 'time']
        values = []

        for label in labels:
            # 从统计数据中提取每个难度的指标值
            row = stats.loc[label]
            # 只选择我们关心的指标
            row_values = [row[metric] for metric in metrics]
            # 归一化处理，使不同指标可以在同一雷达图上比较
            if max(row_values) > 0:
                row_values = [val / max(row_values) for val in row_values]
            # 闭合雷达图
            row_values += row_values[:1]
            values.append(row_values)

        # 绘制雷达图
        for i, val in enumerate(values):
            # 确保角度和值的维度匹配
            ax4.plot(angles, val, label=labels[i])
            ax4.fill(angles, val, alpha=0.25)

        # 设置雷达图的刻度和标签
        ax4.set_xticks(angles[:-1])
        ax4.set_xticklabels(labels)
        ax4.set_title('不同难度下的迷宫特性比较')
        ax4.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))

        canvas4 = FigureCanvasTkAgg(fig4, master=analysis_window)
        canvas4.draw()
        canvas4.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


# 第一个界面：自定义迷宫大小
def show_startup_window():
    global x, y, bg_image_path

    window = tk.Tk()
    window.title('迷宫游戏 - 自定义设置')
    window.geometry('300x250')
    window.resizable(False, False)

    # 标题
    title_label = tk.Label(window, text="迷宫游戏", font=("微软雅黑", 16, "bold"))
    title_label.pack(pady=10)

    # 迷宫大小设置
    size_frame = Frame(window)
    size_frame.pack(pady=10)

    Label(size_frame, text="迷宫宽度:").grid(row=0, column=0, sticky=W, padx=5, pady=5)
    width_var = StringVar(value="10")
    width_entry = Entry(size_frame, textvariable=width_var, width=10)
    width_entry.grid(row=0, column=1, padx=5, pady=5)

    Label(size_frame, text="迷宫高度:").grid(row=1, column=0, sticky=W, padx=5, pady=5)
    height_var = StringVar(value="10")
    height_entry = Entry(size_frame, textvariable=height_var, width=10)
    height_entry.grid(row=1, column=1, padx=5, pady=5)

    # 难度设置
    difficulty_var = StringVar(value="普通")
    difficulty_frame = Frame(window)
    difficulty_frame.pack(pady=10)

    Label(difficulty_frame, text="难度:").grid(row=0, column=0, sticky=W, padx=5, pady=5)
    easy_radio = Radiobutton(difficulty_frame, text="简单", variable=difficulty_var, value="简单")
    easy_radio.grid(row=0, column=1, padx=5, pady=5)
    medium_radio = Radiobutton(difficulty_frame, text="普通", variable=difficulty_var, value="普通")
    medium_radio.grid(row=0, column=2, padx=5, pady=5)
    hard_radio = Radiobutton(difficulty_frame, text="困难", variable=difficulty_var, value="困难")
    hard_radio.grid(row=0, column=3, padx=5, pady=5)

    # 开始游戏按钮
    def start_game():
        try:
            global x, y
            x = int(height_var.get())
            y = int(width_var.get())
            difficulty = difficulty_var.get()

            # 根据难度设置超时时间
            timeout = 30  # 默认普通难度
            if difficulty == "简单":
                timeout = 30
            elif difficulty == "困难":
                timeout = 30

            window.destroy()

            # 启动主游戏窗口
            root = tk.Tk()
            root.title('Maze-迷宫小游戏 v1.0')
            app = Application(master=root, width=x, height=y, bg_path=bg_image_path, difficulty=difficulty)
            app.mainloop()
        except ValueError:
            tk.messagebox.showerror("错误", "请输入有效的数字!")

    start_button = Button(window, text="点击或按Enter键开始", width=20, height=2, command=start_game)
    start_button.pack(pady=20)

    # 绑定Enter键到start_game函数
    window.bind("<Return>", lambda event: start_game())

    window.mainloop()


# 程序入口
if __name__ == "__main__":
    show_startup_window()
