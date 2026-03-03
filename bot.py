from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters, CallbackQueryHandler
import asyncio

TOKEN = "8573484592:AAF-Bns-51l3OH5tBoywiG-ro69SqY0E8ME"
ADMIN_ID = 6658513478  # Your numeric Telegram ID

user_message_map = {}
broadcast_users = set()
current_offer = "🔥 No active offers right now."

# ---------------- MAIN MENU ---------------- #

def main_menu():
    keyboard = [
        [InlineKeyboardButton("👤 Contact Owner", callback_data="contact")],
        [InlineKeyboardButton("🛍 My Services", callback_data="services")],
        [InlineKeyboardButton("📢 My Channel", callback_data="channel")],
        [InlineKeyboardButton("💰 Offers", callback_data="offers")],
        [InlineKeyboardButton("🤖 AI Support", callback_data="ai")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    broadcast_users.add(update.message.chat.id)
    await update.message.reply_text(
        "━━━━━━━━━━━━━━━\n"
        "💎 TeamX Developer™\n"
        "Official Business System\n"
        "━━━━━━━━━━━━━━━",
        reply_markup=main_menu()
    )

# ---------------- BUTTONS ---------------- #

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "contact":
        await query.message.reply_text("📩 Send your message. Owner will reply personally.")

    elif query.data == "services":
        await query.message.reply_text(
            "🛍 Premium Services\n\n"
            "• Telegram Bot Setup\n"
            "• AI Automation System\n"
            "• Business Growth Setup\n"
            "• Branding & Design\n"
            "• Full Automation Package"
        )

    elif query.data == "channel":
        await query.message.reply_text("📢 Join Official Channel:\nhttps://t.me/TeamX_Dev")

    elif query.data == "offers":
        await query.message.reply_text(current_offer)

    elif query.data == "ai":
        await query.message.reply_text("🤖 Ask your question...")

# ---------------- HANDLE MESSAGE ---------------- #

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat.id
    text = update.message.text.lower()

    # 🔥 Admin reply system
    if user_id == ADMIN_ID and update.message.reply_to_message:
        replied_id = update.message.reply_to_message.message_id
        if replied_id in user_message_map:
            target = user_message_map[replied_id]
            await context.bot.send_message(chat_id=target, text=update.message.text)
        return

    # 🤖 Hybrid AI
    if "price" in text:
        await update.message.reply_text("💰 Prices depend on service. Check 🛍 My Services.")
        return

    if "delivery" in text:
        await update.message.reply_text("⏳ Delivery time: 24–48 hours.")
        return

    if "payment" in text:
        await update.message.reply_text("💳 UPI accepted. Send screenshot after payment.")
        return

    if "hello" in text or "hi" in text:
        await update.message.reply_text("👋 Welcome to TeamX Developer™. How can we help you?")
        return

    # 📩 Send to Admin
    if user_id != ADMIN_ID:
        sent = await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"📨 New Message\n\n👤 {update.message.from_user.first_name}\n🆔 {user_id}\n\n💬 {update.message.text}"
        )

        user_message_map[sent.message_id] = user_id
        await update.message.reply_text("📨 Message sent to owner.")

        # 🔥 Auto delete chat
        try:
            await asyncio.sleep(5)
            await update.message.delete()
        except:
            pass

# ---------------- BROADCAST ---------------- #

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.id == ADMIN_ID:
        msg = update.message.text.replace("/broadcast ", "")
        for user in broadcast_users:
            try:
                await context.bot.send_message(chat_id=user, text=msg)
            except:
                pass
        await update.message.reply_text("✅ Broadcast Sent.")

# ---------------- UPDATE OFFER ---------------- #

async def update_offer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_offer
    if update.message.chat.id == ADMIN_ID:
        current_offer = update.message.text.replace("/setoffer ", "")
        await update.message.reply_text("✅ Offer Updated.")

# ---------------- APP RUN ---------------- #

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))
app.add_handler(CommandHandler("broadcast", broadcast))
app.add_handler(CommandHandler("setoffer", update_offer))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
