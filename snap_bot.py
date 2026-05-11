import logging
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot Token (tomar BotFather theke niye nao)
BOT_TOKEN = "8776822620:AAH0yFJXsgRlYOs06QSveq79tzEA5DpeDMM"

# Snapchat API (unofficial)
SNAPCHAT_API_URL = "https://snapchatapi.com/api/v1"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📊 Add Count Check", callback_data='check_add')],
        [InlineKeyboardButton("ℹ️ Help", callback_data='help')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🔥 *Snapchat Add Count Bot*\n\n"
        "👤 Ekta Snapchat username pathao, ami tar add count ber kore dibo!\n\n"
        "💡 Example: `@username` or `username`",
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'check_add':
        await query.edit_message_text(
            "📝 Snapchat username pathao:\n"
            "*Example:* `@username` or `username`",
            parse_mode='Markdown'
        )
    elif query.data == 'help':
        help_text = """
🤖 *How to use:*

1️⃣ Username pathao: `@username` or `username`
2️⃣ Ami add count, friend count, snap score dibo
3️⃣ Multiple username ek sathe pathate paro

*Supported:* Public Snapchat accounts only
*Rate limit:* 10 requests/minute

⚠️ *Note:* Snapchat TOS follow koro!
        """
        await query.edit_message_text(help_text, parse_mode='Markdown')

async def check_snapchat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.text.strip()
    
    # Remove @ if present
    if username.startswith('@'):
        username = username[1:]
    
    if not username.replace('_', '').isalnum():
        await update.message.reply_text("❌ Invalid username! Only letters, numbers, underscores allowed.")
        return
    
    # Show typing
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    try:
        # Snapchat API call (unofficial)
        url = f"https://snapchatapi.com/api/snapchat/user/{username}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('found', False):
                # Format response
                result = f"""
🔍 *Snapchat Profile: {username}*

👥 *Friends:* {data.get('friendsCount', 'N/A')}
📈 *Add Count:* {data.get('incomingFriendRequests', 'N/A')}
📊 *Snap Score:* {data.get('snapScore', 'N/A')}
📱 *Status:* {data.get('status', 'N/A')}

🔗 Profile: snapchat://add/{username}
                """
                await update.message.reply_text(result, parse_mode='Markdown')
            else:
                await update.message.reply_text(f"❌ User `{username}` not found or private account!", parse_mode='Markdown')
        else:
            await update.message.reply_text("❌ API error! Try again later.")
            
    except requests.exceptions.RequestException:
        await update.message.reply_text("❌ Connection error! Snapchat server busy.")
    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text("❌ Something went wrong! Try again.")

def main():
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_snapchat))
    
    # Start bot
    print("🤖 Snapchat Add Count Bot Started!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
