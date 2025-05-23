# -*- coding: utf-8 -*-
"""stockapp.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1mCsmTW5O1WMRATO_rZgwc5k1WH_oviw7
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# Page config
st.set_page_config(page_title="TCS Stock Price Predictor", layout="centered")

# App title
st.title("📈 TCS Stock Price Predictor")
st.markdown("""
Upload a **TCS.csv** file with `Date` and `Close` columns. This app will:
- Train a Linear Regression model on the uploaded data
- Show model performance
- Let you predict the **next day's closing price** by entering the previous day's price
""")

# Upload CSV
uploaded_file = st.file_uploader("📤 Upload your TCS stock price CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        # Load and preprocess data
        df = pd.read_csv(uploaded_file)

        if 'Date' not in df.columns or 'Close' not in df.columns:
            st.error("❌ Your file must contain 'Date' and 'Close' columns.")
            st.stop()

        df['Date'] = pd.to_datetime(df['Date'])
        df.sort_values('Date', inplace=True)
        df.ffill(inplace=True)

        # Create features
        df['Prev_Close'] = df['Close'].shift(1)
        df.dropna(inplace=True)

        # Show dataset
        st.subheader("📄 Recent Data Preview")
        st.dataframe(df.tail())

        # Train/test split
        X = df[['Prev_Close']]
        y = df['Close']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train model
        model = LinearRegression()
        model.fit(X_train, y_train)

        # Evaluate model
        y_pred = model.predict(X_test)
        r2 = r2_score(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))

        st.subheader("📊 Model Performance")
        st.write(f"**R² Score:** {r2:.4f}")
        st.write(f"**RMSE:** ₹{rmse:.2f}")

        # Plot Actual vs Predicted
        st.subheader("🔍 Actual vs Predicted Close Price")
        fig, ax = plt.subplots()
        sns.scatterplot(x=y_test, y=y_pred, ax=ax)
        ax.set_xlabel("Actual Close Price")
        ax.set_ylabel("Predicted Close Price")
        ax.set_title("Actual vs Predicted")
        st.pyplot(fig)

        # User input
        st.subheader("🔮 Predict Next Closing Price")
        default_price = float(df['Close'].iloc[-1])
        user_input = st.number_input(
            "Enter Previous Day's Closing Price (₹)",
            min_value=0.0,
            value=default_price,
            step=0.1,
            format="%.2f"
        )

        if st.button("Predict Next Price"):
            next_pred = model.predict(np.array([[user_input]]))[0]
            st.success(f"📌 Predicted Next Close Price: ₹{next_pred:.2f}")

    except Exception as e:
        st.error(f"⚠️ Something went wrong: {e}")

