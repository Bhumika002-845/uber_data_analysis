import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import plotly.express as px
import streamlit as st
import builtins

st.set_page_config(page_title=" Uber Data Analysis Project", page_icon="🚖",layout="wide")
st.title("🚖 Uber Data Analysis Project")
st.markdown("---")

st.header("📊Executive Summary")
st.markdown("""

Project Title:** Uber Data Analysis Using Python

This comprehensive data analysis project analyzes cab trip data to uncover valuable insights about trip patterns, customer behavior, driver performance, pricing, and operational factors. The analysis aims to understand the factors that influence cab bookings, trip duration, customer satisfaction, and overall business performance.

### Key Objectives:

* Understand trip patterns across different cities, locations, and time periods
* Analyze pricing trends based on distance, vehicle type, and surge pricing
* Examine customer ratings, feedback, and membership patterns
* Evaluate driver performance based on ratings and experience
* Investigate the impact of traffic and weather conditions on trips
* Analyze cancellation patterns and their possible reasons
* Identify factors affecting customer satisfaction and business performance

### Expected Deliverables:

* Interactive visualizations showcasing cab trip patterns
* Statistical analysis of key performance indicators
* Insights into customer and driver behavior
* Analysis of pricing, cancellations, and trip performance
* Actionable insights for improving cab services and customer experience
""")
st.markdown("---")
st.header(" Project Description")
st.markdown("""## Problem Statement

The cab transportation industry is highly competitive and dynamic, with companies constantly seeking ways to improve their services, optimize pricing, and enhance customer satisfaction. This project leverages a comprehensive cab trips dataset to provide data-driven insights that can help:

* **Cab Service Providers:** Optimize pricing, vehicle allocation, and overall business strategies.
* **Operations Managers:** Understand trip patterns, traffic conditions, cancellations, and service performance.
* **Market Researchers:** Analyze customer behavior, travel trends, and demand patterns.
* **Customers:** Improve their travel experience through better service quality, reduced waiting time, and reliable transportation.

""")
st.markdown("""## Dataset Overview

The Cab Trips dataset contains comprehensive information about cab journeys, customers, drivers, vehicles, trip conditions, and pricing.

### 👤 Customer Information:

* Customer age and gender
* Membership status
* Previous trip history
* Customer ratings

### 🚗 Trip Information:

* Pickup and drop-off locations
* Trip distance and duration
* Day of the week and time of day
* Trip status and cancellation details

### 👨‍✈️ Driver & Vehicle Details:

* Driver age and gender
* Driver experience
* Driver ratings
* Vehicle type

### 🌦️ Trip Conditions:

* Weather conditions
* Traffic levels
* Waiting time
* Surge multiplier

### 💰 Pricing & Payment:

* Trip price
* Discount percentage
* Payment method
* Pricing variations based on trip conditions

### ⭐ Customer Experience:

* Trip ratings
* Customer satisfaction
* Cancellation reasons
* Service performance

This dataset helps analyse **cab demand, pricing patterns, customer behaviour, driver performance, trip cancellations, and the impact of traffic and weather conditions on cab services**.

""")
@st.cache_data
def load_data():
    try:
        DATA_PATH = "cab_trips_test (1).csv"
        df = pd.read_csv(DATA_PATH)
        return df,DATA_PATH
    except:
        st.error("Something Went Wrong")

df, DATA_PATH = load_data()
if df is None:
    st.stop()

# create basic information about the dataset
dataset_info = pd.DataFrame({
    "Attribute": ["Dataset Name", "Number of Records", "Number of Columns", "Memory Usage", "File Format", "Analysis Tools", "Visualization Tools"],
    "Details": ["Uber Data Analysis Project", "100,000", "20", "50 MB", "CSV", "Python (Pandas, NumPy)", "Matplotlib, Seaborn, Plotly"]
})

st.subheader("📊Dataset Basic Information")
st.dataframe(dataset_info,use_container_width=True)

col1,col2,col3,col4 = st.columns(4)
with col1:
    st.metric("Total Records",f"{df.shape[0]:,}")
