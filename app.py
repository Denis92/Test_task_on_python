from aiohttp import web
import json
from email.message import EmailMessage
import re
from aiosmtplib import SMTP, errors
import jsonschema

status_send = {"1": ''}

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
            status_send["1"] = "successful send"
        except errors.SMTPAuthenticationError as e:
            status_send["1"] = e.message
            await smtp_client.quit()

    return status_send


@route.post('/send')
async def handle(request):
    try:
        json_req = await request.json()
        jsonschema.validate(instance=json_req, schema=schema)
        if not ("@yandex.ru" in json_req.get("login_email")):
            return web.Response(text="You must use Yandex mailbox to send", status=400)
        valid_email = re.findall(r"^\S+@\S+$", json_req.get("message_recipient"))
        if not valid_email:
            return web.Response(text=f"Not valid message recipient email {json_req.get('message_recipient')}",
                                status=400)
        login_email = json_req.get("login_email")
        password_email = json_req.get("password_email")
        message_recipient = json_req.get("message_recipient")
        subject = json_req.get("subject")
        text = json_req.get("text")
        resp = await say_hello(login_email, password_email, message_recipient, subject, text)
        return web.Response(text=json.dumps(resp))
    except jsonschema.exceptions.ValidationError as e:
        return web.Response(text=e.message, status=400)
    except json.decoder.JSONDecodeError as e:
        return web.Response(text=f"JSON Error: {e.msg}", status=400)


@route.get('/get-result')
async def handler(request):
    try:
        id_send_email = request.rel_url.query["id_send_email"]
        return web.Response(text=status_send.get(id_send_email), status=200)
    except KeyError as e:
        return web.Response(text="Error: Not found params", status=400)


app = web.Application()
app.add_routes(route)

web.run_app(app, port=5000, host="127.0.0.1")
