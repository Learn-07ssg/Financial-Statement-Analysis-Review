import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge

# Streamlit app
def main():
    st.title("Mathematical Accuracy")

    # Upload the Quarter data file
    st.subheader("Upload Quarter Data")
    quarter_file = st.file_uploader("Choose a CSV file for Quarterly Data", type="csv")

    # Upload the Annual data file
    #st.subheader("Upload Annual Data")
    #annual_file = st.file_uploader("Choose a CSV file for Annual Data", type="csv")

    if quarter_file is not None:
        # Load the data from the uploaded Quarter file
        quarter_data = pd.read_csv(quarter_file)

        # Display the first few rows of the uploaded data
        st.write("Quarterly Data Preview:")
        st.dataframe(quarter_data.head())

        # Process and analyze the quarterly data
        process_quarterly_data(quarter_data)
        
        # Display revenue accuracy comparison
        display_revenue_accuracy(quarter_data)

def process_quarterly_data(quarter_data):
    # Filter relevant columns for quarter data
    quarter_data = quarter_data[['Year', 'Quarters', 'Revenues', 'Net Income', 'Operating margin', 'Predicted revenue']].copy()

    # Handle missing values by filling with mean
    quarter_data['Revenues'].fillna(quarter_data['Revenues'].mean(), inplace=True)
    quarter_data['Net Income'].fillna(quarter_data['Net Income'].mean(), inplace=True)
    quarter_data['Operating margin'].fillna(quarter_data['Operating margin'].mean(), inplace=True)

    # Create a sequential index for quarters
    quarter_data['Quarter_Index'] = (quarter_data['Year'] - 2020) * 4 + quarter_data['Quarters'].apply(lambda x: int(x[-1]))

    # Prepare features and targets for regression using quarterly data
    X = quarter_data[['Year', 'Quarter_Index']].values  # Features: Year and Quarter Index
    y_revenue = quarter_data['Revenues'].values  # Target: Actual Quarterly Revenue
    y_net_income = quarter_data['Net Income'].values  # Target: Actual Quarterly Net Income
    y_operating_margin = quarter_data['Operating margin'].values  # Target: Actual Quarterly Operating Margin

    # Split the data into training and testing sets
    X_train, X_test, y_train_revenue, y_test_revenue = train_test_split(X, y_revenue, test_size=0.3, random_state=42)
    X_train, X_test, y_train_net_income, y_test_net_income = train_test_split(X, y_net_income, test_size=0.3, random_state=42)
    X_train, X_test, y_train_operating_margin, y_test_operating_margin = train_test_split(X, y_operating_margin, test_size=0.3, random_state=42)

    # Initialize Ridge models
    ridge_revenue = Ridge(alpha=1.0)
    ridge_net_income = Ridge(alpha=1.0)
    ridge_operating_margin = Ridge(alpha=1.0)

    # Train the models
    ridge_revenue.fit(X_train, y_train_revenue)
    ridge_net_income.fit(X_train, y_train_net_income)
    ridge_operating_margin.fit(X_train, y_train_operating_margin)

    # Predict using the models for all available quarters
    ridge_revenue_preds = ridge_revenue.predict(X)
    ridge_net_income_preds = ridge_net_income.predict(X)
    ridge_operating_margin_preds = ridge_operating_margin.predict(X)

    # Calculate accuracy of predicted values
    ridge_revenue_accuracy = 100 - np.abs((y_revenue - ridge_revenue_preds) / y_revenue) * 100
    ridge_net_income_accuracy = 100 - np.abs((y_net_income - ridge_net_income_preds) / y_net_income) * 100
    ridge_operating_margin_accuracy = 100 - np.abs((y_operating_margin - ridge_operating_margin_preds) / y_operating_margin) * 100

    # Display accuracy
    st.write("Ridge Revenue Accuracy:", np.mean(ridge_revenue_accuracy))
    st.write("Ridge Net Income Accuracy:", np.mean(ridge_net_income_accuracy))
    st.write("Ridge Operating Margin Accuracy:", np.mean(ridge_operating_margin_accuracy))

    # Predict future quarters (2024 Q1, Q2, Q3, Q4)
    future_quarters = pd.DataFrame({
        'Year': [2024, 2024, 2024, 2024],
        'Quarter_Index': [1, 2, 3, 4]
    })

    # Convert future quarters to numpy array
    future_quarters_array = future_quarters[['Year', 'Quarter_Index']].values

    # Predict revenue, net income, and operating margin for future quarters
    ridge_revenue_future_preds = ridge_revenue.predict(future_quarters_array)
    ridge_net_income_future_preds = ridge_net_income.predict(future_quarters_array)
    ridge_operating_margin_future_preds = ridge_operating_margin.predict(future_quarters_array)

    # Create a dataframe to store the predicted values
    predicted_values = pd.DataFrame({
        'Year': [2024, 2024, 2024, 2024],
        'Quarter': ['Q1', 'Q2', 'Q3', 'Q4'],
        'Predicted Revenue (Ridge)': ridge_revenue_future_preds,
        'Predicted Net Income (Ridge)': ridge_net_income_future_preds,
        'Predicted Operating Margin (Ridge)': ridge_operating_margin_future_preds,
    })

    # Display the predicted values
    st.write("Predicted Values for Future Quarters (2024):")
    st.dataframe(predicted_values)

def display_revenue_accuracy(financial_data):
    # Initialize an empty list to store the results
    results = []

    # Iterate through each row to compare predicted and actual revenue
    for index, row in financial_data.iterrows():
        actual_revenue = row['Revenues']
        predicted_revenue = row['Predicted revenue']

        if predicted_revenue == 0:
            accuracy = 'No guidance was given for this quarter'
        else:
            accuracy = f"{(1 - abs(actual_revenue - predicted_revenue) / actual_revenue) * 100:.2f}%"

        results.append({
            'Year': row['Year'],
            'Quarter': row['Quarters'],
            'Actual Revenue': actual_revenue,
            'Predicted Revenue': predicted_revenue,
            'Accuracy': accuracy
        })

    # Convert results to a DataFrame and display
    results_df = pd.DataFrame(results)
    st.subheader("Revenue Accuracy Comparison")
    st.dataframe(results_df)

if __name__ == "__main__":
    main()
