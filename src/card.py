"""新玩法游戏 - 牌类定义
根据玩法.md重新实现
"""

from enum import Enum
import random
from typing import List, Optional


class Suit(Enum):
    """花色枚举"""
    SPADES = "♠"      # 黑桃
    HEARTS = "♥"      # 红心
    CLUBS = "♣"       # 梅花
    DIAMONDS = "♦"    # 方块


class Rank(Enum):
    """牌面大小枚举 - 按照新玩法规则"""
    THREE = (3, "3")
    FOUR = (4, "4")
    FIVE = (5, "5")
    SIX = (6, "6")
    SEVEN = (7, "7")
    EIGHT = (8, "8")
    NINE = (9, "9")
    TEN = (10, "10")
    JACK = (11, "J")
    QUEEN = (12, "Q")
    KING = (13, "K")
    ACE = (14, "A")
    TWO = (15, "2")        # 2是最大的单牌，但不能参与顺子
    SMALL_JOKER = (16, "小王")  # 王不能单出
    BIG_JOKER = (17, "大王")    # 王不能单出
    
    def __init__(self, rank_value, display_name):
        self.rank_value = rank_value
        self.display_name = display_name
    
    def __lt__(self, other):
        if isinstance(other, Rank):
            return self.rank_value < other.rank_value
        return NotImplemented
    
    def __le__(self, other):
        if isinstance(other, Rank):
            return self.rank_value <= other.rank_value
        return NotImplemented
    
    def __gt__(self, other):
        if isinstance(other, Rank):
            return self.rank_value > other.rank_value
        return NotImplemented
    
    def __ge__(self, other):
        if isinstance(other, Rank):
            return self.rank_value >= other.rank_value
        return NotImplemented
    
    def can_be_single(self):
        """判断是否可以单出"""
        return self not in [Rank.SMALL_JOKER, Rank.BIG_JOKER]
    
    def can_be_in_straight(self):
        """判断是否可以参与顺子"""
        return self not in [Rank.TWO, Rank.SMALL_JOKER, Rank.BIG_JOKER]


class Card:
    """扑克牌类"""
    
    def __init__(self, suit: Suit, rank: Rank):
        self.suit = suit
        self.rank = rank
    
    def __str__(self):
        if self.rank in [Rank.SMALL_JOKER, Rank.BIG_JOKER]:
            return self.rank.display_name
        return f"{self.suit.value}{self.rank.display_name}"
    
    def __repr__(self):
        return self.__str__()
    
    def __lt__(self, other):
        if not isinstance(other, Card):
            return NotImplemented
        return self.rank < other.rank
    
    def __le__(self, other):
        if not isinstance(other, Card):
            return NotImplemented
        return self.rank <= other.rank
    
    def __gt__(self, other):
        if not isinstance(other, Card):
            return NotImplemented
        return self.rank > other.rank
    
    def __ge__(self, other):
        if not isinstance(other, Card):
            return NotImplemented
        return self.rank >= other.rank
    
    def __eq__(self, other):
        if not isinstance(other, Card):
            return NotImplemented
        return self.rank == other.rank and self.suit == other.suit
    
    def __hash__(self):
        return hash((self.suit, self.rank))
    
    def can_be_single(self):
        """判断是否可以单出"""
        return self.rank.can_be_single()
    
    def can_be_in_straight(self):
        """判断是否可以参与顺子"""
        return self.rank.can_be_in_straight()
    
    @property
    def is_joker(self):
        """是否为王"""
        return self.rank in [Rank.SMALL_JOKER, Rank.BIG_JOKER]
    
    @property
    def is_two(self):
        """是否为2"""
        return self.rank == Rank.TWO


class CardType(Enum):
    """牌型枚举"""
    SINGLE = "单张"
    PAIR = "对子"
    STRAIGHT = "顺子"
    TRIPLE = "三张"
    TRIPLE_WITH_ONE = "三带一"
    BOMB = "炸弹"
    JOKER_BOMB = "王炸"


class CardPattern:
    """牌型类"""
    
    def __init__(self, cards: List[Card], card_type: CardType, main_rank: Optional[Rank] = None):
        self.cards = sorted(cards)  # 按牌点排序
        self.card_type = card_type
        self.main_rank = main_rank or self._get_main_rank()
    
    def _get_main_rank(self) -> Rank:
        """获取牌型的主要牌点（用于比较大小）"""
        if self.card_type == CardType.SINGLE:
            return self.cards[0].rank
        elif self.card_type == CardType.PAIR:
            return self.cards[0].rank
        elif self.card_type == CardType.STRAIGHT:
            return max(card.rank for card in self.cards)
        elif self.card_type == CardType.TRIPLE:
            return self.cards[0].rank
        elif self.card_type == CardType.TRIPLE_WITH_ONE:
            # 找出出现3次的牌
            rank_count = {}
            for card in self.cards:
                rank_count[card.rank] = rank_count.get(card.rank, 0) + 1
            for rank, count in rank_count.items():
                if count == 3:
                    return rank
        elif self.card_type == CardType.BOMB:
            return self.cards[0].rank
        elif self.card_type == CardType.JOKER_BOMB:
            return Rank.BIG_JOKER
        
        return self.cards[0].rank
    
    def __str__(self):
        return f"{self.card_type.value}: {' '.join(str(card) for card in self.cards)}"
    
    def __repr__(self):
        return str(self)
    
    def can_beat(self, other: 'CardPattern') -> bool:
        """判断是否能压过另一个牌型"""
        if not other:
            return True
        
        # 王炸最大
        if self.card_type == CardType.JOKER_BOMB:
            return True
        
        if other.card_type == CardType.JOKER_BOMB:
            return False
        
        # 炸弹可以压任何非炸弹
        if self.card_type == CardType.BOMB and other.card_type != CardType.BOMB:
            return True
        
        if other.card_type == CardType.BOMB and self.card_type != CardType.BOMB:
            return False
        
        # 同类型比较
        if self.card_type == other.card_type:
            return self.main_rank > other.main_rank
        
        return False


def create_deck() -> List[Card]:
    """创建一副54张牌"""
    deck = []
    
    # 添加普通牌（52张）
    normal_ranks = [r for r in Rank if r not in [Rank.SMALL_JOKER, Rank.BIG_JOKER]]
    normal_suits = list(Suit)
    
    for suit in normal_suits:
        for rank in normal_ranks:
            deck.append(Card(suit, rank))
    
    # 添加大小王（使用红桃和黑桃作为花色）
    deck.append(Card(Suit.HEARTS, Rank.SMALL_JOKER))
    deck.append(Card(Suit.SPADES, Rank.BIG_JOKER))
    
    return deck