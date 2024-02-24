import smtplib


class SMTP:
    def __init__(self, user, user_db):
        self.user = user
        self.user_db = user_db
        self.smtp_server: str = str()
        self.port: int = int()
        self.smtp = smtplib.SMTP(self.smtp_server, self.port)
        self.sender = self.user_db.get(f"Sender({self.user.sender})")

    def gmail(self):
        self.smtp_server = 'smtp.gmail.com'
        self.port = 587
        self.smtp = smtplib.SMTP(self.smtp_server, self.port)
        try:
            self.smtp.starttls()
            self.smtp.login(self.sender.email, self.sender.password)
            print("Connected to Gmail")
        except (ConnectionError, Exception):
            raise Exception("Failed to connect to Gmail")

    def get_message(self, db):
        output = db.query_to_get_data(f"SELECT subject, template FROM template WHERE type = '{self.user.message_type}'")[0]
        subject = output['subject'].format(user=self.user, sender=self.sender)
        template = output['template'].format(user=self.user, sender=self.sender)
        message = f"Subject: {subject}\n\n{template}"
        return message

    def send_email(self, db):
        msg = str(self.get_message(db))
        self.smtp.sendmail(self.sender.email, self.user.email, msg)
        print(f"Email sent: {self.sender.email} -> {self.user.email}")

    def close_connection(self):
        self.smtp.quit()
