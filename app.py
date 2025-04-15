import streamlit as st
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
st.markdown("""
<style>
    /* Main Theme */
    .stApp {
        background: linear-gradient(135deg, #0e1538 0%, #152052 100%);
        color: white;
    }
    
    /* Title Styling with Animation */
    h1 {
        background: linear-gradient(to right, #ff9933, #ffffff, #138808);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem !important;
        text-align: center;
        margin-bottom: 2rem !important;
        text-shadow: 0 0 10px rgba(255,255,255,0.3);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.03); }
        100% { transform: scale(1); }
    }
    
    /* Header Styling - Updated for better visual appeal */
    h2 {
        color: #ffcc00;
        text-align: center;
        padding: 12px;
        border-radius: 10px;
        margin: 20px 0;
        background: linear-gradient(90deg, rgba(14,21,56,0.8) 0%, rgba(21,32,82,0.8) 100%);
        text-shadow: 0 2px 4px rgba(0,0,0,0.5);
        letter-spacing: 1px;
        border-left: 4px solid #ff9933;
        border-right: 4px solid #138808;
    }
    
    h3 {
        color: #00ccff;
        text-align: center;
        padding: 10px;
        border-radius: 10px;
        margin: 20px 0;
        background: rgba(0,0,0,0.3);
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    
    /* Select Box Styling */
    .stSelectbox div {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        color: white !important;
    }
    
    .stSelectbox label {
        color: #ff9933 !important;
        font-weight: bold;
        font-size: 1.1rem;
    }
    
    /* Number Input Styling */
    .stNumberInput div {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 8px;
    }
    
    .stNumberInput label {
        color: #ff9933 !important;
        font-weight: bold;
        font-size: 1.1rem;
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(45deg, #ff9933, #138808);
        color: white;
        border: none;
        padding: 12px 20px;
        font-size: 1.2rem;
        border-radius: 8px;
        font-weight: bold;
        width: 100%;
        transition: all 0.3s;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 15px rgba(0,0,0,0.4);
    }
    
    /* Result styling */
    div[data-testid="stHeader"] {
        background-color: transparent;
    }
    
    /* Winner Styling */
    .win-probability {
        background: linear-gradient(45deg, #4CAF50, #2E7D32);
        padding: 15px;
        border-radius: 10px;
        margin: 15px 0;
        box-shadow: 0 5px 15px rgba(46, 125, 50, 0.3);
    }
    
    /* Loser Styling */
    .lose-probability {
        background: linear-gradient(45deg, #F44336, #B71C1C);
        padding: 15px;
        border-radius: 10px;
        margin: 15px 0;
        box-shadow: 0 5px 15px rgba(183, 28, 28, 0.3);
    }
    
    /* Chart Container */
    .chart-container {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        margin: 30px 0;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
    }
    
    /* Team Indicators */
    .team-indicator {
        display: inline-block;
        padding: 5px 10px;
        border-radius: 20px;
        font-weight: bold;
        margin: 0 5px;
    }
    
    .team-indicator.batting {
        background-color: #4CAF50;
        color: white;
    }
    
    .team-indicator.bowling {
        background-color: #F44336;
        color: white;
    }
    
    /* Cricket-themed divider */
    .cricket-divider {
        text-align: center;
        margin: 20px 0;
        font-size: 24px;
        color: #ff9933;
    }
    
    /* Pulsating effect for predictions */
    @keyframes highlight {
        0% { box-shadow: 0 0 10px rgba(255, 255, 255, 0.5); }
        50% { box-shadow: 0 0 20px rgba(255, 255, 255, 0.8); }
        100% { box-shadow: 0 0 10px rgba(255, 255, 255, 0.5); }
    }
    
    .highlight {
        animation: highlight 2s infinite;
    }
</style>
""", unsafe_allow_html=True)

teams = [
    'Sunrisers Hyderabad',
    'Mumbai Indians',
    'Royal Challengers Bangalore',
    'Kolkata Knight Riders',
    'Kings XI Punjab',
    'Chennai Super Kings',
    'Rajasthan Royals',
    'Delhi Capitals',
    'Gujarat Titans',
    'Lucknow Super Giants',
]

cities = [
    'Hyderabad', 'Mumbai', 'Indore', 'Kolkata', 'Delhi',
    'Chandigarh', 'Jaipur', 'Chennai', 'Cape Town', 'Port Elizabeth',
    'Durban', 'Centurion', 'East London', 'Johannesburg', 'Kimberley',
    'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala',
    'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi',
    'Sharjah', 'Mohali', 'Bengaluru'
]

# Load the model
try:
    pipe = pickle.load(open('pipe.pkl', 'rb'))
except:
    st.error("Model file 'pipe.pkl' not found. This is a template that requires the trained model file to work.")
    pipe = None

# App title with cricket emoji
st.title('🏏 IPL Win Predictor')

# Add cricket-themed divider
st.markdown('<div class="cricket-divider">🏏 ~ 🏆 ~ 🏏</div>', unsafe_allow_html=True)

