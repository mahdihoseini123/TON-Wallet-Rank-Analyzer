import os
import telebot
import requests
import math
from dotenv import load_dotenv # Import for loading environment variables

# --- API Keys ---
# --- START OF EDITS: Read keys from the .env file ---
load_dotenv()
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TONAPI_API_KEY = os.getenv('TONAPI_API_KEY')

# --- Core Functions ---

def calculate_level(usd_value):
    """
    Calculates a level from 1 to 100 based on the wallet's USD value.
    The scale is logarithmic, so leveling up is faster at the beginning.
    Level 100 is calibrated to be around $7.5M (approx. 1M TON at $7.5/TON).
    """
    if usd_value <= 0:
        return 1
    # New logarithmic formula for a more engaging level progression
    # Formula: level = A * log10(value) + B, calibrated for our range
    level = max(1, min(100, int(17 * math.log10(usd_value + 1) - 16)))
    return level

def get_usd_for_level(level):
    """Calculates the approximate USD value required to reach a specific level."""
    if level <= 1:
        return 0
    # This is the inverse formula of the calculate_level function
    # level = 17 * log10(usd + 1) - 16  =>  usd = 10**((level + 16) / 17) - 1
    return 10**((level + 16) / 17) - 1

# --- START OF EDITS: Expanded messaging and leveling system with 100 unique messages ---

# Define the tiers and their corresponding titles
TIERS = [
    (100, "🔱 LEVIATHAN 🔱"), (99, "💎 DIAMOND HANDS 💎"), (95, "👑 TITAN 👑"),
    (90, "🥇 WHALE 🥇"), (80, "🦈 SHARK 🦈"), (70, "🐬 DOLPHIN 🐬"),
    (60, "🛡️ VETERAN 🛡️"), (50, "⚔️ KNIGHT ⚔️"), (40, "🗺️ EXPLORER 🗺️"),
    (25, "🔥 ACOLYTE 🔥"), (10, "🐟 MINNOW 🐟"), (0, "🌱 SPROUT 🌱")
]

