import asyncio
from datetime import datetime

from FreakyUserbot.utils import Freaky_on_cmd, sudo_cmd

Hackfreaksthumb = "./resources/FreakyUserbot.png"


@Freaky.on(Freaky_on_cmd(pattern="send ?(.*)"))
@Freaky.on(sudo_cmd(pattern="send ?(.*)", allow_sudo=True))
async def send(event):
    if event.fwd_from:
        return
    message_id = event.message.id
    input_str = event.pattern_match.group(1)
    start = datetime.now()
    the_plugin_file = "./FreakyUserbot/modules/{}.py".format(input_str)
    end = datetime.now()
    (end - start).seconds
    men = f"Plugin Name - {input_str}.py \nUploaded By Freaky"
    await event.client.send_file(  # pylint:disable=E0602
        event.chat_id,
        the_plugin_file,
        thumb=Hackfreaksthumb,
        caption=men,
        force_document=True,
        allow_cache=False,
        reply_to=message_id,
    )
    await asyncio.sleep(5)
    await event.delete()
