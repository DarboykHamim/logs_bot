import logging
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram.ext import Filters

# Your Bot's token
TOKEN = '7589124589:AAHRqzCUFBRXc7pj_94uzYXHraTObAp6Y48'

# List of authorized user IDs (Initially empty or pre-set list)
authorized_users = [123456789, 987654321]  # Replace with actual user IDs

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to get logs from the API
def fetch_logs(keyword: str):
    url = f"https://noxsword.serv00.net/logs.php?find={keyword}"
    try:
        response = requests.get(url)
        logs = response.json()  # assuming API returns JSON
        return logs[:30]  # return first 30 logs
    except requests.RequestException as e:
        logger.error(f"Error fetching logs: {e}")
        return None

# Command: /free <keyword>
def free(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    
    # Check if user is authorized
    if user_id not in authorized_users:
        update.message.reply_text("You are not authorized to use this command.")
        return

    # Get the keyword from the command argument
    if len(context.args) < 1:
        update.message.reply_text("Please provide a keyword to search for.")
        return

    keyword = context.args[0]

    # Fetch logs based on the keyword
    logs = fetch_logs(keyword)
    if not logs:
        update.message.reply_text("No logs found or error fetching logs.")
        return

    # Send the logs to the user (first 30 logs)
    for log in logs:
        update.message.reply_text(log)  # Assuming the log is a string

# Command: /start
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome to the Log Finder Bot! Use /free <keyword> to search logs.")

# Command: /adduser <user_id>
def add_user(update: Update, context: CallbackContext):
    # Only allow the bot owner (use the user ID of the bot owner)
    bot_owner_id = 123456789  # Replace with your Telegram user ID
    
    # Get the user ID of the sender
    user_id = update.message.from_user.id
    
    # Check if the user is the bot owner
    if user_id != bot_owner_id:
        update.message.reply_text("You are not authorized to add users.")
        return
    
    # Ensure the command includes a user ID
    if len(context.args) < 1:
        update.message.reply_text("Please provide the user ID to add.")
        return
    
    # Get the user ID from the command argument
    try:
        new_user_id = int(context.args[0])
    except ValueError:
        update.message.reply_text("Invalid user ID. Please provide a valid numeric user ID.")
        return
    
    # Add the user to the authorized users list if not already added
    if new_user_id not in authorized_users:
        authorized_users.append(new_user_id)
        update.message.reply_text(f"User ID {new_user_id} has been added as a free user.")
    else:
        update.message.reply_text(f"User ID {new_user_id} is already a free user.")

# Command: /removeuser <user_id>
def remove_user(update: Update, context: CallbackContext):
    # Only allow the bot owner (use the user ID of the bot owner)
    bot_owner_id = 123456789  # Replace with your Telegram user ID
    
    # Get the user ID of the sender
    user_id = update.message.from_user.id
    
    # Check if the user is the bot owner
    if user_id != bot_owner_id:
        update.message.reply_text("You are not authorized to remove users.")
        return
    
    # Ensure the command includes a user ID
    if len(context.args) < 1:
        update.message.reply_text("Please provide the user ID to remove.")
        return
    
    # Get the user ID from the command argument
    try:
        remove_user_id = int(context.args[0])
    except ValueError:
        update.message.reply_text("Invalid user ID. Please provide a valid numeric user ID.")
        return
    
    # Remove the user from the authorized users list if present
    if remove_user_id in authorized_users:
        authorized_users.remove(remove_user_id)
        update.message.reply_text(f"User ID {remove_user_id} has been removed from the free users list.")
    else:
        update.message.reply_text(f"User ID {remove_user_id} is not a free user.")

def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("free", free, pass_args=True))
    dispatcher.add_handler(CommandHandler("adduser", add_user, pass_args=True))
    dispatcher.add_handler(CommandHandler("removeuser", remove_user, pass_args=True))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you send a signal to stop (Ctrl+C)
    updater.idle()

if __name__ == '__main__':
    main()
