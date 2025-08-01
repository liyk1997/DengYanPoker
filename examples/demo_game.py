"""
干瞪眼游戏 - 演示游戏（AI对战）
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.game import DengYanGame
from src.player import AIPlayer


def demo_ai_game():
    """演示AI之间的对战"""
    print("=== 干瞪眼游戏 AI 演示 ===")
    
    # 创建游戏
    game = DengYanGame(3)
    
    # 创建3个AI玩家
    game.players = [
        AIPlayer("保守AI", "conservative"),
        AIPlayer("激进AI", "aggressive"), 
        AIPlayer("智能AI", "smart")
    ]
    
    # 洗牌发牌
    game._shuffle_and_deal()
    
    # 随机选择首个出牌玩家
    import random
    game.current_player_index = random.randint(0, 2)
    print(f"\n{game.players[game.current_player_index].name} 先手出牌")
    
    # 显示初始手牌情况
    print("\n=== 初始手牌情况 ===")
    for player in game.players:
        print(f"{player.name}: {player.get_hand_size()}张牌")
    
    # 开始游戏
    print("\n=== 游戏开始 ===")
    round_count = 0
    max_rounds = 100  # 防止无限循环
    
    while not game.game_over and round_count < max_rounds:
        round_count += 1
        print(f"\n--- 第{round_count}轮 ---")
        
        current_player = game.players[game.current_player_index]
        
        # 检查玩家是否已经出完牌
        if current_player.is_finished:
            game._next_player()
            continue
        
        # 玩家出牌
        played_pattern = current_player.play_turn(game.last_pattern)
        
        if played_pattern:
            # 成功出牌
            game.last_pattern = played_pattern
            game.last_player_index = game.current_player_index
            game.pass_count = 0
            
            # 检查是否获胜
            if current_player.is_finished:
                game.winner = current_player
                game.game_over = True
                break
        else:
            # 跳过
            game.pass_count += 1
        
        # 检查是否所有其他玩家都跳过了
        if game.pass_count >= game.player_count - 1:
            print(f"\n所有其他玩家都跳过了，{game.players[game.last_player_index].name} 获得新一轮出牌权")
            game.current_player_index = game.last_player_index
            game.last_pattern = None
            game.pass_count = 0
        else:
            game._next_player()
        
        # 显示当前状态
        print(f"当前状态: ", end="")
        for i, player in enumerate(game.players):
            status = "✓" if player.is_finished else f"{player.get_hand_size()}张"
            print(f"{player.name}({status})", end=" ")
        print()
    
    # 显示游戏结果
    game._show_game_result()
    
    if round_count >= max_rounds:
        print("游戏达到最大轮数限制")


if __name__ == "__main__":
    demo_ai_game()