# ChatGPT Slack Bot

## プロジェクトの概要

- 社内のSlack上でChatGPTを使えるようにして生産性向上を図ります
- OpenAI APIを用いることでデータが学習されてしまうことを防ぎます

## インストール

このプロジェクトをローカルにセットアップするには、以下の手順を実行します。

### VSCode DevContainerを利用する場合

1. リポジトリをクローンします：

```sh
git clone <リポジトリのURL>
```

2. VSCodeでプロジェクトディレクトリを開きます：

3. .envファイルを作成します：

```
SLACK_BOT_TOKEN=xoxb-xxxxxx-xxxxxx-xxxxxx
SLACK_APP_TOKEN=xapp-1-xxxxxx-xxxxxx-xxxxxx
OPENAI_API_KEY=sk-xxxxxx
DEFAULT_MODEL=gpt-4-0125-preview
```

4. コンテナーで開きます：




## 実行手順
アプリケーションを実行するには、以下のコマンドを実行します：

```sh
python app/app.py
```

## Dockerで実行する場合

Dockerを使用してプロジェクトをセットアップする場合は、以下の手順を実行します：

1. Dockerイメージをビルドします：
```sh
docker build -t <イメージ名> .
```

2. Dockerコンテナを実行します：
```sh
docker run --env-file .env <イメージ名>
```
