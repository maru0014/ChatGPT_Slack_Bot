# ChatGPT Slack Bot

## プロジェクトの概要

- 社内のSlack上でChatGPTを使えるようにして生産性向上を図ります
- OpenAI APIを用いることでデータが学習されてしまうことを防ぎます

## インストール

このプロジェクトをローカルにセットアップするには、以下の手順を実行します。

### VSCode DevContainerを利用する場合

1. リポジトリをクローンします：

```sh
git clone https://github.com/maru0014/ChatGPT_Slack_Bot.git
```

2. VSCodeでプロジェクトディレクトリを開きます：
![image](https://github.com/maru0014/ChatGPT_Slack_Bot/assets/15005576/10e6ddce-dada-4b82-b25a-e4ae53cc71a8)

3. .envファイルを作成します：

```
SLACK_BOT_TOKEN=xoxb-xxxxxx-xxxxxx-xxxxxx
SLACK_APP_TOKEN=xapp-1-xxxxxx-xxxxxx-xxxxxx
OPENAI_API_KEY=sk-xxxxxx
DEFAULT_MODEL=gpt-4-0125-preview
```

4. コンテナーで開きます：
![image](https://github.com/maru0014/ChatGPT_Slack_Bot/assets/15005576/48dc2fd7-94f1-4b63-8fcf-f9abb90ed883)




## 実行手順
アプリケーションを実行するには、以下のコマンドを実行します：

```sh
python app/app.py
```

## Dockerで実行する場合

Dockerを使用してプロジェクトをセットアップする場合は、以下の手順を実行します：

1. Dockerイメージをビルドします：
```sh
docker build -t chatgpt-slack-bot .
```

2. Dockerコンテナを実行します：
```sh
docker run --env-file .env chatgpt-slack-bot
```
