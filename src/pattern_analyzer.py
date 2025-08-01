"""
干瞪眼游戏 - 牌型分析器
"""

from typing import List, Dict, Optional
from collections import Counter
from .card import Card, CardPattern, CardType, Rank


class PatternAnalyzer:
    """牌型分析器"""
    
    @staticmethod
    def analyze_cards(cards: List[Card]) -> Optional[CardPattern]:
        """分析给定牌组的牌型"""
        if not cards:
            return None
        
        cards = sorted(cards)
        card_count = len(cards)
        
        # 单张
        if card_count == 1:
            return CardPattern(cards, CardType.SINGLE)
        
        # 王炸
        if card_count == 2 and PatternAnalyzer._is_joker_bomb(cards):
            return CardPattern(cards, CardType.JOKER_BOMB)
        
        # 对子
        if card_count == 2 and PatternAnalyzer._is_pair(cards):
            return CardPattern(cards, CardType.PAIR)
        
        # 三张
        if card_count == 3 and PatternAnalyzer._is_triple(cards):
            return CardPattern(cards, CardType.TRIPLE)
        
        # 三带一
        if card_count == 4 and PatternAnalyzer._is_triple_with_one(cards):
            return CardPattern(cards, CardType.TRIPLE_WITH_ONE)
        
        # 炸弹
        if card_count == 4 and PatternAnalyzer._is_bomb(cards):
            return CardPattern(cards, CardType.BOMB)
        
        # 顺子
        if card_count >= 5 and PatternAnalyzer._is_straight(cards):
            return CardPattern(cards, CardType.STRAIGHT)
        
        return None
    
    @staticmethod
    def _is_joker_bomb(cards: List[Card]) -> bool:
        """判断是否为王炸"""
        if len(cards) != 2:
            return False
        ranks = [card.rank for card in cards]
        return Rank.SMALL_JOKER in ranks and Rank.BIG_JOKER in ranks
    
    @staticmethod
    def _is_pair(cards: List[Card]) -> bool:
        """判断是否为对子"""
        if len(cards) != 2:
            return False
        return cards[0].rank == cards[1].rank
    
    @staticmethod
    def _is_triple(cards: List[Card]) -> bool:
        """判断是否为三张"""
        if len(cards) != 3:
            return False
        return cards[0].rank == cards[1].rank == cards[2].rank
    
    @staticmethod
    def _is_triple_with_one(cards: List[Card]) -> bool:
        """判断是否为三带一"""
        if len(cards) != 4:
            return False
        
        rank_count = Counter(card.rank for card in cards)
        counts = list(rank_count.values())
        return 3 in counts and 1 in counts
    
    @staticmethod
    def _is_bomb(cards: List[Card]) -> bool:
        """判断是否为炸弹"""
        if len(cards) != 4:
            return False
        return cards[0].rank == cards[1].rank == cards[2].rank == cards[3].rank
    
    @staticmethod
    def _is_straight(cards: List[Card]) -> bool:
        """判断是否为顺子"""
        if len(cards) < 5:
            return False
        
        # 顺子不能包含2和王
        for card in cards:
            if card.rank in [Rank.TWO, Rank.SMALL_JOKER, Rank.BIG_JOKER]:
                return False
        
        # 检查是否连续
        ranks = sorted([card.rank.rank_value for card in cards])
        for i in range(1, len(ranks)):
            if ranks[i] != ranks[i-1] + 1:
                return False
        
        return True
    
    @staticmethod
    def find_all_patterns(hand: List[Card]) -> List[CardPattern]:
        """找出手牌中所有可能的牌型组合"""
        patterns = []
        hand = sorted(hand)
        
        # 单张
        for card in hand:
            patterns.append(CardPattern([card], CardType.SINGLE))
        
        # 对子
        patterns.extend(PatternAnalyzer._find_pairs(hand))
        
        # 三张
        patterns.extend(PatternAnalyzer._find_triples(hand))
        
        # 三带一
        patterns.extend(PatternAnalyzer._find_triple_with_ones(hand))
        
        # 炸弹
        patterns.extend(PatternAnalyzer._find_bombs(hand))
        
        # 王炸
        joker_bomb = PatternAnalyzer._find_joker_bomb(hand)
        if joker_bomb:
            patterns.append(joker_bomb)
        
        # 顺子
        patterns.extend(PatternAnalyzer._find_straights(hand))
        
        return patterns
    
    @staticmethod
    def _find_pairs(hand: List[Card]) -> List[CardPattern]:
        """找出所有对子"""
        pairs = []
        rank_groups = PatternAnalyzer._group_by_rank(hand)
        
        for rank, cards in rank_groups.items():
            if len(cards) >= 2:
                pairs.append(CardPattern(cards[:2], CardType.PAIR))
        
        return pairs
    
    @staticmethod
    def _find_triples(hand: List[Card]) -> List[CardPattern]:
        """找出所有三张"""
        triples = []
        rank_groups = PatternAnalyzer._group_by_rank(hand)
        
        for rank, cards in rank_groups.items():
            if len(cards) >= 3:
                triples.append(CardPattern(cards[:3], CardType.TRIPLE))
        
        return triples
    
    @staticmethod
    def _find_triple_with_ones(hand: List[Card]) -> List[CardPattern]:
        """找出所有三带一"""
        triple_with_ones = []
        rank_groups = PatternAnalyzer._group_by_rank(hand)
        
        # 找出所有三张
        triple_ranks = [rank for rank, cards in rank_groups.items() if len(cards) >= 3]
        
        for triple_rank in triple_ranks:
            triple_cards = rank_groups[triple_rank][:3]
            
            # 找出可以带的单张
            for rank, cards in rank_groups.items():
                if rank != triple_rank and len(cards) >= 1:
                    single_card = cards[0]
                    pattern_cards = triple_cards + [single_card]
                    triple_with_ones.append(CardPattern(pattern_cards, CardType.TRIPLE_WITH_ONE))
        
        return triple_with_ones
    
    @staticmethod
    def _find_bombs(hand: List[Card]) -> List[CardPattern]:
        """找出所有炸弹"""
        bombs = []
        rank_groups = PatternAnalyzer._group_by_rank(hand)
        
        for rank, cards in rank_groups.items():
            if len(cards) == 4:
                bombs.append(CardPattern(cards, CardType.BOMB))
        
        return bombs
    
    @staticmethod
    def _find_joker_bomb(hand: List[Card]) -> Optional[CardPattern]:
        """找出王炸"""
        jokers = [card for card in hand if card.is_joker]
        if len(jokers) == 2:
            return CardPattern(jokers, CardType.JOKER_BOMB)
        return None
    
    @staticmethod
    def _find_straights(hand: List[Card]) -> List[CardPattern]:
        """找出所有顺子"""
        straights = []
        
        # 过滤掉2和王
        valid_cards = [card for card in hand if card.rank not in [Rank.TWO, Rank.SMALL_JOKER, Rank.BIG_JOKER]]
        
        if len(valid_cards) < 5:
            return straights
        
        # 按牌点分组
        rank_groups = PatternAnalyzer._group_by_rank(valid_cards)
        available_ranks = sorted(rank_groups.keys(), key=lambda x: x.rank_value)
        
        # 寻找连续的牌点
        for start_idx in range(len(available_ranks)):
            for length in range(5, len(available_ranks) - start_idx + 1):
                end_idx = start_idx + length
                consecutive_ranks = available_ranks[start_idx:end_idx]
                
                # 检查是否连续
                if PatternAnalyzer._is_consecutive(consecutive_ranks):
                    # 构建顺子
                    straight_cards = []
                    for rank in consecutive_ranks:
                        straight_cards.append(rank_groups[rank][0])  # 每个牌点取一张
                    
                    straights.append(CardPattern(straight_cards, CardType.STRAIGHT))
        
        return straights
    
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
    def _is_consecutive(ranks: List[Rank]) -> bool:
        """检查牌点是否连续"""
        if len(ranks) < 2:
            return True
        
        for i in range(1, len(ranks)):
            if ranks[i].rank_value != ranks[i-1].rank_value + 1:
                return False
        
        return True
    
    @staticmethod
    def find_valid_plays(hand: List[Card], last_pattern: Optional[CardPattern] = None) -> List[CardPattern]:
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