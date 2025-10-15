---
title: 出来るだけクリーンに Windowsで Dockerを使えるようにする
tags:
  - WSL2
  - Docker
  - Docker Engine
  - 環境構築
private: false
updated_at: ""
id: null
organization_url_name: null
slide: false
ignorePublish: false
---

## 想定読者

- Windows をなるべく汚さずに Docker を利用したい人
- Docker Desktop for Windows を使わずに WSL で Docker を使いたい人

:::note info
この記事の多くは各ツールの公式ページからの引用で構成されています。
ググり力（ぐぐりぢから）のある読者の方は、この記事を参考にするよりもご自身で調べていただくほうがより新しく正確な情報を得られるかもしれません。
:::

## この記事で目指すところ

- Windows で WSL を使えるようにする
  - Docker Desktop は利用しない
  - その他 WSL 以外の一切のツールも Windows 側では設定しない
- WSL で Dokcer コマンドを使えるようにする
  - Docker Desktop を先に立ち上げておく...などの事前準備なく、ただ WSL にログインするだけでいつでも Docker コマンドが利用できる状態にする

## 筆者の環境

- Windows 11 Pro （クリーンインストール直後で、特別な設定などはしていない状態）
- VSCode 1.97.2

## 手順

:::note info
以下で特に断りがない限り、各コマンドは PowerShell で実行してください。
:::

### WSL に Ubuntu をインストールする

1. PowerShell で以下のコマンドを実行し、WSL を有効化します。
   ```powershell
   wsl --install
   ```
2. ターミナルの表示に従い、コンピューターを再起動します。
3. 再起動後に再び PowerShell を起動し、以下のコマンドで WSL2 をデフォルトバージョンに設定します。
   ```powershell
   wsl --set-default-version 2
   ```
4. WSL にインストール可能なディストリビューションを検索します。
   ```powershell
   wsl -l -o
   ```
5. 検索結果の中から好きなディストリビューションを選んでインストールします。ここでは Ubuntu24.02 をインストールします。
   ```powershell
   wsl --install -d Ubuntu-24.04
   ```
6. Ubuntu24.04 がインストールされたことを確認します。
   ```powershell
   wsl -l -v
   ```
7. WSL を起動します。
   ```powershell
   wsl -d Ubuntu-24.04
   ```
8. 初回起動時はユーザーの作成を促されます。任意のユーザー名とパスワードを入力してください。
9. WSL が起動すると、プロンプトが PowerShell のものとは少し変わります。WSL 起動後のターミナルで以下のコマンドを実行し、Ubuntu24.04 が起動していることを確認します。
   ```bash
   cat /etc/os-release
   ```

### Docker Engine をインストールする

:::note warn
以下の手順は Ubuntu 用の手順です。
Ubuntu 以外のディストリビューションで DockerEngine をインストールする場合、[公式ドキュメント](https://docs.docker.com/engine/install/)を参考にインストールを実施してください。
:::

1. インストールした Linux ディストリビューションを起動します。前段の手順で WSL が既に起動している場合、この手順は不要です。
   ```powershell
   wsl
   ```
2. Docker の公式 GPG キーを追加します。

   ```bash
   curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
   ```

3. Docker リポジトリを追加します。

   ```bash
   sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
   ```

4. パッケージリストを更新し、Docker Engine をインストールします。

   ```bash
   sudo apt-get update
   sudo apt-get install docker-ce docker-ce-cli containerd.io
   ```

5. Docker サービスを開始します。

   ```bash
   sudo service docker start
   ```

6. Docker が正しくインストールされたことを確認します。
   ```bash
   sudo docker run hello-world
   ```

## 参考資料

1. [【Microsoft 公式】WSL のインストール手順](https://learn.microsoft.com/ja-jp/windows/wsl/install)
2. [【Docker 公式】Install Docker Engine on Ubuntu](https://docs.docker.com/engine/install/ubuntu/)
