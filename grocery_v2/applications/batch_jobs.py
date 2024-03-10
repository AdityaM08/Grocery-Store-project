from datetime import datetime
from celery.schedules import crontab
from applications.models import User, Order
from applications.celery_worker import celery
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText
import smtplib
from jinja2 import Template 
from weasyprint import HTML
import os
import csv

SMTP_SERVER_HOST= "localhost"
SMTP_SERVER_PORT= 1025
SENDER_ADDRESS = "support@thegrocerystore.com"
SENDER_PASSWORD = ""

def send_mail(receiver, subject, message, content="text", attachment=None):
    msg = MIMEMultipart()
    msg['From'] = SENDER_ADDRESS
    msg['To'] = receiver
    msg['Subject'] = subject

    if content == "html":
        msg.attach(MIMEText(message, "html"))
    else:
        msg.attach(MIMEText(message, "plain"))

    if attachment:
        with open(attachment, 'rb') as attachment_:

            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment_.read())

        part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(attachment)}"')
        encoders.encode_base64(part)
        msg.attach(part)

    server = smtplib.SMTP(host = SMTP_SERVER_HOST, port = SMTP_SERVER_PORT)
    server.login(SENDER_ADDRESS, SENDER_PASSWORD)
    server.send_message(msg)
    server.quit()
    return 'Mail Sent successfully !!'

def ConvertToPDF(htmlContent, pdfFile):
    HTML(string=htmlContent).write_pdf(pdfFile)

def get_report_pdf(templateFile, data, username):
    with open(templateFile) as fileTemp:
        template = Template(fileTemp.read())
        html_report = template.render(product_details=data, username=username)
        pdf_report = f"src/{username.split()[0]}.pdf"
        ConvertToPDF(html_report, pdf_report)
        return pdf_report
    
@celery.task()
def data_exporter(product_details, email, name):
    file_name = f'src/{name}_details.csv'
    product_fields = ['Product_Name', 'Product_Category', 'Product_Description', 'Product_Price', 'Product_Unit', 'Product_Stock']

    with open(file_name, 'w', newline='', encoding='utf8') as csvf: 
        cwriter = csv.writer(csvf) 
        cwriter.writerow(product_fields) 
        cwriter.writerows(product_details)

    send_mail(receiver=email, subject="Product Details ", message= "Please find attached product details csv. Thankyou!", attachment=f'src/{name}_details.csv')
    return "CSV file exported!"

@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10, reminder.s(), name='reminder') 
    sender.add_periodic_task(10, monthly_report.s(), name='monthly_report')

    sender.add_periodic_task(
        crontab(minute=0, hour=18, day_of_month='*'),
        reminder.s(),
        name = 'Daily reminder everyday @6PM via mail.'
    )

    sender.add_periodic_task(
        crontab(day_of_month=1, month_of_year='*'),
        monthly_report.s(),
        name = 'Monthly Entertainment Report @1st of every month via mail.'
    )

@celery.task
def reminder():
    users = User.query.filter_by(role = "user").all()
    for user in users:
        if user.latest_log < str(datetime.now()):
            reciver_mail = user.user_email
            send_mail(reciver_mail, subject="Daily Reminder", message="Hey! Visit The GroceryShop and get the fresh for you home!")
    return "Daily reminder done!"

@celery.task
def monthly_report(): 
    users = User.query.filter_by(role = "user").all()
    for user in users:
        name = user.user_name
        mail = user.user_email
        orders = Order.query.filter_by(user_id=user.user_id).all()
        order_details = []
        for o in orders:
            order = []
            order.append(o.order_name)
            order.append(o.order_quantity)
            order.append(o.order_total)
            order.append(o.order_date)
            order_details.append(order)
        file = get_report_pdf("src/monthly_report.html", order_details, name)

        send_mail(mail, subject="Monthly Shopping Report", message = "Hello! Please find attached you monthly shopping report.", attachment=f'{file}')
    return "Monthly Reports Sent!"