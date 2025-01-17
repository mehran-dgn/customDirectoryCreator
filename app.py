import tkinter as tk  
from tkinter import filedialog, messagebox  
import os  
import shutil  
import win32clipboard  

rootDirectory = ""  
createdFolder = ""  
whoIsThisForVal = ""

def askUserToChooseRootDir():  
    global rootDirectory  
    rootDirectory = filedialog.askdirectory()  
    print(f"Selected root directory: {rootDirectory}")  

def createFolder():  
    global createdFolder  
    baseDir = rootDirectory  
    createdFolder = fileNameInput.get()  

    if createdFolder:  
        finalDirectory = os.path.join(baseDir, createdFolder)  
        try:  
            os.mkdir(finalDirectory)  
            print(f"Directory '{finalDirectory}' created successfully.")    
            createdFolder = finalDirectory  
            # fileNameInput.delete(0, tk.END)
        except FileExistsError:  
            error_message = "مشکلی پیش آمده است، بررسی کنید پوشه ای با این نام قبلاً ساخته نشده باشد"  
            messagebox.showerror("Error", error_message) 
        except Exception as e:  
            messagebox.showerror("Error", str(e))    

def pasteFromClipboard():  
    global rootDirectory, createdFolder  

    if not createdFolder:  
        messagebox.showwarning("Warning", "Please create a folder first.")  
        return  

    try:  
        win32clipboard.OpenClipboard()  
        if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_HDROP):  
            file_list = win32clipboard.GetClipboardData(win32clipboard.CF_HDROP)
            print(f"Files in clipboard: {file_list}")  
            for file_path in file_list:  
                print(f"Processing file: {file_path}")  
                if os.path.isfile(file_path):  
                    if file_path.lower().endswith(('.jpg', '.jpeg', '.png')): 
                        try:  
                            shutil.copy(file_path, createdFolder)  
                            print(f"Copied {file_path} to {createdFolder}.")  
                            
                        except Exception as e:  
                            messagebox.showerror("Error", f"Failed to copy {file_path}: {str(e)}")  
                    else:  
                        messagebox.showwarning("Warning", f"{file_path} is not a valid image file.")  
                else:  
                    messagebox.showwarning("Warning", f"{file_path} is not a valid file path in clipboard.")  

        else:  
            messagebox.showwarning("Warning", "The clipboard does not contain file paths.")  

    except Exception as e:  
        messagebox.showerror("Error", f"Failed to read the clipboard: {str(e)}")  
    finally:  
        win32clipboard.CloseClipboard()  
        createdFolder = ""  


def submitPerson():
    global whoIsThisForVal
    whoIsThisForVal = str(submitWhoIsThisFor.get())
    print("shittt")
    directoryToSaveNote =  os.path.join(rootDirectory, createdFolder)  
    file = open(f"{directoryToSaveNote}/details.txt","w")
    print(whoIsThisForVal)
    file.write(f"شماره به نام : {whoIsThisForVal}")
    file.close()

root = tk.Tk()  
root.geometry("340x150")  
root.title("نرم افزار مدیریت و ساخت پوشه ها")  

mainFrame = tk.Frame(root)  
mainFrame.grid(row=0, column=0, sticky="nsew")  


lbl1 = tk.Label(mainFrame, text=":مسیر ذخیره سازی را انتخاب کنید")  
lbl1.grid(row=0, column=1, sticky="ew")  

chooseDirBtn = tk.Button(mainFrame, text="انتخاب", command=askUserToChooseRootDir, width=5)  
chooseDirBtn.grid(row=0, column=0, sticky="ew")  

fileNameLabel = tk.Label(mainFrame, text=":نام فایل را وارد کنید")  
fileNameLabel.grid(row=1, column=1, sticky="ew")  

fileNameInput = tk.Entry(mainFrame)  
fileNameInput.grid(row=1, column=0, sticky="ew")  

createFolderBtn = tk.Button(mainFrame, text="ایجاد پوشه", command=createFolder)  
createFolderBtn.grid(row=2, column=0, sticky="ew")  

whoIsThisFor = tk.Label(mainFrame, text=":به نام")
whoIsThisFor.grid(row=3, column=2, sticky="ew")

submitWhoIsThisFor = tk.Entry(mainFrame)
submitWhoIsThisFor.grid(row=3, column=1, sticky="ew")

pasteButton = tk.Button(mainFrame, text="ثبت", command=submitPerson)  
pasteButton.grid(row=3, column=0, sticky="ew")  


pasteButton = tk.Button(mainFrame, text="چسباندن از کلیپ بورد", command=pasteFromClipboard)  
pasteButton.grid(row=4, column=0, sticky="ew")  


root.grid_rowconfigure(0, weight=1)  
root.grid_columnconfigure(0, weight=1)  
mainFrame.grid_rowconfigure(0, weight=1)  
mainFrame.grid_columnconfigure(0, weight=1)  
mainFrame.grid_columnconfigure(1, weight=1)  

mainFrame.pack()  

root.mainloop()