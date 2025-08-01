"""
干瞪眼游戏 - 测试文件
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.card import Card, Suit, Rank, CardPattern, CardType, create_deck
from src.pattern_analyzer import PatternAnalyzer
from src.player import HumanPlayer, AIPlayer
from src.game import DengYanGame


def test_card_creation():
    """测试牌的创建和比较"""
    print("=== 测试牌的创建和比较 ===")
    
    # 创建一些牌
    card1 = Card(Suit.SPADES, Rank.THREE)
    card2 = Card(Suit.HEARTS, Rank.ACE)
    card3 = Card(Suit.JOKER, Rank.BIG_JOKER)
    
    print(f"牌1: {card1}")
    print(f"牌2: {card2}")
    print(f"牌3: {card3}")
    
    print(f"牌1 < 牌2: {card1 < card2}")
    print(f"牌2 < 牌3: {card2 < card3}")
    
    # 测试一副牌
    deck = create_deck()
    print(f"一副牌共 {len(deck)} 张")
    print("前10张牌:", [str(card) for card in deck[:10]])


def test_pattern_analysis():
    """测试牌型分析"""
    print("\n=== 测试牌型分析 ===")
    
    # 测试单张
    single_cards = [Card(Suit.SPADES, Rank.ACE)]
    single_pattern = PatternAnalyzer.analyze_cards(single_cards)
    print(f"单张: {single_pattern}")
    
    # 测试对子
    pair_cards = [Card(Suit.SPADES, Rank.SEVEN), Card(Suit.HEARTS, Rank.SEVEN)]
    pair_pattern = PatternAnalyzer.analyze_cards(pair_cards)
    print(f"对子: {pair_pattern}")
    
    # 测试三张
    triple_cards = [Card(Suit.SPADES, Rank.KING), Card(Suit.HEARTS, Rank.KING), Card(Suit.CLUBS, Rank.KING)]
    triple_pattern = PatternAnalyzer.analyze_cards(triple_cards)
    print(f"三张: {triple_pattern}")
    
    # 测试三带一
    triple_with_one_cards = [
        Card(Suit.SPADES, Rank.QUEEN), Card(Suit.HEARTS, Rank.QUEEN), 
        Card(Suit.CLUBS, Rank.QUEEN), Card(Suit.DIAMONDS, Rank.FIVE)
    ]
    triple_with_one_pattern = PatternAnalyzer.analyze_cards(triple_with_one_cards)
    print(f"三带一: {triple_with_one_pattern}")
    
    # 测试炸弹
    bomb_cards = [
        Card(Suit.SPADES, Rank.NINE), Card(Suit.HEARTS, Rank.NINE),
        Card(Suit.CLUBS, Rank.NINE), Card(Suit.DIAMONDS, Rank.NINE)
    ]
    bomb_pattern = PatternAnalyzer.analyze_cards(bomb_cards)
    print(f"炸弹: {bomb_pattern}")
    
    # 测试王炸
    joker_bomb_cards = [Card(Suit.JOKER, Rank.SMALL_JOKER), Card(Suit.JOKER, Rank.BIG_JOKER)]
    joker_bomb_pattern = PatternAnalyzer.analyze_cards(joker_bomb_cards)
    print(f"王炸: {joker_bomb_pattern}")
    
    # 测试顺子
    straight_cards = [
        Card(Suit.SPADES, Rank.THREE), Card(Suit.HEARTS, Rank.FOUR),
        Card(Suit.CLUBS, Rank.FIVE), Card(Suit.DIAMONDS, Rank.SIX),
        Card(Suit.SPADES, Rank.SEVEN)
    ]
    straight_pattern = PatternAnalyzer.analyze_cards(straight_cards)
    print(f"顺子: {straight_pattern}")


def test_pattern_comparison():
    """测试牌型比较"""
    print("\n=== 测试牌型比较 ===")
    
    # 创建一些牌型
    single_3 = CardPattern([Card(Suit.SPADES, Rank.THREE)], CardType.SINGLE)
    single_a = CardPattern([Card(Suit.HEARTS, Rank.ACE)], CardType.SINGLE)
    pair_7 = CardPattern([Card(Suit.SPADES, Rank.SEVEN), Card(Suit.HEARTS, Rank.SEVEN)], CardType.PAIR)
    bomb = CardPattern([
        Card(Suit.SPADES, Rank.NINE), Card(Suit.HEARTS, Rank.NINE),
        Card(Suit.CLUBS, Rank.NINE), Card(Suit.DIAMONDS, Rank.NINE)
    ], CardType.BOMB)
    joker_bomb = CardPattern([Card(Suit.JOKER, Rank.SMALL_JOKER), Card(Suit.JOKER, Rank.BIG_JOKER)], CardType.JOKER_BOMB)
    
    print(f"单张A能压单张3: {single_a.can_beat(single_3)}")
    print(f"单张3能压单张A: {single_3.can_beat(single_a)}")
    print(f"对子7能压单张A: {pair_7.can_beat(single_a)}")
    print(f"炸弹能压对子7: {bomb.can_beat(pair_7)}")
    print(f"王炸能压炸弹: {joker_bomb.can_beat(bomb)}")


def test_ai_player():
    """测试AI玩家"""
    print("\n=== 测试AI玩家 ===")
    
    # 创建AI玩家
    ai_player = AIPlayer("测试AI", "conservative")
    
    # 给AI一些牌
    test_cards = [
        Card(Suit.SPADES, Rank.THREE), Card(Suit.HEARTS, Rank.THREE),
        Card(Suit.CLUBS, Rank.SEVEN), Card(Suit.DIAMONDS, Rank.JACK),
        Card(Suit.SPADES, Rank.ACE)
    ]
    ai_player.add_cards(test_cards)
    
    print(f"AI手牌: {ai_player.show_hand()}")
    
    # 测试AI出牌
    last_pattern = CardPattern([Card(Suit.HEARTS, Rank.FIVE)], CardType.SINGLE)
    ai_play = ai_player.play_turn(last_pattern)
    print(f"AI出牌: {ai_play}")
    print(f"AI剩余手牌: {ai_player.show_hand()}")


def test_find_all_patterns():
    """测试找出所有牌型"""
    print("\n=== 测试找出所有牌型 ===")
    
    # 创建一手牌
    hand = [
        Card(Suit.SPADES, Rank.THREE), Card(Suit.HEARTS, Rank.THREE),
        Card(Suit.CLUBS, Rank.SEVEN), Card(Suit.DIAMONDS, Rank.SEVEN),
        Card(Suit.SPADES, Rank.JACK), Card(Suit.HEARTS, Rank.JACK), Card(Suit.CLUBS, Rank.JACK),
        Card(Suit.DIAMONDS, Rank.ACE)
    ]
    
    print("手牌:", " ".join(str(card) for card in sorted(hand)))
    
    all_patterns = PatternAnalyzer.find_all_patterns(hand)
    print(f"找到 {len(all_patterns)} 种牌型:")
    
    for pattern in all_patterns:
        print(f"  {pattern}")


def run_all_tests():
    """运行所有测试"""
    test_card_creation()
    test_pattern_analysis()
    test_pattern_comparison()
    test_ai_player()
    test_find_all_patterns()
    print("\n=== 所有测试完成 ===")


if __name__ == "__main__":
    run_all_tests()