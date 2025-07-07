from django.utils import timezone
from .models import Campaign, PlayerProfile
from matcher.matchers import LevelMatcherStrategy, HasMatcherStrategy, DoesNotHaveMatcherStrategy

def match_player_to_campaigns(player: PlayerProfile, campaigns=None):
    """
    Given a player and a queryset of campaigns (or None for all active),
    checks which campaigns the player matches and adds them to active_campaigns.
    Returns the updated player instance.
    """
    if campaigns is None:
        now = timezone.now()
        campaigns = Campaign.objects.filter(
            enabled=True,
            start_date__lte=now,
            end_date__gte=now
        )

    strategies = [
        LevelMatcherStrategy(),
        HasMatcherStrategy(),
        DoesNotHaveMatcherStrategy(),
    ]

    for campaign in campaigns:
        if all(strategy.matches(player, campaign) for strategy in strategies):
            player.active_campaigns.add(campaign)

    player.save()
    return player
