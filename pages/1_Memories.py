'''import streamlit as st
import os

import base64
import base64

def load_audio_base64(audio_path):
    with open(audio_path, "rb") as f:
        return base64.b64encode(f.read()).decode()
# -------------------------------
# BACKGROUND MUSIC
# -------------------------------
audio_base64 = load_audio_base64("assets/audio/bavra_mann.mp3")

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
    page_title="Memoriessssssssssss-(MAROON-5 type shit)",
    page_icon="😫",
    layout="wide"
)

# -------------------------------
# STYLING
# -------------------------------
st.markdown("""
<style>
/* REMOVE STREAMLIT COLUMN BACKGROUNDS */
div[data-testid="column"] {
    background: transparent !important;
    padding: 0 !important;
    border-radius: 0 !important;
}

/* ALSO CLEAN INNER COLUMN WRAPPER */
div[data-testid="stVerticalBlock"] > div {
    background: transparent !important;
}

         
/* REMOVE STREAMLIT DEFAULT SEPARATORS */
hr {
    display: none !important;
}

div[data-testid="stDivider"] {
    display: none !important;
}

body {
    background: radial-gradient(circle at top, #1b2735, #090a0f);
}

/* Section titles */
.section-title {
    font-size: 36px;
    font-weight: 700;
    text-align: center;
    margin-top: 110px;
    color: white;
}

.section-subtitle {
    text-align: center;
    font-size: 15px;
    color: #b0b0b0;
    margin-bottom: 50px;
}

/* Memory cards */
.memory-card {
    background: rgba(255,255,255,0.96);
    border-radius: 22px;
    padding: 10px;
    box-shadow: 0 18px 40px rgba(0,0,0,0.35);
    margin-bottom: 35px;
    opacity: 0;
    transform: translateY(40px);
    animation: fadeUp 0.8s ease forwards;
}

.memory-card:hover {
    transform: translateY(-6px) scale(1.02);
    transition: all 0.3s ease;
}

/* Video wrapper */
.video-wrapper {
    max-width: 720px;          /* Keeps it elegant on large screens */
    width: 90vw;               /* Responsive on smaller screens */
    margin: 60px auto 40px;
    border-radius: 22px;
    overflow: hidden;
    box-shadow: 0 20px 45px rgba(0,0,0,0.4);
    opacity: 0;
    transform: translateY(40px);
    animation: fadeUp 1s ease forwards;
}

/* Actual video element */
.video-wrapper video {
    width: 100%;
    height: auto;              /* 🔑 THIS ensures full video visibility */
    max-height: 80vh;          /* Prevents tall videos from overflowing screen */
    display: block;
    object-fit: contain;       /* Shows entire video, no cropping */
    background: black;         /* Clean letterboxing if needed */
}

/* Animation */
@keyframes fadeUp {
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.footer {
    text-align: center;
    color: #888;
    margin: 120px 0 40px;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)

def video_to_base64(video_path):
    with open(video_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# -------------------------------
# PAGE INTRO
# -------------------------------
st.markdown("<div class='section-title'>Aap Aur Aapke Khaas </div>", unsafe_allow_html=True)
st.markdown("<div class='section-subtitle'>ಕೆಲವು   ಮುದ್ದಾದ   ಕ್ಷಣಗಳು</div>", unsafe_allow_html=True)

# -------------------------------
# HELPER FUNCTION
# -------------------------------
def render_section(title, subtitle, folder_path, columns=4):
    st.markdown(f"<div class='section-title'>{title}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='section-subtitle'>{subtitle}</div>", unsafe_allow_html=True)

    files = sorted(os.listdir(folder_path))
    images = [f for f in files if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
    videos = [f for f in files if f.lower().endswith('.mp4')]

    if images:
        num_cols = min(columns, len(images))
        cols = st.columns(num_cols)

        for i, img in enumerate(images):
            with cols[i % num_cols]:
                st.markdown("<div class='memory-card'>", unsafe_allow_html=True)
                st.image(os.path.join(folder_path, img), width=320)
                st.markdown("</div>", unsafe_allow_html=True)

    for vid in videos:
        video_path = os.path.join(folder_path, vid)
        video_base64 = video_to_base64(video_path)

        st.markdown(
            f"""
            <div class="video-wrapper">
                <video controls preload="metadata">
                    <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
            </div>
            """,
            unsafe_allow_html=True
        )


import base64

def video_to_base64(video_path):
    with open(video_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# -------------------------------
# SECTIONS
# -------------------------------
render_section(
    "My Fatassss 💕",
    "full sike scenes",
    "assets/her",
    columns=4
)

render_section(
    " SLAYYYYYYYYYYYYYY KWEEEEENNNNNNNNN 🙈🙈",
    "Steamy type shit",
    "assets/herslayyyy",
    columns=4
)

render_section(
    " Heavyyyy Driverrrrrrrrr 🛺🛺",
    "150kmph ",
    "assets/hervrooom",
    columns=4
)

render_section(
    "Shraddhu jackson 🎶🎶",
    "dance india dance brand ambasador",
    "assets/herdance",
    columns=3
)

render_section(
    "U & I 🐾🐾",
    "ye ngo shoutout better join karna hain yaar ",
    "assets/us",
    columns=3
)

render_section(
    "Fantastic four halli version 🥀🥀",
    "gang gang gang",
    "assets/gang",
    columns=4
)

render_section(
    "back in the 3 feet days ",
    "🫣🫣",
    "assets/fam",
    columns=4
)

# -------------------------------
# FOOTER
# -------------------------------
st.markdown(
    "<div class='footer'>Some memories don’t need words.</div>",
    unsafe_allow_html=True
)












import streamlit as st
import os
import base64

# -------------------------------
# HELPER FUNCTIONS
# -------------------------------
def load_audio_base64(audio_path):
    try:
        with open(audio_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except: return None

def video_to_base64(video_path):
    with open(video_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="Memories for Shraddhu ✨",
    page_icon="🌸",
    layout="wide"
)

# -------------------------------
# BACKGROUND MUSIC
# -------------------------------
audio_base64 = load_audio_base64("assets/audio/bavra_mann.mp3")
if audio_base64:
    st.markdown(
        f"""
        <div class="romantic-audio">
            <span style="font-size: 12px; color: #ff4d6d; font-family: 'Comic Sans MS';">🎵 Bavra Mann...</span>
            <audio autoplay loop controls>
                <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
            </audio>
        </div>
        """,
        unsafe_allow_html=True
    )

# -------------------------------
# CUTE & ROMANTIC STYLING
# -------------------------------
st.markdown("""
<style>
/* Soft Romantic Background */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #fff0f3 0%, #ffddd2 100%);
}

/* Floating Audio Player */
.romantic-audio {
    position: fixed;
    bottom: 24px;
    right: 24px;
    background: rgba(255, 255, 255, 0.8);
    backdrop-filter: blur(10px);
    border: 2px solid #ffccd5;
    border-radius: 50px;
    padding: 8px 15px;
    z-index: 9999;
    box-shadow: 0 10px 30px rgba(255, 77, 109, 0.2);
}
.romantic-audio audio { height: 30px; width: 180px; }

/* Titles: Soft & Sparkling */
.section-title {
    font-family: 'Comic Sans MS', cursive, sans-serif;
    font-size: 42px;
    font-weight: bold;
    text-align: center;
    margin-top: 60px;
    color: #c9184a;
    text-shadow: 2px 2px 5px rgba(255, 77, 109, 0.2);
}

.section-subtitle {
    text-align: center;
    font-size: 18px;
    font-family: 'Georgia', serif;
    color: #ff758f;
    margin-bottom: 40px;
    font-style: italic;
}

/* Polaroid Memory Cards */
.memory-card {
    background: white;
    border-radius: 15px;
    padding: 12px;
    box-shadow: 0 12px 25px rgba(0,0,0,0.08);
    margin-bottom: 30px;
    border: 1px solid #ffe5ec;
    transition: transform 0.3s ease;
    text-align: center;
}

.memory-card:hover {
    transform: rotate(-2deg) scale(1.05);
}

.memory-card img {
    border-radius: 8px;
    border: 1px solid #f0f0f0;
}

/* Video Wrapper: Soft Glass */
.video-wrapper {
    max-width: 650px;
    margin: 40px auto;
    border-radius: 30px;
    overflow: hidden;
    padding: 15px;
    background: rgba(255, 255, 255, 0.5);
    backdrop-filter: blur(5px);
    border: 3px dashed #ffb3c1;
    box-shadow: 0 15px 35px rgba(255, 179, 193, 0.3);
}

.video-wrapper video {
    width: 100%;
    border-radius: 20px;
    display: block;
}

.footer {
    text-align: center;
    color: #ff758f;
    margin: 100px 0 50px;
    font-family: 'Comic Sans MS';
    font-size: 18px;
}

/* Remove default Streamlit junk */
#MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# HELPER RENDER FUNCTION
# -------------------------------
def render_section(title, subtitle, folder_path, columns=3):
    if not os.path.exists(folder_path):
        return

    st.markdown(f"<div class='section-title'>{title}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='section-subtitle'>{subtitle}</div>", unsafe_allow_html=True)

    files = sorted(os.listdir(folder_path))
    images = [f for f in files if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
    videos = [f for f in files if f.lower().endswith('.mp4')]

    if images:
        num_cols = min(columns, len(images))
        cols = st.columns(num_cols)
        for i, img in enumerate(images):
            with cols[i % num_cols]:
                st.markdown("<div class='memory-card'>", unsafe_allow_html=True)
                st.image(os.path.join(folder_path, img), use_container_width=True)
                # Small caption if you want to add them later
                st.markdown("</div>", unsafe_allow_html=True)

    for vid in videos:
        video_path = os.path.join(folder_path, vid)
        video_base64 = video_to_base64(video_path)
        st.markdown(
            f"""
            <div class="video-wrapper">
                <video controls>
                    <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
                </video>
            </div>
            """,
            unsafe_allow_html=True
        )

# -------------------------------
# MAIN INTRO
# -------------------------------
st.markdown("<div class='section-title' style='font-size: 55px;'>Aap Aur Aapke Khaas 🌸</div>", unsafe_allow_html=True)
st.markdown("<div class='section-subtitle' style='font-size: 22px;'>ಕೆಲವು ಮುದ್ದಾದ ಕ್ಷಣಗಳು (A walk down memory lane...)</div>", unsafe_allow_html=True)

# -------------------------------
# SECTIONS (Your specific folders)
# -------------------------------
render_section("My Fatassss 💕", "Full sike scenes with my favorite human.", "assets/her")
render_section("SLAYYYY KWEEEN 🙈", "The heat is real type shit.", "assets/herslayyyy")
render_section("Heavy Driver 🛺", "150kmph of pure chaos.", "assets/hervrooom")
render_section("Shraddhu Jackson 🎶", "Dance India Dance brand ambassador behavior.", "assets/herdance")
render_section("U & I 🐾", "Ngo shoutouts and us being us.", "assets/us")
render_section("Fantastic Four 🥀", "The gang gang gang.", "assets/gang")
render_section("The 3-Feet Days", "Back when everything was simple 🫣", "assets/fam")

# -------------------------------
# FOOTER
# -------------------------------
st.markdown("<div class='footer'>I promise to make a thousand more of these with you. ❤️</div>", unsafe_allow_html=True)





import streamlit as st
import os
import base64

# -------------------------------
# HELPER FUNCTIONS
# -------------------------------
def load_audio_base64(audio_path):
    try:
        with open(audio_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except: return None

def video_to_base64(video_path):
    with open(video_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="Memories for Shraddhu ✨",
    page_icon="🌸",
    layout="wide"
)

# -------------------------------
# BACKGROUND MUSIC
# -------------------------------
audio_base64 = load_audio_base64("assets/audio/bavra_mann.mp3")
if audio_base64:
    st.markdown(
        f"""
        <div class="romantic-audio">
            <span style="font-size: 12px; color: #ff4d6d; font-family: 'Comic Sans MS';">🎵 Bavra Mann...</span>
            <audio autoplay loop controls>
                <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
            </audio>
        </div>
        """,
        unsafe_allow_html=True
    )

# -------------------------------
# CUTE & ROMANTIC STYLING
# -------------------------------
st.markdown("""
<style>
/* Soft Romantic Background */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #fff0f3 0%, #ffddd2 100%);
}

/* Floating Audio Player */
.romantic-audio {
    position: fixed;
    bottom: 24px;
    right: 24px;
    background: rgba(255, 255, 255, 0.8);
    backdrop-filter: blur(10px);
    border: 2px solid #ffccd5;
    border-radius: 50px;
    padding: 8px 15px;
    z-index: 9999;
    box-shadow: 0 10px 30px rgba(255, 77, 109, 0.2);
}
.romantic-audio audio { height: 30px; width: 180px; }

/* Titles: Soft & Sparkling */
.section-title {
    font-family: 'Comic Sans MS', cursive, sans-serif;
    font-size: 42px;
    font-weight: bold;
    text-align: center;
    margin-top: 60px;
    color: #c9184a;
    text-shadow: 2px 2px 5px rgba(255, 77, 109, 0.2);
}

.section-subtitle {
    text-align: center;
    font-size: 18px;
    font-family: 'Georgia', serif;
    color: #ff758f;
    margin-bottom: 40px;
    font-style: italic;
}

/* Polaroid Memory Cards */
.memory-card {
    background: white;
    border-radius: 15px;
    padding: 12px;
    box-shadow: 0 12px 25px rgba(0,0,0,0.08);
    margin-bottom: 10px;
    border: 1px solid #ffe5ec;
    transition: transform 0.3s ease;
    text-align: center;
}

.memory-card:hover {
    transform: rotate(-2deg) scale(1.05);
}

.memory-card img {
    border-radius: 8px;
    border: 1px solid #f0f0f0;
}

/* Like button styling */
.like-button-container {
    text-align: center;
    margin-bottom: 20px;
}
.stButton button {
    background-color: #fff0f3 !important;
    color: #ff4d6d !important;
    border: 2px solid #ffccd5 !important;
    border-radius: 20px !important;
    padding: 5px 15px !important;
    font-size: 16px !important;
}
.stButton button:hover {
    background-color: #ffccd5 !important;
    border-color: #ff4d6d !important;
}

/* Video Wrapper: Fixed Sizing */
.video-wrapper {
    max-width: 650px;
    max-height: 500px; /* Added max-height to contain video */
    margin: 40px auto;
    border-radius: 30px;
    overflow: hidden; /* Hide overflow */
    padding: 15px;
    background: rgba(255, 255, 255, 0.5);
    backdrop-filter: blur(5px);
    border: 3px dashed #ffb3c1;
    box-shadow: 0 15px 35px rgba(255, 179, 193, 0.3);
    display: flex;
    justify-content: center;
    align-items: center;
}

.video-wrapper video {
    width: 100%;
    height: auto;
    max-height: 100%; /* Ensure it doesn't exceed wrapper height */
    border-radius: 20px;
    display: block;
    object-fit: contain; /* Maintain aspect ratio */
}

.footer {
    text-align: center;
    color: #ff758f;
    margin: 100px 0 50px;
    font-family: 'Comic Sans MS';
    font-size: 18px;
}

/* Remove default Streamlit junk */
#MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# HELPER RENDER FUNCTION
# -------------------------------
def render_section(title, subtitle, folder_path, columns=3):
    if not os.path.exists(folder_path):
        return

    st.markdown(f"<div class='section-title'>{title}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='section-subtitle'>{subtitle}</div>", unsafe_allow_html=True)

    files = sorted(os.listdir(folder_path))
    images = [f for f in files if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
    videos = [f for f in files if f.lower().endswith('.mp4')]

    if images:
        num_cols = min(columns, len(images))
        cols = st.columns(num_cols)
        for i, img in enumerate(images):
            with cols[i % num_cols]:
                img_path = os.path.join(folder_path, img)
                st.markdown("<div class='memory-card'>", unsafe_allow_html=True)
                st.image(img_path, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Heart/Like Button Logic
                button_key = f"like_{img_path}"
                if button_key not in st.session_state:
                    st.session_state[button_key] = False
                
                liked = st.session_state[button_key]
                button_label = "❤️ Loved it!" if liked else "🤍 Like"
                
                st.markdown("<div class='like-button-container'>", unsafe_allow_html=True)
                if st.button(button_label, key=button_key):
                    st.session_state[button_key] = not liked
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)


    for vid in videos:
        video_path = os.path.join(folder_path, vid)
        video_base64 = video_to_base64(video_path)
        st.markdown(
            f"""
            <div class="video-wrapper">
                <video controls>
                    <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
                </video>
            </div>
            """,
            unsafe_allow_html=True
        )

# -------------------------------
# MAIN INTRO
# -------------------------------
st.markdown("<div class='section-title' style='font-size: 55px;'>Aap Aur Aapke Khaas 🌸</div>", unsafe_allow_html=True)
st.markdown("<div class='section-subtitle' style='font-size: 22px;'>ಕೆಲವು ಮುದ್ದಾದ ಕ್ಷಣಗಳು (A walk down memory lane...)</div>", unsafe_allow_html=True)

# -------------------------------
# SECTIONS (Your specific folders)
# -------------------------------
render_section("My Fatassss 💕", "Full sike scenes with my favorite human.", "assets/her")
render_section("SLAYYYY KWEEEN 🙈", "The heat is real type shit.", "assets/herslayyyy")
render_section("Heavy Driver 🛺", "150kmph of pure chaos.", "assets/hervrooom")
render_section("Shraddhu Jackson 🎶", "Dance India Dance brand ambassador behavior.", "assets/herdance")
render_section("U & I 🐾", "Ngo shoutouts and us being us.", "assets/us")
render_section("Fantastic Four 🥀", "The gang gang gang.", "assets/gang")
render_section("The 3-Feet Days", "Back when everything was simple 🫣", "assets/fam")

# -------------------------------
# FOOTER
# -------------------------------
st.markdown("<div class='footer'>I promise to make a thousand more of these with you. ❤️</div>", unsafe_allow_html=True)'''









