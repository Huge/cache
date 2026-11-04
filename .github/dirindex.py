#!/usr/bin/env python3
"""Write an `ls -l`-style index.html into every directory that lacks one."""
import html, os, subprocess, sys, urllib.parse

root = sys.argv[1] if len(sys.argv) > 1 else "."

# Last commit date per file, from a single git log pass (newest first).
dates = {}
log = subprocess.run(["git", "-C", root, "log", "--format=@%cs", "--name-only", "-z"],
                     capture_output=True, text=True).stdout
date = ""
for tok in log.replace("\n", "\0").split("\0"):
    if tok.startswith("@"):
        date = tok[1:]
    elif tok:
        dates.setdefault(tok, date)

for d, dirs, files in os.walk(root):
    dirs[:] = sorted(x for x in dirs if not x.startswith(".") and x != "__pycache__")
    if "index.html" in files:
        continue
    rel = os.path.relpath(d, root)
    title = "/" if rel == "." else f"/{rel}/"
    rows = [] if rel == "." else [("../", "-", "")]
    rows += [(x + "/", "-", "") for x in dirs]
    for f in sorted(files):
        if f.startswith("."):
            continue
        p = os.path.join(d, f)
        key = os.path.normpath(os.path.join(rel, f))
        rows.append((f, str(os.path.getsize(p)), dates.get(key, "")))
    w = max(len(r[1]) for r in rows) if rows else 1
    lines = "\n".join(
        f'{date:10}  {size:>{w}}  <a href="{urllib.parse.quote(name)}">{html.escape(name)}</a>'
        for name, size, date in rows)
    with open(os.path.join(d, "index.html"), "w") as out:
        out.write(f'<!doctype html><meta charset="utf-8"><meta name="viewport" '
                  f'content="width=device-width"><title>{html.escape(title)}</title>'
                  f'<h1>{html.escape(title)}</h1><pre>\n{lines}\n</pre>\n')
