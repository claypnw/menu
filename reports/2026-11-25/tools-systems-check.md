# Tools and systems weekly check — report 2026-11-24

Weekly run, Tuesday, November 24, 2026, about 7:40 PM Arizona time.
Last check: Tuesday, November 17, 2026 (report-2026-11-17.md in this same folder).
This job proposes only. Nothing was switched, adopted, connected, or bought in this run.

How each find is judged — Clay's scorecard: free first, least spend, accounts he already holds, before speed or comfort. A new service, account, or tool needs a reason rooted in the work itself. What he already has is the first road.

## Summary first

- No change that needs a choice this week. No proposal.
- Skills: built-in count stands at 58 — one name added (`proactive-work`), one removed (`app-creation`). Clay's own skills: 22 then, 24 now — two added, both his own rule work. Three standing custom skills also changed their words.
- Custom connectors: still 3 (GitHub, Cloudflare, Gemini). No new custom connector.
- GitHub publishing road: checked live and it passed. Two changes landed on November 24 itself, already in place, both to cut Cloudflare builds: the single-file publisher now skips a file that already stands byte-for-byte, and the batch publisher can now send files and remove files in one commit. On November 23 the publishers also stopped reading Gmail after a publish and now write a SEARCH OWED line for the letter-watch job instead — that change was already on the record and stands in the current programs.
- GitHub news, November 18 to 24: the entries that touch a one-person setup are issue statuses and repository boards in public preview (November 23), a secret-scanning false-positive cut for Slack (November 23), more predictable notifications from December 1, and `gh event listen` for pull-request events (November 19). None changes his publishing road and none is proposed, for the reasons in section 3.
- Voice, browser, and scheduling: voice and scheduling docs unchanged since the last check. The browser doc changed on November 19; re-read, it makes no road better, faster, or cheaper for Clay's setup.

## 1. Skill catalog — the list of playbooks Muse follows

What was checked: the built-in skills in `/opt/muse/skills` and Clay's own skills in `~/workspace/custom-skills`, name by name, against the last snapshot in this folder (`snapshot-2026-11-17.txt`, saved November 17).

- Built-in skills: 58 then, 58 now. One name added, one removed.
  - Added: `proactive-work` — a playbook for private proactive work: a private copy of the main agent works for the user unasked and hands one result back, with scaffolds for connections, health, loved ones, money, places, projects, shopping, tracking, trips, the week ahead, and work follow-through.
  - Removed: `app-creation` — no longer in the built-in set. No replacement name was claimed by this check; the artifact/space tools are the standing road for pages and apps, and that road was not changed by this job.
  - Fit: no action. Both changes are in Muse's own built-in set, managed by the product, free, and already in place. No switch is needed or proposed.
- Clay's own skills: 22 then, 24 now. Two names added, none removed.
  - `deliver_full_corrected_set` — added November 20. When a set is asked to be corrected, deliver the whole corrected set with every accepted change in place, not a critique or a gap list.
  - `investigate_failure_before_retry` — added November 22. Keep the full error, find its cause, and fix that cause before any retry is treated as the answer.
  - Both are Clay's own rule and work product from this week, not new tools from outside.
  - Fit: no action. They are already his.
  - Two standing skills also had their words changed since November 17: `answer_from_the_record` on November 22 and `check_before_handover` on November 24. Same judgment: his own rule work, already in place.
- New snapshot for this run: `snapshot-2026-11-24.txt` in this same folder, with the full lists as they stand today.

Note on connectors in the snapshot: the snapshot also lists connectors so the counts can be checked next week — 151 built-in connectors now, up from 112 (39 names added, none removed: adobe, ahrefs, airtable, app_00widget, apple_music, basecamp, beehiiv, carrefour, circleback, cloudflare, crunchbase, deepl, descript, dreamrender, filament, gamma, getmattered, google-travel, gopuff, hootsuite, hubspot, krea, kukini, luma, opendoor, opusclip, otter, pandadoc, paperoffice_ai, pool, rememberthemilk, security_ctf, studocu, superhuman, sweetgreen, trustandwill, typeform, walmart, wix), and 3 custom connectors, unchanged. The full connectors review is a different job, on Tuesday nights, and is not in this job's scope.
  - Fit for this job: no action, no proposal. The counts are written here only so next week's check can tell what changed.

