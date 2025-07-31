from flask import Flask, request, jsonify
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Load pre-trained model and vectorizer
with open('cyberbullying_model.pkl', 'rb') as file:
    model = pickle.load(file)

with open('vectorizer.pkl', 'rb') as file:
    vectorizer = pickle.load(file)

# Initialize Flask app
app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        if not data or 'comment' not in data:
            return jsonify({"error": "Missing 'comment' in request body"}), 400

        comment = data['comment']
        print("Received comment:", comment)  # Debug

        # Transform input and predict
        transformed_input = vectorizer.transform([comment])
        prediction = model.predict(transformed_input)

        print("Prediction result:", prediction[0])  # Debug

        return jsonify({"is_offensive": bool(prediction[0])})

    except Exception as e:
        # Print full traceback in terminal
        import traceback
        traceback.print_exc()

        return jsonify({"error": f"Server error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
