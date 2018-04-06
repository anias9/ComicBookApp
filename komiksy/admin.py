from django.contrib import admin
from komiksy import models


admin.site.register(models.Comic) #możliwość dostepu do komiksów
admin.site.register(models.Elementy)