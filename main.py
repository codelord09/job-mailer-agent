import pandas as pd
import smtplib
import openpyxl

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from docx import Document
from email.mime.base import MIMEBase
from email import encoders

contacts = pd.read_excel("contacts.xlsx")  

your_email = "neerajgupta0912@gmail.com"
your_password = "fqkf ceqb ahbk loip"


def get_email_body(file_path):
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])


email_body_template = get_email_body("email_template.docx")


def send_email(receiver_name, company_name, job_link, receiver_email):
    body = (
        email_body_template.replace("{receiver_name}", receiver_name)
        .replace("{company_name}", company_name)
        .replace("{job_link}", job_link)
    )

    subject = "Immediate Joiner | SDE(GenAI) | IIIT Allahabad | 2+ Years Exp"
    msg = MIMEMultipart()
    msg["From"] = your_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "html"))

    with open("Neeraj_Gupta_SDE1.pdf", "rb") as resume:  
        part = MIMEBase("application", "octet-stream")
        part.set_payload(resume.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition", f'attachment; filename="Neeraj_Gupta_SDE1.pdf"'
        )
        msg.attach(part)

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(your_email, your_password)
        server.send_message(msg)
    print(f"Email sent to {receiver_name} ({receiver_email}) for {company_name}.")


for _, row in contacts.iterrows():
    send_email(
        row["Receiver Name"],
        row["Company Name"],
        row["Job Link"],
        row["Receiver Email"],
    )
