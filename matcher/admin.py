from django.contrib import admin
from .models import PlayerProfile, Campaign, Country, Item, Device, InventoryItem, Clan, CampaignHasMatcher, CampaignDoesNotHaveMatcher

admin.site.register(PlayerProfile)
admin.site.register(Campaign)
admin.site.register(Country)
admin.site.register(Item)
admin.site.register(Device)
admin.site.register(InventoryItem)
admin.site.register(Clan)
admin.site.register(CampaignHasMatcher)
admin.site.register(CampaignDoesNotHaveMatcher)
