from time import sleep

from telegram import Bot, Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.error import BadRequest, Unauthorized, ChatMigrated, TimedOut
from telegram.ext import CommandHandler, CallbackQueryHandler, run_async

from tg_bot import dispatcher, OWNER_ID, DEV_USERS
from tg_bot.modules.helper_funcs.chat_status import dev_plus

import tg_bot.modules.sql.users_sql as user_sql
import tg_bot.modules.sql.global_bans_sql as gban_sql


def get_invalid_chats(bot: Bot, update: Update, remove: bool = False):

    chats = user_sql.get_all_chats()
    kicked_chats = 0
    chat_list = []
    for chat in chats:

        id = chat.chat_id
        sleep(0.1)
        try:
            bot.get_chat(id, timeout=60)
        except (BadRequest, Unauthorized):
            kicked_chats += 1
            chat_list.append(id)
        except TimedOut:
            pass

    if not remove:
        return kicked_chats
    else:
        for muted_chat in chat_list:
            sleep(0.1)
            user_sql.rem_chat(muted_chat)
        return kicked_chats


def get_invalid_gban(bot: Bot, update: Update, remove: bool = False):

    banned = gban_sql.get_gban_list()
    ungbanned_users = 0
    ungban_list = []

    for user in banned:
        user_id = user["user_id"]
        sleep(0.1)
        try:
            bot.get_chat(user_id)
        except BadRequest:
            ungbanned_users += 1
            ungban_list.append(user_id)
        except TimedOut:
            pass

    if not remove:
        return ungbanned_users
    else:
        for user_id in ungban_list:
            sleep(0.1)
            gban_sql.ungban_user(user_id)
        return ungbanned_users


@run_async
@dev_plus
def dbcleanup(bot: Bot, update: Update):

    msg = update.effective_message

    msg.reply_text("Getting invalid chat count ...")
    invalid_chat_count = get_invalid_chats(bot, update)

    msg.reply_text("Getting invalid gbanned count ...")
    invalid_gban_count = get_invalid_gban(bot, update)

    reply = "Total invalid chats - {}\n".format(invalid_chat_count)
    reply += "Total invalid gbanned users - {}".format(invalid_gban_count)

    buttons = [
        [InlineKeyboardButton("Cleanup DB", callback_data=f"db_cleanup")]
    ]

    update.effective_message.reply_text(reply, reply_markup=InlineKeyboardMarkup(buttons))


def get_muted_chats(bot: Bot, update: Update, leave: bool = False):

    chats = user_sql.get_all_chats()
    muted_chats = 0
    chat_list = []
    for chat in chats:
        id = chat.chat_id
        sleep(0.1)
        try:
            bot.send_chat_action(id, "TYPING", timeout=60)
        except (BadRequest, Unauthorized):
            muted_chats += +1
            chat_list.append(id)
        except ChatMigrated:
            pass

    if not leave:
        return muted_chats
    else:
        for muted_chat in chat_list:
            sleep(0.1)
            try:
                bot.leaveChat(muted_chat, timeout=60)
            except BadRequest:
                pass
            user_sql.rem_chat(muted_chat)
        return muted_chats


@run_async
@dev_plus
def leave_muted_chats(bot: Bot, update: Update):

    message = update.effective_message
    progress_message = message.reply_text("Getting chat count ...")
    muted_chats = get_muted_chats(bot, update)

    buttons = [
        [InlineKeyboardButton("Leave chats", callback_data=f"db_leave_chat")]
    ]

    update.effective_message.reply_text(f"I am muted in {muted_chats} chats.", reply_markup=InlineKeyboardMarkup(buttons))
    progress_message.delete()


@run_async
def callback_button(bot: Bot, update: Update):

    query = update.callback_query
    message = query.message
    chat_id = update.effective_chat.id
    query_type = query.data

    admin_list = [OWNER_ID] + DEV_USERS
    
    bot.answer_callback_query(query.id)
    if query_type == "db_leave_chat":
        if query.from_user.id in admin_list:
            message.delete()
            progress_message = message.reply_text("Leaving chats ...")
            chat_count = get_muted_chats(bot, update, True)
            progress_message.delete()
            bot.sendMessage(chat_id, f"Left {chat_count} chats.")
        else:
            query.answer("You are not allowed to use this.")
    elif query_type == "db_cleanup":
        if query.from_user.id in admin_list:
            message.delete()
            progress_message = message.reply_text("Cleaning up DB ...")
            invalid_chat_count = get_invalid_chats(bot, update, True)
            invalid_gban_count = get_invalid_gban(bot, update, True)
            progress_message.delete()
            reply = "Cleaned up {} chats and {} gbanned users from db.".format(invalid_chat_count, invalid_gban_count)
            bot.sendMessage(chat_id, reply)
        else:
            query.answer("You are not allowed to use this.")



DB_CLEANUP_HANDLER = CommandHandler("dbcleanup", dbcleanup)
LEAVE_MUTED_CHATS_HANDLER = CommandHandler("leavemutedchats", leave_muted_chats)
BUTTON_HANDLER = CallbackQueryHandler(callback_button, pattern='db_.*')

dispatcher.add_handler(DB_CLEANUP_HANDLER)
dispatcher.add_handler(LEAVE_MUTED_CHATS_HANDLER)
dispatcher.add_handler(BUTTON_HANDLER)

__mod_name__ = "DB Cleanup"