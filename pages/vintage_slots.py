import random
import streamlit as st

st.set_page_config(page_title="Casino Game", page_icon="🎰")

with st.sidebar.expander("Welcome!"):
    st.page_link("app.py", label="Intorduction")
    
with st.sidebar.expander("📊 Instagram Analyzer"):
    st.page_link("pages/SeeWhoDoesntFollowYou.py", label="Home Page")

with st.sidebar.expander("🤖 Flashcard Automation Tool"):
    st.page_link("pages/FlashcardAutomation.py", label="Home Page")
    
with st.sidebar.expander("🎰 Casino"):
    st.page_link("pages/Casino.py", label="Home Page")

# Slot machine symbols
reels_vintage = [
    ["🍒", "🍋", "🍊", "🍇", "🔔", "💰", "7️⃣"],  # Reel 1
    ["7️⃣", "💰", "🍒", "🍋", "🍊", "🍇", "🔔"],  # Reel 2
    ["🍇", "🔔", "💰", "7️⃣", "🍒", "🍊", "🍋"],  # Reel 3
]

# Initialize session state variables if they don't exist
if "balance" not in st.session_state:
    st.session_state.balance = 100  # Default balance
if "bet_multiplier" not in st.session_state:
    st.session_state.bet_multiplier = "1X"  # Default multiplier
if "bet_amount" not in st.session_state:
    st.session_state.bet_amount = 1 * int(st.session_state.bet_multiplier[0])  # Calculate bet amount
if "reels" not in st.session_state:
    st.session_state.reels = [["⬜" for _ in range(3)] for _ in range(3)]  # Empty placeholders
if "win_message" not in st.session_state:
    st.session_state.win_message = ""
if "win_amount" not in st.session_state:
    st.session_state.win_amount = 0

# Function to reset balance
def reset_balance():
    st.session_state.balance = 100
    st.session_state.reels = [["⬜" for _ in range(3)] for _ in range(3)]  # Reset reels
    st.session_state.win_message = ""
    st.session_state.win_amount = 0
    st.rerun()  # Force UI update

# Function to generate a random 3x3 slot result
def spin_reels():
    if st.session_state.balance < st.session_state.bet_amount:
        st.warning("⚠️ Not enough balance to spin!")
        return  # Stop function if balance is too low

    # Deduct bet from balance
    st.session_state.balance -= st.session_state.bet_amount

    middle_row = []
    above_row = []
    below_row = []

    for reel in reels_vintage:
        spin_position = random.randint(0, len(reel) - 1)
        middle_row.append(reel[spin_position])

        above_position = (spin_position - 1) % len(reel)
        below_position = (spin_position + 1) % len(reel)

        above_row.append(reel[above_position])
        below_row.append(reel[below_position])

    # Count money bag symbols
    moneybag_count = middle_row.count("💰")

    # Payouts adjusted for 97.5% RTP
    payout_grand = 200
    payout_major = 8
    payout_minor = 1.5
    payout_mini = 0.5

    # Reset win message and win amount
    st.session_state.win_message = ""
    st.session_state.win_amount = 0

    # Winning Conditions
    if middle_row[0] == middle_row[1] == middle_row[2]:  # 3 of a kind
        if middle_row[0] == "💰":
            win_amount = payout_grand * int(st.session_state.bet_multiplier[0])
            st.session_state.balance += win_amount
            st.session_state.win_message = f"🎰 GRAND JACKPOT! 3 Moneybags! 🤑 +${win_amount}"
            st.session_state.win_amount = win_amount
        else:
            win_amount = payout_major * int(st.session_state.bet_multiplier[0])
            st.session_state.balance += win_amount
            st.session_state.win_message = f"🎉 MAJOR JACKPOT! 3 of a Kind! +${win_amount}"
            st.session_state.win_amount = win_amount
    elif moneybag_count == 2:  # Minor Jackpot
        win_amount = payout_minor * int(st.session_state.bet_multiplier[0])
        st.session_state.balance += win_amount
        st.session_state.win_message = f"💸 MINOR JACKPOT! 2 Moneybags! +${win_amount}"
        st.session_state.win_amount = win_amount
    elif moneybag_count == 1:  # Mini Jackpot
        win_amount = payout_mini * int(st.session_state.bet_multiplier[0])
        st.session_state.balance += win_amount
        st.session_state.win_message = f"💵 MINI JACKPOT! 1 Moneybag! +${win_amount}"
        st.session_state.win_amount = win_amount
    
    # Update the reels in session state
    st.session_state.reels = [above_row, middle_row, below_row]
    st.rerun()  # ✅ Forces UI to update immediately!

# Streamlit UI
st.title("🎰 Slot Machine")

# Display balance & reset button
col1, col2 = st.columns([1, 1])
with col1:
    st.metric("Balance", f"${st.session_state.balance}")
with col2:
    if st.button("🔄 Reset Balance"):
        reset_balance()

# CSS for Red Line Through Middle Row
st.markdown("""
    <style>
        .slot-container {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-top: 30px;
        }
        .slot-table {
            border-spacing: 10px;
            margin: auto;
            width: 400px;
        }
        .slot-cell {
            font-size: 80px;
            font-weight: bold;
            text-align: center;
            background: black;
            color: white;
            border: 5px solid gold;
            width: 120px;
            height: 120px;
            position: relative;
        }
        /* Horizontal red line inside the middle row */
        .middle-row {
            position: relative;
        }
        .middle-row::after {
            content: "";
            position: absolute;
            left: 0%;
            width: 100%;
            height: 5px;
            background-color: red;
            top: 50%;
            transform: translateY(-50%);
            z-index: 2;
        }
    </style>
""", unsafe_allow_html=True)

# Rebuild the slot machine grid dynamically based on `st.session_state.reels`
html_code = """
<div class='slot-container'>
    <table class='slot-table'>
        <tr>
            <td class='slot-cell'>{}</td>
            <td class='slot-cell'>{}</td>
            <td class='slot-cell'>{}</td>
        </tr>
        <tr class='middle-row'>
            <td class='slot-cell'>{}</td>
            <td class='slot-cell'>{}</td>
            <td class='slot-cell'>{}</td>
        </tr>
        <tr>
            <td class='slot-cell'>{}</td>
            <td class='slot-cell'>{}</td>
            <td class='slot-cell'>{}</td>
        </tr>
    </table>
</div>
""".format(*st.session_state.reels[0], *st.session_state.reels[1], *st.session_state.reels[2])

# Display win message below slot machine
temp_message = st.session_state.win_message

# Display Slot Machine
st.markdown(html_code, unsafe_allow_html=True)

if temp_message:
    st.success(temp_message)

# Betting & Spin Controls
col1, col2, col3 = st.columns(3)

multipliers = ['1X', '2X', '3X', '4X', '5X']
with col1:
    st.session_state.bet_multiplier = st.selectbox("Change bet multiplier", options=multipliers, index=multipliers.index(st.session_state.bet_multiplier))
    st.session_state.bet_amount = int(st.session_state.bet_multiplier[0])  # Update bet amount dynamically
with col2:
    if st.button("🎲 Spin Now"):
        spin_reels()
with col3:
    speed_multiplier = st.selectbox("Change speed multiplier", options=multipliers, index=0)

st.page_link("pages/Casino.py", label="Go Back")
