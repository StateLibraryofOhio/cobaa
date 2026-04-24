from pathlib import Path

from django import template
from django.conf import settings
from django.contrib.staticfiles import finders

register = template.Library()


@register.filter
def to_absolute(asset_path):
    normalized_path = str(asset_path).lstrip("/")
    located = finders.find(normalized_path)
    if isinstance(located, (list, tuple)):
        located = located[0] if located else None
    if located:
        return Path(located).resolve().as_uri()
    return Path(settings.STATIC_ROOT / normalized_path).resolve().as_uri()
