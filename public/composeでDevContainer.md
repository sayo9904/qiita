---
title: APIサーバー + RDB + オブジェクトストレージの開発環境をdevcontainerで実現する
tags:
  - "devcontainer"
  - docker
  - docker-compose
private: false
updated_at: ""
id: null
organization_url_name: null
slide: false
ignorePublish: false
---

## はじめに

### 背景

バックエンド（API サーバー）の開発において、RDB などの周辺システムのモックの設定をめんどくさく感じたので、いっそ Docker で模擬環境を作ってしまおうという試みです。

### この記事のサマリ

docker compose の networks 設定を適切に行うことで、まるで本番のようなサーバー間通信を疑似的に再現可能です。
CRUD に関わる機能や DB マイグレーションの検証などが容易に可能になり、バックエンド開発の体験として素晴らしいです。

## 事前に準備が必要なソフトウェア

### 1. Docker

筆者は Windwos マシンに WSL2 + Docker Engine の構成で Docker を利用していますが、DockerDesktop などでも代替可能と思われます（未検証）。

### 2. VSCode (DevContainer)

DevContainer を利用する都合上、エディタは VSCode またはそのフォークを利用することを前提としています。

[DevContainer](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)拡張のインストールを済ませておいてください。

## この記事で目指すところ

今回はバックエンド開発が主目的であり、その開発を円滑に進めるための環境として RDB やオブジェクトストレージを接続可能な状態に作り上げます。

最終的には以下のような状態を目指します。

1. 開発環境として、Go での開発/実行ができるメイン環境があること
2. Go の環境から ORM や`psql`コマンドなどで接続可能な Postgres サーバーがあること

:::note info
Typescript 環境や Python 環境、MySQL 環境などでも、適切に読み替えていただければ再現可能かと思います。

また、要点を抑えれば フロントエンド/バックエンド を同様の方法で管理することも可能です（利用シチュエーションがあるかは微妙ですが）。
:::

## 環境を作る

### 概観

DevContainer で今回の環境を実現するには、以下のような構造になります。

1. Go / postgres にそれぞれ対応したコンテナが起動している
2. 上記 2 つのコンテナは `compose.yml` によって一元管理されている
3. DevContainer は `compose.yml` を利用して 2 つの環境を立ち上げ、そのうちの Go の環境でエディタを開いた状態にする

つまり、以下のようなファイル群が必要になります。

```bash
.devcontaier/
├compose.yml
├devcontainer.json
├Dockerfile.go
└Dockerfile.postgres
```

### Dockerfile.go

これがメインで触る環境になるので、必要に応じて utils 系もインストールしておきましょう。今回は筆者の好みで言語や TZ の設定を入れていますが、それを除けばほぼほぼ最小構成かと思います。
なお、postgres をインストールしておくことでこのコンテナの bash から `psql` コマンドで DB に接続できるようになります。

```Dockerfile:Dockerfile.go
FROM golang:1.25.5-trixie

RUN apt update && apt install -y \
    locales \
    git\
    sudo \
    postgresql postgresql-contrib \
    && apt clean -y \
    && rm -rf /var/lib/apt/lists/*

RUN sed -i -e 's/# \(ja_JP.UTF-8\)/\1/' /etc/locale.gen \
    && locale-gen \
    && update-locale
ENV LANG=ja_JP.UTF-8

ENV TZ=Asia/Tokyo

RUN useradd -m devuser \
    && echo "devuser ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
USER devuser

WORKDIR /workspace
```

### Dockerfile.postgres

DB の初期化スクリプトなどがある場合は `RUN` で叩いておきましょう。

そういった事前設定が不要な場合は、Dockerfile は用意せずに `compose.yml` の `image` キーに 1 行書くだけでも良いかもしれません。

```Dockerfile:Dockerfile.postgres
FROM postgres:18-alpine

ENV LANG ja_JP.utf8
```

### compose.yml

