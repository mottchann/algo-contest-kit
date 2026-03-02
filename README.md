# conpe_prog

競プロのコンテスト用テンプレートを自動生成するための構成です。

## 追加した構成

- `config/contests.yaml`
  - コンテスト種別ごとの設定（保存先・問題数・URL形式・テンプレート）
- `templates/python/common.py`
- `templates/python/abc.py`
- `templates/python/awc.py`
  - 生成時に各問題ファイルへ貼り付けるテンプレート本体
- `tools/gen_contest.py`
  - `contest_id` を受け取り、設定に従ってファイルを生成

## 使い方

### 1. 依存パッケージ

`PyYAML` が必要です。

```bash
pip install pyyaml
```

### 2. 生成実行

```bash
python tools/gen_contest.py abc446
python tools/gen_contest.py awc0013
```

`contest_id` の先頭（`abc` / `awc`）から自動判別します。

## 生成仕様

例: `abc446` の場合

- 生成先: `atcoder/abc/abc446/`
- 生成ファイル: `a.py` ~ `g.py`
- 各ファイルの1行目:
  - `# https://atcoder.jp/contests/abc446/tasks/abc446_a` など
- 2行目以降:
  - `templates/python/abc.py` の内容をそのまま貼り付け

例: `awc0013` の場合

- 生成先: `atcoder/awc/awc0013/`
- 生成ファイル: `a.py` ~ `e.py`
- URL形式は同様
- 2行目以降は `templates/python/awc.py`

## 安全動作

- 生成先ディレクトリが既に存在する場合は、
  `Directory already exists. Aborting.` を出して終了します。
