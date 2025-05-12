import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Colonel Blotto Game", page_icon="🪖")

st.title("LG's Colonel Blotto Game")
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

if admin_pass == "aim2025":  # Change this to your real password
    st.success("🔓 Admin access granted")

    # Option to clear all submissions
    if st.button("🗑️ Clear all submissions"):
        pd.DataFrame(columns=["Name", "Base1", "Base2", "Base3"]).to_csv(data_file, index=False)
        st.success("✅ All submissions cleared.")

    submissions = pd.read_csv(data_file)

    # Sanitize and convert data types
    submissions["Name"] = submissions["Name"].astype(str).str.strip()
    for col in ["Base1", "Base2", "Base3"]:
        submissions[col] = pd.to_numeric(submissions[col], errors="coerce").fillna(0).astype(int)

    st.markdown("### 🗂️ All Submissions")
    st.dataframe(submissions)

    st.markdown("### ⚔️ Round-Robin Matchups")

    def run_matchup(row1, row2):
        wins1 = wins2 = 0
        results = []

        for i in range(1, 4):
            base1 = row1[f"Base{i}"]
            base2 = row2[f"Base{i}"]
            if base1 > base2:
                results.append("1")
                wins1 += 1
            elif base2 > base1:
                results.append("2")
                wins2 += 1
            else:
                results.append("D")

        if wins1 > wins2:
            winner = row1["Name"]
        elif wins2 > wins1:
            winner = row2["Name"]
        else:
            winner = "Draw"

        return {
            "Player 1": row1["Name"],
            "Player 2": row2["Name"],
            "Allocations": f"{row1['Base1']}-{row1['Base2']}-{row1['Base3']} vs {row2['Base1']}-{row2['Base2']}-{row2['Base3']}",
            "Base Results": results,
            "Winner": winner
        }

    results = []
    win_count = {}

    for i in range(len(submissions)):
        for j in range(i + 1, len(submissions)):
            row1 = submissions.iloc[i]
            row2 = submissions.iloc[j]

            result = run_matchup(row1, row2)
            results.append(result)

            winner = result["Winner"].strip()
            if winner != "Draw":
                win_count[winner] = win_count.get(winner, 0) + 1

    if results:
        st.markdown("#### 🧾 Match Results")
        for r in results:
            st.markdown(f"- **{r['Player 1']}** vs **{r['Player 2']}** ➜ ⚔️ Winner: **{r['Winner']}**")
            st.caption(f"Allocations: {r['Allocations']} | Base Wins: {r['Base Results']}")

        st.markdown("### 🏅 Final Tally")
        scores_df = pd.DataFrame(list(win_count.items()), columns=["Player", "Wins"]).sort_values(by="Wins", ascending=False)
        st.dataframe(scores_df)

        if not scores_df.empty:
            max_wins = scores_df["Wins"].max()
            champions_df = scores_df[scores_df["Wins"] == max_wins]

            if len(champions_df) == 1:
                champion_name = champions_df.iloc[0]["Player"]
                st.success(f"👑 **Champion:** {champion_name} ({max_wins} wins)")
            else:
                st.success("🤝 **Co-Champions:**")
                for _, row in champions_df.iterrows():
                    st.markdown(f"- 👑 **{row['Player']}** with **{row['Wins']} wins**")
    else:
        st.info("Not enough submissions to run matchups.")
else:
    st.info("Admin features hidden. Enter password to access.")
