from tkinter import *
from tkinter import filedialog
from tkinter.font import BOLD
from pathlib import Path
from scroll import ScrollFrame
import sqlite3
import os

font_family = ('Sans-Serif Workhorse')
directorPath = Path(__file__).parent.absolute()

class App:
    def __init__(self, root=None):
        self.root = root
        self.root.title('Developers WorkSpace')
        self.root.geometry('900x550+250+80')
        self.root.configure(background='#fcfcfc')
        self.root.resizable(False, False)
        self.page_1 = Page_1(master=self.root, app=self)
        self.page_2 = Page_2(master=self.root, app=self)
        self.frame = Frame(self.root, bg='#fcfcfc')
        self.frame.pack(fill='both', expand=True)
        

        self.label = Label(self.frame, text='Developer WorkSpace', font=(font_family, 30, BOLD), fg="#384850", bg='#f2f2fd', height=2).pack(fill='x')
        
        self.projImg = PhotoImage(file = str(directorPath) + '\Webp.net-resizeimage.png')
        Label(self.frame, width=182, height=170, bg='#f2f2fd', image=self.projImg).place(x=200, y=195)
        self.projectsBtn = Button(self.frame, text='Projects', font=(font_family,12, BOLD), fg="#f8f8f8",bg='#384850', width=18, pady=5, bd=0, cursor='hand2', command=self.make_page_1)
        self.projectsBtn.place(x=200, y=350)
        
        self.docImg = PhotoImage(file = str(directorPath) + '\Webp.net-resizeimage2.png')
        Label(self.frame, width=182, height=175, bg='#f2f2fd', image=self.docImg).place(x=520, y=195)
        self.workspaceBtn = Button(self.frame, text='Documents', font=(font_family,12, BOLD), fg="#f8f8f8",bg='#384850', width=18, pady=5, bd=0, cursor='hand2', command=self.make_page_2)
        self.workspaceBtn.place(x=520, y=350)
  

    def main_page(self):
        self.frame.pack(fill='both', expand=True)

    def make_page_1(self):
        self.frame.pack_forget()
        self.page_1.start_page()

    def make_page_2(self):
        self.frame.pack_forget()
        self.page_2.start_page()


