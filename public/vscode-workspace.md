---
title: VSCode の Workspace で task を使おう
tags:
  - 環境設定
  - VSCode
private: false
updated_at: '2026-07-09T09:21:31+09:00'
id: 0a048c025695ebf5dc5b
organization_url_name: null
slide: false
ignorePublish: false
posting_campaign_uuid: null
agreed_posting_campaign_term: false
---

## この記事は何？

- VSCodeのworkspace機能を理解する
- 複数のディレクトリをまたいだタスクを定義して、プロジェクト全体の開発を容易にする
  ※workspaceでtasksを定義できることに気づいたのが執筆のきっかけでした

## workspaceとは？

VSCodeで複数のディレクトリを同時に開くことができる機能です。
フロントエンドとバックエンドのディレクトリを同時に開いて使ったり、
フロントエンドとAPIモックサーバーを起動して開発を進めたり、活用シチュエーションは多くはないが無いわけではない、筆者にとってはそんな立ち位置です。

![workspaceで2つのディレクトリを開いた様子](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3557028/a978ad44-cc0b-4c9d-9a93-05c8c620f7a2.png)

## workspaceの始め方

詳細な手順は他者の記事等に譲ります。簡単に一言だけ説明すると、コマンドパレットやメニューから「ワークスペースにフォルダーを追加」を選択することで2つ目のフォルダを画面上に追加できます。

このワークスペースの情報（どのフォルダとどのフォルダを開いているか？）は「名前を付けてワークスペースを保存」から `.code-workspace` という拡張子のファイルとして保存できます。この設定ファイルが今回のキモになります。

保存する際、保存場所はどこでも構いませんが、本記事では以下のような構成になっている想定で話を進めます。
（設定ファイル中に相対パスの記述が出てきます）

```bash
~/
├── frontend/                       # ディレクトリ1
├── backend/                        # ディレクトリ2
└── vscode-workspaces/              # workspace設定ファイル置き場
    └── myWebApp.code-workspace     # 今回のworkspaceの設定ファイル
```

## 設定ファイルを深堀りしてみる

以下に今回の説明用のサンプルの設定ファイルを示します。
この設定ファイルは `folders`, `settings`, `tasks` の3つの要素から構成されています。

```json:myWebApp.code-workspace
{
  "folders": [
    {
      "name": "frontend",
      "path": "../frontend"
    },
    {
      "name": "backend",
      "path": "../backend"
    }
  ],
  "settings": {
    "editor.tabSize": 2,
    "editor.formatOnSave": true
  },
  "tasks": {
    "version": "2.0.0",
    "tasks": [
      {
        "label": "start frontend",
        "type": "shell",
        "command": "yarn dev",
        "options": {
          "cwd": "${workspaceFolder:frontend}",
        },
        "presentation": {
          "reveal": "always",
          "group": "dev-server",
        },
      },
      {
        "label": "start backend",
        "type": "shell",
        "command": "go run .",
        "options": {
          "cwd": "${workspaceFolder:backend}",
        },
        "presentation": {
          "reveal": "always",
          "group": "dev-server",
        },
      },
      {
        "label": "start all",
        "dependsOn": ["start frontend", "start backend"],
      },
    ],
  }
}
```

`folders` はワークスペースに追加するディレクトリの情報を記述します。`name` はフォルダにつくエイリアス的な命名、`path` はそのディレクトリのパスです（ワークスペース設定ファイルからの相対パス）。
`folders.path` は `.code-workspace` ファイルに必須の要素らしく、特に自分でカスタマイズせずとも、GUI操作でワークスペースを作成した時点で自動的に定義されます。

`settings` はVSCodeの設定を記述します。記述方法は VSCode の文脈で広く登場する `settings.json` と同じです。
正直に言うとこれは不要だと思います。
ディレクトリごとに言語が違えば使いたい設定は異なるので各ディレクトリ側に `settings.json` を持たせる方が合理的ですし、
言語が同じだとしてもエディタ自体の設定に入れてしまえば済みますからね。

`tasks` はVSCodeのタスクを定義することができます。
こちらも一般的な `tasks.json` と同じ書き方で定義できます。
今回のサンプルでは、FEの起動、BEの起動、FE/BE両方の同時起動の3つのタスクを定義しています。

### workspaceでtasksを使うメリット

通常 workspace を開いた状態でターミナルを開くと、複数抱えているディレクトリのうちのどれか1つのディレクトリの位置でアタッチします（上記の例はおそらくFEのパスからスタートします）。
このような事情があるため、コマンドラインからBEの操作をしようとするときには `cd ../backend` のコマンドを1つ挟む必要があり、これが地味なストレスでした。

今回、workspace自体にタスクを持たせることで、任意のコマンドを好きな方のディレクトリから実行できるようになり、考えることを1つ減らすことができました。
また当然、GUI操作一発でFE/BEの両方を起動できるようにもなりました。

## 余談

もしかすると `launch` や `extentions.recommendations`、 `snippets` のような key も使えるかもしれませんね。

あと、devcontainerとの相性は良くないどころか最悪です。
ローカルに環境を立てている人向けになるかもしれませんね（今更ｗ）。

## 参考資料

- [VS Code のワークスペースをちゃんと使いたい - Qiita](https://qiita.com/amac-53/items/86b1466e93524844c2a8)
- [Integrate with External Tools via Tasks - VSCode official](https://code.visualstudio.com/docs/debugtest/tasks)
- [【VSCode】開発環境を自動で立ち上げる - Zenn](https://zenn.dev/kazuwombat/articles/d9512aebbbae07)
