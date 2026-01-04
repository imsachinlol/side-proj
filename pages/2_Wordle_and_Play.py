'''import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import io

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="Magic Wordle & Art",
    page_icon="✨",
    layout="wide"
)

# -------------------------------
# SESSION STATE INITIALIZATION
# -------------------------------
if "guesses" not in st.session_state:
    st.session_state.guesses = []

if "wordle_done" not in st.session_state:
    st.session_state.wordle_done = False

if "canvas_done" not in st.session_state:
    st.session_state.canvas_done = False

if "show_canvas" not in st.session_state:
    st.session_state.show_canvas = False

if "pen_color" not in st.session_state:
    st.session_state.pen_color = "#ff7a7a"

if "brush_size" not in st.session_state:
    st.session_state.brush_size = 10

# ➕ ERASER STATE (NEW)
if "eraser_on" not in st.session_state:
    st.session_state.eraser_on = False

# -------------------------------
# STYLES
# -------------------------------
st.markdown("""
<style>
.block-container {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.wordle-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
}

.wordle-row {
    display: flex !important;
    justify-content: center !important;
    gap: 10px;
    margin-bottom: 10px;
}

.wordle-box {
    width: 60px;
    height: 60px;
    border: 2px solid #3a3a3c;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 30px;
    font-weight: bold;
    color: white;
    text-transform: uppercase;
}

.correct { background-color: #538d4e; border: none; }
.present { background-color: #b59f3b; border: none; }
.absent  { background-color: #3a3a3c; border: none; }
.empty   { background-color: transparent; }

div[data-testid="stForm"] {
    width: 350px !important;
    margin: 0 auto;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# PART 1: WORDLE
# -------------------------------
if not st.session_state.show_canvas:
    st.markdown("<h1 style='text-align: center;'>Let’s start with a small game 🧩</h1>", unsafe_allow_html=True)

    WORD = "MAGIC"
    MAX_TRIES = 6

    # Render grid
    st.markdown("<div class='wordle-container'>", unsafe_allow_html=True)

    for g_word, colors in st.session_state.guesses:
        row_html = "<div class='wordle-row'>"
        for i, char in enumerate(g_word):
            row_html += f"<div class='wordle-box {colors[i]}'>{char}</div>"
        st.markdown(row_html + "</div>", unsafe_allow_html=True)

    for _ in range(MAX_TRIES - len(st.session_state.guesses)):
        st.markdown(
            "<div class='wordle-row'>" +
            "".join(["<div class='wordle-box empty'></div>"] * 5) +
            "</div>",
            unsafe_allow_html=True
        )

    st.markdown("</div>", unsafe_allow_html=True)

    # End game
    if st.session_state.wordle_done:
        won = any(g[0] == WORD for g in st.session_state.guesses)
        if won:
            st.success(f"Perfect! The word was {WORD}. Some things are still magic ✨")
        else:
            st.error(f"Game Over! The word was {WORD}. Better luck next time!")

        if st.button("Continue to Canvas ✨", use_container_width=True, type="primary"):
            st.session_state.show_canvas = True
            st.rerun()

    else:
        with st.form("wordle_input", clear_on_submit=True):
            guess = st.text_input(
                "Guess",
                max_chars=5,
                label_visibility="collapsed",
                placeholder="GUESS"
            ).upper()
            submitted = st.form_submit_button("Submit", use_container_width=True)

        if submitted and len(guess) == 5:
            results = []
            for i, char in enumerate(guess):
                if char == WORD[i]:
                    results.append("correct")
                elif char in WORD:
                    results.append("present")
                else:
                    results.append("absent")

            st.session_state.guesses.append((guess, results))

            if guess == WORD or len(st.session_state.guesses) >= MAX_TRIES:
                st.session_state.wordle_done = True

            st.rerun()

# -------------------------------
# PART 2: CANVAS (WITH ERASER)
# -------------------------------
elif not st.session_state.canvas_done:
    st.markdown("<h1 style='text-align: center;'>Draw something for me ✨</h1>", unsafe_allow_html=True)

    with st.sidebar:
        st.header("🎨 Palette")
        st.session_state.pen_color = st.color_picker(
            "Color",
            st.session_state.pen_color
        )
        st.session_state.brush_size = st.slider(
            "Size",
            1,
            50,
            st.session_state.brush_size
        )

        brush_type = st.radio("Style", ["Smooth", "Spray"])
        st.session_state.eraser_on = st.checkbox(
            "🧽 Eraser",
            value=st.session_state.eraser_on
        )

        mode = "freedraw" if brush_type == "Smooth" else "point"

        if st.button("Reset Canvas"):
            st.rerun()

    col1, col2, col3 = st.columns([1, 10, 1])
    with col2:
        canvas_result = st_canvas(
            stroke_width=st.session_state.brush_size,
            stroke_color="#111111" if st.session_state.eraser_on else st.session_state.pen_color,
            background_color="#111111",
            height=550,
            width=900,
            drawing_mode=mode,
            key="canvas_main"
        )

        if st.button("💾 Save Drawing", use_container_width=True, type="primary"):
            if canvas_result.image_data is not None:
                img = Image.fromarray(
                    canvas_result.image_data.astype('uint8'),
                    'RGBA'
                )
                buffered = io.BytesIO()
                img.save(buffered, format="PNG")
                st.session_state.final_img = buffered.getvalue()
                st.session_state.canvas_done = True
                st.rerun()

# -------------------------------
# PART 3: FINALE
# -------------------------------
else:
    st.balloons()
    st.markdown("<h1 style='text-align: center;'>Beautiful Work!</h1>", unsafe_allow_html=True)

    col_f1, col_f2, col_f3 = st.columns([1, 2, 1])
    with col_f2:
        st.image(st.session_state.final_img)
        st.download_button(
            "Download Image",
            st.session_state.final_img,
            "art.png",
            "image/png",
            use_container_width=True
        )

        if st.button("Play Again", use_container_width=True):
            st.session_state.clear()
            st.rerun()





















import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import io

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="Magic Wordle & Art",
    page_icon="✨",
    layout="wide"
)

# -------------------------------
# SESSION STATE INITIALIZATION
# -------------------------------
if "phase" not in st.session_state:
    st.session_state.phase = "wordle" # wordle -> canvas -> crossword -> finale

# Wordle State
if "guesses" not in st.session_state:
    st.session_state.guesses = []
if "wordle_done" not in st.session_state:
    st.session_state.wordle_done = False

# Canvas State
if "pen_color" not in st.session_state:
    st.session_state.pen_color = "#ff7a7a"
if "brush_size" not in st.session_state:
    st.session_state.brush_size = 10
if "eraser_on" not in st.session_state:
    st.session_state.eraser_on = False

# Crossword State
CROSSWORD_DATA = {
    "THROWBALL": {"clue": "“A sport she swears she played in college”", "num": "1"},
    "GRAVEYARD": {"clue": "“Where our longest conversations strangely happen”", "num": "2"},
    "VIEWPOINT": {"clue": "“Where the sky did something unforgettable for the first time”", "num": "3"},
    "TIRAMISU": {"clue": "“A dessert she never really says no to”", "num": "4"},
    "CALIFORNIABURRITO": {"clue": "“The place she’d probably pick without opening the menu”", "num": "5"},
    "TRAIN": {"clue": "“Where a story begins when someone decides not to go home”", "num": "6 (Anchor)"},
}

if "cw_answers" not in st.session_state:
    st.session_state.cw_answers = {word: "" for word in CROSSWORD_DATA}

# -------------------------------
# SHARED STYLES
# -------------------------------
st.markdown("""
<style>
/* Centering */
.block-container { display: flex; flex-direction: column; align-items: center; }

/* Wordle Styles */
.wordle-container { display: flex; flex-direction: column; align-items: center; width: 100%; margin-bottom: 20px;}
.wordle-row { display: flex !important; justify-content: center !important; gap: 10px; margin-bottom: 10px; }
.wordle-box {
    width: 60px; height: 60px; border: 2px solid #3a3a3c;
    display: flex; align-items: center; justify-content: center;
    font-size: 30px; font-weight: bold; color: white; text-transform: uppercase;
}
.correct { background-color: #538d4e; border: none; }
.present { background-color: #b59f3b; border: none; }
.absent  { background-color: #3a3a3c; border: none; }
.empty   { background-color: transparent; }

/* Crossword NYT Style */
.cw-grid-container {
    background-color: #000;
    padding: 20px;
    border-radius: 8px;
    display: inline-block;
}
.cw-clue-card {
    background: #1e1e1e;
    padding: 15px;
    border-radius: 10px;
    border-left: 5px solid #ff7a7a;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# PHASE 1: WORDLE
# -------------------------------
if st.session_state.phase == "wordle":
    st.markdown("<h1 style='text-align: center;'>Let’s start with a small game 🧩</h1>", unsafe_allow_html=True)
    WORD = "MAGIC"
    
    st.markdown("<div class='wordle-container'>", unsafe_allow_html=True)
    for g_word, colors in st.session_state.guesses:
        row_html = "<div class='wordle-row'>"
        for i, char in enumerate(g_word):
            row_html += f"<div class='wordle-box {colors[i]}'>{char}</div>"
        st.markdown(row_html + "</div>", unsafe_allow_html=True)
    for _ in range(6 - len(st.session_state.guesses)):
        st.markdown("<div class='wordle-row'>" + "".join(["<div class='wordle-box empty'></div>"]*5) + "</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.wordle_done:
        won = any(g[0] == WORD for g in st.session_state.guesses)
        if won: st.success(f"Perfect! The word was {WORD}. Some things are still magic ✨")
        else: st.error(f"Game Over! The word was {WORD}.")
        
        if st.button("Continue to Canvas ✨", use_container_width=True, type="primary"):
            st.session_state.phase = "canvas"
            st.rerun()
    else:
        with st.form("wordle_input", clear_on_submit=True):
            guess = st.text_input("Guess", max_chars=5, label_visibility="collapsed", placeholder="GUESS").upper()
            if st.form_submit_button("Submit", use_container_width=True) and len(guess) == 5:
                results = ["correct" if c == WORD[i] else "present" if c in WORD else "absent" for i, c in enumerate(guess)]
                st.session_state.guesses.append((guess, results))
                if guess == WORD or len(st.session_state.guesses) >= 6: st.session_state.wordle_done = True
                st.rerun()

# -------------------------------
# PHASE 2: CANVAS
# -------------------------------
elif st.session_state.phase == "canvas":
    st.markdown("<h1 style='text-align: center;'>Draw something for me ✨</h1>", unsafe_allow_html=True)
    with st.sidebar:
        st.header("🎨 Tools")
        st.session_state.pen_color = st.color_picker("Color", st.session_state.pen_color)
        st.session_state.brush_size = st.slider("Size", 1, 50, st.session_state.brush_size)
        st.session_state.eraser_on = st.checkbox("🧽 Eraser")
        if st.button("Clear Canvas"): st.rerun()

    col1, col2, col3 = st.columns([1, 10, 1])
    with col2:
        canvas_result = st_canvas(
            stroke_width=st.session_state.brush_size,
            stroke_color="#111111" if st.session_state.eraser_on else st.session_state.pen_color,
            background_color="#111111",
            height=500, width=900, key="canvas_main"
        )
        if st.button("Save & Continue to Crossword 🧩", use_container_width=True, type="primary"):
            if canvas_result.image_data is not None:
                img = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA')
                buf = io.BytesIO(); img.save(buf, format="PNG")
                st.session_state.final_img = buf.getvalue()
                st.session_state.phase = "crossword"
                st.rerun()

# -------------------------------
# PHASE 3: CROSSWORD (NYT STYLE)
# -------------------------------
elif st.session_state.phase == "crossword":
    st.markdown("<h1 style='text-align: center;'>The Personal Puzzle 🌙</h1>", unsafe_allow_html=True)
    st.caption("Fill in the blanks. These are pieces of us.")

    col_clues, col_grid = st.columns([1, 1])

    with col_clues:
        st.markdown("### 🟦 Clues")
        for word, data in CROSSWORD_DATA.items():
            st.markdown(f"""
            <div class='cw-clue-card'>
                <strong>{data['num']}.</strong> {data['clue']}
            </div>
            """, unsafe_allow_html=True)

    with col_grid:
        st.markdown("### 📝 Your Answers")
        all_correct = True
        for word, data in CROSSWORD_DATA.items():
            user_input = st.text_input(
                f"Word {data['num']}", 
                value=st.session_state.cw_answers[word],
                key=f"input_{word}",
                placeholder=f"{len(word)} letters"
            ).upper().replace(" ", "")
            
            st.session_state.cw_answers[word] = user_input
            
            if user_input != word:
                all_correct = False
        
        st.divider()
        if all_correct:
            st.success("Every piece fits perfectly. ❤️")
            if st.button("Finalize Journey ✨", use_container_width=True, type="primary"):
                st.session_state.phase = "finale"
                st.rerun()
        else:
            st.info("Keep going! The boxes will stay blue until it's all correct.")

# -------------------------------
# PHASE 4: FINALE
# -------------------------------
else:
    st.balloons()
    st.markdown("<h1 style='text-align: center;'>I know what you love. 💖</h1>", unsafe_allow_html=True)
    col_f1, col_f2, col_f3 = st.columns([1, 2, 1])
    with col_f2:
        st.image(st.session_state.final_img, caption="Your Artwork")
        st.download_button("Download Your Drawing", st.session_state.final_img, "us.png", "image/png", use_container_width=True)
        if st.button("Play Again", use_container_width=True):
            st.session_state.clear()
            st.rerun()









































import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import io
import base64

# -------------------------------
# HELPER: AUDIO
# -------------------------------
def load_audio_base64(audio_path):
    try:
        with open(audio_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except: return ""

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="Magic Wordle & Art",
    page_icon="✨",
    layout="wide"
)

# -------------------------------
# GLOBAL SOFT STYLING
# -------------------------------
st.markdown("""
<style>
/* Soft Background for the whole app */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #f3e7e9 0%, #e3eeff 100%);
}

/* Center Content */
.block-container { display: flex; flex-direction: column; align-items: center; }

/* Cute Headers */
h1 {
    font-family: 'Comic Sans MS', cursive, sans-serif;
    color: #8e7dbe !important; /* Soft Lavender */
}

/* --- Wordle Refresh --- */
.wordle-container { display: flex; flex-direction: column; align-items: center; width: 100%; margin-bottom: 20px;}
.wordle-row { display: flex !important; justify-content: center !important; gap: 10px; margin-bottom: 10px; }
.wordle-box {
    width: 60px; height: 60px; 
    border: 2px solid #d1d1d1;
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 30px; font-weight: bold; color: #555; text-transform: uppercase;
    background-color: white;
}
.correct { background-color: #b8e0b8; border: none; color: white; } /* Pastel Green */
.present { background-color: #f9e1a9; border: none; color: white; } /* Pastel Yellow */
.absent  { background-color: #d3d3d3; border: none; color: white; } /* Soft Grey */
.empty   { background-color: rgba(255,255,255,0.5); }

/* --- Canvas Sidebar --- */
[data-testid="stSidebar"] {
    background-color: rgba(255, 255, 255, 0.6) !important;
}

/* --- Floating Audio --- */
.romantic-audio {
    position: fixed;
    bottom: 24px;
    right: 24px;
    background: rgba(255, 255, 255, 0.7);
    backdrop-filter: blur(8px);
    border-radius: 999px;
    padding: 10px 14px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    z-index: 9999;
    border: 1px solid #ffccd5;
}
</style>
""", unsafe_allow_html=True)

# Audio Injection
audio_base64 = load_audio_base64("assets/audio/bavra_mann.mp3")
if audio_base64:
    st.markdown(f"""
        <div class="romantic-audio">
            <audio autoplay loop controls style="width: 200px; height: 30px;">
                <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
            </audio>
        </div>
    """, unsafe_allow_html=True)

# -------------------------------
# SESSION STATE INITIALIZATION
# -------------------------------
if "phase" not in st.session_state:
    st.session_state.phase = "wordle"

if "guesses" not in st.session_state: st.session_state.guesses = []
if "wordle_done" not in st.session_state: st.session_state.wordle_done = False
if "pen_color" not in st.session_state: st.session_state.pen_color = "#ffb7b7"
if "brush_size" not in st.session_state: st.session_state.brush_size = 10
if "eraser_on" not in st.session_state: st.session_state.eraser_on = False

CROSSWORD_DATA = {
    "THROWBALL": {"clue": "A sport she swears she played in college", "num": "1"},
    "GRAVEYARD": {"clue": "Where our longest conversations strangely happen", "num": "2"},
    "VIEWPOINT": {"clue": "Where the sky did something unforgettable for the first time", "num": "3"},
    "TIRAMISU": {"clue": "A dessert she never really says no to", "num": "4"},
    "CALIFORNIABURRITO": {"clue": "The place she is always ready to eat at w/o a second thought", "num": "5"},
    "TRAIN": {"clue": "Where a story begins when someone decides not to go home (fav movie answer)", "num": "6"},
}

if "cw_answers" not in st.session_state:
    st.session_state.cw_answers = {word: "" for word in CROSSWORD_DATA}

# -------------------------------
# PHASE 1: WORDLE
# -------------------------------
if st.session_state.phase == "wordle":
    st.markdown("<h1 style='text-align: center;'>A Small Game for You 🌸</h1>", unsafe_allow_html=True)
    WORD = "MAGIC"
    
    st.markdown("<div class='wordle-container'>", unsafe_allow_html=True)
    for g_word, colors in st.session_state.guesses:
        row_html = "<div class='wordle-row'>"
        for i, char in enumerate(g_word):
            row_html += f"<div class='wordle-box {colors[i]}'>{char}</div>"
        st.markdown(row_html + "</div>", unsafe_allow_html=True)
    
    for _ in range(6 - len(st.session_state.guesses)):
        st.markdown("<div class='wordle-row'>" + "".join(["<div class='wordle-box empty'></div>"]*5) + "</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.wordle_done:
        won = any(g[0] == WORD for g in st.session_state.guesses)
        if won: st.success("Perfect! You found the magic ✨")
        else: st.info(f"The word was {WORD}. You're still magic to me! ☁️")
        
        if st.button("Continue ✨", use_container_width=True, type="primary"):
            st.session_state.phase = "canvas"
            st.rerun()
    else:
        with st.form("wordle_input", clear_on_submit=True):
            guess = st.text_input("Guess", max_chars=5, label_visibility="collapsed", placeholder="GUESS").upper()
            if st.form_submit_button("Check 🍬", use_container_width=True) and len(guess) == 5:
                results = ["correct" if c == WORD[i] else "present" if c in WORD else "absent" for i, c in enumerate(guess)]
                st.session_state.guesses.append((guess, results))
                if guess == WORD or len(st.session_state.guesses) >= 6: st.session_state.wordle_done = True
                st.rerun()

# -------------------------------
# PHASE 2: CANVAS
# -------------------------------
elif st.session_state.phase == "canvas":
    st.markdown("<h1 style='text-align: center;'>Doodle Something Sweet ✨</h1>", unsafe_allow_html=True)
    with st.sidebar:
        st.header("🎨 Palette")
        st.session_state.pen_color = st.color_picker("Pick a color", st.session_state.pen_color)
        st.session_state.brush_size = st.slider("Brush Size", 1, 50, st.session_state.brush_size)
        st.session_state.eraser_on = st.checkbox("🧽 Use Eraser")
        if st.button("Clear Canvas"): st.rerun()

    col1, col2, col3 = st.columns([1, 10, 1])
    with col2:
        canvas_result = st_canvas(
            stroke_width=st.session_state.brush_size,
            stroke_color="#FFFFFF" if st.session_state.eraser_on else st.session_state.pen_color,
            background_color="#FFFFFF", # White background for a clean look
            height=500, width=900, key="canvas_main"
        )
        if st.button("Save & Go to Memory Box ☁️", use_container_width=True, type="primary"):
            if canvas_result and canvas_result.image_data is not None:
                img = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA')
                buf = io.BytesIO()
                img.save(buf, format="PNG")
                st.session_state.final_img = buf.getvalue()
                st.session_state.phase = "crossword"
                st.rerun()

# -------------------------------
# PHASE 3: THE MEMORY BOX (ALREADY CUTE)
# -------------------------------
elif st.session_state.phase == "crossword":
    st.markdown("<style>.memory-card { background: #fff0f6; padding: 20px; border-radius: 20px; border: 2px dashed #ffadad; margin-bottom: 20px; box-shadow: 5px 5px 15px rgba(0,0,0,0.05); } .memory-title { color: #ff4d6d; font-family: 'Comic Sans MS', cursive, sans-serif; font-size: 1.5rem; margin-bottom: 10px; } .stTextInput input { border-radius: 15px !important; border: 2px solid #ffccd5 !important; text-align: center; } </style>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #ff4d6d;'>Our Little Secret Journal 🌸</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        all_correct = True
        correct_count = 0
        for word, data in CROSSWORD_DATA.items():
            st.markdown(f'<div class="memory-card"><div class="memory-title">💌 Memory #{data["num"]}</div><p style="color: #594e52;">{data["clue"]}</p></div>', unsafe_allow_html=True)
            val = st.text_input("Answer", value=st.session_state.cw_answers.get(word, ""), key=f"in_{word}", label_visibility="collapsed").strip().upper()
            st.session_state.cw_answers[word] = val
            if val == word: correct_count += 1
            else: all_correct = False
        
        st.progress(correct_count / len(CROSSWORD_DATA))
        if all_correct:
            st.snow()
            if st.button("Final Surprise 🎁", use_container_width=True, type="primary"):
                st.session_state.phase = "finale"
                st.rerun()

# -------------------------------
# PHASE 4: FINALE
# -------------------------------
else:
    st.balloons()
    st.markdown("<h1 style='text-align: center;'>For You, Always 💖</h1>", unsafe_allow_html=True)
    col_f1, col_f2, col_f3 = st.columns([1, 2, 1])
    with col_f2:
        if "final_img" in st.session_state:
            st.image(st.session_state.final_img, caption="A piece of your heart")
        st.markdown("<p style='text-align: center;'>Every moment with you is my favorite memory.</p>", unsafe_allow_html=True)
        if st.button("Start Over? 🍡", use_container_width=True):
            st.session_state.clear()
            st.rerun()


import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import io
import base64
import os

# -------------------------------
# 1. HELPER FUNCTIONS
# -------------------------------
def load_audio_base64(audio_path):
    try:
        with open(audio_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return ""

# -------------------------------
# 2. PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="Magic Wordle & Art ✨",
    page_icon="🌸",
    layout="wide"
)

# -------------------------------
# 3. SESSION STATE INITIALIZATION
# -------------------------------
if "phase" not in st.session_state:
    st.session_state.phase = "wordle" # wordle -> canvas -> crossword -> finale

# Wordle State
if "guesses" not in st.session_state: st.session_state.guesses = []
if "wordle_done" not in st.session_state: st.session_state.wordle_done = False

# Canvas State
if "pen_color" not in st.session_state: st.session_state.pen_color = "#ffb7b7"
if "brush_size" not in st.session_state: st.session_state.brush_size = 10
if "eraser_on" not in st.session_state: st.session_state.eraser_on = False

# Memory Box Data
CROSSWORD_DATA = {
    "THROWBALL": {"clue": "A sport she swears she played in college", "num": "1"},
    "GRAVEYARD": {"clue": "Where our longest conversations strangely happen", "num": "2"},
    "VIEWPOINT": {"clue": "Where the sky did something unforgettable for the first time", "num": "3"},
    "TIRAMISU": {"clue": "A dessert she never really says no to", "num": "4"},
    "CALIFORNIABURRITO": {"clue": "The place she is always ready to eat at w/o a second thought", "num": "5"},
    "TRAIN": {"clue": "Where a story begins when someone decides not to go home (fav movie answer)", "num": "6"},
}

if "cw_answers" not in st.session_state:
    st.session_state.cw_answers = {word: "" for word in CROSSWORD_DATA}

# -------------------------------
# 4. GLOBAL AESTHETIC STYLING
# -------------------------------
st.markdown("""
<style>
/* Soft Aesthetic Background */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #fdfcfb 0%, #e2d1c3 100%);
}

/* Sidebar Visibility Fix - Making it solid and readable */
[data-testid="stSidebar"] {
    background-color: white !important;
    border-right: 1px solid #ffe5ec;
}
[data-testid="stSidebar"] * {
    color: #4a4a4a !important;
}

/* Floating Audio Player */
.romantic-audio {
    position: fixed;
    bottom: 24px;
    right: 24px;
    background: rgba(255, 255, 255, 0.85);
    backdrop-filter: blur(12px);
    border-radius: 999px;
    padding: 10px 14px;
    box-shadow: 0 8px 25px rgba(255, 105, 135, 0.2);
    z-index: 9999;
    border: 1px solid #ffccd5;
}

/* Wordle Grid Styling */
.wordle-container { display: flex; flex-direction: column; align-items: center; width: 100%; margin-bottom: 20px;}
.wordle-row { display: flex !important; justify-content: center !important; gap: 10px; margin-bottom: 10px; }
.wordle-box {
    width: 60px; height: 60px; 
    border: 2px solid #eee;
    border-radius: 15px;
    display: flex; align-items: center; justify-content: center;
    font-size: 28px; font-weight: bold; color: #555; 
    background-color: white;
}
.correct { background-color: #b8e0b8 !important; color: white !important; border: none; }
.present { background-color: #f9e1a9 !important; color: white !important; border: none; }
.absent  { background-color: #d1d1d1 !important; color: white !important; border: none; }

/* Memory Card Style */
.memory-card {
    background: #fff0f6;
    padding: 20px;
    border-radius: 20px;
    border: 2px dashed #ffadad;
    margin-bottom: 20px;
    box-shadow: 5px 5px 15px rgba(0,0,0,0.03);
}

/* Soft Buttons */
.stButton>button {
    border-radius: 20px !important;
    border: 1px solid #ffccd5 !important;
    background-color: white !important;
    color: #ff4d6d !important;
    transition: all 0.3s ease;
}
.stButton>button:hover {
    background-color: #ff4d6d !important;
    color: white !important;
}

/* Canvas Styling */
.stCanvas {
    border: 5px solid white !important;
    border-radius: 20px !important;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1) !important;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# 5. MUSIC PLAYER
# -------------------------------
audio_base64 = load_audio_base64("assets/audio/bavra_mann.mp3")
if audio_base64:
    st.markdown(f"""
        <div class="romantic-audio">
            <audio autoplay loop controls style="width: 210px; height: 30px;">
                <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
            </audio>
        </div>
    """, unsafe_allow_html=True)

# -------------------------------
# PHASE 1: WORDLE
# -------------------------------
if st.session_state.phase == "wordle":
    st.markdown("<h1 style='text-align: center; color: #8e7dbe;'>A Small Game for You 🧩</h1>", unsafe_allow_html=True)
    WORD = "MAGIC"
    
    st.markdown("<div class='wordle-container'>", unsafe_allow_html=True)
    for g_word, colors in st.session_state.guesses:
        row_html = "<div class='wordle-row'>"
        for i, char in enumerate(g_word):
            row_html += f"<div class='wordle-box {colors[i]}'>{char}</div>"
        st.markdown(row_html + "</div>", unsafe_allow_html=True)
    for _ in range(6 - len(st.session_state.guesses)):
        st.markdown("<div class='wordle-row'>" + "".join(["<div class='wordle-box'></div>"]*5) + "</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.wordle_done:
        if any(g[0] == WORD for g in st.session_state.guesses):
            st.success("Perfect! You found the magic ✨")
        else:
            st.info(f"The word was {WORD}. You're still magic to me! ☁️")
        
        if st.button("Continue to Canvas ✨", use_container_width=True):
            st.session_state.phase = "canvas"
            st.rerun()
    else:
        col_in1, col_in2, col_in3 = st.columns([1,1,1])
        with col_in2:
            with st.form("wordle_input", clear_on_submit=True):
                guess = st.text_input("Guess", max_chars=5, label_visibility="collapsed", placeholder="ENTER 5 LETTERS").upper()
                if st.form_submit_button("Submit 🍬", use_container_width=True) and len(guess) == 5:
                    results = ["correct" if c == WORD[i] else "present" if c in WORD else "absent" for i, c in enumerate(guess)]
                    st.session_state.guesses.append((guess, results))
                    if guess == WORD or len(st.session_state.guesses) >= 6: 
                        st.session_state.wordle_done = True
                    st.rerun()

# -------------------------------
# PHASE 2: CANVAS
# -------------------------------
elif st.session_state.phase == "canvas":
    st.markdown("<h1 style='text-align: center; color: #8e7dbe;'>Doodle Something Sweet ✨</h1>", unsafe_allow_html=True)
    with st.sidebar:
        st.markdown("### 🎨 Palette & Tools")
        st.session_state.pen_color = st.color_picker("Pick a color", st.session_state.pen_color)
        st.session_state.brush_size = st.slider("Brush Size", 1, 50, st.session_state.brush_size)
        st.session_state.eraser_on = st.checkbox("🧽 Use Eraser")
        if st.button("Clear Canvas", use_container_width=True): st.rerun()

    col_c1, col_c2, col_c3 = st.columns([1, 8, 1])
    with col_c2:
        canvas_result = st_canvas(
            stroke_width=st.session_state.brush_size,
            stroke_color="#FFFFFF" if st.session_state.eraser_on else st.session_state.pen_color,
            background_color="#FFFFFF",
            height=450, width=700, drawing_mode="freedraw", key="canvas_main",
        )
        if st.button("Done! Save this Memory ☁️", use_container_width=True, type="primary"):
            if canvas_result and canvas_result.image_data is not None:
                img = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA')
                buf = io.BytesIO()
                img.save(buf, format="PNG")
                st.session_state.final_img = buf.getvalue()
                st.session_state.phase = "crossword"
                st.rerun()

# -------------------------------






import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import io
import base64

def load_audio_base64(audio_path):
    with open(audio_path, "rb") as f:
        return base64.b64encode(f.read()).decode()
# -------------------------------
# BACKGROUND MUSIC
# -------------------------------
audio_base64 = load_audio_base64("assets/audio/bhole.mp3")


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
    page_title="Magic Wordle & Art",
    page_icon="✨",
    layout="wide"
)

# -------------------------------
# SESSION STATE INITIALIZATION
# -------------------------------
if "phase" not in st.session_state:
    st.session_state.phase = "wordle" # wordle -> canvas -> crossword -> finale

# Wordle State
if "guesses" not in st.session_state:
    st.session_state.guesses = []
if "wordle_done" not in st.session_state:
    st.session_state.wordle_done = False

# Canvas State
if "pen_color" not in st.session_state:
    st.session_state.pen_color = "#ff7a7a"
if "brush_size" not in st.session_state:
    st.session_state.brush_size = 10
if "eraser_on" not in st.session_state:
    st.session_state.eraser_on = False

# Crossword State
CROSSWORD_DATA = {
    "THROWBALL": {"clue": "A sport she swears she played in college", "num": "1", "direction": "across", "row": 0, "col": 0},
    "GRAVEYARD": {"clue": "Where our longest conversations strangely happen", "num": "2", "direction": "down", "row": 0, "col": 0},
    "VIEWPOINT": {"clue": "Where the sky did something unforgettable for the first time", "num": "3", "direction": "across", "row": 2, "col": 0},
    "TIRAMISU": {"clue": "A dessert she never really says no to", "num": "4", "direction": "down", "row": 2, "col": 5},
    "CALIFORNIABURRITO": {"clue": "The place she is always ready to eat at w/o a second thought", "num": "5", "direction": "across", "row": 4, "col": 0},
    "TRAIN": {"clue": "Where a story begins when someone decides not to go home(answer is in one of your fav movies)", "num": "6 (Anchor)", "direction": "down", "row": 4, "col": 0},
}

if "cw_answers" not in st.session_state:
    st.session_state.cw_answers = {word: "" for word in CROSSWORD_DATA}

# -------------------------------
# SHARED STYLES
# -------------------------------
st.markdown("""
<style>
/* Centering */
.block-container { display: flex; flex-direction: column; align-items: center; }

/* Wordle Styles */
.wordle-container { display: flex; flex-direction: column; align-items: center; width: 100%; margin-bottom: 20px;}
.wordle-row { display: flex !important; justify-content: center !important; gap: 10px; margin-bottom: 10px; }
.wordle-box {
    width: 60px; height: 60px; border: 2px solid #3a3a3c;
    display: flex; align-items: center; justify-content: center;
    font-size: 30px; font-weight: bold; color: white; text-transform: uppercase;
}
.correct { background-color: #538d4e; border: none; }
.present { background-color: #b59f3b; border: none; }
.absent  { background-color: #3a3a3c; border: none; }
.empty   { background-color: transparent; }

/* NYT-Style Crossword Grid */
.crossword-grid {
    display: inline-block;
    border: 3px solid #000;
    background: #000;
    padding: 0;
    margin: 20px auto;
}

.cw-row {
    display: flex;
    margin: 0;
    padding: 0;
}

.cw-cell {
    width: 40px;
    height: 40px;
    border: 1px solid #000;
    background: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    font-weight: 600;
    text-transform: uppercase;
    position: relative;
    font-family: 'Franklin Gothic Medium', sans-serif;
    color: #000;
}

.cw-cell.black {
    background: #000;
}

.cw-cell.correct {
    background: #f0f0f0;
    color: #000;
}

.cw-cell-number {
    position: absolute;
    top: 2px;
    left: 3px;
    font-size: 10px;
    font-weight: bold;
    color: #000;
}

/* Clue Cards NYT Style */
.cw-clue-section {
    background: #fff;
    padding: 20px;
    border-radius: 8px;
    margin: 10px 0;
    border: 1px solid #ddd;
}

.cw-clue-item {
    padding: 10px 0;
    border-bottom: 1px solid #eee;
    font-size: 16px;
    color: #333;
}

.cw-clue-item:last-child {
    border-bottom: none;
}

.cw-clue-num {
    font-weight: bold;
    margin-right: 8px;
    color: #000;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# PHASE 1: WORDLE
# -------------------------------
if st.session_state.phase == "wordle":
    st.markdown("<h1 style='text-align: center;'>Let's start with a small game 🧩</h1>", unsafe_allow_html=True)
    WORD = "MAGIC"
    
    st.markdown("<div class='wordle-container'>", unsafe_allow_html=True)
    for g_word, colors in st.session_state.guesses:
        row_html = "<div class='wordle-row'>"
        for i, char in enumerate(g_word):
            row_html += f"<div class='wordle-box {colors[i]}'>{char}</div>"
        st.markdown(row_html + "</div>", unsafe_allow_html=True)
    for _ in range(6 - len(st.session_state.guesses)):
        st.markdown("<div class='wordle-row'>" + "".join(["<div class='wordle-box empty'></div>"]*5) + "</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.wordle_done:
        won = any(g[0] == WORD for g in st.session_state.guesses)
        if won: st.success(f"Perfect! The word was {WORD}. Some things are still magic ✨")
        else: st.error(f"Game Over! The word was {WORD}.")
        
        if st.button("Continue to Canvas ✨", use_container_width=True, type="primary"):
            st.session_state.phase = "canvas"
            st.rerun()
    else:
        with st.form("wordle_input", clear_on_submit=True):
            guess = st.text_input("Guess", max_chars=5, label_visibility="collapsed", placeholder="GUESS").upper()
            if st.form_submit_button("Submit", use_container_width=True) and len(guess) == 5:
                results = ["correct" if c == WORD[i] else "present" if c in WORD else "absent" for i, c in enumerate(guess)]
                st.session_state.guesses.append((guess, results))
                if guess == WORD or len(st.session_state.guesses) >= 6: st.session_state.wordle_done = True
                st.rerun()

# -------------------------------
# PHASE 2: CANVAS
# -------------------------------
elif st.session_state.phase == "canvas":
    st.markdown("<h1 style='text-align: center;'>Draw something for me ✨</h1>", unsafe_allow_html=True)
    with st.sidebar:
        st.header("🎨 Tools")
        st.session_state.pen_color = st.color_picker("Color", st.session_state.pen_color)
        st.session_state.brush_size = st.slider("Size", 1, 50, st.session_state.brush_size)
        st.session_state.eraser_on = st.checkbox("🧽 Eraser")
        if st.button("Clear Canvas"): st.rerun()

    col1, col2, col3 = st.columns([1, 10, 1])
    with col2:
        canvas_result = st_canvas(
            stroke_width=st.session_state.brush_size,
            stroke_color="#111111" if st.session_state.eraser_on else st.session_state.pen_color,
            background_color="#111111",
            height=500, width=900, key="canvas_main"
        )
        if st.button("Save & Continue to MEMORY BOXXX", use_container_width=True, type="primary"):
            if canvas_result and canvas_result.image_data is not None:
                img = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA')
                buf = io.BytesIO()
                img.save(buf, format="PNG")
                st.session_state.final_img = buf.getvalue()
                st.session_state.phase = "crossword"
                st.rerun()
            else:
                st.warning("Please draw something first before saving!")

# -------------------------------
# PHASE 3: THE MEMORY BOX (CUTE VERSION)
# -------------------------------
elif st.session_state.phase == "crossword":
    # Custom CSS for the "Cute" vibe
    st.markdown("""
        <style>
        .memory-card {
            background: #fff0f6;
            padding: 20px;
            border-radius: 20px;
            border: 2px dashed #ffadad;
            margin-bottom: 20px;
            box-shadow: 5px 5px 15px rgba(0,0,0,0.05);
        }
        .memory-title {
            color: #ff4d6d;
            font-family: 'Comic Sans MS', cursive, sans-serif;
            font-size: 1.5rem;
            margin-bottom: 10px;
        }
        .stTextInput input {
            border-radius: 15px !important;
            border: 2px solid #ffccd5 !important;
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 style='text-align: center; color: #ff4d6d;'>Our Little Secret Journal 🌸</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #ff758f;'>Can you remember these tiny moments? ✨</p>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        all_correct = True
        total_memories = len(CROSSWORD_DATA)
        correct_count = 0

        for word, data in CROSSWORD_DATA.items():
            # Check if this specific answer is already correct
            is_correct = st.session_state.cw_answers.get(word, "").upper() == word.upper()
            
            # Memory Card Container
            st.markdown(f"""
                <div class="memory-card">
                    <div class="memory-title">💌 Memory #{data['num'].split()[0]}</div>
                    <p style="color: #594e52; font-size: 1.1rem;">{data['clue']}</p>
                </div>
            """, unsafe_allow_html=True)

            # Input field
            val = st.text_input(
                "Guess the word...", 
                value=st.session_state.cw_answers.get(word, ""),
                key=f"input_{word}",
                label_visibility="collapsed",
                placeholder="Type the magic word here..."
            ).strip().upper().replace(" ", "")

            st.session_state.cw_answers[word] = val

            if val == word:
                st.markdown("<p style='color: #ff4d6d; text-align: center; font-weight: bold;'>You got it! 🥰</p>", unsafe_allow_html=True)
                correct_count += 1
            elif val != "":
                st.markdown("<p style='color: #ffb3c1; text-align: center; font-size: 0.8rem;'>Not quite, my love! Try again? 🌸</p>", unsafe_allow_html=True)
                all_correct = False
            else:
                all_correct = False
            
            st.markdown("<br>", unsafe_allow_html=True)

        # Progress bar but make it cute
        progress = correct_count / total_memories
        st.write(f"<p style='text-align: center; color: #ff4d6d;'>{correct_count} of {total_memories} memories found ☁️</p>", unsafe_allow_html=True)
        st.progress(progress)

        if all_correct:
            st.snow() # Fun visual effect!
            st.markdown("<h3 style='text-align: center; color: #ff4d6d;'>Yay! You remembered everything! 💖</h3>", unsafe_allow_html=True)
            if st.button("See My Final Surprise 🎁", use_container_width=True, type="primary"):
                st.session_state.phase = "finale"
                st.rerun()
# -------------------------------
# PHASE 4: FINALE
# -------------------------------
else:
    st.balloons()
    st.markdown("<h1 style='text-align: center;'>I know what you love. 💖</h1>", unsafe_allow_html=True)
    col_f1, col_f2, col_f3 = st.columns([1, 2, 1])
    with col_f2:
        if "final_img" in st.session_state:
            st.image(st.session_state.final_img, caption="Your Artwork")
            st.download_button("Download Your Drawing", st.session_state.final_img, "us.png", "image/png", use_container_width=True)
        if st.button("Play Again", use_container_width=True):
            st.session_state.clear()
            st.rerun()'''







