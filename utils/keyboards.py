from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("🧣 လက်ကိုင်ပုဝါ (Handkerchief)", callback_data='category_handkerchief')],
        [InlineKeyboardButton("👔 အဝတ်အစား (Clothes)", callback_data='category_clothes')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_color_keyboard():
    from data.products import HANDKERCHIEF_COLORS
    keyboard = []
    for i in range(0, len(HANDKERCHIEF_COLORS), 2):
        row = []
        row.append(InlineKeyboardButton(HANDKERCHIEF_COLORS[i], callback_data=f'color_{i}'))
        if i + 1 < len(HANDKERCHIEF_COLORS):
            row.append(InlineKeyboardButton(HANDKERCHIEF_COLORS[i+1], callback_data=f'color_{i+1}'))
        keyboard.append(row)
    keyboard.append([InlineKeyboardButton("🔙 ပြန်သွားမယ် (Back)", callback_data='back_to_main')])
    return InlineKeyboardMarkup(keyboard)

def get_flower_keyboard():
    from data.products import FLOWERS
    keyboard = []
    for i in range(0, len(FLOWERS), 2):
        row = []
        row.append(InlineKeyboardButton(FLOWERS[i], callback_data=f'flower_{i}'))
        if i + 1 < len(FLOWERS):
            row.append(InlineKeyboardButton(FLOWERS[i+1], callback_data=f'flower_{i+1}'))
        keyboard.append(row)
    keyboard.append([InlineKeyboardButton("🔙 ပြန်သွားမယ် (Back)", callback_data='back_to_color')])
    return InlineKeyboardMarkup(keyboard)

def get_confirmation_keyboard():
    keyboard = [
        [InlineKeyboardButton("✅ အတည်ပြုပြီး Cart ထဲထည့်မယ် (Confirm & Add to Cart)", callback_data='confirm_add_cart')],
        [InlineKeyboardButton("🔙 ပြန်ပြင်မယ် (Edit)", callback_data='back_to_color')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_cart_keyboard():
    keyboard = [
        [InlineKeyboardButton("✅ မှာယူမယ် (Confirm Order)", callback_data='confirm_order')],
        [InlineKeyboardButton("🔙 ထပ်ထည့်မည် (add more)", callback_data='back_to_main')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_final_confirmation_keyboard():
    keyboard = [
        [InlineKeyboardButton("✅ သေချာပြီ မှာယူမယ် (Yes, Place Order)", callback_data='place_order')],
        [InlineKeyboardButton("❌ မှာယူမှုပယ်ဖျက်မယ် (Cancel)", callback_data='cancel_order')]
    ]
    return InlineKeyboardMarkup(keyboard)
