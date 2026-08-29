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

點右上角「✏️ 編輯模式」，每張卡片的備註會變成可編輯的文字框，邊打邊自動存在這個瀏覽器的
localStorage（暫存，換瀏覽器、清瀏覽器資料會不見）。

要把修改寫回專案本身：按「💾 存檔到 data/note_overrides.json」。

- **第一次按**：瀏覽器會跳出存檔視窗，導覽到專案的 `data` 資料夾，選到現有的
  `note_overrides.json` 直接覆蓋（沒有的話就在 `data` 資料夾內把檔名打成
  `note_overrides.json` 存新檔）。選過一次之後，瀏覽器會記住這個檔案位置。
- **之後再按**：不會再跳視窗，直接寫入同一個檔案。
- 這個功能只有 Chrome / Edge 這類 Chromium 瀏覽器支援（File System Access API），
  Firefox/Safari 不支援的話，改用旁邊的「下載備份」，把下載的檔案手動蓋掉
  `data/note_overrides.json`。

存檔之後，`data/note_overrides.json` 這個檔案本身就改好了 —— 跟 Claude 說一聲「update」，
它就會重新跑資料管線、`commit`、`push`，大家 `git pull` 就看得到最新備註。

「清除全部本機修改」會清掉這個瀏覽器裡還沒存檔/下載的修改，記得先存檔再清。

## 資料夾結構

- `index.html` — 主頁面
- `data/` — 神火資料（`wisps_final.json` 是唯一權威來源）與 MetaTFT 原始爬取資料
- `assets/` — 圖示與背景裝飾圖
- `scripts/` — 資料處理管線（重新抓 MetaTFT 資料、合併、產生網頁），細節見
  [scripts/README.md](scripts/README.md)

## 資料來源

效果文字以 [MetaTFT](https://www.metatft.com/tables/wisps) 現行資料為準；個人拿取心得備註
整理自使用者手寫筆記（原始比對自 [DataTFT](https://www.datatft.com/s18-database)）。
