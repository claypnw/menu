# Morning dashboard builder — build notes

Placed 2026-11-23 through change control (Hearth ITIL 2.11), closing gap 1 of the pickup check's first run (2026-11-23): the current builder stood only on the working machine, in no repository, so the dashboard could not be re-made from GitHub alone.

- The builder: `build/build_morning_dashboard.py` (55,947 bytes) — the current program, carrying the November 22, 2026 color redesign (parchment sheet on dark walnut, gold trim, burgundy titles, colored status pills) and the November 23, 2026 fixes (linked filament lines, linked Raven's Reach one-line items, the linked AI Transfer box, the whole-page tap pass, the Maggie Apps Report box line, and the archive-process link line).
- Working copy it was placed from: `~/workspace/morning-post/batch/build_morning_dashboard.py` on the working machine. The two stand byte-identical at placement.
- What it does: the morning-menu job collects the night's statuses into the menu record (`morning-menu-<date>.json`); this program renders the dashboard page from that record plus the night KPI record and the standing filament ad file, and publishes the page and the day's report files into this repository. Its full input and behavior notes stand in the program's own header.
- The older builder it replaces: `build/build_morning_menu.py` (12,530 bytes, the pre-redesign program) was removed through the same controlled road in the same sitting; the dashboard's current form is built only by `build_morning_dashboard.py`.
- Rollback: the removed older builder and the prior form of these notes stand in this repository's history.
