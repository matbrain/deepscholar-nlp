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


## アノテーションファイルを出力
```
$ python gen_anno.py config.json
```

各ドキュメントごとに，`.txt`ファイルと`.anno`ファイルが生成される．  
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
    * 0始まり
* 2列目: アノテーションの終了文字のインデックス
    * 0始まり
* 3列目: アノテーションのカテゴリ
* 4列目: アノテーションを行ったユーザー名
    * ユーザーが存在しない場合はユーザーID
* 5列目: 親ノードのアノテーションID
    * 開始文字，終了文字，カテゴリを連結した文字列
    * 親ノードが存在しなければ出力されない
* 6列目: プロパティ（親と子の関係ラベル）
    * 親ノードが存在しなければ出力されない


## スパンアノテーションの学習
Comming soon


## 関係アノテーションの学習
Comming soon


## License
MIT
