"""
Best Credit Card Guide for India
A Streamlit web application to analyze and recommend credit cards
based on user salary, spending habits, and preferences.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data.credit_cards import get_all_cards, POINT_VALUATION
from utils.calculator import rank_cards, calculate_total_spend

# Page configuration
st.set_page_config(
    page_title="Best Credit Card Guide - India",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #64748B;
        text-align: center;
        margin-bottom: 2rem;
    }
    .card-winner {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        color: white;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: #F8FAFC;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #E2E8F0;
    }
    .stMetric {
        background: #F8FAFC;
        padding: 1rem;
        border-radius: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)


def format_currency(amount: float) -> str:
    """Format amount as Indian currency"""
    if amount >= 100000:
        return f"₹{amount/100000:.1f}L"
    elif amount >= 1000:
        return f"₹{amount/1000:.1f}K"
    else:
        return f"₹{amount:,.0f}"


def create_sidebar():
    """Create the sidebar with user inputs"""
    st.sidebar.markdown("## 👤 Your Profile")
    st.sidebar.markdown("---")
    
    # Monthly Salary
    monthly_salary = st.sidebar.number_input(
        "💰 Monthly Salary (₹)",
        min_value=10000,
        max_value=10000000,
        value=75000,
        step=5000,
        help="Your monthly income to check card eligibility",
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("## 💸 Monthly Spends")
    
    # Spending breakdown
    general_spend = st.sidebar.number_input(
        "🛒 General/Retail Spend (₹)",
        min_value=0,
        max_value=1000000,
        value=15000,
        step=1000,
        help="Everyday purchases, groceries, etc.",
    )
    
    travel_spend = st.sidebar.number_input(
        "✈️ Travel Spend (₹)",
        min_value=0,
        max_value=1000000,
        value=5000,
        step=1000,
        help="Flights, hotels, travel bookings",
    )
    
    dining_spend = st.sidebar.number_input(
        "🍽️ Dining/Food Ordering (₹)",
        min_value=0,
        max_value=500000,
        value=5000,
        step=500,
        help="Restaurants, Swiggy, Zomato, etc.",
    )
    
    online_spend = st.sidebar.number_input(
        "🛍️ Online Shopping (₹)",
        min_value=0,
        max_value=1000000,
        value=10000,
        step=1000,
        help="Amazon, Flipkart, Myntra, etc.",
    )
    
    utility_spend = st.sidebar.number_input(
        "💡 Utility Bills (₹)",
        min_value=0,
        max_value=200000,
        value=5000,
        step=500,
        help="Electricity, phone, internet, etc.",
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("## ⚙️ Preferences")
    
    needs_lounge = st.sidebar.checkbox(
        "🛋️ Lounge Access Required",
        value=False,
        help="Filter for cards with airport lounge access",
    )
    
    lifetime_free_only = st.sidebar.checkbox(
        "🆓 Lifetime Free Cards Only",
        value=False,
        help="Show only cards with no annual fee",
    )
    
    is_first_year = st.sidebar.checkbox(
        "🎁 Include Welcome Benefits",
        value=True,
        help="Include first-year welcome bonuses in calculation",
    )
    
    monthly_spends = {
        "general": general_spend,
        "travel": travel_spend,
        "dining": dining_spend,
        "online": online_spend,
        "utilities": utility_spend,
    }
    
    return monthly_salary, monthly_spends, needs_lounge, lifetime_free_only, is_first_year


def display_winner_card(winner: dict):
    """Display the top recommended card with details"""
    st.markdown("### 🏆 Top Recommendation")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #10B981 0%, #059669 100%); 
                    padding: 1.5rem; border-radius: 1rem; color: white;">
            <h2 style="margin: 0; color: white;">{winner['card_name']}</h2>
            <p style="margin: 0.5rem 0; opacity: 0.9;">{winner['bank']} • {winner['card_type']}</p>
            <h3 style="margin: 1rem 0 0.5rem 0; color: white;">Net Annual Benefit: ₹{winner['net_value']:,.0f}</h3>
            <p style="margin: 0; font-size: 0.9rem; opacity: 0.9;">
                Effective Reward Rate: {winner['effective_reward_rate']:.2f}%
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"**📝 Why this card?** {winner['why_recommended']}")
        st.markdown(f"*{winner['description']}*")
    
    with col2:
        breakdown = winner['breakdown']
        st.metric("💰 Total Rewards", f"₹{breakdown['total_rewards']:,.0f}")
        st.metric("🎯 Milestone Bonus", f"₹{breakdown['milestone_value']:,.0f}")
        
        if breakdown['fee_waived']:
            st.metric("📋 Annual Fee", "₹0 (Waived)", delta="Waived!")
        else:
            st.metric("📋 Annual Fee", f"₹{breakdown['effective_fee']:,}")
        
        if breakdown['lounge_value'] > 0:
            st.metric("🛋️ Lounge Value", f"₹{breakdown['lounge_value']:,.0f}")


def display_comparison_table(results: list):
    """Display comparison table for all eligible cards"""
    st.markdown("### 📊 Card Comparison Table")
    
    table_data = []
    for r in results:
        table_data.append({
            "Card Name": r['card_name'],
            "Bank": r['bank'],
            "Annual Fee": f"₹{r['breakdown']['annual_fee']:,}",
            "Effective Fee": f"₹{r['breakdown']['effective_fee']:,}" if not r['breakdown']['fee_waived'] else "₹0 ✓",
            "Net Benefit": f"₹{r['net_value']:,.0f}",
            "Reward Rate": f"{r['effective_reward_rate']:.2f}%",
            "Lounge Access": r['lounge_access'] if r['lounge_access'] != "None" else "❌",
        })
    
    df = pd.DataFrame(table_data)
    
    # Style the dataframe
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Net Benefit": st.column_config.TextColumn("Net Benefit 💰"),
            "Card Name": st.column_config.TextColumn("Card Name 💳"),
        }
    )


def display_chart(results: list):
    """Display bar chart comparing net values"""
    st.markdown("### 📈 Visual Comparison")
    
    # Prepare data for chart
    chart_data = pd.DataFrame([
        {
            "Card": f"{r['card_name']}\n({r['bank']})",
            "Net Benefit (₹)": r['net_value'],
            "Bank": r['bank'],
        }
        for r in results[:8]  # Top 8 cards
    ])
    
    # Create color scale based on bank
    colors = {
        "HDFC": "#004C8F",
        "SBI": "#22409A",
        "Axis": "#97144D",
        "ICICI": "#F58220",
        "Amex": "#006FCF",
        "RBL": "#E31837",
        "IndusInd": "#98002E",
    }
    
    fig = px.bar(
        chart_data,
        x="Card",
        y="Net Benefit (₹)",
        color="Bank",
        color_discrete_map=colors,
        title="Net Annual Benefit by Card",
    )
    
    fig.update_layout(
        xaxis_title="",
        yaxis_title="Net Annual Benefit (₹)",
        showlegend=True,
        height=400,
        xaxis_tickangle=-45,
    )
    
    fig.update_traces(
        texttemplate='₹%{y:,.0f}',
        textposition='outside',
    )
    
    st.plotly_chart(fig, use_container_width=True)


def display_detailed_breakdown(results: list):
    """Display detailed breakdown for top cards"""
    st.markdown("### 🔍 Detailed Analysis")
    
    tabs = st.tabs([f"#{i+1} {r['card_name']}" for i, r in enumerate(results[:5])])
    
    for i, tab in enumerate(tabs):
        with tab:
            result = results[i]
            breakdown = result['breakdown']
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**💵 Fee Structure**")
                st.write(f"Annual Fee: ₹{breakdown['annual_fee']:,}")
                if breakdown['fee_waived']:
                    st.write("✅ Fee Waived (spending threshold met)")
                elif breakdown['annual_fee'] == 0:
                    st.write("✅ Lifetime Free Card")
                else:
                    st.write(f"❌ Fee Applies: ₹{breakdown['effective_fee']:,}")
            
            with col2:
                st.markdown("**🎁 Rewards Earned**")
                for category, value in breakdown['category_rewards'].items():
                    if value > 0:
                        st.write(f"{category.title()}: ₹{value:,.0f}")
                st.write(f"**Total: ₹{breakdown['total_rewards']:,.0f}**")
            
            with col3:
                st.markdown("**🎯 Milestones & Extras**")
                if breakdown['achieved_milestones']:
                    for milestone in breakdown['achieved_milestones']:
                        st.write(f"✅ {milestone}")
                else:
                    st.write("No milestones achieved")
                
                if breakdown['lounge_value'] > 0:
                    st.write(f"🛋️ Lounge Value: ₹{breakdown['lounge_value']:,.0f}")
                
                if breakdown['welcome_value'] > 0:
                    st.write(f"🎁 Welcome Benefit: ₹{breakdown['welcome_value']:,.0f}")


def display_spend_summary(monthly_spends: dict):
    """Display user's spend summary"""
    total_monthly = calculate_total_spend(monthly_spends)
    total_annual = total_monthly * 12
    
    st.markdown("### 📋 Your Spending Profile")
    
    cols = st.columns(len(monthly_spends) + 1)
    
    icons = {
        "general": "🛒",
        "travel": "✈️",
        "dining": "🍽️",
        "online": "🛍️",
        "utilities": "💡",
    }
    
    for i, (category, amount) in enumerate(monthly_spends.items()):
        with cols[i]:
            icon = icons.get(category, "💰")
            st.metric(
                f"{icon} {category.title()}",
                f"₹{amount:,}/mo",
                f"₹{amount*12:,}/yr",
            )
    
    with cols[-1]:
        st.metric(
            "📊 Total",
            f"₹{total_monthly:,}/mo",
            f"₹{total_annual:,}/yr",
        )


