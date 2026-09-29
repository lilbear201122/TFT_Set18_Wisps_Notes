# -*- coding: utf-8 -*-
"""One-off manual patch: apply TFT patch 18.2B / 18.3 / 18.3B Wisp changes on top of
wisps_final.json (run after patch_18_2.py has already been applied).

Sources:
- official zh-TW 18.3 notes:
  https://teamfighttactics.leagueoflegends.com/zh-tw/news/game-updates/teamfight-tactics-patch-18-3/
- HackMD compilation (18.2B / 18.3B hotfix notes): https://hackmd.io/@hathena/HyqLGXSrGl

18.3B itself has no Wisp changes (targeting revert + disabled augments only).
The 18.3 "盛放繁花" section lists Blossom-UPGRADED values; the "神火" section lists base values.

Note: 18.2 notes said Combust base 15% -> 12%, but 18.3 notes say base 18% -> 15%.
We follow the newer 18.3 notes (base 15%).

Does NOT touch data/note_overrides.json (personal notes) by design.
Re-run 4_build_site.py after this.
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'data')
path = os.path.join(DATA, 'wisps_final.json')
wisps = json.load(open(path, encoding='utf-8'))
by_name = {w['name']: w for w in wisps}


def sub(w, idx, old, new):
    """Replace old->new in effects[idx]; fail loudly if the old text isn't there."""
    assert old in w['effects'][idx], (w['name'], idx, old, w['effects'][idx])
    w['effects'][idx] = w['effects'][idx].replace(old, new, 1)


def sub_en(w, field, old, new):
    assert old in w[field], (w['name'], field, old, w[field])
    w[field] = w[field].replace(old, new, 1)


# ---- 18.2B: Polymorph wisps only appear in the first wisp shop of each planning phase ----
POLY_NOTE = '（僅會出現在每個準備階段的第一個神火商店）'
for nm in ('稍稍變形', '變形', '大幅變形'):
    w = by_name[nm]
    if POLY_NOTE not in w['effects'][0]:
        w['effects'][0] += POLY_NOTE

# ---- 18.3 base values (神火 section) ----
by_name['鮮血和鋼鐵']['cost'] = '4'
by_name['三個我']['cost'] = '10'

w = by_name['爆發四散']
sub(w, 0, '12%', '15%')          # base: 18% -> 15% (see docstring about the 18.2 discrepancy)
sub(w, 1, '22%', '18%')          # blossom: 22% -> 18%

w = by_name['魔力土壤']
w['effects'][0] = '我方法師最大魔力降低15%。'
w['effects'][1] = '升級：我方法師最大魔力降低20%。'
sub_en(w, 'effect_en_base', '18%', '15%')
sub_en(w, 'effect_en_blossom', '25%', '20%')

# ---- 18.3 Blossom-upgraded values (盛放繁花 section) ----
w = by_name['動態商店']
sub(w, 1, '26秒', '24秒'); sub_en(w, 'effect_en_blossom', '26 seconds', '24 seconds')

w = by_name['烈炎']
sub(w, 1, '更多真實傷害', '更多真實傷害（1.25%最大生命）')

w = by_name['血汗錢']
sub(w, 1, '升級（1）', '升級（2）')

w = by_name['珍品購物車']
sub(w, 1, '獲得2金錢', '獲得1金錢'); sub_en(w, 'effect_en_blossom', 'Gain 2 Gold', 'Gain 1 Gold')

w = by_name['激烈對決']
sub(w, 1, '7次', '5次'); sub_en(w, 'effect_en_blossom', '7 takedowns', '5 takedowns')

w = by_name['英勇犧牲']
line = '升級：英雄之力提供35%物攻／魔攻與35物防／魔防。'
if len(w['effects']) == 1:
    w['effects'].append(line)

w = by_name['變大吧']
sub(w, 1, '600', '500'); sub_en(w, 'effect_en_blossom', '600', '500')

w = by_name['傭兵部隊']
sub(w, 1, '4.5%', '4%'); sub_en(w, 'effect_en_blossom', '4.5%', '4%')

w = by_name['月光儀式']
sub(w, 1, '升級：', '升級（3）：')

w = by_name['邪惡交易']
w['effects'][1] = '升級：失去2玩家生命。獲得2金錢。'
w['effect_en_blossom'] = 'Lose 2 Player Health. Gain 2 Gold.'

w = by_name['一夫當關']
sub(w, 1, '22%生命和22%', '20%生命和20%'); sub_en(w, 'effect_en_blossom', '22% Health and 22%', '20% Health and 20%')

# ---- 18.3 consumable stat boosters (numbers aren't in any wisp text, so just annotate) ----
CONSUMABLE_NOTE = {
    '雙防或生命': '（18.3：雙防消耗品 10 ⇒ 8）',
    '物攻或攻速': '（18.3：攻速消耗品 8% ⇒ 6%）',
}
for w in wisps:
    if not any(k in w['name_en'] for k in ('Doodad', 'Knick-Knack', 'Thingamajig')):
        continue
    for key, note in CONSUMABLE_NOTE.items():
        if key in w['effects'][0] and note not in w['effects'][0]:
            w['effects'][0] += note

with open(path, 'w', encoding='utf-8') as f:
    json.dump(wisps, f, ensure_ascii=False, indent=1)

print('patched 18.2B/18.3 wisp changes, total wisps', len(wisps))
