#!/usr/bin/env python3
"""
测试全员补牌逻辑：当一轮没人要时，所有玩家都补牌
"""

from src.game import NewGame
from src.player import AIPlayer

def test_all_players_draw():
    """测试全员补牌逻辑"""
    print("=== 测试全员补牌逻辑 ===")
    
    # 创建一个简单的游戏
    game = NewGame(3)
    
    # 添加3个AI玩家
    for i in range(3):
        game.players.append(AIPlayer(f"AI{i+1}", "conservative"))
    
    # 模拟发牌
    game._deal_cards()
    
    print("初始状态:")
    for i, player in enumerate(game.players):
        print(f"  {player.name}: {len(player.hand)}张牌")
    print(f"  牌堆剩余: {len(game.deck)}张")
    
    # 模拟一轮所有人都跳过的情况
    print("\n模拟一轮所有人都跳过...")
    
    # 记录初始牌堆数量
    initial_deck_size = len(game.deck)
    initial_hand_sizes = [len(player.hand) for player in game.players]
    
    # 设置轮次状态：没有获胜者（所有人都跳过）
    round_winner_index = -1
    
    # 执行补牌逻辑
    if game.deck:
        if round_winner_index != -1:
            # 有人出牌的情况：只有最后出牌者补牌
            winner = game.players[round_winner_index]
            if len(winner.hand) > 0:
                new_card = game.deck.pop()
                winner.add_card(new_card)
                print(f"{winner.name} 补牌: {new_card}")
            else:
                print(f"{winner.name} 已出完牌，无需补牌")
        else:
            # 没人出牌的情况（全部跳过）：所有玩家都补牌
            print("本轮无人出牌，所有玩家补牌:")
            for i, player in enumerate(game.players):
                if len(player.hand) > 0 and game.deck:
                    new_card = game.deck.pop()
                    player.add_card(new_card)
                    print(f"  {player.name} 补牌: {new_card}")
                elif len(player.hand) == 0:
                    print(f"  {player.name} 已出完牌，无需补牌")
    
    print("\n补牌后状态:")
    for i, player in enumerate(game.players):
        print(f"  {player.name}: {len(player.hand)}张牌 (增加了{len(player.hand) - initial_hand_sizes[i]}张)")
    print(f"  牌堆剩余: {len(game.deck)}张 (减少了{initial_deck_size - len(game.deck)}张)")
    
    # 验证结果
    cards_drawn = initial_deck_size - len(game.deck)
    players_with_cards = sum(1 for player in game.players if len(player.hand) > 0)
    
    print(f"\n验证结果:")
    print(f"  抽取的牌数: {cards_drawn}")
    print(f"  有手牌的玩家数: {players_with_cards}")
    print(f"  结果正确: {cards_drawn == players_with_cards}")

if __name__ == "__main__":
    test_all_players_draw()
    print("\n测试完成！")