import streamlit as st
import json
import re
import subprocess
from pathlib import Path
import praw

# Initialize Reddit instance using the 'bot1' section of praw.ini
reddit = praw.Reddit("bot1")
import time

# Get subreddit subscriber counts
def get_subreddit_stats(subs):
    stats = []
    for sub in subs:
        try:
            subreddit = reddit.subreddit(sub)
            stats.append((sub, subreddit.subscribers))
        except Exception as e:
            stats.append((sub, 0))  # Fallback if subreddit doesn't exist or fails
    return sorted(stats, key=lambda x: x[1], reverse=True)

STATUS_FILE = "upload_status.json"

sub_file = open("subs.txt", 'r')

SUBREDDITS = [u.strip().replace('r/', '') for u in sub_file.readlines()]

# Load/save metadata
def load_status():
    if Path(STATUS_FILE).exists():
        with open(STATUS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_status(data):
    with open(STATUS_FILE, "w") as f:
        json.dump(data, f, indent=2)

# Streamlit UI
st.title("📤 RedGifs to Reddit Poster")

st.markdown("---")
st.markdown("## 📊 Subreddit Popularity")

with st.spinner("Fetching subreddit data..."):
    subreddit_stats = get_subreddit_stats(SUBREDDITS)

if subreddit_stats:
    for i, (sub, count) in enumerate(subreddit_stats, start=1):
        st.write(f"**{i}. r/{sub}** — 👥 {count:,} subscribers")
else:
    st.info("No subreddit data available.")

status_data = load_status()

# Initialize session state
if "redgifs_url" not in st.session_state:
    st.session_state["redgifs_url"] = ""
if "title" not in st.session_state:
    st.session_state["title"] = ""
if "selected_subreddits" not in st.session_state:
    st.session_state["selected_subreddits"] = []

def clear_form():
    st.session_state["redgifs_url"] = ""
    st.session_state["title"] = ""
    st.session_state["selected_subreddits"] = []

st.markdown("## ➕ Add New RedGifs Link")

with st.form("add_redgifs"):
    redgifs_url = st.text_input("🔗 RedGifs URL", key="redgifs_url")
    title = st.text_input("🎯 Title / Description", key="title")
    selected_subreddits = st.multiselect("📬 Choose Subreddits", SUBREDDITS, key="selected_subreddits")
    
    col1, col2 = st.columns(2)
    submit = col1.form_submit_button("✅ Save Link")

    if submit:
        if not re.match(r"https://www\.redgifs\.com/watch/\S+", redgifs_url):
            st.error("Please enter a valid RedGifs URL.")
        else:
            key = redgifs_url.split("/")[-1]
            status_data[key] = {
                "url": redgifs_url,
                "title": title,
                "subreddits": selected_subreddits,
                "reddit_posts": {}
            }
            save_status(status_data)
            st.success("✅ RedGifs link saved!")

st.markdown("---")
st.markdown("## 📋 Your RedGifs Links")

if not status_data:
    st.info("No RedGifs links added yet.")
else:
    keys_to_delete = []

    for key, metadata in status_data.items():
        redgifs_url = metadata["url"]

        with st.expander(f"🎥 {redgifs_url}"):
            st.write(f"**Title**: {metadata.get('title')}")
            st.write(f"**Subreddits**: {', '.join(metadata.get('subreddits', []))}")

            for sub in metadata.get("subreddits", []):
                post_info = metadata["reddit_posts"].get(sub, {})
                already_posted = post_info.get("posted", False)
                post_url = post_info.get("url")

                col1, col2 = st.columns([3, 1])
                with col1:
                    if post_url:
                        st.markdown(f"🔗 [View post on r/{sub}]({post_url})")
                    else:
                        st.write(f"r/{sub}")

                with col2:
                    if already_posted:
                        st.success("Posted")
                    else:
                        if st.button(f"Post to r/{sub}", key=f"{key}_{sub}"):
                            try:
                                cmd = ["python", "post.py", "--link", redgifs_url, "--sub", sub, "--title", metadata["title"]]
                                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                                output = result.stdout

                                match = re.search(r'https://www\.reddit\.com/r/\S+', output)
                                if match:
                                    post_url = match.group(0)
                                    metadata["reddit_posts"][sub] = {
                                        "posted": True,
                                        "url": post_url
                                    }
                                    st.success(f"📬 Posted to r/{sub}")
                                    st.markdown(f"[View post]({post_url})")
                                else:
                                    st.error("Post completed but Reddit URL not found.")
                            except subprocess.CalledProcessError as e:
                                st.error(f"Failed to post:\n{e.stderr}")

            # Add delete button at the bottom of each expander
            if st.button("🗑️ Delete", key=f"delete_{key}"):
                keys_to_delete.append(key)

        # Save any updates (like Reddit posts)
        status_data[key] = metadata
        save_status(status_data)

    # Handle deletions outside the loop
    if keys_to_delete:
        for key in keys_to_delete:
            del status_data[key]
        save_status(status_data)
        st.success(f"🗑️ Deleted {len(keys_to_delete)} link(s).")
        st.experimental_rerun()