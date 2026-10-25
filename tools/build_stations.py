import csv, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from splits import split_lines, split_station_lines
DB, OUT = sys.argv[1], sys.argv[2]
lines = {l['code']: l['name'] for l in csv.DictReader(open(f'{DB}/out/main/line.csv')) if l['closed'] == '0'}
st = {s['code']: s for s in csv.DictReader(open(f'{DB}/out/main/station.csv')) if s['closed'] == '0'}
groups = {}
for r in csv.DictReader(open(f'{DB}/out/main/register.csv')):
    s = st.get(r['station_code'])
    if not s or r['line_code'] not in lines: continue
    key = (s['name'], s['prefecture'])
    g = groups.setdefault(key, {"name": s['name'], "kana": s['name_kana'], "pref": int(s['prefecture']),
                                "lat": round(float(s['lat']), 4), "lng": round(float(s['lng']), 4), "lines": []})
    if r['line_code'] not in g['lines']: g['lines'].append(r['line_code'])
for g in groups.values():
    g['lines'] = split_station_lines(g['name'], g['lines'])
json.dump({"lines": split_lines(lines), "stations": list(groups.values())}, open(OUT, 'w'), ensure_ascii=False, separators=(',', ':'))
print(len(groups), "stations")
