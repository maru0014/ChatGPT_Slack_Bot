import os

import openai


def respond_gpt(messages: list, model: str) -> str:
    """
    OpenAIのChatGPTを使って応答を取得します
    """
    timeout = int(os.environ.get("TIMEOUT_SECONDS", 30))
    completion = openai.chat.completions.create(
        model=model,
        messages=messages,
        timeout=timeout,
    )
    response_message = completion.choices[0].message.content
    return response_message


if __name__ == "__main__":
    # メッセージの例
    messages = [{"role": "user", "content": "こんにちは"}]

    # モデルの例
    model = "gpt-3.5-turbo"

    # ChatGPTの応答
    response = respond_gpt(messages, model)
    print(f"応答: {response}")
