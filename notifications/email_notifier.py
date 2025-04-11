import subprocess

class EmailNotifier:
    def __init__(self):
        pass  

    def send_email(self, recipient_email, subject, body):
        try:
            process = subprocess.Popen(
                ["mail", "-s", subject, recipient_email],
                stdin=subprocess.PIPE,
                text=True  
            )
            process.communicate(body)

            if process.returncode == 0:
                print("Email sent successfully using system mail.")
            else:
                print(f"Failed to send email using system mail. Return code: {process.returncode}")
        except FileNotFoundError:
            print("The 'mail' command is not available. Please install it (e.g., 'sudo apt install mailutils').")
        except Exception as e:
            print(f"Error while sending email with system mail: {e}")