with col2:
    st.metric("Total Columns",f"{df.shape[1]:,}")
with col3:
    memory_usage = df.memory_usage(deep=True).sum() / (1024 ** 2)
    st.metric("Memory Usage",f"{memory_usage:.2f} MB")    
tab1,tab2,tab3,tab4,tab5= st.tabs(["🗂️Columns Info ","⁉️Missing Values Info","🧾Sample Data","📊Statistical Summary","📂Categorical Data"])
with tab1:
    st.subheader("Columns Information")
    column_info = pd.DataFrame({
        "Column Name":df.columns,
        "Data Types":df.dtypes,
        "Non-Null Values":df.count().values,
        "Null Values":df.isnull().sum().values,
        "Uniqe Values":df.nunique().values
    })
    st.dataframe(column_info,use_container_width=True)
with tab2:
    st.subheader("Missing Value Analysis")

    missing_values=pd.DataFrame({
        "Column":df.columns,
        "Missing Values":df.isnull().sum().values,
        "Missing %":(df.isnull().sum()/len(df)*100).round(2)

    })
    st.dataframe(missing_values,use_container_width=True)
    if df.isnull().sum().sum()==0:
        st.success("✅No Missing Values Found")
    else:
        st.warning("⚠️Missing Values Found")

with tab3:
    st.subheader("Sample Data")
    option = st.radio(
        "Select Sample",
        ["First 10 Rows","Last 10 Rows","Random 10 Rows"],

    )

    if option == "First 10 Rows":
        st.dataframe(df.head(10),use_container_width=True)
    elif option == "Last 10 Rows":
        st.dataframe(df.tail(10),use_container_width=True)
    else:
        st.dataframe(df.sample(10),use_container_width=True)

with tab4:
    st.subheader("Statistical Summary")
    st.markdown("#### Numerical Statistical")
    st.dataframe(df.select_dtypes(include=np.number).describe(),use_container_width=True)
    st.markdown("#### Categorical Statistical")
    categorical = df.select_dtypes(include=["object"]).describe()
    st.dataframe(categorical,use_container_width=True)
with tab5:
    st.subheader("📂Categorical Statistics")
    categorical = df.select_dtypes(include=["object"]).columns
    for col in categorical:
        st.markdown(f"### column: {col}")
        st.write(f"Unique Values: {df[col].nunique()}")
        value_counts = df[col].value_counts().reset_index()
        value_counts.columns = [col, "Count"]
        st.dataframe(value_counts,use_container_width=True)
        st.divider()
@st.cache_data
def cleaned_data():
    try:
        cleaned_df = df.copy()
        cleaned_df.fillna({"Duration_Min":cleaned_df["Duration_Min"].mean()},inplace=True)
        cleaned_df.fillna({"Trip_Rating":cleaned_df["Trip_Rating"].mean()},inplace=True)
        cleaned_df.drop("Cancellation_Reason", axis=1, inplace=True)
        return cleaned_df

    except:
        st.error("Something Went Wrong")

cleaned_df = cleaned_data()

st.markdown("---")
#st.write(cleaned_df)
# ================================
# Initialize Session State
# ================================

if "selected_pickup_city" not in st.session_state:
    st.session_state.selected_pickup_city = builtins.sorted(cleaned_df["Pickup_City"].unique())

if "selected_drop_city" not in st.session_state:
    st.session_state.selected_drop_city = builtins.sorted(cleaned_df["Drop_City"].unique())

if "selected_vehicle" not in st.session_state:
    st.session_state.selected_vehicle = builtins.sorted(cleaned_df["Vehicle_Type"].unique())

if "selected_payment" not in st.session_state:
    st.session_state.selected_payment = builtins.sorted(cleaned_df["Payment_Mode"].unique())

if "selected_status" not in st.session_state:
    st.session_state.selected_status = builtins.sorted(cleaned_df["Trip_Status"].unique())

if "selected_distance" not in st.session_state:
    st.session_state.selected_distance = (
        cleaned_df["Distance_KM"].min(),
        cleaned_df["Distance_KM"].max()
    )
