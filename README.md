# Memory Waltz: The Ball Diary

結合生成式 AI 的互動式心情日記，透過 AI 引導與視覺化，將你的情緒轉化為專屬的「記憶球」。

## 專案功能

這個專案包含三大核心功能：

### 1. AI 引導式記錄
* **心理諮商師角色**：系統內建 Gemini 模型，扮演溫暖的傾聽者。
* **漸進式追問**：不只是單純的問答，AI 會根據你選擇的初始心情（如：焦慮、開心），主動追問事件的細節（人、事、物），引導你完整表達感受。

### 2. 情緒記憶球
* **視覺化轉譯**：對話結束後，AI 會自動分析內容，生成一篇**日記摘要**與**情緒標籤**。
* **色彩映射**：根據分析出的情緒正負向與強度，即時渲染出一顆對應顏色的「記憶球」（例如：金黃色代表開心、深灰藍代表焦慮）。

### 3. 週報回顧
* **RAG 深度分析**：系統能讀取過去累積的日記資料。
* **AI 洞察報告**：一鍵生成週報，包含心情趨勢分佈、核心壓力/快樂源分析，以及 AI 給予的心理建設建議。

---

## 📖 如何使用

你可以選擇直接線上體驗，或是在本地端執行程式碼。

### 方式一：線上體驗
直接點擊下方連結，即可進入 App 使用：
🔗 **[點擊這裡開啟 Memory Waltz](https://memory-waltz-diary-2ykwyntibxypw7dee893xh.streamlit.app/)**

**操作步驟：**
1.  **選擇心情**：在首頁點擊符合你當下感受的按鈕。
2.  **與 AI 對話**：回答 AI 的追問，盡情抒發你的想法。
3.  **生成記憶球**：當對話足夠時，點擊「✨ 結束對話並生成記憶球」。
4.  **查看週報**：點擊左側選單的「📊 回顧與週報」，查看歷史紀錄與 AI 分析報告。

### 方式二：本地端執行

如果你想在自己的電腦上運行：

**1. 下載專案**
```bash
git clone [https://github.com/你的帳號/memory-waltz-diary.git](https://github.com/你的帳號/memory-waltz-diary.git)
cd memory-waltz-diary
```
**2. 安裝必要套件**
```bash
pip install -r requirements.txt
```
**3. 設定 API Key 請將你的 Google Gemini API Key 設定在程式中（建議使用 .streamlit/secrets.toml）：**
```bash
Ini, TOML
# .streamlit/secrets.toml
GOOGLE_API_KEY = "你的_GOOGLE_API_KEY"
```
4. 啟動程式
```bash
streamlit run app.py
```
