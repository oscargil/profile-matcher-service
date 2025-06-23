# services.py
import json
from datetime import datetime
from typing import List, Dict, Any
from models import Player, Campaign

# --- Data Access Simulation ---
def load_mock_db() -> Dict[str, Any]:
    with open("player_profile.json", "r") as f:
        return json.load(f)

def get_current_campaigns() -> List[Dict[str, Any]]:
    with open("campaign_data.json", "r") as f:
        return json.load(f)

mock_player_database = load_mock_db()

# --- Matching Logic ---
def does_profile_match_campaign(player_profile: Player, campaign: Campaign) -> bool:
    """Checks if a player profile matches the conditions of a campaign."""
    now = datetime.utcnow()
    date_format = "%Y-%m-%d %H:%M:%SZ"
    
    start_date = datetime.strptime(campaign.start_date, date_format)
    end_date = datetime.strptime(campaign.end_date, date_format)

    if not campaign.enabled or not (start_date <= now <= end_date):
        return False

    # Matcher conditions
    matchers = campaign.matchers
    
    # Level matcher
    if not (matchers.level.min <= player_profile.level <= matchers.level.max):
        return False

    # 'Has' matcher
    if player_profile.country not in matchers.has.country:
        return False
    if not all(item in player_profile.inventory for item in matchers.has.items):
        return False

    # 'Does not have' matcher
    if any(item in player_profile.inventory for item in matchers.does_not_have.items):
        return False

    return True