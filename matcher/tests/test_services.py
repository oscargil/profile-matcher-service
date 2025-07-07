import pytest
from matcher.models import PlayerProfile, Campaign, Country, Item, Clan, Device, InventoryItem, CampaignHasMatcher, CampaignDoesNotHaveMatcher
from matcher.services import match_player_to_campaigns
from django.utils import timezone

@pytest.fixture
def base_country():
    return Country.objects.create(code="CA")

@pytest.fixture
def forbidden_country():
    return Country.objects.create(code="US")

@pytest.fixture
def item_1():
    return Item.objects.create(name="item_1")

@pytest.fixture
def item_2():
    return Item.objects.create(name="item_2")

@pytest.fixture
def forbidden_item():
    return Item.objects.create(name="item_4")

@pytest.fixture
def base_clan():
    return Clan.objects.create(clan_id="123456", name="Test Clan")

@pytest.fixture
def base_campaign(base_country, item_1):
    campaign = Campaign.objects.create(
        game="mygame",
        name="mycampaign",
        priority=10.5,
        start_date=timezone.now(),
        end_date=timezone.now() + timezone.timedelta(days=10),
        enabled=True,
        last_updated=timezone.now(),
        level_min=1,
        level_max=3,
    )
    has_matcher = CampaignHasMatcher.objects.create(campaign=campaign)
    has_matcher.countries.set([base_country])
    has_matcher.items.set([item_1])
    does_not_have_matcher = CampaignDoesNotHaveMatcher.objects.create(campaign=campaign)
    return campaign

@pytest.fixture
def base_player(base_country, base_clan):
    player = PlayerProfile.objects.create(
        player_id="ok-player",
        credential="test",
        created=timezone.now(),
        modified=timezone.now(),
        last_session=timezone.now(),
        total_spent=0,
        total_refund=0,
        total_transactions=0,
        last_purchase=timezone.now(),
        level=2,
        xp=1000,
        total_playtime=144,
        country=base_country,
        language="en",
        birthdate=timezone.now(),
        gender="male",
        _customfield="test",
        clan=base_clan,
    )
    Device.objects.create(player=player, model="iPhone", carrier="Test", firmware="1.0")
    return player

@pytest.mark.django_db
def test_player_matches_all_rules(base_player, base_campaign, item_1):
    InventoryItem.objects.create(player=base_player, item=item_1, quantity=1)
    match_player_to_campaigns(base_player)
    assert base_campaign in base_player.active_campaigns.all()

@pytest.mark.django_db
def test_player_fails_due_to_level(base_player, base_campaign, item_1):
    base_player.level = 0  # Too low
    base_player.save()
    InventoryItem.objects.create(player=base_player, item=item_1, quantity=1)
    match_player_to_campaigns(base_player)
    assert base_campaign not in base_player.active_campaigns.all()

@pytest.mark.django_db
def test_player_fails_due_to_country(base_player, base_campaign, forbidden_country, item_1):
    base_player.country = forbidden_country
    base_player.save()
    InventoryItem.objects.create(player=base_player, item=item_1, quantity=1)
    match_player_to_campaigns(base_player)
    assert base_campaign not in base_player.active_campaigns.all()

@pytest.mark.django_db
def test_player_fails_due_to_missing_item(base_player, base_campaign, item_2):
    # No item_1 in inventory, only item_2
    InventoryItem.objects.create(player=base_player, item=item_2, quantity=1)
    match_player_to_campaigns(base_player)
    assert base_campaign not in base_player.active_campaigns.all()

@pytest.mark.django_db
def test_player_fails_due_to_forbidden_item(base_player, base_campaign, item_1, forbidden_item):
    InventoryItem.objects.create(player=base_player, item=item_1, quantity=1)
    InventoryItem.objects.create(player=base_player, item=forbidden_item, quantity=1)
    # Add forbidden item to does_not_have_matcher
    matcher = base_campaign.does_not_have_matcher
    matcher.items.set([forbidden_item])
    matcher.save()
    match_player_to_campaigns(base_player)
    assert base_campaign not in base_player.active_campaigns.all() 