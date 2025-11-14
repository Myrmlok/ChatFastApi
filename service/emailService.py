import logging
from email.message import EmailMessage
from email.mime.message import MIMEMessage
from email.mime.multipart import MIMEMultipart
import smtplib
import aiosmtplib
from config.envApp import settings


class EmailService:
    @classmethod
    async def async_send_message(cls,to:str,subject:str,msg:str)->bool:
        try:
            message=EmailMessage()
            message["From"]=settings.EMAIL_USERNAME
            message["To"]=to
            message["Subject"]=subject
            message.set_content(msg)
            await aiosmtplib.send(
                message,
                hostname=settings.EMAIL_HOST,
                port=int(settings.EMAIL_PORT),
                username=settings.EMAIL_USERNAME,
                password=settings.EMAIL_PASSWORD,
                use_tls=True
            )
            logging.info("success to send message to"+to)
            return True

        except Exception as ex:
            logging.error("Can't send message to"+to);
            logging.error(ex)
            return False
