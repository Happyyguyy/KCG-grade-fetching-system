from tkinter import *
from tkinter import messagebox
import sqlite3
import time

# init sqlite3 connection
db = sqlite3.connect("db0.db")
cur = db.cursor()

root = Tk()


class Main:
    def __init__(self, master=None):
        self.config = None
        # new_screen = entryWindow(id)
        self.master = master
        tableFrame = Frame(master, bg="grey", width=500)
        optionFrame = Frame(master, relief=SUNKEN, bd=1, padx=5, pady=2)
        buttonFrame = Frame(master, bd=1)

        tableFrame.grid(row=0, column=1, rowspan=2, stick=NSEW)
        optionFrame.grid(row=0, column=0, stick=NSEW)
        buttonFrame.grid(row=1, column=0, stick=NSEW)

        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        # root.grid_columnconfigure(1)

        # ************ Left Frame ************

        self.data_canvas = Canvas(tableFrame, width=600)
        self.data_canvas.grid(stick=NSEW)
        tableFrame.rowconfigure(0, weight=1)
        tableFrame.columnconfigure(0, weight=1)

        self.data_table = Frame(self.data_canvas, name="data_table")

        # Gets data
        self.print_table(self.config)

        self.data_canvas.create_window(
            (4, 4), window=self.data_table, anchor="nw")

        # Set scrollregion with new data
        self.data_table.update_idletasks()
        self.data_canvas.config(scrollregion=self.data_canvas.bbox(ALL))

        # Create scrollbars and self.config them with self.data_canvas
        vscrollbar = Scrollbar(tableFrame, orient=VERTICAL)
        vscrollbar.grid(row=0, column=1, stick=NS+E)
        vscrollbar.config(command=self.data_canvas.yview)

        hscrollbar = Scrollbar(tableFrame, orient=HORIZONTAL)
        hscrollbar.grid(row=1, stick=EW+S)
        hscrollbar.config(command=self.data_canvas.xview)

        self.data_canvas.config(
            yscrollcommand=vscrollbar.set, xscrollcommand=hscrollbar.set)

        # ************ Option frame ***********

        self.searchbar = Entry(optionFrame)
        self.searchbar.insert(0, "Search")
        self.searchbar.bind(
            "<FocusIn>", lambda e: self.searchbar.delete(0, END))

        search_btn = Button(optionFrame, text="Search", command=self.search)

        option_label = Label(optionFrame, text="Options")

        self.id_onoff = BooleanVar()
        self.id = Checkbutton(optionFrame, text="ID", variable=self.id_onoff)

        self.district_onoff = BooleanVar()
        self.district = Checkbutton(
            optionFrame, text="District", variable=self.district_onoff)

        self.name_onoff = BooleanVar()
        self.name = Checkbutton(optionFrame, text="Name",
                                variable=self.name_onoff)

        self.phone_onoff = BooleanVar()
        self.phone = Checkbutton(
            optionFrame, text="Phone", variable=self.phone_onoff)

        self.email_onoff = BooleanVar()
        self.email = Checkbutton(
            optionFrame, text="Email", variable=self.email_onoff)

        self.leg_page_onoff = BooleanVar()
        self.leg_page = Checkbutton(
            optionFrame, text="Webpage", variable=self.leg_page_onoff)

        party_label = Label(optionFrame, text="Party")

        self.dem_onoff = BooleanVar()
        self.dem_check = Checkbutton(
            optionFrame, text="Democrat", variable=self.dem_onoff)
        self.dem_check.select()

        self.rep_onoff = BooleanVar()
        self.rep_check = Checkbutton(
            optionFrame, text="Republican", variable=self.rep_onoff)
        self.rep_check.select()

        self.ind_onoff = BooleanVar()
        self.ind_check = Checkbutton(
            optionFrame, text="Independent", variable=self.ind_onoff)
        self.ind_check.select()


        title_label = Label(optionFrame, text="House")

        self.sen_onoff = BooleanVar()
        self.sen_check = Checkbutton(
            optionFrame, text="Senate", variable=self.sen_onoff)
        self.sen_check.select()

        self.repr_onoff = BooleanVar()
        self.repr_check = Checkbutton(
            optionFrame, text="Representatives", variable=self.repr_onoff)
        self.repr_check.select()


        refresh_btn = Button(optionFrame, text="Refresh List",
                             command=lambda: print("refresh"))

        self.searchbar.grid()
        search_btn.grid(row=0, column=1)

        option_label.grid(row=1, columnspan=2)

        self.id.grid(row=2, stick=W)
        self.district.grid(row=3, stick=W)
        self.email.grid(row=4, stick=W)
        party_label.grid(row=5, stick=N)
        self.dem_check.grid(row=6, stick=W)
        self.rep_check.grid(row=7, stick=W)
        self.ind_check.grid(row=8, stick=W)

        self.name.grid(row=2, column=1, stick=W)
        self.phone.grid(row=3, column=1, stick=W)
        self.leg_page.grid(row=4, column=1, stick=W)
        title_label.grid(row=5, column=1, stick=N)
        self.sen_check.grid(row=6, column=1, stick=W)
        self.repr_check.grid(row=7, column=1, stick=W)

        refresh_btn.grid(row=9, columnspan=2)

        # ************** Button Frame ******************
        button_dict = {
            "new_entry": self.new_entry,
            "show_archive": self.show_archive,
            "create_all": self.create_all,
            "create_selected": self.create_selected,
            "update_legs": self.update_legs,
            "update_grades": self.update_grades
        }
        col = 0
        for name, func in button_dict.items():
            btn = Button(buttonFrame, text=name.replace(
                "_", " ").title(), command=func)
            btn.pack(side=TOP, fill=X, padx=2, pady=1)

            if col == 0:
                col = 1
            elif col == 1:
                col = 0
        # bind to refresh list
        root.bind("<FocusIn>", lambda e,
                  config=self.config: self.print_table(config))

    def search(self):
        # TODO: Search
        print(self.searchbar.get())

    def get_headings(self):
        # TODO: filtered headings
        config = []


        return config

    def print_table(self, config=None):
        for widget in self.data_table.winfo_children():
            widget.destroy()

        if not config:
            config = ('party', 'name', 'district', 'rhetoric',
                      'donations', 'voting', 'email')
        cur.execute(
            f"SELECT {','.join(config)},legislators.id FROM legislators INNER JOIN grades ON legislators.id = grades.id")
        row_index = 0


        for i in range(len(config)):
            lbl = Label(self.data_table, text=config[i].title())
            lbl.grid(row=0, column=i+1)
        # headings.grid(row=row_index)
        row_index += 1
        self.table_buttons = Frame(self.data_table)

        btn_list = []
        num_rows = 0
        for row in cur.fetchall():
            num_rows += 1
            id = row[-1]
            edit_btn = Button(self.table_buttons, text="Edit",
                              command=lambda id=id: self.edit_screen(edit_btn, id))
            edit_btn.grid(row=row_index-1, column=0)

            sel = BooleanVar()
            row_select = Checkbutton(self.table_buttons)
            row_select.var = sel
            btn_list.append(row_select)
            row_select.grid(row=row_index-1, column=1)

            for i in range(len(row)-1):
                lbl = Label(self.data_table, text=row[i], bd=1)
                lbl.grid(row=row_index, column=i+1)
            # btn_list.append(edit_btn)
            row_index += 1

        self.table_buttons.grid(row=1, rowspan=num_rows)

        print(btn_list)

    def edit_screen(self, master=None, id=None):
        edit_screen = entryWindow(master, id)

    def new_entry(self):
        new_screen = entryWindow()

    def show_archive(self):
        # TODO: show_archive
        pass

    def create_all(self):
        # TODO: create_all
        pass

    def create_selected(self):
        # TODO: create_selected
        pass

    def update_legs(self):
        # TODO: update_legs
        pass

    def update_grades(self):
        # TODO: update_grades
        pass


