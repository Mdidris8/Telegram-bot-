from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
)
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, 
    ConversationHandler, ContextTypes, filters
)

TOKEN = "8284069837:AAFUNLCr1YzOAvl6hjj_syEohwjXHKvOq7g"

QR_CODE_IMAGE_URL = 'https://i.imgur.com/QRcodeSample.png'  # Replace with your QR code image URL

# Define states for conversation
(
    CHOOSING,
    INSTAGRAM_VIEWS,
    INSTAGRAM_FOLLOWERS,
    TELEGRAM_MEMBERS,
    DEPOSIT_UTR,
    DEPOSIT_SCREENSHOT
) = range(6)

START_KEYBOARD = [
    [InlineKeyboardButton("Instagram Views", callback_data='instagram_views')],
    [InlineKeyboardButton("Instagram Followers", callback_data='instagram_followers')],
    [InlineKeyboardButton("Telegram Members", callback_data='telegram_members')],
    [InlineKeyboardButton("Deposit", callback_data='deposit')],
    [InlineKeyboardButton("Help", callback_data='help')]
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome! Please choose an option:",
        reply_markup=InlineKeyboardMarkup(START_KEYBOARD)
    )
    return CHOOSING

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == 'instagram_views':
        text = (
            "Instagram Views Packages:\n\n"
            "1k views = 39 tokens\n"
            "10k views = 99 tokens\n\n"
            "Please send the Reel link for which you want views."
        )
        await query.edit_message_text(text)
        return INSTAGRAM_VIEWS

    elif data == 'instagram_followers':
        text = (
            "Instagram Followers Packages:\n\n"
            "500 followers = 850 tokens\n"
            "1k followers = 1679 tokens\n\n"
            "Please send the Instagram account link where you want followers."
        )
        await query.edit_message_text(text)
        return INSTAGRAM_FOLLOWERS

    elif data == 'telegram_members':
        text = (
            "Telegram Members Packages:\n\n"
            "1k members = 16 tokens\n"
            "10k members = 159 tokens\n\n"
            "Please send the Telegram channel link where you want members."
        )
        await query.edit_message_text(text)
        return TELEGRAM_MEMBERS

    elif data == 'deposit':
        deposit_text = (
            "💰 Deposit Details:\n\n"
            "👉 UPI ID : idris081006@fam   (Tap to copy)\n"
            "👉 Display Name: Mohammad Idris (Tap To Copy)\n\n"
            "💰 List Of Payment Points —\n"
            "▪️ 10.5 ₹ = 300 Points\n"
            "▪️ 21 ₹ = 600 Points\n"
            "▪️ 63 ₹ = 900 Points\n\n"
            "👉 Jis Hisab se Aap Deposit karoge, us hisaab se points add ho jayenge ✅\n\n"
            "⚠️ Note: Minimum Deposit ₹10.5 INR\n"
            "⚠️ After paying, please send your UTR number."
        )
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("✅ Paid (Send screenshot next)", callback_data='paid')]])
        await query.edit_message_media(
            media=InputMediaPhoto(QR_CODE_IMAGE_URL, caption=deposit_text),
            reply_markup=keyboard
        )
        return DEPOSIT_UTR

    elif data == 'paid':
        await query.edit_message_text("Thanks for confirming payment!\nNow please send a screenshot of the payment as proof.")
        return DEPOSIT_SCREENSHOT

    elif data == 'help':
        await query.edit_message_text("For any help contact @sam081116")
        return CHOOSING

    else:
        await query.edit_message_text("Invalid option, please try again.")
        return CHOOSING

# Handlers for collecting user input after options chosen

async def handle_instagram_views(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reel_link = update.message.text
    user = update.message.from_user
    # Save `reel_link` and user info as needed here (e.g. DB or file)
    await update.message.reply_text(
        f"Received your reel link:\n{reel_link}\nOur team will process your Instagram views order soon."
    )
    await update.message.reply_text(
        "Choose another option or send /start to go back to the main menu.",
        reply_markup=InlineKeyboardMarkup(START_KEYBOARD)
    )
    return CHOOSING

async def handle_instagram_followers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    insta_link = update.message.text
    await update.message.reply_text(
        f"Received your Instagram account link:\n{insta_link}\nOur team will process your followers order soon."
    )
    await update.message.reply_text(
        "Choose another option or send /start to go back to the main menu.",
        reply_markup=InlineKeyboardMarkup(START_KEYBOARD)
    )
    return CHOOSING

async def handle_telegram_members(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tg_channel = update.message.text
    await update.message.reply_text(
        f"Received your Telegram channel link:\n{tg_channel}\nOur team will process your members order soon."
    )
    await update.message.reply_text(
        "Choose another option or send /start to go back to the main menu.",
        reply_markup=InlineKeyboardMarkup(START_KEYBOARD)
    )
    return CHOOSING

async def handle_deposit_utr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    utr_no = update.message.text
    context.user_data['deposit_utr'] = utr_no
    await update.message.reply_text(
        "Thank you! Now please send a screenshot of the payment as proof."
    )
    return DEPOSIT_SCREENSHOT

async def handle_deposit_screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo:
        # Save payment screenshot file_id and UTR no for manual verification
        photo_file = update.message.photo[-1]
        file_id = photo_file.file_id
        utr_no = context.user_data.get('deposit_utr', 'Not provided')
        
        # Here you can save file_id and utr_no to DB or notify admin
        
        await update.message.reply_text(
            f"Payment screenshot received.\nUTR Number: {utr_no}\nOur team will verify and add points soon."
        )
        await update.message.reply_text(
            "Choose another option or send /start to go back to the main menu.",
            reply_markup=InlineKeyboardMarkup(START_KEYBOARD)
        )
        return CHOOSING
    else:
        await update.message.reply_text("Please send a valid photo screenshot.")
        return DEPOSIT_SCREENSHOT

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Operation cancelled. Send /start to begin again.")
    return ConversationHandler.END


if __name__ == '__main__':
    import asyncio

    application = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING: [CallbackQueryHandler(button_handler)],
            INSTAGRAM_VIEWS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_instagram_views)],
            INSTAGRAM_FOLLOWERS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_instagram_followers)],
            TELEGRAM_MEMBERS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_telegram_members)],
            DEPOSIT_UTR: [MessageHandler(filters ) ]
