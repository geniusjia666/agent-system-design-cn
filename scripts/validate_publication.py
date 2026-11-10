#!/usr/bin/env python3
"""Check this repository's Chinese skill publication.

Uses the Python standard library only. It reads files and checks text,
JSON, links, frontmatter, and hashes. It does not import or run the skill.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "agent-system-design-cn"

ORIGINAL = {
    "SKILL.md": ("d34219a7767e1b2cf13a0344215202be9a825cae9d635a729435212db063831d", 15824),
    "references/01-架构选型.md": ("71ccd3bb6ce3140f6db143811bb74327e1bdc26adeb6ec0638e53ac6d9da4fbc", 13358),
    "references/02-单Agent设计.md": ("7ef5da2546b3cf237ad4b8a434933e164d07431367db9a88e1a3ba9d4e80af5c", 16284),
    "references/03-工具设计.md": ("90c1c0b16648b19a546603bb6e46279a0ff6ea126a9c32837568045975a11af8", 19875),
    "references/04-上下文与记忆.md": ("3fe664dd7407a0dc2f9eeeed544aa187f94c06125e30c5413f02350d91f43466", 22821),
    "references/05-编排模式.md": ("012a9e288292a282bda32101637df9ca09193ab41302979e43821a0d40f75cdd", 19552),
    "references/06-多Agent协作.md": ("c0082c585df85beb8b5bc7e3aefbc399c4f942cbabd558bce65390e8f9aacd29", 22481),
    "references/07-人类介入与可靠性安全.md": ("a84a0a7cfa0593190cbcd345f78d0650d2f114d18a76e4af961327364d0c44ef", 23585),
    "references/08-评测与迭代.md": ("6b6d3d28f83b9ea436614508ee7e2f636e14944d3b3e403a314e4bd14efd046b", 30515),
    "references/09-框架落地映射.md": ("0b8fe668df81745a77dc42ae032b9d624d6a4bd60eef726a108e7cef83b0b817", 26674),
    "references/10-设计模式索引.md": ("acc77d8640f2e7714bf1127ce0fecad97f9c1ab1b60ed9eb4611bf3f0e3b6a4b", 30588),
    "assets/设计文档模板.md": ("d25b08e3f7bbbb651c16409b7c9ca04153d383ad205ca0f583fd11fffce86364", 9344),
    "assets/设计自检清单.md": ("4b5c5415bd8a4b949d46a0a980c013fd9c4f2002481e67d0fe041ea6aae80d5c", 37061),
    "assets/交接契约模板.json": ("c0cacde5c6d4eb8efc840213de8f821ae94c9a5e89e4e2c41e9c1d0ac328faeb", 10702),
}

LICENSE_SHA256 = "2b7828ef86aa8958b322836f1b66b4b02e5b95a83ca0ed8fd89f095e75a8203d"
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")


def join(*parts: str) -> str:
    return "".join(parts)


CONTENT_NEEDLES = [
    join("/", "Users/"),
    join("/", "home/"),
    join("/", "tmp/"),
    join("/", "opt/", "cursor"),
    join("/", "workspace"),
    join("C:", "\\"),
    join("-----BE", "GIN "),
    join("AK", "IA"),
    join("gh", "p_"),
    join("github_", "pat_"),
    join("x-access-", "token"),
    join("sk-", "proj"),
    join("sk-", "ant"),
]


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def tracked_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT)
        if rel.parts and rel.parts[0] == ".git":
            continue
        files.append(path)
    return files


def heading_slug(title: str) -> str:
    text = title.strip().lower()
    text = re.sub(r"[^\w\s\-\u4e00-\u9fff]", "", text, flags=re.UNICODE)
    text = re.sub(r"\s+", "-", text)
    return text


def headings(text: str) -> list[str]:
    found = []
    for line in text.splitlines():
        match = HEADING_RE.match(line)
        if match:
            found.append(heading_slug(match.group(2)))
    return found


def check_originals(errors: list[str]) -> int:
    present = [path.relative_to(SKILL).as_posix() for path in SKILL.rglob("*") if path.is_file()]
    if sorted(present) != sorted(ORIGINAL):
        fail(errors, f"skill file list differs: {sorted(present)}")
        return 0
    total = 0
    for rel, (digest, size) in sorted(ORIGINAL.items()):
        data = (SKILL / rel).read_bytes()
        total += len(data)
        if len(data) != size or sha256(data) != digest:
            fail(errors, f"hash mismatch: {rel}")
    expected = sum(size for _, size in ORIGINAL.values())
    if total != expected:
        fail(errors, f"byte total {total} != {expected}")
    return total


def check_utf8(path: Path, errors: list[str]) -> str | None:
    data = path.read_bytes()
    if b"\x00" in data:
        fail(errors, f"NUL byte: {path.relative_to(ROOT)}")
        return None
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError as exc:
        fail(errors, f"UTF-8 decode failed: {path.relative_to(ROOT)}: {exc}")
        return None


def json_fences(text: str) -> list[str]:
    bodies = []
    parts = text.split("```")
    for index, part in enumerate(parts):
        if index % 2 == 0 or not part.startswith("json"):
            continue
        body = part.split("\n", 1)[1] if "\n" in part else ""
        bodies.append(body)
    return bodies


def check_links(path: Path, text: str, errors: list[str]) -> int:
    checked = 0
    for match in LINK_RE.finditer(text):
        target = match.group(1).strip()
        if target.startswith(("http://", "https://", "mailto:")):
            continue
        if target.startswith(("<", "javascript:")) or "://" in target:
            fail(errors, f"unsupported link in {path.relative_to(ROOT)}: {target}")
            continue
        path_part, sep, anchor = target.partition("#")
        if not path_part and not sep:
            fail(errors, f"empty link in {path.relative_to(ROOT)}")
            continue
        dest = path.parent / path_part if path_part else path
        try:
            dest = dest.resolve()
            dest.relative_to(ROOT)
        except ValueError:
            fail(errors, f"link escapes repo: {path.relative_to(ROOT)} -> {target}")
            continue
        if path_part and not dest.is_file():
            fail(errors, f"missing link target: {path.relative_to(ROOT)} -> {target}")
            continue
        checked += 1
        if not anchor:
            continue
        dest_text = dest.read_text(encoding="utf-8")
        if anchor not in headings(dest_text):
            fail(errors, f"missing anchor: {path.relative_to(ROOT)} -> {target}")
    return checked


def check_frontmatter(text: str, errors: list[str]) -> None:
    if not text.startswith("---\n"):
        fail(errors, "SKILL.md has no YAML frontmatter")
        return
    end = text.find("\n---\n", 4)
    if end == -1:
        fail(errors, "SKILL.md frontmatter is not closed")
        return
    block = text[4:end]
    names = [line[len("name:") :].strip() for line in block.splitlines() if line.startswith("name:")]
    if names != ["agent-system-design-cn"]:
        fail(errors, f"frontmatter name is {names!r}")
    descriptions = [line for line in block.splitlines() if line.startswith("description:")]
    if len(descriptions) != 1 or not descriptions[0].split(":", 1)[1].strip():
        fail(errors, "frontmatter description is missing")


def check_required_text(errors: list[str]) -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    required = [
        "# Agent系统设计\n",
        "先判断需不需要多 Agent，再设计它们如何协作",
        "https://github.com/geniusjia666/agent-system-design",
        "https://github.com/geniusjia666/agent-system-design-cn",
        "0.1.0",
        "geniusjia666",
        "不是编排框架",
    ]
    for item in required:
        if item not in readme:
            fail(errors, f"README.md missing {item!r}")
    version = (ROOT / "VERSION").read_text(encoding="utf-8")
    if version.strip() != "0.1.0" or version not in {"0.1.0", "0.1.0\n"}:
        fail(errors, "VERSION must contain only 0.1.0")
    sync = (ROOT / "SYNC.md").read_text(encoding="utf-8")
    for item in (
        "https://github.com/geniusjia666/agent-system-design",
        "https://github.com/geniusjia666/agent-system-design-cn",
        "0.1.0",
        "不是自动同步",
        "手动",
    ):
        if item not in sync:
            fail(errors, f"SYNC.md missing {item!r}")
    license_data = (ROOT / "LICENSE").read_bytes()
    if sha256(license_data) != LICENSE_SHA256:
        fail(errors, "LICENSE bytes changed")
    if "Copyright (c) 2026 Skyler" not in license_data.decode("utf-8"):
        fail(errors, "LICENSE copyright line changed")


def check_debris_and_secrets(files: list[Path], errors: list[str]) -> None:
    debris = (join("__MAC", "OSX"), ".DS_Store", join("._"))
    for path in files:
        rel = path.relative_to(ROOT)
        name = path.name
        posix = rel.as_posix()
        if any(part == debris[0] or part == ".DS_Store" or part.startswith("._") for part in rel.parts):
            fail(errors, f"archive debris: {posix}")
        if name == debris[1] or name.startswith("._"):
            fail(errors, f"archive debris: {posix}")
        text = path.read_bytes().decode("utf-8")
        for needle in CONTENT_NEEDLES:
            if needle in text:
                fail(errors, f"forbidden content {needle!r} in {posix}")
        if join("agent-system-design", "_cn") in posix:
            fail(errors, f"old archive directory name: {posix}")


def main() -> int:
    errors: list[str] = []
    if not SKILL.is_dir():
        fail(errors, "missing skills/agent-system-design-cn")
    total = check_originals(errors)
    files = tracked_files()
    link_count = 0
    json_count = 0
    for path in files:
        text = check_utf8(path, errors)
        if text is None:
            continue
        if path.suffix == ".json":
            try:
                json.loads(text)
            except json.JSONDecodeError as exc:
                fail(errors, f"JSON file invalid: {path.relative_to(ROOT)}: {exc}")
            else:
                json_count += 1
        if path.suffix == ".md":
            for body in json_fences(text):
                try:
                    json.loads(body)
                except json.JSONDecodeError as exc:
                    fail(errors, f"JSON fence invalid: {path.relative_to(ROOT)}: {exc}")
                else:
                    json_count += 1
            link_count += check_links(path, text, errors)
    skill_text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    check_frontmatter(skill_text, errors)
    check_required_text(errors)
    check_debris_and_secrets(files, errors)
    if errors:
        for item in errors:
            print(f"ERROR {item}")
        print(f"FAILED {len(errors)}")
        return 1
    print(f"original_files {len(ORIGINAL)}")
    print(f"original_bytes {total}")
    print(f"utf8_files {len(files)}")
    print(f"json_documents {json_count}")
    print(f"local_links {link_count}")
    print("frontmatter agent-system-design-cn")
    print("version 0.1.0")
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
