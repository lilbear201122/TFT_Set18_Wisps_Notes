# TFT Set 18 神火（Wisps）筆記

TFT Set 18 神火機制的完整可篩選筆記工具，純本地 HTML，不需要架站或安裝任何東西。

## 使用方式

Clone 下來之後，直接雙擊開啟 [index.html](index.html)（用瀏覽器開，Chrome/Edge 都可以）。

```bash
git clone <這個 repo 的網址>
cd TFT_Set18_神火筆記
# 直接用瀏覽器打開 index.html
```

裡面可以依階級（白銀／黃金／稜彩）、類別（英雄／戰鬥／金幣經驗／道具／雜項／風險／商店）、
可出現回合篩選，也有搜尋框跟 MetaTFT 英文原文對照開關。篩選面板會固定在畫面上方，往下捲動瀏覽
卡片時不會消失。

## 編輯備註

點右上角「✏️ 編輯模式」，每張卡片的備註會變成可編輯的文字框，修改會**即時存在目前這個瀏覽器
的 localStorage**（換瀏覽器、換電腦、清瀏覽器資料都不會帶過去）。要讓修改變成永久、大家都看
得到的版本：

1. 編輯完之後點「下載 note_overrides.json」，瀏覽器會存一份 JSON 檔。
2. 把下載下來的檔案內容併入 [data/note_overrides.json](data/note_overrides.json)（同一個
   `name_en` 的 key 會覆蓋掉舊的），或是直接把整份內容貼給 Claude 幫你處理。
3. 跑 `python scripts/3_merge_final.py && python scripts/4_build_site.py` 重新產生
   `index.html`，`git commit` + `git push` 分享給大家。

「清除全部本機修改」會清掉這個瀏覽器裡還沒下載備份的修改，記得先下載再清。

## 資料夾結構

- `index.html` — 主頁面
- `data/` — 神火資料（`wisps_final.json` 是唯一權威來源）與 MetaTFT 原始爬取資料
- `assets/` — 圖示與背景裝飾圖
- `scripts/` — 資料處理管線（重新抓 MetaTFT 資料、合併、產生網頁），細節見
  [scripts/README.md](scripts/README.md)

## 資料來源

效果文字以 [MetaTFT](https://www.metatft.com/tables/wisps) 現行資料為準；個人拿取心得備註
整理自使用者手寫筆記（原始比對自 [DataTFT](https://www.datatft.com/s18-database)）。
