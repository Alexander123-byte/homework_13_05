import re
from rest_framework.exceptions import ValidationError


def validate_youtube_url(value):
    youtube_rex = re.compile(r"^(https?://)?(www\.youtube\.com|youtu\.?be)/.+$")

    if not youtube_rex.match(value):
        raise ValidationError("Разрешены только URL-адреса Youtube.")
