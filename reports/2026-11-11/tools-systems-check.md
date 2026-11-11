# Tools and systems weekly check — report 2026-11-10

Weekly run, Tuesday, November 10, 2026, about 7:40 PM Arizona time.
Last check: Monday, November 9, 2026 (report-2026-11-09.md in this same folder).
This job proposes only. Nothing was switched, adopted, connected, or bought in this run.

How each find is judged — Clay's scorecard: free first, least spend, accounts he already holds, before speed or comfort. A new service, account, or tool needs a reason rooted in the work itself. What he already has is the first road.

## Summary first

- No change that needs a choice this week. No proposal.
- Skills: no new skill in name, no skill gone in name. Two of Clay's own skills had their words changed today, November 10.
- GitHub publishing road: checked live and it passed. One change stands in that road since the last check — a mail check after a publish, added November 9 at Clay's order. It is already in place, not a proposal.
- GitHub news, November 9 and 10: seven new entries. All are Copilot, company, or dashboard items, plus a Dependabot pause that starts December 8 and a secret scanning preview for large company plans. None changes his one-person road.
- Voice, browser, and scheduling: no documented change that makes the same work better, faster, or cheaper. This job's own time moved from Monday morning to Tuesday night, under Clay's Tuesday-night order for weekly jobs.

## 1. Skill catalog — the list of playbooks Muse follows

What was checked: the built-in skills in `/opt/muse/skills` and Clay's own skills in `~/workspace/custom-skills`, name by name, against the last snapshot in this folder (`snapshot-2026-11-09.txt`, saved November 9).

- Built-in skills: 57 then, 57 now. No name added, no name removed.
  - Fit: no action. The set he has is the set that stands.
- Clay's own skills: 19 then, 19 now. No name added, no name removed.
  - Two content changes since the last snapshot, both today, November 10:
    - `answer_from_the_record` — the playbook that says check the settled record, every chat and file, before asking or answering — changed November 10 at 6:08 AM Arizona time.
    - `check_before_handover` — the playbook that says check a thing against Clay's own screen and the built thing itself before handing it over — changed November 10 at 10:37 AM Arizona time.
  - Both are his own rule work from today, not new tools from outside.
  - Fit: no action. They are already his.
- New snapshot for this run: `snapshot-2026-11-10.txt` in this same folder, with the full lists as they stand today.

Note on connectors in the snapshot: the snapshot also lists connectors so the counts can be checked next week — 81 built-in connectors now, up from 79, and 1 custom connector, unchanged. The two new built-in names are JustPark, a parking search service for the United Kingdom, and Uber Courier, a local delivery service. Neither was connected or used in this run. The full connectors review is a different job, on Tuesday nights, and is not in this job's scope.
  - Fit for this job: no action, no proposal. The count is written here only so next week's check can tell what changed.

## 2. Custom connectors and the GitHub publishing road

What was checked: the custom connectors folder `~/workspace/custom-connectors` and the GitHub publishing program itself.

- Custom connectors: 1 only — GitHub (`custom.github`). No new custom connector, none removed.
  - The connector record stands as written: it reaches only `api.github.com`, it sends, replaces, and removes files in a repository, and the key is held in Muse's registered connection — never in a file or a log.
- One change in this road since the last check, already in place:
  - On November 9 at 12:41 PM Arizona time the connector record was changed, and at 12:44 PM the publishing program was changed, to add the post-publish mail check Clay ordered: after a publish that passes, the program waits two minutes, then searches Clay's Gmail for a GitHub failure letter about that repository, prints what it finds, and writes the same lines to the standing log at `~/workspace/github-letter-watch/post-publish-checks.log`. A failed mail check never blocks a publish.
  - Fit: this stands. It was Clay's own order, it is free, and it uses the accounts he already holds. No new proposal.
- GitHub publishing road — the fine-grained token road, where Muse publishes to Clay's repositories through the GitHub API with no browser and no upload card:
  - Live check run today: `github_publish.py --check --repo morning-scroll`
  - Result, read back from the run itself: repository `claypnw/morning-scroll`, default branch `main`, final line `VERDICT: PASS` on November 10 at 7:41 PM Arizona time.
  - Fit: this road stands. It is free, it uses the account he already holds, and it is the proven road. No change proposed.

## 3. GitHub's own changelog — what GitHub changed since the last check

What was checked: GitHub's changelog front page (`github.blog/changelog`), read today, November 10 — the page copy was crawled today at 7:41 PM Arizona time. The last check already covered every November entry from November 2 to November 7, one by one. The entries below are the new ones since then, November 9 and 10.

Each item judged for a one-person escrow setup: Clay's repositories, Muse publishing for him, no team.

- **Claude Fable 5.2 in GitHub Copilot — November 9.** A new model inside Copilot, for Copilot Pro+, Max, Business, and Enterprise plans.
  - Not a fit. Clay does not buy Copilot, and Muse does his publishing work, not Copilot. Paid gear with no job to do in his setup.
- **Secret scanning detects secrets in GitHub Actions workflow logs — November 9.** GitHub now scans finished Actions workflow logs for leaked keys, in public preview for companies on GitHub Enterprise Cloud with Secret Protection or Advanced Security.
  - Not a fit today. It is a company-plan preview, and Clay's publishing road does not run Actions workflows whose logs would be scanned. The free secret scanning already noted on November 8 still stands as the part that helps any repository at no cost. No switch proposed.
- **Gemini 4 Carbon in GitHub Copilot — November 10.** A new model inside Copilot, generally available for Copilot Pro+, Max, Business, and Enterprise users.
  - Not a fit. Same reason as the Fable item above: no Copilot in his setup.
