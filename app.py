from flask import Flask, render_template, redirect, request, session, flash, jsonify
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL
import datetime
import time
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
        a = {}
        for i in results:
            # If the time exists
            if i[3].strip()!="":
                a[time.strftime("%I:%M %p", time.strptime(i[3], "%I:%M %p"))]=i
        # Sort according to time using strftime
        b = sorted((time.strptime(d, "%I:%M %p") for d in a.keys()))
        results = []

        for i in b:
            t = ((time.strftime( "%I:%M %p",i)))
            slotId = a[t][0]
            slotQuery = "SELECT COUNT(*) from student_slots WHERE slot_id="+str(slotId)
            cur.execute(slotQuery)
            count = cur.fetchone()
            results.append([a[t][0],a[t][1],a[t][2],a[t][3],a[t][4],a[t][5],8-int(count[0])])
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
        cur = mysql.connection.cursor()
        if recurring == "False":


            date = request.form['date']
            checkQuery = "SELECT id FROM slots WHERE date='"+date+"' AND time='"+time+"'"
            cur.execute(checkQuery)
            if len(cur.fetchall())!=0:
                flash("Slot already exists")
                return redirect('/new_slot')

            query = "INSERT into slots(time, recurring, date) values('" + time + "'," + recurring + ",'"+date+"')"
        else:
            day = request.form['day']
            checkQuery = "SELECT id FROM slots WHERE day='" + day + "' AND time='" + time + "'"
            cur.execute(checkQuery)
            if len(cur.fetchall()) != 0:
                flash("Slot already exists")
                return redirect('/new_slot')

            query = "INSERT into slots(day, time, recurring) values('" + day + "','" + time + "'," + recurring + ")"


        cur.execute(query)
        mysql.connection.commit()
        flash("Slot created successfully")
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


@app.route("/inventory", methods=['GET','POST'])
def inventory():
    if "username" not in session:
        flash("You must be logged in to view that page")
        return redirect('/login')
    if request.method=="GET":
        return render_template("inventory.html")
    else:
        name = request.form['name']
        type = request.form['type']
        description = request.form['description']
        price = request.form['price']
        images = request.files.getlist("images[]")
        for i in images:
            i.save(os.path.join(app.config['UPLOAD_FOLDER'],i.filename))
        cur = mysql.connection.cursor()
        query="INSERT into inventory(type, product_name, description, price) values('"+type+"','"+name+"','"+description+"','"+price+"')"
        cur.execute(query)
        mysql.connection.commit()
        flash("Item added succesfully")
        return redirect("/inventory")

@app.route("/payment", methods=['GET','POST'])
def payment():
    if "username" not in session:
        flash("You must be logged in to view that page")
        return redirect('/login')
    if request.method=="GET":
        cur = mysql.connection.cursor()
        query = "SELECT id, product_name, price from inventory"
        cur.execute(query)
        results = cur.fetchall()
        mydate = datetime.datetime.now()
        month = mydate.strftime("%B")
        return render_template("payment.html", results=results, month=month)
    else:
        payment_by = request.form['payment_by']
        if payment_by.strip()=="Student":
            cur = mysql.connection.cursor()
            student_id = request.form['student_id']
            studentIdCheck = "SELECT * from enrollment WHERE id="+str(student_id)
            cur.execute(studentIdCheck)
            student = cur.fetchone()
            if student is None:
                flash("No student found with that ID")
                return redirect("/payment")
            buyer_name = ""
            buyer_email = ""
            buyer_phone = ""

        else:
            student_id = "0"
            buyer_name = request.form['buyer_name']
            buyer_email = request.form['buyer_email']
            buyer_phone = request.form['buyer_phone']
            if buyer_email.strip() == "" or buyer_name.strip() == "" or buyer_phone.strip() == "":
                flash("invalid data entered. Please make sure buyer name, email and phone are filled in")
                return redirect("/payment")
        mydate = datetime.datetime.now()
        date = mydate.strftime("%d/%m/%Y %I:%M %p")
        product_id = request.form['product_id']
        product_name = ''
        product_price = ''
        if product_id == "Others":
            product_id= "0"
            product_name = request.form['product_name']
            product_price = request.form['product_price']
        cur = mysql.connection.cursor()
        query = "INSERT into sales(student_id, buyer_name, buyer_email, buyer_phone, product_id, date, product_name,\
                product_price) values("+str(student_id)+",'"+buyer_name+"','"+buyer_email+"','"+buyer_phone+"',"+str(product_id)+",\
                '"+date+"','"+product_name+"','"+product_price+"')"
        print(query)
        cur.execute(query)
        mysql.connection.commit()
        flash("Payment successfully recorded")
        return redirect("/payment")


