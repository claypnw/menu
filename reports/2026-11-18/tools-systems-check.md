# Tools and systems weekly check — report 2026-11-17

Weekly run, Tuesday, November 17, 2026, about 7:40 PM Arizona time.
Last check: Tuesday, November 10, 2026 (report-2026-11-10.md in this same folder).
This job proposes only. Nothing was switched, adopted, connected, or bought in this run.

How each find is judged — Clay's scorecard: free first, least spend, accounts he already holds, before speed or comfort. A new service, account, or tool needs a reason rooted in the work itself. What he already has is the first road.

## Summary first

- No change that needs a choice this week. No proposal.
- Skills: one new built-in skill name and three new skills of Clay's own since November 10. All are already in place; none needs a switch.
- Custom connectors: the folder no longer holds GitHub only. Cloudflare and Gemini were added November 12–14, on Clay's own work in those days. That widens the set this job will check from now on.
- GitHub publishing road: checked live and it passed. A batch publishing program was added November 12 — it sends a whole run's files as one commit instead of one commit per file, so a website build runs once per run. It is already in place, not a proposal.
- GitHub news, November 11 to 17: about thirty-one new changelog entries. Almost all are Copilot models, Copilot company gear, or client-app items. The three that touch a one-person setup — issue types for personal accounts, secret scanning for Cloudflare tokens, and GitHub Event Streams — are judged below; none changes his publishing road and none is proposed.
- Voice, browser, and scheduling: the browser doc gained a Muse for Chrome section on November 13, and the scheduling doc changed on November 11. Neither makes the same work better, faster, or cheaper for Clay's setup, for the reasons given in section 4.

## 1. Skill catalog — the list of playbooks Muse follows

What was checked: the built-in skills in `/opt/muse/skills` and Clay's own skills in `~/workspace/custom-skills`, name by name, against the last snapshot in this folder (`snapshot-2026-11-10.txt`, saved November 10).

- Built-in skills: 57 then, 58 now. One name added, none removed.
  - `remember-products` — a playbook for saving products Clay asks to remember, in named lists, and showing them again as product cards without a new search.
  - Fit: no action. It is already built in, it is free, and it serves shopping work he already does. No switch is needed to use it.
- Clay's own skills: 19 then, 22 now. Three names added, none removed.
  - `cloudflare-security-audit` — a security audit playbook, added November 15.
  - `name_the_whole_set_first` — the playbook that says name the whole set item by item before scoping, added November 14.
  - `sweep_dependents_after_a_production_move` — the playbook that says list, update, and verify every builder, checker, menu, and link after a published page moves, added November 13.
  - All three are Clay's own rule and work product from this week, not new tools from outside.
  - Fit: no action. They are already his.
  - Three standing skills also had their words changed since November 10: `answer_from_the_record` on November 11, `check_before_handover` on November 12, and `outside_work_access_gate` on November 16. Same judgment: his own rule work, already in place.
- New snapshot for this run: `snapshot-2026-11-17.txt` in this same folder, with the full lists as they stand today.

Note on connectors in the snapshot: the snapshot also lists connectors so the counts can be checked next week — 112 built-in connectors now, up from 81 (32 names added, `shopify-ucp` removed), and 3 custom connectors, up from 1. The full connectors review is a different job, on Tuesday nights, and is not in this job's scope.
  - Fit for this job: no action, no proposal. The counts are written here only so next week's check can tell what changed, and so the Tuesday connectors review has the jump on its record.

## 2. Custom connectors and the GitHub publishing road

What was checked: the custom connectors folder `~/workspace/custom-connectors` and the GitHub publishing programs themselves.

- Custom connectors: 3 now, not 1. The job body still says "today: GitHub only" — that line is out of date and is corrected here.
  - `custom.github` — unchanged in its record since November 9. It reaches only `api.github.com`, it sends, replaces, and removes files in a repository, and the key is held in Muse's registered connection — never in a file or a log.
  - `custom.cloudflare` — added November 12–14. It reaches only `api.cloudflare.com`, with a token that holds one permission, Cloudflare Pages with Edit access, on Clay's account. Its record names what that scope does and does not reach, proven November 14.
  - `custom.gemini` — added November 13. It reaches only `generativelanguage.googleapis.com`, lists the models the account can call, and generates text from a brief, printing the usage counts each call returns. This is the road Clay settled on November 16 for Gemini-led product searches.
  - Fit: all three stand. Each is free to hold, each uses an account Clay already holds, and each was built on his own order in other work. No new proposal from this job.
- One change in the GitHub road since the last check, already in place:
  - On November 12 a batch publishing program, `github_publish_batch.py`, was added beside the standing program. The standing program sends each file with its own commit, and every commit to a website repository starts a fresh site build. The batch program lands a whole run's files as a single commit through the Git Data API — one push, one build — it skips files that already stand byte-for-byte, it reads every sent file back, and it keeps the November 9 post-publish mail check.
  - Fit: this stands, and it is the one clear cheaper-and-faster gain found this week — fewer builds for the same publish. It was built in other work, it is already in place, and no switch is proposed by this job.
