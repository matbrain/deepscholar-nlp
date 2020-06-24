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

## データのダウンロード
ドキュメント，アノテーション，設定データを作業ディレクトリにダウンロードする．
```
$ python download.py config.json
```

次に，deepscholarのワークスペース内にある`Categories`タブの`Export`ボタンを押して，設定ファイルをダウンロードする．
設定ファイルは，`config.json`で設定した`WORKING_DIR`内に，`categories.json`という名前で保存する．

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
