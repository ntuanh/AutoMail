import os
import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")


def send_mail(to_email, subject, body, image_path=None):
    print("=" * 60)
    print("[MAIL] START")
    print(f"[MAIL] TO: {to_email}")
    print(f"[MAIL] SUBJECT: {subject}")
    print(f"[MAIL] IMAGE: {image_path}")
    print("=" * 60)

    try:
        msg = MIMEMultipart("related")
        msg["Subject"] = subject
        msg["From"] = EMAIL
        msg["To"] = to_email
        msg["Reply-To"] = EMAIL
        msg["X-Mailer"] = "Python SMTP"

        img_html = ""
        if image_path:
            img_html = """
                <img src="cid:lab_image" 
                     width="100%" 
                     style="border-radius: 10px;">
            """

        html = f"""
        <html>
        <body style="font-family: Arial; line-height: 1.6;">
            <div style="max-width: 700px; margin: auto; padding: 20px; border-radius: 12px; background-color: #f8f9fa;">
                {img_html}
                <div style="padding-top:20px;">
                    {body.replace(chr(10), "<br>")}
                </div>
            </div>
        </body>
        </html>
        """

        msg.attach(MIMEText(html, "html", "utf-8"))

        if image_path is not None:
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Không tìm thấy file ảnh tại: {image_path}")

            print("[MAIL] Loading image...")
            with open(image_path, "rb") as f:
                image_bytes = f.read()

            mime_type, _ = mimetypes.guess_type(image_path)
            subtype = None
            if mime_type and mime_type.startswith("image/"):
                subtype = mime_type.split("/", 1)[1]

            img = MIMEImage(image_bytes, _subtype=subtype)
            img.add_header("Content-ID", "<lab_image>")
            img.add_header(
                "Content-Disposition",
                "inline",
                filename=os.path.basename(image_path)
            )
            msg.attach(img)

        print("[SMTP] Connecting...")
        server = smtplib.SMTP("smtp.office365.com", 587)
        server.set_debuglevel(1)

        print("[SMTP] EHLO")
        server.ehlo()
        print("[SMTP] STARTTLS")
        server.starttls()
        print("[SMTP] EHLO AGAIN")
        server.ehlo()

        print("[SMTP] LOGIN")
        server.login(EMAIL, PASSWORD)
        print("[SMTP] LOGIN SUCCESS")

        response = server.sendmail(EMAIL, [to_email], msg.as_string())
        print("[SMTP] SEND RESPONSE:")
        print(response)

        server.quit()
        print(f"[SUCCESS] Sent to {to_email}")

    except Exception as e:
        print("[ERROR] SEND MAIL FAILED")
        print(type(e).__name__)
        print(str(e))
        raise