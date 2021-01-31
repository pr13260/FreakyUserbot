"""use command .ducduckgo"""

from uniborg.util import Freaky_on_cmd

from FreakyUserbot import CMD_HELP


@Freaky.on(Freaky_on_cmd("ducduckgo (.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    sample_url = "https://duckduckgo.com/?q={}".format(input_str.replace(" ", "+"))
    if sample_url:
        link = sample_url.rstrip()
        await event.edit(
            "Let me 🦆 DuckDuckGo that for you:\n🔎 [{}]({})".format(input_str, link)
        )
    else:
        await event.edit("something is wrong. please try again later.")


CMD_HELP.update(
    {
        "duckduckgo": "**Duckduckgo**\
\n\n**Syntax : **`.ducduckgo <query>`\
\n**Usage :** get duckduckgo search query link"
    }
)
