import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os

EMAIL = os.getenv("EMAIL")

PASSWORD = os.getenv("PASSWORD")

def send_mail(
    to_email,
    subject,
    body,
    image_path
):

    msg = MIMEMultipart(
        "related"
    )

    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = to_email

    html = f"""
    <html>

    <body style="
        font-family: Arial;
        line-height: 1.6;
    ">

    <div style="
        max-width: 700px;
        margin: auto;
        padding: 20px;
        border-radius: 12px;
        background-color: #f8f9fa;
    ">

        <img src="cid:lab_image"
             width="100%"
             style="border-radius: 10px;">

        <div style="padding-top:20px;">

            {body.replace(chr(10), "<br>")}

        </div>

    </div>

    </body>
    </html>
    """

    msg.attach(
        MIMEText(
            html,
            "html",
            "utf-8"
        )
    )

    with open(
        image_path,
        "rb"
    ) as f:

        # img = MIMEImage(
        #     f.read()
        # )
        img = MIMEImage(
            f.read(),
            _subtype="jpeg"
        )

        img.add_header(
            "Content-ID",
            "<lab_image>"
        )

        img.add_header(
            "Content-Disposition",
            "inline",
            filename=image_path
        )

        msg.attach(img)

    server = smtplib.SMTP(
        "smtp.office365.com",
        587
    )

    server.starttls()

    server.login(
        EMAIL,
        PASSWORD
    )

    server.sendmail(
        EMAIL,
        to_email,
        msg.as_string()
    )

    server.quit()

    print(
        f"[SUCCESS] Sent to {to_email}"
    )