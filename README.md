# 🎬 RedGifs to Reddit Poster

A Streamlit-powered web dashboard that lets you submit RedGifs links, tag them with metadata, and post them to selected subreddits using PRAW (Python Reddit API Wrapper).

!["Screenshot"](https://github.com/juicesrus/redgifs_to_reddit/blob/main/images/screenshot.png?raw=true)

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/juicesrus)


---

## 🚀 Features

- Paste **RedGifs URLs**
- Add titles, tags, and select subreddits
- Post links to Reddit via PRAW
- Track which subreddits you've posted to
- Manage entries with delete and clear functionality

---

## 🧰 Requirements

- Python 3.10+
- pip (Python package manager)
- Streamlit
- PRAW

---

## 💻 Installation Instructions

> Choose your platform below. These instructions assume **Python is NOT installed**.

---

### Subreddit list

You will need to put the subreddits you wish to post to in ```subs.txt``` which looks like: 

```
r/funny
r/aww
r/test
```

### PRAW credentials

You will need a Reddit API key as well as your username and password.  You can optain the client id and client secret key from Reddit by logging in and visiting https://www.reddit.com/prefs/apps and creating an application. You should put these in the ```praw.ini``` file which is included with this repo:

```
; this is your 14 character personal use script
client_id=
; this is your 27 character secret
client_secret=
; this is the name you gave your application
user_agent=bot1
; this is username for the reddit account the app was created with
username=
; password for the account
password=
```

### 🪟 Windows

1. Download Python from: [https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/)
2. Run the installer and make sure to:
   - ✅ Check **“Add Python to PATH”** during setup
3. Open Command Prompt (`Win + R`, type `cmd`, hit Enter)
4. Install dependencies:
   ```sh
   pip install streamlit praw

## 🍎 macOS installation

### ✅ Step 1: Install Homebrew (if not already installed)

Open Terminal and run:

```sh
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Install dependencies:
```
pip3 install streamlit praw
```

## Linux installation

From within a terminal:

```
sudo apt update
sudo apt install python3 python3-pip -y
```

### Install dependencies:
```
pip3 install streamlit praw
```

## Running the app

Within the folder run:

```
streamlit run ui.py
```

