import os
from flask import Flask, request
from fbmessenger import BaseMessenger

class Messenger(BaseMessenger):
    def __init__(self, page_access_token):
        self.page_access_token = page_access_token
        super(Messenger, self).__init__(self.page_access_token)

    def message(self, message):
        res = self.send({'text': str(message['message']['text'])})
        app.logger.debug('Response: {}'.format(res))

    def delivery(self, message):
        pass

    def read(self, message):
        pass

    def account_linking(self, message):
        pass

    def postback(self, message):
        pass

    def optin(self, message):
        pass

app = Flask(__name__)
app.debug = True
messenger = Messenger(os.environ.get('FB_PAGE_TOKEN'))

@app.route("/webhook", methods=['GET','POST'])
def webhook():
    print("Webhook")
    if request.method == 'GET':
        if request.args.get('hub.verify_token') == os.environ.get('FB_VERIFY_TOKEN'):
            print("Here!")
            return request.args.get('hub.challenge')
        raise ValueError('FB_VERIFY_TOKEN does not match.')
    elif request.method == 'POST':
        messenger.handle(request.get_json(force=True))
    return ''

if __name__ == '__main__':
    app.run(host='0.0.0.0')
