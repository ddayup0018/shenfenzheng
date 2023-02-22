
import tkinter as tk
from tkinter import messagebox
import random


class Sfz:
    def __init__(self,identity_card:str) -> None:
        self.identity_card_strs= identity_card
        self.ai_list = self.get_number()
        self.wi_list = self.get_jiaquan()

    # 获取身份证列表方法
    def get_number(self):
        Ai_list = []
        for i in iter(self.identity_card_strs):
            # 如果输入的身份证验证位为X,则转换为10
            if i == 'X':
                i = 10
            Ai_list.append(int(i))
        return Ai_list

    # 得到加权因子方法
    def get_jiaquan(self):
        # 计算加权位因子
        # W = 2的i-1次方 mod(11),i为右往左
        Wi_list = []
        for i in range(18):
            temp = (2**(i))%11
            Wi_list.append(temp)
        Wi_list.reverse()
        # print(Wi)
        return Wi_list

    # 得到求和列表
    def get_sum(self,index=17):
        temp_list = []
        for i in range(index):
            temp_list.append(self.wi_list[i]*self.ai_list[i])
        return temp_list

    # 检查身份证方法
    def check(self):
        if len(self.ai_list)==18:
            sum18_list = self.get_sum(18)
            sum18 = sum(sum18_list)
            # 求和后mod11结果为1则验证通过
            result = sum18%11
            if result == 1:
                print('验证成功')
                return True
            else:
                print('验证失败')
                return False
        else:
            print('验证的号码必须是18位!')
            return '验证的号码必须是18位!'

    # 创建方法
    def create(self):
        if len(self.ai_list) ==18:
            # 如果等于18位则先验证是否正确，如果不正确则去掉验证位生成正确的验证位
            result = self.check()
            if result == True:
                print('该号码验证通过,无须重新生成!')
                return '该号码验证通过,无须重新生成!'
            else:
                print('验证失败重新生成')
                # 验证失败则校验位无效,去除校验位
                self.ai_list = self.ai_list[:-1]
                # 调用生成身份证方法
                return self.success_num()

        if len(self.ai_list) <18:
            # 如果小于18位则先补齐至17位，再生成正确的验证位
            # 输入的号码位17位无需补齐
            if len(self.ai_list) == 17:
                print('17位')
                pass
            # 输入的号码小于17位则补齐
            if len(self.ai_list) <17:
                print('小于17位')
                list_length = 17 - len(self.ai_list)
                remain =self.random_length(list_length)
                for i in iter(str(remain)):
                    self.ai_list.append(int(i))

            # 调用生成身份证方法
            return self.success_num()

    # 生成身份证方法
    def success_num(self):
        # 通过前17位得到第18位校验码,校验公式
        sum17_list =  self.get_sum()
        sum17 = sum(sum17_list)
        code18 = (12-sum17%11)%11
        # 校验码如果为10则替换为X
        if code18 == 10:
            code18 = 'X'
        # 生成新的符合规则的身份证列表
        result_list = self.ai_list
        result_list.append(code18)
        # 列表中整形元素替换为字符串元素
        result_num_list = list(map(lambda x: str(x),result_list))
        # 列表转为字符串
        result_num = ''.join(result_num_list)
        print(f'符合校验规则的身份证号码生成成功:{result_num}')
        return f'符合校验规则的身份证号码生成成功:{result_num}'

    # 按位生成随机数补齐方法
    def random_length(self,mylength):
        start = 10**(mylength-1)
        end = (10**mylength) -1
        return random.randint(start,end)

def check_id():
    sfz = Sfz(check_var.get())
    msg = sfz.check()
    if msg == True:
        msg = '验证通过'
    elif msg == False:
        msg = '验证失败'
    messagebox.showinfo(title='提示框',message=msg)

def create_id():
    text1.delete(1.0,'end')
    sfz = Sfz(create_var.get())
    msg = sfz.create()
    # messagebox.showinfo(title='提示框',message=msg)
    text1.insert('insert',msg)
    

if __name__ == '__main__':

    root_window =tk.Tk()
    root_window.title('身份证验证器')
    root_window.geometry('320x200')

    check_var = tk.StringVar()
    tk.Label(root_window,text='验证身份证:').grid(row=0,column=0)
    tk.Entry(root_window,textvariable=check_var).grid(row=0,column=1)
    tk.Button(root_window,command=check_id,text='点击验证').grid(row=0,column=2)

    create_var = tk.StringVar()
    tk.Label(root_window,text='生成身份证:').grid(row=1,column=0)
    tk.Entry(root_window,textvariable=create_var).grid(row=1,column=1)
    tk.Button(root_window,command=create_id,text='点击生成').grid(row=1,column=2)
    text1 = tk.Text(root_window,width=40,height=5)
    text1.grid(row=2,columnspan=3)
    root_window.mainloop()


