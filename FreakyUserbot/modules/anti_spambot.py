# From CatUserbot , And Yes I am Noob

import spamwatch
from requests import get
from telethon import events
from telethon.errors import ChatAdminRequiredError
from telethon.tl.types import ChannelParticipantsAdmins

from FreakyUserbot import BOTLOG, BOTLOG_CHATID, CMD_HELP, LOGS
from FreakyUserbot.modules.sql_helper.gban_sql import get_gbanuser, is_gbanned
from FreakyUserbot.utils import Freaky_on_cmd, is_admin

if Config.ANTI_SPAMBOT:

    @Freaky.on(events.ChatAction())
    async def anti_spambot(event):
        if not event.user_joined and not event.user_added:
            return
        chat = event.chat_id
        user = await event.get_user()
        freakadmin = await is_admin(bot, chat, bot.uid)
        if not freakadmin:
            return
        freakbanned = None
        adder = None
        ignore = None
        if event.user_added:
            try:
                adder = event.action_message.sender_id
            except AttributeError:
                return
        async for admin in event.client.iter_participants(
            event.chat_id, filter=ChannelParticipantsAdmins
        ):
            if admin.id == adder:
                ignore = True
                break
        if ignore:
            return
        if is_gbanned(user.id):
            freakgban = get_gbanuser(user.id)
            if freakgban.reason:
                hmm = await event.reply(
                    f"[{user.first_name}](tg://user?id={user.id}) was gbanned by you for the reason `{freakgban.reason}`"
                )
            else:
                hmm = await event.reply(
                    f"[{user.first_name}](tg://user?id={user.id}) was gbanned by you"
                )
            try:
                await bot.edit_permissions(chat, user.id, view_messages=False)
                freakbanned = True
            except Exception as e:
                LOGS.info(e)
        if spamwatch and not freakbanned:
            ban = spamwatch.get_ban(user.id)
            if ban:
                hmm = await event.reply(
                    f"[{user.first_name}](tg://user?id={user.id}) was banned by spamwatch for the reason `{ban.reason}`"
                )
                try:
                    await bot.edit_permissions(chat, user.id, view_messages=False)
                    freakbanned = True
                except Exception as e:
                    LOGS.info(e)
        if not freakbanned:
            try:
                casurl = "https://api.cas.chat/check?user_id={}".format(user.id)
                data = get(casurl).json()
            except Exception as e:
                LOGS.info(e)
                data = None
            if data and data["ok"]:
                reason = (
                    f"[Banned by Combot Anti Spam](https://cas.chat/query?u={user.id})"
                )
                hmm = await event.reply(
                    f"[{user.first_name}](tg://user?id={user.id}) was banned by Combat anti-spam service(CAS) for the reason check {reason}"
                )
                try:
                    await bot.edit_permissions(chat, user.id, view_messages=False)
                    freakbanned = True
                except Exception as e:
                    LOGS.info(e)
        if BOTLOG and freakbanned:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#ANTISPAMBOT\n"
                f"**User :** [{user.first_name}](tg://user?id={user.id})\n"
                f"**Chat :** {event.chat.title} (`{event.chat_id}`)\n"
                f"**Reason :** {hmm.text}",
            )


@Freaky.on(Freaky_on_cmd(pattern="cascheck$"))
async def caschecker(cas):
    freakevent = await edit_or_reply(
        cas,
        "`checking any cas(combot antispam service) banned users here, this may take several minutes too......`",
    )
    text = ""
    chat = cas.chat_id
    try:
        info = await cas.client.get_entity(chat)
    except (TypeError, ValueError) as err:
        await cas.edit(str(err))
        return
    try:
        cas_count, members_count = (0,) * 2
        banned_users = ""
        async for user in cas.client.iter_participants(info.id):
            if banchecker(user.id):
                cas_count += 1
                if not user.deleted:
                    banned_users += f"{user.first_name}-`{user.id}`\n"
                else:
                    banned_users += f"Deleted Account `{user.id}`\n"
            members_count += 1
        text = "**Warning!** Found `{}` of `{}` users are CAS Banned:\n".format(
            cas_count, members_count
        )
        text += banned_users
        if not cas_count:
            text = "No CAS Banned users found!"
    except ChatAdminRequiredError:
        await freakevent.edit("`CAS check failed: Admin privileges are required`")
        return
    except BaseException:
        await freakevent.edit("`CAS check failed`")
        return
    await freakevent.edit(text)


@Freaky.on(Freaky_on_cmd(pattern="swcheck$"))
async def caschecker(cas):
    text = ""
    chat = cas.chat_id
    freakevent = await edit_or_reply(
        cas,
        "`checking any spamwatch banned users here, this may take several minutes too......`",
    )
    try:
        info = await cas.client.get_entity(chat)
    except (TypeError, ValueError) as err:
        await cas.edit(str(err))
        return
    try:
        cas_count, members_count = (0,) * 2
        banned_users = ""
        async for user in cas.client.iter_participants(info.id):
            if spamchecker(user.id):
                cas_count += 1
                if not user.deleted:
                    banned_users += f"{user.first_name}-`{user.id}`\n"
                else:
                    banned_users += f"Deleted Account `{user.id}`\n"
            members_count += 1
        text = "**Warning! **Found `{}` of `{}` users are spamwatch Banned:\n".format(
            cas_count, members_count
        )
        text += banned_users
        if not cas_count:
            text = "No spamwatch Banned users found!"
    except ChatAdminRequiredError:
        await freakevent.edit("`spamwatch check failed: Admin privileges are required`")
        return
    except BaseException:
        await freakevent.edit("`spamwatch check failed`")
        return
    await freakevent.edit(text)


def banchecker(user_id):
    try:
        casurl = "https://api.cas.chat/check?user_id={}".format(user_id)
        data = get(casurl).json()
    except Exception as e:
        LOGS.info(e)
        data = None
    return bool(data and data["ok"])


def spamchecker(user_id):
    ban = None
    if spamwatch:
        ban = spamwatch.get_ban(user_id)
    return bool(ban)


CMD_HELP.update(
    {
        "antispambot": "**Plugin : **`antispambot`\
        \n\n**Syntax : **`.cascheck`\
        \n**Function : **__Searches for cas(combot antispam service) banned users in group and shows you the list__\
        \n\n**Syntax : **`.swcheck`\
        \n**Function : **__Searches for spamwatch banned users in group and shows you the list__"
    }
)
