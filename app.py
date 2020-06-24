from flask import Flask, render_template, redirect, request, session, flash
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL
import datetime
import os

app = Flask(__name__)
# Sql setup
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'ABWorldUser'
app.config['MYSQL_PASSWORD'] = '0XR0MF*&jCKE'
app.config['MYSQL_DB'] = 'ef22yrqyi32q'
app.config['UPLOAD_FOLDER'] = 'images'

mysql = MySQL(app)

app.secret_key = b'AbworldMusicSessionkey1234'

Bootstrap(app)



@app.route('/')
def index():
    return render_template("home.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form['username'];
        password = request.form['password']
        cur = mysql.connection.cursor()
        query = "SELECT * FROM users WHERE name='" + username + "' OR email='" + username + "' AND organization_id=2"
        cur.execute(query)
        records = cur.fetchall()
        if len(records) > 0:
            if records[0][4] == password:
                session['username'] = records[0][2]
                session['logged_in'] = True
                flash("Logged in successfully")
                return redirect('/dashboard')
        flash("Incorrect credentials")
        return redirect("/login")

@app.route("/logout", methods=['GET', 'POST'])
def logout():
    session.pop('username')
    session.pop('logged_in')
    return redirect('/login')

@app.route('/enrollment', methods=['GET', "POST"])
def enrollment():
    if "username" not in session:
        flash("You must be logged in to view that page")
        return redirect('/login')


    if request.method == "GET":
        type = request.args['type']
        cur = mysql.connection.cursor()
        query = 'SELECT * from slots WHERE recurring=1'
        cur.execute(query)
        records = cur.fetchall()
        slots = {}
        for i in records:
            slots[i[0]] = i[2]+" "+i[3]
        mydate = datetime.datetime.now()
        mydate = mydate.strftime("%B")
        if type == 'student':
            return render_template("enrollment.html", student=True, slots=slots, date=mydate)
        else:
            return render_template("enrollment.html", student=False, slots=slots, date=mydate)
    else:
        type = request.form['type']
        name = request.form['studentName']
        gender = request.form['gender']
        dob = request.form['studentDob']
        address = request.form['address']
        age = request.form['studentAge']
        # picture = request.files['picture']
        # If working professional get phone number directly
        if type == "False":
            phone = request.form['phone']
            fatherName=""
            fatherEmail=""
            fatherPhone=""
            fatherOccupation=""
            motherName = ""
            motherEmail = ""
            motherPhone = ""
            motherOccupation = ""
            type="Working"
        if type == "True":
            phone=""
            fatherName = request.form['fatherName']
            fatherPhone = request.form['fatherPhone']
            fatherEmail = request.form['fatherEmail']
            fatherOccupation = request.form['fatheroccupation']
            motherName = request.form['motherName']
            motherPhone = request.form['motherPhone']
            motherEmail = request.form['motherEmail']
            motherOccupation = request.form['motheroccupation']
            type='Student'
        instrument = request.form['Instrument']
        haveInstrument = request.form['haveInstrument']
        course = request.form['Course']
        joiningDate = request.form['joiningDate']
        advancePaid = request.form['advancePaid']
        feePaid = request.form['feePaid']
        awareNess = request.form['awareness']
        if awareNess == 'Others':
            awarenessOther = request.form['awarenessOther']
        else:
            awarenessOther=""
        mydate = datetime.datetime.now()
        feeMonth = mydate.strftime("%B")
        query= "INSERT into enrollment (name, type, gender, age, dob, phone, address, father_name, father_email, father_phone, \
                father_occupation, mother_name, mother_email, mother_phone, mother_occupation, instrument, have_instrument,\
                course, joining_date, advance_paid, fee_paid, fee_month, awareness, awareness_other) values( \
                '"+name+"','"+type+"','"+gender+"','"+age+"','"+dob+"','"+phone+"','"+address+"','"+fatherName+"','"+ \
                fatherEmail+"','"+fatherPhone+"','"+fatherOccupation+"','"+motherName+"','"+motherEmail+"','"+ \
                motherPhone+"','"+motherOccupation+"','"+instrument+"','"+haveInstrument+"','"+course+"','"+ \
                joiningDate+"',"+advancePaid+","+feePaid+",'"+feeMonth+"','"+awareNess+"','"+awarenessOther+"')"
        cur = mysql.connection.cursor()
        cur.execute(query)
        mysql.connection.commit()
        flash("Enrollment succesful")

        #Upload picture
        if "picture" in request.files:
            print("File selected")
            f = request.files['picture']
            f.save(os.path.join(app.config['UPLOAD_FOLDER'],f.filename))

        #Create slots
        StudentIdQuery  = "SELECT id from enrollment WHERE name='"+name+"' AND dob='"+dob+"'"
        cur.execute(StudentIdQuery)
        id = cur.fetchone()
        slots = request.form.getlist("batch-day[]")
        for i in slots:
            slotQuery = "INSERT into student_slots(student_id, slot_id) values("+str(id[0])+","+str(i)+")"
            cur.execute(slotQuery)
            mysql.connection.commit()
        return redirect('/enrollment?type=student')

@app.route("/slots", methods=['GET', 'POST'])
def slots():
    if "username" not in session:
        flash("You must be logged in to view that page")
        return redirect('/login')

    if request.method == "GET":
        cur = mysql.connection.cursor()
        query = "SELECT * FROM slots"
        cur.execute(query)
        results = cur.fetchall()

        return render_template('slots.html',results=results)


@app.route("/new_slot", methods=['GET','POST'])
def new_slot():
    if "username" not in session:
        flash("You must be logged in to view that page")
        return redirect('/login')
    if request.method=="GET":
        return render_template("new_slot.html")
    else:
        time = request.form['time']
        recurring = "True"
        recurring = request.form['recurring']
        if recurring == "False":
            date = request.form['date']
            query = "INSERT into slots(time, recurring, date) values('" + time + "'," + recurring + ",'"+date+"')"
        else:
            day = request.form['day']
            query = "INSERT into slots(day, time, recurring) values('" + day + "','" + time + "'," + recurring + ")"

        cur = mysql.connection.cursor()
        cur.execute(query)
        mysql.connection.commit()
        flash("Slot create successfully")
        return redirect('/slots')

@app.route("/delete_slot", methods=['GET'])
def delete_slot():
    if "username" not in session:
        flash("You must be logged in to view that page")
        return redirect('/login')
    if request.method=="GET":
        id = request.args['id']
        query = "DELETE from slots WHERE id="+id
        cur = mysql.connection.cursor()
        cur.execute(query)
        mysql.connection.commit()
        flash("Slot has been deleted")
        return redirect('/slots')


@app.route("/dashboard", methods=["GET"])
def dashboard():
    if "username" not in session:
        flash("You must be logged in to view that page")
        return redirect('/login')

    if request.method == "GET":
        user = session['username']
        return render_template("dashboard.html", user=user)


if __name__ == '__main__':
    app.run(debug=True)
