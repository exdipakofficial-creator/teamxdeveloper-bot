from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters, CallbackQueryHandler

TOKEN = "8573484592:AAF-Bns-51l3OH5tBoywiG-ro69SqY0E8ME"
ADMIN_ID = 6658513478

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("👤 Contact Owner", callback_data="contact")],
        [InlineKeyboardButton("🛍 My Services", callback_data="services")],
        [InlineKeyboardButton("📢 My Channel", callback_data="channel")],
        [InlineKeyboardButton("💰 Offers", callback_data="offers")],
        [InlineKeyboardButton("🤖 AI Support", callback_data="ai")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "━━━━━━━━━━━━━━━\n"
        "💎 TeamX Developer™\n"
        "Official Business System\n"
        "━━━━━━━━━━━━━━━",
        reply_markup=reply_markup
    )

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "contact":
        await query.message.reply_text("📩 Send your message. Owner will reply soon.")

    elif query.data == "services":
        await query.message.reply_text(
            "🛍 Premium Services\n\n"
            "• Telegram Bot Setup\n"
            "• AI Automation\n"
            "• Business Growth\n"
            "• Branding & Design"
        )

    elif query.data == "channel":
        await query.message.reply_text("📢 Join Official Channel:\nhttps://t.me/TeamX_Dev")

    elif query.data == "offers":
        await query.message.reply_text("🔥 Limited Offer – 20% OFF this week.")

    elif query.data == "ai":
        await query.message.reply_text("🤖 Ask your question...")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat.id
    text = update.message.text.lower()

    # Admin reply system
    if update.message.reply_to_message and user_id == ADMIN_ID:
        try:
            target_id = update.message.reply_to_message.forward_from.id
            await context.bot.send_message(chat_id=target_id, text=update.message.text)
        except:
            pass
        return

    # AI Auto replies
    if "price" in text:
        await update.message.reply_text("💰 Please check 🛍 My Services for pricing details.")
        return

    if "delivery" in text:
        await update.message.reply_text("⏳ Delivery time: 24–48 hours.")
        return

    if "payment" in text:
        await update.message.reply_text("💳 We accept UPI. Send screenshot after payment.")
        return

    # Forward to admin
    if user_id != ADMIN_ID:
        await context.bot.forward_message(
            chat_id=ADMIN_ID,
            from_chat_id=user_id,
            message_id=update.message.message_id
        )
        await update.message.reply_text("📨 Message sent to owner.")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
