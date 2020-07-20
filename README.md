# deepscholar-nlp
deepscholarからのデータ取得と，自然言語処理によるテキストマイニングを実行するプログラム


## 環境設定
`config_sample.json`をコピーして`config.json`を作成し，以下の項目を環境に合わせて書き換える．
* `API_ENDPOINT`: APIのエンドポイント（`https://xxx.deepscholar.app/api/v1`）
* `USER_TOKEN`: deepscholarのトークン（settings画面から自分のトークンを確認できる）
    * トークンは他人に共有しないように注意
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

`WORKING_DIR`内には，以下のファイルがダウンロードされる．
* documents.json
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
        * "_": 次の文字との間にスペースや改行は無い
        * "S": 次の文字との間にスペースがある
        * "N": 次の文字との間に改行がある


## アノテーションファイルを出力
ダウンロードしたファイルを組み合わせて，アノテーションファイルを生成する．
```
$ python gen_anno.py config.json
```

各ドキュメントごとに，`.anno`ファイルが生成される．元ドキュメントがPDFファイルの場合は，
`.txt`ファイルも出力される．  
`.anno`ファイルは以下のような形式となる．

```
9203	9212	Material	userA	9639-9649-Process	output
9203	9212	Material	userB	9639-9649-Process	output
9336	9337	Material	userA	9389-9394-Process	input
9336	9337	Material	userB	9389-9394-Process	input
9346	9347	Material	userA	9389-9394-Process	input
9346	9347	Material	userB	9389-9394-Process	input
9363	9364	Material	userA	9389-9394-Process	input
9363	9364	Material	userB	9389-9394-Process	input
```
* 1列目: アノテーションの開始文字のインデックス
    * 0始まりで，スペースや改行文字も１文字にカウント
* 2列目: アノテーションの終了文字のインデックス
    * 0始まりで，スペースや改行文字も１文字にカウント
* 3列目: アノテーションのカテゴリ
* 4列目: アノテーションを行ったユーザー名
    * ユーザーが存在しない場合はユーザー
* 5列目: 親ノードのアノテーションID
    * 開始文字，終了文字，カテゴリを連結した文字列
    * 親ノードが存在しなければ出力されない
* 6列目: プロパティ（親と子の関係ラベル）
    * 親ノードが存在しなければ出力されない


## License
MIT
