"""
DNR Capital - Daily Intelligence Report
Generates AI report using Anthropic API and sends to Telegram (FREE, instant)
"""

import anthropic
import urllib.request
import json
import datetime
import os

# ─────────────────────────────────────────
# CONFIG — set these as GitHub Secrets
# ─────────────────────────────────────────
ANTHROPIC_API_KEY  = os.environ["ANTHROPIC_API_KEY"]
TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]  # from BotFather
TELEGRAM_CHAT_ID   = os.environ["TELEGRAM_CHAT_ID"]    # your personal chat ID

# ─────────────────────────────────────────
# TOPIC & CASE STUDY ROTATION
# ─────────────────────────────────────────
TOPICS = [
    "Discounted Cash Flow (DCF) Valuation",
    "EBITDA and Enterprise Value",
    "LBO (Leveraged Buyout) Mechanics",
    "M&A Deal Structuring",
    "Capital Structure Optimization",
    "IPO Process and Underwriting",
    "Private Equity Fund Structure (GP/LP)",
    "Pitch Book and CIM Creation",
    "Due Diligence Framework",
    "Comparable Company Analysis (Comps)",
    "Precedent Transaction Analysis",
    "Debt Financing: Term Loans vs Bonds",
    "Working Capital Management",
    "SEBI Regulations for Investment Banks",
    "FEMA and Cross-Border Transactions",
    "Companies Act 2013 Key Provisions",
    "Financial Modeling Best Practices",
    "Equity Research Report Writing",
    "Derivatives: Options and Futures",
    "Credit Rating Methodology",
    "Restructuring and Turnaround",
    "PIPE Transactions",
    "Mezzanine Financing",
    "Fund of Funds Structure",
    "Portfolio Valuation: NAV, IRR, MOIC",
    "SEBI AIF Regulations",
    "RBI Regulations for NBFCs",
    "Venture Capital Term Sheet",
    "Bridge Financing",
    "Convertible Notes",
]

COMPANIES = [
    "Goldman Sachs", "KKR & Co.", "Blackstone Group", "Morgan Stanley",
    "Sequoia Capital India", "ICICI Securities", "Kotak Investment Banking",
    "Warburg Pincus India", "General Atlantic", "TPG Capital",
    "Carlyle Group", "Bain Capital", "Axis Capital", "JM Financial",
]

def get_rotation(items):
    start = datetime.date(2024, 1, 1)
    today = datetime.date.today()
    idx = (today - start).days % len(items)
    return items[idx]

def get_today_topic():   return get_rotation(TOPICS)
def get_today_company(): return get_rotation(COMPANIES)
def format_date():       return datetime.date.today().strftime("%A, %d %B %Y")

# ─────────────────────────────────────────
# GENERATE REPORT VIA ANTHROPIC
# ─────────────────────────────────────────
SYSTEM_PROMPT = """You are the Chief Intelligence Officer of DNR Capital.
Prepare a daily briefing for a 20-year-old CA Intermediate student building DNR Capital
— a firm offering investment banking, private equity, and financial & compliance services.

Format for Telegram using *bold* for headers (single asterisk). Keep under 1500 characters.

Use this exact structure:

🏦 *DNR CAPITAL — DAILY BRIEF*
📅 [date]

━━━━━━━━━━━━━━━━━━━━
📊 *MARKET PULSE*
• [key India market development]
• [key global macro point]
• [one sector or deal news]

━━━━━━━━━━━━━━━━━━━━
🧠 *CONCEPT: [topic title]*
[3-4 sentences: what it is, how it works, why it matters for IB/PE]

━━━━━━━━━━━━━━━━━━━━
🏢 *CASE STUDY: [company]*
[2-3 sentences: what they did right + 1 lesson for DNR Capital]

━━━━━━━━━━━━━━━━━━━━
💡 *FOUNDER'S NOTE*
[1 sharp, motivational line for the journey ahead]

— DNR Capital Intelligence"""

def generate_report():
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=700,
        system=SYSTEM_PROMPT,
        messages=[{
            "role": "user",
            "content": (
                f"Today is {format_date()}.\n"
                f"Today's concept to teach: {get_today_topic()}\n"
                f"Today's case study company: {get_today_company()}\n\n"
                "Generate the daily briefing. Use real knowledge about Indian financial "
                "markets and the company. Be concise, educational, and sharp."
            )
        }]
    )
    return message.content[0].text

# ─────────────────────────────────────────
# SEND TO TELEGRAM
# ─────────────────────────────────────────
def send_telegram(message: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = json.dumps({
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }).encode("utf-8")

    req = urllib.request.Request(
        url, data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            result = json.loads(response.read().decode("utf-8"))
            if result.get("ok"):
                print("✅ Message sent to Telegram successfully!")
                return True
            else:
                print(f"❌ Telegram API error: {result}")
                return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

# ─────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────
def main():
    print(f"📊 Generating DNR Capital Daily Report — {format_date()}")
    print(f"🧠 Topic:   {get_today_topic()}")
    print(f"🏢 Company: {get_today_company()}\n")

    report = generate_report()
    print("--- REPORT PREVIEW ---")
    print(report)
    print("----------------------\n")

    if not send_telegram(report):
        exit(1)

if __name__ == "__main__":
    main()
