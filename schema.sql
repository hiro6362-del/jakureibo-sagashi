-- アプリから届いた路線情報（exported=1 はGitHubのIssueに移し済み）
CREATE TABLE IF NOT EXISTS feedback (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created INTEGER NOT NULL,
  station TEXT,
  line TEXT,
  message TEXT NOT NULL,
  ip_hash TEXT,
  exported INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS feedback_ip ON feedback (ip_hash, created);
