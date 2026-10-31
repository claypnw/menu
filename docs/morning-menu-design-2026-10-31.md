# The Morning Menu — design and what changed

Clay's order, Saturday, October 31, 2026. Written the same day.

## What Clay asked for

Clay was tired of scrolling up and down through scattered overnight text dumps in the chat. He named the ITIL nightly-processing report as the standard: one menu every morning, numbered options, each opening a report. Four rulings shaped the final form:

1. No combined report in any form. The menu is an index only — no report content in it. Behind each option stands that item's own separate report file (its own PDF), one report per item that has a status that night.
2. The hourly status report is the form reference (status per item, exceptions named, counts resting on named records), not a merge target — the menu stands on its own.
3. Chat option buttons are one-shot — after one tap the rest were gone. So the menu is a web page Clay can open any time and tap in any order, as often as he likes.
4. Full production discipline: a fixed builder program makes the page (no freehand HTML each night), the production copy stands alone outside Muse (escrow, below), the process has its flow chart, and the scheduled run is the proof — no hand-run of the production job to test it.

## The shape

- **The page**: `morning.html` at the root of the claypnw/menu repository (the Admin Menu site), rebuilt daily, plus a dated archive copy `morning-<date>.html`. Title: "Morning Menu — <weekday, date>". One row per item: its number and name as links, and a short status line under them. Pending decisions stand on the page as plain text lines (question + choices named). The page's last line names the privacy fact: the menu site is a public GitHub Pages site, so anyone holding the address can open the page and the reports behind it.
- **The reports**: local report files are copied into the same repository under `morning-files/<date>-<slug>` (kpi, lists, billing, community, mailbox PDFs; podcast MP3; the maker-finds side-by-side picture as `<date>-finds.jpg`). Items already public link straight out: the Scroll edition PDF and the yard sheets on the Morning Scroll site, the My Daily Review page, and a maker find's own listing page.
- **The chat message**: one short message — one line saying the morning menu is ready, plus the page link. Pending decisions, when any exist, get their own tappable choice buttons in that same message, under the link. Menu items never get chat buttons.
- **The record**: each night's menu record JSON (`morning-menu-<date>.json`, in the morning-agenda-briefing goal's hidden files) carries every item's full status, its short page line, its links, and the record each status rests on. The morning-menu job's finish line rests on it.

## The moving parts

- **morning-menu** (new cron, daily 05:20 America/Phoenix, owner goal:morning-agenda-briefing): collects the night's report files and statuses from their named records, collects pending decisions from the completion pile, writes the menu record, runs the builder program, and hands one short handoff to the main chat.
- **build_morning_menu.py** (fixed builder, `~/workspace/morning-post/batch/`): reads the menu record, renders `morning.html` + the dated copy, and publishes them with the day's report copies to claypnw/menu in one run of the GitHub key program (`github_publish.py`). Ends VERDICT: PASS/FAIL. A `--local-only` mode builds into a local folder and publishes nothing (the test road).
- **build_billing_pdf.py** (new): turns the billing watch's dated verify log + watch record into the day's one-page billing PDF.
- **build_lists_pdf.py** (new): turns the briefing's lists file into the day's lists PDF.

## What changed in the overnight jobs (all 2026-10-31)

Every job below keeps all of its work, records, gates, and finish/error lines. Only the delivery changed: no chat message; the report stands in its files, and the morning menu carries it.

- **github-billing-watch**: daily chat report removed; the job now builds its own billing PDF right after its verify log. Its ALARM messages stay as their own chat messages: payment failed or at risk, a new charge or billed amount above $0, plan no longer Pro, the check itself failing, and the 75%-of-included-minutes alarm.
- **gilded-pages-healthcare-rollout**: the "Report to the admin in the main chat" instruction removed; the batch record stands in the progress file, the batch verify log, and the finish line.
- **yard-estate-sales-refresh**: the step-13 chat report removed. The sources read / not read naming is preserved in the two places the morning check reads: the run's own report text and the finish line's result text.
- **yard-estate-sales-recheck**: the new-sale chat report removed — on every morning the job now records only; new sales are named in the finish line so the menu carries them.
- **daily-community-learning-check**: chat deliveries removed (the nightly summary and the 15-day-review message). The 15-day proposal is recorded in the dated log and the finish line as a pending decision for the menu. The talk-watch hook is untouched (event-driven, not a report).
- **ai-stories-podcast-nightly**: the delivery chat message removed; the MP3 is the delivery, carried by the menu.
- **maker-finds-watch**: the per-round chat message removed; picks are written to the dated run-log folder (run-log.md + side-by-side images), the finish line names them, and the menu carries the count. The six-empty-rounds question is recorded as a pending decision, not asked in chat.
- **morning-agenda-briefing**: the sent chat briefing stopped. The job still builds and publishes the Scroll; the full lists plus a "morning record" section (the step-10 quotes, the batch status list, the mismatch count, the completion-pile lines) now stand in the briefing-lists file, which the job turns into the lists PDF. Pile marking now keys on inclusion in the morning record. The finish line still carries "Mismatch count today: N (target 0)".
- **morning-jobs-finished-check**: the chat report removed; every computation and record is unchanged. Its delivery is the KPI PDF plus its full report text file (report-message.txt), carried by the menu.
- **hourly-status-update**: unchanged — it stays its own thing; it was the form reference only.

## Escrow (the Contractor Rule)

The production copy stands alone outside Muse: this design note, the builder program (`build_morning_menu.py`), and the morning-menu job's instructions are published in the `docs/` folder of the claypnw/menu repository, alongside the page they produce. The PDF builders live with the other morning batch programs (`~/workspace/morning-post/batch/`) and are covered by the nightly escrow compare like the rest of production.

## Tests (2026-10-31, against today's published outputs only)

- Both PDF builders ran on October 31 files and their PDFs were read back: billing — 1 page, plan/minutes/per-site/album lines correct; lists — 3 pages, headings and items correct (a bullet-dash fault was found and fixed, then re-verified).
- The menu builder ran in `--local-only` mode against a fixture built from today's real menu record and today's published page lines: its page carries the same 10 items in the same order, the same 10 status lines, and the same 12 links — the copied files under the exact `morning-files/2026-10-31-*` names, the Scroll/yard/review/listing links pointing at the same live addresses (the Scroll PDF and the finds image were fetched live and resolve). The dated archive copy came out byte-identical to the standing page.
- The production morning-menu job was NOT hand-run. Its first proof is tomorrow's (November 1) scheduled 05:20 run.
