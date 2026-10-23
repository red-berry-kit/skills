#!/usr/bin/env python3
"""检查 Skill 元数据、包内 Markdown 链接和专业 Skill 名称引用。"""

from pathlib import Path
import re
import sys
import unicodedata
from urllib.parse import unquote, urlsplit


def anchors(text):
    result, counts = set(), {}
    for title in re.findall(r"^#{1,6}\s+(.+?)\s*#*\s*$", text, re.MULTILINE):
        title = title.lower().replace("`", "")
        slug = "".join(
            c for c in title if unicodedata.category(c)[0] not in "PS" or c in "-_"
        ).replace(" ", "-")
        count = counts.get(slug, 0)
        counts[slug] = count + 1
        result.add(f"{slug}-{count}" if count else slug)
    return result


def check(root):
    skills = sorted(root.glob("*/SKILL.md"))
    names = {p.parent.name for p in skills}
    errors = []
    if not skills:
        return ["没有找到 Skill"]
    for entry in skills:
        text = entry.read_text()
        parts = text.split("---\n", 2)
        if len(parts) != 3 or parts[0]:
            errors.append(f"{entry}: frontmatter 缺失")
            continue
        fields = dict(re.findall(r"^(name|description):\s*(.+)$", parts[1], re.MULTILINE))
        if fields.get("name") != entry.parent.name:
            errors.append(f"{entry}: name 与目录不一致")
        description = fields.get("description", "")
        if not description.startswith("Use when ") or re.search(r"[\u3400-\u9fff]", description):
            errors.append(f"{entry}: description 应为英文触发条件")
        if len(description) > 1024:
            errors.append(f"{entry}: description 过长")
        for name in re.findall(r"`((?:redplum-[a-z-]+)|using-redplum)`", text):
            if name not in names:
                errors.append(f"{entry}: 未提供被引用的 Skill {name}")
        for document in entry.parent.rglob("*.md"):
            content = document.read_text()
            links = re.findall(r"!?\[[^\]\n]*\]\(([^)\s]+)(?:\s+[^)]*)?\)", content)
            links += re.findall(r"^\s{0,3}\[[^\]\n]+\]:\s*(\S+)", content, re.MULTILINE)
            for link in links:
                url = urlsplit(link.strip("<>"))
                if url.scheme in {"http", "https", "mailto"}:
                    continue
                target = (document.parent / unquote(url.path)).resolve() if url.path else document.resolve()
                if url.scheme or not target.is_relative_to(entry.parent.resolve()) or not target.is_file():
                    errors.append(f"{document}: 包内链接无效 {link}")
                elif url.fragment and target.suffix == ".md" and unquote(url.fragment) not in anchors(target.read_text()):
                    errors.append(f"{document}: 锚点不存在 {link}")
    return errors


if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent
    errors = check(root)
    for error in errors:
        print(error, file=sys.stderr)
    print(f"检查 {len(list(root.glob('*/SKILL.md')))} 个 Skills，{len(errors)} 个问题")
    sys.exit(bool(errors))
