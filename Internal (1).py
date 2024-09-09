import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Streamlit app
st.title('Internal Consistency')

# Upload financial data
financial_data_file = st.file_uploader("Upload the financial data CSV", type="csv")
annual_report_file = st.file_uploader("Upload the annual report CSV", type="csv")

if financial_data_file is not None and annual_report_file is not None:
    financial_data = pd.read_csv(financial_data_file)
    annual_report = pd.read_csv(annual_report_file)
    
    # Calculate net cash flow for financial data
    financial_data['Net Cash Flow'] = (
        financial_data['Net cash flow by operating activity'] +
        financial_data['Net cash flow by investing activity'] +
        financial_data['Net cash flow by financial activity']
    )
    
    # Add calculated column to annual report data
    annual_report['Net Cash Flow Calculated'] = (
        annual_report['Net cash flow by operating activity'] +
        annual_report['Net cash flow by investing activity'] +
        annual_report['Net cash flow by financial activity']
    )
    
    # Internal consistency check for Net Cash Flow
    financial_data_consistency_check = financial_data[
        financial_data['Net Cash Flow'] != financial_data['Net cash flow by financial activity']
    ]
    
    # Aggregate annual data
    annual_data = financial_data.groupby('Year').agg({
        'Headcount': 'mean',
        'Attrition rate': 'mean',
        'Net Cash Flow': 'sum'
    }).reset_index()
    
    # Classification function based on percentage change
    def classify_trend(changes):
        if all(change > 0 for change in changes):
            return 'Excellent'
        elif all(change >= -10 for change in changes):  # Define a threshold for "Good"
            return 'Good'
        elif any(change < -20 for change in changes):  # Define a threshold for "Bad"
            return 'Bad'
        else:
            return 'Poor'
    
    # Calculate percentage changes for each metric
    headcount_changes = [
        (annual_data.iloc[i]['Headcount'] - annual_data.iloc[i-1]['Headcount']) / annual_data.iloc[i-1]['Headcount'] * 100
        for i in range(1, len(annual_data))
    ]
    
    attrition_changes = [
        (annual_data.iloc[i]['Attrition rate'] - annual_data.iloc[i-1]['Attrition rate']) / annual_data.iloc[i-1]['Attrition rate'] * 100
        for i in range(1, len(annual_data))
    ]
    
    net_cash_flow_changes = [
        (annual_data.iloc[i]['Net Cash Flow'] - annual_data.iloc[i-1]['Net Cash Flow']) / abs(annual_data.iloc[i-1]['Net Cash Flow']) * 100
        for i in range(1, len(annual_data))
    ]
    
    # Classify each metric
    headcount_classification = classify_trend(headcount_changes)
    attrition_classification = classify_trend(attrition_changes)
    net_cash_flow_classification = classify_trend(net_cash_flow_changes)
    
    # Plot all charts: Average Headcount Per Year, Average Attrition Rate Per Year, Total Net Cash Flow Per Year
    st.subheader('Annual Financial Metrics')
    fig, axes = plt.subplots(3, 1, figsize=(8, 12), constrained_layout=True)
    
    # Plot Annual Headcount
    axes[0].bar(annual_data['Year'], annual_data['Headcount'], color='blue')
    axes[0].set_title('Average Headcount Per Year', fontsize=12)
    axes[0].set_xlabel('Year', fontsize=10)
    axes[0].set_ylabel('Average Headcount', fontsize=10)
    axes[0].tick_params(axis='x', labelsize=8)
    axes[0].tick_params(axis='y', labelsize=8)
    
    # Plot Annual Attrition Rate
    axes[1].bar(annual_data['Year'], annual_data['Attrition rate'], color='orange')
    axes[1].set_title('Average Attrition Rate Per Year', fontsize=12)
    axes[1].set_xlabel('Year', fontsize=10)
    axes[1].set_ylabel('Average Attrition Rate (%)', fontsize=10)
    axes[1].tick_params(axis='x', labelsize=8)
    axes[1].tick_params(axis='y', labelsize=8)
    
    # Plot Annual Net Cash Flow with colors for positive and negative values
    colors = ['green' if value > 0 else 'red' for value in annual_data['Net Cash Flow']]
    axes[2].bar(annual_data['Year'], annual_data['Net Cash Flow'], color=colors)
    axes[2].set_title('Total Net Cash Flow Per Year', fontsize=12)
    axes[2].set_xlabel('Year', fontsize=10)
    axes[2].set_ylabel('Total Net Cash Flow', fontsize=10)
    axes[2].tick_params(axis='x', labelsize=8)
    axes[2].tick_params(axis='y', labelsize=8)
    
    plt.subplots_adjust(hspace=0.6)
    st.pyplot(fig)
    
    # Display classification results
    st.subheader('Trend Classification')
    st.write(f"Headcount Trend Classification: **{headcount_classification}**")
    st.write(f"Attrition Rate Trend Classification: **{attrition_classification}**")
    st.write(f"Net Cash Flow Trend Classification: **{net_cash_flow_classification}**")
    
    # Correlation matrix with insight
    st.subheader('Correlation Matrix')
    correlation_data = financial_data[['Headcount', 'Net cash flow by operating activity', 'Attrition rate']]
    correlation_matrix = correlation_data.corr()
    
    plt.figure(figsize=(7, 5))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, cbar_kws={'shrink': 0.8})
    plt.title('Correlation Matrix', fontsize=12)
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    st.pyplot(plt)
    
    st.write("The correlation matrix shows how strongly different factors are related.")
    st.write("- **Moderate negative correlation** between Headcount and Attrition rate, suggesting that as the number of employees increases, the rate at which employees leave the company tends to decrease.")
    st.write("- **Weak positive correlation** between Headcount and Net cash flow, suggesting a slight tendency for higher employee numbers to be associated with higher cash flow from operations.")
    st.write("- **Very weak negative correlation** between Attrition rate and Net cash flow, suggesting little relationship between employee turnover and operational cash flow.")

else:
    st.write("Please upload both financial and annual report datasets to proceed.")
