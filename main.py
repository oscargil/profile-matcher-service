# main.py
import uvicorn
from fastapi import FastAPI, HTTPException
from models import Player, Campaign
from services import (
    mock_player_database,
    get_current_campaigns,
    does_profile_match_campaign,
)
from datetime import datetime

app = FastAPI(
    title="Profile Matcher Service",
    description="A service to match player profiles with active campaigns.",
    version="1.0.0",
)

@app.get("/get_client_config/{player_id}", response_model=Player)
def get_client_config(player_id: str):
    """
    Retrieves a player's profile, matches it against active campaigns,
    and returns the updated profile.
    """
    player_data = mock_player_database.get(player_id)
    if not player_data:
        raise HTTPException(status_code=404, detail="Player not found")

    player = Player(**player_data)
    
    campaigns_data = get_current_campaigns()
    
    for campaign_data in campaigns_data:
        campaign = Campaign(**campaign_data)
        if does_profile_match_campaign(player, campaign):
            if campaign.name not in player.active_campaigns:
                player.active_campaigns.append(campaign.name)
    
    player.modified = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%SZ")
    
    # Update the in-memory "database"
    mock_player_database[player_id] = player.model_dump(by_alias=True)

    return player