- GitHub publishing road — the fine-grained token road, where Muse publishes to Clay's repositories through the GitHub API with no browser and no upload card:
  - Live check run today: `github_publish.py --check --repo morning-scroll`
  - Result, read back from the run itself: repository `claypnw/morning-scroll`, default branch `main`, final line `VERDICT: PASS` on November 17 at 7:41 PM Arizona time.
  - Fit: this road stands. It is free, it uses the account he already holds, and it is the proven road. No change proposed.

## 3. GitHub's own changelog — what GitHub changed since the last check

What was checked: GitHub's changelog front page (`github.blog/changelog`), read today, November 17 — the page copy was crawled today at 7:41 PM Arizona time. The last check covered entries through November 10. The entries below are the new ones, November 11 to 17.

Each item judged for a one-person escrow setup: Clay's repositories, Muse publishing for him, no team.

### The three that touch a one-person setup

- **Issue types and fields are available for personal accounts — November 11.** Custom issue types (defaults Bug, Task, Feature; up to 25) and issue fields (Priority, Effort, Start date, Target date; text, number, date, and choice kinds) are now generally available on repositories a personal account owns, with project views, bulk edits, and API use.
  - Not a fit today, and no proposal. It is free and it is on the account he already holds, which passes the scorecard — and it still has no job to do: Clay's work is tracked in his Goals and his own records, not in GitHub Issues, and no repository of his uses issues to plan work. Taking it up would be a new way of working for its own sake. If a repository ever starts carrying real issue work, this is the first road to look at.
- **Secret scanning detects Cloudflare service tokens — November 12.** GitHub's secret scanning now detects the `cloudflare_access_service_token` type, with partner secrets reported to the issuer when found in public repositories.
  - Fit, as a passive gain only — no action and no proposal. It is automatic, it costs nothing, and it adds a guard around the Cloudflare road Clay took up this week. Nothing needs to be switched on by this job for the detector to exist; his own Cloudflare token is held in the registered connection, never in a repository file.
- **GitHub Event Streams is now in preview — November 17.** An agent can subscribe to a pull request and be woken by events (a review, new commits, a conflict, a merge) instead of polling, with no public webhook endpoint. Access is by waitlist; it is in preview on all plans once approved.
  - Not a fit. Clay's publishing road sends straight to the `main` branch through the API and does not use pull requests, so there is no pull-request polling for this to save. It is also a waitlist preview — a new signup with no work rooted in his setup.

### The rest, grouped

- **Copilot models and Copilot features — November 13, 16, and 17 (the large majority).** New and deprecated Copilot models (GPT-6.2 Astra and Sol, MAI Code 2 and MAI Code 2 Flash, Gemini 4 Hydrogen, plus model deprecations dated December and February), Copilot Fusion updates, the Copilot app and JetBrains and Ignite releases, Copilot code review adaptive effort, Copilot Evals in public preview, Copilot benchmarks, Copilot interacting with a browser, and control over where Copilot customizations come from.
  - Not a fit. Clay does not buy Copilot, and Muse does his publishing work, not Copilot. Paid gear with no job to do in his setup.
- **Secret scanning on demand for developers and agents — November 17.** Copilot's security review can now run GitHub's secret scanning detectors on changes before merge, in Copilot CLI, the Copilot app, the Copilot SDK, and Copilot code review. It is off by default, needs an opt-in, and scans consume AI credits.
  - Not a fit. It rides on Copilot, which is not in his road, and it spends credits. The free repository secret scanning already on his record is the part that helps him.
- **Company and enterprise gear — November 16 and 17.** Budget limit raised to 40,000 budgets per account, monitoring Copilot activity through Microsoft Agent 365, Copilot CLI Microsoft Entra sign-in in preview, and GitHub Enterprise Server support in the Copilot app.
  - Not a fit. Company gear for a team and an enterprise he does not have.
- **AI Scan administration — November 13 and 16.** Managing AI Scan for repositories through the REST API, and bulk-starting AI Scan across repositories.
  - Not a fit today. His repositories are published pages and records, and no AI Scan work stands in his setup. No switch proposed.
- **Dependabot alert dismissal requests now last one year — November 16.** A granted dismissal request for a Dependabot alert now holds for one year.
  - Not a fit, and no action. His publishing road does not depend on Dependabot alerts. The standing date from November 10 still stands: Dependabot alerts pause on repositories with no activity in the past year starting December 8, and any push restarts that clock.
- **Small client and actions items — November 12, 13, and 16.** Actions for ARM32 Linux and Windows retirement, public monitoring alerts gaining direct links, GitHub Mobile on iPhone Duo, VS Code retiring the Local harness in February 2027, and tracking Copilot code review outcomes in Repository insights.
  - Not a fit, and no action. None touches the API publishing road, his repositories, or a device or build he uses.

