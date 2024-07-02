import smtplib
import schedule
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta

# SMTP server configuration (example for Gmail)
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT_NUM = 587
EMAIL_USER = "your_email@gmail.com"
EMAIL_PASSWORD = "your_password"

def dispatch_email(email_subject, email_body, recipient_list):
    email_msg = MIMEMultipart()
    email_msg['From'] = EMAIL_USER
    email_msg['To'] = ', '.join(recipient_list)
    email_msg['Subject'] = email_subject

    email_msg.attach(MIMEText(email_body, 'plain'))

    try:
        email_server = smtplib.SMTP(SMTP_HOST, SMTP_PORT_NUM)
        email_server.starttls()
        email_server.login(EMAIL_USER, EMAIL_PASSWORD)
        email_server.sendmail(EMAIL_USER, recipient_list, email_msg.as_string())
        email_server.quit()
        print(f"Email dispatched to {', '.join(recipient_list)}")
    except Exception as error:
        print(f"Failed to dispatch email. Error: {str(error)}")

def program_email(email_subject, email_body, recipient_list, dispatch_time):
    current_timestamp = datetime.now()
    time_delay = (dispatch_time - current_timestamp).total_seconds()

    if time_delay < 0:
        print("Scheduled time is in the past. Please provide a future time.")
        return

    def job():
        dispatch_email(email_subject, email_body, recipient_list)

    # Schedule the job to run once after the calculated delay
    schedule.every(time_delay).seconds.do(job)
    print(f"Email programmed to be dispatched to {', '.join(recipient_list)} at {dispatch_time}")

def main():
    print("Email Automation Script")

    email_subject = input("Enter the email subject: ")
    email_body = input("Enter the email body: ")
    recipient_list = input("Enter recipient email addresses (comma separated): ").split(',')

    send_now_choice = input("Dispatch now? (yes/no): ").strip().lower()

    if send_now_choice == 'yes':
        dispatch_email(email_subject, email_body, recipient_list)
    else:
        dispatch_date = input("Enter the date to dispatch the email (YYYY-MM-DD): ")
        dispatch_time = input("Enter the time to dispatch the email (HH:MM): ")
        dispatch_datetime = f"{dispatch_date} {dispatch_time}"
        
        try:
            dispatch_timestamp = datetime.strptime(dispatch_datetime, "%Y-%m-%d %H:%M")
            program_email(email_subject, email_body, recipient_list, dispatch_timestamp)
        except ValueError:
            print("Invalid date/time format. Please try again.")
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