def main():
    """Main application function"""
    # Header
    st.markdown('<p class="main-header">💳 Best Credit Card Guide for India</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Find the perfect credit card based on your spending habits and preferences</p>', unsafe_allow_html=True)
    
    # Get user inputs from sidebar
    monthly_salary, monthly_spends, needs_lounge, lifetime_free_only, is_first_year = create_sidebar()
    
    # Get all cards and calculate rankings
    all_cards = get_all_cards()
    
    results = rank_cards(
        cards=all_cards,
        monthly_salary=monthly_salary,
        monthly_spends=monthly_spends,
        needs_lounge=needs_lounge,
        lifetime_free_only=lifetime_free_only,
        is_first_year=is_first_year,
    )
    
    # Display spend summary
    display_spend_summary(monthly_spends)
    
    st.markdown("---")
    
    # Check if we have any eligible cards
    if not results:
        st.warning("""
        ⚠️ **No eligible cards found!**
        
        This could be because:
        - Your salary doesn't meet the minimum requirements
        - You've selected filters that exclude all cards
        
        Try adjusting your filters or increasing your income level.
        """)
        
        # Show all cards anyway for reference
        st.markdown("### 📚 All Available Cards (for reference)")
        all_results = rank_cards(
            cards=all_cards,
            monthly_salary=10000000,  # High salary to show all
            monthly_spends=monthly_spends,
            needs_lounge=False,
            lifetime_free_only=False,
            is_first_year=is_first_year,
        )
        display_comparison_table(all_results)
        return
    
    # Display the winner
    display_winner_card(results[0])
    
    st.markdown("---")
    
    # Display chart
    display_chart(results)
    
    st.markdown("---")
    
    # Display comparison table
    display_comparison_table(results)
    
    st.markdown("---")
    
    # Display detailed breakdown
    display_detailed_breakdown(results)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #64748B; padding: 1rem;">
        <p>💡 <strong>Tip:</strong> Card values are calculated based on your specific spending pattern. 
        Actual benefits may vary based on redemption methods and promotional offers.</p>
        <p style="font-size: 0.8rem;">Point valuations used: HDFC/Axis/Amex = ₹0.50/point | SBI/ICICI/RBL = ₹0.25/point</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
