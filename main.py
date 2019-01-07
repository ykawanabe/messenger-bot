import os
from flask import Flask, request
from pymessenger.bot import Bot

app = Flask(__name__)
app.debug = True
ACCESS_TOKEN = os.environ.get('FB_ACCESS_TOKEN')
bot = Bot(ACCESS_TOKEN)

@app.route("/webhook", methods=['GET','POST'])
def webhook():
    print('hook!')
    if request.method == 'GET':
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    elif request.method == 'POST':
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for m in messaging:
                if m.get('message'):
                    recipient_id = m['sender']['id']
                    bot.send_action(recipient_id, 'mark_seen')
                    if m['message'].get('text'):
                        response = m['message']['text']
                        send_message(recipient_id, response)
                    if m['message'].get('attachments'):
                        for att in m['message'].get('attachments'):
                            response = recipient_id, att['type'], att['payload']['url']
                            send_message(recipient_id, response)
                else:
                    pass
    return "Message Processed"

# def handle_post(json):
#     for event in output

def verify_fb_token(token_sent):
    verify_token = os.environ.get('FB_VERIFY_TOKEN')
    if token_sent == verify_token:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

def send_message(recipient_id, response):
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == '__main__':
    app.run(host='0.0.0.0')
