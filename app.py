from functions import createFolder
from tkinter import filedialog
import tkinter as tk 


root = tk.Tk()
root.title("نرم افزار مدیریت مدارک")
root.geometry("400x300")

directory_label = tk.Label(root,text=":مسیر انتخاب شده")
directory_label.pack(side="right")


folderNameInput = tk.Text(root , height = 5 , width=20)
folderNameInput.pack()

printButton = tk.Button(root,text="print" , command=lambda: createFolder(createFolder.get("1.0","end-1c")))
printButton.pack()

root.mainloop()