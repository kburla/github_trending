import streamlit as st
import sqlite3
import pandas as pd
import altair as alt
from datetime import datetime, timedelta


st.set_page_config(layout="wide")

# Connect to SQLite
DB_PATH = "src/mydatabase.db"
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

st.title("GitHub Trending Repos Dashboards")

selected_date = st.date_input("Select a date to filter trending projects", datetime.now().date())

col1, col2, col3 = st.columns(3)

# Function to fetch and display data for a given table
def display_trending_data(table, table_pretty_name, days_lookback, col, selected_date):
    cursor.execute(f"PRAGMA table_info({table})")
    columns = cursor.fetchall()
    columns = [col[1] for col in columns]
    
    # get trending columns
    trending_column = next((col for col in columns if col.startswith("trending_")), None)
    
    # Translate selected_date to appropriate week number and month number
    if trending_column == "trending_week":
        selected_value = selected_date.isocalendar()[1]
    elif trending_column == "trending_month":
        selected_value = selected_date.month
    else:
        selected_value = selected_date
    
    # Fetch data for the selected date
    query = f"SELECT DISTINCT name, MAX(stars) as total_stars, MAX(forks) as total_forks, url, {trending_column} FROM {table} WHERE {trending_column} = ? GROUP BY name"
    df = pd.read_sql_query(query, conn, params=[selected_value])
    
    # Properly stylize columns
    df_pretty = df.copy()
    df_pretty.columns = [col.replace('_', ' ').title() for col in df.columns]
    
    # Display Data
    col.subheader(table_pretty_name)
    col.dataframe(df_pretty, hide_index=True)

    # Repo Selection
    repo_list = df["name"].tolist()
    selected_repo = col.selectbox(f"Select a repo to see historical trends", repo_list, key=table)
    
    if selected_repo:
        # Get historical data for selected repo
        query = f"""
        SELECT strftime('%Y-%m-%d %H:00:00', date) as hour, MAX(stars) as stars, MAX(forks) as forks
        FROM {table} 
        WHERE name = '{selected_repo}' 
        AND date >= '{(datetime.now() - timedelta(days=days_lookback)).strftime('%Y-%m-%d %H:%M:%S')}' 
        GROUP BY hour
        ORDER BY hour
        """
        history_df = pd.read_sql_query(query, conn)

        # Prepare data for line charts
        history_df['hour'] = pd.to_datetime(history_df['hour'])
        stars_df = history_df[['hour', 'stars']].copy()
        forks_df = history_df[['hour', 'forks']].copy()

        # Calculate min and max for stars and forks
        stars_min = stars_df['stars'].min()
        stars_max = stars_df['stars'].max()
        forks_min = forks_df['forks'].min()
        forks_max = forks_df['forks'].max()

        # Display stars chart
        col.subheader(f"Stars in the Last {days_lookback} Days for {selected_repo}")
        stars_chart = alt.Chart(stars_df).mark_line().encode(
            x=alt.X('hour:T', title='Hour', axis=alt.Axis(format='%Y-%m-%d %H:%M', tickCount='hour')),
            y=alt.Y('stars:Q', title='Stars', scale=alt.Scale(domain=[stars_min, stars_max])),
            tooltip=['hour:T', 'stars:Q']
        )

        stars_layered_chart = alt.layer(stars_chart).properties(
            width=300,
            height=400
        ).configure_axis(
            labelAngle=-45
        )

        col.altair_chart(stars_layered_chart, use_container_width=True)

        # Display forks chart
        col.subheader(f"Forks in the Last {days_lookback} Days for {selected_repo}")
        forks_chart = alt.Chart(forks_df).mark_line().encode(
            x=alt.X('hour:T', title='Hour', axis=alt.Axis(format='%Y-%m-%d %H:%M', tickCount='hour')),
            y=alt.Y('forks:Q', title='Forks', scale=alt.Scale(domain=[forks_min, forks_max])),
            tooltip=['hour:T', 'forks:Q']
        )


        forks_layered_chart = alt.layer(forks_chart).properties(
            width=300,
            height=400
        ).configure_axis(
            labelAngle=-45
        )

        col.altair_chart(forks_layered_chart, use_container_width=True)

display_trending_data('daily_trending_repos', 'Today', 14, col1, selected_date) 
display_trending_data('weekly_trending_repos', 'This Week', 14, col2, selected_date)
display_trending_data('monthly_trending_repos', 'This Month', 14, col3, selected_date)

conn.close()