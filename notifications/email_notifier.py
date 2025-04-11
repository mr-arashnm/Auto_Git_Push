import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailNotifier:
    def __init__(self, smtp_server, smtp_port, sender_email, sender_password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password

    def send_email(self, recipient_email, subject, body):
        try:
            # ایجاد پیام ایمیل
            msg = MIMEMultipart()
            msg["From"] = self.sender_email
            msg["To"] = recipient_email
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))

            # اتصال به سرور SMTP و ارسال ایمیل
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # فعال کردن TLS
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, recipient_email, msg.as_string())

            print("Email sent successfully.")
        except Exception as e:
            print(f"Failed to send email: {e}")