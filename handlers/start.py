from telegram import Update
from telegram.ext import ContextTypes
from utils.keyboards import get_main_menu_keyboard
from database.models import UserSession

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user_id = update.effective_user.id
    UserSession.clear(user_id)  # Clear previous session
    
    welcome_text = (
        "🌸 *Welcome to Myanimalist!* 🌸\n\n"
        "လက်ကိုင်ပုဝါလေးတွေက ဘောင်ချာရပြီး ၁၀ရက်နဲ့ အထက်မှာ Delivery အပ်ပေးပါတယ်ရှင့် 💝\n\n"
        "ကျေးဇူးပြု၍ မှာယူလိုသော ပစ္စည်းအမျိုးအစားကို ရွေးချယ်ပါ:"
    )
    
    await update.message.reply_text(
        welcome_text,
        reply_markup=get_main_menu_keyboard(),
        parse_mode='Markdown'
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle all button callbacks"""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'category_handkerchief':
        from handlers.handkerchief import show_handkerchief
        await show_handkerchief(update, context)
    elif query.data == 'category_clothes':
        await query.edit_message_text("👔 Clothes section coming soon! 🚧")
    elif query.data == 'back_to_main':
        await query.edit_message_text(
            "ကျေးဇူးပြု၍ မှာယူလိုသော ပစ္စည်းအမျိုးအစားကို ရွေးချယ်ပါ:",
            reply_markup=get_main_menu_keyboard()
        )
