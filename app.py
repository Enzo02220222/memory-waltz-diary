import streamlit as st
import google.generativeai as genai
import json
import os
from datetime import datetime
import pandas as pd

# --- 設定API ---
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

# 使用 cache 防止每次重整頁面都重新連線
@st.cache_resource
def get_model():
    genai.configure(api_key=GOOGLE_API_KEY)
    return genai.GenerativeModel('gemini-1.5-flash')
model = get_model()

# --- 檔案處理 (模擬資料庫) ---
DB_FILE = "diary_db.json"
        
def load_data():
    """讀取日記，如果檔案不存在，建立包含預設資料的檔案"""
    if not os.path.exists(DB_FILE):
        default_data = [
            {
                "summary": "連續讀了72小時資料結構，才搞懂bubble sort，很焦慮。",
                "tags": ["焦慮", "bubble sort"],
                "color": "#4B5365",
                "advice": "焦慮代表你在乎。試著一步一步搞懂吧。",
                "mood_score": 3,
                "date": "2025-12-03 14:00",
                "original_mood": "焦慮 😰"
            },
            {
                "summary": "跟好久不見的高中同學去吃鵝鴨村，餐點令我們相當驚艷。",
                "tags": ["開心", "鵝鴨村"],
                "color": "#FFD700",
                "advice": "這就是充電的時刻！記得這種快樂的感覺。",
                "mood_score": 9,
                "date": "2025-12-08 19:30",
                "original_mood": "開心 😄"
            },
            {
                "summary": "加油時被汽油濺了一身，隔壁大爺嚇到點一根菸壓壓驚。",
                "tags": ["驚嚇", "汽油"],
                "color": "#168616",
                "advice": "趕快清潔身體，並請勿在加油站抽菸。",
                "mood_score": 3, 
                "date": "2025-06-14 16:20",
                "original_mood": "焦慮 😰"
            }
        ]
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(default_data, f, ensure_ascii=False, indent=4)
        return default_data
        
    # 如果檔案存在，就正常讀取
    with open(DB_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except:
            return []

def save_data(new_entry):
    """儲存新的日記"""
    data = load_data()
    data.append(new_entry)
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# --- 頁面初始化 ---
st.set_page_config(page_title="Memory Waltz", page_icon="💃", layout="wide")

# --- 自訂 CSS 樣式 ---
st.markdown("""
    <style>
    /* google font */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@400;600&display=swap');

    .stApp {
        background-color: #FDFCF8;
        background-image: radial-gradient(#E6E0D4 1px, transparent 1px);
        background-size: 20px 20px;
    }

    html, body, [class*="css"] {
        font-family: 'Noto Serif TC', serif !important;
        color: #4A3B32;
    }
    
    h1, h2, h3 {
        color: #5D4037 !important;
        font-weight: 600;
    }

    .stButton > button {
        background-color: #F5F0E6;
        color: #5D4037;
        border: 1px solid #D7CCC8;
        border-radius: 15px;
        padding: 0.5em 1em;
        font-size: 18px;
        transition: all 0.3s ease;
        box-shadow: 2px 2px 5px rgba(93, 64, 55, 0.1);
        height: 3em;
        width: 100%;
    }

    .stButton > button:hover {
        background-color: #E6DCC3;
        border-color: #8D6E63;
        transform: translateY(-2px);
        box-shadow: 2px 4px 8px rgba(93, 64, 55, 0.15);
    }
    
    .stButton > button:active {
        background-color: #D7CCC8;
        transform: translateY(0px);
    }

    .stTextInput > div > div > input {
        background-color: #FFFFFF;
        border: 1px solid #D7CCC8;
        border-radius: 10px;
        color: #5D4037;
    }

    .memory-ball {
        width: 100px; 
        height: 100px; 
        border-radius: 50%;
        margin: 10px auto; 
        display: flex; 
        align-items: center; 
        justify-content: center;
        color: white; 
        font-weight: bold; 
        text-shadow: 1px 1px 3px rgba(0,0,0,0.3);
        box-shadow: inset -10px -10px 20px rgba(0,0,0,0.2), 5px 5px 15px rgba(0,0,0,0.1);
        border: 2px solid rgba(255,255,255,0.3);
    }
    
    .big-ball { 
        width: 160px; 
        height: 160px; 
        font-size: 1.5em;
        animation: float 6s ease-in-out infinite; 
    }

    @keyframes float { 
        0% { transform: translatey(0px); } 
        50% { transform: translatey(-15px); } 
        100% { transform: translatey(0px); } 
    }
    
    [data-testid="stSidebar"] {
        background-color: #F7F3E8;
        border-right: 1px solid #E0D6C8;
    }
    </style>
""", unsafe_allow_html=True)

# --- 核心邏輯 ---
if "step" not in st.session_state: st.session_state.step = "mood_selection"
if "history" not in st.session_state: st.session_state.history = []
if "current_mood" not in st.session_state: st.session_state.current_mood = ""

def start_chat(mood):
    st.session_state.current_mood = mood
    st.session_state.step = "chatting"
    initial_prompts = {
        "開心 😄": "太棒了！發生了什麼好事嗎？",
        "累 😴": "辛苦了。是課程太重還是有其他壓力？",
        "平靜 😌": "平靜很棒。今天有什麼微小的美好瞬間嗎？",
        "焦慮 😰": "別急。是期末專案還是人際關係讓你煩惱？",
        "難過 😢": "抱抱你。願意告訴我是什麼讓你難過嗎？"
    }
    st.session_state.history = [{"role": "model", "content": initial_prompts.get(mood, "今天感覺如何？")}]

def generate_memory_ball():
    with st.spinner("正在將回憶凝結成球..."):
        conversation_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.history])
        prompt = f"""
        分析這段日記對話：\n{conversation_text}\n
        請回傳純 JSON (無 markdown)，包含：
        1. "summary": 50字內摘要 (第一人稱)。
        2. "tags": 2-3個情緒標籤 list。
        3. "color": 代表心情的 HEX 顏色。
        4. "advice": 簡短建議。
        5. "mood_score": 1-10分 (1最負面, 10最正面)。
        """
        try:
            response = model.generate_content(prompt)
            clean_text = response.text.replace("```json", "").replace("```", "").strip()
            result = json.loads(clean_text)
            
            # 加上時間戳記並儲存
            result["date"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            result["original_mood"] = st.session_state.current_mood
            save_data(result) # 存入檔案
            
            st.session_state.diary_result = result
            st.session_state.step = "result"
            st.rerun()
        except Exception as e:
            st.error(f"生成失敗: {e}")

# --- 主程式架構 ---
st.sidebar.title("💃 Memory Waltz")
page = st.sidebar.radio("功能選單", ["📝 每日心情紀錄", "📊 回顧與週報"])

# === 頁面 1: 寫日記 ===
if page == "📝 每日心情紀錄":
    st.title("📝 每日心情紀錄")
    
    if st.session_state.step == "mood_selection":
        st.subheader("👋 嗨，今天心情還好嗎？")
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("開心 😄"): start_chat("開心 😄")
            if st.button("焦慮 😰"): start_chat("焦慮 😰")
        with c2:
            if st.button("平靜 😌"): start_chat("平靜 😌")
            if st.button("難過 😢"): start_chat("難過 😢")
        with c3:
            if st.button("累 😴"): start_chat("累 😴")

    elif st.session_state.step == "chatting":
        st.caption(f"目前心情：{st.session_state.current_mood}")
        for msg in st.session_state.history:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
        
        if prompt := st.chat_input("輸入內容..."):
            st.session_state.history.append({"role": "user", "content": prompt})
            chat = model.start_chat(history=[{"role": m["role"], "parts": m["content"]} for m in st.session_state.history[:-1]])
            response = chat.send_message(prompt)
            st.session_state.history.append({"role": "model", "content": response.text})
            st.rerun()

        if len(st.session_state.history) >= 4:
            st.divider()
            if st.button("✨ 結束並生成記憶球", type="primary"):
                generate_memory_ball()

    elif st.session_state.step == "result":
        res = st.session_state.diary_result
        st.balloons()
        st.markdown(f"""
            <div class="memory-ball big-ball" style="background-color: {res['color']};">
                <span style="font-size: 2em;">{res['original_mood'].split()[0]}</span>
            </div>
        """, unsafe_allow_html=True)
        st.success(f"**AI 建議：** {res['advice']}")
        st.info(f"**摘要：** {res['summary']}")
        if st.button("回到首頁"):
            st.session_state.step = "mood_selection"
            st.session_state.history = []
            st.rerun()

# === 頁面 2: 回顧與週報 ===
elif page == "📊 回顧與週報":
    st.title("📊 時光迴廊與週報")
    data = load_data()
    
    if not data:
        st.warning("目前還沒有日記紀錄喔！快去寫第一篇吧。")
    else:
        # 1. 記憶球展示牆
        st.subheader("你的記憶球收藏")
        cols = st.columns(4)
        for idx, entry in enumerate(reversed(data)): # 倒序顯示，最新的在前面
            with cols[idx % 4]:
                st.markdown(f"""
                    <div class="memory-ball" style="background-color: {entry['color']};" title="{entry['summary']}">
                        {entry['date'][5:10]}
                    </div>
                """, unsafe_allow_html=True)
                st.caption(entry['tags'][0])
        
        st.divider()

        # 2. 生成週報 (模擬 RAG 分析)
        st.subheader("📈 AI 心理分析週報")
        if st.button("✨ 生成本週深度洞察報告"):
            with st.spinner("AI 正在閱讀你的回憶並撰寫報告..."):
                # 將所有日記資料轉成文字給 AI 分析
                context = json.dumps(data, ensure_ascii=False)
                prompt = f"""
                你是專業的心理諮商師。這是使用者的日記數據：{context}
                請根據這些資料生成一份「心理健康週報」，包含：
                1. 心情分佈（文字描述主要情緒佔比）。
                2. 核心主題（本週最常出現的煩惱或快樂源頭）。
                3. 下週建議（具體可行的心理建設）。
                請用溫暖、專業的語氣撰寫，使用 Markdown 格式排版。
                """
                report = model.generate_content(prompt)
                st.markdown(report.text)
        
        # 3. 簡單的數據圖表
        if len(data) > 0:
            st.subheader("心情趨勢圖")
            df = pd.DataFrame(data)
            # 簡單把心情分數畫出來
            if "mood_score" in df.columns:
                st.line_chart(df["mood_score"])
            else:
                st.write("累積更多資料後將顯示趨勢圖。")