# List of 100 motivational messages, one for each level
LEVEL_MESSAGES = [
    # Levels 1-9: The Beginning (Sprout & Minnow)
    "Welcome to the TON universe! Every great journey starts with a single step.", # Lvl 1
    "You've planted your seed in the TON ecosystem. Now, let's watch it grow.", # Lvl 2
    "The foundation is set. Each new TON added is a brick in your future empire.", # Lvl 3
    "You're on the ground floor. The only way from here is up! 🚀", # Lvl 4
    "You've started your swim in the great TON ocean! Keep going.", # Lvl 5
    "You're officially making waves, even if they're small for now. Keep the momentum!", # Lvl 6
    "You've left the shallow end. Deeper, more rewarding waters await your exploration.", # Lvl 7
    "Your portfolio is starting to get noticed by the other minnows. You're a leader in your school.", # Lvl 8
    "Excellent progress! You are about to graduate from the novice ranks.", # Lvl 9
    # Levels 10-24: The Journey Begins (Acolyte)
    "You are now an Acolyte of TON! Your dedication to the network is clear.", # Lvl 10
    "You understand the fundamentals. Your belief in The Open Network is strong.", # Lvl 11
    "You're part of the inner circle now. Your journey is inspiring others.", # Lvl 12
    "Keep building. Your portfolio is becoming a testament to your early vision.", # Lvl 13
    "You've moved past the basics. You see the long-term potential.", # Lvl 14
    "Every level you gain solidifies your status as a true TON enthusiast.", # Lvl 15
    "The path of an Acolyte is one of patience and conviction. You are walking it well.", # Lvl 16
    "Your commitment is impressive. The next major rank is on the horizon.", # Lvl 17
    "You're accumulating knowledge and assets. A powerful combination.", # Lvl 18
    "The early believers are often the most rewarded. Stay the course.", # Lvl 19
    "You are halfway to the next major tier. The Explorer rank awaits!", # Lvl 20
    "Your portfolio is growing healthier with every step. Consistency is key.", # Lvl 21
    "You're learning to navigate the ecosystem like a pro.", # Lvl 22
    "The community values members like you. Your presence strengthens the network.", # Lvl 23
    "Just a little more to go! The rank of Explorer is within your grasp.", # Lvl 24
    # Levels 25-39: Becoming Serious (Explorer)
    "You are now an Explorer! You're charting new territories in the TON ecosystem.", # Lvl 25
    "You're building a serious portfolio now, exploring the depths of what TON offers.", # Lvl 26
    "Your bag is getting heavier, and your vision is getting clearer.", # Lvl 27
    "You are no longer just a participant; you are a pioneer.", # Lvl 28
    "Keep accumulating. Great things are ahead for those who explore early.", # Lvl 29
    "Your portfolio is diversifying, showing a deep understanding of the landscape.", # Lvl 30
    "You've seen market cycles and remained steadfast. That's the mark of an Explorer.", # Lvl 31
    "The next rank, Knight, is for those who protect and build the ecosystem. You're on the right path.", # Lvl 32
    "Your conviction is an asset as valuable as your TON.", # Lvl 33
    "You are far ahead of the crowd. Your early explorations will pay off.", # Lvl 34
    "Halfway to Knighthood! Your dedication is truly commendable.", # Lvl 35
    "You're not just holding; you're building a legacy on The Open Network.", # Lvl 36
    "The map of TON is vast, and you've explored more than most.", # Lvl 37
    "Your strategy is sound, your execution is precise.", # Lvl 38
    "The gates of the Knight's Order are opening for you. Prepare yourself.", # Lvl 39
    # Levels 40-59: Established Player (Knight & Veteran)
    "You are a Knight of TON! A protector of the ecosystem with a significant stake.", # Lvl 40
    "Your portfolio is a fortress, built on a foundation of smart decisions.", # Lvl 41
    "You are an inspiration to the newcomers who follow in your footsteps.", # Lvl 42
    "Your journey from a Sprout to a Knight is a story of success.", # Lvl 43
    "You hold a position of honor and responsibility within the community.", # Lvl 44
    "The rank of Veteran is reserved for the truly experienced. You are almost there.", # Lvl 45
    "Your holdings are now significant enough to be considered a strategic asset.", # Lvl 46
    "You've weathered storms and enjoyed the sunshine. A true market participant.", # Lvl 47
    "Your wisdom is as valuable as your wallet.", # Lvl 48
    "You are on the cusp of becoming a true Veteran of the network.", # Lvl 49
    "You are a Veteran! You've seen it all and your portfolio proves it.", # Lvl 50
    "Your experience and holdings command respect. You are a pillar of the community.", # Lvl 51
    "The higher ranks are now clearly within your reach. The Dolphin pod awaits.", # Lvl 52
    "You are a testament to the power of long-term vision.", # Lvl 53
    "Your portfolio is not just an investment; it's a part of TON's history.", # Lvl 54
    "You've earned your stripes. Your reputation precedes you.", # Lvl 55
    "Your strategic moves are becoming a case study for others.", # Lvl 56
    "You are a respected voice in the community.", # Lvl 57
    "Keep navigating the waters; the rank of Dolphin is near.", # Lvl 58
    "Your journey is becoming legendary.", # Lvl 59
    # Levels 60-79: Influencer (Dolphin & Shark)
    "You are a Dolphin! You navigate the ecosystem with grace and intelligence.", # Lvl 60
    "Your portfolio is strong, healthy, and growing with purpose.", # Lvl 61
    "You are part of a pod of smart investors, moving together.", # Lvl 62
    "Your influence is growing. Others look to you for signals.", # Lvl 63
    "You are a significant holder, a key player in the TON ocean.", # Lvl 64
    "You've mastered the art of accumulation and patience.", # Lvl 65
    "Your portfolio is a work of art, crafted with skill and foresight.", # Lvl 66
    "You are approaching the territory of the apex predators. The Sharks.", # Lvl 67
    "Your presence is felt across the network.", # Lvl 68
    "You are a beacon of success for the entire community.", # Lvl 69
    "You are a Shark! A formidable force in these waters.", # Lvl 70
    "You hunt for the best opportunities and your instincts are sharp.", # Lvl 71
    "You are a skilled and serious investor, respected and perhaps feared.", # Lvl 72
    "Your portfolio is a weapon, and you wield it with precision.", # Lvl 73
    "You are in the top percentile of all TON holders.", # Lvl 74
    "The Whale pod is a legendary group. You are on the verge of joining them.", # Lvl 75
    "Your every move is analyzed. You are a market maker.", # Lvl 76
    "You have achieved a level of success most can only dream of.", # Lvl 77
    "Your conviction is unshakable, your strategy proven.", # Lvl 78
    "The title of Whale is not given; it is earned. You have almost earned it.", # Lvl 79
    # Levels 80-94: Elite Status (Whale)
    "You are a WHALE! Your movements create waves in the TON ecosystem.", # Lvl 80
    "You are a major player, and the community watches your every move.", # Lvl 81
    "Your portfolio is a force of nature.", # Lvl 82
    "You have reached a level of influence that can shape markets.", # Lvl 83
    "Your name is whispered in the halls of the TON elite.", # Lvl 84
    "You are a cornerstone of the network's value.", # Lvl 85
    "Your vision for TON is not just a belief; it's a reality you help create.", # Lvl 86
    "You are in a class of your own.", # Lvl 87
    "The rank of Titan is reserved for the truly legendary. It is your destiny.", # Lvl 88
    "You are a living legend of The Open Network.", # Lvl 89
    # Levels 90-99: The Pinnacle (Titan, Diamond Hands)
    "You are a TITAN! You stand among the giants of TON.", # Lvl 90
    "Your influence is immense, your portfolio a monument.", # Lvl 91
    "You are not just part of the ecosystem; you are the ecosystem.", # Lvl 92
    "Your mastery of the TON universe is complete.", # Lvl 93
    "You have ascended to a level few will ever reach.", # Lvl 94
    "You have DIAMOND HANDS! Unbreakable. Unshakeable.", # Lvl 95
    "Your long-term vision is an inspiration to all. You've reached the pinnacle.", # Lvl 96
    "You are a symbol of strength and conviction in the face of any market.", # Lvl 97
    "Your legacy is forged in the blockchain, immutable and eternal.", # Lvl 98
    "The final level awaits. The ultimate rank. You are on the threshold of godhood.", # Lvl 99
    # Level 100: Legendary
    "You are a LEVIATHAN! The ultimate power in the TON Ocean. The ecosystem evolves around you. All hail." # Lvl 100
]

