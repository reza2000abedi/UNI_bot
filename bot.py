
import pandas as pd
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import random

df = pd.read_excel("students.xlsx")
otp_store = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام 👋\nشماره دانشجویی را وارد کنید:")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.strip()
    chat_id = update.message.chat_id

    if user_text.isdigit() and len(user_text) == 8:
        student_id = int(user_text)

        if student_id not in df['student_id'].values:
            await update.message.reply_text("❌ شماره دانشجویی پیدا نشد.")
            return

        otp = random.randint(10000, 99999)
        otp_store[chat_id] = {"student_id": student_id, "otp": otp}

        await update.message.reply_text(f"کد یکبار مصرف شما: {otp}")
        return

    if chat_id in otp_store:
        info = otp_store[chat_id]

        if user_text == str(info["otp"]):

            row = df[df['student_id'] == info["student_id"]].iloc[0]

            msg = f"""
🎓 *نمرات شما*:

📌 نام: {row['name']}
🆔 شماره دانشجویی: {row['student_id']}

نمره میان‌ترم: {row['score_mid']}
نمره پایان‌ترم: {row['score_final']}
فعالیت کلاسی: {row['class_activity']}
"""

            await update.message.reply_markdown(msg)

            del otp_store[chat_id]
            return
        else:
            await update.message.reply_text("❌ کد OTP صحیح نیست.")
            return

    await update.message.reply_text("لطفاً شماره دانشجویی یا OTP را درست وارد کنید.")

app = ApplicationBuilder().token("YOUR_BOT_TOKEN_HERE").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, handle_message))

app.run_polling()
