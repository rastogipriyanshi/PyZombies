from tkinter import*
import tkinter.messagebox as tm
class Hello(Frame):
    def __init__(self,box):
        super().__init__(box)
    
        self.lbl1=Label(self,text="Email ID")
        self.lbl2=Label(self,text="Password")
        self.entry_1=Entry(self)
        self.entry_2=Entry(self,show="*")
        self.lbl1.grid(row=0)
        self.lbl2.grid(row=1)
        self.entry_1.grid(row=0,column=1,padx=10,pady=10)
        self.entry_2.grid(row=1,column=1,padx=10,pady=10)
        self.button1=Button(self,text="LOGIN",bg="light blue", fg="red",command=self.func)

        self.button1.grid(row=2,column=1,padx=7,pady=7)
        self.pack()

    def func(self):
        username=self.entry_1.get()
        password=self.entry_2.get()
        if(username=="priyanshi" and password=="priya"):
            tm.showinfo("Login Info","Welcome")
        else:
            tm.showerror("Login Error","Not registered")
root=Tk()
h=Hello(root)
root.minsize(300,150)
root.mainloop()
  
