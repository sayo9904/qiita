---
title: condaを愛用してきた学生が社会に出てcondaを卒業しpip+venvに乗り換えるまで
tags:
  - Python
  - pip
  - Anaconda
  - 新卒エンジニア
  - venv
private: false
updated_at: '2023-09-18T00:20:37+09:00'
id: b877e9b1509fdca5004c
organization_url_name: null
slide: false
---
## 想定読者
- Pythonでのパッケージ管理ツールについて悩んでいる人
- なんとなく conda を使っている人
- condaから抜け出したい人


## 登場人物の紹介
- **筆者**
  2018年頃から科学計算領域で Python@Anaconda を使い始める。
  就職後社会での conda の肩身の狭さを感じ、最近は conda を卒業しようと考えている。
- **conda**
  Anacondaディストリビューションに含まれるパッケージ・環境・バージョン管理ツール
- **pip**
  Python標準のパッケージ管理ツール
- **venv**
  Python標準の環境管理ツール


## 筆者の執筆時の環境
- Windows 10
- Python 3.11.5
- pip 23.2.1


## conda の明暗
### なぜ conda だったのか？
Python に触れたのが「科学計算領域の人間として」であったことが何よりも大きいです。この領域で conda が好まれていたのには以下のような理由がありました。
- Anaconada に付属する管理ツールであること。Anaconda は、これをインストールするだけで numpy, scipy, matplotlib などの科学計算分野で人気なライブラリが一気に入手できるので人気だった。
- その当時は  numpy などの他言語で書かれたライブラリを pip でインストールするのは困難な場合があった。


### なぜ conda をやめたいのか？
今や私はITエンジニアとして社会にいます。Python を使い始めたころとは時代も私を取り巻く環境も変わり、以下のようなことが気になり始めてきました。
- conda を好んで使う人が少ないこと。
- 仕事の範囲では pip で困る状況が少ないと考えられること。
- numpy や tensorflow などの科学計算ライブラリすらも、近年では pip でのインストールが安定的に提供されていること。

特に1点目は仕事においては非常に重要なことだと思います。
環境構築の手順書を書いたり、あるいは開発環境を他の人に譲渡するときに conda での管理が前提のものであると、チームや相手に大きな負担をかけてしまいます。

そして同時に、conda の乗り換え先としては**Pyhon標準である pip+venv が適切**だと考えました。


## conda / pip+venv
実際のところ、conda と pip+venv にはどのような違いがあるのでしょうか。この2者を主要な機能で比較してみましょう。

### パッケージ編 (conda / pip)
| 項目 | conda | pip+venv |
| ---- | ----- | -------- |
| パッケージ追加 | `conda install {package}` | `pip install {package}` |
| パッケージ一覧 | `conda list` | `pip list` |
| ファイルに出力 | `conda list --export > packages.txt` | `pip freeze > requirements.txt` |
| ファイルからインストール | `conda install --file packages.txt` | `pip install -r requirements.txt` |
| パッケージの一覧 | `conda list` | `pip list` |
| パッケージソース[^packageInstallSource] | Anaconda repo and Cloud | PyPI |

[^packageInstallSource]: [Anaconda | Understanding Conda and Pip](https://www.anaconda.com/blog/understanding-conda-and-pip)

conda と pip では、全くと言って良いほど同じような使用感でコマンドを叩くことができます。
ビルドの差などから conda のほうが高速に動くライブラリがあったり[^runSpeedConpare]、pip がサポートする PyPI のほうがより多くのパッケージが提供されている等の違いがあります。

[^runSpeedConpare]: [Anaconda の NumPy が高速みたいなので試してみた](https://tech.morikatron.ai/entry/2020/03/27/100000)


### 環境編 (conda / venv)
| 項目 | conda | pip+venv |
| ---- | ----- | -------- |
| 環境の作成 | `conda create -n {env}` | `python -m venv {env}` |
| 環境の起動 | `conda activate {env}` | `./{env}/Scripts/activate` |
| 環境の終了 | `conda deactivate` | `deactivate` |
| 環境の削除 | `conda remove -n {env}` | `rm ./{env}` |

venv はコマンドがどれも冗長に感じます。特に activate はめんどくさいです。
venv ではカレントディレクトリに環境名と同名のディレクトリが作られ、その配下に環境の情報が保持されます。環境の起動コマンドはそのディレクトリ内にあるバッチファイルが実体なので、このように冗長になってしまうのです。一方で conde は `~/Anaconda/envs/` 以下に各環境の情報が保持されます。
「venv は1ワークスペース（=ディレクトリ）に対して1環境」という思想であり、A というディレクトリで作った envA は別のディレクトリ B からは呼び出せません。一方で conda は環境を中央管理しているので、作業するディレクトリに関わらずどこからでもどの環境でも再利用できます。


### 比較まとめ
- conda と pip は変わらない使用感で移行できる
- pip のほうが一般的で情報も多く、広く利用しやすい
- venv はコマンドが冗長
- venv は環境の実態がディレクトリなので削除が簡単


## pip+venv を快適に使うために
conda を長年使ってきた身からすると、venv のコマンドの冗長さは耐え難いものがあります。
そこで私は、こちらの [**エイリアスの作成（引数が複数ある場合）【BashとPowerShellの比較】**](https://qiita.com/karakuri-t910/items/d751987065d4c52b3af4) の記事をを参考にし、`$profile` にコマンドを登録しました。
今回は conda と似た使用感で venv を使いたいので、私は以下のように登録しました。

```powershell:$profile
function create() {
  python -m venv $args
}

function activate() {
  . .\$args\Scripts\activate
}
```

これで、conda と似た感覚で、環境の作成～起動～終了は
```powershell:powershell
create {envname}
```
```powershell:powershell
activate {envname}
```
```powershell:powershell
deactivate
```
でそれぞれ行うことができるようになります。


## 最後に
この記事では触れませんでしたが conda の持つ機能として、Python自体のバージョンの切り替え というものがあります。これを vanilla python でやるには py launcher や pyenv などのツールが必要になります。

この記事は「conda を卒業しよう！」と決めてから2週間ほどで執筆しました。まだ見落としている pip+venv が有利な点・不利な点があるかもしれませんが、素直に向き合って、仲良くしていこうと思います。

## 参考
1. [Python Japan | Conda と pip](https://www.python.jp/install/anaconda/pip_and_conda.html)
2. [Python Japan | Conda と venv](https://www.python.jp/install/anaconda/conda_and_venv.html)
