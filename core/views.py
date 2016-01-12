from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse, HttpResponseBadRequest

# Create your views here.

from core.models import Guild, Realm, Character


def guild_view(request, region, realm, guild):

    realm_model = Realm.objects.get(name__iexact=realm)
    guild_model = Guild.objects.get(name__iexact=guild,
                                    realm=realm_model
                                    )

    chars_model = Character.objects.filter(guild=guild_model)

    return render(request, 'core/guild.html', {'guild': guild_model,
                                               'chars': chars_model})


def json_chars(request):
    try:
        guild_param = request.GET['guild']
        realm_param = request.GET['realm']
    except Exception as e:
        return HttpResponseBadRequest('Error reading parameters: {error}'.format(error=e))

    realm = Realm.objects.get(name__iexact=realm_param)
    guild_model = Guild.objects.get(name__iexact=guild_param,
                                    realm=realm
                                    )
    chars_model = Character.objects.filter(guild=guild_model)

    response_as_json = serializers.serialize('json', chars_model)

    return HttpResponse(response_as_json,
                        content_type='application/javascript; encoding=utf-8',
                        )
