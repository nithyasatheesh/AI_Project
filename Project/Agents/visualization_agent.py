import matplotlib.pyplot as plt
import streamlit as st


class VisualizationAgent:

    def visualize_missing_values(self, df):

        missing = df.isnull().sum()

        fig, ax = plt.subplots()

        missing.plot(kind="bar", ax=ax)

        ax.set_title("Missing Values")

        st.pyplot(fig)

    def visualize_outliers(self, df):

        numeric_cols = df.select_dtypes(include="number").columns

        if len(numeric_cols) > 0:

            col = numeric_cols[0]

            fig, ax = plt.subplots()

            ax.boxplot(df[col].dropna())

            ax.set_title(f"Outlier Detection - {col}")

            st.pyplot(fig)