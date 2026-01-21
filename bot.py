# ==================== bot.py (Main) ====================
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import handlers.start as start_handler
import handlers.handkerchief as handkerchief_handler
import config
from database.models import UserSession
import asyncio
from aiohttp import web

# Dummy web server for Render (to keep it alive)
async def health_check(request):
    return web.Response(text="🤖 Myanimalist Bot is running!")

async def start_web_server():
    """Start a simple web server to satisfy Render's port requirement"""
    app = web.Application()
    app.router.add_get('/', health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()
    print("🌐 Web server started on port 8080")

async def handle_text_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle all text inputs based on user's current stage"""
    user_id = update.effective_user.id
    session = UserSession.get(user_id)
    stage = session.get('stage', 'start')
    
    if stage == 'name_input':
        await handkerchief_handler.handle_name_input(update, context)
    elif stage == 'collecting_info':
        # Determine which info we're collecting based on what's already filled
        if 'name' not in session['user_info']:
            await handkerchief_handler.collect_name(update, context)
        elif 'phone' not in session['user_info']:
            await handkerchief_handler.collect_phone(update, context)
        elif 'address' not in session['user_info']:
            await handkerchief_handler.collect_address(update, context)

async def main():
    """Start the bot and web server"""
    # Start web server first
    await start_web_server()
    
    # Build bot application
    application = Application.builder().token(config.BOT_TOKEN).build()
    
    # Start command
    application.add_handler(CommandHandler("start", start_handler.start))
    
    # Callback handlers
    application.add_handler(CallbackQueryHandler(start_handler.button_callback, pattern='^category_'))
    application.add_handler(CallbackQueryHandler(start_handler.button_callback, pattern='^back_to_main$'))
    application.add_handler(CallbackQueryHandler(handkerchief_handler.handle_color_selection, pattern='^color_'))
    application.add_handler(CallbackQueryHandler(handkerchief_handler.handle_color_selection, pattern='^back_to_color$'))
    application.add_handler(CallbackQueryHandler(handkerchief_handler.handle_flower_selection, pattern='^flower_'))
    application.add_handler(CallbackQueryHandler(handkerchief_handler.handle_add_to_cart, pattern='^confirm_add_cart$'))
    application.add_handler(CallbackQueryHandler(handkerchief_handler.handle_confirm_order, pattern='^confirm_order$'))
    application.add_handler(CallbackQueryHandler(handkerchief_handler.place_order, pattern='^place_order$'))
    application.add_handler(CallbackQueryHandler(handkerchief_handler.cancel_order, pattern='^cancel_order$'))
    
    # Text message handler (for name, phone, address inputs)
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        handle_text_input
    ))
    
    print("🤖 Myanimalist Bot is running...")
    
    # Run bot with polling
    await application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    asyncio.run(main())