import streamlit as st
import os
import base64
if not st.session_state.get("birthday_unlocked", False):
    st.markdown("""
    <style>
    .lock-card {
        background: rgba(255, 255, 255, 0.9);
        padding: 60px 40px;
        border-radius: 40px;
        text-align: center;
        max-width: 500px;
        margin: 120px auto;
        box-shadow: 0 20px 50px rgba(255, 77, 109, 0.2);
        border: 3px dashed #ffb3c1;
    }
    .lock-title {
        font-size: 38px;
        color: #ff4d6d;
        font-family: 'Comic Sans MS', cursive;
        margin-bottom: 10px;
    }
    .lock-sub {
        font-size: 20px;
        color: #594e52;
        font-style: italic;
    }
    </style>

    <div class="lock-card">
        <div class="lock-title">Not yet baby girl 💕</div>
        <div class="lock-sub">
            Thoda sa intezaar aur…<br>
            the surprises are warming up 🫶✨
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()
# -------------------------------
# HELPER FUNCTIONS
# -------------------------------
def load_audio_base64(audio_path):
    try:
        with open(audio_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except: return None

def video_to_base64(video_path):
    with open(video_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="Memories for Shraddhu ✨",
    page_icon="🌸",
    layout="wide"
)

# -------------------------------
# BACKGROUND MUSIC
# -------------------------------
audio_base64 = load_audio_base64("assets/audio/bavra_mann.mp3")
if audio_base64:
    st.markdown(
        f"""
        <div class="romantic-audio">
            <span style="font-size: 12px; color: #ff4d6d; font-family: 'Comic Sans MS';">🎵 Bavra Mann...</span>
            <audio autoplay loop controls>
                <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
            </audio>
        </div>
        """,
        unsafe_allow_html=True
    )

# -------------------------------
# CUTE & ROMANTIC STYLING
# -------------------------------
st.markdown("""
<style>
/* Soft Romantic Background */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #fff0f3 0%, #ffddd2 100%);
}