class entryWindow:
    def __init__(self, master=None, id=None):
        self.id = id
        self.master = master
        if id:
            self.data = self.get_data(self.id)
            self.entry_edit()
        else:
            self.data = {}
            self.entry_new()

    def entry_new(self):

        editing = Toplevel(self.master, padx=5, pady=5)
        editing.resizable(width=False, height=False)
        editing.title("New Data")

        id_label = Label(editing, text="ID:")
        id_label.grid(row=0, column=0, stick=E)

        self.id = Entry(editing, bd=1, state=DISABLED, text="")
        # id.insert(0, "")
        # id.config(state="readonly")
        self.id.grid(row=0, column=1, stick=NSEW)

        assembly_label = Label(editing, text="Assembly:")
        assembly_label.grid(row=1, column=0, stick=E)

        self.assembly = Entry(editing)
        self.assembly.insert(0, "")
        self.assembly.grid(row=1, column=1)

        title_label = Label(editing, text="Title:")
        title_label.grid(row=2, column=0, stick=E)

        self.title = Entry(editing)
        self.title.insert(0, "")
        self.title.grid(row=2, column=1)

        first_label = Label(editing, text="First:")
        first_label.grid(row=3, column=0, stick=E)

        self.first = Entry(editing)
        self.first.insert(0, "")
        self.first.grid(row=3, column=1)

        last_label = Label(editing, text="Last:")
        last_label.grid(row=4, column=0, stick=E)

        self.last = Entry(editing)
        self.last.insert(0, "")
        self.last.grid(row=4, column=1)

        district_label = Label(editing, text="District:")
        district_label.grid(row=5, column=0, stick=E)

        self.district = Entry(editing)
        self.district.insert(0, "")
        self.district.grid(row=5, column=1)

        phone_num_label = Label(editing, text="Phone #:")
        phone_num_label.grid(row=6, column=0, stick=E)

        self.phone_num = Entry(editing)
        self.phone_num.insert(0, "")
        self.phone_num.grid(row=6, column=1)

        email_label = Label(editing, text="Email:")
        email_label.grid(row=7, column=0, stick=E)

        self.email = Entry(editing)
        self.email.insert(0, "")
        self.email.grid(row=7, column=1)

        leg_page_label = Label(editing, text="Webpage:")
        leg_page_label.grid(row=8, column=0, stick=E)

        self.leg_page = Entry(editing)
        self.leg_page.insert(0, "")
        self.leg_page.grid(row=8, column=1)

        img_link_label = Label(editing, text="Img Link:")
        img_link_label.grid(row=9, column=0, stick=E)

        self.img_link = Entry(editing)
        self.img_link.insert(0, "")
        self.img_link.grid(row=9, column=1)

        voting_label = Label(editing, text="Voting:")
        voting_label.grid(row=0, column=3, stick=E)

        self.voting = Entry(editing, width=10)
        self.voting.insert(0, "")
        self.voting.grid(row=0, column=4)

        rhetoric_label = Label(editing, text="Rhetoric:")
        rhetoric_label.grid(row=1, column=3, stick=E)

        self.rhetoric = Entry(editing, width=10)
        self.rhetoric.insert(0, "")
        self.rhetoric.grid(row=1, column=4)

        donations_label = Label(editing, text="Donations:")
        donations_label.grid(row=2, column=3, sticky=E)

        self.donations = Entry(editing, width=10)
        self.donations.insert(0, "")
        self.donations.grid(row=2, column=4)

        last_updated_label = Label(editing, text="Last Updated:")
        last_updated_label.grid(row=3, column=3, stick=E)

        self.last_updated = Entry(editing, width=10)
        self.last_updated.insert(0, "")
        self.last_updated.config(state="readonly")
        self.last_updated.grid(row=3, column=4)

        reset_btn = Button(editing, text="Reset",
                           command=lambda: print("Reset"))
        reset_btn.grid(row=4, column=3, columnspan=2,
                       rowspan=2, stick=NSEW, padx=5, pady=2)

        update_btn = Button(editing, text="Update",
                            command=lambda: print("Update"), bg="lightblue")
        update_btn.grid(row=6, column=3, columnspan=2,
                        rowspan=2, stick=NSEW, padx=5, pady=2)

        delete_btn = Button(editing, text="Cancel",
                            command=editing.destroy, bg="red")
        delete_btn.grid(row=8, column=3, columnspan=2,
                        rowspan=2, stick=NSEW, padx=5, pady=2)

    def entry_edit(self):
        editing = Toplevel(self.master, padx=5, pady=5)
        editing.resizable(width=False, height=False)
        editing.title("Edit Data")

        id_label = Label(editing, text="ID:")
        id_label.grid(row=0, column=0, stick=E)

        self.id = Label(editing, bd=1, relief=SUNKEN,
                        text=self.data["id"], anchor=W)
        # id.insert(0, self.data["id"])
        # id.config(state="readonly")
        self.id.grid(row=0, column=1, stick=NSEW)

        assembly_label = Label(editing, text="Assembly:")
        assembly_label.grid(row=1, column=0, stick=E)

        self.assembly = Entry(editing)
        self.assembly.insert(0, self.data["assembly"])
        self.assembly.grid(row=1, column=1)

        title_label = Label(editing, text="Title:")
        title_label.grid(row=2, column=0, stick=E)

        self.title = Entry(editing)
        self.title.insert(0, self.data["title"])
        self.title.grid(row=2, column=1)

        first_label = Label(editing, text="First:")
        first_label.grid(row=3, column=0, stick=E)

        self.first = Entry(editing)
        self.first.insert(0, self.data["first"])
        self.first.grid(row=3, column=1)

        last_label = Label(editing, text="Last:")
        last_label.grid(row=4, column=0, stick=E)

        self.last = Entry(editing)
        self.last.insert(0, self.data["last"])
        self.last.grid(row=4, column=1)

        district_label = Label(editing, text="District:")
        district_label.grid(row=5, column=0, stick=E)

        self.district = Entry(editing)
        self.district.insert(0, self.data["district"])
        self.district.grid(row=5, column=1)

        phone_num_label = Label(editing, text="Phone #:")
        phone_num_label.grid(row=6, column=0, stick=E)

        self.phone_num = Entry(editing)
        self.phone_num.insert(0, self.data["phone_num"])
        self.phone_num.grid(row=6, column=1)

        email_label = Label(editing, text="Email:")
        email_label.grid(row=7, column=0, stick=E)

        self.email = Entry(editing)
        self.email.insert(0, self.data["email"])
        self.email.grid(row=7, column=1)

        leg_page_label = Label(editing, text="Webpage:")
        leg_page_label.grid(row=8, column=0, stick=E)

        self.leg_page = Entry(editing)
        self.leg_page.insert(0, self.data["leg_page"])
        self.leg_page.grid(row=8, column=1)

        img_link_label = Label(editing, text="Img Link:")
        img_link_label.grid(row=9, column=0, stick=E)

        self.img_link = Entry(editing)
        self.img_link.insert(0, self.data["img_link"])
        self.img_link.grid(row=9, column=1)

        voting_label = Label(editing, text="Voting:")
        voting_label.grid(row=0, column=3, stick=E)

        self.voting = Entry(editing, width=10)
        self.voting.insert(0, self.data["voting"])
        self.voting.grid(row=0, column=4)

        rhetoric_label = Label(editing, text="Rhetoric:")
        rhetoric_label.grid(row=1, column=3, stick=E)

        self.rhetoric = Entry(editing, width=10)
        self.rhetoric.insert(0, self.data["rhetoric"])
        self.rhetoric.grid(row=1, column=4)

        donations_label = Label(editing, text="Donations:")
        donations_label.grid(row=2, column=3, sticky=E)

        self.donations = Entry(editing, width=10)
        self.donations.insert(0, self.data["donations"])
        self.donations.grid(row=2, column=4)

        last_updated_label = Label(editing, text="Last Updated:")
        last_updated_label.grid(row=3, column=3, stick=E)

        self.last_updated = Entry(editing, width=10)
        self.last_updated.insert(0, self.data["last_updated"])
        self.last_updated.config(state="readonly")
        self.last_updated.grid(row=3, column=4)

        def reset_entry():
            editing.destroy()
            self.entry_edit()

        def delete_entry(id):
            MsgBox = messagebox.askyesno(
                'Delete Entry', 'Are you sure you want to delete this entry', icon='warning', parent=editing)
            if MsgBox:
                double_check = messagebox.askokcancel(
                    'Entry Deleted', 'Entry Deleted\nPress \'Ok\' to continue\nPress \'Cancel\' to reinstate')
                if double_check:
                    cur.executescript(f"""INSERT INTO 'archive' SELECT legislators.*, voting, rhetoric, donations, last_updated FROM legislators INNER JOIN grades ON legislators.id = grades.id WHERE legislators.id='{id}';
                        DELETE FROM legislators WHERE id='{id}';
                        DELETE FROM grades WHERE id='{id}';""")
                    db.commit()
                    editing.destroy()


        reset_btn = Button(editing, text="Reset", command=reset_entry)
        reset_btn.grid(row=4, column=3, columnspan=2,
                       rowspan=2, stick=NSEW, padx=5, pady=2)

        update_btn = Button(editing, text="Update", command=lambda id=self.data["id"]: print(
            "Update"), bg="lightblue")
        update_btn.grid(row=6, column=3, columnspan=2,
                        rowspan=2, stick=NSEW, padx=5, pady=2)

        delete_btn = Button(
            editing, text="Delete", command=lambda id=self.data["id"]: delete_entry(id), bg="red")
        delete_btn.grid(row=8, column=3, rowspan=2, stick=NSEW, padx=5, pady=2)

        close_btn = Button(editing, text="Close w/o Changes",
                           command=editing.destroy)
        close_btn.grid(row=8, column=4, rowspan=2, stick=NSEW, padx=1, pady=2)

    def get_data(self, id):
        cur.execute(
            f"SELECT legislators.id, assembly, title, name, district, party, phone_num, email, leg_page, last, first, img_link, voting, rhetoric, donations,last_updated FROM legislators INNER JOIN grades ON legislators.id = grades.id WHERE legislators.id='{id}';")

        data = dict(zip(("id", "assembly", "title", "name", "district", "party", "phone_num", "email", "leg_page",
                         "last", "first", "img_link", "voting", "rhetoric", "donations", "last_updated"), cur.fetchone()))
        return data  # Data in dictionary

    def post_data(self, data):


    def update_data(self):
        pass


if __name__ == '__main__':
    main = Main(root)


    root.title("KCG something")
    root.mainloop()
