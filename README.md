# conpe_prog

競プロのコンテスト用テンプレートを、自動で作るためのセットです。

## できること

- `contest_id`（例: `abc446`, `awc0013`）を指定すると、問題ごとのファイルをまとめて作成します。
- コンテスト種別（`abc` / `awc`）は、`contest_id` の先頭から自動で判定します。

## はじめかた（かんたん3ステップ）

### 1. `uv` をインストールする

このプロジェクトは `uv` を使います。まず `uv` を入れてください。

- 公式ドキュメント: https://docs.astral.sh/uv/getting-started/installation/

### 2. 環境を一発で作る

プロジェクトのルート（この `README.md` がある場所）で、次を実行します。

```bash
uv sync
```

これで必要なパッケージをまとめて準備できます。

### 3. コンテスト用ファイルを生成する

```bash
uv run python tools/gen_contest.py abc446
uv run python tools/gen_contest.py awc0013
```

生成されたファイルは以下の場所に作成されます:
- `abc446` → `atcoder/abc/abc446/` 配下に `a.py` 〜 `g.py`
- `awc0013` → `atcoder/awc/awc0013/` 配下に `a.py` 〜 `e.py`

## VS Code で各問題を実行する

`Code Runner` 拡張を使うと、`a.py` や `b.py` をすぐ実行できます。

- 実行したいファイルを開く
- Windowsの場合：`Alt + Ctrl + N` 
- Macの場合：`Option + Ctrl + N`
- そのファイルが実行される

## 安全動作

- 生成先ディレクトリがすでに存在する場合は、
  `Directory already exists. Aborting.` を表示して終了します。
