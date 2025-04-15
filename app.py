import streamlit as st
import pickle
import pandas as pd
import matplotlib.pyplot as plt
teams = ['Sunrisers Hyderabad',
         'Mumbai Indians',
         'Royal Challengers Bangalore',
         'Kolkata Knight Riders',
         'Kings XI Punjab',
         'Chennai Super Kings',
         'Rajasthan Royals',
         'Delhi Capitals',
         'Gujarat Titans',
         'Lucknow Super Giants',]

cities = ['Hyderabad', 'Mumbai', 'Indore', 'Kolkata', 'Delhi',
          'Chandigarh', 'Jaipur', 'Chennai', 'Cape Town', 'Port Elizabeth',
          'Durban', 'Centurion', 'East London', 'Johannesburg', 'Kimberley',
          'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala',
          'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi',
          'Sharjah', 'Mohali', 'Bengaluru']
pipe = pickle.load(open('pipe.pkl', 'rb'))
st.title('🏏 IPL Win Predictor')
col1, col2, col3 = st.columns(3)
with col1:
    batting_team = st.selectbox('Select the batting team', sorted(teams))
with col2:
    bowling_team = st.selectbox('Select the bowling team', sorted(teams))
with col3:
    selected_city = st.selectbox('Select host city', sorted(cities))
target = st.number_input('Target')
col4, col5, col6 = st.columns(3)
with col4:
    score = st.number_input('Score')
with col5:
    overs = st.number_input('Overs completed')
with col6:
    wickets_lost = st.number_input('Wickets out')
if st.button('Predict Probability'):
    runs_left = target - score
    balls_left = 120 - (overs * 6)
    wickets = 10 - wickets_lost
    crr = score / overs if overs > 0 else 0
    rrr = (runs_left * 6) / balls_left if balls_left > 0 else 0
    input_df = pd.DataFrame({
        'batting_team': [batting_team],
        'bowling_team': [bowling_team],
        'city': [selected_city],
        'runs_left': [runs_left],
        'balls_left': [balls_left],
        'wicket_left': [wickets],
        'target': [target],
        'CRR': [crr],
        'RRR': [rrr],
        'inning': [2] 
    })
    result = pipe.predict_proba(input_df)
    loss = result[0][0]
    win = result[0][1]
    st.header(f"🏆 {batting_team} Win Probability: {round(win * 100)}%")
    st.header(f"🎯 {bowling_team} Win Probability: {round(loss * 100)}%")
    fig, ax = plt.subplots()
    ax.pie([win, loss], labels=[batting_team, bowling_team], autopct='%1.1f%%', startangle=90, colors=["#4CAF50", "#F44336"])
    ax.axis('equal') 
    st.pyplot(fig)
