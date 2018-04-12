from django.contrib import admin
from komiksy import models


admin.site.register(models.Comic) #możliwość dostepu do komiksów
admin.site.register(models.Elementy)
admin.site.register(models.Favorite)
admin.site.register(models.Subscription)
admin.site.register(models.Votes)
admin.site.register(models.Comments)