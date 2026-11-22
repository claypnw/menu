// The follow-lists store keeper — Cloudflare Pages Function.
//
// Serves /api/follow-lists on the menu site:
//   GET    -> { youtube: [...handles], x: [...handles] }
//   POST   { list: "yt" | "x", handle } -> adds the handle
//   DELETE { list: "yt" | "x", handle } -> removes the handle
// POST and DELETE answer with the fresh full lists, same shape as GET.
//
// The lists stand in the D1 database "follow-lists", bound to this
// Pages project as FOLLOW_DB (tables youtube_channels and x_handles,
// each: handle TEXT PRIMARY KEY, added TEXT). Clay edits the lists on
// follow-lists.html; the nightly jobs (the YouTube transcription
// downloads and the X post log) read the same store at run start.

const TABLES = { yt: "youtube_channels", x: "x_handles" };
const HANDLE_OK = /^[A-Za-z0-9._-]{1,60}$/;

function json(body, status) {
  return new Response(JSON.stringify(body), {
    status: status || 200,
    headers: { "Content-Type": "application/json" },
  });
}

async function readLists(db) {
  const yt = await db
    .prepare("SELECT handle FROM youtube_channels ORDER BY rowid")
    .all();
  const x = await db
    .prepare("SELECT handle FROM x_handles ORDER BY rowid")
    .all();
  return {
    youtube: (yt.results || []).map((r) => r.handle),
    x: (x.results || []).map((r) => r.handle),
  };
}

export async function onRequest(context) {
  const { request, env } = context;
  const db = env.FOLLOW_DB;
  if (!db) {
    return json({ error: "The follow-lists store is not tied to this site yet." }, 500);
  }
  try {
    if (request.method === "GET") {
      return json(await readLists(db));
    }
    if (request.method === "POST" || request.method === "DELETE") {
      const body = await request.json();
      const table = TABLES[body.list];
      const handle = String(body.handle || "").replace(/^@+/, "").trim();
      if (!table) {
        return json({ error: "That list name is not one of the two lists." }, 400);
      }
      if (!HANDLE_OK.test(handle)) {
        return json(
          { error: "A name can hold only letters, numbers, dots, dashes and underscores — no spaces." },
          400
        );
      }
      if (request.method === "POST") {
        const added = new Date().toISOString().slice(0, 10);
        await db
          .prepare("INSERT OR IGNORE INTO " + table + " (handle, added) VALUES (?, ?)")
          .bind(handle, added)
          .run();
      } else {
        await db
          .prepare("DELETE FROM " + table + " WHERE handle = ?")
          .bind(handle)
          .run();
      }
      return json(await readLists(db));
    }
    return json({ error: "That way of asking is not one this page answers." }, 405);
  } catch (err) {
    return json({ error: "The store could not be reached. Try again in a moment." }, 500);
  }
}
