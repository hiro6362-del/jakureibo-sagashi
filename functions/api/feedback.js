// アプリの「情報を送る」欄から届いた路線情報を保存する（Cloudflare Pages Functions + D1）
// 届いたものは毎日GitHubのIssueに移し、クロが確認してからデータに反映する
const MAX_PER_HOUR = 5;
const json = (body, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { "Content-Type": "application/json" } });
const clip = (s, n) => String(s ?? "").trim().slice(0, n);

async function hash(s) {
  const buf = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(s));
  return [...new Uint8Array(buf)].slice(0, 8).map(b => b.toString(16).padStart(2, "0")).join("");
}

export async function onRequestPost({ request, env }) {
  let body;
  try { body = await request.json(); } catch { return json({ error: "送信内容を読み取れませんでした" }, 400); }
  if (body.website) return json({ ok: true });   // 機械的な送信よけ（人には見えない欄）
  const message = clip(body.message, 1000);
  if (message.length < 2) return json({ error: "内容を書いてください" }, 400);

  const now = Date.now();
  const who = await hash((request.headers.get("CF-Connecting-IP") || "") + (env.SALT || "jakureibo"));
  const recent = await env.DB.prepare("SELECT COUNT(*) AS n FROM feedback WHERE ip_hash = ? AND created > ?")
    .bind(who, now - 3600e3).first();
  if (recent && recent.n >= MAX_PER_HOUR) return json({ error: "少し時間をおいてから送ってください" }, 429);

  await env.DB.prepare("INSERT INTO feedback (created, station, line, message, ip_hash) VALUES (?, ?, ?, ?, ?)")
    .bind(now, clip(body.station, 50), clip(body.line, 80), message, who).run();
  return json({ ok: true });
}
