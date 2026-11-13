#!/usr/bin/env python3
"""检查 Skill 元数据、Markdown 链接、远程规范引用和专业 Skill 名称引用。"""

from pathlib import Path
import re
import sys
import unicodedata
from urllib.parse import unquote, urlsplit

# 本仓库 standards 对外发布的原始地址前缀；指向它的链接按本地文件与锚点核对。
REMOTE_STANDARDS = "/red-berry-kit/skills/main/standards/"


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


def documents(root):
    """读取 Skill 包内全部 Markdown、standards 与 README；tests 只保存历史证据，不参与检查。"""
    found = []
    for skill in sorted(root.glob("*/SKILL.md")):
        found.extend(sorted(skill.parent.rglob("*.md")))
    found += sorted(root.glob("standards/*.md"))
    if (root / "README.md").is_file():
        found.append(root / "README.md")
    return found


def check(root):
    entries = documents(root)
    skills = sorted(root.glob("*/SKILL.md"))
    if not skills:
        return ["没有找到 Skill"]
    names = {p.parent.name for p in skills}
    local_anchors = {p.name: anchors(p.read_text()) for p in (root / "standards").glob("*.md")}
    errors = []
    for entry in entries:
        text = entry.read_text()
        if entry.name == "SKILL.md":
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
        for name in re.findall(r"`((?:redberry-[a-z-]+)|using-redberry)`", text):
            if name not in names:
                errors.append(f"{entry}: 未提供被引用的 Skill {name}")
        links = re.findall(r"!?\[[^\]\n]*\]\(([^)\s]+)(?:\s+[^)]*)?\)", text)
        links += re.findall(r"^\s{0,3}\[[^\]\n]+\]:\s*(\S+)", text, re.MULTILINE)
        for link in links:
            url = urlsplit(link.strip("<>"))
            if url.scheme in {"http", "https", "mailto"}:
                if REMOTE_STANDARDS in url.path:
                    target = url.path.split(REMOTE_STANDARDS, 1)[1]
                    fragment = unquote(url.fragment)
                    if target not in local_anchors:
                        errors.append(f"{entry}: 远程规范文件不存在 {link}")
                    elif fragment and fragment not in local_anchors[target]:
                        errors.append(f"{entry}: 远程规范锚点不存在 {link}")
                continue
            target = (entry.parent / unquote(url.path)).resolve() if url.path else entry.resolve()
            if url.scheme or not target.is_relative_to(root.resolve()) or not target.is_file():
                errors.append(f"{entry}: 包内链接无效 {link}")
            elif url.fragment and target.suffix == ".md" and unquote(url.fragment) not in anchors(target.read_text()):
                errors.append(f"{entry}: 锚点不存在 {link}")
    return errors


if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent
    errors = check(root)
    for error in errors:
        print(error, file=sys.stderr)
    print(f"检查 {len(list(root.glob('*/SKILL.md')))} 个 Skills，{len(errors)} 个问题")
    sys.exit(bool(errors))