# from tkinter import ttk
import tkinter as tk
from tkinter import ttk, filedialog, messagebox 
from tkcalendar import DateEntry
from datetime import datetime, timedelta, date
from time import strptime, struct_time, localtime
import PIL.Image
import PIL.ImageTk
import os.path
import os

# Failed tech messages 
# import os
import sys
import fileinput
import shutil 



# *************************** File Parser *****************************************************

class FailedMessage:

    """
    A class that can read Teach any where messages and orgabize them according to their
    Column name.
    """
    def __init__(self, fileName):
        
        # Descriptive attributes
        self.fileName = fileName
        self.lineCount = None
        self.describe = None
        self.raw = None
        

        if self.lineCount == None and self.describe == None and self.raw == None:
            self.parse_file()

    def parse_file(self):
    
        with open(self.fileName,'r') as f:
            content = f.readlines()
            content = [x.strip() for x in content]

        # record Legend:
        # 
        #  H = header
        #  HD = header columns
        #  L = List Header
        #  LD = List details
        #  LN = Aditional List Header
        #  LDN = Aditional List Details
        #  p1 = ")"
        #  p2 = "()"
        #  p3 = "("
        #  p4 = "(" + string  -> Where leng is > 2
        #  p5 = string + ")"  -> Where leng is > 2
   
        columHeadings = False

        perenCheck = False

        openPeren, openAndClosePeren, closePeren = "(", "()", ")"
        
        template = []
        record = template.copy()

        # Map the Contents
        for line in content:

            # Root Case:
            if line.endswith("headings->") or columHeadings:

                if not columHeadings:
                    record.append("HEADER")
                    columHeadings = True 
                    perenCheck  = False
              
                # if Header Marker or the  Header Description
                elif not line.endswith("headings->") and columHeadings:
                    
                    columHeadings = False
                    record.append("HEADER COLUMNS")

            # List Case:
            elif line.endswith("list->") or line.endswith("list   ->") or perenCheck:
     
                if not perenCheck:
                    record.append("LISTINGS")
                    perenCheck = True
                    
                elif len(line) == 1 and line == openPeren:
                    record.append("OPEN PEREN")
                    perenCheck = True

                elif len(line) == 1 and line == closePeren:
                    record.append("CLOSE PEREN")
                    perenCheck = False
                          
                else:

                    if len(line) == 2 and line == openAndClosePeren:
                        record.append("NO DATA")
                        perenCheck = False
                    
                    elif len(line) > 2 and line[0] == openPeren and line[-1] == closePeren:
                        record.append("DATA EXISTS")
                        perenCheck = True
                                           
                    else:
                        record.append("ERROR READING DATA")

            else: 
                
                record.append(line)

        # Count Lines in file.
        contentLength = len(content)

        # return FailedMessage(contentLength,record,content)

        self.lineCount = contentLength
        self.describe = record
        self.raw = content

        pass

    pass

# ***************************** GUI ***********************************************************

