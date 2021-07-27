from tkinter import Tk, Menu
from tkinter.ttk import Combobox, Treeview, Notebook, Frame, Entry, Label, Button, Style, Separator, Scrollbar
from tkinter.messagebox import showinfo, askyesno
from tkinter.filedialog import asksaveasfilename


def init_gui():
    def init_main_window():
        def init_style():
            def fixed_map(option):
                return [elm for elm in style.map("Treeview", query_opt=option) if elm[:2] != ("!disabled", "!selected")]
            style = Style()
            style.configure("BW.TFrame", foreground="black", background="white")
            style.configure("BW.TNotebook", foreground="black", background="white")
            style.configure("BW.TLabel", foreground="black", background="white")
            style.map("Treeview", foreground=fixed_map("foreground"), background=fixed_map("background"))

        window = Tk()
        init_style()
        screenwidth = window.winfo_screenwidth()
        screenheight = window.winfo_screenheight()
        window.grid_columnconfigure(0, weight=1)
        window.grid_rowconfigure(0, weight=1)
        window.title('风口订单管理系统')
        # window.geometry(f'{int(screenwidth / 2)}x{int(screenheight / 2)}+{int(screenwidth / 4)}+{int(screenheight / 4)}')
        window.geometry(f'{int(screenwidth * 2 / 3)}x{int(screenheight * 2 / 3)}+{int(screenwidth / 6)}+{int(screenheight / 6)}')
        window.minsize(int(screenwidth / 3), int(screenheight / 3))
        return window

    def init_frame_main():
        frame = Frame(window_main, style='BW.TFrame')
        frame.grid_rowconfigure(0, weight=0)
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_rowconfigure(2, weight=0)
        frame.grid_columnconfigure(0, weight=0)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_columnconfigure(2, weight=0)
        sh1 = Separator(frame, orient='horizontal')
        sh2 = Separator(frame, orient='horizontal')
        sv2 = Separator(frame, orient='vertical')
        sv1 = Separator(frame, orient='vertical')
        sh1.grid(row=0, column=0, columnspan=3, sticky='we')
        sh2.grid(row=2, column=0, columnspan=3, sticky='we')
        sv1.grid(row=0, column=0, rowspan=3, sticky='ns')
        sv2.grid(row=0, column=2, rowspan=3, sticky='ns')
        frame.grid(row=0, column=0, sticky='nsew')
        return frame

    def init_notebook():
        def init_frame_overview():
            frame = Frame(tabs, style='BW.TFrame')
            return frame

        def init_frame_order():
            def init_table():
                def init_table_column():
                    _table.column('id', width=2, anchor='center')
                    _table.column('height', width=2, anchor='e')
                    _table.column('width', width=2, anchor='e')
                    _table.column('side', width=2, anchor='e')
                    _table.column('unit_price', width=2, anchor='e')
                    _table.column('price', width=2, anchor='e')
                    _table.column('date', width=2, anchor='center')
                    _table.column('area', width=2, anchor='center')
                    _table.column('phone_number', width=2, anchor='center')
                    _table.column('customer', width=2, anchor='center')
                    _table.column('remark', width=2, anchor='center')
                    _table.heading('id', text='订单号')
                    _table.heading('height', text='长度')
                    _table.heading('width', text='宽度')
                    _table.heading('side', text='边宽')
                    _table.heading('unit_price', text='单位价格')
                    _table.heading('price', text='价格')
                    _table.heading('date', text='日期')
                    _table.heading('area', text='地区')
                    _table.heading('phone_number', text='联系电话')
                    _table.heading('customer', text='联系人')
                    _table.heading('remark', text='备注')

                    for i in range(100):
                        _table.insert('', 'end', text=i + 1, values=list(range(i, i+10)), tags='white' if i % 2 else 'gray')
                    _table.tag_configure('gray', background='light gray')

                _frame = Frame(frame, style='BW.TFrame')
                _frame.grid_rowconfigure(0, weight=1)
                _frame.grid_columnconfigure(0, weight=1)
                _frame.grid_columnconfigure(1, weight=0)
                _frame.grid(row=0, column=0, columnspan=9, sticky='nsew')
                _table = Treeview(_frame, show='headings')
                scrollbar = Scrollbar(_frame, orient='vertical', command=_table.yview)
                _table.configure(yscrollcommand=scrollbar.set)
                _table['columns'] = ('id', 'height', 'width', 'side', 'unit_price', 'price', 'date', 'area', 'phone_number', 'customer', 'remark')
                init_table_column()
                _table.grid(row=0, column=0, sticky='nsew')
                scrollbar.grid(row=0, column=1, sticky='ns')
                return _table

            frame = Frame(tabs, style='BW.TFrame')
            frame.grid_rowconfigure(0, weight=8)
            frame.grid_rowconfigure(1, weight=0)
            frame.grid_rowconfigure(2, weight=0)
            frame.grid_columnconfigure(0, weight=1)
            frame.grid_columnconfigure(1, weight=0)
            frame.grid_columnconfigure(2, weight=0)
            frame.grid_columnconfigure(3, weight=0)
            frame.grid_columnconfigure(4, weight=100)
            frame.grid_columnconfigure(5, weight=0)
            frame.grid_columnconfigure(6, weight=0)
            frame.grid_columnconfigure(7, weight=0)
            frame.grid_columnconfigure(8, weight=1)
            table = init_table()
            sh = Separator(frame, orient='horizontal')
            sh.grid(row=1, column=0, columnspan=9, sticky='we')
            button_pageup = Button(frame, text='上一页', takefocus=0)
            button_pagedown = Button(frame, text='下一页', takefocus=0)
            button_new = Button(frame, text='新建', takefocus=0)
            button_modification = Button(frame, text='编辑', takefocus=0)
            button_display = Button(frame, text='显示', takefocus=0)
            label_page = Label(frame, text='第1页（共1页）', style='BW.TLabel')
            button_pageup.grid(row=2, column=1, sticky='nsew')
            button_pagedown.grid(row=2, column=3, sticky='nsew')
            button_display.grid(row=2, column=5, sticky='nsew', padx=10)
            button_modification.grid(row=2, column=6, sticky='nsew', padx=10)
            button_new.grid(row=2, column=7, sticky='nsew', padx=10)
            label_page.grid(row=2, column=2, sticky='nsew', padx=50)
            return frame

        tabs = Notebook(frame_main, style='BW.TNotebook')
        overview_frame = init_frame_overview()
        tabs.add(overview_frame, text='总览')
        order_frame = init_frame_order()
        tabs.add(order_frame, text='订单')
        product_frame = Frame(tabs, style='BW.TFrame')
        tabs.add(product_frame, text='产品')
        statistics_frame = Frame(tabs, style='BW.TFrame')
        tabs.add(statistics_frame, text='统计')
        tabs.grid(row=1, column=1, sticky='nsew')
        return tabs

    def init_menubar():
        menu = Menu(window_main)
        menu_file = Menu(menu, tearoff=False)
        menu.add_cascade(label='文件', menu=menu_file)
        menu_file.add_command(label='导入')
        menu_file.add_command(label='导出')
        menu_file.add_separator()
        menu_file.add_command(label='设置')
        menu_file.add_separator()
        menu_file.add_command(label='退出')
        menu_edit = Menu(menu, tearoff=False)
        menu.add_cascade(label='编辑', menu=menu_edit)
        menu_edit.add_command(label='新建')
        menu_edit.add_command(label='编辑')
        window_main.config(menu=menu)
        return menu

    window_main = init_main_window()
    menubar = init_menubar()
    frame_main = init_frame_main()
    notebook = init_notebook()
    window_main.mainloop()


if __name__ == '__main__':
    init_gui()