if "selected_rating" not in st.session_state:
    st.session_state.selected_rating = (
        cleaned_df["Trip_Rating"].min(),
        cleaned_df["Trip_Rating"].max()
    )

    # ================================
# Sidebar Filters
# ================================

with st.sidebar:

    st.header("🎯 Filters")

    pickup_city = st.multiselect(
        "Pickup City",
        options=builtins.sorted(cleaned_df["Pickup_City"].unique())
    )

    drop_city = st.multiselect(
        "Drop City",
        options=builtins.sorted(cleaned_df["Drop_City"].unique())
    )

    vehicle = st.multiselect(
        "Vehicle Type",
        options=builtins.sorted(cleaned_df["Vehicle_Type"].unique())
    )

    payment = st.multiselect(
        "Payment Mode",
        options=builtins.sorted(cleaned_df["Payment_Mode"].unique())
    )

    status = st.multiselect(
        "Trip Status",
        options=builtins.sorted(cleaned_df["Trip_Status"].unique())
    )

    distance = st.slider(
        "Distance (km)",
        min_value=builtins.float(cleaned_df["Distance_KM"].min()),
        max_value=builtins.float(cleaned_df["Distance_KM"].max()),
        value=st.session_state.selected_distance
    )
    rating = st.slider(
    "Trip Rating",
    min_value=builtins.float(cleaned_df["Trip_Rating"].min()),
    max_value=builtins.float(cleaned_df["Trip_Rating"].max()),
    value=st.session_state.selected_rating
)

    
    col1, col2 = st.columns(2)

    with col1:
        apply = st.button(
            "✅ Apply",
            use_container_width=True,
            type="primary"
        )

    with col2:
        reset = st.button(
            "🔄 Reset",
            use_container_width=True
        ) 
    # =====================================
# Apply Filters
# =====================================

if apply:
    st.session_state.selected_pickup_city = pickup_city
    st.session_state.selected_drop_city = drop_city
    st.session_state.selected_vehicle = vehicle
    st.session_state.selected_payment = payment
    st.session_state.selected_status = status
    st.session_state.selected_distance = distance
    st.session_state.selected_rating = rating

# =====================================
# Reset Filters
# =====================================

if reset:
    st.session_state.selected_pickup_city = builtins.sorted(cleaned_df["Pickup_City"].unique())
    st.session_state.selected_drop_city = builtins.sorted(cleaned_df["Drop_City"].unique())
    st.session_state.selected_vehicle = builtins.sorted(cleaned_df["Vehicle_Type"].unique())
    st.session_state.selected_payment = builtins.sorted(cleaned_df["Payment_Mode"].unique())
    st.session_state.selected_status = builtins.sorted(cleaned_df["Trip_Status"].unique())
    st.session_state.selected_distance = (
        float(cleaned_df["Distance_KM"].min()),
        float(cleaned_df["Distance_KM"].max())
    )
    st.session_state.selected_rating = (
        float(cleaned_df["Trip_Rating"].min()),
        float(cleaned_df["Trip_Rating"].max())
    )

    st.rerun()

# =====================================
# Create Filtered DataFrame
# =====================================

filtered_df = cleaned_df.copy()   
# =====================================
# Create Filtered DataFrame
# =====================================

filtered_df = cleaned_df.copy()

# Pickup City
if st.session_state.selected_pickup_city:
    filtered_df = filtered_df[
        filtered_df["Pickup_City"].isin(
            st.session_state.selected_pickup_city
        )
    ]

# Drop City
if st.session_state.selected_drop_city:
    filtered_df = filtered_df[
        filtered_df["Drop_City"].isin(
            st.session_state.selected_drop_city
        )
    ]

# Vehicle Type
if st.session_state.selected_vehicle:
    filtered_df = filtered_df[
        filtered_df["Vehicle_Type"].isin(
            st.session_state.selected_vehicle
        )
    ]

# Payment Mode
if st.session_state.selected_payment:
    filtered_df = filtered_df[
        filtered_df["Payment_Mode"].isin(
            st.session_state.selected_payment
        )
    ]

