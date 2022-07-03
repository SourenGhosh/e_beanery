
from django.contrib import admin


from django.apps import apps
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered

from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType

from rest_framework.authtoken.models import Token

app_models = apps.get_app_config('base').get_models()
for model in app_models:
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass
admin.site.register(Token)
admin.site.register(Permission)
admin.site.register(ContentType)