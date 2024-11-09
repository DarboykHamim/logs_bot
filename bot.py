import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Telegram bot token
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
AUTHORIZED_USER_ID = 123456789  # Replace with the authorized user's Telegram user ID

# API endpoint
API_URL = "https://noxsword.serv00.net/logs.php?find="

# Define command handler for the '/findlogs' command
async def find_logs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    # Check if the user is authorized
    if user_id != AUTHORIZED_USER_ID:
        await update.message.reply_text("You are not authorized to use this bot.")
        return

    # Check if a search term was provided
    if not context.args:
        await update.message.reply_text("Please provide a search term after /findlogs.")
        return

    # Join all arguments to form the search query
    search_term = " ".join(context.args)
    
    # Fetch logs from the API
    try:
        response = requests.get(f"{API_URL}{search_term}")
        response.raise_for_status()
        logs = response.json()

        # Limit the logs to 30 entries
        logs = logs[:30]

        # Check if logs were found
        if not logs:
            await update.message.reply_text("No logs found for the given search term.")
            return

        # Format and send logs in batches to avoid Telegram's message size limit
        log_messages = []
        for log in logs:
            log_messages.append(str(log))
        
        log_text = "\n".join(log_messages)
        await update.message.reply_text(log_text)
    
    except requests.exceptions.RequestException as e:
        await update.message.reply_text(f"Error fetching logs: {e}")

# Define the main function to run the bot
def main():
    # Create the bot application
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Add the /findlogs command handler
    application.add_handler(CommandHandler("findlogs", find_logs))

    # Run the bot
    application.run_polling()

if __name__ == "__main__":
    main()
