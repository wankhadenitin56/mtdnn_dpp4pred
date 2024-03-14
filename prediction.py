import os
import subprocess
import pandas as pd
from sklearn.preprocessing import StandardScaler
from keras.models import load_model

# Set your default path here
default_path = r"D:\Project Work\PREDICTION SCRIPT"
path = default_path

# Load training data
dpp4_data = pd.read_csv(os.path.join(path, "X_train.csv"))
print("Number of features in training data:", dpp4_data.shape[1])

# Create function to get predictions using trained model
def dpp4_multitasking(input_dpp4: pd.DataFrame, scaler: StandardScaler, loaded_model) -> tuple:
    # Transform user data to numpy to avoid conflict with names
    dpp4_user_input = scaler.transform(input_dpp4.to_numpy())
    
    # Get predictions for user input
    predictions = loaded_model.predict(dpp4_user_input)

    # Classification prediction
    class_prediction = predictions[0]

    # Regression prediction (change this based on your model's output structure)
    regression_prediction = predictions[1][:, 0] 
    
    return class_prediction, regression_prediction

# Create main function to run descriptor calculation and predictions 
def run_multitasking_prediction(folder: str) -> None:
    # Update the paths for PaDEL-Descriptor and descriptors.xml
    padel_cmd = [
        'java', '-jdpp4', 
        os.path.join(path, 'PaDEL-Descriptor/PaDEL-Descriptor.jdpp4'),
        '-descriptortypes', 
        os.path.join(path, 'PaDEL-Descriptor/descriptors.xml'), 
        '-dir', folder, '-file', folder + '/PaDEL_features.csv', 
        '-2d', '-fingerprints', '-removesalt', '-detectdpp4omaticity', 
        '-standdpp4dizenitro'
    ]

    # Calculate features
    subprocess.call(padel_cmd)
    print("Features calculated")
    
    # Create DataFrame for calculated features
    input_dpp4 = pd.read_csv(folder + "/PaDEL_features.csv")
    print("Number of features in input data:", input_dpp4.shape[1])
    
    # Keep only the features present in the training data
    input_dpp4 = input_dpp4[dpp4_data.columns]

    # Load multitasking model
    loaded_model = load_model(os.path.join(path, "multitasking_model.h5")) 
    print("Model loaded")
    
    # Scale training data
    scaler = StandardScaler()  
    dpp4_data_scaled = scaler.fit_transform(dpp4_data)  
    
    # Run multitasking predictions
    class_pred, regression_pred = dpp4_multitasking(input_dpp4, scaler, loaded_model)    
    print("Classification result: ", class_pred)
    print("Regression result: ", regression_pred)

    # Create DataFrame with results
    res = pd.DataFrame(index=input_dpp4.index)

    # Apply threshold for classification
    threshold = 0.8
    res['Predicted_class'] = (class_pred > threshold).astype(int)
    
    # Interpret class predictions as inhibitor (0) and non-inhibitor (1)
    res['Predicted_class'] = res['Predicted_class'].map({0: 'Inhibitor', 1: 'Non-Inhibitor'})

    res['Regression_output'] = regression_pred

    # Print the results
    print("Predicted Class:", res['Predicted_class'].values)
    print("Regression Output:", res['Regression_output'].values)

    # Save results to csv
    res.to_csv(r"D:\Project Work\PREDICTION SCRIPT\DPP-4-multitasking_predictions.csv", index=False)

    
    return None

# Specify the full path for the file
file_path = r"D:\Project Work\PREDICTION SCRIPT\user_input_smile.smi"

# Prompt user for input
user_input = input("Enter SMILES for compounds: ")

if user_input:
    try:
        # Create a tempordpp4y file and write user input to it
        with open(file_path, "w") as f:
            f.write(user_input)
        print(f"File created at {file_path}")

        # Get multitasking predictions
        run_multitasking_prediction(os.getcwd())  
    except Exception as e:
        print(f"Error: {e}")
else:
    print("No input provided. Exiting.")
