#!/usr/bin/env python3
"""Validate a Claude SKILL.md against the ~/.claude/skills contract.

Usage:
  python3 verify_skill.py                       # checks ~/.claude/skills/*/SKILL.md
  python3 verify_skill.py /path/to/SKILL.md     # checks one file

Checks: frontmatter delimited by '---' on line 1, a non-empty 'name' and
'description' key, and a non-empty markdown body.
"""
import sys, os, glob

def parse(path):
    text = open(path, encoding="utf-8").read()
    lines = text.splitlines()
    errs = []
    if not lines or lines[0].strip() != "---":
        errs.append("frontmatter must start with '---' on line 1")
        return errs, None, None, 0
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        errs.append("frontmatter is not closed with a second '---'")
        return errs, None, None, 0
    fm = {}
    for line in lines[1:end]:
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    body = "\n".join(lines[end + 1:]).strip()
    name = fm.get("name")
    desc = fm.get("description")
    if not name:
        errs.append("missing 'name' in frontmatter")
    if not desc:
        errs.append("missing 'description' in frontmatter")
    if not body:
        errs.append("body is empty")
    return errs, name, desc, len(body)

def check(path):
    print("checking", path)
    errs, name, desc, blen = parse(path)
    if errs:
        for e in errs:
            print("FAIL", e)
        print("RESULT: install is INVALID")
        return False
    print("OK  name=%s" % name)
    print("OK  description present (%d chars)" % len(desc))
    print("OK  frontmatter delimited by --- on line 1")
    print("OK  body present (%d chars)" % blen)
    print("RESULT: install is valid — Claude will discover %s" % name)
    return True

def main():
    if len(sys.argv) > 1:
        paths = sys.argv[1:]
    else:
        paths = sorted(glob.glob(os.path.expanduser("~/.claude/skills/*/SKILL.md")))
        if not paths:
            print("no skills found under ~/.claude/skills/")
            sys.exit(1)
    ok = all(check(p) for p in paths)
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
