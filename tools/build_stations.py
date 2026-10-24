import csv, json, sys
DB, OUT = sys.argv[1], sys.argv[2]
lines = {l['code']: l['name'] for l in csv.DictReader(open(f'{DB}/out/main/line.csv')) if l['closed'] == '0'}
st = {s['code']: s for s in csv.DictReader(open(f'{DB}/out/main/station.csv')) if s['closed'] == '0'}
groups = {}
for r in csv.DictReader(open(f'{DB}/out/main/register.csv')):
    s = st.get(r['station_code'])
    if not s or r['line_code'] not in lines: continue
    key = (s['name'], s['prefecture'])
    g = groups.setdefault(key, {"name": s['name'], "kana": s['name_kana'], "pref": int(s['prefecture']), "lines": []})
    if r['line_code'] not in g['lines']: g['lines'].append(r['line_code'])
json.dump({"lines": lines, "stations": list(groups.values())}, open(OUT, 'w'), ensure_ascii=False, separators=(',', ':'))
print(len(groups), "stations")