class Page_1:
    def __init__(self, master=None, app=None):
        self.master = master
        self.app = app
        self.frame = Frame(self.master, bg='#fcfcfc')
        Label(self.frame, text='Projects', font=(font_family, 30, BOLD), fg="#384850", bg='#f2f2fd', height=2).pack(fill='x')
        self.projects_message = Label()

        # database connection
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()

        # buttons header
        headFrame = Frame(self.frame, width=800, height=40, bg='#fcfcfc')
        headFrame.pack(pady=15)
        headFrame.pack_propagate(False)
        Button(headFrame, text='🡸 Go Back', bg='#384850', fg='#f8f8f8',font=(font_family, 13, BOLD), pady=5, padx=8, bd=0, height=1, cursor='hand2', command=self.go_back).pack(fill=Y, side=LEFT)
        ask = Button(headFrame, text='➕ New', bg='#384850', fg='#f8f8f8',font=(font_family, 13, BOLD), pady=5, padx=8, bd=0, height=1, cursor='hand2', command=self.openFile)
        ask.pack(fill=Y, side=LEFT, padx=8)


        self.projectsHeader = Frame(self.frame, bg='#0066b8', width=800, height=30)
        self.projectsHeader.pack()
        self.projectsHeader.pack_propagate(False)
        nameLbl = Label(self.projectsHeader, text='Name', bg='#0066b8', fg='#fcfcfc', font=(font_family, 10, BOLD), padx=75).pack(side=LEFT, fill=Y)
        pathLbl = Label(self.projectsHeader, text='Directory Path', bg='#0066b8', fg='#fcfcfc', font=(font_family, 10, BOLD), padx=160).pack(side=LEFT, fill=Y)
        pathLbl = Label(self.projectsHeader, text='IDE', bg='#0066b8', fg='#fcfcfc', font=(font_family, 10, BOLD), padx=65).pack(side=LEFT, fill=Y)

        # projects table
        self.projectsFrame = Frame(self.frame, width=800, height=320, bg='#fcfcfc')
        self.projectsFrame.pack()
        self.projectsFrame.pack_propagate(False)

        self.init_projectList()

    def start_page(self):
        self.frame.pack(fill='both', expand=True)

    def go_back(self):
        self.frame.pack_forget()
        self.app.main_page()

    def openFile(self):
        folderPath = filedialog.askdirectory()
        if folderPath:
            self.insert_project(os.path.basename(folderPath), folderPath)
            self.init_projectList()

    def init_projectList(self):
        # clear old projects
        self.clear_projectList()

        # fetch new projects
        listOfTables = self.cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='projects'").fetchall()
        if listOfTables == []:
            self.cursor.execute("""CREATE TABLE projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dirName TEXT,
                dirPath TEXT
            ) """)

        # fill project list
        self.fill_projectList()


    def clear_projectList(self):
        for widgets in self.projectsFrame.winfo_children():
            widgets.destroy()

    def fill_projectList(self):
        projects = self.cursor.execute("SELECT * FROM projects").fetchall()
        round = 0

        if projects:
            self.projects_message.destroy()
            for project in projects:
                if round%2 == 0:
                    row = Frame(self.projectsFrame, height=50, bg='#f2f2fd')
                    row.pack(fill=X, pady=1)
                    row.pack_propagate(False)

                    dirName = Label(row, text=project[1], width=25, font=(font_family, 8, BOLD), fg="#384850", bg='#f2f2fd')
                    dirName.pack(fill=Y, side=LEFT)

                    pathName = Label(row, text=project[2], anchor='w', width=70, font=(font_family, 8), fg="#384850", bg='#f2f2fd')
                    pathName.pack(fill=Y, side=LEFT)

                    vscodeBtn = Button(row, text='Open In VScode' , fg='#fcfcfc', bg='#0066b8', bd=0, pady=5, padx=5, command= lambda val=project[2]:self.open_vscode(val))
                    vscodeBtn.pack(side=LEFT, padx=30)

                    deleteBtn = Button(row, text='🗙' , fg='#384850', bg='#f2f2fd', bd=0, pady=5, padx=5, font=15, command = lambda val=project[0]:self.delete_project(val))
                    deleteBtn.pack(side=RIGHT, fill=Y)
                else:
                    row = Frame(self.projectsFrame, height=50, bg='#fcfcfc')
                    row.pack(fill=X)
                    row.pack_propagate(False)

                    dirName = Label(row, text=project[1], font=(font_family, 8, BOLD), width=25, fg='#384850' ,bg='#fcfcfc')
                    dirName.pack(fill=Y, side=LEFT)

                    pathName = Label(row, text=project[2], anchor='w', font=(font_family, 8), width=70, fg='#384850', bg='#fcfcfc')
                    pathName.pack(fill=Y, side=LEFT)

                    vscodeBtn = Button(row, text='Open In VScode' , fg='#fcfcfc', bg='#0066b8', bd=0, pady=5, padx=5, command= lambda val=project[2]:self.open_vscode(val))
                    vscodeBtn.pack(side=LEFT, padx=30)

                    deleteBtn = Button(row, text='🗙' , fg='#384850', bg='#fcfcfc', bd=0, pady=5, padx=5, font=15, command = lambda val=project[0]:self.delete_project(val))
                    deleteBtn.pack(side=RIGHT, fill=Y)
                round+=1
        else:
            # self.projects_message = Label(self.projectsFrame, text='No Projects Yet..!', fg='#0066b8', font=(font_family,15,BOLD))
            # self.projects_message.pack(fill='both', expand=TRUE)
            contentImg = PhotoImage(file = str(directorPath) + '\construction2.png')
            self.projects_message = Label(self.projectsFrame)
            self.projects_message = Label(self.projectsFrame, width=150, height=150, bg='#fcfcfc')
            self.projects_message.image = contentImg  # <== this is were we anchor the img object
            self.projects_message.configure(image=contentImg)
            self.projects_message.pack(pady=70) # place(x=250, y=150)
    
    def open_vscode(self, dirPath):
        os.chdir(dirPath)
        os.popen('code .')



    # Page 1 SQL Query functions
    def insert_project(self, dirName, dirPath):
        with self.conn:
            self.cursor.execute("INSERT INTO projects (dirName, dirPath) VALUES(?,?)", (dirName, dirPath))

    def delete_project(self, project_id):
        with self.conn:
            self.cursor.execute("DELETE FROM projects WHERE id = ?", [project_id])
        self.init_projectList()






