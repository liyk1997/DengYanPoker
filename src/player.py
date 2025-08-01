"""玩家类 - 人类玩家和AI玩家"""

import random
from typing import List, Optional
from .card import Card
from .pattern_analyzer import PatternAnalyzer, Pattern


class Player:
    """玩家基类"""
    
    def __init__(self, name: str):
        self.name = name
        self.hand: List[Card] = []
    
    def add_card(self, card: Card):
        """添加一张牌到手牌"""
        self.hand.append(card)
        self.hand.sort()
    
    def add_cards(self, cards: List[Card]):
        """添加多张牌到手牌"""
        self.hand.extend(cards)
        self.hand.sort()
    
    def remove_card(self, card: Card):
        """从手牌中移除一张牌"""
        if card in self.hand:
            self.hand.remove(card)
    
    def remove_cards(self, cards: List[Card]):
        """从手牌中移除多张牌"""
        for card in cards:
            self.remove_card(card)
    
    def get_hand_size(self) -> int:
        """获取手牌数量"""
        return len(self.hand)
    
    def show_hand(self) -> str:
        """显示手牌"""
        return " ".join(str(card) for card in self.hand)
    
    def is_finished(self) -> bool:
        """检查是否出完牌"""
        return len(self.hand) == 0
    
    def play_turn(self, last_pattern: Optional[Pattern]) -> Optional[List[Card]]:
        """玩家出牌回合 - 子类需要实现"""
        raise NotImplementedError


class HumanPlayer(Player):
    """人类玩家"""
    
    def play_turn(self, last_pattern: Optional[Pattern]) -> Optional[List[Card]]:
        """人类玩家出牌"""
        print(f"\n{self.name} 的回合")
        print(f"你的手牌: {self.show_hand()}")
        
        if last_pattern:
            print(f"需要压过: {last_pattern}")
        else:
            print("你可以出任意牌型")
        
        while True:
            user_input = input("请选择要出的牌 (输入牌的索引，用空格分隔，或输入'pass'跳过): ").strip()
            
            if user_input.lower() == 'pass':
                if last_pattern is None:
                    print("首轮不能跳过，必须出牌")
                    continue
                return None
            
            try:
                # 解析用户输入的索引
                indices = [int(x) - 1 for x in user_input.split()]
                
                # 验证索引有效性
                if not all(0 <= i < len(self.hand) for i in indices):
                    print("索引超出范围，请重新输入")
                    continue
                
                # 获取选择的牌
                selected_cards = [self.hand[i] for i in indices]
                
                # 检查王是否能单出
                if len(selected_cards) == 1 and not selected_cards[0].can_be_single():
                    print("王不能单出，请重新选择")
                    continue
                
                # 分析牌型
                pattern = PatternAnalyzer.analyze_cards(selected_cards)
                if not pattern:
                    print("无效的牌型，请重新选择")
                    continue
                
                # 检查是否能压过上家
                if last_pattern and not pattern.can_beat(last_pattern):
                    print(f"无法压过上家的 {last_pattern}，请重新选择")
                    continue
                
                return selected_cards
                
            except ValueError:
                print("输入格式错误，请输入数字索引")
            except Exception as e:
                print(f"出现错误: {e}")


