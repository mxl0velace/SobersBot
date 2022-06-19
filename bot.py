import discord
from os import getenv
from dotenv import load_dotenv
from cogs import minecraft

class SobersBot:
    def __init__(self):
        """ Get bot token and set up bot. """
        self.token = getenv('DISCORD_BOT_TOKEN')

        self.bot = discord.Bot(activity = discord.Activity(type=discord.ActivityType.watching, name="you play Minecraft"))

        # Add cogs to our bot:
        self.cogs = [
            {'name': 'Minecraft', 'obj': minecraft.Minecraft, 'active': True},
        ]

        self.add_events()
        self.init_cogs()

    def add_events(self):
        """ Add on_ready() event to bot. We can add more events here in future if required. """
        self.bot.event(self.on_ready)

    async def on_ready(self):
        """ Print output to terminal once bot has successfully connected to Discord """
        print(f'{self.bot.user.name} has connected to Discord!')

    def start_bot(self):
        """ Start our bot with our TOKEN """
        self.bot.run(self.token)

    def init_cogs(self):
        """ Loop through all cogs in our list and add them to our Bot """
        for cog in self.cogs:
            self.bot.add_cog(cog['obj'](self.bot))


if __name__ == '__main__':
    # Load our secret environment variables
    load_dotenv('.env')

    # Initialize our bot
    b = SobersBot()

    # Start our bot
    print("Starting bot (Sobers)")
    b.start_bot()