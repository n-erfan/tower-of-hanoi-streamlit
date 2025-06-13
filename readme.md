# Tower of Hanoi – Streamlit Edition

A fully playable, interactive Tower of Hanoi game built with [Streamlit](https://streamlit.io/).

![Deploy to Streamlit Cloud](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)

## Features

- **Configurable:** Choose number of towers (3–5), disks (3–10), stack order, and UI options.
- **Animated Board:** Visual rods and pastel disks, smoothly redrawn after each move.
- **Drag-and-Drop Style:** Select a rod to pick up a disk, then select a rod to place.
- **Rules Enforced:** Only legal moves allowed, with feedback on illegal attempts.
- **Timer & Move Counter:** Optionally shown; timer starts on first move, stops on completion.
- **Restart & New Game:** Restart with same settings or return to config screen anytime.
- **Victory Feedback:** “Congratulations!” banner with stats on completion.
- **Deployable:** One-click deploy to Streamlit Cloud.

## Setup

1. **Clone the repository:**
    ```
    git clone https://github.com/yourusername/tower-of-hanoi-streamlit.git
    cd tower-of-hanoi-streamlit
    ```

2. **Install dependencies:**
    ```
    pip install -r requirements.txt
    ```

3. **Run the app:**
    ```
    streamlit run app.py
    ```

## Deployment

To deploy on Streamlit Community Cloud:

- Push your code to GitHub.
- Go to [Streamlit Cloud](https://share.streamlit.io/).
- Click **Create app** and select your repo and `app.py` entrypoint.
- Done!

Or use the badge above for one-click deployment.

---

Enjoy solving the Tower of Hanoi in style!
