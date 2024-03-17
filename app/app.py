import os

from openai_ops import respond_gpt
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk.web import WebClient

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))


@app.event("app_mention")
def handle_mention(event: dict, client: WebClient):
    user = event["user"]
    channel = event["channel"]
    ts = event["ts"]

    # 受付メッセージを送信
    text = "少々お待ちください..."
    wip_message = client.chat_postMessage(channel=channel, text=text, thread_ts=ts)

    # OpenAI API用データを準備
    messages = [{"role": "user", "content": event["text"]}]

    # モデルを設定
    model = os.environ.get("DEFAULT_MODEL", "gpt-3.5-turbo")

    # リクエスト
    response = respond_gpt(messages, model)

    # 応答内容を投稿
    message = f"<@{user}> {response}"
    client.chat_update(channel=channel, ts=wip_message["ts"], text=message)


# アプリを起動します
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
