# -*- coding: utf-8 -*-
# Purpose: fuzzy-match metatft's English rows against the docx-derived Chinese rows by
# (category, round range, cost, effect numbers). Writes data/match_result.json + match_report.txt.
# WARNING: the fuzzy disambiguation is unreliable for same-cost/same-round clusters (see
# scripts/README.md "known matcher blind spots") -- 3_merge_final.py hardcodes manual overrides
# for every cluster we found broken. If you re-run this after a metatft content update, MANUALLY
# re-audit data/ambiguous_matches.txt / data/weak_matches.txt style output again before trusting it.
import json, os, re
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'data')

en = json.load(open(os.path.join(DATA, 'metatft_scrape_raw.json'), encoding='utf-8'))
zh = json.load(open(os.path.join(DATA, 'wisps_from_docx.json'), encoding='utf-8'))['wisps']

CAT_MAP = {'Champion':'英雄','Combat':'戰鬥','GoldXP':'金幣／經驗','Item':'道具','Misc':'雜項','Risky':'風險','Shop':'商店'}
TIER_MAP = {'1':'白銀','2':'黃金','3':'稜彩'}

def round_key(s):
    nums = re.findall(r'(\d+)-(\d+)', s)
    if not nums:
        return None
    def k(t):
        return int(t[0]) * 100 + int(t[1])
    return (k(nums[0]), k(nums[-1]))

def nums_in(s):
    return tuple(sorted(int(x) for x in re.findall(r'\d+', s)))

for w in en:
    w['category_zh'] = CAT_MAP[w['category']]
    w['rarity_zh'] = TIER_MAP.get(w['tier'], '')
    w['round_zh_style'] = w['round'].replace(' to ', ' ~ ')
    w['round_key'] = round_key(w['round'])
    w['num_sig'] = nums_in(w['base'] + ' ' + w['blossom'])

for w in zh:
    w['round_key'] = round_key(w['round_range'])
    eff_text = ' '.join(w['effects'])
    w['num_sig'] = nums_in(eff_text)

idx = defaultdict(list)
idx_no_cost = defaultdict(list)
for i, w in enumerate(zh):
    idx[(w['category'], w['round_key'], w['cost'])].append(i)
    idx_no_cost[(w['category'], w['round_key'])].append(i)

used_zh = set()
match_of = {}

def resolve(ei, ew, candidates, reason):
    if len(candidates) == 1:
        zi = candidates[0]
        used_zh.add(zi)
        match_of[ei] = (zi, reason)
    elif len(candidates) > 1:
        best = None
        for i in candidates:
            if zh[i]['num_sig'] == ew['num_sig']:
                best = i
                break
        if best is None:
            scored = sorted(candidates, key=lambda i: -len(set(zh[i]['num_sig']) & set(ew['num_sig'])))
            best = scored[0]
        used_zh.add(best)
        match_of[ei] = (best, reason + '+disambiguated')

# Pass 1: rows with an explicit cost value (including '0') -- anchor these first
for ei, ew in enumerate(en):
    if ew['cost'] == '':
        continue
    cost_zh = ew['cost'] if ew['cost'] != '0' else '—'
    key = (ew['category_zh'], ew['round_key'], cost_zh)
    candidates = [i for i in idx.get(key, []) if i not in used_zh]
    resolve(ei, ew, candidates, 'pass1-exact-cost')

# Pass 2: rows with blank cost on metatft -- fall back to category+round pool
for ei, ew in enumerate(en):
    if ew['cost'] != '' or ei in match_of:
        continue
    candidates = [i for i in idx_no_cost.get((ew['category_zh'], ew['round_key']), []) if i not in used_zh]
    resolve(ei, ew, candidates, 'pass2-no-cost-fallback')

matches = [(ei, match_of[ei][0] if ei in match_of else None, match_of[ei][1] if ei in match_of else 'no-candidate') for ei in range(len(en))]

matched = [m for m in matches if m[1] is not None]
unmatched_en = [en[m[0]] for m in matches if m[1] is None]
unmatched_zh = [zh[i] for i in range(len(zh)) if i not in used_zh]

lines = []
lines.append(f'EN total: {len(en)}, ZH total: {len(zh)}')
lines.append(f'Matched: {len(matched)}')
lines.append(f'Unmatched EN (need fresh zh translation): {len(unmatched_en)}')
for w in unmatched_en:
    cat = w['category']
    name = w['name']
    cost = w['cost']
    rnd = w['round']
    base = w['base']
    blossom = w['blossom']
    lines.append(f'  [{cat}] {name} | cost={cost} | {rnd} | {base} {blossom}')
lines.append('')
lines.append(f'Unmatched ZH (in old doc but not in metatft): {len(unmatched_zh)}')
for w in unmatched_zh:
    cat = w['category']
    name = w['name']
    cost = w['cost']
    rr = w['round_range']
    effects = w['effects']
    lines.append(f'  [{cat}] {name} | cost={cost} | {rr} | {effects}')

with open(os.path.join(DATA, 'match_report.txt'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

json.dump({'matches': matches}, open(os.path.join(DATA, 'match_result.json'), 'w', encoding='utf-8'))
print('done', len(matched), len(unmatched_en), len(unmatched_zh))
