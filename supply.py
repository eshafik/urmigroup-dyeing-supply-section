import datetime

from tkinter import *
from tkinter import ttk, messagebox

from database import Database
from myemail import EmailSend
from pdf import Pdf


class App(object):
    def __init__(self, master):
        self.master = master
        # print("{} x {}".format(self.master.winfo_screenheight(), self.master.winfo_screenwidth()))
        self.master.title('FTML-Supply Section')
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
        self.m_c_l = Label(self.master, text='Machine ', font = 'Aria -16 bold', pady=5)
        self.m_c_l.grid(row=0, column=0, padx=10)


        # Batch Label
        self.b_l = Label(self.master, text='Batch:', font = 'Aria -16 bold', pady=5)
        self.b_l.grid(row=0, column=2, padx=2)

        # Respone Label
        self.r_s_l = Label(self.master, text="Choose Response:", font = 'Aria -13 bold')
        self.r_s_l.grid(row=1, column=0, padx=10)

        # Response Option
        self.response = StringVar()
        self.response_box = ttk.Combobox(self.master, textvariable=self.response, width=15)
        self.response_box.grid(row=1, column=1)
        self.response_box.config(values=(
            "Accepted",
            "NotAvailable",
        ))
        self.response_box.current(0)


        # Send Response
        self.b1 = Button(self.master,text='Send Response', fg='white', bg='blue', relief= RAISED, command=self.confirmRequest, font = 'Aria -13 bold')
        self.b1.grid(row=1, column=2)

        # Request Status
        self.r_s = ttk.LabelFrame(self.master, height=100,width=200, text='Request Status',)
        self.r_s.place(x=10,y=100)

        # Pending/ Accepted in Frame
        self.status = Label(self.r_s, text="Nothing", font = 'Aria -30 bold')
        self.status.pack()

        self.update()
        self.master.mainloop()

    def confirmRequest(self):
        msg = messagebox.askquestion('Send Response', 'Are you sure to send response', icon='warning')
        if msg == 'yes':
            self.send_response()
            self.status.config(text="Done", fg='black', bg='green', font = 'Aria -30 bold')
            messagebox.showinfo('Done','Your response has been placed')
        else:
            messagebox.showinfo('Cancelled','Your response is not forwarded')
    
    def send_response(self):
        db = Database()
        status = self.response.get()
        db.update_value(r_status=status)
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
            data = db.fetch_latest().fetchone()
        except:
            data = None
        machine_no = data[1]
        status = data[4]
        if status == "Accepted":
            self.m_c_l.config(text='Machine ', font = 'Aria -16 bold', pady=5)
            self.status.config(text="No  Request", font = 'Aria -30 bold')
        elif status == "Pending":
            self.m_c_l.config(text='Machine NO.: {}'.format(machine_no), font = 'Aria -16 bold', pady=5)
            self.status.config(text="Request Pending", fg='black', bg='red', font = 'Aria -30 bold')
        elif status == "NotAvailable":
            self.m_c_l.config(text='Machine NO.: {}'.format(machine_no), font = 'Aria -16 bold', pady=5)
            self.status.config(text="Not Available", fg='black', bg='yellow', font = 'Aria -30 bold')
        db.db_close()
        self.master.after(3000, self.update)
        



        

if __name__ == "__main__":
    root = Tk()
    app = App(root)