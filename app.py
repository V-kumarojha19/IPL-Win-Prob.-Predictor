import streamlit as st
import pickle
import pandas as pd

teams = ['Kolkata Knight Riders',
 'Chennai Super Kings',
 'Rajasthan Royals',
 'Royal Challengers Bangalore',
 'Sunrisers Hyderabad',
 'Punjab Kings',
 'Delhi Capitals',
 'Mumbai Indians',
 'Gujarat Titans',
 'Lucknow Super Giants']

cities = ['Bangalore', 'Chandigarh', 'Delhi', 'Mumbai', 'Kolkata', 'Jaipur',
       'Hyderabad', 'Chennai', 'Cape Town', 'Port Elizabeth', 'Durban',
       'Centurion', 'East London', 'Johannesburg', 'Kimberley',
       'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala',
       'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi',
       'Bengaluru', 'Indore', 'Dubai', 'Sharjah', 'Navi Mumbai',
       'Lucknow', 'Guwahati', 'Mohali']

pipe = pickle.load(open('pipe.pkl', 'rb'))

st.title('IPL Win Predictor')

col1,col2 = st.columns(2)

# with col1:
#     batting_team = st.selectbox('Select the Batting Team', sorted(teams))
# with col2:
#     bowling_team = st.selectbox('Select the Bowling Team', sorted(teams))

with col1:
    batting_team = st.selectbox('Select the Batting Team', sorted(teams))
with col2:
    possible_bowling_teams = [team for team in teams if team != batting_team]
    if possible_bowling_teams:
        bowling_team = st.selectbox('Select the Bowling Team', sorted(possible_bowling_teams))
    else:
        st.error("Batting and Bowling teams cannot be same.")

selected_city = st.selectbox('Select Host City', sorted(cities))

target = st.number_input('Target')

col3, col4, col5 = st.columns(3)
with col3:
    score = st.number_input('Score', min_value=0)
with col4:
    overs = st.number_input('Overs Completed', min_value=0, max_value=20)
    if overs > 20:
        st.error('Overs can not be more than 20!')
with col5:
    wickets = st.number_input('Wickets Out', min_value=0, max_value=10)
    if wickets > 10:
        st.error('Wickets cannot be more than 10!')

if st.button('Predict Probability'):
    runs_left = target - score
    balls_left = 120 - overs * 6
    wickets = 10 - wickets
    crr = score / overs
    rrr = (runs_left) * 6 / balls_left

    input_df = pd.DataFrame({'batting_team': [batting_team], 'bowling_team': [bowling_team],
                             'city': [selected_city], 'runs_left': [runs_left], 'balls_left': [balls_left],
                             'wickets': [wickets], 'total_runs_x': [target], 'crr': [crr], 'rrr': [rrr]})

    result = pipe.predict_proba(input_df)
    loss = result[0][0]
    win = result[0][1]
    st.header(batting_team + ': ' + str(round(win * 100)) + '%')
    st.header(bowling_team + ': ' + str(round(loss * 100)) + '%')