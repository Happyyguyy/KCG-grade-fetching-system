import time

try:
    import startup
    assembly = startup.assembly

    from tkinter import *
    from tkinter import messagebox
    from tkinter import filedialog
    import sqlite3
    import time
    import re
    # print("Loading module: create_card")
    # import create_card
    # print("Loading module: spreadsheets")
    # import spreadsheets
    # print("Loading module: get_legs")
    # import get_legs

    # init sqlite3 connection
    db = sqlite3.connect("db.db")
    cur = db.cursor()


    class Main:
        def __init__(self, master=None, root=None, assembly=assembly):
            self.assembly = assembly
            self.root = root
            self.config = ('party', 'title', 'name', 'district', 'rhetoric',
                           'donations', '')

            # new_screen = entryWindow(id)
            self.master = master
            tableFrame = Frame(master, bg="grey", width=500)
            self.tableFrame = tableFrame
            optionFrame = Frame(master, relief=SUNKEN, bd=1, padx=5, pady=2)
            buttonFrame = Frame(master, bd=1)

            tableFrame.grid(row=0, column=1, rowspan=2, stick=NSEW)
            optionFrame.grid(row=0, column=0, stick=NSEW)
            buttonFrame.grid(row=1, column=0, stick=NSEW)

            root.grid_rowconfigure(0, weight=0)
            root.grid_rowconfigure(1, weight=1)
            root.grid_columnconfigure(0, weight=0)
            root.grid_columnconfigure(1, weight=1)


            # ************ table Frame ************

            self.data_canvas = Canvas(tableFrame, width=600)
            self.data_canvas.grid(stick=NSEW)
            tableFrame.rowconfigure(0, weight=1)
            tableFrame.columnconfigure(0, weight=1)

            self.data_table = Frame(self.data_canvas, name="data_table")


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

            search_btn = Button(optionFrame, text="Search",
                                command=self.search)

            option_label = Label(optionFrame, text="Options")



            # grade filter
            self.grade_filter = Frame(optionFrame)

            self.grade_filter_button_list = []


            grade_filter_label = Label(self.grade_filter, text="Grade Filter")
            self.grade_filter_btn = Frame(self.grade_filter)

            grade_filter_all_btn = Button(
                self.grade_filter_btn, text="All", command=lambda: self.grade_filter_reset("all"))
            grade_filter_none_btn = Button(
                self.grade_filter_btn, text="None", command=lambda: self.grade_filter_reset("none"))


            grade_filter_label.grid(row=0, column=0)
            grade_filter_all_btn.grid(row=0, column=0)
            grade_filter_none_btn.grid(row=0, column=1)
            self.grade_filter_btn.grid(row=0, column=1)

            self.grade_filter_config = {}
            self.voting_filter = self.grade_config(
                self.grade_filter, "Voting", row=1, column=0, columnspan=2)
            self.grade_filter_config["voting"] = self.voting_filter
            self.rhetoric_filter = self.grade_config(
                self.grade_filter, "Rhetoric", row=2, column=0, columnspan=2)
            self.grade_filter_config["rhetoric"] = self.rhetoric_filter
            self.donations_filter = self.grade_config(
                self.grade_filter, "Donations", row=3, column=0, columnspan=2)
            self.grade_filter_config["donations"] = self.donations_filter


            refresh_btn = Button(optionFrame, text="Refresh List",
                                 command=self.print_table)

            self.searchbar.grid(row=0)
            search_btn.grid(row=0, column=1)

            option_label.grid(row=1, columnspan=2)

            self.id = self.checkbox(optionFrame, text="ID", row=2)
            self.district = self.checkbox(
                optionFrame, text="District", row=3, state="on")
            self.email = self.checkbox(optionFrame, text="Email", row=4)
            self.party = self.checkbox(
                optionFrame, text="Party", row=5, state="on")
            self.party_config = self.party_check(optionFrame, row=6)

            self.name = self.checkbox(
                optionFrame, text="Name", row=2, column=1, stick=W, state="on")
            self.phone_num = self.checkbox(
                optionFrame, text="Phone #", row=3, column=1, stick=W)
            self.leg_page = self.checkbox(
                optionFrame, text="Webpage", row=4, column=1, stick=W)
            self.title = self.checkbox(
                optionFrame, text="Title", row=5, column=1, stick=W, state="on")

            self.house = self.house_config(optionFrame, row=6, column=1)

            self.grade_filter.grid(row=10, columnspan=2)
            refresh_btn.grid(row=11, columnspan=2)

            # Gets data
            self.print_table()
            # creates window over canvas
            self.data_canvas.create_window(
                (4, 4), window=self.data_table, anchor="nw")
            # Set scrollregion with new data
            self.data_table.update_idletasks()
            self.data_canvas.config(scrollregion=self.data_canvas.bbox(ALL))

            # ************** Button Frame ******************
            button_dict = {
                "new_entry": self.new_entry,
                "show_archive": self.show_archive,
                "create_all": self.create_all,
                "create_selected": self.delay_create,
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
            # root.bind("<FocusIn>", lambda e,
            #           config=self.config: self.print_table())

        def grade_config(self, master, grade, row=0, column=0, rowspan=1, columnspan=1, **kwargs):
            frame = Frame(master)

            _filter_label = Label(frame, text=grade)
            _filter_label.grid(row=0, stick=E)
            _a = self.checkbox(frame, text="A", row=0, column=1, state="on")
            _b = self.checkbox(frame, text="B", row=0, column=2, state="on")
            _c = self.checkbox(frame, text="C", row=0, column=3, state="on")
            _d = self.checkbox(frame, text="D", row=0, column=4, state="on")
            _f = self.checkbox(frame, text="F", row=0, column=5, state="on")
            _none = self.checkbox(frame, text="ø", row=0, column=6, state="on")

            frame.grid(row=row, column=column,
                       rowspan=rowspan, columnspan=columnspan)

            return {"a": _a, "b": _b, "c": _c, "d": _d, "f": _f, "none": _none}

        def house_config(self, master, row=0, column=0, rowspan=1, columnspan=1, stick="w"):
            frame = Frame(master)

            title_label = Label(frame, text="House")

            sen_onoff = BooleanVar()
            sen_check = Checkbutton(
                frame, text="Senate", variable=sen_onoff)
            sen_check.state = sen_onoff
            sen_check.select()

            repr_onoff = BooleanVar()
            repr_check = Checkbutton(
                frame, text="Representatives", variable=repr_onoff)
            repr_check.state = repr_onoff
            repr_check.select()

            title_label.grid(row=0, column=0, stick=N)
            sen_check.grid(row=1, column=0, stick=W)
            repr_check.grid(row=2, column=0, stick=W)

            frame.grid(row=row, column=column, stick=stick,
                       rowspan=rowspan, columnspan=columnspan)

            return {"senate": sen_check, "representative": repr_check}

        def checkbox(self, master, text=None, row=0, column=0, state="off", rowspan=1, columnspan=1, stick="w", **kwargs):

            frame = Frame(master)

            _state = BooleanVar()
            box = Checkbutton(frame, text=text,
                              variable=_state)
            box.state = _state
            if state == "on":
                box.select()

            box.grid()
            frame.grid(row=row, column=column,
                       rowspan=rowspan, columnspan=columnspan, stick=stick)

            return box

        def grade_filter_reset(self, mode):
            for v in self.grade_filter_config.values():
                for box in v.values():
                    if mode == "all":
                        box.select()
                    if mode == "none":
                        box.deselect()

        def party_check(self, master, row=0, column=0, rowspan=1, columnspan=1, stick="w", **kwargs):

            frame = Frame(master)

            party_label = Label(frame, text="Party")

            dem_onoff = BooleanVar()
            dem = Checkbutton(
                frame, text="Democrat", variable=dem_onoff)
            dem.select()
            dem.state = dem_onoff

            rep_onoff = BooleanVar()
            rep = Checkbutton(
                frame, text="Republican", variable=rep_onoff)
            rep.select()
            rep.state = rep_onoff

            ind_onoff = BooleanVar()
            ind = Checkbutton(
                frame, text="Independent", variable=ind_onoff)
            ind.select()
            ind.state = ind_onoff

            party_label.grid(row=0, stick=N)
            dem.grid(row=1, stick=W)
            rep.grid(row=2, stick=W)
            ind.grid(row=3, stick=W)

            frame.grid(row=row, column=column, rowspan=rowspan,
                       columnspan=columnspan, stick=stick)

            return {"dem": dem, "rep": rep, "ind": ind}

        def search(self):
            # TODO: Search
            print(self.searchbar.get())

        def print_table(self):
            # id, title, party, name, district, , rhetoric, donations, email, webpage, phone_num
            self.config_dict = {
                "id": self.id.state.get(),
                "party": self.party.state.get(),
                "title": self.title.state.get(),
                "name": self.name.state.get(),
                "district": self.district.state.get(),
                "voting": True,
                "rhetoric": True,
                "donations": True,
                "email": self.email.state.get(),
                "leg_page": self.leg_page.state.get(),
                "phone_num": self.phone_num.state.get()
            }
            # print(self.config_dict)

            # build config list for sql query
            config = []

            for k, v in self.config_dict.items():
                if v:
                    if k == "id":
                        k = "legislators.id"
                    config.append(k)

            # filter
            keys = ("voting", "rhetoric", "donations", "party", "title")
            filter_config = {k: [] for k in keys}

            for category, v in self.grade_filter_config.items():
                for letter, y in v.items():
                    if y.state.get():
                        if letter == "none":
                            letter = ""
                        filter_config[category].append("'"+letter.upper()+"'")

            print(f"voting IN ({','.join(filter_config['voting'])})")

            for widget in self.data_table.winfo_children():
                widget.destroy()


            if None:
                # TODO: WHERE
                cur.execute(
                    f"SELECT {','.join(config)},legislators.id FROM legislators INNER JOIN grades ON legislators.id = grades.id WHERE voting IN ({','.join(filter_config['voting'])}) OR rhetoric IN ({','.join(filter_config['rhetoric'])}) OR donations IN ({','.join(filter_config['donations'])})")
            else:
                cur.execute(
                    f"SELECT {','.join(config)},legislators.id FROM legislators INNER JOIN grades ON legislators.id = grades.id WHERE (voting IN ({','.join(filter_config['voting'])}) OR rhetoric IN ({','.join(filter_config['rhetoric'])}) OR donations IN ({','.join(filter_config['donations'])})) AND assembly = {assembly} ORDER BY title, last")
            row_index = 0


            for i in range(len(config)):
                if config[i] == "legislators.id":
                    config[i] = "id"
                lbl = Label(self.data_table,
                            text=config[i].replace("_", " ").title())
                lbl.grid(row=0, column=i+1)

            row_index += 1
            self.table_buttons = Frame(self.data_table)

            self.selection_list = []
            num_rows = 0
            for row in cur.fetchall():
                num_rows += 1
                id = row[-1]
                edit_btn = Button(self.table_buttons, text="Edit",
                                  command=lambda id=id: self.edit_screen(edit_btn, id))
                edit_btn.grid(row=row_index-1, column=0)

                create_btn = Button(self.table_buttons, text="New",
                                    command=lambda id=id: self.new_card(id))
                create_btn.grid(row=row_index-1, column=1)

                sel = StringVar()
                row_select = Checkbutton(
                    self.table_buttons, offvalue="", onvalue=id, variable=sel)
                row_select.var = sel
                row_select.deselect()
                self.selection_list.append(row_select)
                row_select.grid(row=row_index-1, column=2)

                for i in range(len(row)-1):
                    lbl = Label(self.data_table, text=row[i], bd=1)
                    lbl.grid(row=row_index, column=i+1)
                # self.selection_list.append(edit_btn)
                row_index += 1

            self.table_buttons.grid(row=1, rowspan=num_rows)

            self.data_table.update_idletasks()
            self.data_canvas.config(scrollregion=self.data_canvas.bbox(ALL))



        def edit_screen(self, master=None, id=None):
            edit_screen = entryWindow(master, id)

        def new_entry(self):
            new_screen = entryWindow()

        def show_archive(self):
            archive = Archive(self.root)

            pass

        def create_all(self):
            for each in self.selection_list:
                each.select()
            self.delay_create()
            time.sleep(1)

        def delay_create(self):
            folder_path = filedialog.askdirectory()
            if not folder_path:
                return
            thing = Toplevel(self.master)
            lbl = Label(thing, text="Generating Report Cards")
            lbl.pack()
            root.after(
                2000, lambda folder_path=folder_path: self.create_selected(folder_path, thing))

        def create_selected(self, folder_path, alert):
            # step through list and generate list
            for each in self.selection_list:
                if each.var.get():
                    # set id
                    id = each.var.get()
                    # Set msg in progress bar
                    # Get data
                    cur.execute(
                        f"SELECT voting,rhetoric,donations,last_updated,last,first,title,district,assembly,name FROM grades INNER JOIN legislators ON legislators.id = grades.id WHERE legislators.id='{id}'")
                    voting, rhetoric, donations, last_updated, last, first, title, district, assembly, name = cur.fetchone()
                    card = create_card.create_card(
                        id, voting, rhetoric, donations)
                    # Set filename
                    filename = f"{last}_{first}_{assembly}{title[:3]}{district}_{last_updated.replace('/', '_')}.jpg".replace(
                        "\"", "")
                    # Save file
                    # card.save(folder_path + filename)
            alert.destroy()
            for each in self.selection_list:
                each.deselect()
            messagebox.showinfo(
                "Done", f"Report cards generated in: {folder_path}")


            # TODO: create_selected: save


        def update_legs(self):
            print("update_legs")
            get_legs.create_data_file()
            pass

        def update_grades(self):
            print("update_grades")
            spreadsheets.import_data()
            pass

        def new_card(self, id):
            # TODO: new_card: save

            cur.execute(
                f"SELECT voting,rhetoric,donations,last_updated,last,first,title,district,assembly FROM grades INNER JOIN legislators ON legislators.id = grades.id WHERE legislators.id='{id}'")
            voting, rhetoric, donations, last_updated, last, first, title, district, assembly = cur.fetchone()
            filename = f"{last}_{first}_{assembly}{title[:3]}{district}_{last_updated.replace('/', '_')}.jpg".replace(
                "\"", "")
            filename = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[
                                                    ("JPEG", ".jpg")], initialdir="Desktop", initialfile=filename)
            print(filename)
            if not filename:
                return
            card = create_card.create_card(id, voting, rhetoric, donations)
            card.show()
            # card.save(filename)



    class entryWindow:
        def __init__(self, master=None, id=None):
            self.base_id = id
            self.master = master
            if id:
                self.data = self.get_data(self.base_id)
                self.entry_edit()
            else:
                self.data = dict.fromkeys(("id", "assembly", "title", "name", "district", "party", "phone_num", "email",
                                           "leg_page", "last", "first", "img_link", "", "rhetoric", "donations", "last_updated"), "")
                self.entry_new()

        def entry_new(self):

            editing = Toplevel(self.master, padx=5, pady=5)
            self.editing = editing
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
            self.assembly.insert(0, self.data["assembly"])
            self.assembly.grid(row=1, column=1)

            self.party_label = Label(editing, text="Party:")
            self.party_label.grid(row=2, column=0, stick=E)

            self.party = Entry(editing)
            self.party.insert(0, self.data["party"])
            self.party.grid(row=2, column=1)

            title_label = Label(editing, text="Title:")
            title_label.grid(row=3, column=0, stick=E)

            self.title = Entry(editing)
            self.title.insert(0, self.data["title"])
            self.title.grid(row=3, column=1)

            first_label = Label(editing, text="First:")
            first_label.grid(row=4, column=0, stick=E)

            self.first = Entry(editing)
            self.first.insert(0, self.data["first"])
            self.first.grid(row=4, column=1)

            last_label = Label(editing, text="Last:")
            last_label.grid(row=5, column=0, stick=E)

            self.last = Entry(editing)
            self.last.insert(0, self.data["last"])
            self.last.grid(row=5, column=1)

            district_label = Label(editing, text="District:")
            district_label.grid(row=6, column=0, stick=E)

            self.district = Entry(editing)
            self.district.insert(0, self.data["district"])
            self.district.grid(row=6, column=1)

            phone_num_label = Label(editing, text="Phone #:")
            phone_num_label.grid(row=7, column=0, stick=E)

            self.phone_num = Entry(editing)
            self.phone_num.insert(0, self.data["phone_num"])
            self.phone_num.grid(row=7, column=1)

            email_label = Label(editing, text="Email:")
            email_label.grid(row=8, column=0, stick=E)

            self.email = Entry(editing)
            self.email.insert(0, self.data["email"])
            self.email.grid(row=8, column=1)

            leg_page_label = Label(editing, text="Webpage:")
            leg_page_label.grid(row=9, column=0, stick=E)

            self.leg_page = Entry(editing)
            self.leg_page.insert(0, self.data["leg_page"])
            self.leg_page.grid(row=9, column=1)

            img_link_label = Label(editing, text="Img Link:")
            img_link_label.grid(row=10, column=0, stick=E)

            self.img_link = Entry(editing)
            self.img_link.insert(0, self.data["img_link"])
            self.img_link.grid(row=10, column=1)

            voting_label = Label(editing, text=":")
            voting_label.grid(row=0, column=3, stick=E)

            self.voting = Entry(editing, width=10)
            self.voting.insert(0, self.data[""])
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

            date = time.strftime("%m/%d/%Y")
            last_updated_label = Label(editing, text="Last Updated:")
            last_updated_label.grid(row=3, column=3, stick=E)

            self.last_updated = Entry(editing, width=10)
            self.last_updated.insert(0, date)
            self.last_updated.grid(row=3, column=4)

            def reset_entry():
                self.entry_new()
                editing.destroy()

            reset_btn = Button(editing, text="Reset",
                               command=lambda: reset_entry())
            reset_btn.grid(row=4, column=3, columnspan=2,
                           rowspan=2, stick=NSEW, padx=5, pady=2)

            input_btn = Button(editing, text="Input",
                               command=lambda: self.post_entry(), bg="lightblue")
            input_btn.grid(row=6, column=3, columnspan=2,
                           rowspan=2, stick=NSEW, padx=5, pady=2)

            delete_btn = Button(editing, text="Cancel",
                                command=editing.destroy, bg="red")
            delete_btn.grid(row=8, column=3, columnspan=2,
                            rowspan=2, stick=NSEW, padx=5, pady=2)

        def entry_edit(self):
            editing = Toplevel(self.master, padx=5, pady=5)
            self.editing = editing
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

            self.party_label = Label(editing, text="Party:")
            self.party_label.grid(row=2, column=0, stick=E)

            self.party = Entry(editing)
            self.party.insert(0, self.data["party"])
            self.party.grid(row=2, column=1)

            title_label = Label(editing, text="Title:")
            title_label.grid(row=3, column=0, stick=E)

            self.title = Entry(editing)
            self.title.insert(0, self.data["title"])
            self.title.grid(row=3, column=1)

            first_label = Label(editing, text="First:")
            first_label.grid(row=4, column=0, stick=E)

            self.first = Entry(editing)
            self.first.insert(0, self.data["first"])
            self.first.grid(row=4, column=1)

            last_label = Label(editing, text="Last:")
            last_label.grid(row=5, column=0, stick=E)

            self.last = Entry(editing)
            self.last.insert(0, self.data["last"])
            self.last.grid(row=5, column=1)

            district_label = Label(editing, text="District:")
            district_label.grid(row=6, column=0, stick=E)

            self.district = Entry(editing)
            self.district.insert(0, self.data["district"])
            self.district.grid(row=6, column=1)

            phone_num_label = Label(editing, text="Phone #:")
            phone_num_label.grid(row=7, column=0, stick=E)

            self.phone_num = Entry(editing)
            self.phone_num.insert(0, self.data["phone_num"])
            self.phone_num.grid(row=7, column=1)

            email_label = Label(editing, text="Email:")
            email_label.grid(row=8, column=0, stick=E)

            self.email = Entry(editing)
            self.email.insert(0, self.data["email"])
            self.email.grid(row=8, column=1)

            leg_page_label = Label(editing, text="Webpage:")
            leg_page_label.grid(row=9, column=0, stick=E)

            self.leg_page = Entry(editing)
            self.leg_page.insert(0, self.data["leg_page"])
            self.leg_page.grid(row=9, column=1)

            img_link_label = Label(editing, text="Img Link:")
            img_link_label.grid(row=10, column=0, stick=E)

            self.img_link = Entry(editing)
            self.img_link.insert(0, self.data["img_link"])
            self.img_link.grid(row=10, column=1)

            voting_label = Label(editing, text=":")
            voting_label.grid(row=0, column=3, stick=E)

            self.voting = Entry(editing, width=10)
            self.voting.insert(0, self.data[""])
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

            reset_btn = Button(editing, text="Reset", command=self.reset_entry)
            reset_btn.grid(row=4, column=3, columnspan=2,
                           rowspan=2, stick=NSEW, padx=5, pady=2)

            update_btn = Button(
                editing, text="Update", command=self.update_entry, bg="lightblue")
            update_btn.grid(row=6, column=3, columnspan=2,
                            rowspan=2, stick=NSEW, padx=5, pady=2)

            delete_btn = Button(
                editing, text="Delete", command=lambda: self.delete_entry(), bg="red")
            delete_btn.grid(row=8, column=3, rowspan=2,
                            stick=NSEW, padx=5, pady=2)

            close_btn = Button(editing, text="Close w/o Changes",
                               command=editing.destroy)
            close_btn.grid(row=8, column=4, rowspan=2,
                           stick=NSEW, padx=1, pady=2)

        def get_data(self, id):
            cur.execute(
                f"SELECT legislators.id, assembly, title, name, district, party, phone_num, email, leg_page, last, first, img_link, , rhetoric, donations,last_updated FROM legislators INNER JOIN grades ON legislators.id = grades.id WHERE legislators.id='{id}';")

            data = dict(zip(("id", "assembly", "title", "name", "district", "party", "phone_num", "email", "leg_page",
                             "last", "first", "img_link", "", "rhetoric", "donations", "last_updated"), cur.fetchone()))
            return data  # Data in dictionary


        def update_data(self):
            # legislators.id, assembly, title, name, district, party, phone_num, email,
            # leg_page, last, first, img_link, , rhetoric, donations,last_updated
            self.data = {
                "id": self.assembly.get() + self.title.get()[:3].lower() + self.last.get().lower() + self.district.get(),
                "assembly": self.assembly.get().strip(" "),
                "title": self.title.get().strip(" ").title(),
                "name": self.first.get().strip(" ").title() + " " + self.last.get().strip(" ").title(),
                "district": self.district.get().strip(" "),
                "party": self.party.get().strip(" ").title(),
                "phone_num": self.phone_num.get().strip(" ").title(),
                "email": self.email.get().strip(" "),
                "leg_page": self.leg_page.get().strip(" "),
                "last": self.last.get().strip(" ").title(),
                "first": self.first.get().strip(" ").title(),
                "img_link": self.img_link.get().strip(" "),
                "voting": self.voting.get().upper().strip(" "),
                "rhetoric": self.rhetoric.get().upper().strip(" "),
                "donations": self.donations.get().upper().strip(" "),
                "last_updated": self.last_updated.get().strip(" ")
            }
            return self.data

        def validate_data(self):
            self.update_data()

            # Regex for validation
            email_regex = re.compile(
                r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
            img_link_regex = re.compile(r"^https://leg.colorado.gov/[^\s]+$")
            leg_page_regex = re.compile(r"^/legislators/[^\s]+$")
            phone_num_regex = re.compile(r"^[\d]{3}-[\d]{3}-[\d]{4}$")
            date_regex = re.compile(r"^[\d]{,2}/[\d]{,2}/[\d]{4}$")
            title_regex = re.compile(r"^Representative|Senator$")
            party_regex = re.compile(r"^Democrat|Republican$")
            num_regex = re.compile(r"[\d]+$")
            grade_regex = re.compile(r"^[ABCDEF]$")

            if not email_regex.match(self.data["email"]):
                messagebox.showwarning(
                    "Wrong Format", "Incorrect Email Format", parent=self.editing)
                self.email.config(bg="pink")
                raise KeyError("Incorrect 'email' Format")
            self.email.config(bg="white")

            if not img_link_regex.match(self.data["img_link"]):
                messagebox.showwarning(
                    "Wrong Format", "Incorrect Img Link Format", parent=self.editing)
                self.img_link.config(bg="pink")
                raise KeyError("Incorrect 'img_link' Format")
            self.img_link.config(bg="white")

            if not leg_page_regex.match(self.data["leg_page"]):
                messagebox.showwarning(
                    "Wrong Format", "Incorrect Webpage Format\nFormat: /legislators/<name>", parent=self.editing)
                self.leg_page.config(bg="pink")
                raise KeyError("Incorrect 'leg_page' Format")
            self.leg_page.config(bg="white")

            if not phone_num_regex.match(self.data["phone_num"]):
                messagebox.showwarning(
                    "Wrong Format", "Incorrect Phone # Format\nFormat: ###-###-####", parent=self.editing)
                self.phone_num.config(bg="pink")
                raise KeyError("Incorrect 'phone_num' Format")
            self.phone_num.config(bg="white")

            if not date_regex.match(self.data["last_updated"]):
                messagebox.showwarning(
                    "Wrong Format", "Incorrect date Format", parent=self.editing)
                self.last_updated.config(bg="pink")
                raise KeyError("Incorrect 'last_updated' Format")
            self.last_updated.config(bg="white")

            if not title_regex.match(self.data["title"]):
                messagebox.showwarning(
                    "Wrong Format", "Entry must be 'Senator' or 'Representative'", parent=self.editing)
                self.title.config(bg="pink")
                raise KeyError("Incorrect 'title' Format")
            self.title.config(bg="white")

            if not party_regex.match(self.data["party"]):
                messagebox.showwarning(
                    "Wrong Format", "Party must be 'Democrat' or 'Republican'", parent=self.editing)
                self.party.config(bg="pink")
                raise KeyError("Incorrect 'party' Format")
            self.party.config(bg="white")

            if not num_regex.match(self.data["assembly"]):
                messagebox.showwarning(
                    "Wrong Format", "Assembly entry must be a number", parent=self.editing)
                self.assembly.config(bg="pink")
                raise KeyError("Incorrect 'assembly' Format")
            self.assembly.config(bg="white")

            if not grade_regex.match(self.data[""]):
                messagebox.showwarning(
                    "Wrong Format", " must be 'A', 'B', 'C', 'D', or 'F'", parent=self.editing)
                self.voting.config(bg="pink")
                raise KeyError("Incorrect '' Format")
            self.voting.config(bg="white")

            if not grade_regex.match(self.data["rhetoric"]):
                messagebox.showwarning(
                    "Wrong Format", "Rhetoric must be 'A', 'B', 'C', 'D', or 'F'", parent=self.editing)
                self.rhetoric.config(bg="pink")
                raise KeyError("Incorrect 'rhetoric' Format")
            self.rhetoric.config(bg="white")

            if not grade_regex.match(self.data["donations"]):
                messagebox.showwarning(
                    "Wrong Format", "Donations must be 'A', 'B', 'C', 'D', or 'F'", parent=self.editing)
                self.donations.config(bg="pink")
                raise KeyError("Incorrect 'donations' Format")
            self.donations.config(bg="white")

            if not num_regex.match(self.data["district"]):
                messagebox.showwarning(
                    "Wrong Format", "District entry must be a number", parent=self.editing)
                self.district.config(bg="pink")
                raise KeyError("Incorrect 'district' Format")
            self.district.config(bg="white")

        def post_entry(self):
            editing = self.editing
            self.update_data()
            try:
                self.validate_data()
            except Exception as e:
                print(e)
                return
            MsgBox = messagebox.askyesno(
                'Update Entry', 'Are you sure you want to update this entry?', icon='warning', parent=editing)
            if MsgBox:
                double_check = messagebox.askokcancel(
                    'Entry Updated', 'Entry Updated\nPress \'Ok\' to continue\nPress \'Cancel\' to revert')
                if double_check:
                        # legislators.id, assembly, title, name, district, party, phone_num, email,
                        # leg_page, last, first, img_link, , rhetoric, donations,last_updated
                    print(self.data["id"])
                    cur.execute(f"""UPDATE legislators SET
                        id = '{self.data["id"]}',
                        assembly = '{self.data["assembly"]}',
                        title = '{self.data["title"]}',
                        name = '{self.data["name"]}',
                        district = '{self.data["district"]}',
                        party = '{self.data["party"]}',
                        phone_num = '{self.data["phone_num"]}',
                        email = '{self.data["email"]}',
                        leg_page = '{self.data["leg_page"]}',
                        last = '{self.data["last"]}',
                        first = '{self.data["first"]}',
                        img_link = '{self.data["img_link"]}'
                        WHERE id='{self.data["id"]}';""")

                    cur.execute(f"""UPDATE grades SET
                        grades.id = '{self.data["id"]}',
                        voting = '{self.data["voting"]}',
                        rhetoric = '{self.data["rhetoric"]}',
                        donations = '{self.data["donations"]}',
                        last_updated = '{self.data["last_updated"]}'
                        WHERE id= '{self.data["id"]}';""")
                    db.commit()
                    editing.destroy()

            pass

        def update_entry(self):
            editing = self.editing
            self.update_data()
            try:
                self.validate_data()
            except Exception as e:
                print(e)
                return
            MsgBox = messagebox.askyesno(
                'Update Entry', 'Are you sure you want to update this entry?', icon='warning', parent=editing)
            if MsgBox:
                double_check = messagebox.askokcancel(
                    'Entry Updated', 'Entry Updated\nPress \'Ok\' to continue\nPress \'Cancel\' to revert')
                if double_check:
                        # legislators.id, assembly, title, name, district, party, phone_num, email,
                        # leg_page, last, first, img_link, , rhetoric, donations,last_updated
                    print(self.data["id"])
                    cur.execute(f"""INSERT INTO legislators
                        (id,assembly,title,name,district,party,phone_num,email,leg_page,last,first,img_link)
                        VALUES
                        ({self.data["id"]},
                        {self.data["assembly"]},
                        {self.data["title"]},
                        {self.data["name"]},
                        {self.data["district"]},
                        {self.data["party"]},
                        {self.data["phone_num"]},
                        {self.data["email"]},
                        {self.data["leg_page"]},
                        {self.data["last"]},
                        {self.data["first"]},
                        {self.data["img_link"]})
                        WHERE id='{self.data["id"]}';""")

                    cur.execute(f"""UPDATE grades SET
                        grades.id = '{self.data["id"]}',
                        voting = '{self.data["voting"]}',
                        rhetoric = '{self.data["rhetoric"]}',
                        donations = '{self.data["donations"]}',
                        last_updated = '{self.data["last_updated"]}'
                        WHERE id= '{self.data["id"]}';""")
                    db.commit()

                    spreadsheets.update_data(
                        self.data["id"], self.data["voting"], self.data["rhetoric"], self.data["donations"])

                    editing.destroy()

        def reset_entry(self):
            self.editing.destroy()
            self.data = self.get_data(self.base_id)
            self.entry_edit()

        def delete_entry(self):
            MsgBox = messagebox.askyesno(
                'Delete Entry', 'Are you sure you want to delete this entry', icon='warning', parent=self.editing)
            if MsgBox:
                double_check = messagebox.askokcancel(
                    'Entry Deleted', 'Entry Deleted\nPress \'Ok\' to continue\nPress \'Cancel\' to reinstate')
                if double_check:
                    self.update_data()
                    cur.executescript(f"""INSERT INTO 'archive' SELECT legislators.*, , rhetoric, donations, last_updated FROM legislators INNER JOIN grades ON legislators.id = grades.id WHERE legislators.id='{self.id}';
                        DELETE FROM legislators WHERE id='{self.id}';
                        DELETE FROM grades WHERE id='{self.id}';""")
                    db.commit()
                    self.editing.destroy()


    class Archive():
        def __init__(self, master=None):
            window = Toplevel(master)
            window.title("Archive")
            window.rowconfigure(0, weight=1)
            window.columnconfigure(0, weight=1)
            canvas = Canvas(window, width=500)
            frame = Frame(canvas, width=500)
            self.print_table(frame)
            # frame.grid(stick=NSEW)
            canvas.grid(stick=NSEW)
            # frame.rowconfigure(0, weight=1)
            # frame.columnconfigure(0, weight=1)
            canvas.rowconfigure(0, weight=1)
            canvas.columnconfigure(0, weight=1)


            canvas.create_window(
                (4, 4), window=frame, anchor="nw")

            vscrollbar = Scrollbar(window, orient=VERTICAL)
            vscrollbar.grid(row=0, column=1, stick=NS+E)
            vscrollbar.config(command=canvas.yview)

            hscrollbar = Scrollbar(window, orient=HORIZONTAL)
            hscrollbar.grid(row=1, stick=EW+S)
            hscrollbar.config(command=canvas.xview)

            canvas.config(
                yscrollcommand=vscrollbar.set, xscrollcommand=hscrollbar.set)

            # Set scrollregion with new data
            canvas.update_idletasks()
            canvas.config(scrollregion=canvas.bbox(ALL))
            canvas.config(width=500, height=500)

            close = Button(window, text="Close", command=self.destroy())
            close.grid(row=10)

        def print_table(self, frame):

            # Get headers
            cur.execute("PRAGMA table_info(archive)")

            col = 0
            for each in cur.fetchall():
                print(each[1])
                cell = Label(frame, text=each[1])
                cell.grid(row=0, column=col)
                col += 1


            cur.execute("SELECT * FROM 'archive';")

            row = 1
            for line in cur.fetchall():
                col = 0
                for each in line:
                    cell = Label(frame, text=each)
                    cell.grid(row=row, column=col)
                    col += 1
                row += 1




    fsaff
    if __name__ == '__main__':
        root = Tk()
        main = Main(root, root)
        # archive = Archive(root)
        root.title("KCG something")
        root.mainloop()
except Exception as e:
    with open("log.log", "w") as log:
        log.write(str(e))
        print(e)
    time.sleep(10)
    while 1:
        1+1