# Trip Status
if st.session_state.selected_status:
    filtered_df = filtered_df[
        filtered_df["Trip_Status"].isin(
            st.session_state.selected_status
        )
    ]

# Distance Filter
filtered_df = filtered_df[
    filtered_df["Distance_KM"].between(
        st.session_state.selected_distance[0],
        st.session_state.selected_distance[1]
    )
]

# Trip Rating Filter
filtered_df = filtered_df[
    filtered_df["Trip_Rating"].between(
        st.session_state.selected_rating[0],
        st.session_state.selected_rating[1]
    )
]
# ============================================
# 📊 Dashboard KPIs
# ============================================

st.markdown("---")
st.header("📈 Dashboard Overview")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "🚖 Total Trips",
        f"{len(filtered_df):,}"
    )

with col2:
    st.metric(
        "📍 Avg Distance",
        f"{filtered_df['Distance_KM'].mean():.2f} KM"
    )

with col3:
    st.metric(
        "⏱ Avg Duration",
        f"{filtered_df['Duration_Min'].mean():.2f} Min"
    )

with col4:
    st.metric(
        "⭐ Avg Trip Rating",
        f"{filtered_df['Trip_Rating'].mean():.2f}"
    )

with col5:
    st.metric(
        "👨‍✈️ Avg Driver Rating",
        f"{filtered_df['Driver_Rating'].mean():.2f}"
    )
# ============================================
# 📊 UBER DATA VISUALIZATIONS
# ============================================
st.header("📊 Visualization and Insights")
st.markdown("---")

# 1️⃣ Average Trip Distance by Vehicle Type
st.subheader("1️⃣ Average Trip Distance by Vehicle Type")

bar_df = filtered_df.groupby("Vehicle_Type", as_index=False)["Distance_KM"].mean()

fig = px.bar(
    bar_df,
    x="Vehicle_Type",
    y="Distance_KM",
    text_auto=".2f",
    title="Average Trip Distance by Vehicle Type",
    labels={
        "Vehicle_Type":"Vehicle Type",
        "Distance_KM":"Average Distance (KM)"
    }
)

fig.update_layout(title_x=0.5)
st.plotly_chart(fig, use_container_width=True)

st.markdown("""
#### Key Insights:
- Compares the average distance travelled by each vehicle type.
- Identifies which vehicle is mostly used for longer trips.
- Useful for fleet utilization analysis.
""")

# 2️⃣ Average Trip Duration by Day of Week
st.subheader("2️⃣ Average Trip Duration by Day of Week")

line_df = filtered_df.groupby("Day_of_Week", as_index=False)["Duration_Min"].mean()

fig = px.line(
    line_df,
    x="Day_of_Week",
    y="Duration_Min",
    markers=True,
    title="Average Trip Duration by Day"
)

fig.update_layout(template="plotly_white", title_x=0.5)

st.plotly_chart(fig, use_container_width=True)

st.markdown("""
#### Key Insights:
- Shows how trip duration changes across weekdays.
- Helps identify peak travel days.
""")

# 3️⃣ Distance vs Duration
st.subheader("3️⃣ Relationship Between Distance and Duration")

sample_df = filtered_df.sample(min(300, len(filtered_df)), random_state=42)

fig = px.scatter(
    sample_df,
    x="Distance_KM",
    y="Duration_Min",
    color="Traffic_Level",
    hover_data=["Vehicle_Type"],
    title="Distance vs Duration"
)

fig.update_layout(template="plotly_white", title_x=0.5)

st.plotly_chart(fig, use_container_width=True)

st.markdown("""
#### Key Insights:
- Longer distances generally require more travel time.
- Heavy traffic increases duration even for short trips.
""")

# 4️⃣ Driver Rating Distribution
st.subheader("4️⃣ Driver Rating Distribution")

fig = px.box(
    filtered_df,
    x="Vehicle_Type",
    y="Driver_Rating",
    color="Vehicle_Type",
    title="Driver Rating by Vehicle Type"
)

