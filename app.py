'''import streamlit as st
from datetime import datetime, timezone, timedelta
import time
import base64

def load_audio_base64(audio_path):
    with open(audio_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# -------------------------------
# BACKGROUND MUSIC
# -------------------------------
audio_base64 = load_audio_base64("assets/audio/Haseen.mp3")

st.markdown(
    f"""
    <style>
    .romantic-audio {{
        position: fixed;
        bottom: 24px;
        right: 24px;
        background: rgba(255, 182, 193, 0.18);
        backdrop-filter: blur(12px);
        border-radius: 999px;
        padding: 10px 14px;
        box-shadow: 0 8px 25px rgba(255, 105, 135, 0.35);
        z-index: 9999;
    }}

    .romantic-audio audio {{
        width: 210px;
        opacity: 0.75;
        filter: drop-shadow(0 0 6px rgba(255, 182, 193, 0.6));
    }}

    .romantic-audio audio::-webkit-media-controls-panel {{
        background: transparent;
    }}
    </style>

    <div class="romantic-audio">
        <audio autoplay loop controls>
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
        </audio>
    </div>
    """,
    unsafe_allow_html=True
)

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="Janamdin ",
    page_icon="🤗",
    layout="centered"
)

# -------------------------------
# CONFIG (EDIT THESE)
# -------------------------------
FRIEND_NAME = "Shradddhhaaa"

BIRTHDAY_DATETIME = datetime(
    2026, 1, 4, 16, 32, 0,
    tzinfo=timezone(timedelta(hours=5, minutes=30))
)

# -------------------------------
# STYLING
# -------------------------------
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    }

    .card {
        background: rgba(255, 255, 255, 0.92);
        padding: 45px 35px;
        border-radius: 25px;
        text-align: center;
        box-shadow: 0px 20px 45px rgba(0,0,0,0.25);
        max-width: 600px;
        margin: 60px auto;
    }

    .title {
        font-size: 34px;
        font-weight: 800;
        margin-bottom: 15px;
        color: black;
        
    }

    .timer {
        font-size: 40px;
        font-weight: 700;
        letter-spacing: 2px;
        margin: 20px 0;
        color: black;
    }

    .subtitle {
        font-size: 17px;
        color: black;
        margin-top: 10px;
    }

    .header {
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        margin-top: 30px;
        margin-bottom: 10px;
        color: white;
    }

    .footer {
        text-align: center;
        color: #aaa;
        margin-top: 20px;
        font-size: 14px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------------
# HEADER
# -------------------------------
st.markdown(
    f"<div class='header'>{FRIEND_NAME}'s Birthday 🍡🍡</div>",
    unsafe_allow_html=True
)

# -------------------------------
# COUNTDOWN LOGIC
# -------------------------------
now = datetime.now(timezone(timedelta(hours=5, minutes=30)))
time_remaining = BIRTHDAY_DATETIME - now

# -------------------------------
# MAIN CARD (EVERYTHING INSIDE)
# -------------------------------
if time_remaining.total_seconds() > 0:
    days = time_remaining.days
    hours, remainder = divmod(time_remaining.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    st.markdown(
        f"""
        <div class="card">
            <div class="title">COUNT DOWNNN 🐽</div>
            <div class="timer">
                {days}d : {hours}h : {minutes}m : {seconds}s
            </div>
            <div class="subtitle">
                din aa raha hain bada khaas , aapka birthday jo hain aas paas 😋😝
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    time.sleep(1)
    st.rerun()

else:
    st.markdown(
        f"""
        <div class="card">
            <div class="title">HAPPY BIRTHDAY {FRIEND_NAME} big dawgggggggg!</div>
            <div class="subtitle">
                It's your day bbg , have a blastttt and loadssss of funnnnn!!!!!!!💕
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# -------------------------------
# FOOTER
# -------------------------------
st.markdown(
    "<div class='footer'>Made with ❤️ just for you</div>",
    unsafe_allow_html=True
)'''

import streamlit as st
from datetime import datetime, timezone, timedelta
import time
import base64
if "birthday_unlocked" not in st.session_state:
    st.session_state["birthday_unlocked"] = False

# -------------------------------
# PAGE CONFIG (Must be first)
# -------------------------------
st.set_page_config(
    page_title="Janamdin Shradddhhaaa ✨",
    page_icon="🌸",
    layout="centered"
)

