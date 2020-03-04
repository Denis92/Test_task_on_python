import os
import aiomongodel
from aiohttp import web
import json
from email.message import EmailMessage
import re
from aiosmtplib import SMTP, errors
import jsonschema
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ServerSelectionTimeoutError
from models import Mail
from datetime import datetime
from config import Setup
from functools import wraps

config_ = Setup()

BASE_DIR = os.path.dirname(__file__)
file_json_schema = os.path.join(BASE_DIR, "schema.json")
with open(file=file_json_schema) as json_file:
    schema = json.load(json_file)

mail_host_name = config_.mail_host_name
mail_port = config_.mail_port
mail_check = config_.mail_check
server_port = config_.server_port
server_host = config_.server_host
mongo_connect = config_.mongo_url
route = web.RouteTableDef()


async def send_email(login_email, password_email, message_recipient, subject, text):
    message = EmailMessage()
    message["From"] = login_email
    message["To"] = message_recipient
    message["Subject"] = subject
    message.set_content(text)
    smtp_client = SMTP(hostname=mail_host_name, port=mail_port)
    async with smtp_client:
        try:
            await smtp_client.connect()
            await smtp_client.starttls()
            await smtp_client.login(username=login_email, password=password_email)
            await smtp_client.send_message(message)
            await smtp_client.quit()
            status_send = "successful send"
        except errors.SMTPException as e:
            status_send = e.message
            await smtp_client.quit()
    return status_send


def decor_validate_json(handle_):
    @wraps(handle_)
    async def wrapper(request):
        try:
            json_req = await request.json()
            jsonschema.validate(instance=json_req, schema=schema)
            if not (mail_check in json_req.get("login_email")):
                create_record = await Mail.q(db=db).create(send_status=f"You must use {mail_check} mailbox to send",
                                                           date_time=datetime.now())
                error_text = f"You must use {mail_check} mailbox to send"
                return web.Response(text=json.dumps({"id": create_record._id, "status": error_text}), status=400)
            if not (mail_check in json_req.get("login_email")):
                create_record = await Mail.q(db=db).create(send_status=f"You must use {mail_check} mailbox to send",
                                                           date_time=datetime.now())
                error_text = f"You must use {mail_check} mailbox to send"
                return web.Response(text=json.dumps({"id": create_record._id, "status": error_text}), status=400)
            valid_email = re.findall(r"^\S+@\S+$", json_req.get("message_recipient"))
            if not valid_email:
                await Mail.q(db=db).create(send_status=f"Not valid message recipient email "
                f"{json_req.get('message_recipient')}", date_time=datetime.now())
                error_text = f"Not valid message recipient email {json_req.get('message_recipient')}"
                return web.Response(text=json.dumps({"status": error_text}), status=400)
            return await handle_(request)
        except jsonschema.exceptions.ValidationError as e:
            create_record = await Mail.q(db=db).create(send_status=e.message, date_time=datetime.now())
            return web.Response(text=json.dumps({"id": create_record._id, "status": e.message}), status=400)
        except json.decoder.JSONDecodeError as e:
            create_record = await Mail.q(db=db).create(send_status=f"JSON Error: {e.msg}", date_time=datetime.now())
            error_text = f"JSON Error: {e.msg}"
            return web.Response(text=json.dumps({"id": create_record._id, "status": error_text}), status=400)

    return wrapper


@route.post('/send')
@decor_validate_json
async def handle(request):
    json_req = await request.json()
    login_email = json_req.get("login_email")
    password_email = json_req.get("password_email")
    message_recipient = json_req.get("message_recipient")
    subject = json_req.get("subject")
    text = json_req.get("text")
    resp = await send_email(login_email, password_email, message_recipient, subject, text)
    create_record = await Mail.q(db=db).create(send_status=f"{resp}", date_time=datetime.now())
    return web.Response(text=json.dumps({"id": create_record._id, "status": resp}))


@route.get('/get-result')
async def handler(request):
    try:
        id_send_email = request.rel_url.query["id_send_email"]
        mail = await Mail.q(db).get(f"{id_send_email}")
        return web.Response(text=json.dumps({"id": id_send_email, "datetime": f"{mail.date_time}",
                                             "status": mail.send_status}), status=200)
    except KeyError as e:
        error_text = "Error: Not found params"
        return web.Response(text=json.dumps({"error": error_text}), status=400)
    except ServerSelectionTimeoutError as e:
        error_text = f"Error: DB connection fail {e}"
        return web.Response(text=json.dumps({"error": error_text}), status=404)
    except aiomongodel.errors.DocumentNotFoundError as e:
        error_text = f"Error: Not found data {e}"
        return web.Response(text=json.dumps({"error": error_text}), status=404)


if __name__ == "__main__":
    client = AsyncIOMotorClient(mongo_connect)
    db = client.aiomongodel
    app = web.Application()
    app.add_routes(route)
    web.run_app(app, port=server_port, host=server_host)
