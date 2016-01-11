from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

from core.models import Guild, Realm


def guild_view(request, region, realm, guild):

    realm_model = Realm.objects.get(name__iexact=realm)
    guild_model = Guild.objects.get(name__iexact=guild,
                                    realm=realm_model
                                    )
    return HttpResponse('{guild}'.format(guild=guild_model))