No proposal from this section.

Dates already on the record, restated only because they are near: the GitHub Actions change for `pull_request_target` events held its second test shut-off on November 16, with the full block by default in public repositories starting December 2 — Clay's road does not use that event. The Dependabot inactive-repository pause starts December 8. No action on either.

## 4. Voice route, browser route, and scheduling

What was checked: Muse's own docs in `~/docs` — `voice.md`, `browser.md`, `scheduling-and-watching.md`, and `muse.md` — plus the live voice-note maker at `~/workspace/bin/voice-note.sh`, its on/off switch, and the speech command itself.

- **Voice route — the `tts` command that makes voice notes and readings.**
  - The doc `~/docs/voice.md` stands unchanged since October 28 Arizona time. No new voice, speed, or price change stands in the docs.
  - The command stands as documented: `/opt/hatch/bin/tts speak`, default voice `avocado_v2:MAI_03`, with `synthesize-script` for more than one speaker.
  - Clay's voice-note maker is unchanged: same file, last changed October 27. It still uses that same default voice, cleans the hiss and the 2.05 kHz tone, adds half a second of quiet at the start, and writes at 128 kb/s.
  - The on/off switch for chat voice notes still reads `off`, matching Clay's ruling on November 9 to stop chat voice notes. No change since the last check.
  - The saved voice choice in `~/user/voice.json` still stands as the designed voice named Grinning Keepsake, unchanged.
  - Fit: the road he has stands. Free, no new account, no gain shown from any other road in the docs.
- **Browser route — Muse's browser inside Muse, apart from Clay's Chrome.**
  - The doc `~/docs/browser.md` changed on November 13 at 4:22 PM Arizona time. The change adds a Muse for Chrome section: an extension, installed from muse.ai/chrome-extension, that lets Muse browse in the user's own Chrome on a computer, using sites they are already signed in to. The same doc sets its limits: it works for messages sent from that computer, it cannot be used from a phone, and Chrome on phones and iPads does not support extensions.
  - The rest of the road stands as before: `browser.browse` for live site work, `browser.search` / `browser.open` / `browser.find` for reading, one sign-in serving every window through the shared profile.
  - Fit: no change proposed, and no proposal. The extension is free, and it uses his own Chrome — and it does not fit the work this job checks: his publishing and scheduled work runs on this machine and from his phone, neither of which the extension serves, and his standing road already reaches the sites his work needs. A new install on his PC needs a reason rooted in the work itself, and none stands this week.
- **Scheduling — the system that runs jobs while Clay is away.**
  - The doc `~/docs/scheduling-and-watching.md` changed on November 11 at 3:24 PM Arizona time. Its core facts stand as before: checks run by polling at set times, not by live watching; timing is loose by minutes; a run's history, not the schedule, is the proof a job ran. The changed wording adds that a job whose run ends blocked on something durable pauses itself and tries again at a later scheduled time, and that `cron.status` shows the block.
  - Fit: no change proposed. That is a clearer statement of how blocked jobs already behave, not a better, faster, or cheaper road.
  - This job itself stands as last reported: weekly on Tuesdays at 7:40 PM Arizona time. This run is the Tuesday run.
- **One docs note, for the record:** `~/docs/muse.md` carries a change time of today, November 17 at 7:03 PM Arizona time, and new or changed docs stand for referrals (November 17), payments and purchases (November 16), spaces (November 13), and privacy and credentials (November 11). The `muse.md` file was read in this run. It holds the product facts, model names, and plan facts. Nothing in it changes the voice, browser, or scheduling roads above, and nothing in it offers the same work better, faster, or cheaper. The connectors doc stands unchanged since November 10; the large built-in connector count jump in section 1 belongs to the Tuesday connectors review, not this job.
  - Fit: no action.

## Proposals that need Clay's decision

None this week. No new skill worth taking, no cheaper or faster road that is not already in place, and no new GitHub change that fits a one-person escrow setup and needs his word. The week's real gains — the batch publishing program, the two new custom connectors, and the three new skills of his own — were all built on his orders in other work and already stand.

Under this job's own rule, a week with no proposal gets no chat note. This report is filed only.

## What was not checked

- The full connectors list, on purpose: the Tuesday connectors review covers connectors. Only the counts and the three custom connectors were checked here, to keep the snapshot whole and to correct the job body's out-of-date "GitHub only" line.
- No live test publish was sent to GitHub in this run. The road was proved with the harmless read check only, which is the check the connector record itself names.
- Skill contents, apart from the new skills' own descriptions and change times, were not read line by line. This check diffs names and change times, as the job sets it.
- The Copilot changelog entries were judged from GitHub's own changelog page, its titles, and the three entries read in full (issue types for personal accounts, secret scanning for Cloudflare tokens, Event Streams, and secret scanning on demand), not from a paid Copilot trial, which this job does not start.