ここまで紹介した 2 つのコンテナを、それぞれ `app`, `postgres` というサービス名で管理します。

この `compose.yml` を書く際に気を付けたいポイントは以下です。

1. app コンテナ（メインのコンテナ）には `sleep infinity` を付けること
2. すべてのサービスに `networks: - {共通NW}` を指定すること

特に 2 番が重要で、これを設定することでコンテナ間での通信が可能になります。

```yaml:compose.yml
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile.go
    command: sleep infinity
    volumes:
      - ../:/workspace:cached
    networks:
      - dev-network
    environment:
      # RDB接続情報
      - DB_HOST=db
      - DB_PORT=5432
      - DB_USER=postgres
      - DB_PASSWORD=postgres
      - DB_NAME=postgres

  postgres:
    build:
      context: .
      dockerfile: Dockerfile.postgres
    networks:
      - dev-network
    restart: on-failure
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: postgres
    ports:
      - "5432:5432"

networks:
  dev-network:
```

### devcontainer.json

VSCode が直接読み取って環境を構成するための設定ファイルです。
`dockerComposeFile` で先ほど作った `compose.yml` を指定しましょう。

```json:devcontainer.json
{
  "name": "Golang API server development environment",
  "dockerComposeFile": [
    "compose.yml"
  ],
  "service": "app",
  "workspaceFolder": "/workspace",
  "postStartCommand": "go mod tidy",
  "customizations": {
    "vscode": {
      "extensions": [
        "golang.go"
      ],
      "settings": {
        "editor.tabSize": 2,
        "editor.formatOnSave": true,
        "editor.formatOnPaste": true,
        "[dockerfile]": {
          "editor.tabSize": 4
        }
      }
    }
  }
}
```

## 環境を使ってみる

ここまでの全ファイルを `.devcontainer/` ディレクトリにまとめ、コマンドパレットから「コンテナで開く」を実行しましょう。
最初はビルドに時間がかかるかもしれませんが、go の環境にログインできていれば成功です。

```bash:Go環境の確認
devuser@5b62fbc7470e:/workspace$ go version
go version go1.25.5 linux/amd64
```

ここまで来たら、DB への接続確認をしてみましょう。

ここでは `psql` コマンドに `-h` オプションを付け、ホスト名を指定するようにします。ここで指定するホスト名は `compose.yml` で指定したサービス名と対応します。

```bash:DB接続確認
devuser@5b62fbc7470e:/workspace$ psql -h postgres -d postgres -U postgres
ユーザー postgres のパスワード:
psql (17.6 (Debian 17.6-0+deb13u1)、サーバー 18.1)
警告： psql のメジャーバージョンは 17 ですが、サーバーのメジャーバージョンは 18 です。
         psql の機能の中で、動作しないものがあるかもしれません。
"help"でヘルプを表示します。

postgres=#
```

バージョンが新しすぎて（？）警告が出ていますがまあ良いでしょう。

まだテーブル作成などを流し込んでいないので情報は入っていませんが、postgres として動いていることは確認できました。

```postgres
postgres=# \d
リレーションが見つかりませんでした。
```

## さいごに

今回初めて `compose.yml` で DevContainer を構築しました。
複数のコンテナを同時起動できる docker compose の強力さはもちろん、それを開発環境の文脈にうまく落とし込んでいる DevContainer の仕様にも感謝の念が止みません。

これから ORM や DB マイグレーションについて学習していこうとしている身でしたので、このような「まるで DB サーバーが本当に立っている」ような環境を構築でき、非常に満足してます。
今後は、DB の永続化や結合テストへの利用なども検討出来たらよいと思いました。

## 参考資料

1. [【Docker】networks で複数の Docker Compose 環境間を通信可能にする](https://qiita.com/fujita-goq/items/63fc1fb70056b8784dfd)
2. [【Docker 公式】Compose のネットワーク機能](https://docs.docker.jp/compose/networking.html)

## special thanks

1. Gemini 3 Pro
