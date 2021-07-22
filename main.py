import discord
from discord.ext import commands
import datetime
import asyncio
import random
import os

client = discord.Client()

# @client.event
# async def on_ready():
#     print('We have logged in as {0.user}'.format(client))

# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return

#     if message.content.startswith('#Yo'):
#         await message.channel.send('YOU GET A PRIZE AND YOU GET A PRIZE AND YOU GET A PRIZE, YOU ALL GET PRIZES!')


client = commands.Bot(command_prefix=">")

def convert(time):
    pos = ["s", "m", "h", "d"]

    time_dict = {"s": 1, "m": 60, "h": 3600, "d": 3600 * 24}

    unit = time[-1]

    if unit not in pos:
        return -1
    try:
        val = int(time[:-1])
    except:
        return -2

    return val * time_dict[unit]

# async def gstart(ctx, mins: int, *, prize: str):

@client.command()
@commands.has_role("High Council")
async def giveaway(ctx):
    await ctx.send("Time to giveaway some goodies!")

    questions = ["Which channel should it be hosted in?",
                 "what long should the giveaway be? [s|m|h|d]",
                 "What is the prize?"
                 ]
    answers = []

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    for i in questions:
        await ctx.send(i)

        try:
            msg = await client.wait_for('message', timeout=300.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send("You didn't answer in time, gotta be quick!!")
            return
        else:
            answers.append(msg.conent)

    try:
        c_id = int(answers[0][2:-1])
    except:
        await ctx.send(f"You didn't give me a proper channel name! Do it like: {ctx.channel.mention}")
        return

    channel = client.get_channel(c_id)

    time = convert(answers[1])
    if time == -1:
        await ctx.send(f"You didn't answer with a proper unit of time. Use: s, m, h, or d")
        return
    elif time == -2:
        await ctx.send(f"The time must be an integer, you doughnut!")
        return
    prize = answers[2]
    await ctx.send(f"The giveaway will be hosted in {channel.mention} and will last {answers[1]}'s!")

    embed = discord.Embed(title="Giveaway!", description=f"{prize}", color=ctx.author.color)
    embed.add_field(name="Hosted by: ", value=ctx.author.mention)
    embed.set_footer(text=f"Ends {answers[1]}'s from now!")

    my_msg = await ctx.send(embed=embed)

    await my_msg.add_reaction("🎉")

    await asyncio.sleep(time)

    new_msg = await channel.fetch_message(my_msg.id)

    users = await new_msg.reactions[0].users().flatten()
    users.pop(users.index(client.users))

    winner = random.choice(users)

    await channel.send(f"Congratulations, {winner.mention}, you won!!!! {prize}")


@client.command()
@commands.has_role("High Council")
async def reroll(ctx, channel: discord.TextChannel, id_, int):
    try:
        new_msg = await channel.fetch_message((id_))
    except:
        await ctx.send("Wrong ID!")
        return

    users = await new_msg.reactions[0].users().flatten()
    users.pop(users.index(client.users))

    winner = random.choice(users)

    await channel.send(f"Congratulations, {winner.mention}, you won!!!!")

    # end = datetime.datetime.utcnow() + datetime.timedelta(seconds=mins * 60)

my_secret = os.environ['TOKEN']
client.run(my_secret)
