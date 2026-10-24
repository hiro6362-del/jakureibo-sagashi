// 画面と駅・弱冷房車データを丸ごとキャッシュし、電波がなくても開けるようにする
// データを更新したら CACHE の番号を上げる
const CACHE = "jakureibo-v3";
const FILES = ["./", "index.html", "manifest.webmanifest", "icon.svg", "icon-192.png", "data/stations.json", "data/rules.json"];
self.addEventListener("install", e => e.waitUntil(caches.open(CACHE).then(c => c.addAll(FILES)).then(() => self.skipWaiting())));
self.addEventListener("activate", e => e.waitUntil(
  caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim())));
self.addEventListener("fetch", e => {
  const url = new URL(e.request.url);
  if (url.origin !== location.origin) return;
  // キャッシュを先に返し、裏でネットから新しいものを取っておく
  e.respondWith(caches.open(CACHE).then(async c => {
    const hit = await c.match(e.request, { ignoreSearch: true });
    const net = fetch(e.request).then(r => { if (r.ok) c.put(e.request, r.clone()); return r; }).catch(() => hit);
    return hit || net;
  }));
});
