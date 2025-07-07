from rest_framework import serializers
from .models import PlayerProfile, Device, InventoryItem, Clan, Campaign, CampaignHasMatcher, CampaignDoesNotHaveMatcher

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['id', 'model', 'carrier', 'firmware']

class InventoryItemSerializer(serializers.ModelSerializer):
    item = serializers.CharField(source='item.name')
    class Meta:
        model = InventoryItem
        fields = ['item', 'quantity']

class ClanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clan
        fields = ['clan_id', 'name']

class CampaignHasMatcherSerializer(serializers.ModelSerializer):
    country = serializers.SlugRelatedField(many=True, slug_field='code', read_only=True, source='countries')
    items = serializers.SlugRelatedField(many=True, slug_field='name', read_only=True)
    class Meta:
        model = CampaignHasMatcher
        fields = ['country', 'items']

class CampaignDoesNotHaveMatcherSerializer(serializers.ModelSerializer):
    items = serializers.SlugRelatedField(many=True, slug_field='name', read_only=True)
    class Meta:
        model = CampaignDoesNotHaveMatcher
        fields = ['items']

class CampaignSerializer(serializers.ModelSerializer):
    matchers = serializers.SerializerMethodField()

    class Meta:
        model = Campaign
        fields = [
            'game', 'name', 'priority', 'matchers',
            'start_date', 'end_date', 'enabled', 'last_updated'
        ]

    def get_matchers(self, obj):
        level = {
            'min': obj.level_min,
            'max': obj.level_max
        }
        has = None
        does_not_have = None
        if hasattr(obj, 'has_matcher'):
            has = CampaignHasMatcherSerializer(obj.has_matcher).data
        if hasattr(obj, 'does_not_have_matcher'):
            does_not_have = CampaignDoesNotHaveMatcherSerializer(obj.does_not_have_matcher).data
        return {
            'level': level,
            'has': has,
            'does_not_have': does_not_have
        }

class PlayerProfileSerializer(serializers.ModelSerializer):
    devices = DeviceSerializer(many=True, read_only=True)
    inventory = serializers.SerializerMethodField()
    clan = ClanSerializer(read_only=True)
    active_campaigns = CampaignSerializer(many=True, read_only=True)
    country = serializers.CharField(source='country.code')

    class Meta:
        model = PlayerProfile
        fields = [
            'player_id', 'credential', 'created', 'modified', 'last_session',
            'total_spent', 'total_refund', 'total_transactions', 'last_purchase',
            'active_campaigns', 'devices', 'level', 'xp', 'total_playtime',
            'country', 'language', 'birthdate', 'gender', 'inventory', 'clan', '_customfield'
        ]

    def get_inventory(self, obj):
        return {item.item.name: item.quantity for item in obj.inventory_items.all()}
    