@app.route("/allSales", methods=['GET','POST'])
def allSales():
    if request.method=="GET":
        cur = mysql.connection.cursor()
        query = "SELECT * from sales order by id"
        cur.execute(query)
        records = cur.fetchall()
        sales = []
        for i in records:
            date = i[6]
            #Check if its in the inventory
            product_id = int(i[5])
            if product_id!=0:
                productQuery = "SELECT product_name, price from inventory WHERE id=" + str(i[5])
                cur.execute(productQuery)
                product = cur.fetchone()

                #Chek if it is not a student
                if int(i[1])==0:
                    productName = product[0]
                    productPrice = product[1]
                    buyerName = i[2]
                    buyerPhone = i[4]
                    sales.append((productName,productPrice,buyerName,buyerPhone, date))
                #if student find name
                else:
                    studentQuery = "SELECT name, phone, father_phone from enrollment WHERE id="+str(i[1])
                    cur.execute(studentQuery)
                    result = cur.fetchone()
                    studentName = result[0]
                    if result[1].strip() == "":
                        studentPhone = result[1]
                    else:
                        studentPhone = result[2]
                    productName = product[0]
                    productPrice = product[1]
                    sales.append((productName, productPrice, studentName, studentPhone, date))
            else:

                if int(i[1])==0:
                    productName = i[7]
                    productPrice = i[8]
                    buyerName = i[2]
                    buyerPhone = i[4]
                    sales.append((productName,productPrice,buyerName,buyerPhone, date))
                #if student find name
                else:
                    studentQuery = "SELECT name, phone, father_phone from enrollment WHERE id="+str(i[1])
                    cur.execute(studentQuery)
                    result = cur.fetchone()
                    studentName = result[0]
                    if result[1].strip()=="":
                        studentPhone = result[1]
                    else:
                        studentPhone = result[2]
                    productName = i[7]
                    productPrice = i[8]
                    sales.append((productName, productPrice, studentName, studentPhone, date))


        return render_template("all_sales.html", sales=sales)

@app.route("/markFeePaid", methods=['POST'])
def markFeePaid():
    if request.method=="POST":
        id = request.form['id']
        month = request.form['month']
        query = "UPDATE enrollment SET fee_month='"+month+"' WHERE id="+id
        cur = mysql.connection.cursor()
        cur.execute(query)
        mysql.connection.commit()
        flash("Fee paid")
        return  redirect("/payment")

@app.route("/getStatus", methods=['GET','POST'])
def getStatus():
    id = request.form['id']
    query = "SELECT name, fee_month from enrollment WHERE id="+id
    cur = mysql.connection.cursor()
    cur.execute(query)
    last_fee_paid = cur.fetchone()
    if last_fee_paid is None:
        print("No student")
        return jsonify({"name": 'No student found'})
    name = last_fee_paid[0]
    last_fee_paid = last_fee_paid[1]

    mydate = datetime.datetime.now()
    feeMonth = mydate.strftime("%B")
    if last_fee_paid == feeMonth:
        status="Paid"
    else:
        status= "Due"

    return jsonify({"name":name, "status": status, "month": feeMonth})

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
