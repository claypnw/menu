#!/usr/bin/env python3
"""Build and publish the Morning Menu page — a fixed program (the admin's
production standard, 2026-10-31). The morning-menu job collects the night's
statuses into the menu record; this program does the mechanical part: it
renders the page and publishes it with the day's report files.

Input:  ~/workspace/goals/morning-agenda-briefing/hidden_files/morning-menu-<date>.json
  {"date": "YYYY-MM-DD",
   "items": [{"n": 1, "name": "...", "slug": "kpi" | null,
              "page_status": "the short line printed on the page",
              "status": "the full status (the record's own words)",
              "record": "the named record the status rests on",
              "links": [{"text": "1 · The Payson Morning Scroll",
                         "href": "https://... or /local/path/file.pdf"}]}],
   "decisions": [{"question": "...", "choices": ["...", "..."],
                  "record": "..."}]}
  A link whose href is an http(s) URL is used as it stands. A link whose
  href is a local file path is copied into the menu repository as
  morning-files/<date>-<slug><ext> (the item's slug names the copy) and the
  page links to it relatively.

Output (one publish run of the GitHub key program, repository "menu"):
  morning.html            — the standing page, rebuilt every morning
  morning-<date>.html     — the dated archive copy (same bytes)
  morning-files/<date>-<slug><ext> — one per copied report file

Usage:
  build_morning_menu.py [--date YYYY-MM-DD] [--local-only]
  --local-only writes the page and copies under
  ~/workspace/morning-post/batch/menu-out-<date>/ and publishes nothing
  (the test road). Without it, the run publishes.

Ends with VERDICT: PASS or FAIL — <reason>. Exit 0 on PASS, 1 on FAIL.
"""
import html
import json
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

HOME = Path.home()
RECORD_DIR = HOME / "workspace/goals/morning-agenda-briefing/hidden_files"
PUBLISH = HOME / "workspace/custom-connectors/custom.github/bin/github_publish.py"
LOCAL_OUT = HOME / "workspace/morning-post/batch/menu-out"

CSS = """
body { font-family: Georgia, 'Times New Roman', serif; background: #fffdf5; color: #111;
       max-width: 44rem; margin: 0 auto; padding: 1.2rem 1rem 3rem; line-height: 1.45; }
h1 { font-size: 1.6rem; border-bottom: 3px solid #8a6d3b; padding-bottom: .4rem; }
p.sub { color: #5a4d33; }
ol { padding-left: 1.4rem; }
li { margin: 0 0 1.1rem 0; font-size: 1.05rem; }
li a { font-weight: bold; }
.status { display: block; margin-top: .15rem; }
.decisions { margin-top: 1.6rem; }
.foot { margin-top: 2rem; color: #5a4d33; font-size: .95rem; }
"""


def fail(reason):
    print(f"VERDICT: FAIL — {reason}")
    sys.exit(1)


def main():
    args = sys.argv[1:]
    local_only = "--local-only" in args
    if "--date" in args:
        day = args[args.index("--date") + 1]
    else:
        day = datetime.now(ZoneInfo("America/Phoenix")).strftime("%Y-%m-%d")

    record_path = RECORD_DIR / f"morning-menu-{day}.json"
    if not record_path.exists():
        fail(f"menu record not found: {record_path}")
    try:
        record = json.loads(record_path.read_text())
    except Exception as e:
        fail(f"menu record is not readable JSON: {e}")
    items = record.get("items")
    if not items:
        fail("menu record holds no items")
    decisions = record.get("decisions") or []

    nice_day = datetime.strptime(day, "%Y-%m-%d").strftime("%A, %B %-d, %Y")

    # Resolve links: copy local files to their repository names.
    copies = []  # (source Path, repo-relative target)
    rows = []
    for item in items:
        links_html = []
        for link in item.get("links") or []:
            href = link.get("href", "")
            text = html.escape(link.get("text", ""))
            if href.startswith("http://") or href.startswith("https://"):
                final = href
            else:
                src = Path(href)
                if not src.exists():
                    fail(f"report file for item {item.get('n')} not found: {href}")
                slug = item.get("slug")
                if not slug:
                    fail(f"item {item.get('n')} links a local file but names no slug")
                target = f"morning-files/{day}-{slug}{src.suffix}"
                copies.append((src, target))
                final = target
            links_html.append(f'<a href="{html.escape(final)}">{text}</a>')
        if not links_html:
            fail(f"item {item.get('n')} carries no links")
        status = html.escape(item.get("page_status") or item.get("status") or "")
        rows.append(
            f"<li>{' — '.join(links_html)}"
            f'<span class="status">{status}</span></li>'
        )

    if decisions:
        dec_lines = []
        for d in decisions:
            q = html.escape(d.get("question", ""))
            ch = " / ".join(html.escape(c) for c in d.get("choices") or [])
            dec_lines.append(f"<li>{q}" + (f" — choices: {ch}" if ch else "") + "</li>")
        decisions_html = (
            '<div class="decisions"><p><b>Decisions waiting:</b></p><ul>'
            + "".join(dec_lines)
            + "</ul></div>"
        )
    else:
        decisions_html = '<div class="decisions"><p><b>Decisions waiting:</b> none this morning.</p></div>'

    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Morning Menu — {nice_day}</title>
<style>{CSS}</style>
</head>
<body>
<h1>Morning Menu — {nice_day}</h1>
<p class="sub">{nice_day} — tap any item to open its own report. Come back and tap another any time.</p>
<ol>
{chr(10).join(rows)}
</ol>
{decisions_html}
<p class="foot">This page is rebuilt every morning. Anyone holding this page's address can open it and the reports behind it.</p>
</body>
</html>
"""

    if local_only:
        out = LOCAL_OUT / day
        (out / "morning-files").mkdir(parents=True, exist_ok=True)
        (out / "morning.html").write_text(page)
        (out / f"morning-{day}.html").write_text(page)
        for src, target in copies:
            shutil.copyfile(src, out / target)
        print(f"local build in {out}: morning.html, morning-{day}.html, {len(copies)} report files")
        print("VERDICT: PASS")
        return

    # Publish: stage the files, one run of the key program.
    with tempfile.TemporaryDirectory() as td:
        stage = Path(td)
        (stage / "morning-files").mkdir()
        (stage / "morning.html").write_text(page)
        (stage / f"morning-{day}.html").write_text(page)
        file_args = []
        for name in ("morning.html", f"morning-{day}.html"):
            file_args += ["--file", str(stage / name), name]
        for src, target in copies:
            staged = stage / target
            shutil.copyfile(src, staged)
            file_args += ["--file", str(staged), target]
        cmd = ["python3", str(PUBLISH), "--repo", "menu", "--branch", "main",
               "--message", f"Morning menu — {day}"] + file_args
        res = subprocess.run(cmd, capture_output=True, text=True)
        sys.stdout.write(res.stdout)
        if res.returncode != 0 or "VERDICT: PASS" not in res.stdout:
            fail("the publish program did not end VERDICT: PASS — see its lines above")
    print(f"published morning.html + morning-{day}.html + {len(copies)} report files to claypnw/menu")
    print("VERDICT: PASS")


if __name__ == "__main__":
    main()
