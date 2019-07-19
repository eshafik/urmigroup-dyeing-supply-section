import sqlite3, datetime

from tkinter import *
from tkinter import ttk, messagebox

from database import Database
from myemail import EmailSend
from pdf import Pdf


class App(object):
    def __init__(self, master=Tk()):
        self.master = master
        # print("{} x {}".format(self.master.winfo_screenheight(), self.master.winfo_screenwidth()))
        self.master.title('FTML-Dyeing Section')
        self.master.geometry('500x200')

        # Menu Section

        self.menuBar = Menu(self.master)
        self.master.config(menu=self.menuBar)

        # File Menu
        self.fileMenu = Menu(self.master)
        self.menuBar.add_cascade(label='File', menu=self.fileMenu)
        self.fileMenu.add_command(label='Send Email', command=self.send_email)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Today's Data", command=self.todayData)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label='Exit', command=quit)

        # Help Menu
        self.helpMenu = Menu(self.master)
        self.menuBar.add_cascade(label='Help', menu=self.helpMenu)
        self.helpMenu.add_command(label='About me')

        # Machine Label
        self.m_c_l = Label(self.master, text='Select M/C:', font = 'Aria -13 bold')
        self.m_c_l.grid(row=0, column=0, padx=5)

        # Machine Selection
        self.m_number = StringVar()
        self.m_c_n = ttk.Combobox(self.master, textvariable=self.m_number, width=8)
        self.m_c_n.grid(row=0, column=1)
        self.m_c_n.config(values = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32'))
        self.m_c_n.current(0)

        # Batch Label
        self.b_l = Label(self.master, text='Batch:', font = 'Aria -13 bold')
        self.b_l.grid(row=0, column=2)

        # Batch Name Input
        self.batch = StringVar()
        self.b_n = Entry(self.master, textvariable=self.batch)
        self.b_n.grid(row=0, column=3)

        # Send Request Button
        self.b1 = Button(self.master,text='Send Request', fg='white', bg='blue', relief= RAISED, command=self.confirmRequest, font = 'Aria -18 bold')
        self.b1.grid(row=1, column=2)

        # Requst Status
        self.r_s = ttk.LabelFrame(self.master, height=100,width=200, text='Request Status')
        self.r_s.place(x=10,y=100)

        # Pending/ Accepted in Frame
        self.status = Label(self.r_s, text="Nothing", font = 'Aria -30 bold')
        self.status.pack()

        self.update()
        self.master.mainloop()

    def confirmRequest(self):
        msg = messagebox.askquestion('Send Request', 'Are you sure to send request', icon='warning')
        if msg == 'yes':
            self.send_request()
            self.status.config(text="Request Pending", fg='black', bg='red', font = 'Aria -30 bold')
            messagebox.showinfo('Done','Your request has been placed')
        else:
            messagebox.showinfo('Cancelled','Your request is not forwarded')
    
    def send_request(self):
        machine_no = self.m_number.get()
        batch_no = self.batch.get()
        time = datetime.datetime.now().strftime("%H:%M:%S")
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        status = "Pending"
        db = Database()
        db.insert_value(machine=machine_no, s_time=time, r_time=None, r_status=status, t_date=date)
        db.db_close()
    
    def send_email(self):
        self.emailWin = Tk()
        self.emailWin.geometry('500x100')
        self.emailWin.title('Send Email')
        self.reciever_email = StringVar()
        email_label = Label(self.emailWin, text='Enter Reciever Email:', font = 'Aria -16 bold')
        email_label.grid(row=0, column=0)
        self.email_entry = Entry(self.emailWin, textvariable=self.reciever_email)
        self.email_entry.grid(row=0, column=1)
        email_button = Button(self.emailWin, text='Send Email', command=self.confirmEmailSend)
        email_button.grid(row=1, column=1)

        self.emailWin.mainloop()

    def confirmEmailSend(self):
        msg = messagebox.askquestion('Send Email', 'Are you sure to send email', icon='warning')
        if msg == 'yes':
            re_email = self.email_entry.get()
            print(re_email.strip())
            db = Database()
            querys = db.fetch_today()
            db.db_close()
            pdf = Pdf()
            pdf.get_pdf(querys)
            send_email = EmailSend(re_email.strip())
            send_email.send_email()
            messagebox.showinfo('Done','Your email has been sent')
            self.emailWin.quit()
            self.emailWin.destroy()
            
        else:
            self.emailWin.quit()
            self.emailWin.destroy()
            messagebox.showerror('Cancelled','Your email is not forwarded')    


    def todayData(self):
        self.data_win = Tk()
        self.data_win.title("Today's Data")
        self.data_win.geometry('500x400')
        Label(self.data_win,text='Machine NO.').grid(row=0,column=0)
        Label(self.data_win,text='Send Time').grid(row=0,column=1)
        Label(self.data_win,text='Recieve Time').grid(row=0,column=2)
        Label(self.data_win,text='Status').grid(row=0,column=3)
        db = Database()
        results = db.fetch_today()
        i = 0
        for result in results:
            i+=1
            Label(self.data_win,text='{}'.format(result[1])).grid(row=i,column=0)
            Label(self.data_win,text='{}'.format(result[2])).grid(row=i,column=1)
            Label(self.data_win,text='{}'.format(result[3])).grid(row=i,column=2)
            Label(self.data_win,text='{}'.format(result[4])).grid(row=i,column=3)

        db.db_close()
        self.data_win.mainloop()

    def update(self):
        db = Database()
        try:
            status = db.fetch_latest().fetchone()[4]
        except:
            status = None
        if status == "Accepted":
            self.status.config(text="Request Accepted", fg='black', bg='green', font = 'Aria -30 bold')
        elif status == "Pending":
            self.status.config(text="Request Pending", fg='black', bg='red', font = 'Aria -30 bold')
        elif status == "NotAvailable":
            self.status.config(text="Not Available", fg='black', bg='yellow', font = 'Aria -30 bold')
        else:
            self.status.config(text="Nothing", font = 'Aria -30 bold')
        
        db.db_close()
        self.master.after(3000, self.update)
        




        

if __name__ == "__main__":

    app = App()