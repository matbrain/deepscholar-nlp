# deepscholar-nlp
deepscholar APIを用いてデータ取得を行うプログラムです．


## 環境設定
`config_sample.json`をコピーして`config.json`を作成し，以下の項目を環境に合わせて書き換えます．
* `API_ENDPOINT`: APIのエンドポイント（`https://xxx.deepscholar.app/api/v1`）
* `USER_TOKEN`: deepscholarのAPIトークン（画面右上のユーザー名 → Settings → APIから自分のトークンを確認できます）
    * トークンは他人に共有しないように注意してください．
* `WORKSPACE`: deepscholarのワークスペース名
* `WORKING_DIR`: 作業ディレクトリのパス．例えば，`work`という名前のディレクトリを作成して，そのパスを設定します．

`config.json`は任意の名前に変更しても動作します．

python 3.xをインストールして，`requests`パッケージをインストールします．
```
$ pip install requests
```
Python 3.8で動作確認済です．

## データのダウンロード
ドキュメント，アノテーション，各種設定データを作業ディレクトリにダウンロードします．
```
$ python download.py config.json
```

`WORKING_DIR`内には，以下のファイルがダウンロードされます．
* documents.json
* entities.json
* nodes.json
* categories.json
* members.json
* 各ドキュメントデータ（.pdf, .txt）
* (PDFの場合のみ)PDFからテキスト抽出したファイル（.pdf.txt.gz）
    * PDFに含まれる文字と位置のrawデータ
    ```
    1	P	59.5275 37.153248 7.1581764 14.151969	_
    1	r	66.68568 37.153248 4.976352 14.151969	_
    1	e	71.662025 37.153248 6.8443522 14.151969	_
    1	p	78.50638 37.153248 7.4720006 14.151969	_
    ```
    * 1列目: ページ番号
    * 2列目: 文字
    * 3列目: 文字の位置（x, y, width, height）
    * 4列目: 区切り文字
        * `_`: 次の文字との間にスペースや改行は無い
        * `S`: 次の文字との間にスペースがある
        * `N`: 次の文字との間に改行がある


## アノテーションファイルを出力
ダウンロードしたファイルを組み合わせて，アノテーションファイルを生成します．
必ず`データのダウンロード`を実行した後に作業を行ってください．

```
$ python gen_anno.py config.json
```

各ドキュメントごとに，`.anno`ファイルが生成されます．ドキュメントがPDFファイルの場合は，`.txt`ファイルも出力されます．

`.anno`ファイルは以下のような形式となります．

```
-1	-1	_	_	9389-9394-Process	entity	Seal
-1	-1	_	_	9441-9446-Process	entity	Heat/Press
-1	-1	_	_	9389-9394-Process	entity	Seal
9203	9212	Material	userA	9639-9649-Process	output	_
9203	9212	Material	userB	9639-9649-Process	output	_
9336	9337	Material	userA	9389-9394-Process	input	_
9336	9337	Material	userB	9389-9394-Process	input	_
9346	9347	Material	userA	9389-9394-Process	input	_
9346	9347	Material	userB	9389-9394-Process	input	_
9363	9364	Material	userA	9389-9394-Process	input	_
9363	9364	Material	userB	9389-9394-Process	input	_
```
* 1列目: アノテーションの開始文字のインデックス
    * 0始まりで，スペースや改行文字も１文字にカウント
    * -1のときは，アノテーションではない（string, float, entityのいずれか）
* 2列目: アノテーションの終了文字のインデックス
    * 0始まりで，スペースや改行文字も１文字にカウント
    * -1のときは，アノテーションではない（string, float, entityのいずれか）
* 3列目: アノテーションのカテゴリ
* 4列目: アノテーションを行ったユーザー名
    * ユーザーが存在しない場合はユーザー
* 5列目: 親ノードのアノテーションID
    * 開始文字，終了文字，カテゴリを連結した文字列
    * 親ノードが存在しなければ出力されない
* 6列目: プロパティ（親と子の関係ラベル）
    * 親ノードが存在しなければ出力されない
* 7列目: プロパティ（親と子の関係ラベル）
    * プロパティの値（string, float, entityの場合のみ有効）


## License
MIT
