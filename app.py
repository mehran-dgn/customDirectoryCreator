import tkinter as tk  
from tkinter import filedialog, messagebox  
import os  
import shutil  
import win32clipboard  


rootDirectory = ""
try:
    with open("usedDirectories.txt", "r") as f:
        saved_directory = f.readline().strip()
        if saved_directory:
            rootDirectory = saved_directory
            print(f"Loaded base directory: {rootDirectory}")
except FileNotFoundError:
    print("No saved directory found")


createdFolder = ""  
optionalDesc = ""
canSubmit = False   



def checkBaseDirectory():
    global rootDirectory
    try:
        with open("usedDirectories.txt", "r") as f:
            first_directory = f.readline().strip()
            if first_directory:
                rootDirectory = first_directory
                return True
    except FileNotFoundError:
        messagebox.showwarning("هشدار", "لطفا یک مسیر پایه را انتخاب کنید")
        return False
    return False

def askUserToChooseRootDir():
    global rootDirectory
    selected_directory = filedialog.askdirectory()
    
    if selected_directory:
        rootDirectory = selected_directory
        with open("usedDirectories.txt", "w") as f:
            f.write(f"{rootDirectory}")
        print(f"Selected root directory: {rootDirectory}")

def createFolder():  
    global createdFolder 
    global canSubmit 
    
    if not rootDirectory:
        messagebox.showwarning("هشدار", "لطفا ابتدا مسیر پایه را انتخاب کنید")
        return
        
    baseDir = rootDirectory  
    createdFolder = fileNameInput.get()  
    canSubmit = True 

    if createdFolder and canSubmit == True:  
        finalDirectory = os.path.join(baseDir, createdFolder)  
        try:  
            os.mkdir(finalDirectory)  
            print(f"Directory '{finalDirectory}' created successfully.")    
            createdFolder = finalDirectory  
        except FileExistsError:  
            error_message = "مشکلی پیش آمده است، بررسی کنید پوشه ای با این نام قبلاً ساخته نشده باشد"  
            messagebox.showerror("Error", error_message) 
        except Exception as e:  
            messagebox.showerror("Error", str(e))
 

def pasteFromClipboard():  
    global rootDirectory, createdFolder  
    global canSubmit
    global optionalDesc
    isSubmitted = False
    if not rootDirectory or not createdFolder:
        messagebox.showwarning("هشدار", "لطفا ابتدا مسیر و پوشه را ایجاد کنید")
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
                            isSubmitted = True 
                            canSubmit = False 

                            
                        except Exception as e:  
                            messagebox.showerror("خطا", f"Failed to copy {file_path}: {str(e)}")  
                    else:  
                        messagebox.showwarning("هشدار", f"{file_path} is not a valid image file.")  
                else:  
                    messagebox.showwarning("هشدار", f"{file_path} is not a valid file path in clipboard.")  

        else:  
            messagebox.showwarning("هشدار", "The clipboard does not contain file paths.")  

    except Exception as e:  
        messagebox.showerror("خطا", f"Failed to read the clipboard: {str(e)}")  
    finally:  
        win32clipboard.CloseClipboard()  
        createdFolder = "" 
        optionalDesc = "" 
        if isSubmitted:
            fileNameInput.delete(0, tk.END)
            submitOptionalDesc.delete(0, tk.END)
            messagebox.showinfo("پیام نرم افزار","انتقال فایل ها با موفقیت انجام شد")



def submitPerson():
    global optionalDesc
    global createdFolder
    if not rootDirectory or not createdFolder:
        messagebox.showerror("خطا","لطفا ابتدا مسیر و پوشه را ایجاد کنید")
        return
        
    optionalDesc = str(submitOptionalDesc.get())
    directoryToSaveNote = os.path.join(rootDirectory, createdFolder)
    file = open(f"{directoryToSaveNote}/details.txt","w")
    file.write(f"{optionalDesc}")
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

optionalDesc = tk.Label(mainFrame, text=":توضیحات")
optionalDesc.grid(row=3, column=2, sticky="ew")

submitOptionalDesc = tk.Entry(mainFrame)
submitOptionalDesc.grid(row=3, column=1, sticky="ew")

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