# from crypt import method
from msilib.schema import Feature
from flask import Flask, redirect, render_template, request, url_for
app = Flask(__name__)
import pickle, numpy as np
model = pickle.load(open('first-innings-score-lr-model.pkl', 'rb'))

@app.route('/')
def redirect_home():
    return render_template('index.html')

@app.route('/index')
def home():
    return render_template('index.html')

@app.route('/predict', methods = ['POST'])
def predict():
    temp_array = list()
    if request.method == 'POST' :
        form_values = request.form
        print(form_values)
        print(form_values['venue'])
        venue = ['M Chinnaswamy Stadium',
                    'Punjab Cricket Association Stadium, Mohali', 'Feroz Shah Kotla',
                    'Wankhede Stadium', 'Sawai Mansingh Stadium',
                    'MA Chidambaram Stadium, Chepauk', 'Eden Gardens',
                    'Dr DY Patil Sports Academy', 'Newlands', "St George's Park",
                    'Kingsmead', 'SuperSport Park', 'Buffalo Park',
                    'New Wanderers Stadium', 'De Beers Diamond Oval',
                    'OUTsurance Oval', 'Brabourne Stadium',
                    'Sardar Patel Stadium, Motera',
                    'Himachal Pradesh Cricket Association Stadium',
                    'Subrata Roy Sahara Stadium',
                    'Rajiv Gandhi International Stadium, Uppal',
                    'Shaheed Veer Narayan Singh International Stadium',
                    'JSCA International Stadium Complex', 'Sheikh Zayed Stadium',
                    'Sharjah Cricket Stadium', 'Dubai International Cricket Stadium',
                    'Barabati Stadium', 'Maharashtra Cricket Association Stadium',
                    'Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium',
                    'Punjab Cricket Association IS Bindra Stadium, Mohali',
                    'Holkar Cricket Stadium'
                ]
        venue_val = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        if form_values['venue'] in venue:
            selected_venue_index = venue.index(form_values['venue'])
            venue_val[selected_venue_index] = 1
            temp_array = temp_array + venue_val

        teams = ['Chennai Super Kings','Delhi Daredevils', 'Kings XI Punjab',
                    'Kolkata Knight Riders', 'Mumbai Indians',
                    'Rajasthan Royals', 'Royal Challengers Bangalore','Sunrisers Hyderabad',
                ]
        batting_team_val = [0,0,0,0,0,0,0,0]
        bowling_team_val = [0,0,0,0,0,0,0,0]

        if form_values['batting_team'] in teams:
            selected_batting_team_index = teams.index(form_values['batting_team'])
            batting_team_val[selected_batting_team_index] = 1
            temp_array += batting_team_val

        if form_values['bowling_team'] in teams:
            selected_bowling_team_index = teams.index(form_values['bowling_team'])
            bowling_team_val[selected_bowling_team_index] = 1
            temp_array += bowling_team_val

        print('batting', batting_team_val)
        print('bowling', bowling_team_val)

        overs               = int(form_values['overs'])
        runs                = int(form_values['runs'])
        wickets             = int(form_values['wickets'])
        runs_in_prev_5      = int(form_values['runs_in_prev_5'])
        wickets_in_prev_5   = int(form_values['wickets_in_prev_5'])

        temp_array += [runs, wickets, overs, runs_in_prev_5, wickets_in_prev_5]
        features    = [np.array(temp_array)]
        print(features)
        predicted_score = model.predict(features)
        predicted_score = int(predicted_score)

        return render_template('result.html',lower_limit = predicted_score-10, upper_limit = predicted_score+5)


if __name__ == '__main__':
	app.run(debug=True)