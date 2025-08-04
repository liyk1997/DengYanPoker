"""
新玩法游戏 - 牌型分析器
根据玩法.md重新实现
"""

from typing import List, Dict, Optional, Tuple
from collections import Counter
from .card import Card, Rank


class PatternType:
    """牌型类型常量"""
    SINGLE = "单牌"           # 单张
    PAIR = "对子"             # 对子
    STRAIGHT = "连牌"         # 连续≥3张
    STRAIGHT_PAIRS = "连队"   # 连续≥2对
    BOMB = "炸弹"             # 三张相同
    HYDROGEN_BOMB = "氢弹"    # 四张相同
    DOUBLE_JOKER = "双王炸弹" # 大小王对
    INVALID = "无效"


class Pattern:
    """牌型类"""
    
    def __init__(self, cards: List[Card], pattern_type: str, main_rank: Optional[Rank] = None):
        self.cards = sorted(cards)  # 按大小排序
        self.pattern_type = pattern_type
        self.main_rank = main_rank  # 主要牌面（用于比较大小）
        self.size = len(cards)
    
    def __str__(self):
        cards_str = " ".join(str(card) for card in self.cards)
        return f"{self.pattern_type}: {cards_str}"
    
    def __repr__(self):
        return self.__str__()
    
    def can_beat(self, other: 'Pattern') -> bool:
        """判断是否能压过另一个牌型"""
        if not other:
            return True
        
        # 双王炸弹最大
        if self.pattern_type == PatternType.DOUBLE_JOKER:
            return True
        
        if other.pattern_type == PatternType.DOUBLE_JOKER:
            return False
        
        # 氢弹可以炸一切非炸弹和小炸弹
        if self.pattern_type == PatternType.HYDROGEN_BOMB:
            return other.pattern_type not in [PatternType.HYDROGEN_BOMB, PatternType.DOUBLE_JOKER]
        
        if other.pattern_type == PatternType.HYDROGEN_BOMB:
            return False
        
        # 炸弹可以压所有非炸弹
        if self.pattern_type == PatternType.BOMB:
            return other.pattern_type not in [PatternType.BOMB, PatternType.HYDROGEN_BOMB, PatternType.DOUBLE_JOKER]
        
        if other.pattern_type == PatternType.BOMB:
            return False
        
        # 相同牌型比较大小（只能"顺大"压制，必须连续）
        if self.pattern_type == other.pattern_type and self.size == other.size:
            if self.main_rank and other.main_rank:
                # 必须是连续的下一个牌面才能压过
                return self.main_rank.rank_value == other.main_rank.rank_value + 1
        
        return False
    
    def get_multiplier(self) -> int:
        """获取倍率"""
        if self.pattern_type == PatternType.DOUBLE_JOKER:
            return 4
        elif self.pattern_type == PatternType.HYDROGEN_BOMB:
            return 4
        elif self.pattern_type == PatternType.BOMB:
            return 2
        return 1


