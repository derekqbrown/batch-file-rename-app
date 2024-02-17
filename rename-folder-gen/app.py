# app to rename files in a folder sequentially using the name of the folder
from tkinter import *
import os
from tkinter import messagebox
import random
from mutagen.easyid3 import EasyID3
from tkinter.filedialog import askdirectory


# this closes the program
def close():
    prompt = messagebox.askyesno("Close Program?",
                                 "Do you want to close the program?")
    if not prompt:
        return
    exit()


class App:
    def __init__(self, window):
        window.title('Batch file renamer')
        Label(window, text="Batch file renamer", font=('bold', 15)).pack()
        frame = Frame(window, width=360, height=250)
        frame.pack()

        Button(window, text='Browse...', command=lambda: self.browse()).place(x=251, y=50)
        Button(window, text='Close', command=lambda: close()).place(x=269, y=200)
        Button(window, text='Use Folder Name', command=lambda: self.rename()).place(x=50, y=100)
        Button(window, text='Randomize Names', command=lambda: self.randomize()).place(x=50, y=150)
        Button(window, text='Folder Batch', command=lambda: self.folder_batch()).place(x=175, y=100)
        Button(window, text='Random Batch', command=lambda: self.random_batch()).place(x=175, y=150)

        self.selected_folder = Entry(window, width=30)
        self.selected_folder.place(x=50, y=54)
        self.selected_folder.insert(0, "Select a folder")
        self.status_txt = Label(window, foreground='red')
        self.status_txt.config(text="Hello there!")
        self.status_txt.pack()

    # This allows the user to select a folder in Windows Explorer
    def browse(self):
        try:
            selection = askdirectory()
            self.selected_folder.delete(0, END)
            self.selected_folder.insert(0, selection)
        except:
            self.error_report()

    # This warns the user that the operation attempted was not successful
    def error_report(self):
        self.status_txt.config(text="Error! Something went wrong...")

    def folder_batch(self):
        folder = self.selected_folder.get().replace('\\', '/')
        for subfolder in os.listdir(folder):
            filename = os.path.join(folder, subfolder).replace('\\', '/')
            self.selected_folder.delete(0, END)
            self.selected_folder.insert(0, filename)
            self.rename()

    def random_batch(self):
        folder = self.selected_folder.get().replace('\\', '/')
        for subfolder in os.listdir(folder):
            filename = os.path.join(folder, subfolder).replace('\\', '/')
            self.selected_folder.delete(0, END)
            self.selected_folder.insert(0, filename)
            self.randomize()

    # renames the files in a folder based on the folder name (e.g. "folder - 01", "folder - 02")
    def rename(self):
        folder = self.selected_folder.get().replace('\\', '/')
        prompt = messagebox.askyesno("Rename these files?",
                                     "Do you wish to rename these "
                                     "files in the folder \n[" + folder.split('/')[-1] +
                                     "]?\nThis cannot be undone")
        if not prompt:
            return
        if not os.path.exists(folder):
            self.status_txt.config(text="Folder could not be found. Please select a folder")
            return
        i = 0
        for file in os.listdir(folder):
            filename = os.path.join(folder, file)

            foldername = folder.split('/')[-1]
            filetype = file.split('.')[-1]
            dest = folder + "/" + foldername + " - " + str(i) + "." + filetype
            os.rename(filename, dest)
            i = i+1
            self.status_txt.config(text="Success!")

    # this randomizes file names using data from the .txt files in the 'resources' folder
    def randomize(self):
        folder = self.selected_folder.get().replace('\\', '/')
        prompt = messagebox.askyesno("Randomize these files?",
                                     "Do you wish to randomize these "
                                     "file names in the folder \n[" + folder.split('/')[-1] +
                                     "]?\nThis cannot be undone!")
        if not prompt:
            return

        if not os.path.exists(folder):
            self.status_txt.config(text="Folder could not be found. Please select a folder")
            return
        with open("resources/adj.txt", 'r+') as temp_file:
            adj_list = temp_file.readlines()
        with open("resources/items.txt", 'r+') as temp_file:
            items_list = temp_file.readlines()
        with open("resources/noun.txt", 'r+') as temp_file:
            noun_list = temp_file.readlines()

        i = 1

        for file in os.listdir(folder):
            filename = os.path.join(folder, file)
            filetype = file.split('.')[-1]

            adj = random.choice(adj_list).replace('\n', '')
            item = random.choice(items_list).replace('\n', '')
            noun = random.choice(noun_list).replace('\n', '')
            rand_num = random.choice([1, 2, 3, 4, 5])

            # this generates a random name
            if rand_num == 5:
                if 'the ' in noun[0:4]:
                    new_name = item + " of the " + adj + " " + noun[4:]
                else:
                    new_name = item + " of " + adj + " " + noun.replace('the ', '')
            elif rand_num == 4:
                new_name = adj + " " + item + " of " + noun
            elif rand_num == 3:
                new_name = item + " of " + noun
            elif rand_num == 2:
                if 'the ' in noun[0:4]:
                    new_name = item + " of the " + adj + " " + noun[4:]
                else:
                    new_name = adj + " " + noun.replace('the ', '')
            else:
                new_name = adj + " " + item

            #  This allows editing of metadata
            if filetype in ['.mp3', 'mp3']:
                audio = EasyID3(filename)
                audio['title'] = u"" + new_name
                audio.save()

            new_name = folder + "/" + new_name + " " + str(i) + "." + filetype

            os.rename(filename, new_name)

            i += 1
            self.status_txt.config(text="Success!")


# these lines of code create the window for the UI
fenster = Tk()
fenster.eval('tk::PlaceWindow . center')
fenster.resizable()
app = App(fenster)

fenster.mainloop()
