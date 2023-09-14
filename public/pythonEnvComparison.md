---
title: condaを愛用してきた学生が社会に出てcondaを卒業する話
tags:
  - 'Python'
  - 'Anaconda'
  - 'pip'
  - 'venv'
  - '新卒エンジニア'
private: true
updated_at: ''
id: null
organization_url_name: null
slide: false
---
## 背景
私は2018年ごろ私自身の初めてのプログラミング言語としてPythonを知り、それ以来Pythonのパッケージ管理・環境管理ツールとして **conda** を愛用してきました。

その理由として、2018年当時私が身を置いていた自然科学計算の分野において conda の使用が推奨されていたことが非常に大きいです。
当時、必須である numpy 等の他言語で書かれたライブラリをインストールする際に pip では安定性に欠けるとされていたこと[^1]や、「Anaconda をインストールしておけば大体使える」という導入の手軽さからなどから、その分野では conda の使用が非常に一般的だったように感じます。
[^1]: [WindowsにPython3系とnumpy・scipyをインストールする方法（2017-04-13）](https://mstn.hateblo.jp/entry/2017/04/13/014519)


現在私は某SIerに入社し、エンジニアとして仕事を始めました。
仕事をしていくうちに、今まで疑うことなく使ってきたcondaの弱みなどが見えてくるようになりました。
この機会にパッケージ管理・環境管理ツールとしての conda と pip+venv を比較し、自分自身の考えを改める場とします。


## 想定読者
- Python初学者
- Pythonでのパッケージ管理ツールについて悩んでいる人
- condaから抜け出したい人
- 私のファン


## パッケージ管理について
パッケージ管理ツールは統一的な操作（コマンド）で各種パッケージのインストール/アンインストールを行えるようにしたり、パッケージ間のバージョン依存関係を解決してくれるのに役立つツールです。
Python では標準で pip が用意されています。


## 環境管理について
環境管理とは、ワークスペースや作業の目的ごとに異なる環境を用意し管理することです。
プロジェクトごとに環境を分けることで、不意の依存問題が起きるリスクを最小限に抑えたり、作業環境を移したり配布したりする際に必要最低限で安全な環境をパッケージングしやすくなる等のメリットがあります。
Python では環境管理ツールとして標準で venv が用意されています。


## conda について
conda は科学計算向けPythonディストリビューションである Anaconda に付属するパッケージ管理・環境管理ツールです。
冒頭で触れたとおり科学計算の分野では C や Fortran などの他言語で書かれたライブラリを使用することがよくあり、かつてはこれらを pip で安全にインストールするのは困難なこともありました。
conda はそのようなライブラリをコンパイル済みのバイナリとして独自のリポジトリに保持し、ユーザーはそのチャンネルからインストールすることができます。


## conda vs pip+venv
私が今まで愛用してきた conda と、Python の標準である pip, venv を、主要な機能で比較していきます。

### パッケージ編 (conda vs pip)
| 項目 | conda | pip+venv |
| ---- | ----- | -------- |
| パッケージ一覧 | `conda list` | `pip list` |
| パッケージ追加 | `conda install {package}` | `pip install {package}` |
| ファイルに出力 | `conda list --export > packages.txt` | `pip freeze > requirements.txt` |
| ファイルからインストール | `conda install --file packages.txt` | `pip install -r requirements.txt` |
| パッケージの一覧 | `conda list -e` | `pip list` |
| パッケージソース[^2] | Anaconda repo and Cloud | PyPI |

[^2]: [Anaconda | Understanding Conda and Pip](https://www.anaconda.com/blog/understanding-conda-and-pip)

この表を見る限りでは（そして私の使用感の上でも）conda と pip には大きな差は感じられません。
ビルドの差などから、conda のほうが高速に動くライブラリがあったり[^3]、pip がサポートする PyPI のほうがより多くのパッケージが提供されている等の違いがあります。

[^3]: [Anaconda の NumPy が高速みたいなので試してみた](https://tech.morikatron.ai/entry/2020/03/27/100000)


### 環境編 (conda vs venv)
| 項目 | conda | pip+venv |
| ---- | ----- | -------- |
| 環境の作成 | `conda create -n {env}` | `python -m venv {env}` |
| 環境の起動 | `conda activate {env}` | `./{env}/Scripts/activate` |
| 環境の終了 | `conda deactivate` | `deactivate` |
| 環境の削除 | `conda remove -n {env}` | `rm ./{env}` |

venv はコマンドがどれも冗長に感じます。特に activate はめんどくさいです。
venv ではカレントディレクトリに環境名と同名のディレクトリが作られ、その配下に環境の情報が保持されます。環境の起動コマンドはそのディレクトリ内にあるバッチファイルが実体なので、このように冗長になってしまうのです。
一方で conde は `~/Anaconda/envs/` 以下に各環境の情報が保持されます。
従って、「venv は1ワークスペース（=ディレクトリ）に対して1環境」という思想であり、A というディレクトリで作った envA は別のディレクトリ B からは呼び出せません。
一方で conda は環境を中央管理しているので、作業するディレクトリに関わらずどこからでもどの環境でも再利用できます。


### 実務編
> ここからは私の主観でのお話になります。

今まで私は少しばかりのこだわりを持って conda を愛用してきましたが、仕事をするうえでこのこだわりは邪魔になりました。
pip はpython標準のツールですから、例えば適当なサーバーでpythonの環境をゼロベースで構築しようとしたとき、yum や apt で python を入手するだけで pip, venv を使えるというのは、それだけで大きなメリットです。
加えて、仕事においては conda の使い方を知らない人のほうが当然多いです。仮に pip, venv も知らないとしても、それでも学習コストは conda のほうが高くなるでしょう。conda と pip を混ぜて使用すると依存関係に問題が生じる恐れもあります。
このような状況下で conda を使い続けるのはエゴが過ぎます。



## 比較まとめ



## 参考
1. [Python Japan | Conda と pip](https://www.python.jp/install/anaconda/pip_and_conda.html)
2. [Python Japan | Conda と venv](https://www.python.jp/install/anaconda/conda_and_venv.html)