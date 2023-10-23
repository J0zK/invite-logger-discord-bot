import disnake
from disnake.ext import commands
import os

loc = os.path.dirname(__file__)
with open(loc+'/key.txt', 'r') as key:
    key = key.read()


class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='h.', intents=disnake.Intents.all(), activity=disnake.Activity(type=disnake.ActivityType.playing, name='Invite logger'), help_command=None)
        self.invites = []
    async def on_ready(self):
        [Invite(invite.inviter, invite.id, invite.guild, invite.uses) for guild in self.guilds for invite in await guild.invites()]
        print('Ready!')
    async def on_member_join(self, member):
        if member.bot is False:
            invite_selected = [invite for invite in self.invites for inv in await member.guild.invites() if inv.id == invite.id and invite.guild == member.guild and inv.uses > invite.uses]
            if invite_selected != []:
                invite_selected = invite_selected[0]
                invite_selected.uses += 1
                print(f'{member.name} has joined to {member.guild.name}\nInvitation used: {invite_selected.id}\nCreator: {invite_selected.creator}')
            else:
                print(f'{member.name} has joined to {member.guild.name} but invite has not found.')
    async def on_invite_create(self, invite):
        Invite(invite.inviter, invite.id, invite.guild, invite.uses)
    async def on_invite_delete(self, invite):
        invite_selected = [inv for inv in self.invites if invite.id == invite.id]
        if invite_selected != []:
            del(invite_selected[0])


class Invite:
    def __init__(self, creator:disnake.User, id:int, guild:disnake.Guild ,uses:int) -> None:
        self.creator, self.id , self.guild, self.uses = creator, id, guild, uses
        bot.invites.append(self)


bot = Client()
bot.run(key)