from sqlite3 import connect, OperationalError
from tkinter import Tk, Button, Frame, ttk, Label, Entry
# from tkinter import Tk, ttk
# from tkinter.ttk import Button, Frame, Label, Entry
from tkinter.messagebox import askyesno, showinfo


class Data:
    def __init__(self):
        self.__conn = connect('data.db')
        try:
            self.__init_table()
        except OperationalError:
            pass
        # self.insert('120, 140, 30, 50, 60, "2021-3-24", "大田", 15897969897, "哦哦哦", ""')

    def __init_table(self):
        # table = self.__conn.execute('PRAGMA TABLE_INFO(MAIN)').fetchall()
        # if len(table) != 11:
        #     self.__conn.execute('DROP TABLE MAIN')
        self.__conn.execute('''CREATE TABLE MAIN(
                             ID INT PRIMARY KEY    NOT NULL,
                             HEIGHT         DOUBLE NOT NULL,
                             WIDTH          DOUBLE NOT NULL,
                             SIDE           DOUBLE NOT NULL,
                             UNIT_PRICE     DOUBLE NOT NULL,
                             PRICE          DOUBLE NOT NULL,
                             DATE           CHAR   NOT NULL,
                             AREA           CHAR   NOT NULL,
                             PHONE_NUMBER   CHAR   NOT NULL,
                             CUSTOMER       CHAR   NOT NULL,
                             REMARK         CHAR            );''')

    def insert(self, values, _id=None):
        """
        :param _id:
        :param values: 'height, width, side, unite_price, price, "date", "area", phone_number, "customer", "remark"'
        """
        table = self.__conn.execute('SELECT ID FROM MAIN').fetchall()
        if _id is None:
            _id = max(table, key=lambda x: x[0])[0] + 1 if table else 0
        else:
            self.delete(_id)
        self.__conn.execute(f'INSERT INTO MAIN VALUES ({_id}, {values});')
        self.__conn.commit()

    def delete(self, _id):
        self.__conn.execute(f'DELETE FROM MAIN WHERE ID = {_id}')
        self.__conn.commit()

    def select(self, page):
        table = self.__conn.execute(f'SELECT * FROM MAIN ORDER BY ID DESC LIMIT 100 OFFSET {100 * page}').fetchall()
        return table


