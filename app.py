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

schema = {
    "type": "object",
    "properties": {
        "login_email": {"type": "string"},
        "password_email": {"type": "string"},
        "message_recipient": {"type": "string"},
        "subject": {"type": "string"},
        "text": {"type": "string"},
    },
    "required": ["login_email", "password_email", "message_recipient", "subject", "text"]
}

route = web.RouteTableDef()


async def say_hello(login_email, password_email, message_recipient, subject, text):
    message = EmailMessage()
    message["From"] = login_email
    message["To"] = message_recipient
    message["Subject"] = subject
    message.set_content(text)
    smtp_client = SMTP(hostname="smtp.yandex.ru", port=587)
    async with smtp_client:
        try:
            await smtp_client.connect()
            await smtp_client.starttls()
            await smtp_client.login(username=login_email, password=password_email)
            await smtp_client.send_message(message)
            await smtp_client.quit()
            status_send = "successful send"
        except errors.SMTPAuthenticationError as e:
            status_send = e.message
            await smtp_client.quit()

    return status_send


@route.post('/send')
async def handle(request):
    try:
        client = AsyncIOMotorClient("mongodb://127.0.0.1:27017/")
        db = client.aiomongodel
        _id = datetime.timestamp(datetime.now())

        try:
            await Mail.q(db).create_indexes()
            json_req = await request.json()
            jsonschema.validate(instance=json_req, schema=schema)
            if not ("@yandex.ru" in json_req.get("login_email")):
                await Mail.q(db=db).create(_id=_id, send_status="You must use Yandex mailbox to send",
                                           date_time=datetime.now())
                return web.Response(text="You must use Yandex mailbox to send", status=400)
            valid_email = re.findall(r"^\S+@\S+$", json_req.get("message_recipient"))
            if not valid_email:
                await Mail.q(db=db).create(_id=_id, send_status=f"Not valid message recipient email "
                f"{json_req.get('message_recipient')}", date_time=datetime.now())
                return web.Response(text=f"Not valid message recipient email {json_req.get('message_recipient')}",
                                    status=400)
            login_email = json_req.get("login_email")
            password_email = json_req.get("password_email")
            message_recipient = json_req.get("message_recipient")
            subject = json_req.get("subject")
            text = json_req.get("text")
            resp = await say_hello(login_email, password_email, message_recipient, subject, text)
            await Mail.q(db=db).create(_id=_id, send_status=f"{resp}", date_time=datetime.now())
            return web.Response(text=json.dumps({"id": _id, "status": resp}))
        except jsonschema.exceptions.ValidationError as e:
            await Mail.q(db=db).create(_id=_id, send_status=e.message, date_time=datetime.now())
            return web.Response(text=e.message, status=400)
        except json.decoder.JSONDecodeError as e:
            await Mail.q(db=db).create(_id=_id, send_status=f"JSON Error: {e.msg}", date_time=datetime.now())
            return web.Response(text=f"JSON Error: {e.msg}", status=400)
    except ServerSelectionTimeoutError as e:
        return web.Response(text=f"Error: DB connection fail {e}", status=500)


@route.get('/get-result')
async def handler(request):
    try:
        client = AsyncIOMotorClient("mongodb://127.0.0.1:27017/")
        db = client.aiomongodel
        id_send_email = request.rel_url.query["id_send_email"]
        mail = await Mail.q(db).get(f"{id_send_email}")
        return web.Response(text=json.dumps({"id": id_send_email, "datetime": f"{mail.date_time}",
                                            "status": mail.send_status}), status=200)
    except KeyError as e:
        return web.Response(text="Error: Not found params", status=400)
    except ServerSelectionTimeoutError as e:
        return web.Response(text=f"Error: DB connection fail {e}", status=500)
    except aiomongodel.errors.DocumentNotFoundError as e:
        return web.Response(text=f"Error: Not found data {e}", status=500)

app = web.Application()
app.add_routes(route)

web.run_app(app, port=5000, host="127.0.0.1")
