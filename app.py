from flask import Flask, request, abort
from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

from bot_agent import BotAgent
import os


#line token
configuration = Configuration(access_token=os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

model = 'ft:gpt-3.5-turbo-0613:personal::7sm7EQwF'

bot_agent = BotAgent(model=model)

app = Flask(__name__)

@app.route("/")
def index():
    return "hello world"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

        input_msg = event.message.text
        
        # Reviced the cmd to reset bot_agent
        if input_msg == "!reset":
            bot_agent.reset()
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text="已重置")]
                )
            )
            return

        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=bot_agent.generate_resp(input_msg))]
            )
        )


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8082))
    app.run(host='0.0.0.0', port=port)

'''
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name garylinebot.de;
    location /{
        proxy_pass  http://127.0.0.1:8082;
        proxy_set_header Host $host;
    }
    
}
'''