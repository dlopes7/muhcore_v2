import os
import sys
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "muhcore.settings")

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

django.setup()

from battlenet import Connection as bnetConnection
from battlenet import Character as bnetCharacter
from battlenet import Guild as bnetGuild
from battlenet import Equipment as bnetEquipment
from battlenet import UNITED_STATES

from core.models import Character, Guild, Spec, Realm, Equipment, IlvlHistory


class Scanner(object):
    def __init__(self):
        print('Connecting to Battlenet')
        self.connection = bnetConnection(public_key='nm3jrgp8avwjpqnptby38z763t9afyes',
                                         private_key='Edt6pnruq8ntrE4YnwnBX4ckBnMddbf8',
                                         locale='en')

    def create_realms(self, region):
        print('Creating Realms..')
        realms = self.connection.get_all_realms(region)
        for realm in realms:
            realm_model, _ = Realm.objects.get_or_create(name=realm.name,
                                                         region=region)

    def populate(self, battlegroup, realm, name):

        guild = self.connection.get_guild(battlegroup, realm, name, fields=[bnetGuild.MEMBERS])
        print('Obtained guild {name} @ {realm} with {members} members'.format(name=guild.name,
                                                                              realm=guild.realm,
                                                                              members=len(guild.members)))

        realm_model, created = Realm.objects.get_or_create(name=realm,
                                                           region=battlegroup)

        guild_model, created = Guild.objects.get_or_create(guild_id='{name}@{realm}'.format(name=guild.name,

                                                                                            realm=realm_model.name,
                                                                                            ),
                                                           name=guild.name,
                                                           realm=realm_model,
                                                           defaults={'number_members': len(guild.members)})

        guild_model.number_members = len(guild.members)
        guild_model.save()

        for member in guild.members:
            char = member['character']

            if char.level == 100:
                print('Looking for {name}...'.format(name=char.name), end='')
                char_all = self.connection.get_character(battlegroup, realm, char.name,
                                                         fields=[bnetCharacter.ITEMS,
                                                                 bnetCharacter.TALENTS,
                                                                 ],
                                                         )  # type: bnetCharacter

                print(char_all.equipment.average_item_level_equipped,
                      char_all.get_class_name(),
                      char_all.get_spec_name(),
                      )

                spec, created = Spec.objects.get_or_create(name=char_all.get_spec_name(),
                                                           spec_class=char_all.get_class_name())

                char_model, created = Character.objects.get_or_create(name=char.name,
                                                                      character_id='{name}@{realm}'.format(
                                                                              name=char.name,
                                                                              realm=realm),
                                                                      )

                create_equipment(char_all.equipment.chest)
                equips = char_all.equipment  # type: bnetEquipment

                char_model.ilvl_equipped = equips.average_item_level_equipped
                char_model.avatar = char_all.get_thumbnail_url()
                char_model.spec = spec
                char_model.guild = guild_model

                char_model.head = create_equipment(equips.head)
                char_model.shoulder = create_equipment(equips.shoulder)
                char_model.neck = create_equipment(equips.neck)
                char_model.back = create_equipment(equips.back)
                char_model.chest = create_equipment(equips.chest)
                char_model.wrist = create_equipment(equips.wrist)
                char_model.hands = create_equipment(equips.hands)
                char_model.waist = create_equipment(equips.waist)
                char_model.legs = create_equipment(equips.legs)
                char_model.feet = create_equipment(equips.feet)
                char_model.finger1 = create_equipment(equips.finger1)
                char_model.finger2 = create_equipment(equips.finger2)
                char_model.trinket1 = create_equipment(equips.trinket1)
                char_model.trinket2 = create_equipment(equips.trinket2)
                char_model.main_hand = create_equipment(equips.main_hand)
                char_model.off_hand = create_equipment(equips.off_hand)

                char_model.save()

                ilvl_history = IlvlHistory(personagem=char_model,
                                           ilvl_equipped=char_model.ilvl_equipped)

                ilvl_history.save()


def create_equipment(equip):
    if equip is None:
        return None

    equip_model, created = Equipment.objects.get_or_create(name=equip.name,
                                                           ilvl=equip.ilvl,
                                                           bonus=equip.bonus,
                                                           equipment_id='{id}_{ilvl}_{bonus}'.format(ilvl=equip.ilvl,
                                                                                                     id=equip.id,
                                                                                                     bonus=equip.bonus),
                                                           )
    return equip_model


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
    # sc.populate(guild_bg, guild_realm, guild_name)
    # sc.create_realms(UNITED_STATES)
