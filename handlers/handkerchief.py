from telegram import Update, InputMediaPhoto
from telegram.ext import ContextTypes, ConversationHandler
from utils.keyboards import (get_color_keyboard, get_flower_keyboard, 
                            get_confirmation_keyboard, get_cart_keyboard,
                            get_final_confirmation_keyboard, get_main_menu_keyboard)
from database.models import UserSession
from data.products import HANDKERCHIEF_IMAGES, HANDKERCHIEF_COLORS, FLOWERS, HANDKERCHIEF_PRICE
from utils.helpers import generate_order_id, format_order_summary, format_owner_notification
import config

# Conversation states
WAITING_NAME, WAITING_PHONE, WAITING_ADDRESS = range(3)

async def show_handkerchief(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show handkerchief images and color selection"""
    query = update.callback_query
    user_id = update.effective_user.id
    
    # Update session
    UserSession.update(user_id, {'stage': 'color_selection', 'current_item': {}})
    
    caption = (
        "🧣 *လက်ကိုင်ပုဝါ*\n\n"
        "❗❗ ချည်စာလုံးရဲ့ အရောင်နဲ့ ပန်းရဲ့ အရောင် ၊ ပန်းပွင့်မှာပါတဲ့ အပွင့်အရေအတွက်နဲ့ "
        "အခြားသောအသေးစိတ်တွေတော့ ရွေးခြယ်လို့မရနိုင်သေးပါဘူးရှင့် ❗❗\n\n"
        f"💰 *စျေးနှုန်း: {HANDKERCHIEF_PRICE:,} Ks*\n\n"
        "ကျေးဇူးပြု၍ အရောင်ရွေးချယ်ပါ:"
    )
    
    # Send images as media group
    media = [InputMediaPhoto(media=HANDKERCHIEF_IMAGES[0], caption=caption, parse_mode='Markdown')]
    for img in HANDKERCHIEF_IMAGES[1:]:
        media.append(InputMediaPhoto(media=img))
    
    # Delete previous message and send new media group
    await query.message.delete()
    messages = await context.bot.send_media_group(
        chat_id=update.effective_chat.id,
        media=media
    )
    
    # Send color selection keyboard
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="ကျေးဇူးပြု၍ အရောင်ရွေးချယ်ပါ:",
        reply_markup=get_color_keyboard()
    )

async def handle_color_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle color selection"""
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    
    if query.data.startswith('color_'):
        color_idx = int(query.data.split('_')[1])
        selected_color = HANDKERCHIEF_COLORS[color_idx]
        
        session = UserSession.get(user_id)
        session['current_item']['color'] = selected_color
        session['stage'] = 'flower_selection'
        UserSession.update(user_id, session)
        
        await query.edit_message_text(
            f"✅ ရွေးချယ်ထားသော အရောင်: *{selected_color}*\n\n"
            "ကျေးဇူးပြု၍ ပန်းအမျိုးအစားရွေးချယ်ပါ:",
            reply_markup=get_flower_keyboard(),
            parse_mode='Markdown'
        )
    elif query.data == 'back_to_color':
        await query.edit_message_text(
            "ကျေးဇူးပြု၍ အရောင်ရွေးချယ်ပါ:",
            reply_markup=get_color_keyboard()
        )

async def handle_flower_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle flower selection"""
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    
    if query.data.startswith('flower_'):
        flower_idx = int(query.data.split('_')[1])
        selected_flower = FLOWERS[flower_idx]
        
        session = UserSession.get(user_id)
        session['current_item']['flower'] = selected_flower
        session['stage'] = 'name_input'
        UserSession.update(user_id, session)
        
        await query.edit_message_text(
            f"✅ ရွေးချယ်ထားသော အရောင်: *{session['current_item']['color']}*\n"
            f"✅ ရွေးချယ်ထားသော ပန်း: *{selected_flower}*\n\n"
            "ကျေးဇူးပြု၍ လက်ကိုင်ပုဝါပေါ်မှာ ထိုးမယ့် နာမည်ကို ရိုက်ထည့်ပါ:",
            parse_mode='Markdown'
        )
        
        return WAITING_NAME

async def handle_name_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle name input for handkerchief"""
    user_id = update.effective_user.id
    name_on_handkerchief = update.message.text.strip()
    
    session = UserSession.get(user_id)
    session['current_item']['name'] = name_on_handkerchief
    session['current_item']['price'] = HANDKERCHIEF_PRICE
    session['current_item']['type'] = 'လက်ကိုင်ပုဝါ'
    session['stage'] = 'confirmation'
    UserSession.update(user_id, session)
    
    summary = (
        "📋 *အတည်ပြုချက်*\n\n"
        f"🧣 ပစ္စည်း: လက်ကိုင်ပုဝါ\n"
        f"🎨 အရောင်: {session['current_item']['color']}\n"
        f"🌸 ပန်း: {session['current_item']['flower']}\n"
        f"✍️ နာမည်: {name_on_handkerchief}\n"
        f"💰 စျေးနှုန်း: {HANDKERCHIEF_PRICE:,} Ks\n\n"
        "အတည်ပြုပြီး Cart ထဲထည့်မလား?"
    )
    
    await update.message.reply_text(
        summary,
        reply_markup=get_confirmation_keyboard(),
        parse_mode='Markdown'
    )
    
    return ConversationHandler.END

async def handle_add_to_cart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Add item to cart"""
    query = update.callback_query
    await query.answer("✅ Cart ထဲသို့ ထည့်ပြီးပါပြီ!")
    user_id = update.effective_user.id
    
    session = UserSession.get(user_id)
    session['cart'].append(session['current_item'].copy())
    session['current_item'] = {}
    session['stage'] = 'cart_review'
    UserSession.update(user_id, session)
    
    cart_summary = "🛒 *Your Cart*\n\n"
    total = 0
    for idx, item in enumerate(session['cart'], 1):
        cart_summary += f"{idx}. {item['type']}\n"
        cart_summary += f"   • အရောင်: {item['color']}\n"
        cart_summary += f"   • ပန်း: {item['flower']}\n"
        cart_summary += f"   • နာမည်: {item['name']}\n"
        cart_summary += f"   • စျေးနှုန်း: {item['price']:,} Ks\n\n"
        total += item['price']
    
    cart_summary += f"💰 *စုစုပေါင်း: {total:,} Ks*\n\n"
    cart_summary += "မှာယူမလား?"
    
    await query.edit_message_text(
        cart_summary,
        reply_markup=get_cart_keyboard(),
        parse_mode='Markdown'
    )

async def handle_confirm_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start collecting user information"""
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    
    session = UserSession.get(user_id)
    session['stage'] = 'collecting_info'
    UserSession.update(user_id, session)
    
    await query.edit_message_text(
        "ကျေးဇူးပြု၍ သင်၏ အမည်ကို ရိုက်ထည့်ပါ:"
    )

async def collect_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Collect customer name"""
    user_id = update.effective_user.id
    name = update.message.text.strip()
    
    session = UserSession.get(user_id)
    session['user_info']['name'] = name
    UserSession.update(user_id, session)
    
    await update.message.reply_text(
        f"✅ အမည်: {name}\n\nကျေးဇူးပြု၍ ဖုန်းနံပါတ်ကို ရိုက်ထည့်ပါ:"
    )
    
    return WAITING_ADDRESS

async def collect_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Collect customer phone"""
    user_id = update.effective_user.id
    phone = update.message.text.strip()
    
    session = UserSession.get(user_id)
    session['user_info']['phone'] = phone
    UserSession.update(user_id, session)
    
    await update.message.reply_text(
        f"✅ ဖုန်းနံပါတ်: {phone}\n\nကျေးဇူးပြု၍ လိပ်စာအပြည့်အစုံကို ရိုက်ထည့်ပါ:"
    )

async def collect_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Collect customer address and show final confirmation"""
    user_id = update.effective_user.id
    address = update.message.text.strip()
    
    session = UserSession.get(user_id)
    session['user_info']['address'] = address
    UserSession.update(user_id, session)
    
    summary, total = format_order_summary(session['cart'], session['user_info'])
    
    await update.message.reply_text(
        summary + "\n\nအတည်ပြုပြီး မှာယူမလား?",
        reply_markup=get_final_confirmation_keyboard(),
        parse_mode='Markdown'
    )

async def place_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Place the final order and notify owner"""
    query = update.callback_query
    await query.answer("✅ မှာယူမှု အောင်မြင်ပါသည်!")
    user_id = update.effective_user.id
    
    session = UserSession.get(user_id)
    
    # Generate order ID
    order_id = generate_order_id('handkerchief')
    
    # Send confirmation to customer
    summary, total = format_order_summary(session['cart'], session['user_info'])
    customer_message = (
        f"✅ *မှာယူမှု အောင်မြင်ပါပြီ!*\n\n"
        f"📝 Order ID: `{order_id}`\n\n"
        f"{summary}\n"
        f"💵 *ငွေကြိုရှင်း လိုအပ်ပါမယ်ရှင့်*\n\n"
        f"ကျေးဇူးတင်ပါတယ်! 🙏"
    )
    
    await query.edit_message_text(
        customer_message,
        parse_mode='Markdown'
    )
    
    # Notify owner
    owner_message = format_owner_notification(
        order_id,
        session['cart'],
        session['user_info'],
        update.effective_user.username
    )
    
    try:
        await context.bot.send_message(
            chat_id=config.OWNER_TELEGRAM_ID,
            text=owner_message,
        )
    except Exception as e:
        print(f"Error sending to owner: {e}")
    
    # Clear session
    UserSession.clear(user_id)
    
    # Show main menu again
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="ထပ်မံမှာယူလိုပါသလား?",
        reply_markup=get_main_menu_keyboard()
    )

async def cancel_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel the order"""
    query = update.callback_query
    await query.answer("မှာယူမှု ပယ်ဖျက်ပြီးပါပြီ")
    user_id = update.effective_user.id
    
    UserSession.clear(user_id)
    
    await query.edit_message_text(
        "မှာယူမှု ပယ်ဖျက်ပြီးပါပြီ။\n\nထပ်မံမှာယူလိုပါသလား?",
        reply_markup=get_main_menu_keyboard()
    )