/* Floating Audio Player */
.romantic-audio {
    position: fixed;
    bottom: 24px;
    right: 24px;
    background: rgba(255, 255, 255, 0.8);
    backdrop-filter: blur(10px);
    border: 2px solid #ffccd5;
    border-radius: 50px;
    padding: 8px 15px;
    z-index: 9999;
    box-shadow: 0 10px 30px rgba(255, 77, 109, 0.2);
}
.romantic-audio audio { height: 30px; width: 180px; }

/* Titles */
.section-title {
    font-family: 'Comic Sans MS', cursive, sans-serif;
    font-size: 42px;
    font-weight: bold;
    text-align: center;
    margin-top: 60px;
    color: #c9184a;
}

.section-subtitle {
    text-align: center;
    font-size: 18px;
    color: #ff758f;
    margin-bottom: 40px;
    font-style: italic;
}

/* Polaroid Memory Cards */
.memory-card {
    background: white;
    border-radius: 15px;
    padding: 12px;
    box-shadow: 0 12px 25px rgba(0,0,0,0.08);
    margin-bottom: 10px;
    border: 1px solid #ffe5ec;
}

/* Like button styling */
.like-button-container {
    text-align: center;
    margin-bottom: 30px;
}
.stButton button {
    background-color: white !important;
    color: #ff4d6d !important;
    border: 2px solid #ffccd5 !important;
    border-radius: 20px !important;
}