- **GitHub App support for Enterprise Copilot seat management — November 10.** Company seat handling for Copilot through a GitHub App.
  - Not a fit. Company gear for a team he does not have.
- **C++ language server now auto-configures MSBuild builds — November 10.** A Copilot coding change for C++ projects in Microsoft build tools.
  - Not a fit. Clay's repositories are published pages and records, not C++ projects, and Copilot is not in his road.
- **A more informative GitHub dashboard — November 10.** GitHub's home dashboard is more compact: six pull requests and issues shown by default instead of three, longer titles on one line, and the agent sessions part hidden when a person has none.
  - Not a fit, and no action. It changes how GitHub's own home page looks. Clay's road publishes through the API and does not go through that dashboard, so nothing in his work gets faster or cheaper.
- **Dependabot alerts will pause on inactive repositories — November 10.** Starting December 8, 2026, GitHub turns off Dependabot alerts on most repositories with no activity in the past year. Existing alerts are archived, not deleted, and can be restored at any time. Any push to a repository turns its alerts back on and starts the one-year clock over.
  - Not a fit today, and no action, with the date kept on the record. Clay's publishing road does not depend on Dependabot alerts, and every publish is a push, which by GitHub's own words turns alerts back on for a repository that is in use. A repository left untouched for a full year would have its alerts paused on December 8, and a single push restores them. No switch is proposed.

No proposal from this section. Every new item is either Copilot gear, company gear, a dashboard look change, or a dated note that needs no switch.

One date already on the record, restated only because its next step is near: the GitHub Actions change for `pull_request_target` events holds its second test shut-off on November 16, from 9:00 to 11:00 AM Arizona time, with the full block by default in public repositories starting December 2. Clay's publishing road does not use that Actions event. No action.

## 4. Voice route, browser route, and scheduling

What was checked: Muse's own docs in `~/docs` — `voice.md`, `browser.md`, `scheduling-and-watching.md`, and `muse.md` — plus the live voice-note maker at `~/workspace/bin/voice-note.sh`, the speech command itself, and this job's own place in the scheduler.

- **Voice route — the `tts` command that makes voice notes and readings.**
  - The doc `~/docs/voice.md` stands unchanged since October 28 Arizona time. No new voice, speed, or price change stands in the docs.
  - The command stands as documented: `/opt/hatch/bin/tts speak`, default voice `avocado_v2:MAI_03`, with `synthesize-script` for more than one speaker.
  - Clay's voice-note maker is unchanged: same file, last changed October 27. It still uses that same default voice, cleans the hiss and the 2.05 kHz tone, adds half a second of quiet at the start, and writes at 128 kb/s.
  - The on/off switch for chat voice notes still reads `off`, matching Clay's ruling on November 9 to stop chat voice notes. No change since the last check.
  - The saved voice choice in `~/user/voice.json` still stands as the designed voice named Grinning Keepsake, unchanged. No switch is proposed for it.
  - Fit: the road he has stands. Free, no new account, no gain shown from any other road in the docs.
- **Browser route — Muse's browser inside Muse, apart from Clay's Chrome.**
  - The doc `~/docs/browser.md` stands unchanged since November 6 Arizona time. It still sets the same road: `browser.browse` for live site work, `browser.search` / `browser.open` / `browser.find` for reading, one sign-in serving every window through the shared profile.
  - No documented change that makes the same work better, faster, or cheaper.
  - Fit: no change proposed.
- **Scheduling — the system that runs jobs while Clay is away.**
  - The doc `~/docs/scheduling-and-watching.md` stands unchanged since October 16 Arizona time. It still sets the same facts: checks run by polling at set times, not by live watching; timing is loose by minutes; a run's history, not the schedule, is the proof a job ran.
  - This job itself was checked in its own schedule record today: it stands enabled, weekly on Tuesdays at 7:40 PM Arizona time. That is a move from the Monday 10:50 AM time in the November 9 report, made under Clay's order that weekly jobs run Tuesday night. This run is the Tuesday run.
  - No documented change that makes the same work better, faster, or cheaper.
  - Fit: no change proposed.
- **One docs note, for the record:** four other Muse docs carry new change times since the last check — `muse.md` on November 10 at 6:53 PM Arizona time, and `connectors.md`, `client-surfaces.md`, and `data-handling.md` on November 10 at 1:46 PM Arizona time, with `ideas.md` and `payments-and-purchases.md` also stamped November 10 at 6:53 PM. The `muse.md` file was read whole in this run. It holds the product facts, model names, and plan facts. Nothing in it changes the voice, browser, or scheduling roads above, and nothing in it offers the same work better, faster, or cheaper. The connectors doc change goes with the two new connector names counted in section 1, which belong to the Tuesday connectors review, not this job.
  - Fit: no action.

## Proposals that need Clay's decision

None this week. This is a quiet week: no new skill worth taking, no cheaper or faster road found in the docs, and no new GitHub change that fits a one-person escrow setup.

Under this job's own rule, a quiet week gets no chat note. This report is filed only.

## What was not checked

- The full connectors list, on purpose: the Tuesday connectors review covers connectors. Only the counts and the one custom GitHub connector were checked here, to keep the snapshot whole.
- No live test publish was sent to GitHub in this run. The road was proved with the harmless read check only, which is the check the connector record itself names.
- Skill contents, apart from change times, were not read line by line. This check diffs names and change times, as the job sets it.
- The two new GitHub changelog entries for Copilot models were judged from GitHub's own changelog page and its titles and plan lines, not from a paid Copilot trial, which this job does not start.
