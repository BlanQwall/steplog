#!/usr/bin/env python3
from pathlib import Path
from datetime import date, timedelta
import sys

# StepLog 项目根目录（本脚本所在目录）
ROOT = Path(__file__).resolve().parent

# weeklog 目录
OUT_DIR = ROOT / "weeklog"

# 模板文件：英文 + 中文
TEMPLATE_EN = OUT_DIR / "week-template-berlin.html"
TEMPLATE_ZH = OUT_DIR / "week-template-berlin-zh.html"


def get_next_monday(today=None):
    """
    返回下一个周一的 date（如果今天是周一，则返回下周一）。
    """
    if today is None:
        today = date.today()

    # Monday=0, Sunday=6
    weekday = today.weekday()
    days_ahead = (0 - weekday) % 7
    if days_ahead == 0:
        days_ahead = 7
    return today + timedelta(days=days_ahead)


def generate_week_page(template_path: Path, out_path: Path, week_str: str):
    """
    从指定模板生成周页面：
    - 读取模板
    - 找到包含 'const WEEK_START' 的那一行
    - 替换成给定的 week_str（YYYY-MM-DD）
    - 写出到 out_path
    """
    if not template_path.exists():
        print(f"Template not found: {template_path}", file=sys.stderr)
        return

    print(f"Generating from {template_path.name} for week {week_str} -> {out_path}")

    content = template_path.read_text(encoding="utf-8")
    lines = content.splitlines()

    new_lines = []
    replaced = False

    for line in lines:
        if "const WEEK_START" in line:
            # 保留原行的前导空白缩进
            prefix = line[: len(line) - len(line.lstrip())]
            new_line = f'{prefix}const WEEK_START = "{week_str}";'
            new_lines.append(new_line)
            replaced = True
        else:
            new_lines.append(line)

    if not replaced:
        print(
            f"WARNING: WEEK_START line not found in template {template_path.name}.",
            file=sys.stderr,
        )

    new_content = "\n".join(new_lines)
    out_path.write_text(new_content, encoding="utf-8")
    print(f"Done writing {out_path}")


def main():
    next_monday = get_next_monday()
    week_str = next_monday.isoformat()  # "YYYY-MM-DD"

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # 输出文件名约定：
    #   英文：week-YYYY-MM-DD.html
    #   中文：week-YYYY-MM-DD-zh.html
    out_en = OUT_DIR / f"week-{week_str}.html"
    out_zh = OUT_DIR / f"week-{week_str}-zh.html"

    # 如已存在则提示覆盖
    for out_path in (out_en, out_zh):
        if out_path.exists():
            print(f"Target file already exists and will be overwritten: {out_path}")

    # 生成英文页面
    generate_week_page(TEMPLATE_EN, out_en, week_str)
    # 生成中文页面
    generate_week_page(TEMPLATE_ZH, out_zh, week_str)


if __name__ == "__main__":
    main()
