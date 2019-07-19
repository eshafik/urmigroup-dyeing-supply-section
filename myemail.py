import smtplib, os, datetime
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 


class EmailSend(object):
    def __init__(self, email):
        self.reciever = email
        self.file_name = datetime.datetime.now().strftime("%d-%b")
    
    def send_email(self):
        fromaddr = "shafikulislam.dorlove6@gmail.com"
        toaddr = self.reciever
        
        # instance of MIMEMultipart 
        msg = MIMEMultipart() 
        
        # storing the senders email address   
        msg['From'] = fromaddr 
        
        # storing the receivers email address  
        msg['To'] = toaddr 
        
        # storing the subject  
        msg['Subject'] = "Daily Report"
        
        # string to store the body of the mail 
        body = "Check the attachment file for the daily report"
        
        # attach the body with the msg instance 
        msg.attach(MIMEText(body, 'plain')) 
        
        # open the file to be sent  
        filename = self.file_name+".xlsx"
        attachment = open(os.getcwd()+"/file/"+self.file_name+".xlsx", "rb") 
        
        # instance of MIMEBase and named as p 
        p = MIMEBase('application', 'octet-stream') 
        
        # To change the payload into encoded form 
        p.set_payload((attachment).read()) 
        
        # encode into base64 
        encoders.encode_base64(p) 
        
        p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
        
        # attach the instance 'p' to instance 'msg' 
        msg.attach(p) 
        
        # creates SMTP session 
        s = smtplib.SMTP('smtp.gmail.com', 587) 
        
        # start TLS for security 
        s.starttls() 
        
        # Authentication 
        s.login(fromaddr, "mypassword") 
        
        # Converts the Multipart msg into a string 
        text = msg.as_string() 
        
        # sending the mail 
        s.sendmail(fromaddr, toaddr, text) 
        
        # terminating the session 
        s.quit() 
        if os.path.exists(os.getcwd()+"/file/"+self.file_name+".xlsx"):
            os.remove(os.getcwd()+"/file/"+self.file_name+".xlsx")
        else:
            print("The file does not exist")
