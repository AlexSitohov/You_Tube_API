import smtplib
from email.message import EmailMessage

SMTP_HOST = 'smtp.gmail.com'
SMTP_PORT = 587

SMTP_USER = "lilinfinitemob@gmail.com"
SMTP_PASSWORD = "zhfpjgqopauywzvm"


def send_email_report_dashboard(current_user):
    username = current_user.dict().get('username')
    user_mail = current_user.dict().get('mail_user')

    email = get_email_template_dashboard(username, user_mail)

    smtp_server = smtplib.SMTP(host=SMTP_HOST, port=SMTP_PORT)
    smtp_server.starttls()
    smtp_server.login(SMTP_USER, SMTP_PASSWORD)
    smtp_server.send_message(email)


def get_email_template_dashboard(username, user_mail):
    email = EmailMessage()
    email['Subject'] = 'Даров'
    email['From'] = SMTP_USER
    email['To'] = user_mail

    email.set_content(
        f'''
        <div>
        <h1 style="color: red;">Здравствуйте {username}. 😊</h1>
        <img src="https://sun9-55.userapi.com/impg/UI7iQX4y_Hi0w-EDdWasIUQi_LQBxw7uAfr5Mg/PZjYAOik45I.jpg?size=2560x1440&quality=96&sign=3aea9c6b509c6c9c0cacbcfaed248d82&type=album" width="600">
        </div>
        ''',
        subtype='html'
    )
    return email
