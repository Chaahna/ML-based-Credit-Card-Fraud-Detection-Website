from flask import *
import sqlite3, hashlib, os
import joblib
import pandas as pd
import numpy as np

from werkzeug.utils import secure_filename
from pprint import pprint

from sklearn.preprocessing import RobustScaler
from sklearn.model_selection import train_test_split


app = Flask(__name__)
app.secret_key = 'random string'
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def root():
    if 'email' in session:
        return render_template_string("<h1>You are logged in</h1> </h1><a href=\"/home\">Get Started</a> </h1><a href=\"/changePassword\">change pass</a> <a href=\"/logout\">logout</a>")
    else:
        return redirect(url_for('loginForm'))


@app.route("/changePassword", methods=["GET", "POST"])
def changePassword():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    if request.method == "POST":
        oldPassword = request.form['oldpassword']
        oldPassword = hashlib.md5(oldPassword.encode()).hexdigest()
        newPassword = request.form['newpassword']
        newPassword = hashlib.md5(newPassword.encode()).hexdigest()
        with sqlite3.connect('database.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT userId, password FROM users WHERE email = '" + session['email'] + "'")
            userId, password = cur.fetchone()
            if (password == oldPassword):
                try:
                    cur.execute("UPDATE users SET password = ? WHERE userId = ?", (newPassword, userId))
                    conn.commit()
                    msg="Changed successfully"
                except:
                    conn.rollback()
                    msg = "Failed"
                return render_template("changePassword.html", msg=msg)
            else:
                msg = "Wrong password"
        conn.close()
        return render_template("changePassword.html", msg=msg)
    else:
        return render_template("changePassword.html")

@app.route("/loginForm")
def loginForm():
    if 'email' in session:
        return redirect(url_for('root'))
    else:
        return render_template('login.html', error='')

@app.route("/login", methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if is_valid(email, password):
            session['email'] = email
            return redirect(url_for('root'))
        else:
            error = 'Invalid UserId / Password'
            return render_template('login.html', error=error)

@app.route("/register", methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        #Parse form data
        password = request.form['password']
        email = request.form['email']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        phone = request.form['phone']

        with sqlite3.connect('database.db') as con:
            try:
                cur = con.cursor()
                cur.execute('INSERT INTO users (password, email, firstName, lastName, phone) VALUES (?, ?, ?, ?, ?)', (hashlib.md5(password.encode()).hexdigest(), email, firstName, lastName, phone))

                con.commit()

                msg = "Registered Successfully"    

            except:
                con.rollback()
                msg = "Error occured"
        con.close()
        return render_template("login.html", error=msg)

@app.route("/registerationForm")
def registrationForm():
    return render_template("register.html")

@app.route("/logout")
def logout():
    session.pop('email', None)
    return redirect(url_for('root'))

def is_valid(email, password):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute('SELECT email, password FROM users')
    data = cur.fetchall()
    for row in data:
        if row[0] == email and row[1] == hashlib.md5(password.encode()).hexdigest():
            return True
    return False

@app.errorhandler(404) 
# inbuilt function which takes error as parameter 
def not_found(e): 
# defining function 
  return render_template("404.html")

@app.route('/home')
def home():
	return render_template('home.html')

def preprocessing(data):
	X = data.drop('Class', axis=1)
	y = data['Class']

	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

	robust_scaler = RobustScaler().fit(X_train)

	X_test = pd.DataFrame(robust_scaler.transform(X_test), columns=X.columns)

	return X_test, y_test

@app.route('/results')
def results():
	data = pd.read_csv('creditcard.csv')
	labels = {0: "Not Fraud", 1: "Fraud"}

	X_test, y_test = preprocessing(data)

	rf_model = joblib.load('models/random_forest_model.pkl')	
	lr_model = joblib.load('models/logistic_regression_model.pkl')	
	#nb_model = joblib.load('models/naive_bayes_model.pkl')	
	
	input_tuple = X_test.sample(1) # Select a random row from X_test

	pprint(input_tuple)

	rf_prediction = labels[rf_model.predict(input_tuple)[0]]
	lr_prediction = labels[lr_model.predict(input_tuple)[0]]
	#nb_prediction = labels[nb_model.predict(input_tuple)[0]]
	y_true = labels[y_test.iloc[input_tuple.index[0]]]

	new_input_tuple = input_tuple.to_dict('records')[0] # Convert DataFrame to format => [{col_name_1: value_1, col_name_2: value_2, ...}, {second_row}]

	# Converting Amount & Time values to the ones before preprocessing so that it can be displayed on webpage
	new_input_tuple['Amount'] = data.iloc[input_tuple.index[0]]['Amount']
	new_input_tuple['Time'] = data.iloc[input_tuple.index[0]]['Time']

	for col in new_input_tuple: # Round off each value to 4 decimal values so that it looks good on webpage
		new_input_tuple[col] = round(new_input_tuple[col], 4)

	return render_template("results.html", lr_prediction=lr_prediction, rf_prediction=rf_prediction, y_true=y_true, input_tuple=new_input_tuple)




if __name__ == '__main__':
    app.run(debug=True)
