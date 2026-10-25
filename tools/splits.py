# 元データでは1路線だが、実際は線路も停車駅も別の2系統に分かれている路線
# 元の路線コードは1つ目の系統に使い、2つ目には新しいコードを付ける
SPLITS = {
    "11320": [  # JR常磐線(上野～取手)
        ("11320", "JR常磐線(快速)",
         ["上野", "日暮里", "三河島", "南千住", "北千住", "松戸", "柏", "我孫子", "天王台", "取手"]),
        ("11320L", "JR常磐線(各駅停車)",
         ["北千住", "綾瀬", "亀有", "金町", "松戸", "北松戸", "馬橋", "新松戸", "北小金", "南柏", "柏", "北柏", "我孫子", "天王台", "取手"]),
    ],
}


def split_lines(lines):
    """路線コード→名前の表に、分けた系統を反映する"""
    for parts in SPLITS.values():
        for code, name, _ in parts:
            lines[code] = name
    return lines


def split_station_lines(station_name, line_codes):
    """駅が持つ路線コードの並びを、分けた系統に置き換える"""
    out = []
    for c in line_codes:
        if c in SPLITS:
            out += [code for code, _, stops in SPLITS[c] if station_name in stops and code not in out]
        elif c not in out:
            out.append(c)
    return out
