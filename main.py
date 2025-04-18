import logging
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from openai import AsyncOpenAI

# إعداد تسجيل السجلات
logging.basicConfig(level=logging.INFO)

# التوكنات
TELEGRAM_TOKEN = "8181709413:AAGX5hqkr25v56qhbDY2aBHGOhGuue6-up0"
OPENROUTER_API_KEY = "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"

# إعداد عميل OpenRouter غير متزامن
openai_client = AsyncOpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

# دالة لمعالجة الرسائل
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        logging.warning("🚫 تم تجاهل رسالة غير نصية أو فاضية")
        return

    user_message = update.message.text
    logging.info(f"📩 استلمت رسالة من {update.effective_user.first_name}: {user_message}")

    try:
        response = await openai_client.chat.completions.create(
            model="mistralai/mistral-7b-instruct",
            messages=[{"role": "user", "content": user_message}]
        )
        reply = response.choices[0].message.content
    except Exception as e:
        logging.error(f"❌ حدث خطأ مع OpenRouter: {e}")
        reply = "حدث خطأ أثناء الاتصال بـ OpenRouter."

    await update.message.reply_text(reply)

# الدالة الرئيسية لتشغيل البوت
async def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logging.info("🤖 البوت يعمل الآن...")
    await app.run_polling()

# تشغيل البوت
if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()
    asyncio.run(main())