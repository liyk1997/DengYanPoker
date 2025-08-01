"""
干瞪眼游戏 - 游戏主逻辑
"""

import random
from typing import List, Optional

from .card import Card, CardPattern, create_deck
from .player import Player, HumanPlayer, AIPlayer
from .pattern_analyzer import PatternAnalyzer


class DengYanGame:
    """干瞪眼游戏主类"""
    
    def __init__(self, player_count: int = 3):
        self.player_count = player_count
        self.players: List[Player] = []
        self.deck: List[Card] = []
        self.current_player_index = 0
        self.last_pattern: Optional[CardPattern] = None
        self.last_player_index: Optional[int] = None
        self.pass_count = 0  # 连续跳过的玩家数
        self.game_over = False
        self.winner: Optional[Player] = None
        self.round_count = 0
    
    def setup_game(self, human_players: int = 1):
        """设置游戏"""
        print("=== 干瞪眼游戏 ===")
        print(f"玩家数量: {self.player_count}")
        print(f"人类玩家: {human_players}, AI玩家: {self.player_count - human_players}")
        
        # 创建玩家
        self.players = []
        for i in range(human_players):
            name = input(f"请输入玩家{i+1}的名字: ").strip() or f"玩家{i+1}"
            self.players.append(HumanPlayer(name))
        
        ai_strategies = ["conservative", "aggressive", "smart"]
        for i in range(self.player_count - human_players):
            strategy = ai_strategies[i % len(ai_strategies)]
            name = f"AI_{strategy}"
            self.players.append(AIPlayer(name, strategy))
        
        # 洗牌发牌
        self._shuffle_and_deal()
        
        # 随机选择首个出牌玩家
        self.current_player_index = random.randint(0, self.player_count - 1)
        print(f"\n{self.players[self.current_player_index].name} 先手出牌")
    
    def _shuffle_and_deal(self):
        """洗牌和发牌"""
        self.deck = create_deck()
        random.shuffle(self.deck)
        
        # 计算每人发牌数量
        cards_per_player = 54 // self.player_count
        remaining_cards = 54 % self.player_count
        
        print(f"\n发牌: 每人{cards_per_player}张牌")
        if remaining_cards > 0:
            print(f"剩余{remaining_cards}张牌作为底牌")
        
        # 发牌
        card_index = 0
        for player in self.players:
            player_cards = self.deck[card_index:card_index + cards_per_player]
            player.add_cards(player_cards)
            card_index += cards_per_player
            print(f"{player.name}: {player.get_hand_size()}张牌")
    
    def play_game(self):
        """开始游戏"""
        print("\n=== 游戏开始 ===")
        
        while not self.game_over:
            self._play_round()
        
        self._show_game_result()
    
    def _play_round(self):
        """进行一轮游戏"""
        self.round_count += 1
        print(f"\n--- 第{self.round_count}轮 ---")
        
        current_player = self.players[self.current_player_index]
        
        # 检查玩家是否已经出完牌
        if current_player.is_finished:
            self._next_player()
            return
        
        # 玩家出牌
        played_pattern = current_player.play_turn(self.last_pattern)
        
        if played_pattern:
            # 成功出牌
            self.last_pattern = played_pattern
            self.last_player_index = self.current_player_index
            self.pass_count = 0
            
            # 检查是否获胜
            if current_player.is_finished:
                self.winner = current_player
                self.game_over = True
                return
        else:
            # 跳过
            self.pass_count += 1
        
        # 检查是否所有其他玩家都跳过了
        if self.pass_count >= self.player_count - 1:
            print(f"\n所有其他玩家都跳过了，{self.players[self.last_player_index].name} 获得新一轮出牌权")
            self.current_player_index = self.last_player_index
            self.last_pattern = None
            self.pass_count = 0
        else:
            self._next_player()
    
    def _next_player(self):
        """切换到下一个玩家"""
        self.current_player_index = (self.current_player_index + 1) % self.player_count
        
        # 跳过已经出完牌的玩家
        while self.players[self.current_player_index].is_finished:
            self.current_player_index = (self.current_player_index + 1) % self.player_count
    
    def _show_game_result(self):
        """显示游戏结果"""
        print("\n=== 游戏结束 ===")
        if self.winner:
            print(f"🎉 恭喜 {self.winner.name} 获胜！")
        
        print("\n最终手牌情况:")
        for player in self.players:
            if player.is_finished:
                print(f"{player.name}: 已出完牌 ✓")
            else:
                print(f"{player.name}: {player.get_hand_size()}张牌 - {player.show_hand()}")
    
    def show_game_status(self):
        """显示当前游戏状态"""
        print(f"\n=== 游戏状态 ===")
        print(f"当前轮次: {self.round_count}")
        print(f"当前玩家: {self.players[self.current_player_index].name}")
        if self.last_pattern:
            print(f"上次出牌: {self.last_pattern} (by {self.players[self.last_player_index].name})")
        else:
            print("上次出牌: 无")
        
        print("\n玩家手牌数量:")
        for i, player in enumerate(self.players):
            status = "✓" if player.is_finished else f"{player.get_hand_size()}张"
            current_mark = " <- 当前" if i == self.current_player_index else ""
            print(f"  {player.name}: {status}{current_mark}")


def main():
    """主函数"""
    print("欢迎来到干瞪眼游戏！")
    
    # 游戏设置
    while True:
        try:
            player_count = int(input("请输入玩家数量 (2-4): ").strip())
            if 2 <= player_count <= 4:
                break
            else:
                print("玩家数量必须在2-4之间")
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
    game = DengYanGame(player_count)
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