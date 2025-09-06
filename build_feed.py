# build_feed.py
from datetime import datetime, date, time, timedelta
from zoneinfo import ZoneInfo
from pathlib import Path
import html

SRC = Path("cytaty.txt")
DST = Path("index.xml")

BASE_LINK = "https://pilara87.github.io/cytaty-rss/"   # Twój GitHub Pages URL
CHANNEL_TITLE = "Metro cytaty"
CHANNEL_DESC = "Lekki, zabawny cytat na start dnia."
LANG = "pl-PL"
TTL_MIN = 1440

# Którego dnia zaczynamy (pierwszy cytat)? Dopasuj według uznania:
START_DATE = date(2025, 9, 6)

TZ = ZoneInfo("Europe/Warsaw")

def rfc822(dt: datetime) -> str:
    return dt.strftime("%a, %d %b %Y %H:%M:%S %z")

quotes = [ln.strip() for ln in SRC.read_text(encoding="utf-8").splitlines() if ln.strip()]
if not quotes:
    raise SystemExit("Brak cytatów w cytaty.txt")

today = datetime.now(TZ).date()
idx = (today - START_DATE).days % len(quotes)
quote = quotes[idx]
num = idx + 1

now = datetime.now(TZ)
pub = datetime.combine(today, time(0, 5), TZ)  # 00:05 czasu PL każdego dnia
link = f"{BASE_LINK}#{num}"

# Bezpieczne CDATA (na wypadek ']]>' w tekście)
safe_cdata = quote.replace("]]>", "]]]]><![CDATA[>")

parts = []
parts.append('<?xml version="1.0" encoding="UTF-8"?>')
parts.append('<rss version="2.0">')
parts.append('  <channel>')
parts.append(f'    <title>{html.escape(CHANNEL_TITLE)}</title>')
parts.append(f'    <link>{html.escape(BASE_LINK)}</link>')
parts.append(f'    <description>{html.escape(CHANNEL_DESC)}</description>')
parts.append(f'    <language>{LANG}</language>')
parts.append(f'    <lastBuildDate>{rfc822(now)}</lastBuildDate>')
parts.append(f'    <ttl>{TTL_MIN}</ttl>')
parts.append('    <item>')
parts.append(f'      <title>Cytat #{num}</title>')
parts.append(f'      <link>{html.escape(link)}</link>')
parts.append(f'      <guid>{html.escape(link)}</guid>')
parts.append(f'      <pubDate>{rfc822(pub)}</pubDate>')
parts.append(f'      <description><![CDATA[{safe_cdata}]]></description>')
parts.append('    </item>')
parts.append('  </channel>')
parts.append('</rss>')

DST.write_text("\n".join(parts), encoding="utf-8")
print(f"Zbudowano {DST} z cytatem #{num}")
