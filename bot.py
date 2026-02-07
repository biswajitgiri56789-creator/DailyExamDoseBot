import json, random, os
from datetime import datetime
from telegram import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=BOT_TOKEN)

subjects = json.load(open("subjects.json", encoding="utf-8"))
chapters = json.load(open("chapters.json", encoding="utf-8"))
posted = json.load(open("posted.json", encoding="utf-8"))

def pick():
    cls = random.choice(list(subjects.keys()))
    lang = random.choice(["bn", "en"])
    subject = random.choice(subjects[cls][lang])
    chapter = random.choice(chapters.get(subject, ["Important Topic"]))

    key = f"{cls}-{subject}-{chapter}"
    if key in posted:
        return None

    posted.append(key)
    json.dump(posted, open("posted.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    now = datetime.now().strftime("%d %B %Y | %I:%M %p")

    if lang == "bn":
        question = f"{chapter} অধ্যায়ের গুরুত্বপূর্ণ প্রশ্ন আলোচনা কর।"
    else:
        question = f"Discuss the most important questions from {chapter}."

    return f"""
📘 *Daily Exam Dose*

🎓 *Class:* {cls}
📚 *Subject:* {subject}
📖 *Chapter:* {chapter}

📝 *Important Suggestion Question:*
{question}

🕒 {now}
"""

msg = pick()
if msg:
    bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode="Markdown")