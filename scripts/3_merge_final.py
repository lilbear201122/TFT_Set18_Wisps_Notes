# -*- coding: utf-8 -*-
# Purpose: apply 2_match_en_zh.py's fuzzy matches PLUS a hand-verified override table (see
# scripts/README.md) on top, then write data/wisps_final.json -- the single source of truth
# 4_build_site.py reads from. If metatft's content changes, re-run 1+2, then re-audit every
# override below still points at the right pair before trusting this output.
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'data')

en = json.load(open(os.path.join(DATA, 'metatft_scrape_raw.json'), encoding='utf-8'))
zh = json.load(open(os.path.join(DATA, 'wisps_from_docx.json'), encoding='utf-8'))['wisps']
match_data = json.load(open(os.path.join(DATA, 'match_result.json'), encoding='utf-8'))['matches']

# name -> index lookups
en_by_name = {w['name']: i for i, w in enumerate(en)}
zh_by_name_idx = {w['name']: i for i, w in enumerate(zh)}

match_of_ei = {ei: zi for ei, zi, reason in match_data if zi is not None}

# --- manual corrections to the automated match (verified by content, see match audit) ---
# name collisions (same zh name used twice) are resolved by explicit index, not name lookup
# clear every zh slot this cluster of English names currently (possibly wrongly) claims,
# so re-assignment below starts from a clean slate for this whole group
CLUSTER_EN_NAMES = [
    'Flow', "Snacktime!", 'Regeneration', 'Solar Gift', 'Journeyman',
    'Mana-Rich Soil', "Solitude's Cloak", 'Blaze', 'Radiantize', 'Treetop Archers',
    'Scrappy', 'Training Yard', 'Early Fix', 'Doodad Jar', 'Potioncraft',
    'Doodad Bag', 'Knick-Knack Bag', 'Thingamajig Bag',
    'Doodad Sack', 'Knick-Knack Sack', 'Thingamajig Sack',
    'Knick-Knack Jar', 'Thingamajig Jar',
    'Phantom Armor', 'Preppers',
]
for nm in CLUSTER_EN_NAMES:
    ei = en_by_name[nm]
    if ei in match_of_ei:
        del match_of_ei[ei]

# the two '雜物罐' rows (2-1~2-7) are only distinguishable by their effect text
zh_juwuguan_armor = next(i for i, w in enumerate(zh) if w['name'] == '雜物罐' and '雙防' in w['effects'][0])
zh_juwuguan_ap = next(i for i, w in enumerate(zh) if w['name'] == '雜物罐' and '魔攻' in w['effects'][0])

match_of_ei[en_by_name['Flow']] = zh_by_name_idx['風湧']
match_of_ei[en_by_name['Regeneration']] = zh_by_name_idx['回復']
match_of_ei[en_by_name['Solar Gift']] = zh_by_name_idx['日輝之禮']
match_of_ei[en_by_name['Journeyman']] = zh_by_name_idx['旅行者']
match_of_ei[en_by_name["Mana-Rich Soil"]] = zh_by_name_idx['魔力土壤']
match_of_ei[en_by_name["Solitude's Cloak"]] = zh_by_name_idx['孤寂斗篷']
match_of_ei[en_by_name['Blaze']] = zh_by_name_idx['烈炎']
match_of_ei[en_by_name['Radiantize']] = zh_by_name_idx['光芒萬丈']
match_of_ei[en_by_name['Treetop Archers']] = zh_by_name_idx['樹梢射手']
match_of_ei[en_by_name['Scrappy']] = zh_by_name_idx['鬥志旺盛']
match_of_ei[en_by_name['Training Yard']] = zh_by_name_idx['訓練場']
match_of_ei[en_by_name['Early Fix']] = zh_by_name_idx['提前修復']
match_of_ei[en_by_name['Potioncraft']] = zh_by_name_idx['藥水製作']
match_of_ei[en_by_name['Doodad Jar']] = zh_juwuguan_armor
match_of_ei[en_by_name['Thingamajig Jar']] = zh_juwuguan_ap
match_of_ei[en_by_name['Knick-Knack Jar']] = zh_by_name_idx['小玩意罐']
match_of_ei[en_by_name['Doodad Bag']] = zh_by_name_idx['雜物包']
match_of_ei[en_by_name['Knick-Knack Bag']] = zh_by_name_idx['小玩意包']
match_of_ei[en_by_name['Thingamajig Bag']] = zh_by_name_idx['雜物袋']
match_of_ei[en_by_name['Doodad Sack']] = zh_by_name_idx['雜物麻袋']
match_of_ei[en_by_name['Knick-Knack Sack']] = zh_by_name_idx['小玩意布袋']
match_of_ei[en_by_name['Thingamajig Sack']] = zh_by_name_idx['雜物布袋']
match_of_ei[en_by_name['Phantom Armor']] = zh_by_name_idx['鬼魅護甲']
match_of_ei[en_by_name['Preppers']] = zh_by_name_idx['準備者']
# Snacktime! genuinely has no old-dataset counterpart -- leave unmatched -> fresh translation
match_of_ei.pop(en_by_name["Snacktime!"], None)

