#!/usr/bin/env python3
"""校验 SKILL.md 的 frontmatter 是否符合技能加载契约。

CI 里跑：python3 tools/check_skill.py
"""

import re
import sys

import yaml

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
REQUIRED = ("name", "description")


def main(path="SKILL.md"):
    text = open(path, encoding="utf-8").read()
    if not text.startswith("---"):
        sys.exit("frontmatter 缺失：首行必须是 ---")
    parts = text.split("---", 2)
    if len(parts) < 3:
        sys.exit("frontmatter 未闭合：需要一个结束的 ---")
    data = yaml.safe_load(parts[1])
    if not isinstance(data, dict):
        sys.exit("frontmatter 必须是映射")
    for key in REQUIRED:
        if not data.get(key):
            sys.exit(f"缺少必填字段：{key}")
    if not NAME_RE.match(data["name"]):
        sys.exit(f"name 不合规（要 kebab-case）：{data['name']}")
    desc = str(data["description"]).strip()
    if len(desc) > 900:
        sys.exit(f"description 过长（{len(desc)} 字符），会挤占目录预算")
    if "Use when" not in desc and "使用时机" not in desc:
        print("warn: description 里没有明确的触发条件（Use when …）")
    for camel in ("disableModelInvocation", "modelInvocable", "userInvocable"):
        if camel in data:
            sys.exit(f"驼峰字段会导致技能被忽略：{camel} → 改成 kebab-case")
    print(f"ok: name={data['name']}, description={len(desc)} 字符")
    return 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
