# 💳 Best Credit Card Guide for India

A comprehensive Streamlit web application that analyzes and recommends the best credit cards based on your salary, spending habits, and preferences.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.40+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ Features

- **Smart Eligibility Check**: Filters cards based on your monthly salary
- **Personalized Recommendations**: Calculates net annual benefit based on your spending pattern
- **Category Multipliers**: Considers special rewards for travel, dining, online shopping, etc.
- **Fee Analysis**: Accounts for fee waivers based on spending thresholds
- **Milestone Benefits**: Includes bonus rewards for hitting spending milestones
- **Lounge Access Valuation**: Calculates the monetary value of airport lounge access
- **Interactive Visualizations**: Beautiful charts comparing card benefits
- **Detailed Breakdowns**: See exactly how each card's value is calculated

## 🏦 Supported Cards

The app includes data for 12 popular Indian credit cards:

| Card | Bank | Type |
|------|------|------|
| HDFC Infinia | HDFC | Super Premium |
| HDFC Regalia Gold | HDFC | Premium |
| HDFC Diners Black | HDFC | Super Premium |
| SBI Cashback | SBI | Regular |
| SBI SimplyCLICK | SBI | Entry Level |
| Axis Atlas | Axis | Travel Premium |
| Axis Flipkart | Axis | Lifetime Free |
| ICICI Amazon Pay | ICICI | Co-branded |
| ICICI Coral | ICICI | Entry Premium |
| Amex Platinum Travel | Amex | Travel |
| RBL Shoprite | RBL | Lifetime Free |
| IndusInd Tiger | IndusInd | Lifetime Free |

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- [UV](https://github.com/astral-sh/uv) package manager (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd credit-card-guide-india
   ```

2. **Install dependencies with UV**
   ```bash
   uv sync
   ```

3. **Run the application**
   ```bash
   uv run streamlit run app.py
   ```

4. **Open your browser** and navigate to `http://localhost:8501`

### Alternative: Using pip

```bash
pip install streamlit pandas plotly
streamlit run app.py
```

## 📖 How It Works

### The Logic Engine

The recommendation engine calculates the **Net Annual Benefit** for each card:

```
Net Value = Total Rewards + Milestone Benefits + Lounge Value + Welcome Bonus - Effective Fee
```

#### 1. Eligibility Check
Cards are filtered based on minimum salary requirements.

#### 2. Fee Calculation
```python
if annual_spend >= fee_waiver_threshold:
    effective_fee = 0
else:
    effective_fee = annual_fee
```

#### 3. Reward Calculation
- **Base Rate**: Applied to general spending
- **Category Multipliers**: Higher rates for travel, dining, online shopping
- **Point Valuation**: Bank-specific point values (₹0.25 - ₹0.50 per point)

#### 4. Milestone Benefits
Bonus points/cashback for reaching spending thresholds (e.g., ₹4L, ₹8L annually)

#### 5. Lounge Value
Calculated at ₹1,500 per lounge visit saved

## 🎯 User Inputs

### Salary
Your monthly income determines which cards you're eligible for.

### Monthly Spends
- **General/Retail**: Everyday purchases, groceries
- **Travel**: Flights, hotels, travel bookings
- **Dining**: Restaurants, food delivery apps
- **Online Shopping**: Amazon, Flipkart, Myntra, etc.
- **Utilities**: Electricity, phone, internet bills

### Preferences
- **Lounge Access Required**: Filter for cards with airport lounge benefits
- **Lifetime Free Only**: Show only zero annual fee cards
- **Include Welcome Benefits**: Factor in first-year bonuses

## 📊 Output

1. **Top Recommendation**: The best card with detailed explanation
2. **Visual Comparison**: Bar chart of top eligible cards
3. **Comparison Table**: All eligible cards with key metrics
4. **Detailed Analysis**: Deep dive into top 5 cards

## 🛠️ Project Structure

```
credit-card-guide-india/
├── app.py                 # Main Streamlit application
├── pyproject.toml         # Project configuration (UV)
├── README.md              # Documentation
├── data/
│   ├── __init__.py
│   └── credit_cards.py    # Credit card database
└── utils/
    ├── __init__.py
    └── calculator.py      # Value calculation logic
```

## 🔧 Extending the Database

To add more cards, edit `data/credit_cards.py`:

```python
{
    "card_name": "New Card Name",
    "bank": "Bank Name",
    "annual_fee": 1000,
    "fee_waiver_threshold": 100000,
    "min_salary_req": 30000,
    "base_reward_rate": 0.01,
    "category_multipliers": {
        "travel": 0.02,
        "dining": 0.015,
        "online": 0.02,
        "utilities": 0.01,
    },
    "lounge_access": "4 per year",
    "lounge_visits_per_quarter": 1,
    "milestone_benefits": {
        100000: 1000,  # Spend ₹1L, get 1000 points
    },
    "fuel_surcharge_waiver": True,
    "card_type": "Regular",
    "joining_fee": 500,
    "welcome_benefit": 500,
    "description": "Card description",
}
```

## 📝 Point Valuations

| Bank | Point Value |
|------|-------------|
| HDFC | ₹0.50 |
| Axis | ₹0.50 |
| Amex | ₹0.50 |
| IndusInd | ₹0.50 |
| SBI | ₹0.25 |
| ICICI | ₹0.25 |
| RBL | ₹0.25 |

## ⚠️ Disclaimer

This tool is for informational purposes only. Card features, fees, and reward rates may change. Always verify current terms with the issuing bank before applying for a credit card.

## 📄 License

MIT License - feel free to use and modify for your needs.

## 🤝 Contributing

Contributions are welcome! Please feel free to:
- Add more credit cards to the database
- Improve the calculation logic
- Enhance the UI/UX
- Fix bugs or issues

---

Made with ❤️ for the Indian credit card community
