---
title: condaを愛用してきた学生が社会に出てcondaを卒業しpip+venvに乗り換えるまで
tags:
  - Python
  - pip
  - Anaconda
  - 新卒エンジニア
  - venv
private: true
updated_at: '2023-09-16T19:30:07+09:00'
id: 1ead4603ad04950f1bdc
organization_url_name: null
slide: false
---
## 背景
私は2018年ごろ私自身の初めてのプログラミング言語としてPythonを知り、それ以来Pythonのパッケージ管理・環境管理ツールとして **conda** を愛用してきました。

その理由として、2018年当時私が身を置いていた自然科学計算の分野において conda の使用が推奨されていたことが非常に大きいです。
当時 numpy 等の他言語で書かれたライブラリをインストールする際に pip では安定性に欠けるとされていたこと[^1]や、「Anaconda をインストールしておけば大体使える」という導入の手軽さからなどから、その分野では conda の使用が非常に一般的だったように感じます。
[^1]: [WindowsにPython3系とnumpy・scipyをインストールする方法（2017-04-13）](https://mstn.hateblo.jp/entry/2017/04/13/014519)


現在私は某SIerに入社し、エンジニアとして仕事を始めました。
仕事をしていくうちに、今まで大きく疑うことなく使ってきた conda の弱みなどが見えてくるようになりました。
結局私は conda から pip+venv に乗り換えようという決意をしました。

この記事では、そう決めるに至るまでの考えと、実際に移行するにあたり行った準備についてお話しします。


## 想定読者
- Python初学者
- Pythonでのパッケージ管理ツールについて悩んでいる人
- condaから抜け出したい人
- 私のファン

## 筆者の執筆時の環境
- Windows 10 pro
- Python 3.11.5
- pip 23.2.1


## 用語の紹介
### pip
**pip** はPython標準のパッケージ管理ツールです。
パッケージ管理ツールは統一的な操作（コマンド）で各種パッケージのインストール/アンインストールを行えるようにしたり、パッケージ間のバージョン依存関係を解決してくれるのに役立つツールです。

### venv
**venv** はPython標準の環境管理ツールです。
環境管理とは、ワークスペースや作業の目的ごとに異なる環境を用意し管理することです。プロジェクトごとに環境を分けることで、不意の依存問題が起きるリスクを最小限に抑えたり、作業環境を移したり配布したりする際に必要最低限で安全な環境をパッケージングしやすくなる等のメリットがあります。

### conda 
**conda** は科学計算向けPythonディストリビューションである Anaconda に付属するパッケージ管理・環境管理・バージョン管理ツールです。
冒頭で触れたとおり科学計算の分野では C や Fortran などの他言語で書かれたライブラリを使用することがよくあり、かつてはこれらを pip で安全にインストールするのは困難なこともありました。conda はそのようなライブラリをコンパイル済みのバイナリとして独自のリポジトリに保持し、ユーザーはそのチャンネルからインストールすることができます。


## なぜ conda をやめたのか？
前段で紹介したように、conda は pip, venv の機能に加え、pyenv 等で行うような Python 自体のバージョン管理も行うことができる、いわば「全部入り管理ツール」です。さらに、冒頭でお話ししたように私のバックグラウンドも考えると、conda は本当に最高のツールでした。そういうわけで、私は少しばかりのこだわりを持って conda を愛用してきました。

ところが、仕事をするうえではこのこだわりは邪魔になりました。
pip はpython標準のツールですから、例えば適当なサーバーでpythonの環境をゼロベースで構築しようとしたとき、yum や apt で python を入手するだけで pip, venv を使えるというのは、それだけで大きなメリットです。
そもそも仕事の場においては conda の使い方を知らない人のほうが当然多いです。仮に pip, venv も知らないとしても、それでも学習コストは conda のほうが高くなるでしょう。中途半端に conda と pip を混ぜて使用すると依存関係に問題が生じる恐れもあります。

このように私を取り巻く状況がいつの間にか変化していることに気づいたとき、今後も conda を使い続ける意味はあるのだろうか、と考えました。結局、
1. conda よりも pip のほうが一般的であること
2. 仕事の範囲では pip で困る状況が少ないと考えられること
3. そもそも科学計算分野でも近年では pip でのインストールが安定的に提供されていること

という3点で、conda からの脱却を決めました。


## conda / pip+venv
実際のところ、conda と pip+venv にはどのような違いがあるのでしょうか。
この2者を主要な機能で比較してみましょう。

### パッケージ編 (conda / pip)
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


### 環境編 (conda / venv)
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


## 使用感を変えないために
エイリアス書こう



## 参考
1. [Python Japan | Conda と pip](https://www.python.jp/install/anaconda/pip_and_conda.html)
2. [Python Japan | Conda と venv](https://www.python.jp/install/anaconda/conda_and_venv.html)
