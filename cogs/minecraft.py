from discord.ext import commands
from discord.commands import slash_command, Option, permissions
from mcstatus import MinecraftServer
from os import getenv
from mcrcon import MCRcon

SOBERS_ID = 688078632689598516 # Sober Socials
TEST_ID = 751405284836114453 # Test Server
TEST_ROLE_ID = 800318488798560286 # Bee, in Test Server
CMT_ID = 688080042613276792 # Committee, in Sober Socials
VERIFIED_ID = 695059499219681393 # Verified Member, in Sober Socials
testGuilds = [TEST_ID, SOBERS_ID]

class Minecraft(commands.Cog):
    """Minecraft specific commands."""

    def __init__(self, bot):
        self.bot = bot
        self.host = getenv('SERVER_IP')
        self.query_port = int(getenv('QUERY_PORT'))
        self.rcon_port = int(getenv('RCON_PORT'))
        self.rcon_pwd = getenv('RCON_PASSWORD')

        # Init our endpoints / Create connection
        self.query_server = MinecraftServer(self.host)
        
    @slash_command(name='status', description="Check our Minecraft server status.", guild_ids=testGuilds)
    @permissions.has_role("Committee")  # <= Checks for admin rights
    async def status(self, ctx):
        """ Get server status using MinecraftServer """
        status = self.query_server.status()
        await ctx.respond(f"The server has {status.players.online} players and replied in {status.latency} ms")

    @slash_command(name='msg', description="Message the server or a player.", guild_ids=testGuilds, permissions=[permissions.Permission(id=TEST_ROLE_ID, type=1, permission=True)])
    async def msg(self, ctx, msg : Option(str, "Message to send"), player : Option(str, "The player to message", required=False)):
        """ Message server or a specific player """
        if player is None:
            with MCRcon(host=self.host, password=self.rcon_pwd, port=self.rcon_port) as mcr:
                mcr.command(f"say {msg}")
                await ctx.respond(f"Messaged Minecraft server", ephemeral=True)
        else:
            with MCRcon(host=self.host, password=self.rcon_pwd, port=self.rcon_port) as mcr:
                resp = mcr.command(f"tell {player} {msg}")
                await ctx.respond(f"Server response: {resp}", ephemeral=True)

    @slash_command(name='whitelist', description="Add yourself to the Minecraft server whitelist", guild_ids=testGuilds)
    @permissions.has_role("Verified Member")
    async def whitelist(self, ctx, username:str):
        """ Whitelist a player on the server """
        if username == None: # Should be avoided by using slash commands, kept in for legacy
            await ctx.respond("Usage: /whitelist <your minecraft username>", ephemeral=True)
        else:
            with MCRcon(host=self.host, password=self.rcon_pwd, port=self.rcon_port) as mcr:
                resp = mcr.command(f"whitelist add {username}")
                print(f"User {ctx.author.name} ({ctx.author.nick}) added {username} to the whitelist.")
                print(resp)
                await ctx.respond(f"Whitelisted user {username}.")