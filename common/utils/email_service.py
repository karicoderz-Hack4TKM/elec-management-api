import smtplib
from flask import current_app

from  email.message import EmailMessage


# for docs refer : https://docs.python.org/3/library/smtplib.html
class EmailService:

    def sendSimpleEmail(self, username, password, toAddress, subject, message, priority):
        messagePayload = "\r\n".join([
            "From: " + username,
            "To: " + toAddress,
            "Subject: " + subject,
            "X-Priority: " + priority,
            "",
            message
        ])

        try:
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.ehlo()
            server.starttls()
            try:
                server.login(username, password)
                try:
                    response = server.sendmail(username, toAddress, messagePayload)
                    server.quit()
                    return {"code": 200, "message": "SMTP Email sent Successfully : " + str(response)}, 200
                except Exception as e:
                    server.quit()
                    return {"code": 421, "message": "SMTP Failed to send Email : " + str(e)}, 421
            except Exception as e:
                server.quit()
                return {"code": 421, "message": "SMTP Email Account Login Failed : " + str(e)}, 421

        except Exception as e:
            print("SMTP Server connection Failed : " + str(e))
            return {"code": 421, "message": "SMTP Server connection Failed : " + str(e)}, 421



class EmailSend:
    def sendEmailWithHtml(self, subject, reciever_email, html):
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = current_app.config["EMAIL_USERNAME"]
        msg["To"] = reciever_email
        msg.add_alternative(html, subtype="html")
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                try:
                    smtp.login(current_app.config["EMAIL_USERNAME"], current_app.config["EMAIL_PASSWORD"])
                    try:
                        smtp.send_message(msg)
                        return {"code": 200, "message": "SMTP Email sent Successfully : "}, 200
                    except Exception as e:
                        smtp.quit()
                        return {"code": 421, "message": "SMTP Failed to send Email : " + str(e)}, 421
                except Exception as e:
                    smtp.quit()
                    return {"code": 421, "message": "SMTP Email Account Login Failed : " + str(e)}, 421

        except Exception as e:
            print("SMTP Server connection Failed : " + str(e))
            return {"code": 421, "message": "SMTP Server connection Failed : " + str(e)}, 421