import html

from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName
from telethon.utils import get_input_location

from HackfreaksUserbot import CMD_HELP, sclient
from HackfreaksUserbot.modules.sql_helper.gmute_sql import is_gmuted
from HackfreaksUserbot.modules.sql_helper.mute_sql import is_muted
from HackfreaksUserbot.utils import Hackfreaks_on_cmd, edit_or_reply, sudo_cmd


@Hackfreaks.on(Hackfreaks_on_cmd("info ?(.*)"))
@Hackfreaks.on(sudo_cmd("info ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    replied_user, error_i_a = await get_full_user(event)
    if replied_user is None:
        await edit_or_reply(event, str(error_i_a))
        return False
    replied_user_profile_photos = await borg(
        GetUserPhotosRequest(
            user_id=replied_user.user.id, offset=42, max_id=0, limit=80
        )
    )
    replied_user_profile_photos_count = "None"
    try:
        replied_user_profile_photos_count = replied_user_profile_photos.count
    except AttributeError:
        pass
    user_id = replied_user.user.id
    first_name = html.escape(replied_user.user.first_name)
    if first_name is not None:
        first_name = first_name.replace("\u2060", "")
    last_name = replied_user.user.last_name
    last_name = (
        last_name.replace("\u2060", "") if last_name else ("Last Name not found")
    )
    user_bio = replied_user.about
    if user_bio is not None:
        user_bio = html.escape(replied_user.about)
    common_chats = replied_user.common_chats_count
    try:
        dc_id, location = get_input_location(replied_user.profile_photo)
    except Exception as e:
        dc_id = "Unknown."
        str(e)
    shazam = replied_user_profile_photos_count
    if is_gmuted(user_id):
        is_gbanned = "This User Is Gbanned"
    elif not is_gmuted(user_id):
        is_gbanned = False
    if is_muted(user_id, "gmute"):
        is_gmutted = "User is Tapped."
    elif not is_muted(user_id, "gmute"):
        is_gmutted = False
    caption = f"""<b>Dᴇᴛᴀɪʟᴇᴅ UsᴇʀIɴғᴏ<b>
<b>ID</b>: <code>{user_id}</code>
<b>Pᴇʀᴍᴀɴᴇɴᴛ Lɪɴᴋ</b>: <a href='tg://user?id={user_id}'>Click Here</a>
<b>Fɪʀsᴛ Nᴀᴍᴇ</b>: <code>{first_name}</code>
<b>Lᴀsᴛ Nᴀᴍᴇ</b>: <code>{last_name}</code>
<b>Bɪᴏ</b>: <code>{user_bio}</code>
<b>DC ID</b>: <code>{dc_id}</code>
<b>Nᴜᴍʙᴇʀ ᴏғ Pʀᴏғɪʟᴇ Pɪᴄs</b>: <code>{shazam}</code>
<b>Is Rᴇsᴛʀɪᴄᴛᴇᴅ</b>: <code>{replied_user.user.restricted}</code>
<b>Is Vᴇʀɪғɪᴇᴅ ʙʏ Tᴇʟᴇɢʀᴀᴍ</b>: <code>{replied_user.user.verified}</code>
<b>Is Bᴏᴛ</b>: <code>{replied_user.user.bot}</code>
<b>Cᴏᴍᴍᴏɴ Cʜᴀᴛs</b>: <code>{common_chats}</code>
<b>Is Gʙᴀɴɴᴇᴅ</b>: <code>{is_gbanned}</code>
<b>Is Gᴍuᴛᴇᴅ</b>: <code>{is_gmutted}</code>
"""
    message_id_to_reply = event.message.reply_to_msg_id
    if not message_id_to_reply:
        message_id_to_reply = event.message.id
    await borg.send_message(
        event.chat_id,
        caption,
        reply_to=message_id_to_reply,
        parse_mode="HTML",
        file=replied_user.profile_photo,
        force_document=False,
        silent=True,
    )
    await event.delete()


async def get_full_user(event):
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.forward:
            replied_user = await event.client(
                GetFullUserRequest(
                    previous_message.forward.sender_id
                    or previous_message.forward.channel_id
                )
            )
            return replied_user, None
        else:
            replied_user = await event.client(
                GetFullUserRequest(previous_message.sender_id)
            )
            return replied_user, None
    else:
        input_str = None
        try:
            input_str = event.pattern_match.group(1)
        except IndexError as e:
            return None, e
        if event.is_private:
            try:
                user_id = event.chat_id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user, None
            except Exception as e:
                return None, e
        elif event.message.entities is not None:
            mention_entity = event.message.entities
            probable_user_mention_entity = mention_entity[0]
            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user, None
            else:
                try:
                    user_object = await event.client.get_entity(input_str)
                    user_id = user_object.id
                    replied_user = await event.client(GetFullUserRequest(user_id))
                    return replied_user, None
                except Exception as e:
                    return None, e
        else:
            try:
                user_object = await event.client.get_entity(int(input_str))
                user_id = user_object.id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user, None
            except Exception as e:
                return None, e


@Hackfreaks.on(Hackfreaks_on_cmd("cas ?(.*)"))
@Hackfreaks.on(sudo_cmd("cas ?(.*)", allow_sudo=True))
async def gibinfo(event):
    if not event.pattern_match.group(1):
        user = (
            (await event.get_reply_message()).sender if event.is_reply else event.sender
        )
        lolu = await event.client(GetFullUserRequest(user.id))
    else:
        try:
            lolu = await event.client(GetFullUserRequest(event.pattern_match.group(1)))
        except:
            await event.edit("<i>No User Found.</i>", parse_mode="HTML")
            return
    try:
        cas_url = f"https://combot.org/api/cas/check?user_id={lolu.user.id}"
        r = get(cas_url, timeout=3)
        data = r.json()
    except:
        data = None
    if data and data["ok"]:
        reason = f"<i>True</i>"
    else:
        reason = f"<i>False</i>"
    if sclient is None:
        oki = "<i>Token Invalid</i>"
    elif sclient:
        hmmyes = sclient.is_banned(lolu.user.id)
        if hmmyes:
            oki = f"""<i>True</i>
<b>~ Reason :</b> <i>{hmmyes.reason}</i>"""
        else:
            pass
    infomsg = (
        f"<b>CAS Iɴғᴏ Oғ</b> <a href=tg://user?id={lolu.user.id}>{lolu.user.first_name}</a>: \n"
        f"<b>- UsᴇʀNᴀᴍᴇ :</b> <i>{lolu.user.username}</i>\n"
        f"<b>- Iᴅ :</b> <i>{lolu.user.id}</i>\n"
        f"<b>- Bᴏᴛ :</b> <i>{lolu.user.bot}</i>\n"
        f"<b>- CAS Bᴀɴɴᴇᴅ :</b> {reason} \n"
    )
    await event.edit(infomsg, parse_mode="HTML")


CMD_HELP.update(
    {
        "information": "**Information**\
\n\n**Syntax : **`.info <mention a username/reply to a message>`\
\n**Usage :** Gives you information about the username.\
\n\n**Syntax : **`.cas <mention a username/reply to a message>`\
\n**Usage :** Shows if the person is banned in CAS or not."
    }
)
