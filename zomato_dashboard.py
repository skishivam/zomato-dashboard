import streamlit as st
import pandas as pd
import plotly.express as px

# Set page settings
st.set_page_config(page_title="Zomato Dashboard", layout="wide")

# Load cleaned Zomato data
df = pd.read_csv("cleaned_zomato.csv")

# Clean column names (safe)
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
df.fillna("Unknown", inplace=True)

# Show available columns for debugging
# st.write("Available Columns:", df.columns.tolist())

# Streamlit app title
st.title("🍽️ Zomato Restaurant Data Dashboard")

# Sidebar city filter
city_list = df['city'].dropna().unique()
selected_city = st.sidebar.selectbox("📍 Select a City", sorted(city_list))

# Filter data by selected city
filtered_df = df[df['city'] == selected_city]

# Show total restaurants
st.metric(label="🍴 Total Restaurants", value=filtered_df.shape[0])

# --- Top Cuisines Pie Chart ---
st.subheader("Top 5 Cuisines in " + selected_city)
top_cuisines = filtered_df['cuisines'].value_counts().head(5)
fig1 = px.pie(names=top_cuisines.index, values=top_cuisines.values, title="Cuisine Distribution")
st.plotly_chart(fig1, use_container_width=True)

# --- Ratings Distribution ---
st.subheader("⭐ Rating Distribution")
fig2 = px.histogram(filtered_df, x="aggregate_rating", nbins=20, title="Rating Histogram")
st.plotly_chart(fig2, use_container_width=True)

# --- Cost for Two Box Plot ---
st.subheader("💰 Cost for Two Distribution")
fig3 = px.box(filtered_df, y="average_cost_for_two", title="Cost Distribution")
st.plotly_chart(fig3, use_container_width=True)

# --- Delivery Availability Pie ---
st.subheader("📦 Delivery Availability")
# Map 1 → Yes, 0 → No (if needed)
if filtered_df['delivery'].dtype in ['int64', 'float64']:
    filtered_df['delivery_status'] = filtered_df['delivery'].map({1: 'Yes', 0: 'No'})
else:
    filtered_df['delivery_status'] = filtered_df['delivery']

delivery_count = filtered_df['delivery_status'].value_counts()
fig4 = px.pie(filtered_df, names="delivery", title="Delivery Availability (1 = Yes, 0 = No)")

st.plotly_chart(fig4, use_container_width=True)
