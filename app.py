import streamlit as st
import pandas as pd

# Path to your local Excel file
file_path = 'tablice_streamlit.xlsx'

# Read the Excel file
df = pd.read_excel(file_path, engine='openpyxl')

# Ensure 'Date' column is in datetime format
df['Datum'] = pd.to_datetime(df['Datum'], errors='coerce').dt.date  # Convert to date format only

# Sidebar filters
st.sidebar.header("Filteri")

# Date filter
date_filter = st.sidebar.date_input("Odaberi datum", [])

# Season filter (assuming tags are categorical)
season_filter = st.sidebar.multiselect("Odaberi prvenstvo", df['Prvenstvo'].unique())

# Round filter
round_filter = st.sidebar.multiselect("Odaberi kolo", df['Kolo'].unique())

# Team filter (assuming 'Team' is a column in the data)
team_filter = st.sidebar.multiselect("Odaberi ekipe", df['Utakmica'].unique())

# Goals For filter (assuming goals for is numeric)
goals_for_filter = st.sidebar.slider("Golovi domaćina", 
                                     int(df['GF'].min()), int(df['GF'].max()), 
                                     (int(df['GF'].min()), int(df['GF'].max())))

# Goals Against filter (assuming goals against is numeric)
goals_against_filter = st.sidebar.slider("Golovi gosta", 
                                         int(df['GA'].min()), int(df['GA'].max()), 
                                         (int(df['GA'].min()), int(df['GA'].max())))

# End Score filter (string)
end_result_filter = st.sidebar.text_input("Odaberi konačni rezultat (W / D / L)")

# Apply filters to the dataframe
filtered_df = df

if date_filter:
    filtered_df = filtered_df[filtered_df['Datum'] == pd.to_datetime(date_filter)]

if season_filter:
    filtered_df = filtered_df[filtered_df['Prvenstvo'].isin(season_filter)]

if round_filter:
    filtered_df = filtered_df[filtered_df['Kolo'].isin(round_filter)]

if team_filter:
    filtered_df = filtered_df[filtered_df['Utakmica'].isin(team_filter)]

# Apply string filter for End Score
if end_result_filter:
    filtered_df = filtered_df[filtered_df['Rezultat'].str.contains(score_filter, na=False)]

# Apply numeric filters
filtered_df = filtered_df[(filtered_df['GF'] >= goals_for_filter[0]) & (filtered_df['GF'] <= goals_for_filter[1])]
filtered_df = filtered_df[(filtered_df['GA'] >= goals_against_filter[0]) & (filtered_df['GA'] <= goals_against_filter[1])]

# Display filtered dataframe
st.dataframe(filtered_df)
