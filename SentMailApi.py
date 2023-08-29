import smtplib
from flask import Flask, request
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os.path

app= Flask(__name__)

@app.route("/SentMail", methods=['POST'])
def Sent():
    if request.method == "POST":

        #Parameters
        params = request.json
        param_Subject = params.get('subject')
        param_Body = params.get('body')
        param_Sender= params.get('Sender')
        param_Email = params.get('mail')
        param_Paths= params.get('Paths')

        #Message
        msg = MIMEMultipart()

        msg['Subject'] = param_Subject
        msg.attach(MIMEText(param_Body,'plain'))

        #Add Attachments
        Attachment_Number=len(param_Paths)
        while Attachment_Number>0:#Sequentially attaching files to mail with while loop

            file_Locations= param_Paths[Attachment_Number-1]
            file_Name = os.path.basename(file_Locations)
            attacment = open(file_Locations,"rb")
            part = MIMEBase('application','octet_stream')
            part.set_payload((attacment).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',"attachment; filename= %s" % file_Name)
            msg.attach(part)
            Attachment_Number= Attachment_Number-1

        #Send Mail
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        text= msg.as_string()
        server.login(param_Sender,'THİS İS APP PASSWORD FOR YOUR GMAİL, NOT YOUR GMAİL PASSWORD')#Login gmail
        server.sendmail(param_Sender,param_Email,text)

        return "sucsess"
    else:
        return "fail"

#Running app
if __name__=='__main__':
    app.run(debug=True)