class PatternAnalyzer:
    """牌型分析器"""
    
    @staticmethod
    def analyze_cards(cards: List[Card]) -> Pattern:
        """分析给定牌组的牌型"""
        if not cards:
            return Pattern([], PatternType.INVALID)
        
        # 按牌面大小分组
        rank_counts = Counter(card.rank for card in cards)
        ranks = list(rank_counts.keys())
        counts = list(rank_counts.values())
        
        # 双王炸弹：大小王对
        if len(cards) == 2 and set(ranks) == {Rank.SMALL_JOKER, Rank.BIG_JOKER}:
            return Pattern(cards, PatternType.DOUBLE_JOKER, Rank.BIG_JOKER)
        
        # 氢弹：四张相同
        if len(cards) == 4 and len(set(ranks)) == 1:
            return Pattern(cards, PatternType.HYDROGEN_BOMB, ranks[0])
        
        # 炸弹：三张相同
        if len(cards) == 3 and len(set(ranks)) == 1:
            return Pattern(cards, PatternType.BOMB, ranks[0])
        
        # 对子：两张相同
        if len(cards) == 2 and len(set(ranks)) == 1:
            return Pattern(cards, PatternType.PAIR, ranks[0])
        
        # 单牌：单张（王不能单出）
        if len(cards) == 1:
            if cards[0].can_be_single():
                return Pattern(cards, PatternType.SINGLE, ranks[0])
            else:
                return Pattern(cards, PatternType.INVALID)
        
        # 连牌：连续≥3张（2和王不能参与）
        if len(cards) >= 3 and PatternAnalyzer._is_straight(ranks):
            return Pattern(cards, PatternType.STRAIGHT, max(ranks))
        
        # 连队：连续≥2对
        if len(cards) >= 4 and len(cards) % 2 == 0 and PatternAnalyzer._is_straight_pairs(rank_counts):
            return Pattern(cards, PatternType.STRAIGHT_PAIRS, max(ranks))
        
        return Pattern(cards, PatternType.INVALID)
    
    @staticmethod
    def _is_straight(ranks: List[Rank]) -> bool:
        """检查是否为连牌（连续≥3张，不能有2和王）"""
        # 检查是否都能参与顺子
        if not all(rank.can_be_in_straight() for rank in ranks):
            return False
        
        # 检查是否有重复
        if len(set(ranks)) != len(ranks):
            return False
        
        # 排序并检查连续性
        sorted_ranks = sorted(ranks, key=lambda x: x.rank_value)
        for i in range(1, len(sorted_ranks)):
            if sorted_ranks[i].rank_value - sorted_ranks[i-1].rank_value != 1:
                return False
        
        return True
    
    @staticmethod
    def _is_straight_pairs(rank_counts: Dict[Rank, int]) -> bool:
        """检查是否为连队（连续≥2对）"""
        # 所有牌都必须是对子
        if not all(count == 2 for count in rank_counts.values()):
            return False
        
        # 检查是否都能参与顺子
        ranks = list(rank_counts.keys())
        if not all(rank.can_be_in_straight() for rank in ranks):
            return False
        
        # 检查连续性
        sorted_ranks = sorted(ranks, key=lambda x: x.rank_value)
        for i in range(1, len(sorted_ranks)):
            if sorted_ranks[i].rank_value - sorted_ranks[i-1].rank_value != 1:
                return False
        
        return True
    
    @staticmethod
    def find_all_patterns(hand: List[Card]) -> List[Pattern]:
        """找出手牌中所有可能的牌型组合"""
        patterns = []
        hand = sorted(hand)
        
        # 单张
        for card in hand:
            pattern = PatternAnalyzer.analyze_cards([card])
            if pattern.pattern_type != PatternType.INVALID:
                patterns.append(pattern)
        
        # 对子
        patterns.extend(PatternAnalyzer._find_pairs(hand))
        
        # 三张
        patterns.extend(PatternAnalyzer._find_triples(hand))
        
        # 四张
        patterns.extend(PatternAnalyzer._find_hydrogen_bombs(hand))
        
        # 双王炸弹
        double_joker = PatternAnalyzer._find_double_joker(hand)
        if double_joker:
            patterns.append(double_joker)
        
        # 连牌
        patterns.extend(PatternAnalyzer._find_straights(hand))
        
        # 连队
        patterns.extend(PatternAnalyzer._find_straight_pairs(hand))
        
        return patterns
    
    @staticmethod
    def _find_pairs(hand: List[Card]) -> List[Pattern]:
        """找出所有对子"""
        pairs = []
        rank_groups = PatternAnalyzer._group_by_rank(hand)
        
        for rank, cards in rank_groups.items():
            if len(cards) >= 2:
                pairs.append(Pattern(cards[:2], PatternType.PAIR, rank))
        
        return pairs
    
    @staticmethod
    def _find_triples(hand: List[Card]) -> List[Pattern]:
        """找出所有三张"""
        triples = []
        rank_groups = PatternAnalyzer._group_by_rank(hand)
        
        for rank, cards in rank_groups.items():
            if len(cards) >= 3:
                triples.append(Pattern(cards[:3], PatternType.BOMB, rank))
        
        return triples
    
    @staticmethod
    def _find_hydrogen_bombs(hand: List[Card]) -> List[Pattern]:
        """找出所有氢弹"""
        hydrogen_bombs = []
        rank_groups = PatternAnalyzer._group_by_rank(hand)
        
        for rank, cards in rank_groups.items():
            if len(cards) == 4:
                hydrogen_bombs.append(Pattern(cards, PatternType.HYDROGEN_BOMB, rank))
        
        return hydrogen_bombs
    
    @staticmethod
    def _find_double_joker(hand: List[Card]) -> Optional[Pattern]:
        """找出双王炸弹"""
        jokers = [card for card in hand if card.rank in [Rank.SMALL_JOKER, Rank.BIG_JOKER]]
        if len(jokers) == 2:
            return Pattern(jokers, PatternType.DOUBLE_JOKER, Rank.BIG_JOKER)
        return None
    
    @staticmethod
    def _find_straights(hand: List[Card]) -> List[Pattern]:
        """找出所有连牌"""
        straights = []
        
        # 过滤掉2和王
        valid_cards = [card for card in hand if card.rank.can_be_in_straight()]
        
        if len(valid_cards) < 3:
            return straights
        
        # 按牌点分组
        rank_groups = PatternAnalyzer._group_by_rank(valid_cards)
        available_ranks = sorted(rank_groups.keys(), key=lambda x: x.rank_value)
        
        # 寻找连续的牌点
        for start_idx in range(len(available_ranks)):
            for length in range(3, len(available_ranks) - start_idx + 1):
                end_idx = start_idx + length
                consecutive_ranks = available_ranks[start_idx:end_idx]
                
                # 检查是否连续
                if PatternAnalyzer._is_straight(consecutive_ranks):
                    # 构建连牌
                    straight_cards = []
                    for rank in consecutive_ranks:
                        straight_cards.append(rank_groups[rank][0])  # 每个牌点取一张
                    
                    straights.append(Pattern(straight_cards, PatternType.STRAIGHT, max(consecutive_ranks)))
        
        return straights
    
    @staticmethod
    def _find_straight_pairs(hand: List[Card]) -> List[Pattern]:
        """找出所有连队"""
        straight_pairs = []
        
        # 过滤掉2和王
        valid_cards = [card for card in hand if card.rank.can_be_in_straight()]
        
        if len(valid_cards) < 4:
            return straight_pairs
        
        # 按牌点分组
        rank_groups = PatternAnalyzer._group_by_rank(valid_cards)
        
        # 只考虑有对子的牌点
        pair_ranks = [rank for rank, cards in rank_groups.items() if len(cards) >= 2]
        pair_ranks = sorted(pair_ranks, key=lambda x: x.rank_value)
        
        # 寻找连续的对子
        for start_idx in range(len(pair_ranks)):
            for length in range(2, len(pair_ranks) - start_idx + 1):
                end_idx = start_idx + length
                consecutive_ranks = pair_ranks[start_idx:end_idx]
                
                # 检查是否连续
                if PatternAnalyzer._is_straight(consecutive_ranks):
                    # 构建连队
                    straight_pair_cards = []
                    for rank in consecutive_ranks:
                        straight_pair_cards.extend(rank_groups[rank][:2])  # 每个牌点取两张
                    
                    straight_pairs.append(Pattern(straight_pair_cards, PatternType.STRAIGHT_PAIRS, max(consecutive_ranks)))
        
        return straight_pairs
    
    @staticmethod
    def _group_by_rank(cards: List[Card]) -> Dict[Rank, List[Card]]:
        """按牌点分组"""
        groups = {}
        for card in cards:
            if card.rank not in groups:
                groups[card.rank] = []
            groups[card.rank].append(card)
        return groups
    
    @staticmethod
    def find_valid_plays(hand: List[Card], last_pattern: Optional[Pattern] = None) -> List[Pattern]:
        """找出可以出的牌型（能压过上家或首次出牌）"""
        all_patterns = PatternAnalyzer.find_all_patterns(hand)
        
        if not last_pattern:
            # 首次出牌，可以出任意牌型
            return all_patterns
        
        # 找出能压过上家的牌型
        valid_patterns = []
        for pattern in all_patterns:
            if pattern.can_beat(last_pattern):
                valid_patterns.append(pattern)
        
        return valid_patterns