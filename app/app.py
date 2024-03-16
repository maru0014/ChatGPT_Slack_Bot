import os

from openai import APITimeoutError
from openai_ops import calculate_tokens, respond_gpt
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk.web import WebClient

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))


def is_bot_dm(message) -> bool:
    """
    dmのメッセージかどうかを判定します
    """
    return message["channel_type"] == "im"


@app.event("app_mention")
@app.event(event="message", matchers=[is_bot_dm])
def handle_mention(event: dict, client: WebClient):
    """
    botへのメンションやDMに対して応答します
    """
    messages = []
    user = event["user"]
    channel = event["channel"]
    ts = event["ts"]

    # 受付メッセージを送信
    text = "少々お待ちください..."
    wip_message = client.chat_postMessage(channel=channel, text=text, thread_ts=ts)

    # thread_tsがある場合はスレッドのメッセージを取得
    if "thread_ts" in event:
        messages = get_thread_messages(channel, event["thread_ts"], client)
    else:
        messages = [{"role": "user", "content": event["text"]}]

    try:
        # モデルとトークン数の上限を取得
        model = os.environ.get("DEFAULT_MODEL", "gpt-3.5-turbo")
        limit = int(os.environ.get("TOKEN_LIMIT", 4000))
        tokens = calculate_tokens(messages, model)

        if tokens > limit:
            # トークン数が上限を超えている場合はエラーメッセージを送信
            message = (
                f"<@{user}> 申し訳ありません。トークン数が上限を超えています。"
                "新しいスレッドを開始するか、メッセージの文字数を減らして再度お試しください。"
            )
            client.chat_update(channel=channel, ts=wip_message["ts"], text=message)
            return

        response = respond_gpt(messages, model)
        message = f"<@{user}> {response}"
        client.chat_update(channel=channel, ts=wip_message["ts"], text=message)
    except APITimeoutError as e:
        print(f"[ERROR] {e}")
        message = (
            f"<@{user}> 申し訳ありません。タイムアウトが発生しました。\n"
            "再度お試しください。改善されない場合は管理者までご連絡ください。"
        )
        client.chat_update(channel=channel, ts=wip_message["ts"], text=message)
    except Exception as e:
        print(f"[ERROR] {e}")
        message = (
            f"<@{user}> 申し訳ありません。エラーが発生しました。\n"
            f"次のエラー内容を管理者にお伝え下さい。\n{e}"
        )
        client.chat_update(channel=channel, ts=wip_message["ts"], text=message)


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