class Page_2:
    def __init__(self, master=None, app=None):
        self.master = master
        self.app = app
        self.frame = Frame(self.master, bg='#fcfcfc')
        Label(self.frame, text='Documents', font=(font_family, 30, BOLD), fg="#384850", bg='#f2f2fd', height=2).pack(fill='x')
        
        # global variables
        self.content_old_frame = Frame()
        self.doc_modal = Frame()
        self.note_modal = Frame()
        self.remove_modal = Frame()
        self.selected_nav_noteAlert = Label()
        self.current_nav_id = 0

        # database connection
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()
        
        # Content frame
        self.contentFrame = Frame(self.frame, bg='#fcfcfc', width=700, height=450)
        self.contentFrame.place(x=200, y=98) #y=98
        self.contentFrame.pack_propagate(False)

        contentImg = PhotoImage(file = str(directorPath) + '\Webp.net-resizeimage3.png')
        empty_img = Label(self.contentFrame, width=150, height=150, bg='#fcfcfc')
        empty_img.image = contentImg  # <== this is were we anchor the img object
        empty_img.configure(image=contentImg)
        empty_img.place(x=271, y=149) # place(x=271, y=149)

        # SideBar frame
        self.sideBarFrame = Frame(self.frame, bg='#f8f8f8', width=200, height=450)
        self.sideBarFrame.place(x=0, y=98) #y=98
        self.sideBarFrame.pack_propagate(False)
        Button(self.sideBarFrame, text='🡸 Go Back', bg='#384850', fg='#f8f8f8',font=(font_family, 13, BOLD), pady=5, bd=0, height=1, cursor='hand2', command=self.go_back).pack(fill='x')
        Label(self.sideBarFrame, text='Documents', pady=3, bg='#e16259', fg='#f8f8f8', font=(font_family, 11, BOLD)).pack(fill='x')
        
        # actions frame
        actions = Frame(self.sideBarFrame, bg='#e16259', pady=5, padx=7, height=20)
        actions.pack(fill='x')
        Button(actions, text='Add',    bd=0, width=10, bg='#fdf5f2', fg='#e16259',font=(font_family, 10, BOLD), cursor='hand2', command= self.add_document).pack(side=LEFT) #➕
        Button(actions, text='Delete', bd=0, width=10, bg='#fdf5f2', fg='#e16259',font=(font_family, 10, BOLD), cursor='hand2', command= self.delete_document).pack(side=RIGHT) #➕

        # navigation list frame
        self.navListFrame = Frame(self.sideBarFrame, bg='#f2f2fd', width=200, height=389, bd=0)
        self.navListFrame.pack(fill='both')
        self.navListFrame.pack_propagate(False)
        Scrollbar(self.navListFrame, orient='vertical').pack(fill='y', side=RIGHT)
        
        # initialize navList
        self.init_navList()

    def start_page(self):
        self.frame.pack(fill='both', expand=True)

    def go_back(self):
        self.frame.pack_forget()
        self.content_old_frame.destroy()
        self.doc_modal.destroy()
        self.note_modal.destroy()
        self.remove_modal.destroy()
        self.current_nav_id = 0
        self.app.main_page()



    def init_navList(self):
        # clear old navs
        self.clear_navList()
        
        # fetch new navs
        listOfTables = self.cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='documents'").fetchall()
        if listOfTables == []:
            self.cursor.execute("""CREATE TABLE documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT
            ) """)

            self.cursor.execute("""CREATE TABLE contents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                doc_id INTEGER,
                title TEXT,
                command TEXT,
                description TEXT,
                FOREIGN KEY (doc_id) REFERENCES documents(id)
            ) """)

        # self.inst('React')
        # self.inst('Vanilla JS')
        # self.inst('Laravel')

        # self.insert_note(1, 'React Hooks' ,'useEffect()', 'this is a description')
        # self.insert_note(1, 'NPM Package Manager' ,'npm start', 'this is another description')
        # self.insert_note(2, 'JS built-in funcs' , 'getElementById()', 'this is a description')
        # self.insert_note(3, 'back-end concepts' , 'middleware()', 'this is a description')

        # fill navBar 
        self.fill_navList()
    
    def clear_navList(self):
        for widgets in self.navListFrame.winfo_children():
            widgets.destroy()

    def fill_navList(self):
        documents = self.cursor.execute("SELECT * FROM documents").fetchall()
        if documents:
            for doc in documents:
                navButton = Button(self.navListFrame, text=doc[1], font=(font_family, 10, BOLD), bd=0, pady=5, bg='#fdf5f2', fg='#e16259', cursor='hand2', command= lambda value=doc[0]:self.fill_contnet(value))
                navButton.pack(fill='x')
        else:
            notFoundLabel = Label(self.navListFrame, text='No Docs Found', font=(font_family, 10, BOLD), bd=0, pady=200, bg='#fdf5f2', fg='#e16259')
            notFoundLabel.pack(fill='x')
    
    def fill_contnet(self, doc_id):
        self.current_nav_id = doc_id
        self.doc_modal.destroy()
        self.note_modal.destroy()
        self.remove_modal.destroy()
        selected_nav_content = self.cursor.execute("SELECT * FROM contents WHERE doc_id = ?", [doc_id]).fetchall()
        selected_nav_title = self.cursor.execute("SELECT title FROM documents WHERE id = ?", [doc_id]).fetchone()
        
        if self.content_old_frame:
            self.content_old_frame.destroy()
            self.toggle_content_frame(selected_nav_content, selected_nav_title)
        else:
            self.toggle_content_frame(selected_nav_content, selected_nav_title)

    def toggle_content_frame(self, contents, title):
        # selected_frame = Frame(self.contentFrame, width=700, height=450, bg='#fcfcfc')
        # selected_frame.pack(fill='both')
        # selected_frame.pack_propagate(False)
        # scroll = Scrollbar(selected_frame, orient='vertical')
        # scroll.pack(fill='y', side=RIGHT)

        selected_frame = ScrollFrame(self.contentFrame)

        selected_frame_header = Frame(selected_frame.viewPort, width=620, height=37, bg='#f2f2fd',)
        selected_frame_header.pack(pady=10) # place(x=30, y=15)
        selected_frame_header.pack_propagate(False)


        header_title = Label(selected_frame_header, text=title[0], bg='#f2f2fd', font=(font_family, 17, BOLD), fg='#384850')
        header_title.place(x=160, y=0, width=300, height=37)
        add_note = Button(selected_frame_header, text='➕ New', bd=0, bg='#384850', fg='white', font=(font_family, 11, BOLD), padx=15, cursor='hand2', command= self.add_content)
        add_note.pack(fill=Y, side=RIGHT)

        if contents:
            self.selected_nav_noteAlert.destroy()
            for content in contents:
                # Card 
                card = Frame(selected_frame.viewPort, width=620, height= 150, bd=0, bg='#fdf5f2')
                card.pack(pady=15) # place(x=30, y=y_diminsion)
                card.pack_propagate(False)

                # Title area
                card_title = Label(card, text=content[2], pady=5, bg='#e16259', fg='#f8f8f8', font=(font_family,10, BOLD))
                card_title.pack(fill=X)
                close = Button(card_title, text='🗙', font=(font_family,9), bg='#fdf5f2', fg='#e16259', bd=0, cursor='hand2', command= lambda val = content[0]:self.delete_note(val)).pack(side=RIGHT, fill=Y)
                edit = Button(card_title, text='⌨', font=(font_family,10), bg='#fdf5f2', fg='#e16259', bd=0, cursor='hand2', command= lambda val = content[0]:self.edit_note(val)).pack(side=RIGHT, fill=Y, padx=2)
                
                # Command area
                command = Label(card, text=content[3], width=82, pady=8, bg='#fcfcfc', fg='#384850', bd=0)
                command.place(x=20, y=40)
                command.pack_propagate(False)
                Button(command, text='❒', font=13, bd=0, bg='#f1f1f1', fg='#384850', cursor='hand2', command= lambda val=content[3]:self.copyToClip(val)).pack(side=RIGHT, fill=Y)
                
                # Description area
                Label(card, text=content[4], width=82, pady=5, height=3, bd=0, bg='#fcfcfc').place(x=20, y=80)
        else:
            contentImg = PhotoImage(file = str(directorPath) + '\Webp.net-resizeimage3.png')
            self.selected_nav_noteAlert = Label(selected_frame.viewPort, width=150, height=150, bg='#fcfcfc')
            self.selected_nav_noteAlert.image = contentImg  # <== this is were we anchor the img object
            self.selected_nav_noteAlert.configure(image=contentImg)
            self.selected_nav_noteAlert.pack(pady=85) # place(x=250, y=150)

        self.content_old_frame = selected_frame
        
        selected_frame.pack(side="top", fill="both", expand=True)
        selected_frame.pack_propagate(False)

    def copyToClip(self, copy):
        command = 'echo ' + copy.strip() + '| clip'
        os.system(command)

    def add_content(self):
        title = StringVar()
        command = StringVar()
        desc = StringVar()
        self.content_old_frame.destroy()
        self.doc_modal.destroy()
        self.remove_modal.destroy()

        if self.note_modal: self.note_modal.destroy()

        # Card
        self.note_modal = Frame(self.contentFrame, width=500, height=300, bg='#f2f2fd')
        self.note_modal.place(x=100, y=70)
        self.note_modal.pack_propagate(False)
        Label(self.note_modal, text='New Note', font=(font_family, 11, BOLD), pady=5, bg='#384850', fg='#f8f8f8').pack(fill='x')
        
        # Title entry
        titleLabel = Label(self.note_modal, text='Title',font=(font_family, 10, BOLD), fg='#f8f8f8', bg='#384850', bd=0, padx=34)
        titleLabel.place(x=58,y=50, height=30) #+35
        titleEntry = Entry(self.note_modal, width=45, bd=0, textvariable=title)
        titleEntry.place(x=155, y=50, height=30) #+35

        # Command entry
        titleLabel = Label(self.note_modal, text='Command',font=(font_family, 10, BOLD), fg='#f8f8f8', bg='#384850', bd=0, padx=15)
        titleLabel.place(x=58,y=95, height=30) #+35
        commandEntry = Entry(self.note_modal, width=45, bd=0, textvariable=command)
        commandEntry.place(x=155, y=95, height=30) #+35

        # Description entry
        titleLabel = Label(self.note_modal, text='Description',font=(font_family, 10, BOLD), fg='#f8f8f8', bg='#384850', bd=0, padx=13)
        titleLabel.place(x=57,y=140, height=30) #+35
        descEntry = Text(self.note_modal, width=34, bd=0)
        descEntry.place(x=155, y=140, height=100) #+35

        submit = Button(self.note_modal, text='Create', bd=0, font=(font_family, 8, BOLD), padx=5, bg='#384850', fg='#f8f8f8', cursor='hand2', command=lambda:self.insert_note(self.current_nav_id, title.get(), command.get(), descEntry.get("1.0",'end-1c')))
        submit.place(x=185, y=255, width= 145, height=30)
    
    def edit_note(self, note_id):
        title = StringVar()
        command = StringVar()
        desc = StringVar()
        self.content_old_frame.destroy()
        self.doc_modal.destroy()
        self.remove_modal.destroy()

        if self.note_modal: self.note_modal.destroy()

        # Card
        self.note_modal = Frame(self.contentFrame, width=500, height=300, bg='#f2f2fd')
        self.note_modal.place(x=100, y=70)
        self.note_modal.pack_propagate(False)
        Label(self.note_modal, text='Edit Note', font=(font_family, 11, BOLD), pady=5, bg='#384850', fg='#f8f8f8').pack(fill='x')
        
        # Title entry
        titleLabel = Label(self.note_modal, text='Title',font=(font_family, 10, BOLD), fg='#f8f8f8', bg='#384850', bd=0, padx=34)
        titleLabel.place(x=58,y=50, height=30) #+35
        titleEntry = Entry(self.note_modal, width=45, bd=0, textvariable=title)
        titleEntry.place(x=155, y=50, height=30) #+35

        # Command entry
        titleLabel = Label(self.note_modal, text='Command',font=(font_family, 10, BOLD), fg='#f8f8f8', bg='#384850', bd=0, padx=15)
        titleLabel.place(x=58,y=95, height=30) #+35
        commandEntry = Entry(self.note_modal, width=45, bd=0, textvariable=command)
        commandEntry.place(x=155, y=95, height=30) #+35

        # Description entry
        titleLabel = Label(self.note_modal, text='Description',font=(font_family, 10, BOLD), fg='#f8f8f8', bg='#384850', bd=0, padx=13)
        titleLabel.place(x=57,y=140, height=30) #+35
        descEntry = Text(self.note_modal, width=34, bd=0)
        descEntry.place(x=155, y=140, height=100) #+35

        submit = Button(self.note_modal, text='Update', bd=0, font=(font_family, 8, BOLD), padx=5, bg='#384850', fg='#f8f8f8', cursor='hand2', command=lambda:self.update_note(self.current_nav_id, note_id, title.get(), command.get(), descEntry.get("1.0",'end-1c')))
        submit.place(x=185, y=255, width= 145, height=30)

        toBe_update_note = self.cursor.execute("SELECT * FROM contents WHERE id = ?", [note_id]).fetchone()
        title.set(toBe_update_note[2])
        command.set(toBe_update_note[3])
        descEntry.insert(0.0, toBe_update_note[4])
    
    def add_document(self):
        title = StringVar()
        self.content_old_frame.destroy()
        self.remove_modal.destroy()
        self.note_modal.destroy()

        if self.doc_modal: self.doc_modal.destroy()

        self.doc_modal = Frame(self.contentFrame, width=350, height=120, bg='#f2f2fd')
        self.doc_modal.place(x=185, y=167)
        self.doc_modal.pack_propagate(False)
        Label(self.doc_modal, text='Choose document title', font=(font_family, 11, BOLD), pady=5, bg='#384850', fg='#f8f8f8').pack(fill='x')
        
        titleEntry = Entry(self.doc_modal, width=40, bd=0, justify=CENTER, textvariable= title)
        titleEntry.place(x=55, y=50, height=20)
        
        submit = Button(self.doc_modal, text='Create', bd=0, font=(font_family, 10, BOLD), padx=5, pady=2, bg='#384850', fg='#f8f8f8', cursor='hand2', command=lambda:self.insert_document(title))
        submit.place(x=120, y=85, width=110)

    def delete_document(self):
        self.content_old_frame.destroy()
        self.note_modal.destroy()
        self.doc_modal.destroy()
        if self.remove_modal: self.remove_modal.destroy()

        if self.current_nav_id != 0:
            selected_nav_title = self.cursor.execute("SELECT title FROM documents WHERE id = ?", [self.current_nav_id]).fetchone()

            self.remove_modal = Frame(self.contentFrame, width=350, height=120, bg='#f2f2fd')
            self.remove_modal.place(x=185, y=167)
            self.remove_modal.pack_propagate(False)
            
            Label(self.remove_modal, text='Delete ' + selected_nav_title[0] + ' document?' , font=(font_family, 11, BOLD), pady=5, bg='#384850', fg='#f8f8f8').pack(fill='x')
            Label(self.remove_modal, text='This action also includes removing all the related notes', fg='#384850', bg='#f2f2fd', pady=10).pack(fill=X)
            submit = Button(self.remove_modal, text='Delete', bd=0, font=(font_family, 10, BOLD), pady=2, bg='#384850', fg='#f8f8f8', cursor='hand2', command= self.remove_document)
            submit.place(x=120, y=85, width=110)


    # Page 2 SQL Query functions
    def insert_note(self, doc_id, title, command, description):
        with self.conn:
            self.cursor.execute("INSERT INTO contents (doc_id, title, command, description) VALUES(?,?,?,?)", (doc_id, title, command, description))
        self.note_modal.destroy()
        self.fill_contnet(doc_id)

    def update_note(self, doc_id, note_id, title, command, description):
        with self.conn:
            self.cursor.execute("UPDATE contents SET title=?, command=?, description=? WHERE id=? ", (title, command, description, note_id))
        self.note_modal.destroy()
        self.fill_contnet(doc_id)

    def delete_note(self, note_id):
        with self.conn:
            self.cursor.execute("DELETE FROM contents WHERE id = ?", [note_id])
        self.fill_contnet(self.current_nav_id)

    def insert_document(self, title):
        with self.conn:
            self.cursor.execute("INSERT INTO documents (title) VALUES(?)", [title.get()])
        self.init_navList()
        self.doc_modal.destroy()

    def inst(self, title):
        with self.conn:
            self.cursor.execute("INSERT INTO documents (title) VALUES(?)", [title])

    def remove_document(self):
        self.note_modal.destroy()
        with self.conn:
            self.cursor.execute("DELETE FROM documents WHERE id = ?", [self.current_nav_id])
            self.cursor.execute("DELETE FROM contents WHERE doc_id = ?", [self.current_nav_id])
        self.current_nav_id = 0
        self.content_old_frame.destroy()
        self.remove_modal.destroy()
        self.init_navList()

    def insert_project(self, dirName, pathName):
        with self.conn:
            self.cursor.execute("INSERT INTO projects (dirName, pathName) VALUES(?,?)", (dirName, pathName))




if __name__ == '__main__':
    root = Tk()
    app = App(root)
    root.mainloop()