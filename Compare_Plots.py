from PIL import Image, ImageTk, ImageChops, ImageFile
from tkinter import Tk, BOTH, Text, INSERT, END, Listbox, ANCHOR
from tkinter import messagebox as mbox
from tkinter.ttk import Frame, Label, Style, Button, Entry
import os

class Window(Frame):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):
        """
        Function defines basic layout of whole program.
        """

        # Start instances atributes
        self.master.title("Image Compare")
        self.pack(fill=BOTH, expand=1)
        self.listOfPaths = []
        self.lenght = 0
        self.i = 0
        self.directory1 = "C:\\Plots1"
        self.directory2 = "C:\\Plots2"

        Style().configure("TFrame", background="#333")

        # Defining of entry and text fields
        self.path1 = Entry(self, width=50)
        self.path1.place(x=10, y=10)

        self.path2 = Entry(self, width=50)
        self.path2.place(x=10, y=35)

        self.startFromEntry = Entry(self)
        self.startFromEntry.place(x=450, y=10)

        self.plot1PathText = Text(self, height=3, width=75)
        self.plot1PathText.place(x=620, y=670)

        self.plot2PathText = Text(self, height=3, width=75)
        self.plot2PathText.place(x=1230, y=670)

        self.lb = Listbox(self, height=15, width=100)
        self.lb.place(x=620, y=740)

        # Defining buttons
        previousButton = Button(self, text="Previous", command=
                                self.previousButtonFunction)
        previousButton.place(x=10, y=670)

        nextButton = Button(self, text="Next", command=self.nextButtonFunction)
        nextButton.place(x=100, y=670)

        differentButton = Button(self, text="Different", command=
                                 self.differentButtonFunction)
        differentButton.place(x=300, y=670)

        deleteButton = Button(self, text="Delete", command=
                                         self.deleteButtonFunction)
        deleteButton.place(x=380, y=670)

        getPathButton = Button(self, text="Get Path", command=
                               self.get_filepaths)
        getPathButton.place(x=350, y=8)

        startFromButton = Button(self, text="Start From", command=
                                 self.startFromButtonFunction)
        startFromButton.place(x=600, y=8)

    def onError(self):
        string = self.listOfPaths[self.i]
        string = string.replace(self.directory1, self.directory2)
        mbox.showerror("Error", "There is no plot {}".format(string))

    def onError2(self):
        mbox.showerror("Error", "The same paths")

    def onLastPicture(self):
        mbox.showinfo("Last plot", "That is the last plot.")

    def onFirstPicture(self):
        mbox.showinfo("First plot", "That is the first plot.")

    def deleteButtonFunction(self):
        result = mbox.askquestion("Delete", "Are You Sure?", icon='warning')
        if result == 'yes':
            self.lb.delete(ANCHOR)
        else:
            return None

    def startFromButtonFunction(self):
        """
        Functionality startFromButton, from which chart program is starting.
        """
        # Get value from entry
        a = int(self.startFromEntry.get()) - 1
        # Check if value is proper
        if a < 0 or a >= self.lenght:
            print("Wrong number")
        else:
            self.i = a
            self.picture(self.i)

    def nextButtonFunction(self):
        """
        Functionality nextButton, next picture is choosen.
        """
        if self.i == self.lenght - 1:
            self.onLastPicture()
        else:
            self.i += 1
            self.picture(self.i)

    def previousButtonFunction(self):
        """
        Functionality previousButton, previousPicture picture is choosen.
        """
        if self.i == 0:
            self.onFirstPicture()
        else:
            self.i -= 1
            self.picture(self.i)

    def differentButtonFunction(self):
        adr = self.listOfPaths[self.i]
        self.addToListbox(adr)

    def addToListbox(self, adr):
        try:
            if adr in self.lb.get(0, END):
                return None
            else:
                self.lb.insert(0, adr)
        except TypeError:
            self.lb.insert(0, adr)

    def picture(self, adr):
        """
        This function creates three lables with pictures, first label show
        differences between pictures in next two labels.
        """
        adress_1 = self.listOfPaths[adr]
        adress_2 = adress_1.replace(self.directory1, self.directory2)

        file_img1 = Image.open(adress_1)
        try:
            file_img2 = Image.open(adress_2)
        except FileNotFoundError:
            adr = self.listOfPaths[self.i]
            self.addToListbox(adr)
            self.onError()
            return None

        self.fill_text_fields(adress_1, adress_2)
        diff = ImageChops.difference(file_img1, file_img2)
        diff = diff.resize((600, 600))
        diffjov = ImageTk.PhotoImage(diff)
        label1 = Label(self, image=diffjov)
        label1.image = diffjov
        label1.place(x=10, y=60)

        file_img1 = file_img1.resize((600, 600))
        image_2 = ImageTk.PhotoImage(file_img1)
        label2 = Label(self, image=image_2)
        label2.image = image_2
        label2.place(x=620, y=60)

        file_img2 = file_img2.resize((600, 600))
        image_3 = ImageTk.PhotoImage(file_img2)
        label3 = Label(self, image=image_3)
        label3.image = image_3
        label3.place(x=1230, y=60)

    def fill_text_fields(self, adr_1, adr_2):
        self.plot1PathText.config(state="normal")
        self.plot1PathText.delete("1.0", END)
        self.plot1PathText.insert(INSERT, adr_1)
        self.plot1PathText.config(state="disabled")

        self.plot2PathText.config(state="normal")
        self.plot2PathText.delete("1.0", END)
        self.plot2PathText.insert(INSERT, adr_2)
        self.plot1PathText.config(state="disabled")


    def get_filepaths(self):
        """
        This function will generate the file names in a directory
        tree by walking the tree either top-down or bottom-up. For each
        directory in the tree rooted at directory top (including top itself),
        it yields a 3-tuple (dirpath, dirnames, filenames).
        """
        self.directory1 = self.path1.get()
        self.directory2 = self.path2.get()
        if self.directory1 == self.directory2:
            self.onError2()
            return None

        file_paths = [] # List which will store all of the full filepaths.
        self.i = 0

        # Walk the tree.
        for root, directories, files in os.walk(self.directory1):
            for filename in files:
                # Join the two strings in order to form the full filepath.
                filepath = os.path.join(root, filename)
                file_paths.append(filepath) # Add it to the list.

        self.listOfPaths = file_paths
        self.lenght = len(file_paths)
        self.picture(self.i)
        print(self.lenght)

def main():

    root = Tk()
    root.geometry("1920x1080+0+0")
    app = Window()

    def onExit():
        if mbox.askyesno("Exit", "Do you want to quit the application?"):
            root.destroy()

    root.protocol("WM_DELETE_WINDOW", onExit)
    root.mainloop()
    


if __name__ == '__main__':
    main()
