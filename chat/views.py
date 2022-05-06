import logging

from django.contrib import messages
from django.shortcuts import get_object_or_404, render
from django.utils.crypto import get_random_string

from .forms import HostRoomForm, JoinRoomForm
from .models import Room

logger = logging.getLogger(__name__)


def index(request):
    host_room_form = HostRoomForm()
    join_room_form = JoinRoomForm()
    if request.method == "POST":
        if "host_room" in request.POST:
            host_form = HostRoomForm(request.POST)
            if host_form.is_valid():
                artist = host_form.save(commit=True)
                room_code = get_random_string(length=6).upper()
                room = Room.objects.create(name=room_code)
                room.artists.add(artist)
                folks = Room.objects.get(name=room_code).artists.values_list(
                    "nickname", flat=True
                )
                request.session["nickname"] = artist.nickname
                context = {
                    "room_code": room_code,
                    "folks": folks,
                    "nickname": artist.nickname,
                }
                return render(request, "room.html", context)

        elif "join_room" in request.POST:
            join_form = JoinRoomForm(request.POST)
            if join_form.is_valid():
                artist = join_form.save(commit=False)
                room_code = join_form.cleaned_data.get(
                    "temp_room_code", "temp code bulunamadi"
                ).upper()
                room = get_object_or_404(Room, name=room_code)

                if room.artists.filter(nickname=artist.nickname).exists():
                    messages.info(
                        request,
                        "There is someone else with the "
                        "same nickname on the room. "
                        "Please set another nickname %s." % artist.nickname,
                        fail_silently=True,
                    )
                    context = {
                        "host_room_form": host_room_form,
                        "join_room_form": join_room_form,
                    }
                    return render(request, "index.html", context)
                else:
                    artist.save()
                    room.artists.add(artist)
                    folks = Room.objects.get(
                        name=room_code
                    ).artists.values_list("nickname", flat=True)
                    request.session["nickname"] = artist.nickname
                    context = {
                        "room_code": room_code,
                        "folks": folks,
                        "nickname": artist.nickname,
                    }
                    return render(request, "room.html", context)

    context = {
        "host_room_form": host_room_form,
        "join_room_form": join_room_form,
    }
    return render(request, "index.html", context)
