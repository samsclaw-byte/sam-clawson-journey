import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
from datetime import datetime, timedelta

# Page config
st.set_page_config(
    page_title="Sam's Health Dashboard",
    page_icon="🏃‍♀️",
    layout="wide"
)

# Title
st.title("🏃‍♀️ Sam's Health Dashboard")
st.markdown("*WHOOP + Nutrition Analytics*")

# Load data
@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_data():
    """Load WHOOP and habit data"""
    data_dir = os.path.expanduser('~/.openclaw/workspace/dashboard')
    
    # Load WHOOP data
    whoop_path = os.path.join(data_dir, 'whoop_data.csv')
    if os.path.exists(whoop_path):
        whoop_df = pd.read_csv(whoop_path)
        whoop_df['date'] = pd.to_datetime(whoop_df['date'])
    else:
        whoop_df = pd.DataFrame()
    
    # Load habit data
    habit_path = os.path.join(data_dir, 'habit_data.csv')
    if os.path.exists(habit_path):
        habit_df = pd.read_csv(habit_path)
        habit_df['date'] = pd.to_datetime(habit_df['date'])
    else:
        habit_df = pd.DataFrame()
    
    # Merge if both exist
    if not whoop_df.empty and not habit_df.empty:
        merged = pd.merge(whoop_df, habit_df, on='date', how='outer')
    elif not whoop_df.empty:
        merged = whoop_df
    elif not habit_df.empty:
        merged = habit_df
    else:
        merged = pd.DataFrame()
    
    return merged.sort_values('date') if not merged.empty else merged

# Load data
df = load_data()

if df.empty:
    st.warning("⚠️ No data found. Run sync_whoop.py and sync_habits.py first!")
    st.stop()

# Sidebar filters
st.sidebar.header("📊 Filters")

# Date range
date_range = st.sidebar.date_input(
    "Date Range",
    value=[df['date'].min().date(), df['date'].max().date()],
    min_value=df['date'].min().date(),
    max_value=df['date'].max().date()
)

# Filter data
if len(date_range) == 2:
    mask = (df['date'] >= pd.Timestamp(date_range[0])) & (df['date'] <= pd.Timestamp(date_range[1]))
    filtered_df = df[mask]
else:
    filtered_df = df

# Latest stats
st.header("📈 Latest Stats")
col1, col2, col3, col4 = st.columns(4)

latest = filtered_df.iloc[0] if not filtered_df.empty else None

if latest is not None:
    with col1:
        recovery = latest.get('recovery_score', 0)
        color = '🟢' if recovery >= 67 else '🟡' if recovery >= 34 else '🔴'
        st.metric("Recovery", f"{color} {recovery}%")
    
    with col2:
        sleep_perf = latest.get('sleep_performance', 0)
        st.metric("Sleep Performance", f"{sleep_perf}%")
    
    with col3:
        strain = latest.get('strain', 0)
        st.metric("Strain", f"{strain}")
    
    with col4:
        calories = latest.get('calories_burned', 0)
        st.metric("Calories Burned", f"{int(calories):,}")

# Habit Tracking Section
st.header("🎯 Habit Tracking")

# Habit streaks
if 'water_streak' in filtered_df.columns:
    col1, col2, col3, col4 = st.columns(4)
    
    latest_habit = filtered_df.iloc[0] if not filtered_df.empty else None
    
    if latest_habit is not None:
        with col1:
            water_streak = int(latest_habit.get('water_streak', 0))
            st.metric("💧 Water Streak", f"{water_streak} days 🔥")
        
        with col2:
            exercise_streak = int(latest_habit.get('exercise_streak', 0))
            st.metric("🏃 Exercise Streak", f"{exercise_streak} days 🔥")
        
        with col3:
            multi_streak = int(latest_habit.get('multi_streak', 0))
            st.metric("💊 Multi Streak", f"{multi_streak} days 🔥")
        
        with col4:
            fruit_streak = int(latest_habit.get('fruit_streak', 0))
            st.metric("🍎 Fruit Streak", f"{fruit_streak} days 🔥")

# Today's habits
st.subheader("Today's Progress")
col1, col2, col3, col4 = st.columns(4)

