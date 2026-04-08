import config
from datetime import datetime

def generate_order_id(order_type):
    """Generate unique order ID"""
    counter = config.ORDER_COUNTERS[order_type]
    order_id = f"TELE_{order_type.upper()}_{counter:03d}"
    config.ORDER_COUNTERS[order_type] += 1
    return order_id

def format_order_summary(cart, user_info):
    """Format order summary for display"""
    summary = "📋 *Order Summary*\n\n"
    total = 0
    
    for idx, item in enumerate(cart, 1):
        summary += f"{idx}. {item['type']}\n"
        summary += f"   • အရောင်: {item['color']}\n"
        summary += f"   • ပန်း: {item['flower']}\n"
        summary += f"   • နာမည်: {item['name']}\n"
        summary += f"   • စျေးနှုန်း: {item['price']:,} Ks\n\n"
        total += item['price']
    
    summary += f"💰 *စုစုပေါင်း: {total:,} Ks*\n\n"
    summary += "👤 *Customer Information*\n"
    summary += f"📛 Name: {user_info.get('name', 'N/A')}\n"
    summary += f"📱 Phone: {user_info.get('phone', 'N/A')}\n"
    summary += f"📍 Address: {user_info.get('address', 'N/A')}\n"
    
    return summary, total

def format_owner_notification(order_id, cart, user_info, user_telegram):
    """Format notification message for owner - NO MARKDOWN"""
    message = f"🛍️ NEW ORDER\n"
    message += f"━━━━━━━━━━━━━━━━━\n\n"
    message += f"📝 Order ID: {order_id}\n\n"
    
    message += f"👤 Customer Details:\n"
    message += f"📛 Name: {user_info['name']}\n"
    message += f"📱 Phone: {user_info['phone']}\n"
    message += f"📍 Address: {user_info['address']}\n"
    message += f"💬 Telegram: @{user_telegram if user_telegram else 'N/A'}\n\n"
    
    message += f"📦 Order Items:\n"
    total = 0
    for idx, item in enumerate(cart, 1):
        message += f"\n{idx}. လက်ကိုင်ပုဝါ\n"
        message += f"   • အရောင်: {item['color']}\n"
        message += f"   • ပန်း: {item['flower']}\n"
        message += f"   • ထိုးမယ့်နာမည်: {item['name']}\n"
        message += f"   • စျေးနှုန်း: {item['price']:,} Ks\n"
        total += item['price']
    
    message += f"\n💰 Total: {total:,} Ks\n"
    message += f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    message += f"\n━━━━━━━━━━━━━━━━━\n"
    message += f"💵 ငွေကြိုရှင်း လိုအပ်ပါမယ် ✅"
    
    return message