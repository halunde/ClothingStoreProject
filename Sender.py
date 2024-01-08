import smtplib as st
from email.message import EmailMessage

def email_alert(subject, body, to):
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to
    
    
    user = "shubhamlohar952@gmail.com"
    msg['from'] = user
    password = "ddziygagporbxxov"
    
    server = st.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(user,password)
    server.send_message(msg)
    server.quit()
    
if __name__ == '__main__':
    email_alert("Hey","Hello World..","shubhmechanics952@gmail.com")
    