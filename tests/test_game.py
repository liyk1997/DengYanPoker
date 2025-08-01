"""测试文件"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.card import Card, Rank, Suit
from src.pattern_analyzer import PatternAnalyzer
from src.player import HumanPlayer, AIPlayer
from src.game import NewGame


def test_card_creation():
    """测试牌的创建和比较"""
    print("=== 测试牌的创建和比较 ===")
    
    # 创建一些测试牌
    card1 = Card(Suit.HEARTS, Rank.THREE)
    card2 = Card(Suit.SPADES, Rank.ACE)
    card3 = Card(Suit.HEARTS, Rank.SMALL_JOKER)  # 王牌可以用任意花色
    card4 = Card(Suit.SPADES, Rank.BIG_JOKER)    # 王牌可以用任意花色
    
    print(f"红桃3: {card1}")
    print(f"黑桃A: {card2}")
    print(f"小王: {card3}")
    print(f"大王: {card4}")
    
    # 测试比较
    print(f"红桃3 < 黑桃A: {card1 < card2}")
    print(f"小王 < 大王: {card3 < card4}")
    
    # 测试新规则
    print(f"红桃3 能单出: {card1.can_be_single()}")
    print(f"小王 能单出: {card3.can_be_single()}")
    print(f"红桃3 能参与顺子: {card1.can_be_in_straight()}")
    print(f"红桃2 能参与顺子: {Card(Suit.HEARTS, Rank.TWO).can_be_in_straight()}")
    print()


def test_pattern_analysis():
    """测试牌型分析"""
    print("=== 测试牌型分析 ===")
    
    # 测试单牌
    single_cards = [Card(Suit.HEARTS, Rank.FIVE)]
    single_pattern = PatternAnalyzer.analyze_cards(single_cards)
    print(f"单牌: {single_pattern}")
    
    # 测试对子
    pair_cards = [Card(Suit.HEARTS, Rank.SEVEN), Card(Suit.SPADES, Rank.SEVEN)]
    pair_pattern = PatternAnalyzer.analyze_cards(pair_cards)
    print(f"对子: {pair_pattern}")
    
    # 测试三张
    triple_cards = [
        Card(Suit.HEARTS, Rank.NINE), 
        Card(Suit.SPADES, Rank.NINE), 
        Card(Suit.CLUBS, Rank.NINE)
    ]
    triple_pattern = PatternAnalyzer.analyze_cards(triple_cards)
    print(f"三张: {triple_pattern}")
    
    # 测试氢弹（四张）
    bomb_cards = [
        Card(Suit.HEARTS, Rank.KING), 
        Card(Suit.SPADES, Rank.KING), 
        Card(Suit.CLUBS, Rank.KING),
        Card(Suit.DIAMONDS, Rank.KING)
    ]
    bomb_pattern = PatternAnalyzer.analyze_cards(bomb_cards)
    print(f"氢弹: {bomb_pattern}")
    
    # 测试双王炸弹
    joker_bomb_cards = [Card(Suit.HEARTS, Rank.SMALL_JOKER), Card(Suit.SPADES, Rank.BIG_JOKER)]
    joker_bomb_pattern = PatternAnalyzer.analyze_cards(joker_bomb_cards)
    print(f"双王炸弹: {joker_bomb_pattern}")
    
    # 测试连牌（顺子）
    straight_cards = [
        Card(Suit.HEARTS, Rank.THREE),
        Card(Suit.SPADES, Rank.FOUR),
        Card(Suit.CLUBS, Rank.FIVE),
        Card(Suit.DIAMONDS, Rank.SIX),
        Card(Suit.HEARTS, Rank.SEVEN)
    ]
    straight_pattern = PatternAnalyzer.analyze_cards(straight_cards)
    print(f"连牌: {straight_pattern}")
    
    # 测试连队
    straight_pairs_cards = [
        Card(Suit.HEARTS, Rank.FIVE), Card(Suit.SPADES, Rank.FIVE),
        Card(Suit.HEARTS, Rank.SIX), Card(Suit.SPADES, Rank.SIX),
        Card(Suit.HEARTS, Rank.SEVEN), Card(Suit.SPADES, Rank.SEVEN)
    ]
    straight_pairs_pattern = PatternAnalyzer.analyze_cards(straight_pairs_cards)
    print(f"连队: {straight_pairs_pattern}")
    print()


def test_pattern_comparison():
    """测试牌型比较"""
    print("=== 测试牌型比较 ===")
    
    # 创建不同的牌型
    single1 = PatternAnalyzer.analyze_cards([Card(Suit.HEARTS, Rank.FIVE)])
    single2 = PatternAnalyzer.analyze_cards([Card(Suit.SPADES, Rank.EIGHT)])
    
    pair1 = PatternAnalyzer.analyze_cards([
        Card(Suit.HEARTS, Rank.SEVEN), 
        Card(Suit.SPADES, Rank.SEVEN)
    ])
    pair2 = PatternAnalyzer.analyze_cards([
        Card(Suit.HEARTS, Rank.JACK), 
        Card(Suit.SPADES, Rank.JACK)
    ])
    
    bomb = PatternAnalyzer.analyze_cards([
        Card(Suit.HEARTS, Rank.KING), 
        Card(Suit.SPADES, Rank.KING), 
        Card(Suit.CLUBS, Rank.KING),
        Card(Suit.DIAMONDS, Rank.KING)
    ])
    
    joker_bomb = PatternAnalyzer.analyze_cards([
        Card(Suit.HEARTS, Rank.SMALL_JOKER), 
        Card(Suit.SPADES, Rank.BIG_JOKER)
    ])
    
    # 测试比较
    print(f"{single2} 能压过 {single1}: {single2.can_beat(single1)}")
    print(f"{pair2} 能压过 {pair1}: {pair2.can_beat(pair1)}")
    print(f"{bomb} 能压过 {pair2}: {bomb.can_beat(pair2)}")
    print(f"{joker_bomb} 能压过 {bomb}: {joker_bomb.can_beat(bomb)}")
    
    # 测试倍率
    print(f"单牌倍率: {single1.get_multiplier()}")
    print(f"氢弹倍率: {bomb.get_multiplier()}")
    print(f"双王炸弹倍率: {joker_bomb.get_multiplier()}")
    print()


def test_ai_player():
    """测试AI玩家出牌"""
    print("=== 测试AI玩家出牌 ===")
    
    # 创建AI玩家
    ai_player = AIPlayer("测试AI", "smart")
    
    # 给AI玩家一些牌
    test_cards = [
        Card(Suit.HEARTS, Rank.THREE),
        Card(Suit.SPADES, Rank.FIVE),
        Card(Suit.HEARTS, Rank.SEVEN),
        Card(Suit.SPADES, Rank.SEVEN),
        Card(Suit.CLUBS, Rank.NINE),
        Card(Suit.HEARTS, Rank.JACK),
        Card(Suit.SPADES, Rank.KING)
    ]
    
    ai_player.add_cards(test_cards)
    print(f"AI手牌: {ai_player.show_hand()}")
    
    # 测试首轮出牌
    first_play = ai_player.play_turn(None)
    if first_play:
        first_pattern = PatternAnalyzer.analyze_cards(first_play)
        print(f"AI首轮出牌: {first_pattern}")
        # 移除出的牌
        ai_player.remove_cards(first_play)
    
    # 测试跟牌
    last_pattern = PatternAnalyzer.analyze_cards([Card(Suit.HEARTS, Rank.SIX)])
    follow_play = ai_player.play_turn(last_pattern)
    if follow_play:
        follow_pattern = PatternAnalyzer.analyze_cards(follow_play)
        print(f"AI跟牌: {follow_pattern}")
    else:
        print("AI选择跳过")
    print()


def test_game_setup():
    """测试游戏设置"""
    print("=== 测试游戏设置 ===")
    
    # 创建游戏
    game = NewGame(3)
    game.setup_game(1)
    
    print(f"游戏玩家数: {len(game.players)}")
    print(f"庄家: {game.players[game.dealer_index].name}")
    
    for i, player in enumerate(game.players):
        print(f"{player.name}: {len(player.hand)}张牌")
    
    print(f"牌堆剩余: {len(game.deck)}张")
    print()


def main():
    """运行所有测试"""
    print("开始测试新玩法...")
    
    test_card_creation()
    test_pattern_analysis()
    test_pattern_comparison()
    test_ai_player()
    test_game_setup()
    
    print("所有测试完成！")


if __name__ == "__main__":
    main()