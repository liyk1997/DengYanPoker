"""
新玩法游戏 - 演示游戏（AI对战）
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.game import NewGame
from src.player import AIPlayer
from src.card import Card, Rank, Suit
from src.pattern_analyzer import PatternAnalyzer


def demo_ai_game():
    """演示AI之间的对战"""
    print("=== 新玩法游戏 AI 演示 ===")
    
    # 创建游戏
    game = NewGame(3)
    
    # 设置游戏（1个人类玩家，2个AI）
    game.setup_game(human_players=1)
    
    # 开始游戏
    game.play_game()


def demo_pattern_analysis():
    """演示牌型分析"""
    print("\n=== 牌型分析演示 ===")
    
    # 演示各种牌型
    patterns = [
        # 单牌
        [Card(Suit.HEARTS, Rank.FIVE)],
        # 对子
        [Card(Suit.HEARTS, Rank.SEVEN), Card(Suit.SPADES, Rank.SEVEN)],
        # 三张
        [Card(Suit.HEARTS, Rank.NINE), Card(Suit.SPADES, Rank.NINE), Card(Suit.CLUBS, Rank.NINE)],
        # 氢弹
        [Card(Suit.HEARTS, Rank.KING), Card(Suit.SPADES, Rank.KING), 
         Card(Suit.CLUBS, Rank.KING), Card(Suit.DIAMONDS, Rank.KING)],
        # 双王炸弹
        [Card(Suit.HEARTS, Rank.SMALL_JOKER), Card(Suit.SPADES, Rank.BIG_JOKER)],
        # 连牌
        [Card(Suit.HEARTS, Rank.THREE), Card(Suit.SPADES, Rank.FOUR),
         Card(Suit.CLUBS, Rank.FIVE), Card(Suit.DIAMONDS, Rank.SIX),
         Card(Suit.HEARTS, Rank.SEVEN)],
        # 连队
        [Card(Suit.HEARTS, Rank.FIVE), Card(Suit.SPADES, Rank.FIVE),
         Card(Suit.HEARTS, Rank.SIX), Card(Suit.SPADES, Rank.SIX),
         Card(Suit.HEARTS, Rank.SEVEN), Card(Suit.SPADES, Rank.SEVEN)]
    ]
    
    for cards in patterns:
        pattern = PatternAnalyzer.analyze_cards(cards)
        if pattern:
            print(f"{pattern} - 倍率: {pattern.get_multiplier()}")
        else:
            print(f"无效牌型: {[str(card) for card in cards]}")


def demo_new_rules():
    """演示新规则"""
    print("\n=== 新规则演示 ===")
    
    # 王不能单出
    small_joker = Card(Suit.HEARTS, Rank.SMALL_JOKER)
    big_joker = Card(Suit.SPADES, Rank.BIG_JOKER)
    three = Card(Suit.HEARTS, Rank.THREE)
    
    print(f"小王能单出: {small_joker.can_be_single()}")
    print(f"大王能单出: {big_joker.can_be_single()}")
    print(f"红桃3能单出: {three.can_be_single()}")
    
    # 2不能参与顺子
    two = Card(Suit.HEARTS, Rank.TWO)
    ace = Card(Suit.SPADES, Rank.ACE)
    
    print(f"红桃2能参与顺子: {two.can_be_in_straight()}")
    print(f"黑桃A能参与顺子: {ace.can_be_in_straight()}")


if __name__ == "__main__":
    demo_pattern_analysis()
    demo_new_rules()
    demo_ai_game()