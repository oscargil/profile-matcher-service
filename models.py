# models.py
from pydantic import BaseModel, Field
from typing import List, Dict, Any

class Device(BaseModel):
    id: int
    model: str
    carrier: str
    firmware: str

class Clan(BaseModel):
    id: str
    name: str

class Player(BaseModel):
    player_id: str
    credential: str
    created: str
    modified: str
    last_session: str
    total_spent: int
    total_refund: int
    total_transactions: int
    last_purchase: str
    active_campaigns: List[str] = Field(default_factory=list)
    devices: List[Device]
    level: int
    xp: int
    total_playtime: int
    country: str
    language: str
    birthdate: str
    gender: str
    inventory: Dict[str, Any]
    clan: Clan
    custom_field: Any = Field(None, alias='_customfield')

class LevelMatcher(BaseModel):
    min: int
    max: int

class HasMatcher(BaseModel):
    country: List[str]
    items: List[str]

class DoesNotHaveMatcher(BaseModel):
    items: List[str]

class Matchers(BaseModel):
    level: LevelMatcher
    has: HasMatcher
    does_not_have: DoesNotHaveMatcher = Field(alias='does_not_have')

class Campaign(BaseModel):
    game: str
    name: str
    priority: float
    matchers: Matchers
    start_date: str
    end_date: str
    enabled: bool
    last_updated: str