# deepscholar-nlp
deepscholarからのデータを取得と，自然言語処理によるテキストマイニングを実行するプログラム

## 環境設定
`config_sample.json`をコピーして`config.json`を作成し，以下の項目を環境に合わせて書き換える．
* `API_ENDPOINT`: APIのエンドポイント（`https://xxx.deepscholar.app/api/v1`）
* `USER_TOKEN`: deepscholarのトークン（settings画面から自分のトークンを確認できる）
* `WORKSPACE`: ワークスペース名
* `WORKING_DIR`: 作業ディレクトリのパス．例えば，`work`という名前のディレクトリを作成して設定する．

`config.json`は任意の名前に変更しても良い．

python 3.xをインストールして，`requests`パッケージをインストールする．
```
$ pip install requests
```

## データのダウンロード
ドキュメント，アノテーション，その他の設定データを作業ディレクトリにダウンロードする．
```
$ python download.py config.json
```

## CoNLLフォーマットへ変換
データをCoNLLフォーマット（自然言語処理で標準的に用いられているフォーマット）へ変換する．
```
$ python gen_conll.py config.json
```
