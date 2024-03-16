import os

import openai
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk.web import WebClient

# ボットトークンとソケットモードハンドラーを使ってアプリを初期化します
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))


# リスナーマッチャー： 簡略化されたバージョンのリスナーミドルウェア
def is_bot_dm(message) -> bool:
    return message["channel_type"] == "im"


# 'hello' を含むメッセージをリッスンします
# 指定可能なリスナーのメソッド引数の一覧は以下のモジュールドキュメントを参考にしてください：
# https://slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html
@app.message("hello")
def message_hello(message, say):
    # イベントがトリガーされたチャンネルへ say() でメッセージを送信します
    say(f"Hey there <@{message['user']}>!")


@app.event(event="message", matchers=[is_bot_dm])
@app.event("app_mention")
def handle_mention(event: dict, client: WebClient):
    messages = []
    user = event["user"]
    channel = event["channel"]
    ts = event["ts"]

    # 受付メッセージを送信
    text = "少々お待ちください..."
    received_msg = client.chat_postMessage(channel=channel, text=text, thread_ts=ts)

    # thread_tsがある場合はスレッドのメッセージを取得
    if "thread_ts" in event:
        messages = get_thread_messages(channel, event["thread_ts"], client)
    else:
        messages = [{"role": "user", "content": event["text"]}]

    # ChatGPTの応答を取得して送信
    try:
        response = respond_gpt(messages)
        message = f"<@{user}> {response}"
        client.chat_update(channel=channel, ts=received_msg["ts"], text=message)
    except Exception as e:
        message = f"<@{user}> 申し訳ありません。エラーが発生しました。\n{e}"
        client.chat_update(channel=channel, ts=received_msg["ts"], text=message)


def respond_gpt(messages) -> str:
    """
    OpenAIのChatGPTを使って応答を取得します
    """
    model = os.environ["DEFAULT_MODEL"]
    completion = openai.chat.completions.create(
        model=model,
        messages=messages,
    )
    response_message = completion.choices[0].message.content
    return response_message


def get_thread_messages(channel: str, ts: str, client: WebClient) -> list:
    """
    スレッドのメッセージを取得してOpenAI用のmessagesを作成します
    """
    messages = []

    # スレッドのメッセージを取得
    replies = client.conversations_replies(channel=channel, ts=ts)

    # replies["messages"]をループしてOpenAI用のmessagesを作成
    for message in replies["messages"]:
        if "subtype" not in message:
            if "bot_id" in message:
                role = "assistant"
            else:
                role = "user"
            messages.append({"role": role, "content": message["text"]})

    # 一番最後のmessageがassistantの場合は削除
    if messages[-1]["role"] == "assistant":
        messages.pop(-1)
    return messages


# アプリを起動します
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
