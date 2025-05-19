from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from src.config import Config
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]  # /opt/render/project/src
TEMPLATE_FOLDER = PROJECT_ROOT / "src" / "templates"

mail_config = ConnectionConfig(
    MAIL_USERNAME = Config.MAIL_USERNAME,
    MAIL_PASSWORD = Config.MAIL_PASSWORD,
    MAIL_FROM = Config.MAIL_FROM,
    MAIL_PORT = Config.MAIL_PORT,
    MAIL_SERVER = Config.MAIL_SERVER,
    MAIL_FROM_NAME = Config.MAIL_FROM_NAME,
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True,
    TEMPLATE_FOLDER = TEMPLATE_FOLDER
)

mail= FastMail(
    config = mail_config
)

def create_message(recipients:list[str],subject:str,body:str):

    message = MessageSchema(
        recipients=recipients,
        subject=subject,
        body=body,
        subtype=MessageType.html
    )

    return message