def get_motivational_message(level, usd_value, ton_balance, ton_price_usd):
    """Generates a creative, motivational message based on the user's level."""
    
    formatted_usd = f"{usd_value:,.2f}"
    formatted_ton = f"{ton_balance:,.3f}"
    
    # Find the appropriate title based on the level
    user_title = ""
    for min_level, title in TIERS:
        if level >= min_level:
            user_title = title
            break
            
    # Select the specific message from the list of 100
    # Level 1 corresponds to index 0
    user_message = LEVEL_MESSAGES[level - 1]

    header = (
        f"✅ Wallet Analysis Complete:\n\n"
        f"💰 **Balance:** `{formatted_ton}` TON\n"
        f"💵 **Approx. Value:** `${formatted_usd}`\n"
        f"🏆 **Your Rank:** **Level {level}** - {user_title}\n\n"
    )
    
    next_level_message = ""
    if level < 100:
        next_level_usd = get_usd_for_level(level + 1)
        usd_needed = next_level_usd - usd_value
        if usd_needed > 0 and ton_price_usd > 0:
            ton_needed = usd_needed / ton_price_usd
            next_level_message = f"\n\n💡 **Next Level:** Deposit just **{ton_needed:.2f} more TON** to reach Level {level + 1}!"
        
    return header + user_message + next_level_message
# --- END OF EDITS ---

def fetch_wallet_data(wallet_address):
    """
    Fetches balance, USD value, and calculates the level for a given wallet address.
    """
    headers = {"Authorization": f"Bearer {TONAPI_API_KEY}"}
    
    try:
        # 1. Get main account info
        account_url = f"https://tonapi.io/v2/accounts/{wallet_address}"
        account_res = requests.get(account_url, headers=headers)
        account_res.raise_for_status()
        account_data = account_res.json()
        ton_balance = int(account_data['balance']) / 1_000_000_000

        # 2. Get real-time TON price
        ton_price_usd = 7.5  # Fallback price
        try:
            price_url = "https://api.coingecko.com/api/v3/simple/price?ids=the-open-network&vs_currencies=usd"
            price_res = requests.get(price_url).json()
            ton_price_usd = price_res['the-open-network']['usd']
        except Exception as e:
            print(f"Error fetching price: {e}")

        total_usd_value = ton_balance * ton_price_usd

        # 3. Calculate user level
        level = calculate_level(total_usd_value)

        return {
            "level": level,
            "usdValue": total_usd_value,
            "tonBalance": ton_balance,
            "tonPriceUsd": ton_price_usd
        }
    except requests.exceptions.HTTPError as http_err:
        if http_err.response.status_code == 404:
            raise ValueError("Wallet address not found or not active on the network.")
        raise ConnectionError(f"Error communicating with TONAPI: {http_err}")
    except Exception as e:
        raise e

# --- Main Telegram Bot Logic ---
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "✨ Welcome to the TON Wallet Rank Analyzer! ✨\n\nPlease send your TON wallet address to discover your level.")

@bot.message_handler(func=lambda message: message.text is not None and not message.text.startswith('/'))
def handle_address(message):
    chat_id = message.chat.id
    wallet_address = message.text.strip()

    if not (wallet_address.startswith('UQ') or wallet_address.startswith('EQ')):
        bot.reply_to(message, "❌ Invalid address format. Please send a valid TON wallet address.")
        return
        
    waiting_msg = None
    try:
        waiting_msg = bot.reply_to(message, "⏳ Analyzing your wallet...")
        
        # Fetch and analyze data
        wallet_data = fetch_wallet_data(wallet_address)
        
        # Generate motivational message
        response_text = get_motivational_message(
            wallet_data['level'],
            wallet_data['usdValue'],
            wallet_data['tonBalance'],
            wallet_data['tonPriceUsd'] 
        )
        
        # Send the result to the user
        bot.send_message(chat_id, response_text, parse_mode="Markdown")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        bot.send_message(chat_id, f"❌ An error occurred: {e}")
    finally:
        if waiting_msg:
            try:
                bot.delete_message(chat_id, waiting_msg.message_id)
            except Exception as delete_error:
                print(f"Could not delete waiting message: {delete_error}")


# --- Run the Bot ---
if __name__ == '__main__':
    print("TON Wallet Rank Analyzer Bot is running...")
    bot.polling(none_stop=True)
