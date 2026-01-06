"""
Credit Card Database for Indian Cards
Contains detailed information about popular Indian credit cards including:
- Fee structure
- Reward rates
- Category multipliers
- Milestone benefits
- Lounge access
"""

from typing import List, Dict, Any

# Point valuation rates (₹ per point for different banks)
POINT_VALUATION = {
    "HDFC": 0.50,  # HDFC points valued at ₹0.50 each
    "SBI": 0.25,  # SBI points valued at ₹0.25 each
    "Axis": 0.50,  # Axis Edge points valued at ₹0.50 each
    "ICICI": 0.25,  # ICICI payback points valued at ₹0.25 each
    "Amex": 0.50,  # Amex MR points valued at ₹0.50 each
    "RBL": 0.25,  # RBL points
    "IndusInd": 0.50,  # IndusInd points
}

# Comprehensive Indian Credit Card Database
CREDIT_CARDS: List[Dict[str, Any]] = [
    {
        "card_name": "HDFC Infinia",
        "bank": "HDFC",
        "annual_fee": 12500,
        "fee_waiver_threshold": 1000000,  # ₹10L annual spend for fee waiver
        "min_salary_req": 300000,  # ₹3L monthly income
        "base_reward_rate": 0.033,  # 3.3% (5 points per ₹150)
        "category_multipliers": {
            "travel": 0.05,  # 5% on travel bookings via SmartBuy
            "dining": 0.033,
            "online": 0.033,
            "utilities": 0.033,
        },
        "lounge_access": "Unlimited domestic & international",
        "lounge_visits_per_quarter": 999,  # Unlimited
        "milestone_benefits": {
            800000: 10000,  # ₹8L spend = 10,000 bonus points (₹5,000 value)
            1500000: 25000,  # ₹15L spend = 25,000 bonus points (₹12,500 value)
        },
        "fuel_surcharge_waiver": True,
        "card_type": "Super Premium",
        "joining_fee": 12500,
        "welcome_benefit": 12500,  # Welcome points worth ₹12,500
        "description": "India's most premium card with unmatched rewards and luxury benefits",
    },
    {
        "card_name": "HDFC Regalia Gold",
        "bank": "HDFC",
        "annual_fee": 2500,
        "fee_waiver_threshold": 300000,  # ₹3L annual spend
        "min_salary_req": 60000,  # ₹60K monthly income
        "base_reward_rate": 0.02,  # 2% (4 points per ₹150)
        "category_multipliers": {
            "travel": 0.04,  # 4% on SmartBuy
            "dining": 0.02,
            "online": 0.02,
            "utilities": 0.02,
        },
        "lounge_access": "8 per year (domestic & international)",
        "lounge_visits_per_quarter": 2,
        "milestone_benefits": {
            500000: 5000,  # ₹5L spend = 5,000 bonus points
        },
        "fuel_surcharge_waiver": True,
        "card_type": "Premium",
        "joining_fee": 2500,
        "welcome_benefit": 2500,
        "description": "Great all-rounder for mid-income professionals",
    },
    {
        "card_name": "HDFC Diners Black",
        "bank": "HDFC",
        "annual_fee": 10000,
        "fee_waiver_threshold": 500000,  # ₹5L annual spend
        "min_salary_req": 175000,  # ₹1.75L monthly income
        "base_reward_rate": 0.033,  # 3.3%
        "category_multipliers": {
            "travel": 0.10,  # 10x on SmartBuy = 10%
            "dining": 0.10,  # 10x on dining
            "online": 0.033,
            "utilities": 0.033,
        },
        "lounge_access": "Unlimited via Diners Club network",
        "lounge_visits_per_quarter": 999,
        "milestone_benefits": {
            400000: 10000,  # ₹4L = 10,000 points
            800000: 25000,  # ₹8L = 25,000 points
        },
        "fuel_surcharge_waiver": True,
        "card_type": "Super Premium",
        "joining_fee": 10000,
        "welcome_benefit": 10000,
        "description": "Best for dining and travel with 10x rewards on SmartBuy",
    },
    {
        "card_name": "SBI Cashback Card",
        "bank": "SBI",
        "annual_fee": 999,
        "fee_waiver_threshold": 200000,  # ₹2L annual spend
        "min_salary_req": 30000,  # ₹30K monthly income
        "base_reward_rate": 0.01,  # 1% cashback
        "category_multipliers": {
            "travel": 0.01,
            "dining": 0.01,
            "online": 0.05,  # 5% on online spends
            "utilities": 0.01,
        },
        "lounge_access": "4 per year (domestic)",
        "lounge_visits_per_quarter": 1,
        "milestone_benefits": {},
        "fuel_surcharge_waiver": True,
        "card_type": "Regular",
        "joining_fee": 999,
        "welcome_benefit": 0,
        "description": "Best for online shoppers with 5% cashback on online purchases",
    },
    {
        "card_name": "SBI SimplyCLICK",
        "bank": "SBI",
        "annual_fee": 499,
        "fee_waiver_threshold": 100000,  # ₹1L annual spend
        "min_salary_req": 25000,  # ₹25K monthly income
        "base_reward_rate": 0.0125,  # 1.25% (5 points per ₹100, 1 point = ₹0.25)
        "category_multipliers": {
            "travel": 0.0125,
            "dining": 0.0125,
            "online": 0.025,  # 10x on partner sites = 2.5%
            "utilities": 0.0125,
        },
        "lounge_access": "None",
        "lounge_visits_per_quarter": 0,
        "milestone_benefits": {
            100000: 2000,  # ₹1L = 2,000 bonus points
            200000: 2000,  # Additional ₹2L = 2,000 more
        },
        "fuel_surcharge_waiver": True,
        "card_type": "Entry Level",
        "joining_fee": 499,
        "welcome_benefit": 500,
        "description": "Perfect entry-level card for online shopping enthusiasts",
    },
    {
        "card_name": "Axis Atlas",
        "bank": "Axis",
        "annual_fee": 5000,
        "fee_waiver_threshold": 1500000,  # No easy waiver, spend ₹15L
        "min_salary_req": 125000,  # ₹1.25L monthly income
        "base_reward_rate": 0.02,  # 2% (5 EDGE miles per ₹200)
        "category_multipliers": {
            "travel": 0.05,  # 5% on travel (flight/hotel bookings)
            "dining": 0.02,
            "online": 0.02,
            "utilities": 0.02,
        },
        "lounge_access": "8 international + 8 domestic per year",
        "lounge_visits_per_quarter": 4,
        "milestone_benefits": {
            750000: 7500,  # ₹7.5L spend = 15,000 bonus miles
            1500000: 12500,  # ₹15L spend = 25,000 bonus miles
        },
        "fuel_surcharge_waiver": True,
        "card_type": "Travel Premium",
        "joining_fee": 5000,
        "welcome_benefit": 5000,
        "description": "Best travel card for frequent flyers with EDGE miles",
    },
    {
        "card_name": "Axis Flipkart",
        "bank": "Axis",
        "annual_fee": 500,
        "fee_waiver_threshold": 0,  # Lifetime Free
        "min_salary_req": 15000,  # ₹15K monthly income
        "base_reward_rate": 0.015,  # 1.5% on general
        "category_multipliers": {
            "travel": 0.015,
            "dining": 0.015,
            "online": 0.05,  # 5% on Flipkart
            "utilities": 0.015,
        },
        "lounge_access": "4 per year (domestic)",
        "lounge_visits_per_quarter": 1,
        "milestone_benefits": {},
        "fuel_surcharge_waiver": True,
        "card_type": "Lifetime Free",
        "joining_fee": 0,
        "welcome_benefit": 0,
        "description": "Lifetime free card with excellent Flipkart rewards",
    },
    {
        "card_name": "ICICI Amazon Pay",
        "bank": "ICICI",
        "annual_fee": 500,
        "fee_waiver_threshold": 0,  # Effectively LTF for Prime members
        "min_salary_req": 20000,  # ₹20K monthly income
        "base_reward_rate": 0.01,  # 1% on general
        "category_multipliers": {
            "travel": 0.01,
            "dining": 0.01,
            "online": 0.05,  # 5% on Amazon (Prime members)
            "utilities": 0.02,  # 2% on bill payments
        },
        "lounge_access": "None",
        "lounge_visits_per_quarter": 0,
        "milestone_benefits": {},
        "fuel_surcharge_waiver": True,
        "card_type": "Co-branded",
        "joining_fee": 0,
        "welcome_benefit": 500,  # Amazon voucher
        "description": "Best for Amazon shoppers with 5% cashback for Prime members",
    },
    {
        "card_name": "ICICI Coral",
        "bank": "ICICI",
        "annual_fee": 500,
        "fee_waiver_threshold": 150000,  # ₹1.5L annual spend
        "min_salary_req": 30000,  # ₹30K monthly income
        "base_reward_rate": 0.01,  # 2 payback points per ₹100
        "category_multipliers": {
            "travel": 0.01,
            "dining": 0.02,  # 2x on dining
            "online": 0.01,
            "utilities": 0.01,
        },
        "lounge_access": "1 per quarter (domestic)",
        "lounge_visits_per_quarter": 1,
        "milestone_benefits": {},
        "fuel_surcharge_waiver": True,
        "card_type": "Entry Premium",
        "joining_fee": 500,
        "welcome_benefit": 500,
        "description": "Good starter card with dining benefits and lounge access",
    },
    {
        "card_name": "Amex Platinum Travel",
        "bank": "Amex",
        "annual_fee": 3500,
        "fee_waiver_threshold": 0,  # No fee waiver
        "min_salary_req": 50000,  # ₹50K monthly income
        "base_reward_rate": 0.01,  # 1 MR point per ₹50 = 1%
        "category_multipliers": {
            "travel": 0.05,  # 5x on travel = 5%
            "dining": 0.01,
            "online": 0.01,
            "utilities": 0.01,
        },
        "lounge_access": "4 per quarter (domestic)",
        "lounge_visits_per_quarter": 4,
        "milestone_benefits": {
            190000: 10000,  # 10,000 bonus MR points at ₹1.9L
            400000: 20000,  # 20,000 bonus MR points at ₹4L
        },
        "fuel_surcharge_waiver": False,
        "card_type": "Travel",
        "joining_fee": 3500,
        "welcome_benefit": 5000,
        "description": "Best for travelers with Amex network and milestone rewards",
    },
    {
        "card_name": "RBL Shoprite",
        "bank": "RBL",
        "annual_fee": 0,
        "fee_waiver_threshold": 0,  # Lifetime Free
        "min_salary_req": 15000,  # ₹15K monthly income
        "base_reward_rate": 0.0125,  # 1.25%
        "category_multipliers": {
            "travel": 0.0125,
            "dining": 0.0125,
            "online": 0.025,  # 2.5% on grocery & online
            "utilities": 0.0125,
        },
        "lounge_access": "None",
        "lounge_visits_per_quarter": 0,
        "milestone_benefits": {},
        "fuel_surcharge_waiver": True,
        "card_type": "Lifetime Free",
        "joining_fee": 0,
        "welcome_benefit": 0,
        "description": "Completely free card with decent rewards for everyday spends",
    },
    {
        "card_name": "IndusInd Tiger",
        "bank": "IndusInd",
        "annual_fee": 0,
        "fee_waiver_threshold": 0,  # Lifetime Free
        "min_salary_req": 20000,  # ₹20K monthly income
        "base_reward_rate": 0.0175,  # 1.75%
        "category_multipliers": {
            "travel": 0.0175,
            "dining": 0.0175,
            "online": 0.035,  # 2x on weekends
            "utilities": 0.0175,
        },
        "lounge_access": "2 per quarter (domestic)",
        "lounge_visits_per_quarter": 2,
        "milestone_benefits": {
            50000: 500,  # ₹50K = 500 bonus points
            100000: 1000,  # ₹1L = 1,000 bonus points
        },
        "fuel_surcharge_waiver": True,
        "card_type": "Lifetime Free",
        "joining_fee": 0,
        "welcome_benefit": 0,
        "description": "Great lifetime free card with lounge access and weekend rewards",
    },
]


def get_all_cards() -> List[Dict[str, Any]]:
    """Returns the complete list of credit cards"""
    return CREDIT_CARDS


def get_lifetime_free_cards() -> List[Dict[str, Any]]:
    """Returns only lifetime free cards"""
    return [card for card in CREDIT_CARDS if card["annual_fee"] == 0]


def get_cards_by_bank(bank: str) -> List[Dict[str, Any]]:
    """Filter cards by bank name"""
    return [card for card in CREDIT_CARDS if card["bank"].lower() == bank.lower()]


def get_eligible_cards(monthly_salary: int) -> List[Dict[str, Any]]:
    """Filter cards based on salary eligibility"""
    return [card for card in CREDIT_CARDS if card["min_salary_req"] <= monthly_salary]


def get_cards_with_lounge_access() -> List[Dict[str, Any]]:
    """Returns cards that offer lounge access"""
    return [card for card in CREDIT_CARDS if card["lounge_visits_per_quarter"] > 0]
