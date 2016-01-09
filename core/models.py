from django.db import models


class Boss(models.Model):
    nome = models.CharField(max_length=200)
    identificador = models.IntegerField(unique=True)

    def __str__(self):
        return self.nome


class Realm(models.Model):
    name = models.CharField(max_length=200)
    region = models.CharField(max_length=10)
      

class Guild(models.Model):
    name = models.CharField(max_length=200)
    realm = models.ForeignKey(Realm, related_name='guild_realm')
    guild_id = models.CharField(max_length=200)
    number_members = models.IntegerField()
    wowprogress_id = models.CharField(max_length=200,)
    wowprogress_progress = models.CharField(max_length=50)

    def __str__(self):
        return self.name + "@" + self.realm.name


class Equipment(models.Model):
    name = models.CharField(max_length=200)
    ilvl = models.IntegerField(null=True)
    bonus = models.CharField(max_length=200)
    equipment_id = models.CharField(max_length=300, unique=True)
    wowhead_id = models.CharField(max_length=300, null=True)
    dropped_by = models.ForeignKey(Boss, related_name='equipment_dropped_by', null=True)

    def __str__(self):
        return '{name}, ilvl: {ilvl}, slot: {slot}'.format(name=self.name,
                                                           ilvl=self.ilvl,
                                                           slot=self.slot

                                                                 )


class Spec(models.Model):
    spec_class = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7)


class Character(models.Model):
    name = models.CharField(max_length=200)
    character_id = models.CharField(max_length=200)

    ilvl_equipped = models.IntegerField(null=True)
    avatar = models.CharField(max_length=800, null=True)
    spec = models.ForeignKey(Spec, related_name='character_spec', null=True)
    guild = models.ForeignKey(Guild, related_name='character_guild', null=True)
    head = models.ForeignKey(Equipment, related_name='character_head', null=True)
    shoulder = models.ForeignKey(Equipment, related_name='character_shoulder', null=True)
    neck = models.ForeignKey(Equipment, related_name='character_neck', null=True)
    back = models.ForeignKey(Equipment, related_name='character_back', null=True)
    chest = models.ForeignKey(Equipment, related_name='character_chest', null=True)
    wrist = models.ForeignKey(Equipment, related_name='character_wrist', null=True)
    hands = models.ForeignKey(Equipment, related_name='character_hands', null=True)
    waist = models.ForeignKey(Equipment, related_name='character_waist', null=True)
    legs = models.ForeignKey(Equipment, related_name='character_legs', null=True)
    feet = models.ForeignKey(Equipment, related_name='character_feet', null=True)
    finger1 = models.ForeignKey(Equipment, related_name='character_finger1', null=True)
    finger2 = models.ForeignKey(Equipment, related_name='character_finger2', null=True)
    trinket1 = models.ForeignKey(Equipment, related_name='character_trinket1', null=True)
    trinket2 = models.ForeignKey(Equipment, related_name='character_trinket2', null=True)
    main_hand = models.ForeignKey(Equipment, related_name='character_main_hand', null=True)
    off_hand = models.ForeignKey(Equipment, related_name='character_off_hand', null=True)

    def __str__(self):
        return self.character_id


class IlvlHistory(models.Model):
    data = models.DateTimeField(auto_now=True)
    personagem = models.ForeignKey(Character)
    ilvl_equipped = models.IntegerField()


class Bis(models.Model):
    bis_id = models.CharField(max_length=200)
    bis_class = models.CharField(max_length=200, default='1')
    spec = models.CharField(max_length=200, default='1')

    dropped_by = models.ForeignKey(Boss, related_name='bis_dropped_by')
    head = models.ForeignKey(Equipment, related_name='bis_head')
    shoulder = models.ForeignKey(Equipment, related_name='bis_shoulder')
    neck = models.ForeignKey(Equipment, related_name='bis_neck')
    back = models.ForeignKey(Equipment, related_name='bis_back')
    chest = models.ForeignKey(Equipment, related_name='bis_chest')
    wrist = models.ForeignKey(Equipment, related_name='bis_wrist')
    hands = models.ForeignKey(Equipment, related_name='bis_hands')
    waist = models.ForeignKey(Equipment, related_name='bis_waist')
    legs = models.ForeignKey(Equipment, related_name='bis_legs')
    feet = models.ForeignKey(Equipment, related_name='bis_feet')
    finger1 = models.ForeignKey(Equipment, related_name='bis_finger1')
    finger2 = models.ForeignKey(Equipment, related_name='bis_finger2')
    trinket1 = models.ForeignKey(Equipment, related_name='bis_trinket1')
    trinket2 = models.ForeignKey(Equipment, related_name='bis_trinket2')
    main_hand = models.ForeignKey(Equipment, related_name='bis_main_hand')
    off_hand = models.ForeignKey(Equipment, related_name='bis_off_hand')
