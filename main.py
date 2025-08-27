import telebot
from telebot import types

# ==============================
# 🔑 BOT CONFIG
# ==============================
TOKEN = "8284069837:AAFUNLCr1YzOAvl6hjj_syEohwjXHKvOq7g"   # ✅ Your Bot Token
CHANNEL_ID = -1003028883651   # ✅ Your Private Channel ID
UPI_ID = "idris081006@fam"    # ✅ Your UPI ID
QR_CODE_PATH = "qr.png"       # ⚠️ Apna QR Code ka image file (bot ke same folder me rakho)

bot = telebot.TeleBot('8284069837:AAFUNLCr1YzOAvl6hjj_syEohwjXHKvOq7g')


# ==============================
# 🔰 MAIN MENU FUNCTION
# ==============================
def main_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("💠 Buy 1K Views", "💠 Buy 10K Views")
    markup.add("💰 Deposit", "❓ Help")
    bot.send_message(chat_id, "📌 Please choose an option:", reply_markup=markup)


# ==============================
# 🔰 START COMMAND
# ==============================
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f"👋 Welcome {message.from_user.first_name}!")
    main_menu(message.chat.id)


# ==============================
# 🔰 TEXT HANDLER (ORDERS + DEPOSIT + HELP)
# ==============================
@bot.message_handler(func=lambda msg: True)
def handle_message(message):
    user = message.from_user
    username = f"@{user.username}" if user.username else user.first_name

    # ---- BUY 1K VIEWS ----
    if message.text == "💠 Buy 1K Views":
        msg = bot.send_message(message.chat.id, "🔗 Send your Instagram link for *1K Views – 39 Token*")
        bot.register_next_step_handler(msg, lambda m: process_order(m, username, "1K Views – 39 Token"))

    # ---- BUY 10K VIEWS ----
    elif message.text == "💠 Buy 10K Views":
        msg = bot.send_message(message.chat.id, "🔗 Send your Instagram link for *10K Views – 99 Token*")
        bot.register_next_step_handler(msg, lambda m: process_order(m, username, "10K Views – 99 Token"))

    # ---- DEPOSIT ----
    elif message.text == "💰 Deposit":
        send_deposit_instructions(message.chat.id, username)

    # ---- HELP ----
    elif message.text == "❓ Help":
        bot.send_message(message.chat.id, "📞 Contact support: @YourSupportUsername")

    else:
        bot.send_message(message.chat.id, "❌ Invalid option. Please use the menu below.")
        main_menu(message.chat.id)


# ==============================
# 🔰 PROCESS ORDER (Forward to Admin Channel)
# ==============================
def process_order(message, username, order_type):
    insta_link = message.text
    order_text = (
        f"🆕 New Order Received\n\n"
        f"👤 User: {username}\n"
        f"📌 Order: {order_type}\n"
        f"🔗 Link: {insta_link}"
    )
    bot.send_message(CHANNEL_ID, order_text)
    bot.send_message(message.chat.id, "✅ Your order has been placed successfully!")
    main_menu(message.chat.id)


# ==============================
# 🔰 DEPOSIT FLOW
# ==============================
def send_deposit_instructions(chat_id, username):
    order_text = f"💰 Deposit Request\n\nUser: {username}"
    bot.send_message(CHANNEL_ID, order_text)

    inline_markup = types.InlineKeyboardMarkup()
    confirm_btn = types.InlineKeyboardButton("✅ I have paid", callback_data="paid")
    cancel_btn = types.InlineKeyboardButton("❌ Cancel", callback_data="cancel_deposit")
    inline_markup.add(confirm_btn, cancel_btn)

    caption = (
        f"💳 *Deposit Instructions*\n\n"
        f"📌 UPI ID: `{UPI_ID}`\n"
        f"📷 Scan the QR below to pay\n\n"
        f"👉 After payment, click ✅ I have paid"
    )
    with open(QR_CODE_PATH, "rb") as qr:
        bot.send_photo(chat_id, qr, caption, parse_mode="Markdown", reply_markup=inline_markup)


# ==============================
# 🔰 INLINE BUTTON HANDLER
# ==============================
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user = call.from_user
    username = f"@{user.username}" if user.username else user.first_name

    if call.data == "paid":
        bot.send_message(call.message.chat.id,
                         "📤 Please send your *payment screenshot or UTR number* here.")
        bot.answer_callback_query(call.id, "✅ Now send payment proof!")
        bot.register_next_step_handler(call.message, get_payment_proof, username)

    elif call.data == "cancel_deposit":
        bot.send_message(call.message.chat.id, "❌ Deposit cancelled. Returning to main menu...")
        main_menu(call.message.chat.id)
        bot.answer_callback_query(call.id, "Cancelled!")


# ==============================
# 🔰 PAYMENT PROOF HANDLER
# ==============================
def get_payment_proof(message, username):
    if message.photo:
        file_id = message.photo[-1].file_id
        bot.send_message(CHANNEL_ID,
                         f"💰 Payment Proof Received\n\nUser: {username}\n📷 Screenshot below 👇")
        bot.send_photo(CHANNEL_ID, file_id)

    elif message.text:
        bot.send_message(CHANNEL_ID,
                         f"💰 Payment Proof Received\n\nUser: {username}\nUTR / Note: {message.text}")

    bot.send_message(message.chat.id, "✅ Your payment proof has been submitted. We’ll verify soon.")
    main_menu(message.chat.id)


# ==============================
# 🔰 RUN BOT
# ==============================
print("🤖 Bot is running...")
bot.polling()
