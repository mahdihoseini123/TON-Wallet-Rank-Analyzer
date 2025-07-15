# TON-Wallet-Rank-Analyzer
TON-Wallet-Rank-Analyzer
# TON Wallet Rank Analyzer Bot

# TON Wallet Rank Analyzer Bot

A Telegram bot submitted for the "Build with TONAPI" contest. This bot analyzes a TON wallet's holdings to determine its rank and level within the TON ecosystem, providing motivational, gamified feedback to encourage user engagement and investment.

## ✨ Key Features

- **Dynamic Leveling System:** Ranks users from Level 1 to 100 based on the real-time USD value of their TON assets, using a logarithmic scale for engaging progression.
- **Motivational Feedback:** Provides unique, creative messages for different tiers (Pioneer, Explorer, Whale, Legend) to encourage users to increase their holdings.
- **"Next Mission" Goal:** Calculates and displays the exact amount of TON needed to reach the next level, giving users a clear and achievable target.
- **Reliable Data:** Uses the official **TONAPI.io** service to reliably fetch on-chain data and the **CoinGecko API** for real-time market prices.

## 🚀 How to Run

1.  **Clone the repository.**
2.  **Install dependencies:**
    ```bash
    pip install pyTelegramBotAPI requests
    ```
3.  **Create a `.env` file** and add your keys:
    ```ini
    TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
    TONAPI_API_KEY=YOUR_TONAPI_API_KEY
    ```
4.  **Run the bot:**
    ```bash
    python main.py
    ```

## 📺 YouTube Demo

*[بعد از ساخت ویدیو، لینک آن را اینجا قرار دهید]*
