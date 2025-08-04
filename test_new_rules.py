#!/usr/bin/env python3
"""
测试新规则：
1. 2可以管住其他所有单牌
2. 对2可以管住其他所有对子
3. 当一轮没人要时，所有玩家都补牌
"""

from src.card import Card, Suit, Rank
from src.pattern_analyzer import PatternAnalyzer

def test_two_special_power():
    """测试2的特殊压制能力"""
    print("=== 测试2的特殊压制能力 ===")
    
    # 测试单牌2压制其他单牌
    two_single = PatternAnalyzer.analyze_cards([Card(Suit.HEARTS, Rank.TWO)])
    ace_single = PatternAnalyzer.analyze_cards([Card(Suit.SPADES, Rank.ACE)])
    king_single = PatternAnalyzer.analyze_cards([Card(Suit.CLUBS, Rank.KING)])
    three_single = PatternAnalyzer.analyze_cards([Card(Suit.DIAMONDS, Rank.THREE)])
    
    print(f"单牌2能压过单牌A: {two_single.can_beat(ace_single)}")
    print(f"单牌2能压过单牌K: {two_single.can_beat(king_single)}")
    print(f"单牌2能压过单牌3: {two_single.can_beat(three_single)}")
    
    # 测试对2压制其他对子
    two_pair = PatternAnalyzer.analyze_cards([
        Card(Suit.HEARTS, Rank.TWO), 
        Card(Suit.SPADES, Rank.TWO)
    ])
    ace_pair = PatternAnalyzer.analyze_cards([
        Card(Suit.HEARTS, Rank.ACE), 
        Card(Suit.SPADES, Rank.ACE)
    ])
    king_pair = PatternAnalyzer.analyze_cards([
        Card(Suit.HEARTS, Rank.KING), 
        Card(Suit.SPADES, Rank.KING)
    ])
    
    print(f"对2能压过对A: {two_pair.can_beat(ace_pair)}")
    print(f"对2能压过对K: {two_pair.can_beat(king_pair)}")
    
    # 测试其他牌不能跳跃压制
    five_single = PatternAnalyzer.analyze_cards([Card(Suit.HEARTS, Rank.FIVE)])
    print(f"单牌5能压过单牌3: {five_single.can_beat(three_single)}")  # 应该是False
    
    four_single = PatternAnalyzer.analyze_cards([Card(Suit.HEARTS, Rank.FOUR)])
    print(f"单牌4能压过单牌3: {four_single.can_beat(three_single)}")  # 应该是True

def test_normal_sequence():
    """测试正常的连续压制"""
    print("\n=== 测试正常的连续压制 ===")
    
    three = PatternAnalyzer.analyze_cards([Card(Suit.HEARTS, Rank.THREE)])
    four = PatternAnalyzer.analyze_cards([Card(Suit.HEARTS, Rank.FOUR)])
    five = PatternAnalyzer.analyze_cards([Card(Suit.HEARTS, Rank.FIVE)])
    
    print(f"4能压过3: {four.can_beat(three)}")  # True
    print(f"5能压过3: {five.can_beat(three)}")  # False (跳跃)
    print(f"5能压过4: {five.can_beat(four)}")  # True

if __name__ == "__main__":
    test_two_special_power()
    test_normal_sequence()
    print("\n测试完成！")