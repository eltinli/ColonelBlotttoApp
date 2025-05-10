import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Initialize session state for storing submissions
if 'submissions' not in st.session_state:
    st.session_state.submissions = []

st.set_page_config(page_title="Colonel Blotto", layout="centered")
st.title("🪖 Colonel Blotto Game: 3 Bases, 30 Troops")

st.markdown("""
Welcome, Commander! You have **30 troops** to allocate across **3 battlefields**.
Your goal: Win more battlefields than your opponents. Choose wisely! 🧠⚔️
""")

name = st.text_input("🎖️ Enter your name or alias:")

st.markdown("### 📦 Allocate your troops below")
alloc = [0, 0, 0]
cols = st.columns(3)
for i in range(3):
    with cols[i]:
        st.markdown(f"#### 🏰 Base {i+1}")
        alloc[i] = st.slider("", min_value=0, max_value=30, step=1, key=f"base_{i+1}")

# Total check
total = sum(alloc)
st.metric("Total Troops Allocated", total, delta=total - 30)

if st.button("🚀 Submit Strategy"):
    if total != 30:
        st.error("❌ Total troops must equal 30.")
    elif name.strip() == "":
        st.error("❌ Please enter your name.")
    else:
        st.session_state.submissions.append({'name': name, 'allocation': alloc})
        st.success("✅ Strategy submitted!")
        # Show chart
        st.markdown("#### 📊 Your Allocation")
        fig, ax = plt.subplots()
        ax.bar([f"Base {i+1}" for i in range(3)], alloc, color="skyblue")
        ax.set_ylabel("Troops")
        ax.set_ylim(0, max(alloc) + 5)
        st.pyplot(fig)

# Show all submissions
if st.checkbox("📋 Show all submissions"):
    df = pd.DataFrame(st.session_state.submissions)
    st.dataframe(df)

# Matchup simulator
st.markdown("---")
st.header("⚔️ Simulate Head-to-Head Matchups")

def simulate_match(a, b):
    wins_a = sum([1 for i in range(3) if a[i] > b[i]])
    wins_b = sum([1 for i in range(3) if a[i] < b[i]])
    if wins_a > wins_b:
        return "A"
    elif wins_b > wins_a:
        return "B"
    else:
        return "Draw"

if st.button("🏁 Run All Matchups") and len(st.session_state.submissions) > 1:
    st.subheader("📈 Results")
    results = []
    subs = st.session_state.submissions
    for i in range(len(subs)):
        for j in range(i+1, len(subs)):
            p1 = subs[i]
            p2 = subs[j]
            outcome = simulate_match(p1['allocation'], p2['allocation'])
            winner = p1['name'] if outcome == "A" else p2['name'] if outcome == "B" else "Draw"
            results.append({
                'Matchup': f"{p1['name']} vs {p2['name']}",
                'Winner': winner
            })
    st.dataframe(pd.DataFrame(results))
