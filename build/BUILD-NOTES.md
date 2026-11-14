# Build notes — Morning Menu

- `build/build_morning_menu.py` — builds the Morning Menu page (morning.html plus the dated archive copy) from the night's records: the Scroll edition link, KPI page, GitHub billing minutes, yard sheets, the AI community report, My Daily Review, and the night reports, in the menu's fixed order. It runs on Muse's side in the 05:45 menu job, after the 05:35 finished-check; the reader's check runs after it publishes. Its inputs are the per-job night records named inside the program.
