import os
import django
from django.utils import timezone

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from matcher.models import (
    PlayerProfile, Campaign, Country, Item, Device, InventoryItem, Clan,
    CampaignHasMatcher, CampaignDoesNotHaveMatcher
)

# --- Reset all relevant tables ---
Device.objects.all().delete()
InventoryItem.objects.all().delete()
PlayerProfile.objects.all().delete()
Clan.objects.all().delete()
CampaignHasMatcher.objects.all().delete()
CampaignDoesNotHaveMatcher.objects.all().delete()
Campaign.objects.all().delete()
Country.objects.all().delete()
Item.objects.all().delete()

# --- Create countries and items ---
country_ca, _ = Country.objects.get_or_create(code="CA")
country_us, _ = Country.objects.get_or_create(code="US")
country_ro, _ = Country.objects.get_or_create(code="RO")

item_1, _ = Item.objects.get_or_create(name="item_1")
item_4, _ = Item.objects.get_or_create(name="item_4")
item_34, _ = Item.objects.get_or_create(name="item_34")
item_55, _ = Item.objects.get_or_create(name="item_55")
cash, _ = Item.objects.get_or_create(name="cash")
coins, _ = Item.objects.get_or_create(name="coins")

# --- Create campaign ---
campaign, _ = Campaign.objects.get_or_create(
    game="mygame",
    name="mycampaign",
    priority=10.5,
    start_date="2022-01-25 00:00:00Z",
    end_date="2022-02-25 00:00:00Z",
    enabled=True,
    last_updated="2021-07-13 11:46:58Z",
    level_min=1,
    level_max=3,
)

has_matcher, _ = CampaignHasMatcher.objects.get_or_create(campaign=campaign)
has_matcher.countries.set([country_us, country_ro, country_ca])
has_matcher.items.set([item_1])

does_not_have_matcher, _ = CampaignDoesNotHaveMatcher.objects.get_or_create(campaign=campaign)
does_not_have_matcher.items.set([item_4])

# --- Create clan ---
clan, _ = Clan.objects.get_or_create(clan_id="123456", name="Hello world clan")

# --- Create player profile ---
player, _ = PlayerProfile.objects.get_or_create(
    player_id="97983be2-98b7-11e7-90cf-082e5f28d836",
    credential="apple_credential",
    created="2021-01-10 13:37:17Z",
    modified="2021-01-23 13:37:17Z",
    last_session="2021-01-23 13:37:17Z",
    total_spent=400,
    total_refund=0,
    total_transactions=5,
    last_purchase="2021-01-22 13:37:17Z",
    level=3,
    xp=1000,
    total_playtime=144,
    country=country_ca,
    language="fr",
    birthdate="2000-01-10 13:37:17Z",
    gender="male",
    _customfield="mycustom",
    clan=clan,
)

# --- Create device ---
Device.objects.get_or_create(
    player=player,
    model="apple iphone 11",
    carrier="vodafone",
    firmware="123"
)

# --- Create inventory ---
InventoryItem.objects.get_or_create(player=player, item=item_1, quantity=1)
InventoryItem.objects.get_or_create(player=player, item=item_34, quantity=3)
InventoryItem.objects.get_or_create(player=player, item=item_55, quantity=2)
InventoryItem.objects.get_or_create(player=player, item=cash, quantity=123)
InventoryItem.objects.get_or_create(player=player, item=coins, quantity=123)

print("Database reset and initialized with example campaign and player profile.") 