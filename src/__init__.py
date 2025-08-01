"""
新玩法游戏 - 核心模块
"""

from .card import Card, Suit, Rank, create_deck
from .pattern_analyzer import PatternAnalyzer, Pattern, PatternType
from .player import Player, HumanPlayer, AIPlayer
from .game import NewGame

__version__ = "2.0.0"
__author__ = "liyk1997"
__description__ = "新玩法扑克游戏Python实现"

__all__ = [
    "Card", "Suit", "Rank", "create_deck",
    "PatternAnalyzer", "Pattern", "PatternType",
    "Player", "HumanPlayer", "AIPlayer", 
    "NewGame"
]