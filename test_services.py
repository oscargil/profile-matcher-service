import pytest
from datetime import datetime, timedelta
from models import Player, Campaign, Matchers, LevelMatcher, HasMatcher, DoesNotHaveMatcher, Clan, Device
from services import does_profile_match_campaign

@pytest.fixture
def base_player():
    return Player(
        player_id="test-player",
        credential="test-cred",
        created="2021-01-10 13:37:17Z",
        modified="2021-01-23 13:37:17Z",
        last_session="2021-01-23 13:37:17Z",
        total_spent=100,
        total_refund=0,
        total_transactions=1,
        last_purchase="2021-01-22 13:37:17Z",
        active_campaigns=[],
        devices=[Device(id=1, model="test", carrier="test", firmware="1.0")],
        level=3,
        xp=1000,
        total_playtime=100,
        country="CA",
        language="en",
        birthdate="2000-01-10 13:37:17Z",
        gender="male",
        inventory={"item_1": 1, "item_2": 2},
        clan=Clan(id="1", name="Test Clan"),
        _customfield="custom"
    )

@pytest.fixture
def base_campaign():
    now = datetime.utcnow()
    return Campaign(
        game="testgame",
        name="testcampaign",
        priority=1.0,
        matchers=Matchers(
            level=LevelMatcher(min=1, max=3),
            has=HasMatcher(country=["CA"], items=["item_1"]),
            does_not_have=DoesNotHaveMatcher(items=["item_4"])
        ),
        start_date=(now - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%SZ"),
        end_date=(now + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%SZ"),
        enabled=True,
        last_updated=now.strftime("%Y-%m-%d %H:%M:%SZ")
    )

def test_player_matches_campaign(base_player, base_campaign):
    assert does_profile_match_campaign(base_player, base_campaign) is True

def test_player_does_not_match_due_to_level(base_player, base_campaign):
    base_player.level = 5
    assert does_profile_match_campaign(base_player, base_campaign) is False

def test_player_does_not_match_due_to_missing_item(base_player, base_campaign):
    base_player.inventory.pop("item_1")
    assert does_profile_match_campaign(base_player, base_campaign) is False

def test_player_does_not_match_due_to_forbidden_item(base_player, base_campaign):
    base_player.inventory["item_4"] = 1
    assert does_profile_match_campaign(base_player, base_campaign) is False

def test_campaign_not_enabled(base_player, base_campaign):
    base_campaign.enabled = False
    assert does_profile_match_campaign(base_player, base_campaign) is False

def test_campaign_out_of_date_range(base_player, base_campaign):
    base_campaign.start_date = (datetime.utcnow() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%SZ")
    base_campaign.end_date = (datetime.utcnow() + timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%SZ")
    assert does_profile_match_campaign(base_player, base_campaign) is False
