"""
干瞪眼游戏 - 核心模块
"""

from .card import Card, Suit, Rank, CardPattern, CardType, create_deck
from .pattern_analyzer import PatternAnalyzer
from .player import Player, HumanPlayer, AIPlayer
from .game import DengYanGame

__version__ = "1.0.0"
__author__ = "liyk1997"
__description__ = "干瞪眼扑克游戏Python实现"

__all__ = [
    "Card", "Suit", "Rank", "CardPattern", "CardType", "create_deck",
    "PatternAnalyzer",
    "Player", "HumanPlayer", "AIPlayer", 
    "DengYanGame"
]