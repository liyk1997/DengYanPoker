"""新玩法游戏 - 游戏主逻辑
根据玩法.md重新实现"""

from typing import List, Optional
from .card import create_deck
from .player import Player, HumanPlayer, AIPlayer
from .pattern_analyzer import PatternAnalyzer, Pattern


class NewGame:
    """新玩法游戏类"""
    
    def __init__(self, player_count: int = 3):
        if not 2 <= player_count <= 6:
            raise ValueError("玩家数量必须在2-6之间")
        
        self.player_count = player_count
        self.players: List[Player] = []
        self.deck = create_deck()
        self.current_player_index = 0
        self.dealer_index = 0  # 庄家索引
        self.last_pattern: Optional[Pattern] = None
        self.last_player_index = -1
        self.game_over = False
        self.winner: Optional[Player] = None
        self.round_count = 0
        self.base_score = 1  # 底分
    
    def setup_game(self, human_players: int = 1):
        """设置游戏"""
        if not 1 <= human_players <= self.player_count:
            raise ValueError(f"人类玩家数量必须在1-{self.player_count}之间")
        
        # 创建玩家
        self.players = []
        for i in range(human_players):
            self.players.append(HumanPlayer(f"玩家{i+1}"))
        
        ai_strategies = ["conservative", "aggressive", "smart"]
        for i in range(self.player_count - human_players):
            strategy = ai_strategies[i % len(ai_strategies)]
            self.players.append(AIPlayer(f"AI{i+1}", strategy))
        
        # 洗牌发牌
        import random
        random.shuffle(self.deck)
        self._deal_cards()
        
        # 庄家先出牌
        self.current_player_index = self.dealer_index
        
        print(f"游戏开始！{self.player_count}名玩家参与")
        print(f"庄家: {self.players[self.dealer_index].name}")
        for i, player in enumerate(self.players):
            print(f"{player.name}: {len(player.hand)}张牌")
    
    def _deal_cards(self):
        """发牌 - 庄家6张，其他人5张"""
        # 庄家6张
        for _ in range(6):
            if self.deck:
                self.players[self.dealer_index].add_card(self.deck.pop())
        
        # 其他人5张
        for i in range(self.player_count):
            if i != self.dealer_index:
                for _ in range(5):
                    if self.deck:
                        self.players[i].add_card(self.deck.pop())
    
    def play_game(self):
        """开始游戏"""
        print("\n=== 游戏开始 ===")
        
        while not self.game_over:
            self._play_round()
            self.round_count += 1
        
        self._show_results()
    
    def _play_round(self):
        """进行一轮游戏"""
        print(f"\n--- 第{self.round_count + 1}轮 ---")
        
        # 显示当前状态
        self._show_game_state()
        
        # 玩家轮流出牌
        consecutive_passes = 0
        round_winner_index = -1
        
        while consecutive_passes < self.player_count - 1:
            current_player = self.players[self.current_player_index]
            
            # 检查是否胜利
            if len(current_player.hand) == 0:
                self.game_over = True
                self.winner = current_player
                return
            
            print(f"\n{current_player.name} 的回合")
            
            # 玩家出牌
            played_cards = current_player.play_turn(self.last_pattern)
            
            if played_cards:
                # 有效出牌
                pattern = PatternAnalyzer.analyze_cards(played_cards)
                print(f"{current_player.name} 出牌: {pattern}")
                
                self.last_pattern = pattern
                self.last_player_index = self.current_player_index
                round_winner_index = self.current_player_index
                consecutive_passes = 0
                
                # 移除出的牌
                for card in played_cards:
                    current_player.remove_card(card)
                
            else:
                # 跳过
                print(f"{current_player.name} 跳过")
                consecutive_passes += 1
            
            # 下一个玩家（逆时针）
            self.current_player_index = (self.current_player_index - 1) % self.player_count
        
        # 轮次结束，最后出牌者补牌
        if round_winner_index != -1 and self.deck:
            winner = self.players[round_winner_index]
            new_card = self.deck.pop()
            winner.add_card(new_card)
            print(f"{winner.name} 补牌: {new_card}")
        
        # 重新开始，最后出牌者先出
        self.last_pattern = None
        self.current_player_index = round_winner_index if round_winner_index != -1 else self.dealer_index
        
        # 检查牌堆是否抽完
        if not self.deck:
            print("牌堆已抽完，不再补牌")
    
    def _show_game_state(self):
        """显示游戏状态"""
        print("\n当前状态:")
        for i, player in enumerate(self.players):
            marker = " <- 当前玩家" if i == self.current_player_index else ""
            dealer_marker = " (庄家)" if i == self.dealer_index else ""
            print(f"  {player.name}: {len(player.hand)}张牌{dealer_marker}{marker}")
        
        if self.last_pattern:
            last_player = self.players[self.last_player_index]
            print(f"  上家出牌: {last_player.name} - {self.last_pattern}")
        
        print(f"  牌堆剩余: {len(self.deck)}张")
    
    def _calculate_score(self, player: Player, winner_pattern: Optional[Pattern] = None) -> int:
        """计算积分"""
        remaining_cards = len(player.hand)
        
        # 基础积分
        score = self.base_score * remaining_cards
        
        # 春天倍率（剩余5张）
        if remaining_cards == 5:
            score *= 2
            print(f"  {player.name} 春天！积分翻倍")
        
        # 胜利者牌型倍率
        if winner_pattern:
            multiplier = winner_pattern.get_multiplier()
            if multiplier > 1:
                score *= multiplier
                print(f"  胜利者使用{winner_pattern.pattern_type}，积分 x{multiplier}")
        
        return score
    
    def _show_results(self):
        """显示游戏结果"""
        print("\n=== 游戏结束 ===")
        if self.winner:
            print(f"🎉 {self.winner.name} 获胜！")
        
        # 计算积分
        winner_pattern = self.last_pattern if self.winner else None
        
        print("\n最终结果:")
        # 按剩余牌数排序
        sorted_players = sorted(self.players, key=lambda p: len(p.hand))
        for i, player in enumerate(sorted_players):
            rank = i + 1
            remaining = len(player.hand)
            if remaining == 0:
                print(f"  {rank}. {player.name}: 胜利! 🏆")
            else:
                score = self._calculate_score(player, winner_pattern)
                print(f"  {rank}. {player.name}: 剩余{remaining}张牌，积分{score}")
    



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


if __name__ == "__main__":
    main()