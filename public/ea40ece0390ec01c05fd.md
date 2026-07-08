---
title: CIにバレないようにこっそりpushする
tags:
  - Git
  - GitHub
  - 個人開発
  - GitHubActions
private: false
updated_at: '2026-02-04T01:19:42+09:00'
id: ea40ece0390ec01c05fd
organization_url_name: null
slide: false
ignorePublish: false
posting_campaign_uuid: null
agreed_posting_campaign_term: false
---
## 想定シチュエーション
- 個人開発で、一日の進捗をとりあえずpushしたいが、テストやビルドが通らないことは分かりきっているので CI は動いてほしくないとき
- チームメンバーにとりあえずのレビューをもらいたいのでpushしたいが、テストやビルドが通らない...（以下同文）

## このコマンドを打っておこう
```bash
git commit --allow-empty -m "[skip ci]"
git push origin HEAD
```

### ポイント
1. Githubの場合、`[skip ci]` のようなキーワードを含むコミットメッセージをHEADにしてpushすると GitHub Actions の実行をスキップできる。
2. `git commit` には `--allow-empty` というオプションがあり、ステージングが空でもコミットを作成することができるようになる。

## 参考資料
- [GitHubドキュメント ワークフロー実行をスキップする](https://docs.github.com/ja/actions/how-tos/manage-workflow-runs/skip-workflow-runs)
- [Qiita gitで空コミットするにはgit commit --allow-empty](https://qiita.com/lni_T/items/36abcff16256282a1a6e)