class AIPlayer(Player):
    """AI玩家"""
    
    def __init__(self, name: str, strategy: str = "smart"):
        super().__init__(name)
        self.strategy = strategy
    
    def play_turn(self, last_pattern: Optional[Pattern]) -> Optional[List[Card]]:
        """AI玩家出牌"""
        print(f"\n{self.name} 思考中...")
        
        if last_pattern is None:
            # 首轮出牌，选择最小的牌
            return self._play_first_turn()
        else:
            # 尝试压过上家
            return self._try_beat_pattern(last_pattern)
    
    def _play_first_turn(self) -> List[Card]:
        """首轮出牌策略"""
        if self.strategy == "aggressive":
            # 激进策略：出大牌
            return self._find_best_pattern()
        else:
            # 保守策略：出最小的能出的牌
            # 找到最小的能单出的牌
            valid_singles = [card for card in self.hand if card.can_be_single()]
            if valid_singles:
                return [min(valid_singles)]
            else:
                # 如果没有能单出的牌，出最小的对子
                return self._find_smallest_pair() or [self.hand[0]]
    
    def _find_smallest_pair(self) -> Optional[List[Card]]:
        """找到最小的对子"""
        for i in range(len(self.hand)):
            for j in range(i + 1, len(self.hand)):
                if self.hand[i].rank == self.hand[j].rank:
                    return [self.hand[i], self.hand[j]]
        return None
    
    def _try_beat_pattern(self, last_pattern: Pattern) -> Optional[List[Card]]:
        """尝试压过指定牌型"""
        possible_plays = self._find_beating_patterns(last_pattern)
        
        if not possible_plays:
            return None  # 跳过
        
        if self.strategy == "conservative":
            # 保守策略：选择最小的能压过的牌
            return min(possible_plays, key=lambda cards: sum(card.rank.rank_value for card in cards))
        elif self.strategy == "aggressive":
            # 激进策略：选择最大的牌
            return max(possible_plays, key=lambda cards: sum(card.rank.rank_value for card in cards))
        else:
            # 智能策略：综合考虑
            return self._smart_choice(possible_plays, last_pattern)
    
    def _find_beating_patterns(self, last_pattern: Pattern) -> List[List[Card]]:
        """找出所有能压过指定牌型的组合"""
        possible_plays = []
        
        # 生成所有可能的牌型组合
        all_patterns = self._generate_all_patterns()
        
        for cards in all_patterns:
            pattern = PatternAnalyzer.analyze_cards(cards)
            if pattern and pattern.can_beat(last_pattern):
                possible_plays.append(cards)
        
        return possible_plays
    
    def _generate_all_patterns(self) -> List[List[Card]]:
        """生成所有可能的牌型组合"""
        patterns = []
        
        # 单牌（只有能单出的牌）
        for card in self.hand:
            if card.can_be_single():
                patterns.append([card])
        
        # 对子
        for i in range(len(self.hand)):
            for j in range(i + 1, len(self.hand)):
                if self.hand[i].rank == self.hand[j].rank:
                    patterns.append([self.hand[i], self.hand[j]])
        
        # 三张
        for i in range(len(self.hand)):
            for j in range(i + 1, len(self.hand)):
                for k in range(j + 1, len(self.hand)):
                    if (self.hand[i].rank == self.hand[j].rank == self.hand[k].rank):
                        patterns.append([self.hand[i], self.hand[j], self.hand[k]])
        
        # 氢弹（四张）
        for i in range(len(self.hand)):
            for j in range(i + 1, len(self.hand)):
                for k in range(j + 1, len(self.hand)):
                    for l in range(k + 1, len(self.hand)):
                        if (self.hand[i].rank == self.hand[j].rank == 
                            self.hand[k].rank == self.hand[l].rank):
                            patterns.append([self.hand[i], self.hand[j], 
                                           self.hand[k], self.hand[l]])
        
        # 连牌（顺子）
        patterns.extend(self._find_straights())
        
        # 连队（连续对子）
        patterns.extend(self._find_straight_pairs())
        
        # 双王炸弹
        jokers = [card for card in self.hand if card.rank.name in ['SMALL_JOKER', 'BIG_JOKER']]
        if len(jokers) == 2:
            patterns.append(jokers)
        
        return patterns
    
    def _find_straights(self) -> List[List[Card]]:
        """找出所有可能的连牌"""
        straights = []
        valid_cards = [card for card in self.hand if card.can_be_in_straight()]
        
        # 按点数分组
        rank_groups = {}
        for card in valid_cards:
            rank = card.rank
            if rank not in rank_groups:
                rank_groups[rank] = []
            rank_groups[rank].append(card)
        
        # 找连续的点数
        sorted_ranks = sorted(rank_groups.keys(), key=lambda r: r.rank_value)
        
        for start_idx in range(len(sorted_ranks)):
            for length in range(5, len(sorted_ranks) - start_idx + 1):  # 至少5张
                consecutive_ranks = sorted_ranks[start_idx:start_idx + length]
                
                # 检查是否连续
                if all(consecutive_ranks[i].rank_value == consecutive_ranks[i-1].rank_value + 1 
                       for i in range(1, len(consecutive_ranks))):
                    # 每个点数选一张牌
                    straight_cards = [rank_groups[rank][0] for rank in consecutive_ranks]
                    straights.append(straight_cards)
        
        return straights
    
    def _find_straight_pairs(self) -> List[List[Card]]:
        """找出所有可能的连队"""
        straight_pairs = []
        valid_cards = [card for card in self.hand if card.can_be_in_straight()]
        
        # 按点数分组
        rank_groups = {}
        for card in valid_cards:
            rank = card.rank
            if rank not in rank_groups:
                rank_groups[rank] = []
            rank_groups[rank].append(card)
        
        # 只保留有对子的点数
        pair_ranks = {rank: cards for rank, cards in rank_groups.items() if len(cards) >= 2}
        
        # 找连续的对子
        sorted_ranks = sorted(pair_ranks.keys(), key=lambda r: r.rank_value)
        
        for start_idx in range(len(sorted_ranks)):
            for length in range(3, len(sorted_ranks) - start_idx + 1):  # 至少3对
                consecutive_ranks = sorted_ranks[start_idx:start_idx + length]
                
                # 检查是否连续
                if all(consecutive_ranks[i].rank_value == consecutive_ranks[i-1].rank_value + 1 
                       for i in range(1, len(consecutive_ranks))):
                    # 每个点数选两张牌
                    pair_cards = []
                    for rank in consecutive_ranks:
                        pair_cards.extend(pair_ranks[rank][:2])
                    straight_pairs.append(pair_cards)
        
        return straight_pairs
    
    def _find_best_pattern(self) -> List[Card]:
        """找出最佳牌型"""
        all_patterns = self._generate_all_patterns()
        
        if not all_patterns:
            # 如果没有有效牌型，出最小的能出的牌
            valid_singles = [card for card in self.hand if card.can_be_single()]
            if valid_singles:
                return [min(valid_singles)]
            else:
                return self._find_smallest_pair() or [self.hand[0]]
        
        # 优先选择氢弹，然后是双王炸弹，三张，连牌，连队，对子，最后是单牌
        for pattern_cards in sorted(all_patterns, key=lambda x: (-len(x), -sum(card.rank.rank_value for card in x))):
            pattern = PatternAnalyzer.analyze_cards(pattern_cards)
            if pattern:
                return pattern_cards
        
        return [self.hand[0]]  # 兜底
    
    def _smart_choice(self, possible_plays: List[List[Card]], last_pattern: Pattern) -> List[Card]:
        """智能选择策略"""
        if not possible_plays:
            return None
        
        # 如果手牌很少，优先出大牌
        if len(self.hand) <= 3:
            return max(possible_plays, key=lambda cards: sum(card.rank.rank_value for card in cards))
        
        # 否则选择中等大小的牌
        possible_plays.sort(key=lambda cards: sum(card.rank.rank_value for card in cards))
        return possible_plays[len(possible_plays) // 2]