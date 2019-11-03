import tkinter as tk
from item import TopFuntion, Tree

root = tk.Tk()
root.title('妇产科门诊绩效分配小工具')
root.resizable(0, 0)

rb_v = tk.StringVar()
f0 = tk.Frame(root, height=80, width=600)
f1 = tk.Frame(root, height=400, width=600)
f0_1 = tk.Frame(root, height=5, width=600, bg='aqua')
f0.grid(row=0, column=0)
f0_1.grid(row=1, column=0)
f1.grid(row=2, column=0)

tree = Tree(f1)
tree.create()

item_0 = TopFuntion(f0, tree.tree)
item_0.create_title()




if __name__ == '__main__':
    root.mainloop()
