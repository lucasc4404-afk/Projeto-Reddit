# 🚀 Reddit Pulse - Top Engagement Dashboard

A modern analytics platform and web interface designed to track, analyze, and visualize the most engaged posts from Reddit on **Technology** and **Soccer** (*Futebol*).

---

## 📋 Features

- **Reddit OAuth2 Extractor (`reddit_engagement_analyzer.py`)**:
  - Collects the 100 most recent posts from Reddit using the official OAuth2 API endpoint.
  - Computes community engagement score:
    $$\text{Total Engagement} = \text{Score (Upvotes)} + \text{Number of Comments}$$
  - Ranks and extracts the Top 5 highest engagement posts per category.
  - Automatically exports datasets to JSON format.

- **Modern Web Dashboard (`index.html`)**:
  - **Tab Navigation**: Clean separation between **Technology** and **Soccer** topics.
  - **Glassmorphism & SaaS Design**: Responsive layout with dark/light mode toggle.
  - **Engagement Badges**: Special podium ranks (🥇 #1, 🥈 #2, 🥉 #3) with custom medal styling.
  - **Real-Time Controls**: Search bar to filter posts instantly by title, summary, or tags, plus sort options (Engagement, Upvotes, Comments).
  - **Safe Navigation**: Validated URLs pointing to Reddit search and subreddits, preventing Internal Server Errors.
  - **Data Import**: Allows importing custom JSON outputs directly from the UI.

---

## 🛠️ Project Structure

```bash
├── index.html                      # Modern interactive frontend dashboard
├── reddit_engagement_analyzer.py  # Python script for Reddit OAuth2 data extraction
├── top5_por_topico.json            # Curated dataset with top 5 posts per category
├── .gitignore                      # Git ignore rules
└── README.md                       # Project documentation
```

---

## 🚀 Getting Started

### 1. View Dashboard
Simply open `index.html` in your web browser:
- Double-click `index.html` or run:
  ```powershell
  start index.html
  ```

### 2. Run the Extractor (Optional)
To fetch live data from Reddit:
1. Register a free Reddit application of type `script` at [Reddit App Preferences](https://www.reddit.com/prefs/apps).
2. Set your environment variables and execute:
   ```powershell
   $env:REDDIT_CLIENT_ID="YOUR_CLIENT_ID"
   $env:REDDIT_CLIENT_SECRET="YOUR_CLIENT_SECRET"
   python reddit_engagement_analyzer.py
   ```

---

## 📄 License
This project is open-source and available under the MIT License.
