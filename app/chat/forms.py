from django import forms
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from .models import Artist, Room


class HostRoomForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ['nickname', ]
        labels = {
            'nickname': _('nickname'),
        }

        error_messages = {
            'nickname': {
                'max_length': _('nickname must be 30 characters or less')
            }
        }

    def clean_nickname(self):
        cleaned = super().clean()
        nickname = cleaned.get('nickname')
        if nickname != slugify(nickname):
            raise ValidationError('nickname must contain only letters, '
                                  'numbers, dashes, or underscores')
        return nickname


class JoinRoomForm(forms.ModelForm):
    temp_room_code = forms.CharField(max_length=6, min_length=6)

    class Meta:
        model = Artist
        fields = ['nickname', 'temp_room_code', ]
        labels = {
            'nickname': _('nickname'),
        }

        error_messages = {
            'nickname': {
                'max_length': _('nickname must be 30 characters or less')
            }
        }

    def clean_nickname(self):
        cleaned = super().clean()
        nickname = cleaned.get('nickname')
        if nickname != slugify(nickname):
            raise ValidationError('nickname must contain only letters, '
                                  'numbers, dashes, or underscores')
        return nickname
