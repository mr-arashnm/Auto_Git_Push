import subprocess

class EmailNotifier:
    def __init__(self):
        pass  # نیازی به تنظیمات SMTP نیست

    def send_email(self, recipient_email, subject, body):
        """
        ارسال ایمیل با استفاده از ابزار سیستم (مانند mail یا sendmail)
        :param recipient_email: آدرس گیرنده ایمیل
        :param subject: موضوع ایمیل
        :param body: محتوای ایمیل
        """
        try:
            # اجرای دستور mail برای ارسال ایمیل
            process = subprocess.Popen(
                ["mail", "-s", subject, recipient_email],
                stdin=subprocess.PIPE,
                text=True  # فعال کردن حالت متنی برای ارسال ورودی
            )
            process.communicate(body)  # ارسال محتوای ایمیل به stdin ابزار mail

            # بررسی وضعیت ارسال
            if process.returncode == 0:
                print("Email sent successfully using system mail.")
            else:
                print(f"Failed to send email using system mail. Return code: {process.returncode}")
        except FileNotFoundError:
            print("The 'mail' command is not available. Please install it (e.g., 'sudo apt install mailutils').")
        except Exception as e:
            print(f"Error while sending email with system mail: {e}")