import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import io
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
def load_audio_base64(audio_path):
    # Note: Ensure the path is correct for your local setup
    try:
        with open(audio_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return ""

# -------------------------------
# BACKGROUND MUSIC
# -------------------------------
audio_base64 = load_audio_base64("assets/audio/bhole.mp3")

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Dancing+Script:wght@400;700&display=swap');

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

    /* Letter Styling */
    .letter-bg {{
        background-color: #fce4ec;
        padding: 40px;
        border-radius: 20px;
        border: 2px solid #f8bbd0;
    }}

    .letter-paper {{
        background: #fffdf5;
        padding: 50px;
        border-radius: 5px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        font-family: 'Dancing Script', cursive;
        font-size: 24px;
        line-height: 1.6;
        color: #4a4a4a;
        max-width: 800px;
        margin: 20px auto;
        position: relative;
        border-left: 40px solid #ffccd5;
    }}

    .letter-content {{
        margin-bottom: 20px;
    }}

    .quote-box {{
        font-style: italic;
        color: #ff4d6d;
        font-weight: bold;
        padding: 10px 0;
        text-align: center;
    }}

    .signature {{
        text-align: right;
        font-size: 30px;
        color: #ff4d6d;
        margin-top: 30px;
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
    page_title="Magic Wordle & Art",
    page_icon="✨",
    layout="wide"
)

# -------------------------------
# SESSION STATE INITIALIZATION
# -------------------------------
if "phase" not in st.session_state:
    st.session_state.phase = "wordle" 

if "guesses" not in st.session_state:
    st.session_state.guesses = []
if "wordle_done" not in st.session_state:
    st.session_state.wordle_done = False

if "pen_color" not in st.session_state:
    st.session_state.pen_color = "#ff7a7a"
if "brush_size" not in st.session_state:
    st.session_state.brush_size = 10
if "eraser_on" not in st.session_state:
    st.session_state.eraser_on = False

CROSSWORD_DATA = {
    "THROWBALL": {"clue": "A sport you swear you played in college", "num": "1", "direction": "across", "row": 0, "col": 0},
    "GRAVEYARD": {"clue": "Where our longest conversations strangely happen", "num": "2", "direction": "down", "row": 0, "col": 0},
    "VIEWPOINT": {"clue": "Where the sky did something unforgettable for the first time", "num": "3", "direction": "across", "row": 2, "col": 0},
    "TIRAMISU": {"clue": "A dessert you never really say no to", "num": "4", "direction": "down", "row": 2, "col": 5},
    "CALIFORNIABURRITO": {"clue": "The place your fatass is always ready to eat at w/o a second thought", "num": "5", "direction": "across", "row": 4, "col": 0},
    "TRAIN": {"clue": "Where a story begins when someone decides not to go home(answer is in one of your fav movies)", "num": "6 (Anchor)", "direction": "down", "row": 4, "col": 0},
}

if "cw_answers" not in st.session_state:
    st.session_state.cw_answers = {word: "" for word in CROSSWORD_DATA}

# -------------------------------
# SHARED STYLES
# -------------------------------
st.markdown("""
<style>
.block-container { display: flex; flex-direction: column; align-items: center; }
.wordle-container { display: flex; flex-direction: column; align-items: center; width: 100%; margin-bottom: 20px;}
.wordle-row { display: flex !important; justify-content: center !important; gap: 10px; margin-bottom: 10px; }
.wordle-box {
    width: 60px; height: 60px; border: 2px solid #3a3a3c;
    display: flex; align-items: center; justify-content: center;
    font-size: 30px; font-weight: bold; color: white; text-transform: uppercase;
}
.correct { background-color: #538d4e; border: none; }
.present { background-color: #b59f3b; border: none; }
.absent  { background-color: #3a3a3c; border: none; }
.empty   { background-color: transparent; }
</style>
""", unsafe_allow_html=True)

# -------------------------------
# PHASE 1: WORDLE
# -------------------------------
if st.session_state.phase == "wordle":
    st.markdown("<h1 style='text-align: center;'>Let's start with a small game 🧩</h1>", unsafe_allow_html=True)
    WORD = "MAGIC"
    
    st.markdown("<div class='wordle-container'>", unsafe_allow_html=True)
    for g_word, colors in st.session_state.guesses:
        row_html = "<div class='wordle-row'>"
        for i, char in enumerate(g_word):
            row_html += f"<div class='wordle-box {colors[i]}'>{char}</div>"
        st.markdown(row_html + "</div>", unsafe_allow_html=True)
    for _ in range(6 - len(st.session_state.guesses)):
        st.markdown("<div class='wordle-row'>" + "".join(["<div class='wordle-box empty'></div>"]*5) + "</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.wordle_done:
        won = any(g[0] == WORD for g in st.session_state.guesses)
        if won: st.success(f"Perfect! The word was {WORD}. My smartie got itttttttt")
        else: st.error(f"Game Over! The word was {WORD}.Its okieeee cutuuuu")
        
        if st.button("Continue to Canvas ✨", use_container_width=True, type="primary"):
            st.session_state.phase = "canvas"
            st.rerun()
    else:
        with st.form("wordle_input", clear_on_submit=True):
            guess = st.text_input("Guess", max_chars=5, label_visibility="collapsed", placeholder="GUESS").upper()
            if st.form_submit_button("Submit", use_container_width=True) and len(guess) == 5:
                results = ["correct" if c == WORD[i] else "present" if c in WORD else "absent" for i, c in enumerate(guess)]
                st.session_state.guesses.append((guess, results))
                if guess == WORD or len(st.session_state.guesses) >= 6: st.session_state.wordle_done = True
                st.rerun()

# -------------------------------
# PHASE 2: CANVAS
# -------------------------------
elif st.session_state.phase == "canvas":
    st.markdown("<h1 style='text-align: center;'>Draw something for me ✨</h1>", unsafe_allow_html=True)
    with st.sidebar:
        st.header("🎨 Tools")
        st.session_state.pen_color = st.color_picker("Color", st.session_state.pen_color)
        st.session_state.brush_size = st.slider("Size", 1, 50, st.session_state.brush_size)
        st.session_state.eraser_on = st.checkbox("🧽 Eraser")
        if st.button("Clear Canvas"): st.rerun()

    col1, col2, col3 = st.columns([1, 10, 1])
    with col2:
        canvas_result = st_canvas(
            stroke_width=st.session_state.brush_size,
            stroke_color="#111111" if st.session_state.eraser_on else st.session_state.pen_color,
            background_color="#111111",
            height=500, width=900, key="canvas_main"
        )
        if st.button("Save & Continue to MEMORY BOXXX", use_container_width=True, type="primary"):
            if canvas_result and canvas_result.image_data is not None:
                img = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA')
                buf = io.BytesIO()
                img.save(buf, format="PNG")
                st.session_state.final_img = buf.getvalue()
                st.session_state.phase = "crossword"
                st.rerun()
            else:
                st.warning("Please draw something first before saving!")

# -------------------------------
# PHASE 3: THE MEMORY BOX (CUTE VERSION)
# -------------------------------
elif st.session_state.phase == "crossword":
    # Custom CSS for the "Cute" vibe
    st.markdown("""
        <style>
        .memory-card {
            background: #fff0f6;
            padding: 20px;
            border-radius: 20px;
            border: 2px dashed #ffadad;
            margin-bottom: 20px;
            box-shadow: 5px 5px 15px rgba(0,0,0,0.05);
        }
        .memory-title {
            color: #ff4d6d;
            font-family: 'Comic Sans MS', cursive, sans-serif;
            font-size: 1.5rem;
            margin-bottom: 10px;
        }
        .stTextInput input {
            border-radius: 15px !important;
            border: 2px solid #ffccd5 !important;
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 style='text-align: center; color: #ff4d6d;'>Our Little Secret Journal 🌸</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #ff758f;'>Can you remember these tiny moments? ✨</p>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        all_correct = True
        total_memories = len(CROSSWORD_DATA)
        correct_count = 0

        for word, data in CROSSWORD_DATA.items():
            # Check if this specific answer is already correct
            is_correct = st.session_state.cw_answers.get(word, "").upper() == word.upper()
            
            # Memory Card Container
            st.markdown(f"""
                <div class="memory-card">
                    <div class="memory-title">💌 Memory #{data['num'].split()[0]}</div>
                    <p style="color: #594e52; font-size: 1.1rem;">{data['clue']}</p>
                </div>
            """, unsafe_allow_html=True)

            # Input field
            val = st.text_input(
                "Guess the word...", 
                value=st.session_state.cw_answers.get(word, ""),
                key=f"input_{word}",
                label_visibility="collapsed",
                placeholder="Type the magic word here..."
            ).strip().upper().replace(" ", "")

            st.session_state.cw_answers[word] = val

            if val == word:
                st.markdown("<p style='color: #ff4d6d; text-align: center; font-weight: bold;'>You got it! 🥰</p>", unsafe_allow_html=True)
                correct_count += 1
            elif val != "":
                st.markdown("<p style='color: #ffb3c1; text-align: center; font-size: 0.8rem;'>Not quite, my love! Try again? 🌸</p>", unsafe_allow_html=True)
                all_correct = False
            else:
                all_correct = False
            
            st.markdown("<br>", unsafe_allow_html=True)

        # Progress bar but make it cute
        progress = correct_count / total_memories
        st.write(f"<p style='text-align: center; color: #ff4d6d;'>{correct_count} of {total_memories} memories found ☁️</p>", unsafe_allow_html=True)
        st.progress(progress)

        if all_correct:
            st.snow() # Fun visual effect!
            st.markdown("<h3 style='text-align: center; color: #ff4d6d;'>Yay! You remembered everything! 💖</h3>", unsafe_allow_html=True)
            if st.button("See My Final Surprise 🎁", use_container_width=True, type="primary"):
                st.session_state.phase = "finale"
                st.rerun()

# -------------------------------
# PHASE 4: FINALE
# -------------------------------
else:
    st.balloons()
    
    # Import the new font 'Caveat' and 'Satisfy' for the signature
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Caveat:wght@400;700&family=Satisfy&display=swap');

    .letter-bg {
        background: #fdf0f4;
        padding: 30px;
        border-radius: 30px;
        display: flex;
        justify-content: center;
    }

    .letter-paper {
        background: white;
        padding: 40px;
        width: 90%;
        max-width: 700px;
        border-radius: 5px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        font-family: 'Caveat', cursive;
        font-size: 28px; /* Slightly larger for the new font */
        line-height: 1.4;
        color: #444;
        border-left: 35px solid #ffdde1;
        position: relative;
    }

    .quote-box {
        font-family: 'Caveat', cursive;
        color: #ff4d6d;
        font-weight: 700;
        padding: 20px 0;
        text-align: center;
        font-size: 30px;
    }

    .signature {
        text-align: right;
        font-family: 'Satisfy', cursive;
        font-size: 35px;
        color: #ff4d6d;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

    # The Letter - Note: No indentation here to prevent "code block" rendering
    st.markdown(f"""
<div class="letter-bg">
<div class="letter-paper">
Happiest Birthday to you Shraddhaaaaaa😘. <br><br>
You're 21 now huh. One oldie only bro you are, but a very pretty oldie. 
I feel blessed to have known you for a year almost (kinda jealous of your childhood buddies). <br><br>
You're super fun, amazing and kind babe and the energy you give off is very homely. 
Every moment with you feels so effortlessly nice but the only drawback is:
<div class="quote-box">
" Aapke saath hone par waqt aise guzarta hain maanon waqt ko hi kahi waqt se pehle pahochna ho "
</div>
You make me feel safe and I'm sure you make all of those around you feel safe. 
You are a very special girl shraddha 💗💗 and I'm lucky to have you. <br><br>
I hope by the time your next birthday comes you achieve everything you've ever wanted 
and this year be one of the most fun ones ever.
<div class="signature">
With love,<br>
Sachin
</div>
</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("<h2 style='text-align: center; color: #ff4d6d; margin-top: 50px;'>Hope you liked it 💖</h2>", unsafe_allow_html=True)
    
    col_f1, col_f2, col_f3 = st.columns([1, 2, 1])
    with col_f2:
        if "final_img" in st.session_state:
            st.image(st.session_state.final_img, caption="Your Artwork", use_container_width=True)
            st.download_button("Download Your Drawing", st.session_state.final_img, "us.png", "image/png", use_container_width=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Play Again", use_container_width=True):
            st.session_state.clear()
            st.rerun()









