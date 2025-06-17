from typing import List
from models import Update

updates: List[Update] = []

def add_update(update: Update):
    updates.append(update)

def get_all_updates() -> List[Update]:
    return updates

def clear_updates():
    updates.clear()
