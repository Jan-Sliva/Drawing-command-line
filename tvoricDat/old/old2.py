from tkinter import *
from tkinter.ttk import Scale
from tkinter import colorchooser,filedialog,messagebox
import PIL.ImageGrab as ImageGrab


lX, lY = None, None

#Defining Class and constructor of the Program
class Draw():
    def __init__(self,root):

        self.root = root
        self.root.title("Copy Assignment Painter")
        self.root.geometry("500x500")
        self.root.configure(background="white")

        self.background = Canvas(self.root,bg='white',height=500,width=500)
        self.background.place(x=0,y=0)


        self.background.bind("<B1-Motion>",self.paint)
        self.background.bind("<Button-1>",self.penUp)
        self.background.bind("<Button-3>",self.rightButton)

    def penUp(self, event):
        global lX, lY
        print("Left Button")
        lX, lY = None, None

    def rightButton(self, event):
        print("Right Button")

    def paint(self,event):
        global lX, lY

        if (lX is None):
            lX = event.x
            lY = event.y
            return

        self.background.create_line(lX,lY,event.x,event.y,fill="black",width=2)
        lX = event.x
        lY = event.y

    

if __name__ =="__main__":
    root = Tk()
    p= Draw(root)
    root.mainloop()