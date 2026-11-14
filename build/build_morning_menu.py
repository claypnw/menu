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
                  "record": "..."}],
   "night_reports": [{"name": "the report's plain name, with its date",
                      "slug": "copy slug or null",
                      "href": "https://... or /local/path/file.pdf"}]}
  A link whose href is an http(s) URL is used as it stands. A link whose
  href is a local file path is copied into the menu repository as
  morning-files/<date>-<slug><ext> (the item's slug names the copy) and the
  page links to it relatively.
  The night_reports list carries every report created during the night
  just ended that is not already linked from a numbered item (added
  2026-11-11 — the admin's order: all the reports created during the
  night stand on this menu). The builder prints them as a standing
  "Reports from last night" section after the filament section: a web
  address is used as it stands; a local file is copied into the menu
  repository as reports/<date>/<slug><ext> in the same publish run and
  linked relatively. An empty or missing list prints the quiet-night
  line in the section, so the section stands every morning.
  The builder renumbers the items by their order in the record (1, 2, 3, ...)
  and rewrites the leading number in each item's first link text to match,
  so the numbers printed on the page always run in sequence from 1,
  whatever slot numbers the record carries (added 2026-11-11 — the admin's
  order: menu numbers in sequential order starting with one).
  The builder also reads the standing filament ad file
  ~/workspace/morning-post/filament-ad.md (written each morning by the daily
  filament sale check) when it stands, and prints it as a section of its
  own after the numbered items: first line the headline, each following
  line one line of the ad.

Output (one publish run of the GitHub key program, repository "menu"):
  morning.html            — the standing page, rebuilt every morning
  morning-<date>.html     — the dated archive copy (same bytes)
  morning-files/<date>-<slug><ext> — one per copied item report file
  reports/<date>/<slug><ext> — one per copied night-report file

Usage:
  build_morning_menu.py [--date YYYY-MM-DD] [--local-only]
  --local-only writes the page and copies under
  ~/workspace/morning-post/batch/menu-out-<date>/ and publishes nothing
  (the test road). Without it, the run publishes.

Ends with VERDICT: PASS or FAIL — <reason>. Exit 0 on PASS, 1 on FAIL.
"""
import html
import json
import re
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
AD_FILE = HOME / "workspace/morning-post/filament-ad.md"

CSS = """
body { font-family: Georgia, 'Times New Roman', serif; background: #fffdf5; color: #111;
       max-width: 44rem; margin: 0 auto; padding: 1.2rem 1rem 3rem; line-height: 1.45; }
h1 { font-size: 1.6rem; border-bottom: 3px solid #8a6d3b; padding-bottom: .4rem; }
p.sub { color: #5a4d33; }
ol { padding-left: 0; list-style: none; }
li { margin: 0 0 1.1rem 0; font-size: 1.05rem; }
li a { font-weight: bold; }
.status { display: block; margin-top: .15rem; }
.decisions { margin-top: 1.6rem; }
.filament { margin-top: 1.6rem; }
.night { margin-top: 1.6rem; }
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
    for display_n, item in enumerate(items, start=1):
        links_html = []
        for link_i, link in enumerate(item.get("links") or []):
            href = link.get("href", "")
            raw_text = link.get("text", "")
            if link_i == 0:
                # The page number is the item's position on the page, not
                # the slot number the record may carry: strip any leading
                # "N · " and print the sequential number instead.
                raw_text = re.sub(r"^\s*\d+\s*·\s*", "", raw_text)
                raw_text = f"{display_n} · {raw_text}"
            text = html.escape(raw_text)
            if href.startswith("http://") or href.startswith("https://"):
                final = href
            else:
                src = Path(href)
                if not src.exists():
                    fail(f"report file for item {display_n} not found: {href}")
                slug = item.get("slug")
                if not slug:
                    fail(f"item {display_n} links a local file but names no slug")
                target = f"morning-files/{day}-{slug}{src.suffix}"
                copies.append((src, target))
                final = target
            links_html.append(f'<a href="{html.escape(final)}">{text}</a>')
        if not links_html:
            fail(f"item {display_n} carries no links")
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

    # The filament ad section: the standing file the daily filament sale
    # check writes. First line is the headline; each following line is one
    # line of the ad. No file (or an empty file) means no section.
    ad_lines = []
    if AD_FILE.exists():
        ad_lines = [ln.strip() for ln in AD_FILE.read_text().splitlines() if ln.strip()]
    if ad_lines:
        ad_lis = "".join(f"<li>{html.escape(ln)}</li>" for ln in ad_lines[1:])
        filament_html = (
            f'<div class="filament"><p><b>{html.escape(ad_lines[0])}</b></p>'
            f"<ul>{ad_lis}</ul></div>"
        )
    else:
        filament_html = ""

    # The night reports section: every report created during the night
    # just ended that is not already linked from a numbered item (the
    # admin's order, 2026-11-11). A web address is used as it stands; a
    # local file is copied into the repository under reports/<date>/
    # in this same publish run and linked relatively. An empty list
    # prints the quiet-night line, so the section stands every morning.
    night_reports = record.get("night_reports") or []
    nr_rows = []
    for nr_i, nr in enumerate(night_reports, start=1):
        name = nr.get("name", "")
        href = nr.get("href", "")
        if not name or not href:
            fail(f"night report {nr_i} lacks a name or an href")
        if href.startswith("http://") or href.startswith("https://"):
            final = href
        else:
            src = Path(href)
            if not src.exists():
                fail(f"night report file not found: {href}")
            slug = nr.get("slug")
            if not slug:
                fail(f"night report {nr_i} links a local file but names no slug")
            target = f"reports/{day}/{slug}{src.suffix}"
            copies.append((src, target))
            final = target
        nr_rows.append(f'<li><a href="{html.escape(final)}">{html.escape(name)}</a></li>')
    if nr_rows:
        night_html = (
            '<div class="night"><p><b>Reports from last night:</b></p><ul>'
            + "".join(nr_rows)
            + "</ul></div>"
        )
    else:
        night_html = (
            '<div class="night"><p><b>Reports from last night:</b> '
            "none — no reports were created last night.</p></div>"
        )

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
{filament_html}
{night_html}
{decisions_html}
<p class="foot">This page is rebuilt every morning. Anyone holding this page's address can open it and the reports behind it.</p>
</body>
</html>
"""

    print(f"numbering: {len(rows)} items numbered 1..{len(rows)} in order")
    print("filament ad: " + (f"section included, {len(ad_lines)} lines from {AD_FILE}"
                             if ad_lines else "no ad file — section left off"))
    print("night reports: " + (f"{len(nr_rows)} listed"
                               if nr_rows else "none — quiet-night line printed"))

    if local_only:
        out = LOCAL_OUT / day
        (out / "morning-files").mkdir(parents=True, exist_ok=True)
        (out / "morning.html").write_text(page)
        (out / f"morning-{day}.html").write_text(page)
        for src, target in copies:
            dest = out / target
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dest)
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
            staged.parent.mkdir(parents=True, exist_ok=True)
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