if latest is not None:
    with col1:
        water = latest.get('water', 0)
        water_pct = min(100, (water / 8) * 100)
        st.progress(water_pct / 100, text=f"Water: {int(water)}/8 glasses")
    
    with col2:
        exercise = latest.get('exercise', False)
        exercise_min = int(latest.get('exercise_minutes', 0))
        st.progress(1.0 if exercise else 0.0, text=f"Exercise: {'✅' if exercise else '❌'} ({exercise_min} min)")
    
    with col3:
        multi = latest.get('multivitamin', False)
        st.progress(1.0 if multi else 0.0, text=f"Multivitamin: {'✅' if multi else '❌'}")
    
    with col4:
        fruit = latest.get('fruit', False)
        st.progress(1.0 if fruit else 0.0, text=f"Fruit: {'✅' if fruit else '❌'}")

# Habit trends
st.subheader("Habit Trends")
col1, col2 = st.columns(2)

with col1:
    if 'water' in filtered_df.columns:
        fig = px.bar(
            filtered_df,
            x='date',
            y='water',
            title='Daily Water Intake (glasses)',
            labels={'water': 'Glasses', 'date': 'Date'}
        )
        fig.add_hline(y=8, line_dash="dash", line_color="green", annotation_text="Goal")
        st.plotly_chart(fig, use_container_width=True)

with col2:
    if 'exercise_minutes' in filtered_df.columns:
        fig = px.bar(
            filtered_df,
            x='date',
            y='exercise_minutes',
            title='Exercise Duration (minutes)',
            labels={'exercise_minutes': 'Minutes', 'date': 'Date'},
            color='exercise_minutes',
            color_continuous_scale=['red', 'yellow', 'green']
        )
        fig.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Goal")
        st.plotly_chart(fig, use_container_width=True)

# Charts Section
st.header("📊 Trends")

# Recovery trend
col1, col2 = st.columns(2)

with col1:
    st.subheader("Recovery Score Trend")
    if 'recovery_score' in filtered_df.columns:
        fig = px.line(
            filtered_df, 
            x='date', 
            y='recovery_score',
            title='Recovery Score Over Time',
            labels={'recovery_score': 'Recovery %', 'date': 'Date'}
        )
        fig.add_hline(y=67, line_dash="dash", line_color="green", annotation_text="Good")
        fig.add_hline(y=34, line_dash="dash", line_color="red", annotation_text="Poor")
        st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Sleep Performance")
    if 'sleep_performance' in filtered_df.columns:
        fig = px.bar(
            filtered_df,
            x='date',
            y='sleep_performance',
            title='Sleep Performance %',
            color='sleep_performance',
            color_continuous_scale=['red', 'yellow', 'green']
        )
        st.plotly_chart(fig, use_container_width=True)

# Sleep stages breakdown
col1, col2 = st.columns(2)

with col1:
    st.subheader("Sleep Stages (Hours)")
    sleep_cols = ['deep_sleep_hours', 'rem_sleep_hours', 'light_sleep_hours', 'awake_hours']
    available_cols = [c for c in sleep_cols if c in filtered_df.columns]
    
    if available_cols:
        sleep_df = filtered_df[['date'] + available_cols].copy()
        fig = px.area(
            sleep_df,
            x='date',
            y=available_cols,
            title='Sleep Composition',
            labels={'value': 'Hours', 'variable': 'Stage'}
        )
        st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Strain vs Recovery")
    if 'strain' in filtered_df.columns and 'recovery_score' in filtered_df.columns:
        fig = px.scatter(
            filtered_df,
            x='strain',
            y='recovery_score',
            title='Strain vs Recovery',
            labels={'strain': 'Strain', 'recovery_score': 'Recovery %'},
            trendline='ols'
        )
        st.plotly_chart(fig, use_container_width=True)

# HRV and Resting HR
col1, col2 = st.columns(2)

with col1:
    st.subheader("Heart Rate Variability (HRV)")
    if 'hrv' in filtered_df.columns:
        fig = px.line(
            filtered_df,
            x='date',
            y='hrv',
            title='HRV Trend (ms)'
        )
        st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Resting Heart Rate")
    if 'resting_hr' in filtered_df.columns:
        fig = px.line(
            filtered_df,
            x='date',
            y='resting_hr',
            title='RHR Trend (bpm)'
        )
        st.plotly_chart(fig, use_container_width=True)

# Data table
st.header("📋 Raw Data")
with st.expander("View Data Table"):
    st.dataframe(filtered_df.sort_values('date', ascending=False))

# Export button
if st.button("📥 Export to CSV"):
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name=f"health_data_{datetime.now().strftime('%Y-%m-%d')}.csv",
        mime="text/csv"
    )

st.markdown("---")
st.markdown("*Last updated: {}*".format(datetime.now().strftime("%Y-%m-%d %H:%M")))
