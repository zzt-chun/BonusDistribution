import tkinter as tk
from tkinter import ttk, messagebox


class TopFuntion(object):

    #def __init__(self, fb, name, score, duration, modulus, final_bonus=None):
    def __init__(self, fb, obj: ttk.Treeview):
        """
        :param fb: 画布
        :param name: 姓名
        :param score: 得分
        :param duration: 工时占比
        :param modulus: 奖金系数
        :param final_bonus: 最后奖金
        """
        self.fb = fb
        self.obj = obj
        self.name = tk.StringVar()
        self.score = tk.StringVar()
        self.duration = tk.StringVar()
        self.bonus = tk.StringVar()

    def create_title(self):
        tk.Label(self.fb, text="姓名:").grid(row=0, column=0, padx=3, pady=2)
        tk.Label(self.fb, text="得分:").grid(row=0, column=2, padx=3, pady=2)
        tk.Label(self.fb, text="工时占比（一个月填0.33）:").grid(row=0, column=4, padx=1, pady=2)
        tk.Entry(self.fb, textvariable=self.name, width=12).grid(row=0, column=1, padx=1, pady=2)
        #self.name.set("例如：张三")
        tk.Entry(self.fb, textvariable=self.score, width=8).grid(row=0, column=3, padx=1, pady=2)
        #elf.score.set("例如：60")
        tk.Entry(self.fb, textvariable=self.duration, width=8).grid(row=0, column=5, padx=3, pady=2)
        #self.duration.set("例如：一个月填0.33")
        tk.Button(self.fb, text='添加', command=lambda: self.add_item(), width=8)\
            .grid(row=0, column=6, padx=3, pady=2)
        tk.Button(self.fb, text='删除', command=lambda: self.delete_item(), width=8)\
            .grid(row=0, column=7, padx=3, pady=2)
        tk.Label(self.fb, text="奖金总额:").grid(row=1, column=3, padx=3, pady=2)
        tk.Entry(self.fb, text="如：张三", textvariable=self.bonus, width=12).grid(row=1, column=4, padx=3, pady=2)
        tk.Button(self.fb, text='分配奖金', command=lambda: self.compute(), width=8)\
            .grid(row=1, column=5, padx=5, pady=2)

    def add_item(self):
        name = self.name.get().strip()
        score = self.score.get().strip()
        duration = self.duration.get().strip()
        if name == "":
            messagebox.showerror("添加记录异常", "姓名不能为空\n例如：张三")
            return
        if not score.isdigit() or int(score) > 100 or  int(score) < 0:
            messagebox.showerror("添加记录异常", "得分不是整数或者 大于100 或者 小于0\n例如：60")
            return
        if not self.is_float(duration) or float(duration) > 1 or float(duration) < 0:
            messagebox.showerror("添加记录异常", "工时占比不能为空 或者大于1 或者小于0\n例如：一个月填0.33\n例如：二个月填0.66\n例如：三个月填1")
            return
        self.obj.insert('', "end", values=[name, int(score), float(duration)])
        self.name.set("")
        self.score.set("")
        self.duration.set("")
        messagebox.showinfo("添加成功", "成功添加一条记录 \n姓名      ：%s\n得分      ：%s\n工时占比：%s" % (name, score, duration))

    def is_float(self, item):
        try:
            float(item)
            return True
        except:
            return False

    def delete_item(self):
        smbol = self.obj.focus()
        try:
            values = self.obj.item(smbol)["values"]
            self.obj.delete(smbol)
            messagebox.showinfo("删除成功", "成功删除一条记录： %s" % values)
        except Exception:
            messagebox.showerror("删除异常", "请先选中需要删除的记录")

    def compute(self):
        #奖金总额
        bonus = self.bonus.get().strip()
        if bonus == '' or not bonus.isdigit() or int(bonus) <= 0:
            messagebox.showerror("计算异常", "奖金总额不能为空 或者不是整数 或者小于0\n例如：12000")
            return
        bonus = int(bonus)
        items = self.obj.get_children()
        if len(items) == 0:
            messagebox.showerror("计算异常", "没有添加记录不能计算奖金")
            return
        new_users = []
        for item in items:
            new_users.append(self.obj.item(item)["values"])
            self.obj.delete(item)
        sum_modulus = 0
        for user in new_users:
            if len(user) != 3:
                user.pop()
                user.pop()
            # print("user[1] = %s , user[2] = %s " % (user[1], user[2]))
            # print("type(user[1]) = %s , type(user[2] ) = %s " % (type(user[1]), type(user[2])))
            user.append(self.analyze_score(int(user[1]))*float(user[2]))
            #print(user)
            sum_modulus += user[3]
        if sum_modulus == 0:
            messagebox.showinfo("奖金分配失败", "没有一个人能到达领奖要求")
            return

        _index = [0, 0, 0, 0]
        real_bonus = 0
        for user in new_users:
            #print("user[3] = %s , sum_modulus = %s , bonus = %s " % (user[3], sum_modulus, bonus))
            #print("type(user[3]) = %s , type(sum_modulus) = %s , type(bonus) = %s " % (type(user[3]), type(sum_modulus), type(bonus)))
            user.append(int((user[3]/sum_modulus)*bonus))
            _index = _index if _index[3] > user[3] else user
            real_bonus += user[4]
        _index[4] += bonus - real_bonus
        for user in new_users:
            self.obj.insert('', 'end', values=user)
        if bonus > real_bonus:
            messagebox.showinfo("分配奖金成功", "分配奖金成功！\n由于小数点原因最终绩效最高分获得者%s多分了%s元" % (_index[0], bonus - real_bonus))

    def analyze_score(self, score: int):
        _sum = 0
        if score < 60:
            return _sum
        _sum += 6

        if 80 <= score:
            _sum += (score-80)*0.2

        if 60 <= score:
            _sum += ((score-60) if score < 80 else 20)*0.1

        return _sum





class Tree(object):

    def __init__(self, fb):
        self.fb = fb

    def create(self):

        f = tk.Frame(self.fb, width=400, height=400)

        f.pack(side=tk.LEFT)

        sb3 = tk.Scrollbar(f, orient=tk.VERTICAL)  # 竖向拉条
        sb3.pack(side=tk.RIGHT, fill=tk.BOTH)

        self.tree = ttk.Treeview(f, show='headings', yscrollcommand=sb3.set)  # 表格
        self.tree.pack(side=tk.TOP)

        sb3.config(command=self.tree.yview)

        # 读取excel内容
        self.tree['height'] = 12  # 设置展示的行数

        data = ["姓名", "得分", "工时占比", "奖金系数", "最终奖金(元)"]
        self.tree["columns"] = data

        for name in data:
            self.tree.column(name, width=10 * 8, anchor='center')  # 设置宽度
            self.tree.heading(name, text=name)  # 显示表头
