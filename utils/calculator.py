"""
Credit Card Value Calculator
The brain of the recommendation engine that calculates net annual benefit
"""

from typing import Dict, Any, List, Tuple
from data.credit_cards import POINT_VALUATION


def calculate_annual_spend(monthly_spends: Dict[str, int]) -> Dict[str, int]:
    """Convert monthly spends to annual spends"""
    return {category: amount * 12 for category, amount in monthly_spends.items()}


def calculate_total_spend(spends: Dict[str, int]) -> int:
    """Calculate total spend across all categories"""
    return sum(spends.values())


def check_eligibility(card: Dict[str, Any], monthly_salary: int) -> bool:
    """Check if user is eligible for the card based on salary"""
    return monthly_salary >= card["min_salary_req"]


def calculate_effective_fee(card: Dict[str, Any], annual_spend: int) -> int:
    """
    Calculate the effective annual fee after considering fee waiver threshold
    Returns 0 if annual spend exceeds the waiver threshold
    """
    if card["fee_waiver_threshold"] == 0:
        # Lifetime free card
        return 0
    elif annual_spend >= card["fee_waiver_threshold"]:
        # Fee waived due to spend threshold
        return 0
    else:
        return card["annual_fee"]


def calculate_base_rewards(
    card: Dict[str, Any], 
    annual_spends: Dict[str, int]
) -> Tuple[float, Dict[str, float]]:
    """
    Calculate rewards based on base rate and category multipliers
    Returns total reward value and breakdown by category
    """
    bank = card["bank"]
    point_value = POINT_VALUATION.get(bank, 0.25)
    
    category_rewards = {}
    total_rewards = 0.0
    
    # Map user spend categories to card multipliers
    category_mapping = {
        "general": "base",
        "travel": "travel",
        "dining": "dining",
        "online": "online",
        "utilities": "utilities",
    }
    
    for user_category, amount in annual_spends.items():
        if user_category == "general":
            # Apply base reward rate
            reward_rate = card["base_reward_rate"]
        else:
            # Try to get category multiplier, fall back to base rate
            reward_rate = card["category_multipliers"].get(
                user_category, card["base_reward_rate"]
            )
        
        reward_value = amount * reward_rate
        category_rewards[user_category] = reward_value
        total_rewards += reward_value
    
    return total_rewards, category_rewards


def calculate_milestone_benefits(
    card: Dict[str, Any], 
    annual_spend: int
) -> Tuple[float, List[str]]:
    """
    Calculate milestone benefits based on annual spend
    Returns total milestone value and list of achieved milestones
    """
    bank = card["bank"]
    point_value = POINT_VALUATION.get(bank, 0.25)
    
    total_milestone_value = 0.0
    achieved_milestones = []
    
    for threshold, points in card["milestone_benefits"].items():
        threshold_int = int(threshold) if isinstance(threshold, str) else threshold
        if annual_spend >= threshold_int:
            value = points * point_value
            total_milestone_value += value
            achieved_milestones.append(
                f"₹{threshold_int:,} spend → {points:,} points (₹{value:,.0f})"
            )
    
    return total_milestone_value, achieved_milestones


def calculate_lounge_value(card: Dict[str, Any], needs_lounge: bool) -> float:
    """
    Calculate the value of lounge access
    Assuming ₹1,500 per lounge visit saved
    """
    if not needs_lounge:
        return 0.0
    
    LOUNGE_VALUE_PER_VISIT = 1500  # ₹1,500 per visit
    quarterly_visits = card["lounge_visits_per_quarter"]
    
    if quarterly_visits >= 999:  # Unlimited
        # Assume 12 visits per year for unlimited
        return 12 * LOUNGE_VALUE_PER_VISIT
    
    annual_visits = quarterly_visits * 4
    return annual_visits * LOUNGE_VALUE_PER_VISIT


