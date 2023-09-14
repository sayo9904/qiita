---
title: conda vs pip+venv
tags:
  - 'Python'
private: true
updated_at: ''
id: null
organization_url_name: null
slide: false
---
## 背景
私は2018年ごろ私自身の初めてのプログラミング言語としてPythonを知り、それ以来Pythonの環境管理ツールとして **conda** を愛用してきました。

その理由として、2018年当時私が身を置いていた自然科学計算の畑において conda の使用が推奨されていたことが非常に大きいです。
当時、必須である numpy 等の他言語で書かれたライブラリをインストールする際に pip では安定性に欠けるとされていたことや、「Anaconda をインストールしておけば大体使える」という導入の手軽さからなどから、その分野では conda の使用が非常に一般的だったように感じます。

現在私は某SIerに入社し、エンジニアとして社会に出ました。
仕事をしていくうちに、今まで疑うことなく使ってきたcondaの弱みなどが見えてくるようになりました。
この機会にパッケージ管理・環境管理ツールとしての conda と pip+venv を比較し、自分自身の考えを改める場とします。

## 想定読者
- Python初学者
- Pythonでのパッケージ管理ツールについて悩んでいる人
- condaから抜け出したい人
- 私のファン

## パッケージ管理について


## conda vs pip+venv
~~タイトル回収ｷﾀｰｰｰ~~

### 各種コマンドについて
| 項目 | conda | pip+venv |
| ---- | ----- | -------- |
| 環境の作成 | `conda create -n {env}` | `python -m venv {env}` |
| 環境の起動 | `conda activate {env}` | `./{env}/Scripts/activate` |
| 環境の終了 | `conda deactivate` | `deactivate` |
| 環境の削除 | `conda remove -n {env}` | `rm ./{env}` |
| 環境内のパッケージ一覧 | `conda list` | `pip list` |
| パッケージ追加 | `conda install {package}` | `pip install {package}` |
| ファイルから一括インストール | `` | `pip install -r requirements.txt` |



### その他の比較
- conda はpowershellを起動したら絶対`(base)`ってつくからうざい
- conda のほうがライブラリが乏しい場合すらある
- venvは1ワークスペースに対して1環境という思想
- 

## 比較のまとめ
condaはライブラリ事態は中央管理し、書く環境からシンボリックリンクしているので不整合が怖い
pipは書く環境にいらないディレクトリができるのうざい 起動コマンド長い