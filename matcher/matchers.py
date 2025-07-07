class BaseMatcherStrategy:
    def matches(self, player, campaign):
        raise NotImplementedError
    
class LevelMatcherStrategy(BaseMatcherStrategy):
    def matches(self, player, campaign):
        if campaign.level_min is not None and player.level < campaign.level_min:
            return False
        if campaign.level_max is not None and player.level > campaign.level_max:
            return False
        return True

class HasMatcherStrategy(BaseMatcherStrategy):
    def matches(self, player, campaign):
        has_matcher = getattr(campaign, 'has_matcher', None)
        if not has_matcher:
            return True
        # Country
        if has_matcher.countries.exists() and player.country not in has_matcher.countries.all():
            return False
        # Items
        player_items = set(item.item.name for item in player.inventory_items.all())
        matcher_items = set(item.name for item in has_matcher.items.all())
        if matcher_items and not matcher_items.issubset(player_items):
            return False
        return True

class DoesNotHaveMatcherStrategy(BaseMatcherStrategy):
    def matches(self, player, campaign):
        does_not_have_matcher = getattr(campaign, 'does_not_have_matcher', None)
        if not does_not_have_matcher:
            return True
        player_items = set(item.item.name for item in player.inventory_items.all())
        forbidden_items = set(item.name for item in does_not_have_matcher.items.all())
        if forbidden_items and player_items.intersection(forbidden_items):
            return False
        return True