## 2. Custom connectors and the GitHub publishing road

What was checked: the custom connectors folder `~/workspace/custom-connectors` and the GitHub publishing programs themselves.

- Custom connectors: still 3. The job body still says "today: GitHub only" — that line stays out of date, as noted last week.
  - `custom.github` — its record (CONNECTOR.md) is unchanged since November 9. It reaches only `api.github.com`, and the key is held in Muse's registered connection — never in a file or a log. Its two programs changed this week; see below.
  - `custom.cloudflare` — unchanged since November 14. It reaches only `api.cloudflare.com`, with a token holding one permission, Cloudflare Pages with Edit access, on Clay's account.
  - `custom.gemini` — its record changed on November 21 and its helper `gemini_call.py` changed the same day. No new work is given to Gemini under Clay's order of November 22, so this job notes the change and proposes nothing about it.
  - Fit: all three stand as records. Each is free to hold and uses an account Clay already holds. No new proposal from this job.
- Changes in the GitHub road since the last check, all already in place:
  - November 23 (already on Clay's record, verified in the current programs in this run): the publishers no longer read Gmail after a publish. `github_publish.py` writes a SEARCH OWED line instead, and the github-letter-watch job runs the failure-letter searches. This keeps a Gmail approval ask from surfacing inside a publishing worker.
  - November 24, the Cloudflare build cut, in `github_publish.py`: a file whose standing record already matches the local file is not sent — no commit, and no site build. A run where every named file already stands unchanged lands nothing and writes no owed line and no change-control record. The expected-sha refusal check still runs first, so a stale base is still refused even when the content matches.
  - November 24, the Cloudflare build cut, in `github_publish_batch.py`: removals now ride the same commit as sends (`--delete`). A run can send files and remove files in one commit — one push, one build — and a run may name only removals. Each removed path is read back and must no longer stand.
  - Fit: both November 24 changes stand, and they serve the settled one-build-per-site-per-day round and the free plan's 500 builds a month. Fewer commits for the same publish is a cheaper road on an account he already holds, built in other work and already in place. No switch is proposed by this job.
- GitHub publishing road — the fine-grained token road, where Muse publishes to Clay's repositories through the GitHub API with no browser and no upload card:
  - Live check run today: `github_publish.py --check --repo morning-scroll`
  - Result, read back from the run itself: repository `claypnw/morning-scroll`, default branch `main`, final line `VERDICT: PASS` on November 24 at 7:40 PM Arizona time, exit code 0.
  - Fit: this road stands. It is free, it uses the account he already holds, and it is the proven road. No change proposed.

## 3. GitHub's own changelog — what GitHub changed since the last check

What was checked: GitHub's changelog month page for November 2026 (`github.blog/changelog/month/11-2026/`), read today, November 24, with the Slack secret-scanning entry read in full. The last check covered entries through November 17. The entries below are the new ones, November 18 to 24.

Each item judged for a one-person escrow setup: Clay's repositories, Muse publishing for him, no team.

### The ones that touch a one-person setup

- **Issue statuses and repository boards in public preview — November 23.** Issues now carry statuses (Backlog, In progress, In review, and others; seven in all) that show across the issues page and dashboard and can be filtered with `status:`, and repositories gain saved board views with drag-and-drop status updates.
  - Not a fit today, and no proposal. It is free and on the account he already holds — and it still has no job to do, for the same reason as last week's issue types and fields: Clay's work is tracked in his Goals and his own records, not in GitHub Issues, and no repository of his uses issues to plan work.
- **Secret scanning reduces false positives for Slack — November 23.** The `slack_incoming_webhook_url` detector now excludes URLs that do not use Slack's incoming-webhook format. Published November 23, read in full in this run.
  - Fit, as a passive gain only — no action and no proposal. It is automatic and costs nothing. Clay does not use Slack secrets in his repositories, so the gain is small; nothing needs to be switched on.
- **More predictable notifications on GitHub.com — starting December 1.** Over the week from December 1, routine actions (commenting, submitting a review, changing thread state, merge queue activity) no longer resubscribe a user after they unsubscribe; mentions, assignments, and review requests still will.
  - Fit, as a passive gain only — no action and no proposal. It is automatic, free, and it slightly cuts unwanted GitHub mail on his account. His publishing road does not depend on notifications.
- **Pull-request events now waitable via `gh event listen` — November 19.** GitHub CLI v2.105.0 supports Event Streams: `gh event listen` with a pull-request URL prints each event as JSON instead of polling.
  - Not a fit, for the same reason as last week's Event Streams preview: Clay's publishing road sends straight to the `main` branch through the API and does not use pull requests, so there is no pull-request polling for this to save. It is also a preview that needs Event Streams access.

### The rest, grouped

- **Pin your favorite repositories to your dashboard — announced, then rolled back November 23.** GitHub's own editor's note says the change was temporarily rolled back on November 23 while the experience is improved.
  - Not a fit, and no action. It is a dashboard comfort item, it is not standing live, and it does not touch the publishing road.
- **Code coverage uploads reject non-Cobertura XML — November 23, and usage reports gain a `user_id` column on December 1.** The upload-code-coverage action now fails with a clear error on a non-Cobertura report; detailed, AI, and premium request usage reports gain a `user_id` column after `username` on December 1, shifting later columns.
  - Not a fit, and no action. Clay's setup runs neither coverage uploads nor scripts that read those usage reports by column position.
- **GitHub Enterprise Server 3.23 release candidate — November 20.** Projects filter improvements (OR and parentheses), AI secret detection that runs on the appliance itself, and expiring OAuth tokens in preview.
  - Not a fit. Enterprise Server is a self-hosted company product; Clay uses github.com on a personal account.
- **Company and organization gear — November 19 and 20.** Security advisory work through scoped custom repository roles (organization owners), Azure DevOps live migrations to GitHub Enterprise Cloud with data residency now generally available, GHE.com audit logs streaming to S3 via OIDC, and RHEL 9 and 10 runner images for Team and Enterprise Cloud larger runners.
  - Not a fit. Company gear for organizations and enterprises he does not have, on plans he does not hold.
- **Small client items — November 20.** GitHub Desktop 3.7.0 supports multiple accounts per host, and failed optional checks no longer block a mergeable pull request.
  - Not a fit, and no action. Clay does not use GitHub Desktop for publishing — the API road does that work — and his road does not use pull requests.
- **Copilot items — November 18.** Copilot gained connectors to eight more services through GitHub-verified MCP servers in public preview (Box, Buildkite, Calendly, ClickUp, Mixpanel, Supabase, Webflow, Wix), and Gemini 4 Neon became generally available in Copilot for paid Copilot plans.
  - Not a fit. Clay does not buy Copilot, and Muse does his publishing work, not Copilot. Paid gear with no job to do in his setup.

No proposal from this section.

Dates already on the record, restated only because they are near: the GitHub Actions change for `pull_request_target` events blocks by default in public repositories starting December 2 — Clay's road does not use that event. The Dependabot inactive-repository pause starts December 8; any push restarts that clock. Hosted runners stop running ARM32 jobs on December 8; his road runs no hosted ARM32 jobs. No action on any of these.

## 4. Voice route, browser route, and scheduling

What was checked: Muse's own docs in `~/docs` — `voice.md`, `browser.md`, `scheduling-and-watching.md`, and `muse.md` — plus the live voice-note maker at `~/workspace/bin/voice-note.sh`, its on/off switch, and the speech command itself.

- **Voice route — the `tts` command that makes voice notes and readings.**
  - The doc `~/docs/voice.md` stands unchanged since October 28 Arizona time. No new voice, speed, or price change stands in the docs.
  - The command stands as documented: `/opt/hatch/bin/tts speak`, default voice `avocado_v2:MAI_03`, with `synthesize-script` for more than one speaker.
  - Clay's voice-note maker is unchanged: same file, last changed October 27. It still uses that same default voice, cleans the hiss and the 2.05 kHz tone, adds half a second of quiet at the start, and writes at 128 kb/s.
  - The on/off switch for chat voice notes still reads `off`, matching Clay's ruling on November 9 to stop chat voice notes. No change since the last check.
  - The saved voice choice in `~/user/voice.json` still stands as the designed voice named Grinning Keepsake, unchanged since November 8.
  - Fit: the road he has stands. Free, no new account, no gain shown from any other road in the docs.
- **Browser route — Muse's browser inside Muse, apart from Clay's Chrome.**
  - The doc `~/docs/browser.md` changed on November 19 at 4:57 PM Arizona time. Re-read in this run: the Muse for Chrome section stands as reported last week (extension from muse.ai/chrome-extension, works only for messages sent from that computer, no phone use), and the rest of the road stands as before — `browser.browse` for live site work, `browser.search` / `browser.open` / `browser.find` for reading, `browser.windows` to list and manage windows and tabs, one sign-in serving every window through the shared profile.
  - Fit: no change proposed. Nothing in the changed doc offers the same work better, faster, or cheaper for Clay's setup, and the extension judgment from last week stands: his publishing and scheduled work runs on this machine and from his phone, neither of which the extension serves.
- **Scheduling — the system that runs jobs while Clay is away.**
  - The doc `~/docs/scheduling-and-watching.md` stands unchanged since November 11. Its core facts stand as before: checks run by polling at set times, not by live watching; timing is loose by minutes; a run's history, not the schedule, is the proof a job ran.
  - Fit: no change proposed. No better, faster, or cheaper road stands in the doc.
  - This job itself stands as last reported: weekly on Tuesdays at 7:40 PM Arizona time. This run is the Tuesday run.
- **One docs note, for the record:** `~/docs/muse.md` changed today, November 24, and a new `~/docs/ideas.md` stands dated today; `client-surfaces.md` changed November 23, and `payments-and-purchases.md` and `privacy-and-credentials.md` changed November 19. Nothing in those changes touches the voice, browser, or scheduling roads above, and nothing in them offers the same work better, faster, or cheaper. The connectors doc stands unchanged since November 10; the built-in connector count jump in section 1 belongs to the Tuesday connectors review, not this job.
  - Fit: no action.

## Proposals that need Clay's decision

None this week. No new skill worth taking, no cheaper or faster road that is not already in place, and no new GitHub change that fits a one-person escrow setup and needs his word. The week's real gains — the two November 24 build-cut changes in the GitHub publishers — were built in other work and already stand.

Under this job's own rule, a week with no proposal gets no chat note. This report is filed only.

## What was not checked

- The full connectors list, on purpose: the Tuesday connectors review covers connectors. Only the counts and the three custom connectors were checked here, to keep the snapshot whole.
- No live test publish was sent to GitHub in this run. The road was proved with the harmless read check only, which is the check the connector record itself names.
- Skill contents, apart from the new skills' own descriptions and change times, were not read line by line. This check diffs names and change times, as the job sets it.
- The GitHub changelog entries were judged from GitHub's own changelog month page and the one entry read in full (secret scanning for Slack, November 23), plus a release-notes index summary for titles and dates the month page truncates — not from a paid Copilot trial, which this job does not start.
- The browser doc's November 19 change was judged from a full re-read of the current doc and its change time; no prior copy of the doc stands on this machine to diff against, so the exact changed lines are not claimed.
