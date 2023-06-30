from flask import Flask, render_template, request, redirect
import numpy as np
import pickle
import pandas as pd

app = Flask(__name__)

model = pickle.load(open('model.pkl', 'rb'))

@app.route("/",  methods=['GET', 'POST'])
def home():
 
    return render_template("index.html")  

@app.route('/predict', methods=['GET', 'POST'])
def predict():

	if request.method == 'POST':

		room_type = request.form.get("room_type")
		person_capacity = float(request.form.get("person_capacity"))

		if request.form.get("host_is_superhost") == 'Yes':
			host_is_superhost = 1
		else:
			host_is_superhost = 0

		if request.form.get("listings") == '1':
			multi = 0
			biz = 0
		elif request.form.get("listings") == '2-4':
			multi = 1
			biz = 0
		else:
			multi = 0
			biz = 1

		cleanliness_rating = float(request.form.get("cleanliness_rating"))
		guest_satisfaction_overall =  float(request.form.get('guest_satisfaction_overall'))
		bedrooms = int(request.form.get('bedrooms'))
		dist = float(request.form['dist'])/10
		metro_dist = float(request.form['metro_dist'])/50
		attr_index = float(request.form['attr_index'])
		city = request.form['city']

		input_data = pd.DataFrame({'room_type' : [room_type], 'person_capacity' : [person_capacity], 'host_is_superhost' : [host_is_superhost],
					'multi' : [multi], 'biz': [biz], 'cleanliness_rating' : [cleanliness_rating], 
					'guest_satisfaction_overall' : [guest_satisfaction_overall], 'bedrooms' : [bedrooms], 'dist' : [dist], 
					'metro_dist' : [metro_dist], 'attr_index' : [attr_index], 'city' : [city]})
		
		prediction = model.predict(input_data)
		return render_template('index.html', prediction_text='Predicted price of listing is {}'.format(int(prediction[0])))

if __name__ == "__main__":
    app.run(debug=False) 