# app.py
from flask import Flask, render_template, request
#from prediction import run_multitasking_prediction  # Assuming your script is named prediction.py

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get SMILES input from the form
        smiles_input = request.form['smiles_input']

        # Get multitasking predictions using the prediction script
        #result = run_multitasking_prediction(smiles_input)

        # Render the result template with the prediction results
        return render_template('result.html', result=result)
    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
