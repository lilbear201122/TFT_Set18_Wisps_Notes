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
可出現回合篩選，也有搜尋框跟 MetaTFT 英文原文對照開關。

## 資料夾結構

- `index.html` — 主頁面
- `data/` — 神火資料（`wisps_final.json` 是唯一權威來源）與 MetaTFT 原始爬取資料
- `assets/` — 圖示與背景裝飾圖
- `scripts/` — 資料處理管線（重新抓 MetaTFT 資料、合併、產生網頁），細節見
  [scripts/README.md](scripts/README.md)

## 資料來源

效果文字以 [MetaTFT](https://www.metatft.com/tables/wisps) 現行資料為準；個人拿取心得備註
整理自使用者手寫筆記（原始比對自 [DataTFT](https://www.datatft.com/s18-database)）。
