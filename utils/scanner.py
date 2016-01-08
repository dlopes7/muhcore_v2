import os
import sys
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "muhcore.settings")

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

django.setup()

from battlenet import Connection as bnetConnection, Character as bnetCharacter, Guild as bnetGuild, UNITED_STATES
from core.models import Character, Guild


class Scanner(object):
    def __init__(self):
        self.connection = bnetConnection(public_key='nm3jrgp8avwjpqnptby38z763t9afyes',
                                         private_key='Edt6pnruq8ntrE4YnwnBX4ckBnMddbf8', locale='en')

    def populate(self, battlegroup, realm, name):
        guild = self.connection.get_guild(battlegroup, realm, name, fields=[bnetGuild.MEMBERS])
        print('Obtained guild {name} @ {realm} with {members} members'.format(name=guild.name,
                                                                              realm=guild.realm,
                                                                              members=len(guild.members)))

        guild_model, created = Guild.objects.get_or_create(guild_id='{name}@{realm}'.format(name=guild.name,
                                                                                            realm=guild.realm))

        guild_model.number_members = len(guild.members)
        guild_model.name = guild.name
        guild_model.realm = guild.realm

        guild_model.save()

        for member in guild.members:
            char = member['character']
            if char.level == 100:
                char_all = self.connection.get_character(battlegroup, realm, name,
                                                         fields=[bnetCharacter.ITEMS,
                                                                 bnetCharacter.TALENTS])

                print(char.name, char_all.get_class_name())

                char_model = Character.objects.get_or_create(name=char.name,
                                                             )


def create_specs():
    print('Creating specs...')
    specs = {'Death Knight': {'color': '#C41F3B',
                              'specs': ['Unholy',
                                        'Frost',
                                        'Blood']},
             'Druid': {'color': '#FF7D0A',
                       'specs': ['Balance',
                                 'Guardian',
                                 'Feral',
                                 'Restoration']},
             'Hunter': {'color': '#ABD473',
                        'specs': ['Marksmanshipt',
                                  'Beast Mastery',
                                  'Survival']},
             'Mage': {'color': '#69CCF0',
                      'specs': ['Arcane',
                                'Fire',
                                'Frost']},
             'Monk': {'color': '#00FF96',
                      'specs': ['Mistweaver',
                                'Brewmaster',
                                'Windwalker']},
             'Paladin': {'color': '#F58CBA',
                         'specs': ['Holy',
                                   'Retribution',
                                   'Protection']},
             'Priest': {'color': '#FFFFFF',
                        'specs': ['Holy',
                                  'Discipline',
                                  'Shadow']},
             'Rogue': {'color': '#FFF569',
                       'specs': ['Combat',
                                 'Assassination',
                                 'Subtetly']},
             'Shaman': {'color': '#0070DE',
                        'specs': ['Restoration',
                                  'Elemental',
                                  'Enhancement']},
             'Warlock': {'color': '#9482C9',
                         'specs': ['Affliction',
                                   'Destruction',
                                   'Demonology']},
             'Warrior': {'color': '#C79C6E',
                         'specs': ['Protection',
                                   'Fury',
                                   'Arms']},
             }

    for wow_class, details in specs.items():
        color = details['color']
        for spec in details['specs']:
            Spec.objects.get_or_create(spec_class=wow_class,
                                       name=spec,
                                       color=color)


if __name__ == '__main__':
    guild_name = 'Defiant'
    guild_realm = 'Azralon'
    guild_bg = UNITED_STATES

    create_specs()

    sc = Scanner()
    sc.populate(guild_bg, guild_realm, guild_name)

