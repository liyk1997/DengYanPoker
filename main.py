#!/usr/bin/env python3
"""
新玩法游戏 - 主入口文件
"""

from src.game import NewGame
from src.player import HumanPlayer, AIPlayer


def main():
    """主函数"""
    print("欢迎来到新玩法游戏！")
    
    # 游戏设置
    while True:
        try:
            player_count = int(input("请输入玩家数量 (2-6): ").strip())
            if 2 <= player_count <= 6:
                break
            else:
                print("玩家数量必须在2-6之间")
        except ValueError:
            print("请输入有效数字")
    
    while True:
        try:
            human_players = int(input(f"请输入人类玩家数量 (1-{player_count}): ").strip())
            if 1 <= human_players <= player_count:
                break
            else:
                print(f"人类玩家数量必须在1-{player_count}之间")
        except ValueError:
            print("请输入有效数字")
    
    # 创建并开始游戏
    game = NewGame(player_count)
    game.setup_game(human_players)
    game.play_game()
    
    # 询问是否再来一局
    while True:
        play_again = input("\n是否再来一局？(y/n): ").strip().lower()
        if play_again in ['y', 'yes', '是']:
            main()
            break
        elif play_again in ['n', 'no', '否']:
            print("感谢游戏！")
            break
        else:
            print("请输入 y 或 n")


if __name__ == "__main__":
    main()