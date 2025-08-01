"""
干瞪眼游戏 - 玩家类
"""

from typing import List, Optional
from abc import ABC, abstractmethod
import random

from .card import Card, CardPattern
from .pattern_analyzer import PatternAnalyzer


class Player(ABC):
    """玩家基类"""
    
    def __init__(self, name: str):
        self.name = name
        self.hand: List[Card] = []
        self.is_finished = False
    
    def add_cards(self, cards: List[Card]):
        """添加牌到手牌"""
        self.hand.extend(cards)
        self.hand.sort()
    
    def remove_cards(self, cards: List[Card]):
        """从手牌中移除牌"""
        for card in cards:
            if card in self.hand:
                self.hand.remove(card)
        
        # 检查是否出完牌
        if not self.hand:
            self.is_finished = True
    
    def get_hand_size(self) -> int:
        """获取手牌数量"""
        return len(self.hand)
    
    def show_hand(self) -> str:
        """显示手牌"""
        return " ".join(str(card) for card in sorted(self.hand))
    
    @abstractmethod
    def play_turn(self, last_pattern: Optional[CardPattern] = None) -> Optional[CardPattern]:
        """玩家出牌回合"""
        pass
    
    def can_play(self, last_pattern: Optional[CardPattern] = None) -> bool:
        """判断是否能出牌"""
        valid_plays = PatternAnalyzer.find_valid_plays(self.hand, last_pattern)
        return len(valid_plays) > 0


class HumanPlayer(Player):
    """人类玩家"""
    
    def play_turn(self, last_pattern: Optional[CardPattern] = None) -> Optional[CardPattern]:
        """人类玩家出牌"""
        print(f"\n{self.name} 的回合")
        print(f"手牌: {self.show_hand()}")
        
        if last_pattern:
            print(f"上家出牌: {last_pattern}")
        
        valid_plays = PatternAnalyzer.find_valid_plays(self.hand, last_pattern)
        
        if not valid_plays:
            print("无法出牌，跳过")
            return None
        
        print("\n可出的牌型:")
        for i, pattern in enumerate(valid_plays, 1):
            print(f"{i}. {pattern}")
        
        print(f"{len(valid_plays) + 1}. 跳过")
        
        while True:
            try:
                choice = input(f"请选择 (1-{len(valid_plays) + 1}): ").strip()
                choice_num = int(choice)
                
                if choice_num == len(valid_plays) + 1:
                    print("选择跳过")
                    return None
                elif 1 <= choice_num <= len(valid_plays):
                    selected_pattern = valid_plays[choice_num - 1]
                    self.remove_cards(selected_pattern.cards)
                    print(f"出牌: {selected_pattern}")
                    return selected_pattern
                else:
                    print("无效选择，请重新输入")
            except ValueError:
                print("请输入数字")


class AIPlayer(Player):
    """AI玩家"""
    
    def __init__(self, name: str, strategy: str = "conservative"):
        super().__init__(name)
        self.strategy = strategy  # conservative, aggressive, smart
    
    def play_turn(self, last_pattern: Optional[CardPattern] = None) -> Optional[CardPattern]:
        """AI玩家出牌"""
        print(f"\n{self.name} 的回合")
        print(f"手牌数量: {self.get_hand_size()}")
        
        if last_pattern:
            print(f"上家出牌: {last_pattern}")
        
        valid_plays = PatternAnalyzer.find_valid_plays(self.hand, last_pattern)
        
        if not valid_plays:
            print(f"{self.name} 无法出牌，跳过")
            return None
        
        # 根据策略选择出牌
        selected_pattern = self._choose_pattern(valid_plays, last_pattern)
        
        if selected_pattern:
            self.remove_cards(selected_pattern.cards)
            print(f"{self.name} 出牌: {selected_pattern}")
            return selected_pattern
        else:
            print(f"{self.name} 选择跳过")
            return None
    
    def _choose_pattern(self, valid_plays: List[CardPattern], last_pattern: Optional[CardPattern]) -> Optional[CardPattern]:
        """根据策略选择出牌"""
        if self.strategy == "conservative":
            return self._conservative_strategy(valid_plays, last_pattern)
        elif self.strategy == "aggressive":
            return self._aggressive_strategy(valid_plays, last_pattern)
        elif self.strategy == "smart":
            return self._smart_strategy(valid_plays, last_pattern)
        else:
            return random.choice(valid_plays) if valid_plays else None
    
    def _conservative_strategy(self, valid_plays: List[CardPattern], last_pattern: Optional[CardPattern]) -> Optional[CardPattern]:
        """保守策略：出最小的牌"""
        if not valid_plays:
            return None
        
        # 优先出单张小牌
        singles = [p for p in valid_plays if p.card_type.name == "SINGLE"]
        if singles:
            return min(singles, key=lambda x: x.main_rank.rank_value)
        
        # 其次出对子
        pairs = [p for p in valid_plays if p.card_type.name == "PAIR"]
        if pairs:
            return min(pairs, key=lambda x: x.main_rank.rank_value)
        
        # 最后出其他牌型
        return min(valid_plays, key=lambda x: x.main_rank.rank_value)
    
    def _aggressive_strategy(self, valid_plays: List[CardPattern], last_pattern: Optional[CardPattern]) -> Optional[CardPattern]:
        """激进策略：优先出大牌和炸弹"""
        if not valid_plays:
            return None
        
        # 优先出炸弹
        bombs = [p for p in valid_plays if p.card_type.name in ["BOMB", "JOKER_BOMB"]]
        if bombs:
            return max(bombs, key=lambda x: x.main_rank.rank_value)
        
        # 其次出大牌
        return max(valid_plays, key=lambda x: x.main_rank.rank_value)
    
    def _smart_strategy(self, valid_plays: List[CardPattern], last_pattern: Optional[CardPattern]) -> Optional[CardPattern]:
        """智能策略：综合考虑手牌情况"""
        if not valid_plays:
            return None
        
        # 如果手牌很少，优先出大牌快速结束
        if self.get_hand_size() <= 3:
            return max(valid_plays, key=lambda x: x.main_rank.rank_value)
        
        # 如果有炸弹且不是被迫出，保留炸弹
        if last_pattern and last_pattern.card_type.name not in ["BOMB", "JOKER_BOMB"]:
            non_bombs = [p for p in valid_plays if p.card_type.name not in ["BOMB", "JOKER_BOMB"]]
            if non_bombs:
                valid_plays = non_bombs
        
        # 优先出单张小牌
        singles = [p for p in valid_plays if p.card_type.name == "SINGLE"]
        if singles:
            return min(singles, key=lambda x: x.main_rank.rank_value)
        
        # 其次出对子
        pairs = [p for p in valid_plays if p.card_type.name == "PAIR"]
        if pairs:
            return min(pairs, key=lambda x: x.main_rank.rank_value)
        
        # 最后出其他牌型
        return min(valid_plays, key=lambda x: x.main_rank.rank_value)