# --- consistency check: no zh index used twice, print any leftover collisions ---
from collections import Counter
zi_counts = Counter(match_of_ei.values())
dupes = {zi: c for zi, c in zi_counts.items() if c > 1}
if dupes:
    lines = ['DUPLICATE ZH ASSIGNMENTS FOUND:']
    for zi, c in dupes.items():
        claimers = [en[ei]['name'] for ei, z in match_of_ei.items() if z == zi]
        lines.append(f'  zh[{zi}]={zh[zi]["name"]!r} claimed by {claimers}')
    open(os.path.join(DATA, 'consistency_errors.txt'), 'w', encoding='utf-8').write('\n'.join(lines))
else:
    open(os.path.join(DATA, 'consistency_errors.txt'), 'w', encoding='utf-8').write('OK: no duplicate zh assignments\n')

# --- hand-translated entries for wisps with no counterpart in the old dataset ---
FRESH_ZH = {
    'Potted Lifebloom': {
        'name': '盆栽生命花',
        'base': '獲得1個暫時的生命綻花。',
        'blossom': '',
        'conditions': '古木羈絆啟動',
    },
    'Potted Stonebark': {
        'name': '盆栽石紋樹',
        'base': '獲得1個暫時的石紋樹。',
        'blossom': '',
        'conditions': '古木羈絆啟動',
    },
    "Bear's Visit": {
        'name': '熊靈來訪',
        'base': '本場戰鬥獲得熊之原始增益。',
        'blossom': '',
        'conditions': '原始羈絆啟動',
    },
    "Tiger's Visit": {
        'name': '虎靈來訪',
        'base': '本場戰鬥獲得虎之原始增益。',
        'blossom': '',
        'conditions': '原始羈絆啟動',
    },
    "Turtle's Visit": {
        'name': '龜靈來訪',
        'base': '本場戰鬥獲得龜之原始增益。',
        'blossom': '',
        'conditions': '原始羈絆啟動',
    },
    'Snacktime!': {
        'name': '點心時間！',
        'base': '「BFF」會吞噬受其傷害且生命低於15%的敵軍。',
        'blossom': '「BFF」會吞噬受其傷害且生命低於20%的敵軍。',
        'conditions': 'Sprykin 羈絆啟動',
    },
}

CAT_MAP = {'Champion': '英雄', 'Combat': '戰鬥', 'GoldXP': '金幣／經驗', 'Item': '道具', 'Misc': '雜項', 'Risky': '風險', 'Shop': '商店'}
CAT_MAP_DISPLAY_EN = {'Champion': 'Champion', 'Combat': 'Combat', 'GoldXP': 'GoldXP', 'Item': 'Item', 'Misc': 'Misc', 'Risky': 'Risky', 'Shop': 'Shop'}
TIER_MAP = {'1': '白銀', '2': '黃金', '3': '稜彩'}

final = []
for ei, ew in enumerate(en):
    zi = match_of_ei.get(ei)
    icon_tier = ew['tier']
    icon_cat = ew['category'].lower()
    icon_file = f"t_shopcardsicon18_{icon_cat}_tier{icon_tier}.png"

    round_zh = ew['round'].replace(' to ', ' ~ ').replace(', ', '；')

    if zi is not None:
        zw = zh[zi]
        name_zh = zw['name']
        cost = ew['cost'] if ew['cost'] not in ('', None) else zw['cost']
        effects_zh = list(zw['effects'])
        notes_zh = list(zw['notes'])
        has_personal_note = zw['has_personal_note']
        official_zh = True
    else:
        fresh = FRESH_ZH[ew['name']]
        name_zh = fresh['name']
        cost = ew['cost'] if ew['cost'] not in ('', None) else '—'
        effects_zh = [fresh['base']]
        if fresh['blossom']:
            effects_zh.append('升級：' + fresh['blossom'])
        notes_zh = []
        if fresh['conditions']:
            notes_zh.append('【刷新條件】' + fresh['conditions'])
        has_personal_note = False
        official_zh = False

    final.append({
        'name': name_zh,
        'name_en': ew['name'],
        'category': CAT_MAP[ew['category']],
        'category_en': ew['category'],
        'rarity': TIER_MAP.get(ew['tier'], ''),
        'cost': cost if cost else '—',
        'round_range': round_zh,
        'round_range_en': ew['round'],
        'effects': effects_zh,
        'notes': notes_zh,
        'has_personal_note': has_personal_note,
        'official_zh_source': official_zh,
        'icon': icon_file,
        'effect_en_base': ew['base'],
        'effect_en_blossom': ew['blossom'],
        'conditions_en': ew['conditions'],
    })

out_path = os.path.join(DATA, 'wisps_final.json')
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(final, f, ensure_ascii=False, indent=1)

print('total', len(final))
print('official_zh_source True:', sum(1 for w in final if w['official_zh_source']))
print('official_zh_source False (fresh translation):', sum(1 for w in final if not w['official_zh_source']))
print('has_personal_note True:', sum(1 for w in final if w['has_personal_note']))
