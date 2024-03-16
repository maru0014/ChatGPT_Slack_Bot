# 公式のPythonイメージをベースにする
FROM python:3.12-slim

# アップデート
RUN apt-get update \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/*

# requirements.txtをコピーしてpip installを実行
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# appフォルダ内の全てのファイルをコンテナ内にコピー
COPY /app .

# app.pyを実行
CMD ["python", "app.py"]
