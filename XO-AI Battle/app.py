import streamlit as st
import math
import random
import time

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="❌⭕- AI Battle", layout="centered")

st.title("❌⭕- AI Battle")
st.caption("❌ You VS⭕ AI")

# -----------------------------
# SESSION STATE INIT
# -----------------------------
def init_state():
    if "board" not in st.session_state:
        st.session_state.board = [" " for _ in range(9)]

    if "score" not in st.session_state:
        st.session_state.score = {"You": 0, "AI": 0, "Draw": 0}

    if "game_over" not in st.session_state:
        st.session_state.game_over = False

init_state()

board = st.session_state.board
score = st.session_state.score

# -----------------------------
# GAME LOGIC
# -----------------------------
def check_winner(b):
    wins = [
        (0,1,2),(3,4,5),(6,7,8),
        (0,3,6),(1,4,7),(2,5,8),
        (0,4,8),(2,4,6)
    ]
    for a,b1,c in wins:
        if b[a] == b[b1] == b[c] != " ":
            return b[a]
    return None

def is_draw(b):
    return " " not in b and check_winner(b) is None

# -----------------------------
# DIFFICULTY
# -----------------------------
difficulty = st.selectbox("🧠 Difficulty", ["Easy", "Medium", "Hard"])

def depth_limit():
    if difficulty == "Easy":
        return 1
    elif difficulty == "Medium":
        return 3
    else:
        return 9

# -----------------------------
# MINIMAX
# -----------------------------
def minimax(b, is_max, depth, max_depth):
    winner = check_winner(b)

    if winner == "O":
        return 10 - depth
    if winner == "X":
        return depth - 10
    if is_draw(b):
        return 0
    if depth >= max_depth:
        return 0

    if is_max:
        best = -math.inf
        for i in range(9):
            if b[i] == " ":
                b[i] = "O"
                best = max(best, minimax(b, False, depth+1, max_depth))
                b[i] = " "
        return best
    else:
        best = math.inf
        for i in range(9):
            if b[i] == " ":
                b[i] = "X"
                best = min(best, minimax(b, True, depth+1, max_depth))
                b[i] = " "
        return best

# -----------------------------
# AI MOVE
# -----------------------------
def best_move(b):
    best_score = -math.inf
    move = None

    for i in range(9):
        if b[i] == " ":
            b[i] = "O"
            score_val = minimax(b, False, 0, depth_limit())
            b[i] = " "

            # Easy randomness
            if difficulty == "Easy":
                score_val += random.randint(-2, 2)

            if score_val > best_score:
                best_score = score_val
                move = i

    return move

def ai_turn():
    time.sleep(0.2)
    move = best_move(board)
    if move is not None:
        board[move] = "O"

# -----------------------------
# SCORE UPDATE (FIXED)
# -----------------------------
def update_score_once():
    if st.session_state.game_over:
        return

    winner = check_winner(board)

    if winner == "X":
        score["You"] += 1
        st.success("🏆 You Win!")
    elif winner == "O":
        score["AI"] += 1
        st.error("🤖 AI Wins!")
    elif is_draw(board):
        score["Draw"] += 1
        st.warning("🤝 Draw!")

    st.session_state.game_over = True

# -----------------------------
# RESET GAME
# -----------------------------
def reset_board():
    st.session_state.board = [" " for _ in range(9)]
    st.session_state.game_over = False
    st.rerun()

if st.button("🔄 New Game"):
    reset_board()

# -----------------------------
# SCOREBOARD
# -----------------------------
st.divider()

col1, col2, col3 = st.columns(3)
col1.metric("You ❌", score["You"])
col2.metric("AI ⭕", score["AI"])
col3.metric("Draw 🤝", score["Draw"])

st.divider()

# -----------------------------
# GAME END CHECK
# -----------------------------
if not st.session_state.game_over:
    winner = check_winner(board)

    if winner or is_draw(board):
        update_score_once()

# -----------------------------
# BOARD UI
# -----------------------------
for i in range(3):
    cols = st.columns(3)

    for j in range(3):
        idx = i*3 + j

        with cols[j]:

            cell = board[idx]

            if cell != " ":
                st.markdown(f"## {'❌' if cell=='X' else '⭕'}")
            else:
                if not st.session_state.game_over:
                    if st.button("➕", key=idx, use_container_width=True):
                        board[idx] = "X"

                        if not check_winner(board):
                            ai_turn()

                        st.rerun()
                else:
                    st.button(" ", disabled=True, key="d"+str(idx))