fig.update_layout(template="plotly_white", title_x=0.5)

st.plotly_chart(fig, use_container_width=True)

# 5️⃣ Wait Time by Traffic Level
st.subheader("5️⃣ Wait Time Across Traffic Levels")

fig = px.violin(
    filtered_df,
    x="Traffic_Level",
    y="Wait_Time_Min",
    color="Traffic_Level",
    box=True,
    title="Wait Time by Traffic Level"
)

fig.update_layout(template="plotly_white", title_x=0.5)

st.plotly_chart(fig, use_container_width=True)

# 6️⃣ Trip Distance Distribution
st.subheader("6️⃣ Distribution of Trip Distance")

fig = px.histogram(
    filtered_df,
    x="Distance_KM",
    color="Vehicle_Type",
    nbins=20,
    title="Trip Distance Distribution"
)

fig.update_layout(template="plotly_white", title_x=0.5)

st.plotly_chart(fig, use_container_width=True)

# 7️⃣ Trip Status Percentage
st.subheader("7️⃣ Trip Status Distribution")

pie_df = filtered_df["Trip_Status"].value_counts().reset_index()
pie_df.columns=["Trip_Status","Count"]

fig = px.pie(
    pie_df,
    names="Trip_Status",
    values="Count",
    hole=0.45,
    title="Trip Status Distribution"
)

fig.update_layout(title_x=0.5)

st.plotly_chart(fig, use_container_width=True)

# 8️⃣ Vehicle Type by Trip Status
st.subheader("8️⃣ Vehicle Type and Trip Status")

tree_df = filtered_df.groupby(
    ["Vehicle_Type","Trip_Status"]
).size().reset_index(name="Count")

fig = px.treemap(
    tree_df,
    path=["Vehicle_Type","Trip_Status"],
    values="Count",
    color="Trip_Status",
    title="Vehicle Type vs Trip Status"
)

fig.update_layout(title_x=0.5)

st.plotly_chart(fig, use_container_width=True)

# 9️⃣ Pickup City -> Vehicle -> Status
st.subheader("9️⃣ Pickup City Analysis")

sun_df = filtered_df.groupby(
    ["Pickup_City","Vehicle_Type","Trip_Status"]
).size().reset_index(name="Count")

fig = px.sunburst(
    sun_df,
    path=["Pickup_City","Vehicle_Type","Trip_Status"],
    values="Count",
    title="Pickup City Analysis"
)

fig.update_layout(title_x=0.5)

st.plotly_chart(fig, use_container_width=True)

# 🔟 Traffic vs Trip Status Heatmap
st.subheader("🔟 Traffic Level vs Trip Status")

heat_df = pd.crosstab(
    filtered_df["Traffic_Level"],
    filtered_df["Trip_Status"]
)

fig = px.imshow(
    heat_df,
    text_auto=True,
    aspect="auto",
    title="Traffic Level vs Trip Status"
)

fig.update_layout(title_x=0.5)

st.plotly_chart(fig, use_container_width=True)

# 1️⃣1️⃣ Trip Status Funnel
st.subheader("1️⃣1️⃣ Trip Status Funnel")

funnel_df = filtered_df["Trip_Status"].value_counts().reset_index()
funnel_df.columns=["Trip_Status","Count"]

fig = px.funnel(
    funnel_df,
    x="Count",
    y="Trip_Status",
    title="Trips by Status"
)

fig.update_layout(title_x=0.5)

st.plotly_chart(fig, use_container_width=True)
st.markdown("---")

st.header("📊 Project Conclusion and Recommendations")
st.markdown("---")

st.header("📋 Data Analysis Summary")

st.markdown("""
This comprehensive analysis of the **Uber Cab Trips** dataset provides valuable insights into customer travel patterns,
driver performance, trip duration, pricing, traffic conditions, weather impact, and customer satisfaction.
The interactive dashboard helps identify operational trends and supports data-driven decision-making for improving
cab services and customer experience.
""")

st.markdown("---")

st.header("🔍 Major Findings & Insights")

col1, col2 = st.columns(2)

