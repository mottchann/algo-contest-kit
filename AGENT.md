競プロのコンテスト用ファイルの自動作成

方針
自動でテンプレートが作成されるようにしたい。
ABCとAWCに対応させたい。

設計
ABCディレクトリ配下にabcXXXディレクトリを作成(XXXは1以上の自然数)
abcXXXディレクトリ内にa.py, b.py, c.py, d.py, e.py, f.py, g.pyの7ファイルを作成
それぞれのpyファイルの1行目にabcXXXに対応する問題のURLを記載
2行目以降はモジュールや関数などテンプレートファイルと同様

構成
"""
conpe_prog/
  README.md

  config/
    contests.yaml                 # 動的要素（問題数/URL/配置/テンプレ指定/例外）を全部ここに集約

  tools/
    gen_contest.py                # 生成スクリプト（contest_id を受け取り、YAMLに従って作成）

  templates/
    python/
      common.py                   # 共通テンプレ（imports, II/LI/LMI, 定番関数など）
      abc.py                      # ABC用テンプレ（common + ABC固有差分があるなら）
      awc.py                      # AWC用テンプレ（common + AWC固有差分があるなら）

  atcoder/
    abc/
      abc446/
        a.py
        b.py
        c.py
        d.py
        e.py
        f.py
        g.py
      abc447/
        a.py
        ...
    awc/
      awc0013/
        a.py
        b.py
        c.py
        d.py
        e.py
      awc0014/
        a.py
        ...   
"""

templates/ は “生成に使う資材置き場”
atcoder/ 以下は “生成される作業場（解答置き場）”
tools/ は “生成器（スクリプト）置き場”

URL作成ルール
https://atcoder.jp/contests/{contest_id}/tasks/{contest_id}_{letter}

コンテストidは手入力で受け取る

URLの違いはgenで埋める
テンプレで先頭に {URL} のプレースホルダ（または固定コメント行）して、genファイルでURLを生成して先頭行に書く。
例：各 a.py の1行目だけ # <URL> を書く、2行目以降はテンプレ貼り付け。

変わり得るもの（問題数・URL形式・保存先など）を全部 YAML に寄せる

# config.yaml
contest_types:
  abc:
    root_dir: "atcoder/abc"
    tasks: ["a","b","c","d","e","f","g"]
    url_template: "https://atcoder.jp/contests/{contest_id}/tasks/{contest_id}_{task}"
    filename_template: "{task}.py"
    template_file: "templates/python/common.py"

  awc:
    root_dir: "atcoder/awc"
    tasks: ["a","b","c","d","e"]
    url_template: "https://atcoder.jp/contests/{contest_id}/tasks/{contest_id}_{task}"
    filename_template: "{task}.py"
    template_file: "templates/python/common.py"

ディレクトリが存在したら終了にする
if os.path.exists(target_dir):
    print("Directory already exists. Aborting.")
    sys.exit(1)