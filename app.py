import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Python Data Cleaning Tool",
    page_icon="🧹",
    layout="wide"
)

st.title("🧹 Python Data Cleaning Tool")
st.write("Upload a CSV file to check and clean missing values.")

# Upload CSV file
uploaded_file = st.file_uploader(
    "Upload your CSV dataset",
    type=["csv"]
)

if uploaded_file is not None:

    # Load dataset
    df = pd.read_csv(uploaded_file)

    st.success("Dataset loaded successfully!")

    # Dataset information
    st.header("Dataset Preview")
    st.dataframe(df.head())

    st.write("Dataset Shape:", df.shape)

    # Missing values
    st.header("Missing Values")

    missing_values = df.isnull().sum()

    st.dataframe(
        missing_values[missing_values > 0]
    )

    # Clean data button
    if st.button("Clean Dataset"):

        df_cleaned = df.copy()

        # Fill numerical missing values with median
        numerical_columns = df_cleaned.select_dtypes(
            include="number"
        ).columns

        for column in numerical_columns:
            df_cleaned[column] = df_cleaned[column].fillna(
                df_cleaned[column].median()
            )

        # Fill categorical missing values with mode
        categorical_columns = df_cleaned.select_dtypes(
            exclude="number"
        ).columns

        for column in categorical_columns:
            if df_cleaned[column].isnull().any():
                df_cleaned[column] = df_cleaned[column].fillna(
                    df_cleaned[column].mode()[0]
                )

        st.success("Dataset cleaned successfully!")

        st.header("Cleaned Dataset")
        st.dataframe(df_cleaned.head())

        # Download cleaned file
        csv = df_cleaned.to_csv(index=False)

        st.download_button(
            label="Download Cleaned CSV",
            data=csv,
            file_name="cleaned_data.csv",
            mime="text/csv"
        )