# Team selection section
st.markdown("<h3 style='text-align: center; color: #00ccff;'>Team Selection</h3>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    batting_team = st.selectbox('Select the batting team', sorted(teams))
with col2:
    bowling_team = st.selectbox('Select the bowling team', sorted(teams))
with col3:
    selected_city = st.selectbox('Select host city', sorted(cities))

# Match details section
st.markdown("<h3 style='text-align: center; color: #00ccff;'>Match Details</h3>", unsafe_allow_html=True)
target = st.number_input('Target', min_value=0, value=0)

col4, col5, col6 = st.columns(3)
with col4:
    score = st.number_input('Current Score', min_value=0, value=0)
with col5:
    overs = st.number_input('Overs completed', min_value=0.0, max_value=20.0, value=0.0, step=0.1)
with col6:
    wickets_lost = st.number_input('Wickets out', min_value=0, max_value=10, value=0)

# Create a visually appealing button
st.markdown('<div style="text-align: center; margin: 30px 0;">', unsafe_allow_html=True)
predict_button = st.button('📊 Predict Win Probability 📊')
st.markdown('</div>', unsafe_allow_html=True)

if predict_button and pipe is not None:
    if batting_team == bowling_team:
        st.error("Batting and bowling teams cannot be the same!")
    elif target <= 0:
        st.error("Please enter a valid target score greater than 0")
    else:
        with st.spinner('Calculating win probabilities...'):
            # Calculate required metrics
            runs_left = target - score
            balls_left = 120 - (overs * 6)
            wickets = 10 - wickets_lost
            crr = score / overs if overs > 0 else 0
            rrr = (runs_left * 6) / balls_left if balls_left > 0 else float('inf')
            
            # Create input dataframe
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
            
            # Predict probability
            result = pipe.predict_proba(input_df)
            loss = result[0][0]
            win = result[0][1]
            
            # Match summary
            st.markdown(f"""
            <div style="background: rgba(0,0,0,0.4); padding: 20px; border-radius: 10px; margin: 20px 0;">
                <h3 style="text-align: center; color: #00ccff;">Match Summary</h3>
                <table style="width: 100%; color: white;">
                    <tr>
                        <td><strong>Target:</strong></td>
                        <td>{target}</td>
                        <td><strong>Current Score:</strong></td>
                        <td>{score}/{wickets_lost}</td>
                    </tr>
                    <tr>
                        <td><strong>Overs:</strong></td>
                        <td>{overs}/20.0</td>
                        <td><strong>Required Run Rate:</strong></td>
                        <td>{round(rrr, 2)}</td>
                    </tr>
                    <tr>
                        <td><strong>Runs Needed:</strong></td>
                        <td>{runs_left}</td>
                        <td><strong>Balls Left:</strong></td>
                        <td>{int(balls_left)}</td>
                    </tr>
                </table>
            </div>
            """, unsafe_allow_html=True)
            
            # Display results with styling
            st.markdown(f"""
            <div class="win-probability highlight">
                <h2>🏆 {batting_team} Win Probability: {round(win * 100)}%</h2>
            </div>
            <div class="lose-probability">
                <h2>🎯 {bowling_team} Win Probability: {round(loss * 100)}%</h2>
            </div>
            """, unsafe_allow_html=True)
            
            # Create a normal pie chart
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Data for the pie chart
            sizes = [win, loss]
            labels = [f"{batting_team}\n{round(win * 100)}%", f"{bowling_team}\n{round(loss * 100)}%"]
            colors = ['#4CAF50', '#F44336']
            explode = (0.1, 0)  # explode the first slice for emphasis
            
            # Create the pie chart
            wedges, texts, autotexts = ax.pie(
                sizes, 
                labels=labels,
                colors=colors,
                autopct='',
                startangle=90,
                explode=explode,
                shadow=True,
                wedgeprops={'edgecolor': 'white', 'linewidth': 2}
            )
            
            # Style the labels
            plt.setp(texts, fontsize=14, fontweight='bold')
            
            # Add a title
            ax.set_title("Win Probability Analysis", fontsize=18, color='#ffcc00', pad=20)
            
            # Equal aspect ratio ensures that pie is drawn as a circle
            ax.axis('equal')
            
            # Set facecolor to transparent
            fig.patch.set_facecolor('#0e1538')
            ax.set_facecolor('#0e1538')
            st.pyplot(fig)
            st.markdown("<h3 style='text-align: center; color: #00ccff;'>Match Insights</h3>", unsafe_allow_html=True)
            
            if win > 0.7:
                st.markdown(f"""
                <div style="background: rgba(76, 175, 80, 0.2); padding: 15px; border-radius: 10px; margin: 15px 0;">
                    <p>🔥 <strong>{batting_team}</strong> is in a dominant position with a {round(win * 100)}% chance of winning!</p>
                    <p>They need {runs_left} runs from {int(balls_left)} balls with {wickets} wickets in hand.</p>
                </div>
                """, unsafe_allow_html=True)
            elif loss > 0.7:
                st.markdown(f"""
                <div style="background: rgba(244, 67, 54, 0.2); padding: 15px; border-radius: 10px; margin: 15px 0;">
                    <p>🛡️ <strong>{bowling_team}</strong> is in control with a {round(loss * 100)}% chance of defending their total!</p>
                    <p>The batting team needs {runs_left} runs from {int(balls_left)} balls with only {wickets} wickets left.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background: rgba(255, 153, 51, 0.2); padding: 15px; border-radius: 10px; margin: 15px 0;">
                    <p>⚡ This is a nail-biting contest! The match is evenly poised with both teams having a solid chance.</p>
                    <p>The required run rate is {round(rrr, 2)}, and the batting team has {wickets} wickets remaining.</p>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("""
            <div style="text-align: center; margin-top: 50px; padding: 20px; background-color: rgba(0,0,0,0.2); border-radius: 10px;">
                <p style="color: #bbbbbb; font-size: 0.8rem;">
                    This predictor uses machine learning to estimate win probabilities based on historical IPL data.
                    Actual match outcomes may vary due to factors not captured in the model.
                </p>
                <p style="color: #ff9933; font-size: 0.9rem;">
                    🏏 Enjoy the game of cricket! 🏏
                </p>
            </div>
            """, unsafe_allow_html=True)