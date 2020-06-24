# deepscholar-nlp
deepscholarからのデータ取得と，自然言語処理によるテキストマイニングを実行するプログラム

## 環境設定
`config_sample.json`をコピーして`config.json`を作成し，以下の項目を環境に合わせて書き換える．
* `API_ENDPOINT`: APIのエンドポイント（`https://xxx.deepscholar.app/api/v1`）
* `USER_TOKEN`: deepscholarのトークン（settings画面から自分のトークンを確認できる）
* `WORKSPACE`: deepscholarのワークスペース名
* `WORKING_DIR`: 作業ディレクトリのパス．例えば，`work`という名前のディレクトリを作成して設定する．

`config.json`は任意の名前に変更しても良い．

python 3.xをインストールして，`requests`パッケージをインストールする．
```
$ pip install requests
```
Python 3.8で動作確認済．

## データのダウンロード
ドキュメント，アノテーション，設定データを作業ディレクトリにダウンロードする．
```
$ python download.py config.json
```

次に，deepscholarのワークスペース内にある`Categories`タブの`Export`ボタンを押して，設定ファイルをダウンロードする．
設定ファイルは，`WORKING_DIR`内に`categories.json`という名前で保存する．

最終的に，`WORKING_DIR`内には，以下のファイルがダウンロードされる．
* documents.json
* nodes.json
* categories.json
* 各ドキュメントデータ

## CoNLLフォーマットへ変換
データをCoNLLフォーマット（自然言語処理で標準的に用いられているフォーマット）へ変換する．
```
$ python gen_conll.py config.json
```
`WORKING_DIR`内に`xxx.conll`が生成される．

以下のようなCoNLLファイルが生成される．
```
A	_	O	_
s	S	O	_
f	_	B-category	8040 relation
e	_	I-category	_
a	_	I-category	_
t	_	I-category	_
u	_	I-category	_
r	_	I-category	_
e	_	I-category	_
d	S	E-category	_
i	_	O	_
n	_	O	_
:	N	O	_
S	_	O	_
```
* 1列目: 文字
* 2列目: 区切り文字
    * `S`: 直後にスペース文字がある
    * `N`: 直後に改行がある
    * `_`: それ以外
* 3列目: スパンのBIOEタグ
* 4列目: 親ノードのidとプロパティ（関係ラベル）
    * 上記の例だと，`featured`というスパンの親は，8040行目から始まるスパンで，関係ラベルは`relation`ということを表す．

## スパンアノテーションの学習
Comming soon

## 関係アノテーションの学習
Comming soon

## License
MIT
