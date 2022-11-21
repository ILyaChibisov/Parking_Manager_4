from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import mimetypes
import email.mime.application


def send_file_to_email(to_email, file):
    msg = MIMEMultipart()
    msg['Subject'] = 'Отчёт СРНЗ АВИАПАРК'
    msg['From'] = 'iliachibisov@mail.ru'
    msg['To'] = to_email

    txt = MIMEText('Отчёт СРНЗ АВИАПАРК')
    msg.attach(txt)

    filename = file
    fo=open(filename, 'rb')
    attach = email.mime.application.MIMEApplication(fo.read(), _subtype="xls")
    fo.close()
    attach.add_header('Content-Disposition', 'attachment', filename=filename)
    msg.attach(attach)
    s = smtplib.SMTP('smtp.mail.ru: 25')
    s.starttls()
    s.login('iliachibisov@mail.ru', 'Th8CnkK9QZiYYQFk5enF')
    s.send_message(msg)
    s.quit()


if __name__ == '__menu__':
    menu()
