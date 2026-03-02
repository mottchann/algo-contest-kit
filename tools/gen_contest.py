from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    import yaml
except ModuleNotFoundError as exc:
    raise SystemExit(
        "PyYAML が必要です。`pip install pyyaml` を実行してください。"
    ) from exc

ROOT_DIR = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT_DIR / "config" / "contests.yaml"


def load_config(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"設定ファイルが見つかりません: {path}")
    with path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file)
    if not isinstance(data, dict) or "contest_types" not in data:
        raise ValueError("設定ファイルの形式が不正です。contest_types が必要です。")
    return data


def infer_contest_type(contest_id: str) -> str | None:
    lowered = contest_id.lower()
    if lowered.startswith("abc"):
        return "abc"
    if lowered.startswith("awc"):
        return "awc"
    return None


def validate_contest_id(contest_id: str) -> None:
    lowered = contest_id.lower()
    if not (lowered.startswith("abc") or lowered.startswith("awc")):
        raise ValueError(
            "contest_id は abc446 や awc0013 のように入力してください。"
        )
    suffix = lowered[3:]
    if not suffix.isdigit() or int(suffix) < 1:
        raise ValueError("contest_id の数値部分は 1 以上の自然数にしてください。")


def generate(contest_id: str) -> Path:
    contest_id = contest_id.lower()
    validate_contest_id(contest_id)

    config = load_config(CONFIG_PATH)
    contest_types = config["contest_types"]

    resolved_type = infer_contest_type(contest_id)
    if resolved_type is None:
        raise ValueError("contest_id の接頭辞を abc/awc にしてください。")

    resolved_type = resolved_type.lower()
    if resolved_type not in contest_types:
        raise ValueError(f"未対応のコンテスト種別です: {resolved_type}")

    contest_conf = contest_types[resolved_type]
    root_dir = ROOT_DIR / contest_conf["root_dir"]
    target_dir = root_dir / contest_id

    if target_dir.exists():
        print("Directory already exists. Aborting.")
        sys.exit(1)

    template_path = ROOT_DIR / contest_conf["template_file"]
    if not template_path.exists():
        raise FileNotFoundError(f"テンプレートが見つかりません: {template_path}")

    template_body = template_path.read_text(encoding="utf-8").rstrip() + "\n"
    target_dir.mkdir(parents=True, exist_ok=False)

    for task in contest_conf["tasks"]:
        url = contest_conf["url_template"].format(contest_id=contest_id, task=task)
        filename = contest_conf["filename_template"].format(
            contest_id=contest_id,
            task=task,
        )
        content = f"# {url}\n" + template_body
        (target_dir / filename).write_text(content, encoding="utf-8")

    return target_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="ABC/AWC のコンテスト用ファイルを自動生成します。"
    )
    parser.add_argument("contest_id", help="例: abc446, awc0013")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    created_dir = generate(args.contest_id)
    print(f"Created: {created_dir}")


if __name__ == "__main__":
    main()
