from django.db import models

# Create your models here.

class Country(models.Model):
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.code

class Item(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Clan(models.Model):
    clan_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Campaign(models.Model):
    game = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    priority = models.FloatField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    enabled = models.BooleanField(default=True)
    last_updated = models.DateTimeField()
    level_min = models.IntegerField(null=True, blank=True)
    level_max = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

class CampaignHasMatcher(models.Model):
    campaign = models.OneToOneField(Campaign, related_name='has_matcher', on_delete=models.CASCADE)
    countries = models.ManyToManyField(Country, blank=True)
    items = models.ManyToManyField(Item, blank=True, related_name='has_matcher_items')

class CampaignDoesNotHaveMatcher(models.Model):
    campaign = models.OneToOneField(Campaign, related_name='does_not_have_matcher', on_delete=models.CASCADE)
    items = models.ManyToManyField(Item, blank=True, related_name='does_not_have_matcher_items')

class PlayerProfile(models.Model):
    player_id = models.CharField(max_length=100, unique=True)
    credential = models.CharField(max_length=100)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    last_session = models.DateTimeField()
    total_spent = models.IntegerField()
    total_refund = models.IntegerField()
    total_transactions = models.IntegerField()
    last_purchase = models.DateTimeField()
    level = models.IntegerField()
    xp = models.IntegerField()
    total_playtime = models.IntegerField()
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    language = models.CharField(max_length=10)
    birthdate = models.DateTimeField()
    gender = models.CharField(max_length=10)
    _customfield = models.CharField(max_length=100, null=True, blank=True)
    active_campaigns = models.ManyToManyField(Campaign, blank=True, related_name='active_players')
    clan = models.ForeignKey(Clan, related_name='members', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.player_id

class Device(models.Model):
    player = models.ForeignKey(PlayerProfile, related_name='devices', on_delete=models.CASCADE)
    model = models.CharField(max_length=100)
    carrier = models.CharField(max_length=100)
    firmware = models.CharField(max_length=100)

class InventoryItem(models.Model):
    player = models.ForeignKey(PlayerProfile, related_name='inventory_items', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()