class GUI:
    def __init__(self):
        self.__data = Data()
        main = Tk()
        screenwidth = main.winfo_screenwidth()
        screenheight = main.winfo_screenheight()
        main.grid_rowconfigure(0, weight=8)
        main.grid_rowconfigure(1, weight=1)
        main.grid_columnconfigure(0, weight=5)
        main.grid_columnconfigure(1, weight=1)
        main.title('风口订单管理系统')
        main.withdraw()
        main.geometry(f'{int(screenwidth / 2)}x{int(screenheight / 2)}+{int(screenwidth / 4)}+{int(screenheight / 4)}')
        bottom_frame = Frame(main)
        bottom_frame.grid_rowconfigure(0, weight=1)
        bottom_frame.grid_columnconfigure(0, weight=1)
        bottom_frame.grid_columnconfigure(1, weight=5)
        bottom_frame.grid_columnconfigure(2, weight=1)
        self.__page_label = page_label = Label(bottom_frame, text='/')
        statistics = Button(bottom_frame, text='统计', height=1)
        filtrate = Button(bottom_frame, text='筛选', height=1)
        page_label.grid(row=0, column=1, sticky='nsew')
        statistics.grid(row=0, column=0, sticky='nsew', padx=20, pady=10)
        filtrate.grid(row=0, column=2, sticky='nsew', padx=20, pady=10)
        bottom_frame.grid(row=1, column=0, sticky='nsew')
        input_frame = Frame(main)
        for i in range(20):
            input_frame.grid_rowconfigure(i, weight=1)
        input_frame.grid_rowconfigure(20, weight=10)
        input_frame.grid_columnconfigure(0, weight=1)
        height_label = Label(input_frame, text='长度', width=1)
        width_label = Label(input_frame, text='宽度', width=1)
        side_label = Label(input_frame, text='边宽', width=1)
        unit_price_label = Label(input_frame, text='单位价格', width=1)
        price_label = Label(input_frame, text='价格', width=1)
        date_label = Label(input_frame, text='日期', width=1)
        area_label = Label(input_frame, text='地区', width=1)
        phone_number_label = Label(input_frame, text='联系电话', width=1)
        customer_label = Label(input_frame, text='联系人', width=1)
        remark_label = Label(input_frame, text='备注', width=1)
        height = Entry(input_frame, state='readonly', width=1)
        width = Entry(input_frame, state='readonly', width=1)
        side = Entry(input_frame, state='readonly', width=1)
        unit_price = Entry(input_frame, state='readonly', width=1)
        price = Entry(input_frame, state='readonly', width=1)
        date_frame = Frame(input_frame)
        date_frame.grid_rowconfigure(0, weight=1)
        date_frame.grid_columnconfigure(0, weight=1)
        date_frame.grid_columnconfigure(1, weight=1)
        date_frame.grid_columnconfigure(2, weight=1)
        year = ttk.Combobox(date_frame, state='disabled', width=1)
        year['values'] = list(range(2021, 2032))
        month = ttk.Combobox(date_frame, state='disabled', width=1)
        month['values'] = list(range(1, 13))
        day = ttk.Combobox(date_frame, state='disabled', width=1)
        year.grid(row=0, column=0, sticky='ew')
        month.grid(row=0, column=1, sticky='ew')
        day.grid(row=0, column=2, sticky='ew')
        area = ttk.Combobox(input_frame, state='disabled', width=1)
        area['values'] = ['小陶', '大田', '洪田']
        phone_number = Entry(input_frame, state='readonly', width=1)
        customer = Entry(input_frame, state='readonly', width=1)
        remark = Entry(input_frame, state='readonly', width=1)
        self.__input = (height, width, side, unit_price, price, (year, month, day), area, phone_number, customer, remark)
        height_label.grid(column=0, row=0, sticky='ew')
        height.grid(column=0, row=1, sticky='ew', padx=50)
        width_label.grid(column=0, row=2, sticky='ew')
        width.grid(column=0, row=3, sticky='ew', padx=50)
        side_label.grid(column=0, row=4, sticky='ew')
        side.grid(column=0, row=5, sticky='ew', padx=50)
        unit_price_label.grid(column=0, row=6, sticky='ew')
        unit_price.grid(column=0, row=7, sticky='ew', padx=50)
        price_label.grid(column=0, row=8, sticky='ew')
        price.grid(column=0, row=9, sticky='ew', padx=50)
        date_label.grid(column=0, row=10, sticky='ew')
        date_frame.grid(column=0, row=11, sticky='ew', padx=50)
        area_label.grid(column=0, row=12, sticky='ew')
        area.grid(column=0, row=13, sticky='ew', padx=50)
        phone_number_label.grid(column=0, row=14, sticky='ew')
        phone_number.grid(column=0, row=15, sticky='ew', padx=50)
        customer_label.grid(column=0, row=16, sticky='ew')
        customer.grid(column=0, row=17, sticky='ew', padx=50)
        remark_label.grid(column=0, row=18, sticky='ew')
        remark.grid(column=0, row=19, sticky='ew', padx=50)
        button_frame = Frame(input_frame, width=1)
        button_frame.grid_rowconfigure(0, weight=1)
        button_frame.grid_rowconfigure(1, weight=1)
        button_frame.grid_rowconfigure(2, weight=1)
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        button_frame.grid_columnconfigure(2, weight=1)
        self.__modification = modification = Button(button_frame, text='修改', command=self.__modification_command, state='disabled', width=1)
        self.__save = save = Button(button_frame, text='保存', command=self.__save_command, width=1)
        self.__insert = insert = Button(button_frame, text='新建', command=self.__insert_command, width=1)
        self.__cancel = cancel = Button(button_frame, text='取消', command=self.__cancel_command, width=1)
        self.__delete = delete = Button(button_frame, text='删除', command=self.__delete_command, state='disabled', width=1)
        self.__confirm = confirm = Button(button_frame, text='确定', command=self.__confirm_command, width=1)
        modification.grid(row=1, column=1, sticky='nsew', padx=2, pady=25)
        insert.grid(row=1, column=2, sticky='nsew', padx=20, pady=25)
        save.grid(row=1, column=0, sticky='nsew', padx=20, pady=25)
        save.grid_remove()
        cancel.grid(row=1, column=2, sticky='nsew', padx=20, pady=25)
        cancel.grid_remove()
        delete.grid(row=1, column=0, sticky='nsew', padx=20, pady=25)
        confirm.grid(row=1, column=0, sticky='nsew', padx=20, pady=25)
        confirm.grid_remove()
        button_frame.grid(row=20, column=0, sticky='nsew')
        input_frame.grid(row=0, column=1, sticky='nsew')
        table_frame = Frame(main)
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        self.__table = table = ttk.Treeview(table_frame, selectmode='extended')
        table.bind('<<TreeviewSelect>>', self.__select_item)
        table['columns'] = ('id', 'height', 'width', 'side', 'unit_price', 'price', 'date', 'area', 'phone_number', 'customer', 'remark')
        table['displaycolumns'] = ('height', 'width', 'side', 'unit_price', 'price', 'date', 'area', 'phone_number', 'customer', 'remark')
        table_frame.grid(row=0, column=0, sticky='nsew')
        table.column('#0', width=1)
        table.column('height', width=2, anchor='e')
        table.column('width', width=2, anchor='e')
        table.column('side', width=2, anchor='e')
        table.column('unit_price', width=2, anchor='e')
        table.column('price', width=2, anchor='e')
        table.column('date', width=2, anchor='center')
        table.column('area', width=2, anchor='center')
        table.column('phone_number', width=2, anchor='center')
        table.column('customer', width=2, anchor='center')
        table.column('remark', width=2, anchor='center')
        table.heading('height', text='长度')
        table.heading('width', text='宽度')
        table.heading('side', text='边宽')
        table.heading('unit_price', text='单位价格')
        table.heading('price', text='价格')
        table.heading('date', text='日期')
        table.heading('area', text='地区')
        table.heading('phone_number', text='联系电话')
        table.heading('customer', text='联系人')
        table.heading('remark', text='备注')
        self.__load_table(page=0)
        table.grid(row=0, column=0, sticky='nsew')
        main.deiconify()
        main.mainloop()

    def __load_table(self, page):
        table = self.__data.select(page=page)
        for item in self.__table.get_children():
            self.__table.delete(item)
        for i in range(len(table) - 1, -1, -1):
            self.__table.insert('', 0, text=i + 1, values=table[i])

    def __select_item(self, event):
        items = self.__table.selection()
        if len(items) == 0:
            self.__modification['state'] = 'disabled'
            self.__delete['state'] = 'disabled'
        elif len(items) == 1:
            self.__modification['state'] = 'normal'
            self.__delete['state'] = 'normal'
        else:
            self.__modification['state'] = 'disabled'
            self.__delete['state'] = 'normal'
        item = self.__table.item(items[0])['values'] if len(items) == 1 else None
        for i in (0, 1, 2, 3, 4, 6, 7, 8, 9):
            state = self.__input[i]['state']
            self.__input[i]['state'] = 'normal'
            self.__input[i].delete(0, 'end')
            self.__input[i].insert(0, item[i + 1]) if item is not None else 0
            self.__input[i]['state'] = state
        date = item[6].split('-') if item is not None else 0
        for i in range(3):
            state = self.__input[5][i]['state']
            self.__input[5][i]['state'] = 'normal'
            self.__input[5][i].delete(0, 'end')
            self.__input[5][i].insert(0, date[i]) if item is not None else 0
            self.__input[5][i]['state'] = state

    def __modification_command(self):
        self.__modification.grid_remove()
        self.__insert.grid_remove()
        self.__delete.grid_remove()
        self.__cancel.grid()
        self.__save.grid()
        self.__table['selectmode'] = 'none'
        for i in (0, 1, 2, 3, 4, 6, 7, 8, 9):
            self.__input[i]['state'] = 'normal'
        for i in self.__input[5]:
            i['state'] = 'normal'

    def __insert_command(self):
        self.__modification.grid_remove()
        self.__insert.grid_remove()
        self.__delete.grid_remove()
        self.__cancel.grid()
        self.__confirm.grid()
        for focus in self.__table.selection():
            self.__table.selection_remove(focus)
        self.__table['selectmode'] = 'none'
        for i in (0, 1, 2, 3, 4, 6, 7, 8, 9):
            self.__input[i]['state'] = 'normal'
            self.__input[i].delete(0, 'end')
        for i in self.__input[5]:
            i['state'] = 'normal'
            i.delete(0, 'end')

    def __save_command(self):
        flag = False
        string = ''
        for i in range(5):
            if not self.__input[i].get():
                flag = True
            string += self.__input[i].get()
            string += ', '
        substr = '"'
        for i in range(3):
            if not self.__input[5][i].get():
                flag = True
            substr += self.__input[5][i].get()
            substr += '-' if i != 2 else '", '
        string += substr
        for i in range(6, 10):
            if not self.__input[i].get() and i != 9:
                flag = True
            string += '"'
            string += self.__input[i].get()
            string += '", ' if i != 9 else '"'
        if flag:
            showinfo('提示', '请输入正确的数值。')
        else:
            self.__modification.grid()
            self.__insert.grid()
            self.__delete.grid()
            self.__cancel.grid_remove()
            self.__save.grid_remove()
            self.__table['selectmode'] = 'extended'
            for i in (0, 1, 2, 3, 4, 7, 8, 9):
                self.__input[i]['state'] = 'readonly'
            for i in self.__input[5]:
                i['state'] = 'disabled'
            self.__input[6]['state'] = 'disabled'
            _id = self.__table.item(self.__table.selection()[0])['values'][0]
            self.__data.insert(string, _id=_id)
            self.__load_table(page=0)
            for item in self.__table.get_children():
                if self.__table.item(item)['values'][0] == _id:
                    self.__table.selection_add(item)
                    break

    def __delete_command(self):
        items = self.__table.selection()
        if len(items) == 1:
            str1 = '删除项目'
            str2 = '确实要永久删除这个项目吗？'
        else:
            str1 = '删除多个项目'
            str2 = f'确实要永久删除这{len(items)}项吗？'
        if askyesno(str1, str2):
            for item in items:
                self.__data.delete(self.__table.item(item)['values'][0])
            for i in (0, 1, 2, 3, 4, 6, 7, 8, 9):
                self.__input[i]['state'] = 'normal'
                self.__input[i].delete(0, 'end')
                self.__input[i]['state'] = 'readonly' if i != 6 else 'disabled'
            for i in range(3):
                self.__input[5][i]['state'] = 'normal'
                self.__input[5][i].delete(0, 'end')
                self.__input[5][i]['state'] = 'disabled'
            self.__load_table(page=0)
        self.__delete['state'] = 'disabled'
        self.__modification['state'] = 'disabled'

    def __cancel_command(self):
        self.__modification.grid()
        self.__insert.grid()
        self.__delete.grid()
        self.__cancel.grid_remove()
        self.__save.grid_remove()
        self.__confirm.grid_remove()
        self.__table['selectmode'] = 'extended'
        items = self.__table.selection()
        item = self.__table.item(items[0])['values'] if len(items) == 1 else None
        for i in (0, 1, 2, 3, 4, 6, 7, 8, 9):
            self.__input[i].delete(0, 'end')
            self.__input[i].insert(0, item[i + 1]) if item is not None else 0
            self.__input[i]['state'] = 'readonly' if i != 6 else 'disabled'
        for i in range(3):
            self.__input[5][i].delete(0, 'end')
            self.__input[5][i].insert(0, item[i + 1]) if item is not None else 0
            self.__input[5][i]['state'] = 'disabled'

    def __confirm_command(self):
        flag = False
        string = ''
        for i in range(5):
            if not self.__input[i].get():
                flag = True
            string += self.__input[i].get()
            string += ', '
        substr = '"'
        for i in range(3):
            if not self.__input[5][i].get():
                flag = True
            substr += self.__input[5][i].get()
            substr += '-' if i != 2 else '", '
        string += substr
        for i in range(6, 10):
            if not self.__input[i].get() and i != 9:
                flag = True
            string += '"'
            string += self.__input[i].get()
            string += '", ' if i != 9 else '"'
        if flag:
            showinfo('提示', '请输入正确的数值。')
        else:
            self.__modification.grid()
            self.__insert.grid()
            self.__delete.grid()
            self.__cancel.grid_remove()
            self.__confirm.grid_remove()
            self.__table['selectmode'] = 'extended'
            for i in (0, 1, 2, 3, 4, 7, 8, 9):
                self.__input[i]['state'] = 'readonly'
            for i in self.__input[5]:
                i['state'] = 'disabled'
            self.__input[6]['state'] = 'disabled'
            self.__data.insert(string)
            self.__load_table(page=0)
            self.__table.selection_add(self.__table.get_children()[0])


if __name__ == '__main__':
    # data = Data()
    GUI()
