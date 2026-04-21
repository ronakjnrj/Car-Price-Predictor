from flask import Flask, render_template, request
import pandas as pd
import joblib
from datetime import date

app = Flask(__name__)

# Load model
model = joblib.load('car_price_model.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    Car_Age = date.today().year - int(request.form['Year'])

    input_data = {
        'Car': [request.form['Car']],
        'Model': [request.form['Model'].lower()],
        'Kilometers': [float(request.form['Kilometers'])],
        'Fuel': [int(request.form['Fuel'])],
        'Transmission': [int(request.form['Transmission'])],
        'Car_Age': Car_Age,
    }

    print(input_data)
    
    new_car = pd.DataFrame(input_data)
    
    # Predict
    prediction = model.predict(new_car)
    output = round(prediction[0], 2)

    return render_template('index.html', prediction_text=f'Estimated Price: ₹{output}')

if __name__ == "__main__":
    app.run(debug=True)

