import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Colonel Blotto Game", page_icon="🪖")

st.title("🎖️ Colonel Blotto Game")
st.markdown("Allocate exactly **30 troops** across **3 bases**. Highest troop wins a base.")

# --- Submission Handling Setup ---
data_file = "submissions.csv"

# Initialize submissions file if not present
if not os.path.exists(data_file):
    pd.DataFrame(columns=["Name", "Base1", "Base2", "Base3"]).to_csv(data_file, index=False)

# --- Player Input ---
name = st.text_input("Enter your name or alias")

st.subheader("🔢 Troop Allocation")

b1 = st.number_input("Base 1", min_value=0, max_value=30, step=1, value=10, key="base1")
b2 = st.number_input("Base 2", min_value=0, max_value=30, step=1, value=10, key="base2")
b3 = st.number_input("Base 3", min_value=0, max_value=30, step=1, value=10, key="base3")

total = b1 + b2 + b3
st.markdown(f"**Total Allocated:** {total}/30")

# Submit button
if total != 30:
    st.warning("⚠️ Total must be exactly 30.")
else:
    if st.button("✅ Submit Allocation"):
        if name.strip() == "":
            st.error("Please enter a name before submitting.")
        else:
            new_row = pd.DataFrame([[name.strip(), b1, b2, b3]], columns=["Name", "Base1", "Base2", "Base3"])
            old_data = pd.read_csv(data_file)
            updated_data = pd.concat([old_data, new_row], ignore_index=True)
            updated_data.to_csv(data_file, index=False)

            st.success("🎯 Strategy submitted successfully!")
            st.bar_chart([b1, b2, b3])

# --- Admin Controls ---
st.divider()
st.subheader("🔐 Admin Login")
admin_pass = st.text_input("Enter admin password to unlock controls", type="password")

if admin_pass == "mysecretpassword":  # Change this to your real password
    st.success("🔓 Admin access granted")

    # Option to clear all submissions
    if st.button("🗑️ Clear all submissions"):
        pd.DataFrame(columns=["Name", "Base1", "Base2", "Base3"]).to_csv(data_file, index=False)
        st.success("✅ All submissions cleared.")

    submissions = pd.read_csv(data_file)
    st.markdown("### 🗂️ All Submissions")
    st.dataframe(submissions)

    st.markdown("### ⚔️ Run All Matchups")

    def run_matchup(row1, row2):
        wins1 = wins2 = 0
        for i in range(1, 4):
            if row1[f"Base{i}"] > row2[f"Base{i}"]:
                wins1 += 1
            elif row1[f"Base{i}"] < row2[f"Base{i}"]:
                wins2 += 1
        if wins1 > wins2:
            return row1["Name"]
        elif wins2 > wins1:
            return row2["Name"]
        else:
            return "Draw"

    results = []
    for i in range(len(submissions)):
        for j in range(i + 1, len(submissions)):
            p1 = submissions.iloc[i]
            p2 = submissions.iloc[j]
            result = run_matchup(p1, p2)
            results.append(f"{p1['Name']} vs {p2['Name']} ➜ Winner: {result}")

    if results:
        st.markdown("#### Matchup Results")
        for r in results:
            st.write(r)
    else:
        st.info("Not enough submissions to run matchups.")
else:
    st.info("Admin features hidden. Enter password to access.")