/* Fixed Video Sizing - Prevents the "Massive Video" issue */
.video-wrapper {
    max-width: 450px; /* Reduced width for a cuter look */
    margin: 20px auto;
    border-radius: 20px;
    overflow: hidden;
    background: white;
    padding: 10px;
    border: 2px dashed #ffb3c1;
    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
}

.video-wrapper video {
    width: 100%;
    max-height: 70vh; /* Limits height based on screen size */
    border-radius: 15px;
    display: block;
    object-fit: contain;
}

.footer {
    text-align: center;
    color: #ff758f;
    margin: 100px 0 50px;
    font-size: 18px;
}

#MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# HELPER RENDER FUNCTION
# -------------------------------
def render_section(title, subtitle, folder_path, columns=3):
    if not os.path.exists(folder_path):
        return

    st.markdown(f"<div class='section-title'>{title}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='section-subtitle'>{subtitle}</div>", unsafe_allow_html=True)

    files = sorted(os.listdir(folder_path))
    images = [f for f in files if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
    videos = [f for f in files if f.lower().endswith('.mp4')]

    # Render Images
    if images:
        num_cols = min(columns, len(images))
        cols = st.columns(num_cols)
        for i, img in enumerate(images):
            img_path = os.path.join(folder_path, img)
            with cols[i % num_cols]:
                st.markdown("<div class='memory-card'>", unsafe_allow_html=True)
                st.image(img_path, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
                # --- FIXED LIKE LOGIC ---
                status_key = f"status_{img_path}"
                button_key = f"btn_{img_path}"
                
                if status_key not in st.session_state:
                    st.session_state[status_key] = False
                
                liked = st.session_state[status_key]
                label = "❤️ Loved it!" if liked else "🤍 Like"
                
                if st.button(label, key=button_key, use_container_width=True):
                    st.session_state[status_key] = not liked
                    st.rerun()

    # Render Videos
    for vid in videos:
        video_path = os.path.join(folder_path, vid)
        video_base64 = video_to_base64(video_path)
        st.markdown(
            f"""
            <div class="video-wrapper">
                <video controls>
                    <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
                </video>
            </div>
            """,
            unsafe_allow_html=True
        )

# -------------------------------
# CONTENT
# -------------------------------
st.markdown("<div class='section-title' style='font-size: 55px;'>Aap Aur Aapke Khaas 🌸</div>", unsafe_allow_html=True)
st.markdown("<div class='section-subtitle' style='font-size: 22px;'>ಕೆಲವು ಮುದ್ದಾದ ಕ್ಷಣಗಳು</div>", unsafe_allow_html=True)

render_section("My Fatassss 💕", "Full sike scenes.", "assets/her")
render_section("SLAYYYY 🙈", "Steamy type shit.", "assets/herslayyyy")
render_section("Heavy Driver 🛺", "150kmph auto driver", "assets/hervrooom")
render_section("Shraddhu Jackson 🎶", "Dance India Dance Brand Ambassador", "assets/herdance")
render_section("U & I 🐾", "Ye making u feel guilty abt leaving ngo ", "assets/us")
render_section("Fantastic Four 🥀", "Gang gang gang", "assets/gang")
render_section("Back in the 3-Feet Days", "🫣🫣", "assets/fam")

st.markdown("<div class='footer'>I promise to make a thousand more of these with you. ❤️</div>", unsafe_allow_html=True)