class App():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("2020 Script Runner Version: 1")
        self.root.geometry(f"850x850+{self.root.winfo_x()}+{self.root.winfo_y()}")
        self.root['background'] = "#4E4187"
        self.frame_dir = tk.Frame(self.root, padx=40, pady=40, bg="#4E4187",relief=tk.SUNKEN)

        default_dir = "Q:\\Sampro\\techAnywhere"

        # self.img = ImageTk.PhotoImage(Image.open(r'icons\runner.png'))
        self.im = PIL.Image.open('runner.png')
        self.photo = PIL.ImageTk.PhotoImage(self.im)
        self.label = tk.Label(self.frame_dir, image=self.photo, bg="#4E4187",fg="#7DDE92")

        # Directory Frame 1 of 2
        self.tar_dir_lab = tk.StringVar(value=f"Default Directory ---- {default_dir} -----------------------------------")
        self.tar_dir = tk.StringVar(value=default_dir)

        self.lab1 = tk.Label(self.frame_dir, text="Target Directory:", bg="#4E4187",fg="#7DDE92",font=("Sans","13","bold"))
        self.btn1 = tk.Button(self.frame_dir, text="Browse", width=len("Target Directory"),command=self.targetDir_browse)
        self.entry = tk.Entry(self.frame_dir,width=70,textvariable = self.tar_dir_lab, state="readonly",font=("Sans","13","italic"))

        # Directory Frame 2 of 2
        self.bk_dir = tk.StringVar(value='')
        self.bk_dir_lab = tk.StringVar(value=" ---------------------------------- Default Value is None ---------------------------------------")
        self.bk_dir_req = tk.BooleanVar(value=False)
        
        self.lab2 = tk.Label(self.frame_dir, text="Backup Directory:", bg="#4E4187",fg="#7DDE92",font=("Sans","13","bold"))
        self.btn2 = tk.Button(self.frame_dir, text="Browse", width=len("Target Directory"),command=self.backUpDir_browse,state="disabled")
        self.entry2 = tk.Entry(self.frame_dir,width=70,textvariable = self.bk_dir_lab, state="readonly",font=("Sans","13","italic"))
        self.radio_btn_false1 = tk.Radiobutton(self.frame_dir, value=False, text="No",variable=self.bk_dir_req, bg="#4E4187",font=("Sans","12","bold"),command=self.getbk)
        self.radio_btn_True1 = tk.Radiobutton(self.frame_dir, value=True, text="Yes",variable=self.bk_dir_req,bg="#4E4187",font=("Sans","12","bold"),command=self.getbk)
        self.lab3 = tk.Label(self.frame_dir, text="Note: Select Yes, to backup all original files.", bg="#4E4187",fg="#7DDE92",font=("Aharoni","11","bold"))
        
        # Date Frame
        self.date_dir_req = tk.BooleanVar(value=False)

        self.lab4 = tk.Label(self.frame_dir, text="Delete Dates Outside this Range (Excluesive Start Date & Inclusive End Date):", bg="#4E4187",fg="#7DDE92",font=("Sans","13","bold"))
        self.lab5 = tk.Label(self.frame_dir, text="Start Date", bg="#4E4187",fg="#7DDE92",font=("Sans","13","bold"))
        self.lab6 = tk.Label(self.frame_dir, text="End Date", bg="#4E4187",fg="#7DDE92",font=("Sans","13","bold"))
        self.dEntry1 = DateEntry(self.frame_dir,fieldbackground='red',width=20,state="disabled",font=("Sans","10","bold"),date_pattern="dd/mm/yy")
        self.dEntry2 = DateEntry(self.frame_dir,fieldbackground='red',width=20,state="disabled",font=("Sans","10","bold"),date_pattern="dd/mm/yy")
        self.lab7 = tk.Label(self.frame_dir, text="Note: Select Yes, to activate the filter.", bg="#4E4187",fg="#7DDE92",font=("Aharoni","11","bold"))
        self.radio_btn_false2 = tk.Radiobutton(self.frame_dir, value=False, text="No",variable=self.date_dir_req, bg="#4E4187",font=("Sans","12","bold"),command=self.getDateEntry)
        self.radio_btn_True2 = tk.Radiobutton(self.frame_dir, value=True, text="Yes",variable=self.date_dir_req,bg="#4E4187",font=("Sans","12","bold"),command=self.getDateEntry )

        # Execute Frame
        self.btn3 = tk.Button(self.frame_dir, text="Execute", width=10,height=5,bg="#E09558",fg="#4E4187",font=("Goudy Stout","13","bold"), relief=tk.RAISED,command = self.execute)

        # pack excute
        self.btn3.grid(row=10,column=0,columnspan=3,padx=(30,30),pady=(30,30),sticky='NSEW')

        # Pack Date Frame
        self.radio_btn_false2.grid(row=9,column=1,padx=(361,0),pady=(0,0), sticky="W")
        self.radio_btn_True2.grid(row=9,column=1,padx=(411,0),pady=(0,0), sticky="W")
        self.lab7.grid(row=9,column=1,padx=(72,0),pady=(0,0), sticky="W")
        self.dEntry2.grid(row=8,column=1,padx=(0,168),pady=(0,0), sticky="E")
        self.dEntry1.grid(row=8,column=1,padx=(75,0),pady=(0,0), sticky="W")
        self.lab6.grid(row=7,column=1,padx=(0,175),pady=(0,0), sticky="E")
        self.lab5.grid(row=7,column=1,padx=(75,0),pady=(0,0), sticky="W")
        self.lab4.grid(row=6,column=0,columnspan=3,padx=(0,0),pady=(40,10), sticky="W")
        
        # pack dir 2
        self.lab3.grid(row=5,column=0,columnspan=2,padx=(0,0),pady=(0,0), sticky="W")
        self.radio_btn_false1.grid(row=5,column=1,padx=(200,0),pady=(0,0), sticky="W")
        self.radio_btn_True1.grid(row=5,column=1,padx=(250,0),pady=(0,0), sticky="W")
        self.entry2.grid(row=4,column=1,padx=(0,0),pady=(0,0))
        self.btn2.grid(row=4,column=0,padx=(0,0),pady=(0,0))
        self.lab2.grid(row=3,column=0,columnspan=3,padx=(0,0),pady=(40,10), sticky="W")

        # pack dir 1
        self.entry.grid(row=2,column=1,padx=(0,0),pady=(0,0))
        self.btn1.grid(row=2,column=0,padx=(0,0),pady=(0,0))
        self.lab1.grid(row=1,column=0,columnspan=3,padx=(0,0),pady=(30,10), sticky="W")

        self.label.grid(row=0,column=0,columnspan=3,padx=(0,0),pady=(30,10), sticky="NSEW")

        self.frame_dir.pack()
        self.root.mainloop()
    

    # Get & Check Target Direcrtory and set a Directory string to a string called "tar_dir".
    def targetDir_browse(self):
        a = filedialog.askdirectory()
        isdir = os.path.isdir(a)
        
        if len(a) == 0 or not isdir:
            self.tar_dir.set("C:/Users/justi/Desktop/filestofilter")
            self.tar_dir_lab.set(f"Default Directory ---- C:/Users/justi/Desktop/filestofilter-----------------------------------")
            if isdir == False and len(a) != 0:
                messagebox.showerror(title="WHOOPS", message=f"It appears that {str(a)} is unreachable. Ensure you have a valid connection to AFO network drives.",parent=self.frame_dir)
        else:
            self.tar_dir_lab.set(a)
            self.tar_dir.set(a) 

    # Determine if user needs a backup and check the users desired backup location. 
    def backUpDir_browse(self):
        a = filedialog.askdirectory()
        isdir = os.path.isdir(a)
        radio =  self.bk_dir_req.get()
        emptyPath = (len(a)==0)
        defaultTarget = "C:/Users/justi/Desktop/filestofilter"

        if radio:
            self.bk_dir_lab.set(f"Default Directory ---- C:/Users/justi/Desktop/filestofilter-----------------------------------")
            self.bk_dir.set(defaultTarget)

            if isdir and a != defaultTarget:
                self.bk_dir_lab.set(a)
                self.bk_dir.set(a)
            else:

                if emptyPath:
                    self.bk_dir_lab.set(f"Default Directory ---- C:/Users/justi/Desktop/filestofilter-----------------------------------")
                    self.bk_dir.set(defaultTarget)
                else:
                    messagebox.showerror(title="WHOOPS", message=f"It appears that {str(a)} is unreachable. Ensure you have a valid connection to AFO network drives.",parent=self.frame_dir)
                    self.btn2['state'] = "disabled"
                    self.bk_dir_req.set(False)
        else:
            self.bk_dir_lab.set(" ---------------------------------- Default Value is None ---------------------------------------")
            self.bk_dir.set("")
            self.btn2['state'] = "disabled"
            self.bk_dir_req.set(False)

    # Determine if user would like a back up directory via radio buttons
    def getbk(self):
        a = self.bk_dir_req.get()

        if a:
            self.btn2['state'] = "active"
            self.bk_dir_lab.set(f"Default Directory ---- C:/Users/justi/Desktop/filestofilter-----------------------------------")
            self.bk_dir.set("C:/Users/justi/Desktop/filestofilter")
        else:
            self.bk_dir_lab.set(" ---------------------------------- Default Value is None ---------------------------------------")
            self.btn2['state'] = "disabled"
            self.bk_dir.set("")
  
    # Check Dates for valid input
    def getDateEntry(self):

        a = self.date_dir_req.get()

        if a:
            self.dEntry1['state'] = 'active'
            self.dEntry2['state'] = 'active'

        else:
            self.dEntry1.delete(0, "end")
            self.dEntry2.delete(0, "end")
            self.dEntry1['state'] = 'disabled'
            self.dEntry2['state'] = 'disabled'

    
    def makeDir(self):

        pass

    def makeBackups(self):

        pass

    def check_start_end(self):
        val=False
        blank_time = " 00:00:00"
        d1_start = self.dEntry1.get()
        d2_end = self.dEntry2.get()
        day_start = datetime.strptime(f"{d1_start}{blank_time}", '%d/%m/%y %H:%M:%S')
        day_end = datetime.strptime(f"{d2_end}{blank_time}", '%d/%m/%y %H:%M:%S')

        if (day_end - day_start).days < 0:
            messagebox.showerror(title="WHOOPS", message=f"It appears that Start Date is greater than your End Date.",parent=self.frame_dir)
            
        elif (day_end - day_start).days <=0:
            messagebox.showerror(title="WHOOPS", message=f"It appears that Start Date is greater than your End Date.",parent=self.frame_dir)
        else:
            val = True
        return val

    
    def isDate(self):
        val1= False
        val2= False

        d1_str = self.dEntry1.get()
        d2_str = self.dEntry2.get()
        blank_time = " 00:00:00"

        d1_test = f"{d1_str}{blank_time}"
        d2_test = f"{d2_str}{blank_time}"
        
        try:
            d1t = (datetime.strptime(d1_test, '%d/%m/%y %H:%M:%S'))
            val1= True
        except ValueError:

            val1= False
        try:
            d2t = (datetime.strptime(d2_test, '%d/%m/%y %H:%M:%S'))
            val2= True
        except ValueError:
            
            val2= False
        
   
        
        if not val1 and not val2:
            messagebox.showerror(title="WHOOPS", message=f"It appears Both Dates you entered are incorect.",parent=self.frame_dir)
            return False
             
        elif val1 and not val2:
            messagebox.showerror(title="WHOOPS", message=f"It appears the END Date you entered is incorect.",parent=self.frame_dir)
            return False
        
        elif val2 and not val1:
            messagebox.showerror(title="WHOOPS", message=f"It appears the Start Date you entered is incorect.",parent=self.frame_dir)
            return False
        
        else:
            d1t = None
            d2t = None
            
            return True
    
    def execute(self):

        check_BK_DIR = False
        check_date_filter = False
        bk_path = None
        dates_to_protect = None

        
        # **************************** CASE BACKUP IS REQUIRED *************************


        if self.bk_dir.get():
            
            is_path_C_drive = self.bk_dir.get()[0:2] == "C:"

            if is_path_C_drive:

                check_BK_DIR = True

                pass

            else:
                
                recomendedPath = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
                MsgBox = messagebox.askquestion (title = "Unable to Save!!!",message=f'You do not have permissions to use this application to save in this directory\n\nWould you like to save in the recomended Directory?\n\n\n Recomended Directory: {recomendedPath}',parent=self.frame_dir)
                
                if MsgBox == 'yes':
                    self.bk_dir_lab.set(f"{recomendedPath}")
                    self.bk_dir.set(f"{recomendedPath}")
                    self.execute()

                else:
                    self.tar_dir_lab.set("Default Directory ---- C:/Users/justi/Desktop/filestofilter-----------------------------------")
                    self.tar_dir.set("C:/Users/justi/Desktop/filestofilter")
                    return

   
        if self.date_dir_req.get():

            if self.isDate():
                if self.check_start_end():
                    
                    check_date_filter = True
                    pass

                else:
                    return
            else:
                return
            
            pass


        if check_BK_DIR:

            parent_directory = self.bk_dir.get()

            todays_temp_date = datetime.now()
            year = todays_temp_date.strftime("%Y")
            month = todays_temp_date.strftime("%B")
            day = todays_temp_date.strftime("%d")

            folder_name = f"TAM_BACKUPS_{year}_{month}_{day}"
            bk_path = os.path.join(parent_directory,folder_name).replace("\\","/")

            try:  
                os.mkdir(bk_path)  
            except OSError:

                max = 9
                min = 1
                

                #  While loop that will help create a folder to save back ups.
                while min < max:
                    try:
                        copy_num = f"COPY_{min}"
                        folder_name = f"TAM_BACKUPS_{year}_{month}_{day}_{copy_num}"
                        bk_path = os.path.join(parent_directory,folder_name).replace("\\","/")
                        os.mkdir(bk_path)
                        min = min + 10
                    except OSError:
                        if min == 9:

                            return
            
                    min = min+1  
        

            pass


        # *****************  CASE DATES ***************************************


        # If Dates are required, create a list of all dates between the start and end Date.
        if check_date_filter:

            # Empty List to save dates
            dates_to_protect = []

            d1_str = self.dEntry1.get()
            d2_str = self.dEntry2.get()
            blank_time = " 00:00:00"

            d1_test = f"{d1_str}{blank_time}"
            d2_test = f"{d2_str}{blank_time}"


            # .replace("\\","/")

            d1t = (datetime.strptime(d1_test, '%d/%m/%y %H:%M:%S'))
            d2t = (datetime.strptime(d2_test, '%d/%m/%y %H:%M:%S'))

            days_between_dates = (d2t - d1t).days


            #  Make a list of date strings to locate.
            for new_day in range(days_between_dates):

                new_day = datetime.strftime((d1t + timedelta(new_day + 1)), "%Y/%m/%d").replace("/","-")

                dates_to_protect.append(new_day)


        #  ******************************* EXECUTE SCRIPT RUNNER FUNCTION ************************
        
        # Run Script to make a folder with backup and filter by date.
        if  check_BK_DIR and check_date_filter:

            self.runTechScript_01(target_path = self.tar_dir.get(), backup_path = bk_path, save_these_dates = dates_to_protect)

            return

        # Run Script to make a folder with backup and disregard all dates.
        elif check_BK_DIR and check_date_filter == False:

            self.runTechScript_01(target_path = self.tar_dir.get(), backup_path = bk_path, save_these_dates = None)

            return
        
        # Run Script, do not backup and disregard all dates.
        elif check_BK_DIR == False and check_date_filter == False:

            self.runTechScript_01(target_path = self.tar_dir.get(), backup_path = None, save_these_dates = None)

            return
    

    def runTechScript_01(self,target_path, backup_path=None, save_these_dates=None):

        mssg1 = ""
        mssg2 = ""
        mssg = ""
        files_ammended = 0

        total_files = 0

        dirList = []

        #  Iterate directory with txt files.
        for file in os.listdir(target_path):
            filename = os.fsdecode(file)
            
            if filename.endswith(".txt"):
                dirList.append(os.path.join(target_path, filename))

                total_files = total_files + 1
                continue
            else:
                continue


        objList = []
        if save_these_dates != None:

            date_str = ""

            #  Iterate filenames and create objects.
            for file in dirList:
                objList.append(FailedMessage(file))


            objIndex = 0

            for fileLoc in dirList:
                
                describeText = objList[objIndex].describe
                objDescribeLineIndex = 0

                with fileinput.FileInput(fileLoc, inplace = True, backup ='.bak') as f:

                    for line in f: 

                        if describeText[objDescribeLineIndex] != "DATA EXISTS":
                            print(line, end ='') 
                        
                        elif describeText[objDescribeLineIndex] == "DATA EXISTS" :

                            for _date in save_these_dates:

                                if _date in line:

                                    print(line, end ='') 

                                    if _date == save_these_dates[-1]:
                                        
                                        date_str = date_str + f" {_date}"
                                    
                                    elif _date == save_these_dates[0]:
                                        
                                        date_str = date_str + f"{_date},"

                                    else:

                                        date_str = date_str + f" {_date},"
                        else:
                            pass

                        files_ammended = files_ammended + 1
                        
                        objDescribeLineIndex += 1
                        
                objIndex += 1

                mssg1 = f"""A total of {files_ammended} files where ammended from the path: {target_path}. Files containg column dates have been left unedited. The range of dates are...\n{date_str}."""
        
        else:

            #  Iterate filenames and create objects.
            for file in dirList:
                objList.append(FailedMessage(file))

            objIndex = 0

            for fileLoc in dirList:
                
                describeText = objList[objIndex].describe
                objDescribeLineIndex = 0

                with fileinput.FileInput(fileLoc, inplace = True, backup ='.bak') as f:

                    for line in f: 

                        if describeText[objDescribeLineIndex] != "DATA EXISTS":
                            print(line, end ='') 

                        else:
                            pass
                        
                        objDescribeLineIndex += 1
                        
                objIndex += 1

            mssg1 = f"""A total of {files_ammended} files where ammended from the path: {target_path}."""

        
        if backup_path != None:

       
            files_BackedUP = 0

            for file in os.listdir(target_path):
                
                # filename = os.fsdecode(file)
            
                if file.endswith(".bak"):

                    try:
                        sourceFile = os.path.join(target_path,file)
                        shutil.move(sourceFile,backup_path)
                        
                        files_BackedUP = files_BackedUP + 1

                    except ValueError:

                        # failed_backups = failed_backups + 1
                        pass


                    

                    # dirList.append(os.path.join(target_path, filename))
                    continue
                else:
                    continue
            
            backup_path_corrected = backup_path.replace("/","\\")

            mssg2 = f"""\n{files_BackedUP} of {total_files} backup files have been placed in...\n{backup_path_corrected}\n"""

        else:

            pass
        
        mssg = f"{mssg1}{mssg2}"

        messagebox.showinfo(title = "Script Runner Has Made it to the Finish Line",message=mssg,parent=self.frame_dir)

        return



def main():

    root = App()

    return root


if __name__ == "__main__":
    main()




        

 