def calculate_net_value(
    card: Dict[str, Any],
    monthly_salary: int,
    monthly_spends: Dict[str, int],
    needs_lounge: bool = False,
    is_first_year: bool = False,
) -> Dict[str, Any]:
    """
    Main calculation function that computes the net annual benefit
    
    Returns a dictionary with:
    - is_eligible: Boolean
    - net_value: Net annual benefit (rewards - fees)
    - breakdown: Detailed breakdown of all components
    - why_recommended: Explanation for why this card scored well/poorly
    """
    # Check eligibility
    is_eligible = check_eligibility(card, monthly_salary)
    
    if not is_eligible:
        return {
            "card_name": card["card_name"],
            "bank": card["bank"],
            "is_eligible": False,
            "net_value": 0,
            "reason": f"Requires minimum salary of ₹{card['min_salary_req']:,}/month",
            "breakdown": {},
        }
    
    # Calculate annual spends
    annual_spends = calculate_annual_spend(monthly_spends)
    total_annual_spend = calculate_total_spend(annual_spends)
    
    # Calculate effective fee
    effective_fee = calculate_effective_fee(card, total_annual_spend)
    fee_waived = effective_fee == 0 and card["annual_fee"] > 0
    
    # Calculate rewards
    total_rewards, category_rewards = calculate_base_rewards(card, annual_spends)
    
    # Calculate milestone benefits
    milestone_value, achieved_milestones = calculate_milestone_benefits(
        card, total_annual_spend
    )
    
    # Calculate lounge value
    lounge_value = calculate_lounge_value(card, needs_lounge)
    
    # Welcome benefit (first year only)
    welcome_value = card["welcome_benefit"] if is_first_year else 0
    
    # Calculate net value
    gross_benefits = total_rewards + milestone_value + lounge_value + welcome_value
    net_value = gross_benefits - effective_fee
    
    # Calculate effective reward rate
    effective_reward_rate = (total_rewards / total_annual_spend * 100) if total_annual_spend > 0 else 0
    
    # Generate recommendation reason
    reasons = []
    
    # Find the best category
    if category_rewards:
        best_category = max(category_rewards, key=category_rewards.get)
        best_category_value = category_rewards[best_category]
        if best_category_value > 0:
            rate = card["category_multipliers"].get(best_category, card["base_reward_rate"])
            reasons.append(f"{rate*100:.1f}% rewards on {best_category} spend")
    
    if fee_waived:
        reasons.append(f"Fee waived (spend > ₹{card['fee_waiver_threshold']:,})")
    elif card["annual_fee"] == 0:
        reasons.append("Lifetime free card")
    
    if achieved_milestones:
        reasons.append(f"{len(achieved_milestones)} milestone benefit(s) achieved")
    
    if lounge_value > 0:
        visits = card["lounge_visits_per_quarter"] * 4
        if card["lounge_visits_per_quarter"] >= 999:
            reasons.append("Unlimited lounge access")
        else:
            reasons.append(f"{visits} lounge visits/year")
    
    return {
        "card_name": card["card_name"],
        "bank": card["bank"],
        "card_type": card["card_type"],
        "is_eligible": True,
        "net_value": net_value,
        "effective_reward_rate": effective_reward_rate,
        "breakdown": {
            "annual_fee": card["annual_fee"],
            "effective_fee": effective_fee,
            "fee_waived": fee_waived,
            "total_rewards": total_rewards,
            "category_rewards": category_rewards,
            "milestone_value": milestone_value,
            "achieved_milestones": achieved_milestones,
            "lounge_value": lounge_value,
            "welcome_value": welcome_value,
            "gross_benefits": gross_benefits,
            "total_annual_spend": total_annual_spend,
        },
        "why_recommended": " | ".join(reasons) if reasons else "Basic rewards on all spends",
        "lounge_access": card["lounge_access"],
        "description": card["description"],
    }


def rank_cards(
    cards: List[Dict[str, Any]],
    monthly_salary: int,
    monthly_spends: Dict[str, int],
    needs_lounge: bool = False,
    lifetime_free_only: bool = False,
    is_first_year: bool = False,
) -> List[Dict[str, Any]]:
    """
    Rank all cards based on net value for the user's profile
    Returns sorted list of card analysis results
    """
    results = []
    
    for card in cards:
        # Filter for lifetime free if requested
        if lifetime_free_only and card["annual_fee"] > 0:
            continue
        
        # Filter for lounge access if required
        if needs_lounge and card["lounge_visits_per_quarter"] == 0:
            continue
        
        analysis = calculate_net_value(
            card=card,
            monthly_salary=monthly_salary,
            monthly_spends=monthly_spends,
            needs_lounge=needs_lounge,
            is_first_year=is_first_year,
        )
        
        if analysis["is_eligible"]:
            results.append(analysis)
    
    # Sort by net value (descending)
    results.sort(key=lambda x: x["net_value"], reverse=True)
    
    return results
