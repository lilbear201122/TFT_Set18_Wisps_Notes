# 維護說明

## 資料管線（依序執行）

```
python scripts/1_extract_docx.py    # 讀 data/*.docx（使用者手寫筆記）-> data/wisps_from_docx.json, data/round_price.json
python scripts/2_match_en_zh.py     # 拿 data/metatft_scrape_raw.json 跟上一步結果做模糊比對 -> data/match_result.json
python scripts/3_merge_final.py     # 套用 2 的結果 + 手動校正表 -> data/wisps_final.json（最終資料源）
python scripts/4_build_site.py      # 讀 wisps_final.json + round_price.json -> ../index.html, data/wisps_data.js
```

`data/wisps_final.json` 是唯一真正被網站使用的資料檔；其餘都是產生它的中間產物。

## 更新 MetaTFT 資料（沒有寫成腳本 -- 需要瀏覽器）

MetaTFT 的 Wisps 表（https://www.metatft.com/tables/wisps）是 React 動態渲染的，沒有公開
API，必須在瀏覽器裡執行 JS 才能拿到完整資料。步驟：

1. 開啟 https://www.metatft.com/tables/wisps，點一下「Show Blossom upgrade」把升級效果也顯示出來。
2. 在 DevTools console 執行以下程式碼，把每一列的名稱／類別／階級／費用／回合／效果／升級／
   刷新條件都抓出來：

   ```js
   const rows = document.querySelectorAll('table tbody tr');
   const data = Array.from(rows).map(r => {
     const icon = r.querySelector('.WispIconCell img');
     const name = r.querySelector('.WispNameCell .WispName').textContent.trim();
     const category = r.querySelector('.WispNameCell .WispCategory').textContent.trim();
     const goldSpan = r.querySelector('.WispCostCell .NewSetWispGold');
     const cost = goldSpan ? goldSpan.textContent.replace(/\D/g,'') : '';
     const round = r.querySelector('.WispRoundCell .WispRoundBand').textContent.trim();
     const effectCell = r.querySelector('.WispEffectCell');
     const effectDivs = Array.from(effectCell.querySelectorAll(':scope > div'));
     let base = '', blossom = '', conditions = '';
     effectDivs.forEach(d => {
       if (d.classList.contains('NewSetWispUpgrade')) blossom = d.textContent.replace('Blossom upgrade:', '').trim();
       else if (d.classList.contains('WispConditions')) conditions = d.textContent.replace('Only appears if:', '').trim();
       else base = d.textContent.trim();
     });
     const tierMatch = icon.title.match(/Tier (\d)/);
     return {name, category, tier: tierMatch ? tierMatch[1] : '', iconSrc: icon.src, cost, round, base, blossom, conditions};
   });
   copy(JSON.stringify(data));  // 複製到剪貼簿
   ```

3. 把剪貼簿內容存成 `data/metatft_scrape_raw.json`（覆蓋舊檔）。
4. 圖示（category+tier icon，共最多 18 張，`t_shopcardsicon18_<category>_tier<N>.png`）從
   `iconSrc` 欄位下載，存進 `../assets/icons/`（把網址裡 `width=72` 換成 `width=200` 可拿到較
   高解析度版本）。若 metatft 新增了以前沒有的 category/tier 組合，記得補下載新圖。
5. 重新跑管線第 2～4 步。

## 已知的比對死角（matcher blind spots）

`2_match_en_zh.py` 是用 (類別, 回合, 費用) 當 key、效果文字裡的數字當消歧號來猜英中對應，
**同一個 (類別,回合,費用) 底下有兩個以上候選、且數字重疊度又低的時候，猜錯機率很高**。
第一次建置時人工抓出以下幾類必翻車：

- 同回合同費用、內容完全不同的技能（例如 `Blaze`／`Radiantize`／`Treetop Archers` 三個一組
  在 `烈炎`／`光芒萬丈`／`樹梢射手` 之間繞圈互換）。
- 消耗品家族（`Doodad`／`Knick-Knack`／`Thingamajig` × `Jar`／`Bag`／`Sack`，對應中文的
  雙防或生命／物攻或攻速／魔攻或魔力回復），共 9～10 個一組，光看數字幾乎沒有辨識度。
- 純粹「獲得指定道具」類的技能（數字很少或沒有數字，例如 `Phantom Armor`／`Preppers`）。

`3_merge_final.py` 裡的 `CLUSTER_EN_NAMES` / 明確 override 區塊就是針對這些死角寫的手動修正，
**每次 metatft 內容更新後都要重新核對這些 override 是否還正確**（尤其是新增/刪除同一
類別＋回合＋費用底下的技能時，配對可能會整組跑掉）。建議做法：跑完 2 之後，用
`data/match_report.txt` 看 unmatched 清單，並寫一個「數字集合完全對不上」的檢查（可參考
`3_merge_final.py` 開頭註解描述的邏輯）挑出可疑配對，人工核對 `data/metatft_scrape_raw.json`
與 `data/wisps_from_docx.json` 的原文再決定要不要修正 override。

## 個人筆記 vs 官方資料

- `has_personal_note = true`：中文備註來自使用者在 Word 檔裡手寫的拿取心得，效果文字/費用/
  回合已在合併時盡量改採 metatft 現行資料。
- `has_personal_note = false` 且 `official_zh_source = true`：DataTFT/舊筆記裡沒寫拿取心得，
  但名稱翻譯是有出處的官方／DataTFT 譯名。
- `official_zh_source = false`：metatft 上有、但舊資料集完全沒收錄的新內容（目前 6 個），
  中文是本專案臨時機翻，未經正式在地化確認，卡片上會標「新內容／機翻」。
