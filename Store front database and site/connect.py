from flask import Flask, render_template,request,session,url_for,redirect
import sqlite3
from datetime import date , datetime
# 
app = Flask(__name__)
app.secret_key = 'your-secret-key'
# 
def calculateAge(birthDate):
    date_object = datetime.strptime(birthDate, '%Y-%m-%d').date()
    today = date.today()
    age = today.year - date_object.year -((today.month, today.day) < (date_object.month, date_object.day))
 
    return age
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        connection = sqlite3.connect("Clothing_factory_db")
        cursor = connection.cursor()
        username = request.form['username']
        password = request.form['password']
        cursor.execute(f"select Username,Password from Account where Username = '{username}'")
        user = cursor.fetchone()
        if user and password == user[1]:
            session['username'] = user[0]
            return redirect(url_for("main_page"))
        else:
            return render_template("login.html", error="invalid username or password")
    return render_template("login.html")
@app.route('/main')
def main_page():
    if 'username' in session:
        return render_template("main page.html",username=session["username"])
    else:
       return render_template("login_page.html") 
@app.route('/women')
def women_shop():
    if 'username' in session:
        return render_template("women shop.html",username=session["username"])
    else:
       return render_template("login_page.html")
@app.route('/men')
def men_shop():
    if 'username' in session:
        return render_template("men shop.html",username=session["username"])
    else:
       return render_template("login_page.html")
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        connection = sqlite3.connect("Clothing_factory_db")
        cursor = connection.cursor()
        
        username = request.form['username']
        password = request.form['password']
        fname = request.form["first_name"]
        lname = request.form["last_name"]
        years = calculateAge(request.form["DOB"])
        Gen = request.form["Gender"]
        cursor.execute(f"insert into Account (Username,Password) values ('{username}', '{password}')")
        cursor.execute(f"insert into Customer (first_name, last_name,Gender ,Age) values ('{fname}', '{lname}','{Gen}','{years}')")
        connection.commit()
        cursor.close()
        connection.close()
    return render_template("sign up.html")
@app.route('/logout')
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))
    
if __name__ == '__main__':
    app.run(debug=True)
