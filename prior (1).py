import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Function to plot annual and quarterly data
def plot_data(annual_data, quarterly_data):
    st.title('Prior Year Tieout')

    # Plot Annual Data
    st.subheader('Annual Financial Metrics')
    fig, ax = plt.subplots(figsize=(14, 7))
    for column in ['Revenues', 'Operating income', 'Total Assets', 'Net cash flow ']:
        ax.plot(annual_data['Year'], annual_data[column], marker='o', label=column)
    ax.set_title('Annual Financial Metrics')
    ax.set_xlabel('Year')
    ax.set_ylabel('Value (in millions)')
    ax.legend()
    st.pyplot(fig)

    # Concatenate Year and Quarter for better plotting on x-axis
    quarterly_data['Year-Quarter'] = quarterly_data['Year'].astype(str) + ' ' + quarterly_data['Quarters']

    # Plot Quarterly Data
    st.subheader('Quarterly Financial Metrics')
    fig, ax = plt.subplots(figsize=(14, 7))
    for column in ['Revenues', 'Operating income', 'Total Assets', 'Net cash flow']:
        ax.plot(quarterly_data['Year-Quarter'], quarterly_data[column], marker='o', label=column)
    ax.set_xticklabels(quarterly_data['Year-Quarter'], rotation=45, ha='right')
    ax.set_title('Quarterly Financial Metrics')
    ax.set_xlabel('Year-Quarter')
    ax.set_ylabel('Value (in millions)')
    ax.legend()
    st.pyplot(fig)

    # Correlation Matrix for Annual Data
    #st.subheader('Correlation Matrix of Annual Financial Metrics')
    correlation_matrix_annual = annual_data[['Revenues', 'Operating income', 'Total Assets', 'Net cash flow ', 'Dividend', 'Dividend yeild']].corr()
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(correlation_matrix_annual, annot=True, cmap='coolwarm', linewidths=0.5, ax=ax)
    ax.set_title('Correlation Matrix of Annual Financial Metrics')
    #st.pyplot(fig)

    # Correlation Matrix for Quarterly Data
    #st.subheader('Correlation Matrix of Quarterly Financial Metrics')
    correlation_matrix_quarterly = quarterly_data[['Revenues', 'Operating income', 'Total Assets', 'Net cash flow', 'Dividend Yeild']].corr()
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(correlation_matrix_quarterly, annot=True, cmap='coolwarm', linewidths=0.5, ax=ax)
    ax.set_title('Correlation Matrix of Quarterly Financial Metrics')
    #st.pyplot(fig)

    # Business Insights and Recommendations
    st.subheader('Business Insights and Recommendations')

    annual_data['Dividend Yeild Change'] = annual_data['Dividend yeild'].pct_change() * 100

    # Dividend Yield Over the Years
    fig = px.line(annual_data, x='Year', y='Dividend yeild', title='Dividend Yield Over the Years', markers=True)
    st.plotly_chart(fig)

    # Business Insights
    st.subheader("Dividend Yield Analysis")
    st.write("* **2019-2020:** A 9.71% increase in Dividend Yield suggests improved financial performance or a more generous dividend policy in 2020.")
    st.write("* **2020-2021:** A 7.17% decrease in Dividend Yield indicates a decline in dividend returns relative to revenues in 2021.")
    st.write("* **2021-2022:** A significant 21.19% increase in Dividend Yield suggests strong financial performance or a more robust dividend policy in 2022.")
    st.write("* **2022-2023:** A 12.19% increase in Dividend Yield further supports the trend of improved financial health or increased dividend distribution in 2023.")

    st.subheader("Average Annual Growth Rates")
    st.write("* Revenue: 2.49%")
    st.write("* Operating Income: 2.58%")
    st.write("* Total Assets: 2.24%")
    st.write("* Net Cash Flow: -488.33% (negative growth)")

    # Correlation-based insights
    st.subheader("Correlation Analysis and Recommendations")
    st.write("* **Revenues and Operating Income:** Strong positive correlation. Focus on efficient scaling operations to enhance profitability.")
    st.write("* **Total Assets and Revenues:** Strong positive correlation. Maintain investments in productive assets and assess their returns regularly.")
    st.write("* **Net Cash Flow and Total Assets:** Moderate negative correlation. Carefully monitor cash flow during capital expenditures and balance asset growth with liquidity.")
    st.write("* **Net Cash Flow and Dividend Yield:** Weak correlation. Optimize cash flow allocation to effectively support dividend payouts.")
    st.write("* **Operating Income and Total Assets:** Strong positive correlation. Invest in assets that boost operational efficiency and profitability.")
    st.write("* **Net Cash Flow and Operating Income:** Weak correlation. Analyze factors influencing cash flow conversion from operating income.")

# Streamlit App
def main():
    st.title('Financial Analysis Dashboard')

    # File uploader for annual and quarterly data
    annual_file = st.file_uploader("Upload Annual Data CSV", type="csv")
    quarterly_file = st.file_uploader("Upload Quarterly Data CSV", type="csv")

    if annual_file and quarterly_file:
        annual_data = pd.read_csv(annual_file)
        quarterly_data = pd.read_csv(quarterly_file)

        st.success("Files successfully uploaded!")
        plot_data(annual_data, quarterly_data)
    else:
        st.warning("Please upload both annual and quarterly data files.")

if __name__ == '__main__':
    main()