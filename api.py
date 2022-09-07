import pickle
import sqlite3
import pyrebase
import datetime
from flask import Flask, request, render_template
 
app=Flask(__name__)

conf = {
    "apiKey": "AIzaSyCT1e96tqXnpUBT9T8YJq7N_goWW8LFxIU",
    "authDomain": "fakenewsdetection-a73ba.firebaseapp.com",
    "projectId": "fakenewsdetection-a73ba",
    "storageBucket": "fakenewsdetection-a73ba.appspot.com",
    "messagingSenderId": "989183519823",
    "appId": "1:989183519823:web:676ade3a4389e41a1b0e3a",
    "measurementId": "G-8KVV3H2X2L",
    "databaseURL":"https://fakenewsdetection-a73ba-default-rtdb.firebaseio.com/"
}

firebase = pyrebase.initialize_app(conf)
db = firebase.database()


with open('logistic_model.pkl', 'rb') as pkl:
    model = pickle.load(pkl)
    
with open('tfidf.pkl', 'rb') as tfidf:
    tfidf = pickle.load(tfidf)


@app.route("/predict",methods=['POST','GET'])
def predict():
    if request.method == 'POST':
        text = request.form['news']
        transformed = tfidf.transform([text])
        result = model.predict(transformed)[0]
        ct = datetime.datetime.now()
        if result == 'credible':
            flag = "Real"
        else:
            flag = "Fake"

        data = {'Prediction Time': str(ct), 'Text':text, 'Flag':flag}
        insertIntoLocalDB(data)
        db.child("Predictions").push(data)
        print(flag)
        return render_template('result.html', flag= flag)
    else:
        predictions = db.child("Predictions").get().each()
        
        return render_template('data.html', predictions=predictions)
    

@app.route('/')
def home():
	return render_template('home.html')


def insertIntoLocalDB(dictionary):
    local_db = sqlite3.connect('predictions.db')
    local_db.execute(f"INSERT INTO PREDICTIONS(CREATION_TIME, TEXT_BODY, FLAG)"
             f"VALUES ('{dictionary['Prediction Time']}', '{dictionary['Text']}', '{dictionary['Flag']}')")
    local_db.commit()
    local_db.close()


if __name__=='__main__':
    app.run()