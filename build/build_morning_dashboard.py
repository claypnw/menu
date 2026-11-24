#!/usr/bin/env python3
"""Build and publish the Morning Dashboard page — a fixed program.
The morning-menu job collects the night's statuses into the menu record;
this program does the mechanical part: it renders the dashboard page
(Maggie's dashboard form, the warm tan Skyrim look — Clay's direction,
2026-11-16) and publishes it with the day's report files, at the same
address the Morning Menu page has always stood at, so the admin's
morning link opens the dashboard from 2026-11-16 on.

Input:  ~/workspace/goals/morning-agenda-briefing/hidden_files/morning-menu-<date>.json
  (the same record the menu builder reads — see build_morning_menu.py)
  plus the night KPI record
  ~/workspace/goals/morning-agenda-briefing/hidden_files/morning-kpi-records/night-<date>.json
  for the overnight-run tile, and the standing filament ad file
  ~/workspace/morning-post/filament-ad.md when it stands.

  A link whose href is an http(s) URL is used as it stands. A link whose
  href is a local file path is copied into the menu repository as
  morning-files/<date>-<slug><ext> and the page links to it relatively.
  Night reports print as the "From last night" cards; a local night-report
  file is copied as reports/<date>/<slug><ext> in the same publish run.

  Every report card's open link carries that report's last update in
  parentheses — "Open report (updated November 17, 5:12 AM)" — in
  Arizona time (Clay's ask, 2026-11-16). The time comes from that
  report's own freshest dated record: the night KPI record's finish
  entry for that piece when it stands there; otherwise the freshest
  dated build or publish record named for that report for that
  morning (the dated files in the item's own record line, the report
  file itself when it is a local file, or a standing report's known
  dated record). No dated record — no time is shown for that card;
  a time is never guessed. The run prints one "updated time:" line
  per card, naming any card left without a time.

  The RV report card is a standing card (Clay's order, 2026-11-16): the
  Class C motorhome search report, updated each night. Its address is
  RV_URL below — when the report's production home (a GitHub repository
  served by Cloudflare) stands, this one line changes to that address.

Output (one publish run of the GitHub key program, repository "menu"):
  morning.html            — the standing page, rebuilt every morning
  morning-<date>.html     — the dated archive copy (same bytes)
  morning-files/<date>-<slug><ext> — one per copied item report file
  reports/<date>/<slug><ext> — one per copied night-report file

Usage:
  build_morning_dashboard.py [--date YYYY-MM-DD] [--local-only]
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
FILAMENT_DIR = HOME / "workspace/goals/black-friday-list/hidden_files"

# The RV report — the Class C motorhome search (Clay's order, 2026-11-16:
# the card stands on the dashboard every morning). Production home since
# 2026-11-16: repository claypnw/class-c-motorhome-search, served by
# Cloudflare at the address below.
RV_URL = "https://class-c-motorhome-search.pages.dev/"

# The product search application (Clay's order, 2026-11-16): the
# standing card that opens the search page. It stands every morning,
# whether or not any search is scheduled; the scheduled-search cards
# below join it when a search has run.
SEARCH_URL = "https://product-search-9qc.pages.dev/product-search.html"

# The System Documentation repository (Clay's order, 2026-11-18): the
# documentation library's own repository — the standards, the systems,
# and who does what, everything a new AI reads to come in cold. The
# standing card stands every morning so the admin can open the library
# from the dashboard.
DOCS_URL = "https://github.com/claypnw/system-documentation"

# The follow lists page (Clay's order, 2026-11-22): the page where
# Clay himself keeps the two lists the nightly logging jobs follow —
# the YouTube channels for the transcription downloads and the X
# handles for the post log. It stands on this same site, beside the
# dashboard; its lists stand in the follow-lists store (a D1
# database), which the nightly jobs read at the start of each run.
FOLLOW_LISTS_URL = "add-channels-and-handles.html"

# The AI Transfer Drive tree (Clay's order, 2026-11-20): the dashboard
# reads the live tree each morning and shows its open hand-offs, with
# the dead or unsure ones flagged in their own lines. No tree yet, or a
# failed Drive read, is stated plainly on the card — never guessed.
DRIVE_CLI = Path("/opt/hatch/bin/hatch_gws_cli")
AI_TRANSFER_FOLDERS = ("For Gemini", "For Muggy", "For Maggie")
# The AI Transfer root folder's own address, as Drive itself returned
# it (files get, 2026-11-23): the card's title taps through to the
# tree (Clay's order, 2026-11-23 — the dashboard is the short summary
# and every box taps to its detail).
AI_TRANSFER_ROOT_URL = ("https://drive.google.com/drive/folders/"
                        "1o0eyduDI9XJ163jet7qDXqKZlaZm8FWM")

# The Maggie Apps Report (Clay's ask to Maggie, carried on Raven's
# Reach 2026-11-18): her counterpart to the Muse connectors report —
# the apps and connections on her side. She published it in the Health
# repository; the standing card stands beside the connectors report
# card every morning. The Health repository is private, so the report
# opens with the admin's GitHub sign-in.
MAGGIE_APPS_URL = ("https://github.com/claypnw/Health/blob/main/"
                   "standards/Maggie%20Apps%20Report.md")

# The report's own check date, read from the report itself (its date
# line and its dated checks): the card's summary line carries it, in
# the form Maggie suggested and Clay approved on 2026-11-23 (Raven's
# Reach THREAD-apps-expansion-20261123). Refresh this date when the
# report is refreshed.
MAGGIE_APPS_CHECKED = "November 23, 2026"

# The Black Friday sweep status record (Clay's order, 2026-11-18): the
# nightly sweep writes this small record each night it runs; the
# standing Black Friday card below reads it for its summary line and
# its update time. No record — the card still stands, with no time.
BF_STATUS = FILAMENT_DIR / "sweep-status.json"
BF_URL = "black-friday.html"

# The scheduled product searches (Clay's design, 2026-11-16): the
# standing record the search program's runner keeps. A search that has
# run stands here as a card with its last run time and a link to its
# newest results page. No record, or no run yet — no card.
SCHEDULED_SEARCHES = HOME / "workspace/search-program/scheduled-searches.json"

# The Raven's Reach nightly archive audit (Maggie's proposal on the
# board; Clay approved it 2026-11-20): the nightly job checks the
# board for talks finished in substance but still standing open and
# writes its result here. The standing card shows the count and the
# names, or a clean line when none stand. No result file — the card
# says the audit has not run yet, plainly.
RR_AUDIT_RESULT = (HOME / "workspace/goals/raven-s-reach-automated-"
                   "communication/hidden_files/nightly-audit/"
                   "audit-latest.json")

AZ = ZoneInfo("America/Phoenix")

# Which night-record run stands for which report (Clay's rule, 2026-11-16:
# the night record's finish entry first). Keys are report names in lower
# case; values are the night record's run keys for that report.
NIGHT_MATCH = {
    "the payson morning scroll": ["scroll", "briefing"],
    "github billing": ["billing"],
    "yard & estate sales": ["yard"],
    "the steward's ledger": ["ledger"],
    "the gilded pages": ["healthcare"],
}

# Standing night reports whose dated build record stands at a known
# place when the night record names no finish entry for them. The
# {day} in a path is filled with the dashboard's date.
NIGHT_REPORT_FILES = {
    "the effort log": [
        HOME / "workspace/effort-log/effort-log.html",
        HOME / "workspace/effort-log/effort-data.csv",
    ],
    "the steward's ledger": [
        HOME / "workspace/batch-logs/stewards-ledger-daily/{day}.log",
    ],
    "the gilded pages": [
        HOME / "workspace/batch-logs/gilded-pages-healthcare-rollout/{day}.log",
    ],
}

# The RV report's dated publish record (one per night).
RV_PUBLISH_RECORD = (HOME / "workspace/goals/class-c-motorhome-search-for-payson"
                     / "hidden_files" / "publish-record-{day}.md")
RV_PRODUCTION_PAGE = (HOME / "workspace/goals/class-c-motorhome-search-for-payson"
                      / "hidden_files" / "production" / "index.html")

CSS = """
:root{
  --ink:#2B1D10;
  --gold:#C9A227;
  --gold-bright:#E7C65A;
  --gold-deep:#8A6D1F;
  --iron:#3A3F44;
  --wood-dark:#2E1F14;
  --wood:#4A3220;
  --wood-light:#6B4A2C;
  --parchment:#F3E5C3;
  --parchment-light:#FBF3DC;
  --parchment-deep:#E4D0A2;
  --red:#7E2F22;
  --green:#47603C;
  --amber:#8A5A00;
}
*{ box-sizing:border-box; }
body{ margin:0; color:var(--ink);
  font-family: Georgia, 'Times New Roman', Times, serif;
  background:
    radial-gradient(1200px 500px at 50% -80px, rgba(231,198,90,.20), rgba(0,0,0,0) 60%),
    repeating-linear-gradient(90deg, rgba(0,0,0,.16) 0 2px, rgba(0,0,0,0) 2px 90px),
    repeating-linear-gradient(0deg, rgba(255,235,190,.05) 0 3px, rgba(0,0,0,0) 3px 7px),
    linear-gradient(180deg, #241708 0%, #3A2615 34%, #2E1F14 70%, #1D1208 100%);
  background-color:var(--wood-dark);
  min-height:100vh;
}
.wrap{ max-width:1460px; margin:14px auto 22px; padding:22px 26px 30px;
  background:
    radial-gradient(900px 380px at 50% 0, rgba(255,250,230,.55), rgba(0,0,0,0) 55%),
    repeating-linear-gradient(0deg, rgba(122,90,44,.045) 0 2px, rgba(0,0,0,0) 2px 5px),
    linear-gradient(168deg, #F6EAC9 0%, var(--parchment) 45%, var(--parchment-deep) 100%);
  border:3px solid var(--wood);
  outline:1px solid var(--gold-deep);
  outline-offset:-7px;
  border-radius:6px;
  box-shadow: 0 18px 50px rgba(0,0,0,.65), inset 0 0 60px rgba(122,90,44,.18);
}
.topbar{ display:flex; justify-content:space-between; align-items:center;
  background:linear-gradient(180deg, #4A4F55, var(--iron) 55%, #26292D);
  border:1px solid #17191C; border-bottom:3px solid var(--gold);
  border-radius:6px; padding:9px 14px;
  box-shadow: inset 0 1px 0 rgba(255,255,255,.25), 0 3px 8px rgba(0,0,0,.35);
}
.topbar .brand{ font-size:16.5px; font-weight:bold; letter-spacing:1.2px;
  color:var(--gold-bright); text-shadow:0 1px 2px rgba(0,0,0,.8); }
.headrow{ display:flex; justify-content:space-between; align-items:flex-end; gap:12px; margin-top:16px; }
h1{ margin:0; font-size:40px; font-weight:normal; letter-spacing:1.5px; color:#3A2410;
  text-shadow: 0 1px 0 #FFF6DC, 0 -1px 1px rgba(60,35,10,.55), 0 3px 6px rgba(90,60,20,.25); }
.date{ font-size:15.5px; margin-top:4px; color:#5A4020; font-style:italic; }
.refresh{ text-align:right; }
.refresh button{ font-family:inherit; font-size:14.5px; font-weight:bold; letter-spacing:.4px;
  background:linear-gradient(180deg, var(--wood-light), var(--wood) 60%, #3A2615);
  color:#F7E9C4; border:1.5px solid var(--gold-deep); border-radius:8px; padding:9px 16px; cursor:pointer;
  box-shadow: inset 0 1px 0 rgba(255,240,200,.35), 0 3px 7px rgba(40,25,8,.45);
  text-shadow:0 1px 2px rgba(0,0,0,.6); }
.refresh button:hover{ background:linear-gradient(180deg, #7D5836, #573D24 60%, #452D18); }
.refresh .note{ font-size:12.5px; margin-top:5px; color:#5A4020; }
.tiles{ display:grid; grid-template-columns: repeat(4, 1fr); gap:12px; margin:16px 0 4px; }
.tile{ position:relative; overflow:hidden;
  background:linear-gradient(165deg, #FFF9E8 0%, var(--parchment-light) 55%, #EFDFB4 100%);
  border:1.5px solid var(--wood); border-radius:10px; padding:14px 16px 13px;
  box-shadow: inset 0 0 0 1px rgba(201,162,39,.45), inset 0 1px 0 #FFFDF4, 0 4px 10px rgba(46,28,8,.35); }
.tile::before{ content:""; position:absolute; top:0; left:0; right:0; height:5px;
  background:linear-gradient(90deg, var(--gold-deep), var(--gold-bright), var(--gold-deep)); }
.tile .lab{ font-size:12px; letter-spacing:2px; text-transform:uppercase; color:var(--red); font-weight:bold; }
.tile .big{ font-size:26px; font-weight:bold; margin:6px 0 8px; color:#33200E;
  text-shadow:0 1px 0 #FFF6DC; }
.tile .small{ font-size:13px; margin-top:6px; color:#4A3520; }
.bar{ display:flex; height:10px; background:#D8C08C; border:1px solid #A5854C; border-radius:5px; overflow:hidden;
  box-shadow: inset 0 1px 3px rgba(70,45,10,.45); }
.bar .fill{ background:linear-gradient(180deg, #74905F, var(--green) 60%, #3A5230); }
.bar .rest{ background:linear-gradient(180deg, #D3B87F, #B99B5E); }
h2.group{ font-size:21px; font-weight:normal; letter-spacing:2.5px; text-transform:uppercase;
  color:#F3D98B; margin:26px 0 12px; padding:9px 14px 8px 42px; position:relative;
  background:linear-gradient(180deg, #5A3D22 0%, var(--wood) 45%, #33220F 100%);
  border:1.5px solid #241708; border-bottom:3px solid var(--gold);
  border-radius:6px;
  text-shadow:0 1px 3px rgba(0,0,0,.85);
  box-shadow: inset 0 1px 0 rgba(255,235,180,.30), 0 4px 10px rgba(46,28,8,.40); }
h2.group::before{ content:""; position:absolute; left:15px; top:50%; width:11px; height:11px;
  transform:translateY(-50%) rotate(45deg);
  background:linear-gradient(135deg, var(--gold-bright), var(--gold-deep));
  border:1px solid #5E4A12; box-shadow:0 0 6px rgba(231,198,90,.65); }
.cards{ display:grid; grid-template-columns: repeat(4, 1fr); gap:12px; }
.cards4{ display:grid; grid-template-columns: repeat(4, 1fr); gap:12px; }
.card{ position:relative;
  background:linear-gradient(168deg, #FFFBEF 0%, var(--parchment-light) 58%, #F0DFAF 100%);
  border:1.5px solid var(--wood); border-radius:10px; padding:13px 15px 14px;
  box-shadow: inset 0 0 0 1px rgba(201,162,39,.40), inset 0 1px 0 #FFFDF4, 0 4px 10px rgba(46,28,8,.32); }
.card .row{ display:flex; justify-content:space-between; align-items:flex-start; gap:8px;
  border-bottom:1px solid rgba(138,109,31,.45); padding-bottom:6px; }
.card h3{ margin:0; font-size:17.5px; color:var(--red); letter-spacing:.3px;
  text-shadow:0 1px 0 #FFF6DC; }
.card .st{ font-size:11.5px; white-space:nowrap; color:#2F4423; font-weight:bold;
  letter-spacing:.6px; text-transform:uppercase;
  background:linear-gradient(180deg, #DCE8C8, #B9CCA0);
  border:1px solid #6E8452; border-radius:20px; padding:2px 9px;
  box-shadow: inset 0 1px 0 rgba(255,255,255,.7); }
.card .st.warn{ color:#6E4200;
  background:linear-gradient(180deg, #F7E3AE, #EBCB7E);
  border-color:#A5854C; }
.card .det{ font-size:14px; margin-top:7px; line-height:1.45; color:#332412; }
.card .links{ margin-top:9px; font-size:14.5px; }
.card .links a{ color:#7E2F22; font-weight:bold; margin-right:14px;
  text-decoration:none; border-bottom:1.5px solid var(--gold); }
.card .links a:hover{ color:#A03A28; border-bottom-color:var(--red); }
.cards4 .card h3{ font-size:16.5px; border-bottom:1px solid rgba(138,109,31,.45); padding-bottom:6px; }
.cards4 .card h3 a{ text-decoration:none; border-bottom:1.5px solid var(--gold); }
.decisions{ background:linear-gradient(168deg, #FFFBEF, var(--parchment-light) 60%, #F0DFAF);
  border:1.5px solid var(--wood); border-radius:10px; padding:12px 16px;
  box-shadow: inset 0 0 0 1px rgba(201,162,39,.40), 0 4px 10px rgba(46,28,8,.32); }
.decisions ul{ margin:6px 0; padding-left:20px; font-size:14.5px; line-height:1.5; }
.filament{ background:linear-gradient(168deg, #FFF6DC 0%, #F7EAC4 55%, #EDD9A4 100%);
  border:1.5px solid var(--wood); border-radius:10px; padding:12px 18px;
  box-shadow: inset 0 0 0 1px rgba(201,162,39,.45), inset 0 1px 0 #FFFDF4, 0 4px 10px rgba(46,28,8,.32); }
.filament ul{ margin:4px 0; padding-left:18px; font-size:14px; line-height:1.55; column-count:3; column-gap:30px; }
.filament li{ break-inside: avoid; margin-bottom:4px; }
.filament a{ color:#7E2F22; }
.note-line{ font-size:14px; font-style:italic; margin-top:12px; }
footer{ margin-top:34px; border-top:3px double var(--gold-deep); padding-top:12px;
  font-size:13.5px; text-align:center; line-height:1.55; color:#5A4020; }
@media (max-width: 1100px) { .cards { grid-template-columns: repeat(3, 1fr); } .filament ul { column-count:2; } }
@media (max-width: 900px) { .tiles, .cards4 { grid-template-columns: repeat(2, 1fr); } .cards { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 560px) { .tiles, .cards, .cards4 { grid-template-columns: 1fr; } .filament ul { column-count:1; } h1 { font-size:31px; } .headrow { flex-direction:column; align-items:flex-start; } .refresh { text-align:left; } .wrap { margin:0; padding:16px 14px 24px; border-radius:0; } h2.group { font-size:18px; letter-spacing:1.6px; } }
"""


def fail(reason):
    print(f"VERDICT: FAIL — {reason}")
    sys.exit(1)


def split_status(page_status):
    """Split a page_status line into (state word, detail). The state word
    is the part before the first ' — ' when it names a state; the detail
    is what follows. Without the split, the whole line is the detail."""
    text = (page_status or "").strip()
    if " — " in text:
        head, tail = text.split(" — ", 1)
        if head.lower().startswith(("finished", "had an error", "no record")):
            return head, tail
    return "", text


def format_updated(when):
    """The parenthetical update words for a link, in Arizona time —
    the form: (updated November 17, 5:12 AM)."""
    if when is None:
        return ""
    return f" (updated {when.strftime('%B %-d, %-I:%M %p')})"


def freshest_mtime(paths, day):
    """The freshest file time among the dated records in paths: first
    only the files whose name carries the day's date; if none of those
    stand, the files whose own time falls on the day. None if no such
    dated record stands."""
    existing = [p for p in paths if p and Path(p).exists()]
    dated = [p for p in existing if day in Path(p).name]
    pool = dated
    if not pool:
        pool = [p for p in existing
                if datetime.fromtimestamp(Path(p).stat().st_mtime, AZ)
                .strftime("%Y-%m-%d") == day]
    if not pool:
        return None
    freshest = max(pool, key=lambda p: Path(p).stat().st_mtime)
    return datetime.fromtimestamp(Path(freshest).stat().st_mtime, AZ)


def record_paths(item):
    """The file paths named in an item's own record line, in order."""
    text = item.get("record") or ""
    found = re.findall(r"(?:~/|/home/hatch/)[^\s,;()]+", text)
    paths = []
    for raw in found:
        raw = raw.rstrip(".")
        p = Path(raw).expanduser() if raw.startswith("~/") else Path(raw)
        if p not in paths:
            paths.append(p)
    return paths


def drive_list_files(query):
    """List Drive files for one query through the standing Drive road."""
    params = {
        "q": query,
        "fields": "files(id,name,mimeType,parents,trashed,webViewLink)",
        "pageSize": 1000,
        "orderBy": "name",
    }
    result = subprocess.run(
        [str(DRIVE_CLI), "drive", "files", "list", "--params",
         json.dumps(params), "--page-all", "--page-limit", "10"],
        capture_output=True, text=True, timeout=60,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())
    text = result.stdout.strip()
    payloads = []
    try:
        payloads = [json.loads(text)]
    except Exception:
        for line in text.splitlines():
            if line.strip():
                payloads.append(json.loads(line))
    files = []
    for payload in payloads:
        if isinstance(payload, dict):
            files.extend(payload.get("files") or [])
    return files


def ai_transfer_lines(day):
    """The AI Transfer card's lines, read from the live Drive tree.

    A hand-off folder is open while it stands in one of the three
    receiver folders. Its age comes from the date in its name, never
    from a Drive timestamp. A failed read is named as not checked.
    Each line comes back as (text, address): a hand-off line carries
    its own folder's Drive address, so the card can make the line a
    tap through to that folder (Clay's order, 2026-11-23); a line
    naming no standing folder carries None, or the tree's root
    address for a missing-folder line.
    """
    try:
        dashboard_date = datetime.strptime(day, "%Y-%m-%d").date()
        roots = drive_list_files(
            "name = 'AI Transfer' and "
            "mimeType = 'application/vnd.google-apps.folder' and trashed = false"
        )
        if not roots:
            return [("AI Transfer — not built yet.", None)]
        if len(roots) != 1:
            return [("AI Transfer — not checked this morning.", None)]
        root_url = roots[0].get("webViewLink") or AI_TRANSFER_ROOT_URL
        root_children = drive_list_files(
            f"'{roots[0]['id']}' in parents and trashed = false"
        )
        receiver_folders = {
            child.get("name"): child for child in root_children
            if child.get("mimeType") == "application/vnd.google-apps.folder"
        }
        hand_offs = []
        missing = []
        for folder_name in AI_TRANSFER_FOLDERS:
            folder = receiver_folders.get(folder_name)
            if folder is None:
                missing.append(folder_name)
                continue
            children = drive_list_files(
                f"'{folder['id']}' in parents and "
                "mimeType = 'application/vnd.google-apps.folder' and trashed = false"
            )
            for child in children:
                contents = drive_list_files(
                    f"'{child['id']}' in parents and trashed = false"
                )
                child_url = (child.get("webViewLink")
                             or "https://drive.google.com/drive/folders/"
                             + child["id"])
                hand_offs.append((child.get("name", ""), contents,
                                  child_url))
        lines = [
            (f"{len(hand_offs)} open hand-off"
             + ("" if len(hand_offs) == 1 else "s"), None)
        ]
        for name, contents, handoff_url in hand_offs:
            is_wip = name.startswith("WIP ")
            match = re.match(r"^(?:WIP\s+)?(\d{4}-\d{2}-\d{2})\b", name)
            flags = []
            if not contents:
                flags.append("empty — the daily prune takes it")
            if match:
                try:
                    age = (dashboard_date - datetime.strptime(
                        match.group(1), "%Y-%m-%d").date()).days
                except Exception:
                    age = None
            else:
                age = None
            if age is None:
                line = f"{name} — date not readable"
            else:
                line = f"{name} — {age} day" + ("" if age == 1 else "s") + " old"
                if is_wip and age > 1:
                    flags.append("still marked WIP")
                if age >= 7:
                    flags.append("seven days old — the daily prune takes it")
            if flags:
                line += " — " + "; ".join(flags)
            lines.append((line, handoff_url))
        for folder_name in missing:
            lines.append((f"Missing folder: {folder_name}", root_url))
        return lines
    except Exception:
        return [("AI Transfer — not checked this morning.", None)]


RR_HOME_URL = ("https://github.com/claypnw/Health/tree/main/"
               "standards/Raven's%20Reach")

# The archive process page (Clay's ask, 2026-11-19; placed
# 2026-11-23): the short plain-words page that says how a talk
# closes and moves to the Archive. It stands on this same site,
# beside the dashboard; the Raven's Reach card below links to it.
ARCHIVE_PROCESS_URL = "archive-process.html"

# The Daily Security & Outage Brief (Clay approved the brief
# 2026-11-24): the morning-security-brief-daily job writes each
# morning's brief as a PDF at this one fixed address on this same
# site, overwritten every day; the standing card below links to it.
SECURITY_BRIEF_URL = ("https://menu-c8u.pages.dev/reports/"
                      "daily-security-brief.pdf")


def rr_audit_card():
    """The Raven's Reach nightly archive audit card's body, read from
    the audit's latest result file: a count line, then one bullet per
    finished talk still standing open — one line each, the talk's name
    and its state in a few plain words, and every bullet a link to that
    talk's folder in the repository (the dashboard is the short
    summary; the tap carries him to the full detail — Clay's order,
    2026-11-23). The audit record names each talk's folder but carries
    no path of its own; its dated text states these talks stand in
    Active, so the bullets link there, and an item with no folder name
    links to the Raven's Reach home folder. The audit reports only —
    it closes and archives nothing. No file: the audit has not run
    yet. Returns (state word, card body HTML)."""
    try:
        if not RR_AUDIT_RESULT.exists():
            return ("Not run yet",
                    "The nightly archive audit has not run yet.")
        result = json.loads(RR_AUDIT_RESULT.read_text())
    except Exception:
        return ("Updated each night",
                "The nightly archive audit result could not be read "
                "this morning.")
    items = result.get("concluded_but_open") or []
    count = result.get("concluded_but_open_count", len(items))
    # Four-class correction (2026-11-23, Archive-Reading work0):
    # concluded_but_open now holds ONLY talks whose conclusion stands
    # verified on completion evidence — a receipt test alone never
    # labels a talk finished here. The other classes are named in a
    # plain counts line under the list, never dressed as done.
    counts = result.get("class_counts") or {}
    extra = ""
    if counts:
        bits = []
        if counts.get("answered-but-work-pending"):
            bits.append(f"{counts['answered-but-work-pending']} with "
                        f"work still being done")
        if counts.get("unanswered"):
            bits.append(f"{counts['unanswered']} waiting on an answer")
        if counts.get("uncertain-unreviewed"):
            bits.append(f"{counts['uncertain-unreviewed']} not yet "
                        f"reviewed")
        if bits:
            extra = ("<p>Also standing on Raven's Reach: "
                     + ", ".join(bits) + ".</p>")
    if count == 0 or not items:
        return ("Updated each night",
                "Clean — no finished talk stands open on "
                "Raven's Reach." + extra)
    lead = (f"{count} finished talk" + ("" if count == 1 else "s")
            + " still standing open on Raven's Reach:")
    lis = []
    for item in items:
        kind = item.get("kind", "")
        if kind in ("verified-concluded-awaiting-archive",
                    "nothing-waiting"):
            state = "finished — only the closing step left"
        elif kind == "receipt-only":
            state = "finished — only a receipt left"
        else:
            state = item.get("missing", "").split(" (notes:")[0].strip()
        folder = item.get("folder", "")
        if folder and re.fullmatch(r"[A-Za-z0-9_.\-]+", folder):
            url = f"{RR_HOME_URL}/Active/{folder}"
        else:
            url = RR_HOME_URL
        # The address is built here from the constant above and a
        # folder name held to plain letters, digits, "_", "." and "-",
        # so it goes in unescaped — escaping it would print the
        # apostrophe in "Raven's" as a code in the address.
        lis.append(f'<li><a href="{url}">'
                   f"{html.escape(item.get('name', ''))} — "
                   f"{html.escape(state)}</a></li>")
    return ("Updated each night",
            f"{html.escape(lead)}"
            f'<ul style="margin:4px 0; padding-left:18px;">'
            f"{''.join(lis)}</ul>" + extra)


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

    # The header line carries the time this page was built beside the
    # date (Clay's order, 2026-11-19): date and time together are the
    # dashboard's last update, in Arizona time.
    built_time = datetime.now(AZ).strftime("%-I:%M %p")

    # The night record for this morning — the first road for a report's
    # update time (its finish entry for that piece).
    night_runs = {}
    night_path_early = RECORD_DIR / "morning-kpi-records" / f"night-{day}.json"
    if night_path_early.exists():
        try:
            for run in json.loads(night_path_early.read_text()).get("runs") or []:
                if run.get("key"):
                    night_runs[run["key"]] = run
        except Exception:
            night_runs = {}

    def night_finish_for(name, slug=None):
        keys = list(NIGHT_MATCH.get((name or "").strip().lower()) or [])
        if slug and slug not in keys:
            keys.append(slug)
        for key in keys:
            run = night_runs.get(key)
            finish = (run or {}).get("finish_time")
            if finish:
                try:
                    return datetime.strptime(f"{day} {finish}", "%Y-%m-%d %H:%M").replace(tzinfo=AZ)
                except Exception:
                    return None
        # No named match: a run whose own name stands inside the
        # report's name, or the other way round.
        low = (name or "").strip().lower()
        for run in night_runs.values():
            run_name = (run.get("name") or "").strip().lower()
            finish = run.get("finish_time")
            if finish and run_name and (run_name in low or low in run_name):
                try:
                    return datetime.strptime(f"{day} {finish}", "%Y-%m-%d %H:%M").replace(tzinfo=AZ)
                except Exception:
                    return None
        return None

    def update_time_for(item):
        """A morning report's last update: the night record's finish
        entry first; otherwise the freshest dated record named in the
        item's own record line, or the report file itself when local."""
        when = night_finish_for(item.get("name", ""), item.get("slug"))
        if when is not None:
            return when
        paths = record_paths(item)
        for link in item.get("links") or []:
            href = link.get("href", "")
            if href and not href.startswith(("http://", "https://")):
                paths.append(Path(href))
        return freshest_mtime(paths, day)

    def rv_update_time():
        """The RV report's last update, from its dated publish record:
        the sent time written in that record; otherwise that record's
        own time; otherwise the production page's time for the day."""
        rec = Path(str(RV_PUBLISH_RECORD).format(day=day))
        if rec.exists():
            m = re.search(r"sent\s+(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2})(?::\d{2})?",
                          rec.read_text(errors="ignore"))
            if m:
                try:
                    return datetime.strptime(f"{m.group(1)} {m.group(2)}",
                                             "%Y-%m-%d %H:%M").replace(tzinfo=AZ)
                except Exception:
                    pass
            return freshest_mtime([rec], day)
        return freshest_mtime([RV_PRODUCTION_PAGE], day)

    # One line per report card, for the run record: the time shown, or
    # the gap named when no dated record stands for that card.
    time_report = []

    # Resolve links: copy local files to their repository names.
    copies = []  # (source Path, repo-relative target)

    def resolve(item, href, kind, idx):
        if href.startswith("http://") or href.startswith("https://"):
            return href
        src = Path(href)
        if not src.exists():
            fail(f"report file for {kind} {idx} not found: {href}")
        slug = item.get("slug")
        if not slug:
            fail(f"{kind} {idx} links a local file but names no slug")
        if kind == "item":
            target = f"morning-files/{day}-{slug}{src.suffix}"
        else:
            target = f"reports/{day}/{slug}{src.suffix}"
        copies.append((src, target))
        return target

    # Morning report cards.
    cards = []
    item_first_link = {}
    for i, item in enumerate(items, start=1):
        item_when = update_time_for(item)
        time_report.append((item.get("name", ""), item_when))
        suffix = format_updated(item_when)
        links_html = []
        for link_i, link in enumerate(item.get("links") or []):
            href = link.get("href", "")
            final = resolve(item, href, "item", i)
            if link_i == 0:
                label = "Open PDF" if final.lower().endswith(".pdf") else "Open report"
            else:
                label = re.sub(r"^\s*\d+\s*·\s*", "", link.get("text", "")).strip()
                label = label[:1].upper() + label[1:] if label else "Open"
            links_html.append(f'<a href="{html.escape(final)}">{html.escape(label + suffix)}</a>')
        if not links_html:
            fail(f"item {i} carries no links")
        # The item's first link, in its attribute-ready form, kept by
        # name so the summary tiles above the cards can tap through to
        # the same detail (Clay's order, 2026-11-23).
        item_first_link[item.get("name", "")] = re.search(
            r'href="([^"]+)"', links_html[0]).group(1)
        state, detail = split_status(item.get("page_status") or item.get("status") or "")
        warn = "" if state.lower() == "finished" or not state else " warn"
        st_html = f'<span class="st{warn}">{html.escape(state)}</span>' if state else ""
        cards.append(
            f'<div class="card"><div class="row"><h3>{html.escape(item.get("name", ""))}</h3>'
            f"{st_html}</div>"
            f'<div class="det">{html.escape(detail)}</div>'
            f'<div class="links">{"".join(links_html)}</div></div>'
        )
        # The standing Maggie Apps Report card stands beside the Muse
        # connectors report card (Clay's ask, 2026-11-18): her
        # counterpart report, in the Health repository. It is a standing
        # report, not a morning report — its link carries no update time.
        if item.get("name", "") == "Muse connectors report":
            time_report.append(("Aela Apps Report (standing report — not a morning report)", None))
            cards.append(
                '<div class="card"><div class="row">'
                "<h3>Aela Apps Report</h3>"
                '<span class="st">Standing</span></div>'
                '<div class="det">Apps in use and available to add — '
                f"checked {MAGGIE_APPS_CHECKED}. Aela's counterpart "
                "to the Muse connectors report — the apps and "
                "connections on her side. It stands in the Health "
                "repository and opens with your GitHub sign-in.</div>"
                f'<div class="links"><a href="{MAGGIE_APPS_URL}">Open report</a></div></div>'
            )

    # The standing RV report card (Clay's order, 2026-11-16).
    rv_when = rv_update_time()
    time_report.append(("Class C motorhome search — the RV report", rv_when))
    cards.append(
        '<div class="card"><div class="row">'
        "<h3>Class C motorhome search — the RV report</h3>"
        '<span class="st">Updated each night</span></div>'
        '<div class="det">Class C, under 30 feet, under $25,000 — Payson first. '
        "Each listing stands with the seller's full write-up.</div>"
        f'<div class="links"><a href="{RV_URL}">Open report{format_updated(rv_when)}</a></div></div>'
    )

    # The standing product search card (Clay's order, 2026-11-16): the
    # door to the search page, on the dashboard every morning. It is a
    # standing page, not a morning report, and no dated record for it
    # stands for this morning — its link carries no update time.
    time_report.append(("Product search (standing search page — not a morning report)", None))
    cards.append(
        '<div class="card"><div class="row">'
        "<h3>Product search</h3>"
        '<span class="st">Standing</span></div>'
        '<div class="det">The search page — set the words, the place, and '
        "the stores, then search now or set a search to run on a schedule.</div>"
        f'<div class="links"><a href="{SEARCH_URL}">Open the search page</a></div></div>'
    )

    # The standing System Documentation card (Clay's order, 2026-11-18):
    # the door to the documentation library's own repository. It is a
    # standing library, not a morning report, and no dated record for it
    # stands for this morning — its link carries no update time.
    time_report.append(("System Documentation (standing library — not a morning report)", None))
    cards.append(
        '<div class="card"><div class="row">'
        "<h3>System Documentation</h3>"
        '<span class="st">Standing</span></div>'
        '<div class="det">The documentation library — the standards, the '
        "systems, and who does what. Everything a new AI reads to come "
        "in cold.</div>"
        f'<div class="links"><a href="{DOCS_URL}">Open the documentation</a></div></div>'
    )

    # The standing follow lists card (Clay's order, 2026-11-22): the
    # door to the page where Clay keeps the two lists the nightly
    # logging jobs follow. It is a standing page, not a morning
    # report, and no dated record for it stands for this morning —
    # its link carries no update time.
    time_report.append(("Add YouTube channels and X handles (standing page — not a morning report)", None))
    cards.append(
        '<div class="card"><div class="row">'
        "<h3>Add YouTube channels and X handles</h3>"
        '<span class="st">Standing</span></div>'
        '<div class="det">The YouTube channels and X handles the '
        "nightly jobs follow. Add or remove a name here and the "
        "next run picks it up.</div>"
        f'<div class="links"><a href="{FOLLOW_LISTS_URL}">Open the page</a></div></div>'
    )

    # The standing AI Transfer card (Clay's order, 2026-11-20): a live
    # count and one line for each open hand-off in the Drive tree.
    ai_lines = ai_transfer_lines(day)
    ai_first = ai_lines[0][0] if ai_lines else ""
    if ai_first == "AI Transfer — not built yet.":
        ai_state, ai_warn = "Not built", " warn"
    elif ai_first == "AI Transfer — not checked this morning.":
        ai_state, ai_warn = "Not checked", " warn"
    else:
        ai_state, ai_warn = "Standing", ""
    time_report.append(("AI Transfer (standing Drive status — not a morning report)", None))
    ai_det = "<br>".join(
        f'<a href="{html.escape(url)}">{html.escape(text)}</a>'
        if url else html.escape(text)
        for text, url in ai_lines)
    cards.append(
        '<div class="card"><div class="row">'
        f'<h3><a href="{AI_TRANSFER_ROOT_URL}" style="color:#2B2118;">AI Transfer</a></h3>'
        f'<span class="st{ai_warn}">{ai_state}</span></div>'
        f'<div class="det">{ai_det}</div></div>'
    )

    # The standing Raven's Reach nightly archive audit card (Clay
    # approved Maggie's proposal 2026-11-20): the count of talks
    # finished in substance but still standing open, with their names,
    # or a clean line when none stand.
    rr_state, rr_body = rr_audit_card()
    rr_warn = " warn" if rr_state == "Not run yet" else ""
    time_report.append(("Raven's Reach nightly archive audit (standing audit result — not a morning report)", None))
    cards.append(
        '<div class="card"><div class="row">'
        "<h3>Raven's Reach — nightly archive audit</h3>"
        f'<span class="st{rr_warn}">{rr_state}</span></div>'
        f'<div class="det">{rr_body}</div>'
        f'<div class="links"><a href="{ARCHIVE_PROCESS_URL}">'
        "How talks close and move to the Archive</a></div></div>"
    )

    # The standing Daily Security & Outage Brief card (Clay approved
    # the brief 2026-11-24): the morning-security-brief-daily job
    # publishes each morning's brief — the past day's job log, the
    # cyber and outage news, and the preparedness reminder — as a PDF
    # at the one fixed address above, overwritten every day.
    time_report.append(("Daily Security & Outage Brief (standing daily PDF — not a morning report)", None))
    cards.append(
        '<div class="card"><div class="row">'
        "<h3>Daily Security &amp; Outage Brief</h3>"
        '<span class="st">Updated each morning</span></div>'
        '<div class="det">The morning security, outage and job-log '
        "brief — last night's jobs, the day's cyber and outage news, "
        "and the preparedness reminder, in one short PDF.</div>"
        f'<div class="links"><a href="{SECURITY_BRIEF_URL}">'
        "Daily Security &amp; Outage Brief (PDF)</a></div></div>"
    )

    # The standing Black Friday card (Clay's order, 2026-11-18): the
    # nightly sweep's report, one card every morning while the sweep
    # runs. Its summary line and update time come from the sweep's
    # status record when one stands.
    bf_when = None
    bf_summary = ("The nightly sweep of the Black Friday list — the "
                  "coffee maker, the filament, the swatters, and the "
                  "solar generator package, each judged by its own "
                  "good-deal line.")
    try:
        if BF_STATUS.exists():
            bf = json.loads(BF_STATUS.read_text())
            if bf.get("summary"):
                bf_summary = str(bf["summary"])
            try:
                bf_when = datetime.fromisoformat(
                    str(bf.get("date", "")) + "T21:30:00").replace(tzinfo=AZ)
            except Exception:
                bf_when = None
    except Exception:
        pass
    time_report.append(("Black Friday list — nightly sweep", bf_when))
    cards.append(
        '<div class="card"><div class="row">'
        "<h3>Black Friday list — nightly sweep</h3>"
        '<span class="st">Updated each night</span></div>'
        f'<div class="det">{html.escape(bf_summary)}</div>'
        f'<div class="links"><a href="{BF_URL}">Open the Black Friday report'
        f"{format_updated(bf_when)}</a></div></div>"
    )

    # Scheduled product search cards — one per search that has run.
    try:
        if SCHEDULED_SEARCHES.exists():
            sched = json.loads(SCHEDULED_SEARCHES.read_text())
            for s in sched.get("searches") or []:
                last = s.get("last_run") or {}
                url = last.get("results_url")
                if not url:
                    continue
                sched_when = None
                try:
                    at = datetime.fromisoformat(last.get("at", ""))
                    if at.tzinfo is not None:
                        at = at.astimezone(AZ)
                    sched_when = at
                    when = at.strftime("%A, %B %-d, %I:%M %p")
                except Exception:
                    when = str(last.get("at", ""))
                time_report.append((f"Scheduled search — {s.get('name', '')}", sched_when))
                sch = s.get("schedule") or {}
                kind = sch.get("kind", "")
                if kind == "single":
                    runs_words = f"One single search, ran {when}"
                elif kind:
                    runs_words = (f"Runs {kind} at {sch.get('time', '')} · "
                                  f"last run {when}")
                else:
                    runs_words = f"Last run {when}"
                cards.append(
                    '<div class="card"><div class="row">'
                    f"<h3>Scheduled search — {html.escape(s.get('name', ''))}</h3>"
                    '<span class="st">Finished</span></div>'
                    f'<div class="det">{html.escape(runs_words)}.</div>'
                    f'<div class="links"><a href="{html.escape(url)}">'
                    f"Open newest results{format_updated(sched_when)}</a></div></div>"
                )
    except Exception:
        pass

    # Maker finds note, when the record's excluded list names it.
    maker_note = ""
    for ex in record.get("excluded") or []:
        if str(ex.get("item", "")).startswith("Maker finds"):
            maker_note = ('<p class="note-line">Maker finds — the nightly hunt for pieces '
                          "to make into the Hearth found no true fit last night, so no new "
                          "pick stands here today.</p>")
            break

    # Tiles.
    tiles = []
    night_path = RECORD_DIR / "morning-kpi-records" / f"night-{day}.json"
    if night_path.exists():
        try:
            night = json.loads(night_path.read_text())
            total = int(night.get("set_total") or 0)
            runs = night.get("runs") or []
            finished = sum(1 for r in runs if r.get("final_state") == "finished")
            failed = sum(1 for r in runs if r.get("final_state") in ("failed", "error"))
            no_record = max(total - finished - failed, 0)
            pct = (finished / total * 100) if total else 0
            tile_inner = (
                '<div class="lab">Overnight run</div>'
                f'<div class="big">{finished} / {total} finished</div>'
                f'<div class="bar"><div class="fill" style="width:{pct:.1f}%"></div>'
                f'<div class="rest" style="width:{100 - pct:.1f}%"></div></div>'
                f'<div class="small">{finished} finished · {failed} failed · '
                f"{no_record} no record</div>"
            )
            kpi_href = item_first_link.get("Last night's KPIs", "")
            if kpi_href:
                tile_inner = (
                    f'<a href="{kpi_href}" style="color:inherit; '
                    f'text-decoration:none; display:block;">{tile_inner}</a>'
                )
            tiles.append(f'<div class="tile">{tile_inner}</div>')
        except Exception:
            pass
    by_name = {it.get("name", ""): (it.get("page_status") or "") for it in items}
    billing = by_name.get("GitHub billing", "")
    m = re.search(r"([\d,]+) minutes.*?([\d.]+)%", billing)
    if m:
        tile_inner = (
            '<div class="lab">GitHub billing</div>'
            f'<div class="big">{m.group(2)}% of cycle</div>'
            f'<div class="bar"><div class="fill" style="width:{m.group(2)}%"></div></div>'
            f'<div class="small">{m.group(1)} minutes used</div>'
        )
        billing_href = item_first_link.get("GitHub billing", "")
        if billing_href:
            tile_inner = (
                f'<a href="{billing_href}" style="color:inherit; '
                f'text-decoration:none; display:block;">{tile_inner}</a>'
            )
        tiles.append(f'<div class="tile">{tile_inner}</div>')
    conn = by_name.get("Muse connectors report", "")
    m = re.search(r"(\d+) connectors, (\d+) connected", conn)
    if m:
        total_c, conn_c = int(m.group(1)), int(m.group(2))
        pct = (conn_c / total_c * 100) if total_c else 0
        tile_inner = (
            '<div class="lab">Connectors</div>'
            f'<div class="big">{conn_c} / {total_c} connected</div>'
            f'<div class="bar"><div class="fill" style="width:{pct:.0f}%"></div></div>'
            f'<div class="small">{conn_c} working for you</div>'
        )
        conn_href = item_first_link.get("Muse connectors report", "")
        if conn_href:
            tile_inner = (
                f'<a href="{conn_href}" style="color:inherit; '
                f'text-decoration:none; display:block;">{tile_inner}</a>'
            )
        tiles.append(f'<div class="tile">{tile_inner}</div>')
    if decisions:
        tiles.append(
            '<div class="tile"><div class="lab">Decisions waiting</div>'
            f'<div class="big">{len(decisions)} waiting</div>'
            '<div class="small">Named in full below.</div></div>'
        )
    else:
        tiles.append(
            '<div class="tile"><div class="lab">Decisions waiting</div>'
            '<div class="big" style="font-size:19px; padding-top:5px;">None this morning.</div>'
            '<div class="small">No choice or approval is waiting on you.</div></div>'
        )

    # Decisions section — stands only when a decision waits (the tile
    # carries the count either way, as on Maggie's dashboard).
    if decisions:
        dec_lis = []
        for d in decisions:
            q = html.escape(d.get("question", ""))
            ch = " / ".join(html.escape(c) for c in d.get("choices") or [])
            dec_lis.append(f"<li>{q}" + (f" — choices: {ch}" if ch else "") + "</li>")
        decisions_html = (
            '<h2 class="group">Waiting on your word</h2><div class="decisions"><ul>'
            + "".join(dec_lis) + "</ul></div>"
        )
    else:
        decisions_html = ""

    # The filament ad: headline, pick lines, and a closing not-checked line.
    ad_lines = []
    if AD_FILE.exists():
        ad_lines = [ln.strip() for ln in AD_FILE.read_text().splitlines() if ln.strip()]
    filament_html = ""
    filament_tile = ""
    if ad_lines:
        picks = ad_lines[1:]
        tail_note = ""
        if picks and picks[-1].lower().startswith("not checked"):
            tail_note = picks[-1]
            picks = picks[:-1]
        # Each pick is a link to its own product page (Clay's order,
        # 2026-11-16; standing form settled 2026-11-23). The link rides
        # at the end of the ad line itself, after " | " — the line text,
        # then " | ", then the bare link. A line with a link renders as
        # one link, the whole line the tap target. A line with no link
        # renders as plain text.
        def pick_li(ln):
            text, sep, url = ln.rpartition(" | ")
            if sep and url.startswith("http") and " " not in url:
                return (f'<li><a href="{html.escape(url)}">'
                        f'{html.escape(text)}</a></li>')
            return f"<li>{html.escape(ln)}</li>"
        ad_lis = "".join(pick_li(ln) for ln in picks)
        filament_html = (
            f'<h2 class="group" id="filament">{html.escape(ad_lines[0])}</h2>'
            f'<div class="filament"><ul>{ad_lis}</ul>'
            + (f'<p style="margin:4px 0 0; font-size:14px;">{html.escape(tail_note)}</p>'
               if tail_note else "")
            + "</div>"
        )
        filament_tile = (
            '<div class="card"><h3><a href="#filament" style="color:#2B2118;">Filament sales</a></h3>'
            f'<div class="det">{len(picks)} listings — the full list stands below</div></div>'
        )

    # From last night cards.
    night_reports = record.get("night_reports") or []
    nr_cards = []
    for nr_i, nr in enumerate(night_reports, start=1):
        name = nr.get("name", "")
        href = nr.get("href", "")
        if not name or not href:
            fail(f"night report {nr_i} lacks a name or an href")
        final = resolve(nr, href, "night", nr_i)
        if " — " in name:
            title, detail = name.split(" — ", 1)
        else:
            title, detail = name, ""
        nr_when = night_finish_for(title, nr.get("slug"))
        if nr_when is None:
            known = NIGHT_REPORT_FILES.get(title.strip().lower()) or []
            known_paths = [Path(str(p).format(day=day)) if "{day}" in str(p) else Path(p)
                           for p in known]
            nr_when = freshest_mtime(known_paths, day)
        time_report.append((f"From last night — {title}", nr_when))
        nr_cards.append(
            f'<div class="card"><h3><a href="{html.escape(final)}" '
            f'style="color:#2B2118;">{html.escape(title)}</a>{html.escape(format_updated(nr_when))}</h3>'
            + (f'<div class="det">{html.escape(detail)}</div>' if detail else "")
            + "</div>"
        )
    if filament_tile:
        nr_cards.append(filament_tile)
    if nr_cards:
        night_html = ('<h2 class="group">From last night</h2><div class="cards4">'
                      + "".join(nr_cards) + "</div>")
    else:
        night_html = ('<h2 class="group">From last night</h2>'
                      '<p class="note-line">None — no reports were created last night.</p>')

    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Morning Dashboard — {nice_day}</title>
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
<div class="topbar"><div class="brand">✦ Mogollon's Hearth</div></div>
<div class="headrow">
  <div><h1>Morning Dashboard</h1><div class="date">{nice_day} — last update {built_time}</div></div>
  <div class="refresh"><button onclick="location.reload()">↻ Refresh reports</button>
  <div class="note">Latest reports · checked this morning</div></div>
</div>
<div class="tiles">
{chr(10).join(tiles)}
</div>
<h2 class="group">Morning reports</h2>
<div class="cards">
{chr(10).join(cards)}
</div>
{maker_note}
{night_html}
{decisions_html}
{filament_html}
<footer>This page is rebuilt every morning. Anyone holding this page's address can open it and the reports behind it.</footer>
</div>
</body>
</html>
"""

    print(f"header date line: {nice_day} — last update {built_time}")
    print(f"dashboard: {len(cards)} morning report cards (including the standing Maggie Apps Report card, the standing RV report card, the standing product search card, the standing System Documentation card, the standing follow lists card, and the standing AI Transfer card), "
          f"{len(tiles)} tiles, {len(nr_cards)} from-last-night cards")
    for card_name, card_when in time_report:
        if card_when is not None:
            print(f"updated time: {card_name} — shown{format_updated(card_when)}")
        else:
            print(f"updated time: {card_name} — none shown, no dated record stands for this card for {day}")
    print("filament ad: " + (f"section included, {len(ad_lines)} lines from {AD_FILE}"
                             if ad_lines else "no ad file — section left off"))
    print("decisions: " + (f"{len(decisions)} waiting" if decisions else "none"))

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
               "--message", f"Morning dashboard — {day}"] + file_args
        res = subprocess.run(cmd, capture_output=True, text=True)
        sys.stdout.write(res.stdout)
        if res.returncode != 0 or "VERDICT: PASS" not in res.stdout:
            fail("the publish program did not end VERDICT: PASS — see its lines above")
    print(f"published morning.html + morning-{day}.html + {len(copies)} report files to claypnw/menu")
    print("VERDICT: PASS")


if __name__ == "__main__":
    main()