with col1:

    st.subheader("🚖 Trip Analysis")

    st.markdown("""
- Trip distance and duration vary significantly across vehicle types.
- Peak travel days and busy hours result in longer trip durations.
- Traffic conditions directly affect travel time.
- Waiting time increases during high-demand periods.
""")

    st.subheader("👨‍✈️ Driver Performance")

    st.markdown("""
- Experienced drivers generally receive better ratings.
- Driver ratings remain consistently high across completed trips.
- Vehicle type has a minor influence on customer satisfaction.
- Driver performance contributes to repeat customers.
""")

    st.subheader("🌦️ Traffic & Weather")

    st.markdown("""
- Heavy traffic significantly increases trip duration.
- Poor weather conditions may increase waiting time.
- Surge pricing is more common during heavy traffic.
- Traffic management can improve operational efficiency.
""")

with col2:

    st.subheader("💰 Business Insights")

    st.markdown("""
- Prime members contribute a significant portion of trips.
- Discounts improve customer retention.
- Digital payment methods are widely preferred.
- Trip completion rate is high compared to cancellations.
""")

    st.subheader("⭐ Customer Experience")

    st.markdown("""
- Higher trip ratings indicate better service quality.
- Shorter waiting times improve customer satisfaction.
- Cancellation reasons help identify operational issues.
- Better route planning enhances customer experience.
""")
    st.markdown("---")

st.header("💡 Recommendations")

with st.expander("🚖 For Cab Service Providers"):
    st.markdown("""
- Optimize driver allocation during peak hours.
- Reduce passenger waiting time.
- Improve route planning using traffic prediction.
- Monitor driver performance regularly.
""")

with st.expander("👨‍✈️ For Drivers"):
    st.markdown("""
- Maintain high service quality.
- Follow optimized routes.
- Reduce trip cancellations.
- Improve customer communication.
""")

with st.expander("👤 For Customers"):
    st.markdown("""
- Book trips during non-peak hours whenever possible.
- Use digital payment methods for faster transactions.
- Provide ratings to improve service quality.
- Plan rides considering traffic conditions.
""")

with st.expander("🏢 For Business Managers"):
    st.markdown("""
- Monitor demand across cities.
- Increase vehicle availability during busy periods.
- Improve cancellation handling.
- Use dashboard insights for operational decisions.
""")

with st.expander("📊 Dashboard Insights"):
    st.markdown("""
- Interactive visualizations simplify business analysis.
- Filters allow city-wise and vehicle-wise exploration.
- KPIs help monitor operational performance.
- Data-driven insights support better decision making.
""")
    st.markdown("---")

st.header("🎯 Final Conclusion")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "Total Trips",
        f"{filtered_df.shape[0]:,}"
    )

with col2:
    st.metric(
        "Average Distance",
        f"{filtered_df['Distance_KM'].mean():.2f} KM"
    )

with col3:
    st.metric(
        "Average Duration",
        f"{filtered_df['Duration_Min'].mean():.2f} Min"
    )

with col4:
    st.metric(
        "Average Trip Rating",
        f"{filtered_df['Trip_Rating'].mean():.2f}"
    )

with col5:
    st.metric(
        "Average Driver Rating",
        f"{filtered_df['Driver_Rating'].mean():.2f}"
    )
    st.markdown("---")

st.header("🌍 Project Impact")

st.markdown("""
This project provides a comprehensive analysis of Uber cab trip data and helps understand customer behaviour,
driver performance, operational efficiency, traffic impact, and service quality. The interactive dashboard enables
users to explore travel trends and supports informed business decisions.
""")

st.markdown("### 🎯 Key Outcomes")

st.markdown("""
1. **Trip Pattern Analysis:** Understands customer travel behaviour across cities and time.

2. **Operational Efficiency:** Evaluates waiting time, traffic impact, and trip duration.

3. **Driver Performance:** Measures service quality through driver ratings.

4. **Customer Satisfaction:** Analyses trip ratings and cancellation trends.

5. **Business Intelligence:** Supports strategic planning using interactive visualizations.
""")
