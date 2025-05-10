## Project Documentation: Colonel Blotto Streamlit App

This project implements a one-shot Colonel Blotto game using Streamlit and deploys it to Streamlit Cloud for interactive classroom use. Players allocate 30 troops across 3 battlefields. An admin panel allows for secure monitoring, matchup analysis, and scorekeeping.

---

###  Step-by-Step Overview

**1. Build the App Logic (`blotto_streamlit_app.py`)**
- Players enter their name and allocate **30 troops across 3 bases**
- Input validated (must sum to 30)
- Submissions saved to a local `submissions.csv`
- Visual feedback via bar chart
- Admin-only panel:
  - View all submissions
  - Run round-robin matchups
  - Tally wins and declare a champion
  - Clear all submissions
- Admin access is protected by a hidden password field

---

**2. Test Locally (Optional)**
```bash
streamlit run blotto_streamlit_app.py
```

---

**3. Upload to GitHub**
- Create a new public repository
- Upload `blotto_streamlit_app.py`
- (Optional) Add `.gitignore` to exclude `submissions.csv` from being tracked

---

**4. Deploy on Streamlit Cloud**
- Go to [https://streamlit.io/cloud](https://streamlit.io/cloud)
- Log in via GitHub
- Click **"New app"**
- Select the GitHub repo and `blotto_streamlit_app.py`
- Click **Deploy**
- App is hosted at a public URL, e.g.:
  ```
  https://your-app-name.streamlit.app
  ```

---

**5. Share with Classmates**
- Generate a QR code using: [https://www.qr-code-generator.com](https://www.qr-code-generator.com)
- Students scan the QR code to access and submit their allocations

---

**6. Admin Panel Capabilities**
- Login via password (hidden)
- View full submission list
- Run all pairwise matchups (round-robin)
- Display match results and base-by-base outcomes
- Count wins and declare the top-scoring player as **Champion**
- Clear all submissions with one click

---

### 🔧 Tools Used

| Component      | Tool/Platform                 |
|----------------|-------------------------------|
| Frontend       | Streamlit                     |
| Backend Logic  | Python                        |
| Hosting        | Streamlit Cloud               |
| Data Storage   | Local CSV (`submissions.csv`) |
| Version Control| GitHub                        |
| QR Sharing     | Online QR code generator      |

---

This app serves as an educational tool to introduce game theory, mixed strategies, and Nash equilibrium through hands-on experimentation and live competition.