def load_audio_base64(audio_path):
    try:
        with open(audio_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return None

# -------------------------------
# CONFIG
# -------------------------------
FRIEND_NAME = "Shradddhhaaa"
# Set to your desired date
BIRTHDAY_DATETIME = datetime(
    2026, 1, 5, 0, 0, 0,
    tzinfo=timezone(timedelta(hours=5, minutes=30))
)

# -------------------------------
# BACKGROUND MUSIC (Floating Romantic Player)
# -------------------------------
audio_data = load_audio_base64("assets/audio/Haseen.mp3")

if audio_data:
    st.markdown(
        f"""
        <div class="romantic-audio">
            <p style="margin:0; font-size: 12px; color: #ff4d6d; font-weight: bold; text-align: center;">🎵 Haseen</p>
            <audio autoplay loop controls>
                <source src="data:audio/mp3;base64,{audio_data}" type="audio/mp3">
            </audio>
        </div>
        <style>
        .romantic-audio {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: rgba(255, 255, 255, 0.7);
            backdrop-filter: blur(10px);
            border: 2px solid #ffccd5;
            border-radius: 30px;
            padding: 10px;
            z-index: 9999;
            box-shadow: 0 10px 25px rgba(255, 77, 109, 0.2);
        }}
        audio {{ height: 30px; width: 200px; }}
        </style>
        """,
        unsafe_allow_html=True
    )

# -------------------------------
# ROMANTIC STYLING
# -------------------------------
st.markdown(
    """
    <style>
    /* Gradient Background */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #ffafbd 0%, #ffc3a0 100%);
    }

    /* Card Styling */
    .card {
        background: rgba(255, 255, 255, 0.85);
        padding: 50px 40px;
        border-radius: 40px;
        text-align: center;
        border: 4px solid #ffffff;
        box-shadow: 0px 20px 60px rgba(255, 77, 109, 0.15);
        max-width: 600px;
        margin: 40px auto;
    }

    .header-text {
        font-family: 'Parisienne', cursive, sans-serif;
        color: white;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        font-size: 45px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 0px;
    }

    .title {
        font-size: 30px;
        font-family: 'Parisienne', cursive, sans-serif;
        color: #ff4d6d;
        margin-bottom: 10px;
    }

    .timer {
        font-size: 45px;
        font-weight: 800;
        color: #c9184a;
        font-family: 'Courier New', Courier, monospace;
        background: #fff0f3;
        padding: 15px;
        border-radius: 20px;
        display: inline-block;
        margin: 20px 0;
    }

    .subtitle {
        font-size: 19px;
        color: #594e52;
        line-height: 1.5;
        font-style: italic;
    }

    .footer {
        text-align: center;
        color: white;
        font-weight: bold;
        margin-top: 30px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------------
# CONTENT
# -------------------------------
st.markdown(f"<p class='header-text'>{FRIEND_NAME}'s Birthday 🍬</p>", unsafe_allow_html=True)

now = datetime.now(timezone(timedelta(hours=5, minutes=30)))
time_remaining = BIRTHDAY_DATETIME - now

if time_remaining.total_seconds() > 0 and not st.session_state["birthday_unlocked"]:

    days = time_remaining.days
    hours, remainder = divmod(time_remaining.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    st.markdown(
        f"""
        <div class="card">
            <div class="title">Counting down to the magic... ✨</div>
            <div class="timer">
                {days}d : {hours}h : {minutes}m : {seconds}s
            </div>
            <div class="subtitle">
                "Din aa raha hain bada khaas,<br>
                aapka birthday jo hain aas paas..." 😋🌸
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    time.sleep(1)
    st.rerun()

else:
    st.session_state["birthday_unlocked"] = True
    st.balloons()
    st.markdown(
        f"""
        <div class="card">
            <h1 style="color: #ff4d6d;">Happy Birthday {FRIEND_NAME}! 🎂</h1>
            <div class="subtitle">
                It's your day big dawggggg <br>
                Have a blast and loads of fun, bbg💕✨
            </div>
            <p style="font-size: 40px; margin-top: 20px;">🌸🍡✨🎁</p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<div class='footer'>Made with ❤️ just for you</div>", unsafe_allow_html=True)
