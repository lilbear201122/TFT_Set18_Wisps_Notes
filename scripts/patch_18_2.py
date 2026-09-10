# -*- coding: utf-8 -*-
"""One-off manual patch: apply TFT patch 18.2's Wisp changes on top of wisps_final.json.
MetaTFT had not refreshed its Wisps table for this patch yet at the time this was written
(same cost values as before 18.2), so these numbers come directly from the official
zh-TW patch notes:
https://teamfighttactics.leagueoflegends.com/zh-tw/news/game-updates/teamfight-tactics-patch-18-2/

Does NOT touch data/note_overrides.json (personal notes) by design.
Re-run 4_build_site.py after this. If MetaTFT's own table catches up later and
scripts 1-3 get re-run from scratch, this patch becomes unnecessary (should be re-verified
against MetaTFT at that point rather than re-applied blindly).
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'data')
path = os.path.join(DATA, 'wisps_final.json')
wisps = json.load(open(path, encoding='utf-8'))
by_name = {w['name']: w for w in wisps}

# simple cost-only changes: zh name -> new cost
SIMPLE_COST = {
    '光盾': '3', '後排巨星': '1', '腰帶多多': '1', '傾盆大雨': '2', '施加痛苦': '4',
    '鐵木': '2', '大器晚成': '4', '閃電風暴': '3', '天降雷霆': '1', '團契': '3',
    '巨人靈氣': '3', '英靈之門': '2', '傭兵': '2', '鐵核心': '1', '殺戮狂熱': '2',
    '殺手的悔恨': '1', '魔力土壤': '2', '石化護盾': '1', '鬼魅徽章': '2', '復仇': '2',
    '孤寂斗篷': '2', '一夫當關': '2', '超級暴擊': '2', '樹梢射手': '3', '地動山搖': '3',
    '約德爾之魂': '2', '策略性損失': '4', '發薪日': '3', '慢速學習': '2', '一律五費': '8',
    '一律四費': '3', '閃光火焰': '1', '不倒翁': '3', '藥水製作': '2', '烈炎': '3',
    '光芒萬丈': '3',
}
for nm, cost in SIMPLE_COST.items():
    w = by_name.get(nm)
    if w is None:
        print(f'WARNING: {nm!r} not found (SIMPLE_COST)')
        continue
    w['cost'] = cost

# cost + one text substitution (dmg%/chance% etc.), applied to the first matching effect line only
COST_AND_SUB = {
    '爆發四散': ('3', '15%', '12%'),
    '竊賊': ('2', None, None),  # handled separately below (two 15%->20% substitutions)
}
w = by_name['爆發四散']
w['cost'] = '3'
w['effects'][0] = w['effects'][0].replace('15%', '12%', 1)

w = by_name['竊賊']
w['cost'] = '2'
w['effects'] = [e.replace('15%', '20%') for e in w['effects']]

# dual base/upgrade cost where the wisp already encodes the upgrade cost as "升級（N）："
w = by_name['開小號']
w['cost'] = '6'
w['effects'][1] = w['effects'][1].replace('升級（6）', '升級（5）')

# dual base/upgrade cost with NO separate upgrade line in the text -- show both numbers in
# the cost field itself since there's nowhere else to put the second value
DUAL_COST_NO_UPGRADE_LINE = {
    '邊境村莊': '3／2',
    '中路': '4／3',
    '搜索隊': '1／0',
    '起始城鎮': '2／1',
}
for nm, cost in DUAL_COST_NO_UPGRADE_LINE.items():
    by_name[nm]['cost'] = cost

# Potted Lifebloom / Potted Stonebark: official zh-TW names revealed by this patch note
# (differ from our earlier machine-translated placeholder names) + new dual cost
w = by_name['盆栽生命花']
w['name'] = '生命花盆栽'
w['cost'] = '1／0'
by_name['生命花盆栽'] = w
w = by_name['盆栽石紋樹']
w['name'] = '石皮樹盆栽'
w['cost'] = '1／0'
by_name['石皮樹盆栽'] = w

# Borrowed Gear: effect wording changed (now triggers at combat start), no cost change
w = by_name['借來的裝備']
w['effects'][0] = '戰鬥開始時，' + w['effects'][0]
w['effects'][1] = '戰鬥開始時，' + w['effects'][1]

# Field of Mice removed entirely from the game in 18.2
wisps = [w for w in wisps if w['name'] != '老鼠之地']

with open(path, 'w', encoding='utf-8') as f:
    json.dump(wisps, f, ensure_ascii=False, indent=1)

print('patched', len(SIMPLE_COST) + 2 + 1 + len(DUAL_COST_NO_UPGRADE_LINE) + 2 + 1, 'wisps, removed 1 (老鼠之地), total now', len(wisps))
