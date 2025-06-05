import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Diamond Price Explorer", layout="wide")
st.title("Diamond Price Explorer")

uploaded_file = st.file_uploader("Upload diamond price data", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df_clean = df.dropna(subset=["price", "cut", "color", "clarity"])

    st.subheader("Raw Data")
    st.dataframe(df_clean.head())

    selected_cut = st.sidebar.multiselect("Select Cut", options=sorted(df_clean['cut'].dropna().unique()),
                                          default=df_clean['cut'].unique())
    selected_color = st.sidebar.multiselect("Select Color", options=sorted(df_clean['color'].dropna().unique()),
                                            default=df_clean['color'].unique())
    selected_clarity = st.sidebar.multiselect("Select Clarity", options=sorted(df_clean['clarity'].dropna().unique()),
                                              default=df_clean['clarity'].unique())

    filtered_df = df_clean[
        (df_clean["cut"].isin(selected_cut)) &
        (df_clean["color"].isin(selected_color)) &
        (df_clean["clarity"].isin(selected_clarity))
        ]

    st.subheader("Summary Statistics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Average Price", f"${filtered_df['price'].mean():,.2f}")
    col2.metric("Median Price", f"${filtered_df['price'].median():,.2f}")
    col3.metric("Total Diamonds", f"{len(filtered_df):,}")

    st.subheader("Average Price by Quality Grades")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown("Price by Cut")
        fig1, ax1 = plt.subplots()
        filtered_df.boxplot(column="price", by="cut", ax=ax1)
        ax1.set_title("Price by Cut")
        ax1.set_ylabel("Price ($)")
        ax1.set_xlabel("Cut")
        plt.suptitle("")
        st.pyplot(fig1)

    with col2:
        st.markdown("Price Distribution Histogram")
        fig_hist, ax_hist = plt.subplots()
        ax_hist.hist(filtered_df["price"], bins=50, color="skyblue", edgecolor="black")
        ax_hist.set_title("Histogram of Diamond Prices")
        ax_hist.set_xlabel("Price ($)")
        ax_hist.set_ylabel("Count")
        st.pyplot(fig_hist)

    with col3:
        st.markdown("Average Price by Color Grade")
        avg_price_by_color = filtered_df.groupby("color")["price"].mean().sort_index()
        fig_line, ax_line = plt.subplots()
        ax_line.plot(avg_price_by_color.index, avg_price_by_color.values, marker='o', linestyle='-')
        ax_line.set_title("Average Diamond Price by Color Grade")
        ax_line.set_xlabel("Color Grade")
        ax_line.set_ylabel("Average Price ($)")
        ax_line.grid(True)
        st.pyplot(fig_line)

    st.success("Use filters to explore how quality factors impact pricing. Great for pricing strategy or customer education!")
