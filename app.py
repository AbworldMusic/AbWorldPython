from flask import Flask, render_template, redirect, request, session, flash, jsonify, send_from_directory
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL
import datetime
import time
from time import mktime
import os
import hashlib
import time
app = Flask(__name__)
# Sql setup
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'ABWorldUser'
app.config['MYSQL_PASSWORD'] = '0XR0MF*&jCKE'
app.config['MYSQL_DB'] = 'ef22yrqyi32q'
app.config['UPLOAD_FOLDER'] = 'images'
app.config['MAX_CONTENT_LENGTH'] = 1000 * 1024 * 1024

mysql = MySQL(app)

app.secret_key = b'AbworldMusicSessionkey1234'

Bootstrap(app)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


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
        password = hashlib.sha3_256(password.encode()).hexdigest()
        cur = mysql.connection.cursor()
        query = "SELECT * FROM users WHERE fullname='" + username + "' OR email='" + username + "'"
        cur.execute(query)
        records = cur.fetchall()
        if len(records) > 0:
            if records[0][5].strip() == "unset":
                print(records)
                return redirect("/reset_password?id="+str(records[0][0]))
            elif records[0][5] == password:
                session['username'] = records[0][2]
                session['logged_in'] = True
                flash("Logged in successfully", "success")
                return redirect('/dashboard')
        flash("Incorrect credentials", "danger")
        return redirect("/login")

@app.route("/reset_password", methods=['GET', 'POST'])
def reset_password():
    if request.method=="GET":
        id = request.args['id']
        return render_template("reset_password.html", id=id)
    else:
        id = request.form['id']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password != confirm_password:
            flash("Password fields do not match",'danger')
            return redirect("/reset_password?id="+id)
        else:
            cur = mysql.connection.cursor()
            password = hashlib.sha3_256(password.encode()).hexdigest()
            query = "UPDATE users SET password='"+password+"' WHERE id="+id
            cur.execute(query)
            mysql.connection.commit()
            flash("Password set succesfully. Login to continue","success")
            return redirect("/login")

@app.route("/logout", methods=['GET', 'POST'])
def logout():
    session.pop('username')
    session.pop('logged_in')
    return redirect('/login')


@app.route('/enrollment', methods=['GET', "POST"])
def enrollment():
    if "username" not in session:
        flash("You must be logged in to view that page", 'danger')
        return redirect('/login')

    if request.method == "GET":
        type = request.args['type']
        cur = mysql.connection.cursor()
        query = 'SELECT * from slots WHERE recurring=1'
        cur.execute(query)
        records = cur.fetchall()
        slots = {}
        for i in records:
            slots[i[0]] = i[2] + " " + i[3]
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
            fatherName = ""
            fatherEmail = ""
            fatherPhone = ""
            fatherOccupation = ""
            motherName = ""
            motherEmail = ""
            motherPhone = ""
            motherOccupation = ""
            type = "Working"
            email = request.form['email']
        if type == "True":
            phone = request.form['studentPhone']
            fatherName = request.form['fatherName']
            fatherPhone = request.form['fatherPhone']
            fatherEmail = request.form['fatherEmail']
            fatherOccupation = request.form['fatheroccupation']
            motherName = request.form['motherName']
            motherPhone = request.form['motherPhone']
            motherEmail = request.form['motherEmail']
            motherOccupation = request.form['motheroccupation']
            type = 'Student'
            email = request.form['studentEmail']
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
            awarenessOther = ""
        mydate = datetime.datetime.now()
        feeMonth = mydate.strftime("%B")
        last_fee_paid_date = mydate.strftime("%Y-%m-%d")
        query = "INSERT into enrollment (name, type, gender, age, dob, phone, address, father_name, father_email, father_phone, \
                father_occupation, mother_name, mother_email, mother_phone, mother_occupation, instrument, have_instrument,\
                course, joining_date, advance_paid, fee_paid,last_fee_paid_date, fee_month, awareness, awareness_other, email) values( \
                '" + name + "','" + type + "','" + gender + "','" + age + "','" + dob + "','" + phone + "','" + address + "','" + fatherName + "','" + \
                fatherEmail + "','" + fatherPhone + "','" + fatherOccupation + "','" + motherName + "','" + motherEmail + "','" + \
                motherPhone + "','" + motherOccupation + "','" + instrument + "','" + haveInstrument + "','" + course + "','" + \
                joiningDate + "'," + advancePaid + "," + feePaid + ",'" + last_fee_paid_date + "','" + feeMonth + "','" + awareNess + "','" + awarenessOther + "','"+email+"')"
        cur = mysql.connection.cursor()
        cur.execute(query)
        mysql.connection.commit()
        flash("Enrollment successful", 'success')
        getLastEnrollment = "SELECT id from enrollment order by id DESC LIMIT 1"
        cur.execute(getLastEnrollment)
        link_id = cur.fetchone()[0]

        # Upload picture
        if "picture" in request.files:
            f = request.files['picture']
            if f.filename.strip() != "":
                query = "INSERT into files (filename, type, link_id) values ('" + f.filename + "','profile'," + str(link_id) + ")"
                cur.execute(query)
                mysql.connection.commit()

                f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))

        # Create slots
        StudentIdQuery = "SELECT id from enrollment WHERE name='" + name + "' AND dob='" + dob + "'"
        cur.execute(StudentIdQuery)
        id = cur.fetchone()
        slots = request.form.getlist("batch-day[]")
        for i in slots:
            slotQuery = "INSERT into student_slots(student_id, slot_id) values(" + str(id[0]) + "," + str(i) + ")"
            cur.execute(slotQuery)

        # Update sales
        fee = ""
        if course == "Intermediate":
            fee = 1500
        elif course == "Hobby":
            fee = 1000
        elif course == "Advanced":
            fee = 2000
        salesQuery = "INSERT into sales (student_id, date, product_name, product_price) values (" + str(link_id) + ",'" + last_fee_paid_date + "','Fees for enrollment','" + str(fee) + "')"
        cur.execute(salesQuery)

        # Update students lesson
        lessonQuery = "SELECT id from lessons WHERE category='"+instrument+"' ORDER BY id ASC LIMIT 1"
        cur.execute(lessonQuery)
        res = cur.fetchone()
        if res is not None:
            updateLesson = "INSERT into progress (student_id, lesson_id) values ("+str(link_id)+","+str(res[0])+")"
            cur.execute(updateLesson)
        mysql.connection.commit()
        return redirect('/enrollment?type=student')


@app.route("/slots", methods=['GET', 'POST'])
def slots():
    if "username" not in session:
        flash("You must be logged in to view that page", 'danger')
        return redirect('/login')

    if request.method == "GET":
        cur = mysql.connection.cursor()
        query = "SELECT * FROM slots WHERE recurring=true"
        cur.execute(query)
        results = cur.fetchall()
        a = {}
        for i in results:
            # If the time exists
            if i[3].strip() != "":
                a[time.strftime("%A %I:%M %p", time.strptime(i[2]+" "+i[3], "%A %I:%M %p"))] = i
        # Sort according to time using strftime
        b = sorted((time.strptime(d, "%A %I:%M %p") for d in a.keys()))
        results = []

        for i in b:
            t = ((time.strftime("%A %I:%M %p", i)))
            slotId = a[t][0]
            slotQuery = "SELECT COUNT(*) from student_slots WHERE slot_id=" + str(slotId)
            cur.execute(slotQuery)
            count = cur.fetchone()
            results.append([a[t][0], a[t][1], a[t][2], a[t][3], a[t][4], a[t][5], 8 - int(count[0])])
        return render_template('slots.html', results=results)


@app.route("/new_slot", methods=['GET', 'POST'])
def new_slot():
    if "username" not in session:
        flash("You must be logged in to view that page", 'danger')
        return redirect('/login')
    if request.method == "GET":
        return render_template("new_slot.html")
    else:
        time = request.form['time']
        recurring = "True"
        recurring = request.form['recurring']
        cur = mysql.connection.cursor()
        if recurring == "False":

            date = request.form['date']
            checkQuery = "SELECT id FROM slots WHERE date='" + date + "' AND time='" + time + "'"
            cur.execute(checkQuery)
            if len(cur.fetchall()) != 0:
                flash("Slot already exists", "danger")
                return redirect('/new_slot')

            query = "INSERT into slots(time, recurring, date) values('" + time + "'," + recurring + ",'" + date + "')"
        else:
            day = request.form['day']
            checkQuery = "SELECT id FROM slots WHERE day='" + day + "' AND time='" + time + "'"
            cur.execute(checkQuery)
            if len(cur.fetchall()) != 0:
                flash("Slot already exists", "danger")
                return redirect('/new_slot')

            query = "INSERT into slots(day, time, recurring) values('" + day + "','" + time + "'," + recurring + ")"

        cur.execute(query)
        mysql.connection.commit()
        flash("Slot created successfully", "success")
        return redirect('/slots')


@app.route("/delete_slot", methods=['GET'])
def delete_slot():
    if "username" not in session:
        flash("You must be logged in to view that page", "danger")
        return redirect('/login')
    if request.method == "GET":
        id = request.args['id']
        query = "DELETE from slots WHERE id=" + id
        cur = mysql.connection.cursor()
        cur.execute(query)
        mysql.connection.commit()
        flash("Slot has been deleted", "danger")
        return redirect('/slots')


@app.route("/inventory", methods=['GET', 'POST'])
def inventory():
    if "username" not in session:
        flash("You must be logged in to view that page", "danger")
        return redirect('/login')
    if request.method == "GET":
        return render_template("inventory.html")
    else:
        name = request.form['name']
        type = request.form['type']
        description = request.form['description']
        price = request.form['price']
        images = request.files.getlist("images[]")
        for i in images:
            i.save(os.path.join(app.config['UPLOAD_FOLDER'], i.filename))
        cur = mysql.connection.cursor()
        query = "INSERT into inventory(type, product_name, description, price) values('" + type + "','" + name + "','" + description + "','" + price + "')"
        cur.execute(query)
        mysql.connection.commit()
        flash("Item added succesfully", "success")
        return redirect("/inventory")


@app.route("/payment", methods=['GET', 'POST'])
def payment():
    if "username" not in session:
        flash("You must be logged in to view that page", "danger")
        return redirect('/login')
    if request.method == "GET":
        cur = mysql.connection.cursor()
        query = "SELECT id, product_name, price from inventory"
        cur.execute(query)
        results = cur.fetchall()
        mydate = datetime.datetime.now()
        month = mydate.strftime("%B")
        return render_template("payment.html", results=results, month=month)
    else:
        payment_by = request.form['payment_by']
        if payment_by.strip() == "Student":
            cur = mysql.connection.cursor()
            student_id = request.form['student_id']
            studentIdCheck = "SELECT * from enrollment WHERE id=" + str(student_id)
            cur.execute(studentIdCheck)
            student = cur.fetchone()
            if student is None:
                flash("No student found with that ID", "danger")
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
                flash("invalid data entered. Please make sure buyer name, email and phone are filled in", "danger")
                return redirect("/payment")
        mydate = datetime.datetime.now()
        date = mydate.strftime("%d/%m/%Y %I:%M %p")
        product_id = request.form['product_id']
        product_name = ''
        product_price = ''
        if product_id == "Others":
            product_id = "0"
            product_name = request.form['product_name']
            product_price = request.form['product_price']
        cur = mysql.connection.cursor()
        query = "INSERT into sales(student_id, buyer_name, buyer_email, buyer_phone, product_id, date, product_name,\
                product_price) values(" + str(
            student_id) + ",'" + buyer_name + "','" + buyer_email + "','" + buyer_phone + "'," + str(product_id) + ",\
                '" + date + "','" + product_name + "','" + product_price + "')"
        cur.execute(query)
        mysql.connection.commit()
        flash("Payment successfully recorded", "success")
        return redirect("/payment")


@app.route("/allSales", methods=['GET', 'POST'])
def allSales():
    if request.method == "GET":
        cur = mysql.connection.cursor()
        query = "SELECT * from sales order by id"
        cur.execute(query)
        records = cur.fetchall()
        sales = []
        for i in records:
            date = i[6]
            # Check if its in the inventory
            product_id = int(i[5])
            if product_id != 0:
                productQuery = "SELECT product_name, price from inventory WHERE id=" + str(i[5])
                cur.execute(productQuery)
                product = cur.fetchone()

                # Chek if it is not a student
                if int(i[1]) == 0:
                    productName = product[0]
                    productPrice = product[1]
                    buyerName = i[2]
                    buyerPhone = i[4]
                    sales.append((productName, productPrice, buyerName, buyerPhone, date))
                # if student find name
                else:
                    studentQuery = "SELECT name, phone, father_phone from enrollment WHERE id=" + str(i[1])
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

                if int(i[1]) == 0:
                    productName = i[7]
                    productPrice = i[8]
                    buyerName = i[2]
                    buyerPhone = i[4]
                    sales.append((productName, productPrice, buyerName, buyerPhone, date))
                # if student find name
                else:
                    studentQuery = "SELECT name, phone, father_phone from enrollment WHERE id=" + str(i[1])
                    cur.execute(studentQuery)
                    result = cur.fetchone()
                    studentName = result[0]
                    if result[1].strip() == "":
                        studentPhone = result[1]
                    else:
                        studentPhone = result[2]
                    productName = i[7]
                    productPrice = i[8]
                    sales.append((productName, productPrice, studentName, studentPhone, date))

        return render_template("all_sales.html", sales=sales)


@app.route("/markFeePaid", methods=['POST'])
def markFeePaid():
    if request.method == "POST":
        id = request.form['id']
        month = request.form['month']
        mydate = datetime.datetime.now()
        date = mydate.strftime("%Y-%m-%d")
        query = "UPDATE enrollment SET fee_month='" + month + "', last_fee_paid_date='" + date + "' WHERE id=" + id
        cur = mysql.connection.cursor()
        cur.execute(query)
        query = "SELECT course from enrollment WHERE id="+id
        cur.execute(query)
        res = cur.fetchone()
        course = res[0]
        fee = ""
        if course=="Intermediate":
            fee = 1500
        elif course == "Hobby":
            fee = 1000
        elif course == "Advanced":
            fee = 2000

        date = mydate.strftime("%d/%m/%Y %I:%M %p")
        pr_name = "Fees for "+ month
        query = "INSERT into sales (student_id, date, product_name, product_price) values ("+id+",'"+date+"','"+pr_name+"','"+str(fee)+"')"
        cur.execute(query)
        mysql.connection.commit()
        flash("Fee paid", "success")
        return redirect("/payment")

@app.route("/API_facultyStatus", methods=['GET', 'POST'])
def facultyStatus():
    if request.method=="GET":
        mydate = datetime.datetime.now()
        date = mydate.strftime("%d/%m/%Y")
        id = request.args['id']
        query = "SELECT type from arrival_logs WHERE user_id="+str(id)+" AND time LIKE '%"+ date +"%' ORDER BY id DESC LIMIT 1"
        cur = mysql.connection.cursor()
        cur.execute(query)
        res = cur.fetchone()
        return jsonify({"status": res})

@app.route("/getStatus", methods=['GET', 'POST'])
def getStatus():
    id = request.form['id']
    query = "SELECT name, fee_month from enrollment WHERE id=" + id
    cur = mysql.connection.cursor()
    cur.execute(query)
    last_fee_paid = cur.fetchone()
    if last_fee_paid is None:
        return jsonify({"name": 'No student found'})
    name = last_fee_paid[0]
    last_fee_paid = last_fee_paid[1]

    month_number = time.strptime(last_fee_paid, "%B").tm_mon
    lastMonth = time.strptime(str(month_number), "%m")
    lastMonth = time.strftime("%B", lastMonth)
    if month_number == 12:
        month_number = 0

    feeMonth = time.strptime(str(month_number + 1), "%m")
    feeMonth = time.strftime("%B", feeMonth)



    mydate = datetime.datetime.now()
    currentMonth = mydate.strftime("%B")
    lastPayment = "SELECT date, product_name from sales WHERE student_id="+str(id)+" AND product_name like '%Fees for%' order by id DESC LIMIT 1"
    cur.execute(lastPayment)
    res = cur.fetchone()
    if res is not None:
        lastPayment  = res[0]+" ("+res[1]+")"
    else:
        lastPayment = ""

    if currentMonth == lastMonth:
        status = "Paid"
    else:
        status = "Due"

    return jsonify({"name": name, "status": status, "month": feeMonth, "lastPayment": lastPayment})


@app.route("/dashboard", methods=["GET"])
def dashboard():
    if "username" not in session:
        flash("You must be logged in to view that page", "danger")
        return redirect('/login')

    if request.method == "GET":
        user = session['username']
        return render_template("dashboard.html", user=user)


@app.route("/dailyTransactions", methods=['GET'])
def daily_transaction():
    if request.method == "GET":
        if "on" in request.args:
            mydate = time.strptime(request.args['on'], '%m/%d/%Y')
            mydate = datetime.datetime.fromtimestamp(mktime(mydate))
        else:
            mydate = datetime.datetime.now()
        date = mydate.strftime("%d %B %Y, %A")
        date2 = mydate.strftime("%m/%d/%YYYY")

        salesDate = mydate.strftime("%d %m %Y")
        cur = mysql.connection.cursor()
        query = "SELECT * FROM sales WHERE date like '%" + salesDate.replace(" ", "%") + "%'"
        cur.execute(query)
        result = cur.fetchall()

        dailySales = {"inventory_sales": 0, "fee_payment": 0, "enrollment": 0}
        for i in result:

            product_id = i[5]
            if int(product_id) != 0:
                product_query = "SELECT price from inventory WHERE id=" + str(product_id)
                cur.execute(product_query)
                product_price = cur.fetchone()
                dailySales['inventory_sales'] = dailySales['inventory_sales'] + float(product_price[0])
            else:
                product_price = i[8]
                dailySales['inventory_sales'] = dailySales['inventory_sales'] + float(product_price)

        joinDate = mydate.strftime("%Y-%m-%d")

        cur = mysql.connection.cursor()
        enrollments = "SELECT advance_paid, course, fee_paid, joining_date, last_fee_paid_date FROM enrollment " \
                      "WHERE joining_date like '%" + joinDate + "%' OR last_fee_paid_date like '%" + joinDate + "%'"
        cur.execute(enrollments)
        result = cur.fetchall()

        for i in result:
            advance_paid = int(i[0])
            joining_date = i[3]
            last_fee_paid_date = i[4]
            if advance_paid and last_fee_paid_date in joining_date and last_fee_paid_date.strip() != "":
                dailySales['enrollment'] = dailySales['enrollment'] + 500

            course = i[1]
            fee_paid = i[2]
            if last_fee_paid_date.strip() != "" and last_fee_paid_date not in joining_date:
                key = "fee_payment"
            else:
                key = "enrollment"
            if fee_paid:
                if course == "Hobby":
                    dailySales[key] = dailySales[key] + 500
                elif course == "Intermediate":
                    dailySales[key] = dailySales[key] + 1000
                elif course == "Advanced":
                    dailySales[key] = dailySales[key] + 1500

        return render_template("daily_transactions.html", date=date, date2=date2, dailySales=dailySales)


@app.route("/inventoryItems", methods=['GET'])
def inventoryItems():
    if request.method == "GET":
        cur = mysql.connection.cursor()
        query = "SELECT id, product_name, description, type, price from inventory"
        cur.execute(query)
        results = cur.fetchall()
        data = []
        for i in results:
            data.append({
                "id": i[0],
                "product_name": i[1],
                "description": i[2],
                "type": i[3],
                "price": i[4]
            })

        return render_template("inventory_items.html", data=data)


@app.route("/delete_item", methods=["GET"])
def delete_item():
    if request.method == "GET":
        if "id" in request.args:
            id = request.args["id"]
            query = "DELETE from inventory WHERE id=" + str(id)
            print(query)
            cur = mysql.connection.cursor()
            cur.execute(query)
            mysql.connection.commit()
            flash("Item deleted", 'danger')
            return redirect("/inventoryItems")


@app.route("/students", methods=['GET', 'POST'])
def students():
    if request.method == "GET":
        query = "SELECT id, name, gender, instrument, course from enrollment order by id"
        cur = mysql.connection.cursor()
        cur.execute(query)
        results = cur.fetchall()
        data = []
        for i in results:
            data.append({
                "id": i[0],
                "name": i[1],
                "gender": i[2],
                "instrument": i[3],
                "course": i[4]
            })
        return render_template("students.html", data=data)


@app.route("/student_dashboard", methods=["GET"])
def student_dashboard():
    if request.method == "GET":
        if "id" in request.args:
            id = request.args['id']
            query = "SELECT * from enrollment WHERE id=" + id
            cur = mysql.connection.cursor()
            cur.execute(query)
            result = cur.fetchone()
            data = {"id": id,
                    "name": result[1],
                    "type": result[2],
                    "gender": result[3],
                    "age": result[4],
                    "dob": result[5],
                    "phone": result[6],
                    "address": result[7],
                    "father_name": result[8],
                    "father_email": result[9],
                    "father_phone": result[10],
                    "father_occupation": result[11],
                    "mother_name": result[12],
                    "mother_email": result[13],
                    "mother_phone": result[14],
                    "mother_occupation": result[15],
                    "instrument": result[16],
                    "course": result[18],
                    "joining_date": result[19],
                    "email": result[26]
                    }
            image = ""
            fileQuery  = "SELECT filename from files WHERE type='profile' AND link_id="+ id
            cur.execute(fileQuery)
            result = cur.fetchone()

            if result != None:
                image = result[0]
            return render_template("student_dashboard.html", data=data, image=image)


@app.route("/studioSessions", methods=['GET','POST'])
def studioSessions():
    if request.method=="GET":
        return render_template("studio_sessions.html")
    else:
        student_id  = request.form['student_id']
        scheduled_on = request.form['scheduled_on']
        song = request.form['song']
        details = request.form['details']
        cur = mysql.connection.cursor()
        checkStudent = "SELECT * from enrollment WHERE id="+str(student_id)
        cur.execute(checkStudent)
        res = cur.fetchall()
        if res is None or len(res)==0:
            flash("Student id not found", "danger")
            return redirect("/studioSessions")

        query = "INSERT into studio (student_id, scheduled_on, song, details) values ("+str(student_id)+",'"+scheduled_on+"','"+song+"','"+details+"')"
        cur.execute(query)
        mysql.connection.commit()
        flash("Studio session scheduled successfully", "success")
        return redirect('/studioSessions')

@app.route("/lessonPlan", methods=['GET'])
def lessonPlan():
    if request.method == "GET":
        cur = mysql.connection.cursor()
        query = "SELECT * from levels order by position"
        cur.execute(query)
        result = cur.fetchall()
        data = []
        for i in result:
            data.append({
                "id": i[0],
                'name': i[1],
                "color": i[3]
            })

        return render_template("lesson_plan.html",data=data)

@app.route('/add_new_level', methods=['GET','POST'])
def add_new_level():
    if request.method=='GET':
        return render_template("add_new_level.html")
    else:
        name = request.form['name']
        position = request.form['position']
        color = request.form['color']
        cur = mysql.connection.cursor()
        query = "INSERT into levels (name, position, color) values('"+name+"',"+position+",'"+color+"')"
        print(query)
        cur.execute(query)
        mysql.connection.commit()
        flash("Level was created successfully", "success")
        return redirect('/lessonPlan')

@app.route("/add_new_lesson", methods=['GET','POST'])
def add_new_lesson():
    if request.method=="GET":
        if "id" in request.args:
            id=request.args['id']
            query = "SELECT name from levels WHERE id="+str(id)
            cur = mysql.connection.cursor()
            cur.execute(query)
            level = cur.fetchone()[0]
            return render_template("add_new_lesson.html", level=level, level_id=id)
    else:
        name = request.form['name']
        level = request.form['level']
        desc = request.form['desc']
        category = request.form['category']
        desc = desc.replace("'","")
        query = "INSERT into lessons (title, category, description, level) values('"+name+"','"+category+"','"+desc+"',"+level+")"
        cur = mysql.connection.cursor()
        cur.execute(query)
        mysql.connection.commit()

        getLatestId = "SELECT id from lessons order by id DESC LIMIT 1"
        cur.execute(getLatestId)
        lessonId = cur.fetchone()[0]
        images = request.files.getlist("images[]")
        for i in images:
            query = "INSERT into files (filename, type, link_id) values ('"+i.filename+"','lesson',"+str(lessonId)+")"
            cur.execute(query)
            mysql.connection.commit()
            i.save(os.path.join(app.config['UPLOAD_FOLDER'], i.filename))
        flash("Lessons added successfully", 'success')
        return redirect("/lessonPlan")

@app.route("/load_lessons", methods=['GET',"POST"])
def load_lessons():
    if request.method == "POST":
        cur = mysql.connection.cursor()
        query = "SELECT id, title from lessons WHERE level="+request.form['id']
        print(query)
        cur.execute(query)
        result = cur.fetchall()
        data = []
        for i in result:
            data.append({
                "id": i[0],
                "name": i[1]
            })
        return jsonify(data)

@app.route("/view_lesson", methods=["GET", 'POST'])
def view_lesson():
    if request.method=="GET":
        if "id" in request.args:
            cur = mysql.connection.cursor()
            query = "SELECT title, category, description, level from lessons WHERE id="+request.args['id']
            cur.execute(query)
            result = cur.fetchone()
            data = {
                'id': request.args['id'],
                'name': result[0],
                'category': result[1],
                'desc': result[2],
                'level': result[3]
            }
            return render_template("view_lesson.html",data=data)

@app.route("/view_images_for_lesson", methods=['GET',"POST"])
def view_images_for_lesson():
    cur = mysql.connection.cursor()
    query = "SELECT filename from files WHERE type='lesson' AND link_id="+request.form['id']
    cur.execute(query)
    result = cur.fetchall()
    data = []
    for i in result:
        data.append(i[0])
    return jsonify(data)

@app.route("/leads", methods=['POST','GET'])
def leads():
    if request.method=="GET":
        cur = mysql.connection.cursor()
        query = "SELECT * from leads"
        cur.execute(query)
        results = cur.fetchall()
        data = []
        for i in results:
            record = {}
            record['id']=i[0]
            record['name'] = i[1]
            record['phone'] = i[2]
            record['email'] = i[3]
            record['enquiry_for'] = i[4]
            record['note'] = i[5]
            record['is_pending'] = i[6]
            record['is_stalled'] = i[7]
            record['is_converted'] = i[8]
            if i[6]:
                record['status'] = "Pending"
                record['color'] = "orange"
            elif i[7]:
                record['status'] = "Stalled"
                record['color'] = "#007bff"
            elif i[8]:
                record['status'] = "Completed"
                record['color'] = "green"
            elif i[9]:
                record['status'] = "Suppressed"
                record['color'] = "red"

            else:
                record['status'] = "Pending"
                record['color'] = "orange"
            record["created_at"] = i[10]
            record["updated_at"] = i[11]

            data.append(record)

        return render_template("all_leads.html", data=data)


@app.route("/new_lead", methods=['POST',"GET"])
def new_lead():
    if request.method=="GET":
        return render_template("leads.html")
    else:
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        note = request.form['note']
        enquiry_for = request.form['enquiry_for']
        cur = mysql.connection.cursor()
        mydate = datetime.datetime.now()
        date = mydate.strftime("%d/%m/%Y %I:%M %p")

        query = "INSERT into leads (name, phone, email, enquiry_for, note, is_pending, created_at) values('"+name+"'" \
              ",'"+phone+"','"+email+"','"+enquiry_for+"','"+note+"', 1 ,'"+date+"')"
        cur.execute(query)
        mysql.connection.commit()
        flash("Lead registered successfully","success")
        return redirect("/leads")

@app.route("/view_lead", methods=['GET','POST'])
def view_lead():
    if "id" in request.args:
        id = request.args['id']
        cur = mysql.connection.cursor()
        query = 'SELECT * from leads WHERE id='+id
        cur.execute(query)
        result = cur.fetchone()
        data = {"id": result[0], "name": result[1], "phone": result[2], 'email': result[3],"enquiry_for": result[4], "note": result[5]}
        if result[6]:
            data['status'] = "Pending"
            data['color'] = "orange"
        elif result[7]:
            data['status'] = "Stalled"
            data['color'] = "#007bff"
        elif result[8]:
            data['status'] = "Completed"
            data['color'] = "green"
        elif result[9]:
            data['status'] = "Suppressed"
            data['color'] = "red"

        else:
            data['status'] = "Pending"
            data['color'] = "orange"
        data["created_at"] = result[10]
        data["updated_at"] = result[11]

        return render_template("view_lead.html", data=data)

@app.route("/update_lead_notes", methods=['POST'])
def update_lead_notes():
    id = request.form['id']
    note = request.form['note']
    mydate = datetime.datetime.now()
    date = mydate.strftime("%d/%m/%Y %I:%M %p")
    cur = mysql.connection.cursor()
    query = "UPDATE leads set note='"+note+"', updated_at='"+date+"' WHERE id="+id
    cur.execute(query)
    mysql.connection.commit()
    flash("Lead updated", "success")
    return redirect("/leads")

@app.route("/update_lead_status", methods=['GET','POST'])
def update_lead_status():
    if request.method=="GET":
        id = request.args['id']
        status = request.args['status']
        pending = 0
        stalled = 0
        completed = 0
        suppressed = 0

        mydate = datetime.datetime.now()
        date = mydate.strftime("%d/%m/%Y %I:%M %p")
        if status=="stall":
            stalled = 1
        if status=="completed":
            completed = 1
        if status =="suppress":
            suppressed = 1

        cur = mysql.connection.cursor()
        query = "UPDATE leads set is_pending="+str(pending)+",is_stalled="+str(stalled)+"," \
                "is_converted="+str(completed)+", is_suppressed="+str(suppressed)+", updated_at='"+date+"' WHERE id="+id
        cur.execute(query)
        mysql.connection.commit()
        flash("lead status updated")
        return redirect("/view_lead?id="+id)

@app.route("/edit_student", methods=["GET","POST"])
def edit_student():
    if request.method=="GET":
        id = request.args['id']
        query = "SELECT name, gender, type, instrument, course, joining_date, father_name, father_phone, father_email, father_occupation,"+ \
                "mother_name, mother_phone, mother_email, mother_occupation, phone, email from enrollment WHERE id="+str(id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        record = cur.fetchone()

        data = {
            "id": str(id),
            "name": record[0],
            "gender": record[1],
            "type": record[2],
            "instrument": record[3],
            "course": record[4],
            "joining_date": record[5],
            "father_name": record[6],
            "father_phone": record[7],
            "father_email": record[8],
            "father_occupation": record[9],
            "mother_name": record[10],
            "mother_phone": record[11],
            "mother_email": record[12],
            "mother_occupation": record[12],
            "phone": record[13],
            "email": record[14]
        }
        print(data)
        return render_template("edit_student.html", data=data)
    else:
        id = request.form['id']
        name = request.form['studentName']
        gender = request.form['gender']
        instrument = request.form['instrument']
        type = request.form['type']
        if type=="Student":
            father_name = request.form['father_name']
            father_phone = request.form['father_phone']
            father_email = request.form['father_email']
            father_occupation = request.form['father_occupation']
            mother_name = request.form['mother_name']
            mother_phone = request.form['mother_phone']
            mother_email = request.form['mother_email']
            mother_occupation = request.form['mother_occupation']
            phone = ''
            email = ''
        else:
            father_name = ''
            father_phone = ''
            father_email = ''
            father_occupation = ''
            mother_name = ''
            mother_phone = ''
            mother_email = ''
            mother_occupation = ''
            phone = request.form['phone']
            email = request.form['email']
        query = "UPDATE enrollment set name='"+name+"',gender='"+gender+"',"+\
            "instrument='"+instrument+"',father_name='"+father_name+"',father_phone='"+father_phone+"',"+ \
            "father_phone = '"+father_phone+"', father_occupation = '"+father_occupation+"', "+ \
            "mother_name='"+mother_name+"',mother_phone='"+mother_phone+"',"+ \
            "mother_phone = '" + mother_phone + "', mother_occupation = '" + mother_occupation + "', " + \
            "phone='"+phone+"', email='"+email+"' WHERE id="+str(id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        mysql.connection.commit()
        flash("Student data updated successfully",'success')
        return redirect("/students")

@app.route("/delete_student", methods=["GET","POST"])
def delete_student():
    if request.method=="GET":
        if "id" in request.args:
            query = "DELETE from enrollment WHERE id="+str(request.args["id"])
            cur = mysql.connection.cursor()
            cur.execute(query)
            mysql.connection.commit()
            flash("Student deleted","danger")
            return redirect("/students")


@app.route("/teachers_day",methods=["GET","POST"])
def teachers_day():
    if request.method=="GET":
        if "completed" in request.args:
            flash("Way to go! Your entry was submitted successfully", 'success')
        return render_template("teacher_day.html")
    else:
        passcode = request.form['passcode']
        if passcode.strip().upper()=="ABWRLD":
            return render_template("teachers_day_submission.html")
        else:
            flash("Incorrect passcode", "danger")
            return redirect("/teachers_day")

@app.route("/teachers_day_submission",methods=["POST"])
def teachers_day_submission():
    if request.method=="POST":
        name = request.form['name']
        standard = request.form['standard']
        branch = request.form['branch']
        cur = mysql.connection.cursor()
        insertQuery = "INSERT into teachers_day(name, standard, branch) values('"+name+"','"+standard+"','"+branch+"')"
        cur.execute(insertQuery)
        mysql.connection.commit()


        getLastEntry = "SELECT id from teachers_day order by id DESC LIMIT 1"
        cur.execute(getLastEntry)
        link_id = cur.fetchone()[0]

        return str(link_id)

@app.route("/teachers_day_upload", methods=['POST'])
def teachers_day_upload():
    if request.method == "POST":
        file = request.files["file"]
        file_name = request.form['file_name']
        file_type = request.form['file_type']
        print(file_name)
        print(file_type)
        link_id = request.form['link_id']
        chunk_number = request.form['chunk_number']

        if chunk_number==0:
            cur = mysql.connection.cursor()
            query = "INSERT into files (filename, type, link_id) values ('"+file_name+"','"+file_type+"',"+str(link_id)+")"
            cur.execute(query)
            print(query)
            mysql.connection.commit()

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
        else:
            with open(os.path.join(app.config['UPLOAD_FOLDER'], file_name), 'ab') as f:
                f.seek(int(request.form['byteoffset']))
                f.write(file.stream.read())

                if str(f.tell()//(1024*1024)) >= request.form['total_chunks']:
                    print("Total", str(f.tell()//(1024*1024)))
                    return "Complete"

                print(f.tell()//(1024*1024))
                return str(f.tell()//(1024*1024))

@app.route("/new_user", methods=["GET","POST"])
def new_user():
    if request.method=="GET":
        return render_template("new_user.html")
    else:
        fullname = request.form['fullname']
        email = request.form['email']
        phone = request.form['phone']
        role = request.form['role']
        cur = mysql.connection.cursor()
        query = "INSERT into users (fullname, email, phone, role) values('"+fullname+"','"+email+"','"+phone+"','"+role+"')"
        cur.execute(query)
        mysql.connection.commit()
        flash("User created successfully","success")
        return redirect("/users")

@app.route("/users", methods=["GET","POST"])
def users():
    if request.method=="GET":
        cur = mysql.connection.cursor()
        query = "SELECT * from users"
        cur.execute(query)
        result = cur.fetchall()
        records = []
        for i in result:
            records.append({
                "id": i[0],
                "fullname": i[1],
                "email": i[2],
                "phone": i[3],
                "role": i[4]
            })
        return render_template("users.html", data=records)

@app.route("/edit_user", methods=["GET","POST"])
def edit_user():
    if request.method=="GET":
        cur = mysql.connection.cursor()
        id = request.args['id']
        query = "SELECT * from users where id="+str(id)
        cur.execute(query)
        result = cur.fetchone()
        data = {"id": result[0],"fullname": result[1],"email": result[2],"phone": result[3],"role": result[4]}
        all_slots = {}
        faculty_slots = []
        if data['role']=='Faculty':
            query = 'SELECT * from slots WHERE recurring=1'
            cur.execute(query)
            records = cur.fetchall()
            for i in records:
                all_slots[i[0]] = i[2] + " " + i[3]
            facultySlots = "SELECT slot_id from faculty_slots WHERE faculty_id="+id
            cur.execute(facultySlots)
            records = cur.fetchall()
            for i in records:
                slotQuery = 'SELECT * from slots WHERE recurring=1 AND id='+str(i[0])
                cur.execute(slotQuery)
                # return slotQuery
                result = cur.fetchone()
                faculty_slots.append(result[2] + " " + result[3])

        return render_template("edit_user.html", data=data, slots=all_slots, faculty_slots=faculty_slots)
    else:
        id = request.form['id']
        fullname = request.form['fullname']
        email = request.form['email']
        phone = request.form['phone']
        role = request.form['role']
        cur = mysql.connection.cursor()
        query = "UPDATE users set fullname='"+fullname+"',email='"+email+"',phone='"+phone+"',role='"+role+"' WHERE id="+id
        cur.execute(query)
        if role=="Faculty":
            # Delete all slots first
            deleteSlots = "DELETE from faculty_slots WHERE faculty_id="+id
            cur.execute(deleteSlots)
            slots = request.form.getlist("slots[]")
            for i in slots:
                slotQuery = "INSERT into faculty_slots(faculty_id, slot_id) values(" + id + "," + str(i) + ")"
                cur.execute(slotQuery)
        mysql.connection.commit()
        flash("User updated successfully", "success")
        return redirect("/users")

@app.route("/delete_user", methods=["GET","POST"])
def delete_user():
    if request.method=="GET":
        cur = mysql.connection.cursor()
        id = request.args['id']
        query = "DELETE from users WHERE id="+id
        cur.execute(query)
        mysql.connection.commit()
        flash("User deleted",'danger')
        return redirect('/users')

# Mobile app APIs
@app.route("/api/API_login", methods=["GET","POST"])
def API_login():
    if request.method == "POST":
        id = request.form["id"]
        password = request.form['password']
        password = hashlib.sha3_256(password.encode()).hexdigest()

        cur = mysql.connection.cursor()

        studentQuery = "SELECT id, name, age, instrument, course from enrollment where phone='"+id+"' AND password='"+password+"'"
        cur.execute(studentQuery)
        result = cur.fetchone()
        if result is not None:
            return jsonify({
                "message": "success",
                "id": result[0],
                "role": "Student",
                "name": result[1],
                "age": result[2],
                "instrument": result[3],
                "course": result[4]
            })


        userQuery = "SELECT id, fullname, role from users where phone='"+id+"' AND password='"+password+"'"
        cur.execute(userQuery)
        result = cur.fetchone()
        if result is not None:
            return jsonify({
                "message": "success",
                "id": result[0],
                "role": result[2],
                "name": result[1],
            })

        guestQuery = "SELECT id, name, enquiry_for from leads where phone='" + id + "' AND password='" + password + "'"
        cur.execute(guestQuery)
        result = cur.fetchone()
        if result is not None:
            return jsonify({
                "message": "success",
                "id": result[0],
                "role": "Guest",
                "name": result[1],
                "enquiry_for": result[2],
            })
        return jsonify({
            "message": "failure",
        })


@app.route("/API_forgot_password", methods=['POST'])
def API_forgot_password():
    phone = request.form['phone']
    email = request.form['email']
    cur = mysql.connection.cursor()
    studentQuery = "SELECT id from enrollment where phone='" + phone + "' AND email='" + email + "'"
    cur.execute(studentQuery)
    result = cur.fetchone()
    if result is not None:
        return jsonify({"message": "success", "found_in":'enrollment', "id": result[0]})
    facultyQuery = "SELECT id from users where phone='" + phone + "' AND email='" + email + "'"
    cur.execute(facultyQuery)
    result = cur.fetchone()
    if result is not None:
        return jsonify({"message": "success","found_in":'users', "id": result[0]})
    guestQuery = "SELECT id from leads where phone='" + phone + "' AND email='" + email + "'"
    cur.execute(guestQuery)
    result = cur.fetchone()
    if result is not None:
        return jsonify({"message": "success","found_in":'leads', "id": result[0]})
    return jsonify({"message": "success","found_in": ""})


@app.route("/API_reset_password", methods=['GET', 'POST'])
def API_reset_password():
    if request.method=="POST":
        id = request.form['id']
        password = request.form['password']
        role = request.form['role']
        cur = mysql.connection.cursor()
        password = hashlib.sha3_256(password.encode()).hexdigest()
        query = "UPDATE "+role+" SET password='"+password+"' WHERE id="+id
        cur.execute(query)
        mysql.connection.commit()
        return jsonify({"message":"success"})

@app.route("/API_get_class_details", methods=["GET"])
def API_get_next_class():
    if request.method == "GET":
        id = request.args['id']
        query = "SELECT slot_id from student_slots WHERE student_id="+str(id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        result = cur.fetchall()
        slots = []
        sorted_slots = []
        for i in result:
            slot_time_query = "SELECT day, time from slots WHERE id="+str(i[0])
            cur.execute(slot_time_query)
            for j in cur.fetchall():
               slots.append(j[0]+" "+j[1])
        b = sorted((time.strptime(d, "%A %I:%M %p") for d in slots))
        for i in b:
            t = ((time.strftime("%A %I:%M %p", i)))
            sorted_slots.append(t)
        return jsonify({"slots": sorted_slots[::-1]})

@app.route("/API_get_profile_picture_url", methods=["GET"])
def API_get_profile_picture_url():
    if request.method == "GET":
        id  = request.args['id']
        query = "SELECT filename from files WHERE link_id="+str(id)
        cur  = mysql.connection.cursor()
        cur.execute(query)
        image = ''
        fileQuery = "SELECT filename from files WHERE type='profile' AND link_id=" + id
        cur.execute(fileQuery)
        result = cur.fetchone()

        if result != None:
            image = result[0]

        return jsonify({"image": "https://abworldmusic.in/MySite/images/"+str(image)})

@app.route("/API_update_profile_picture_url", methods=["POST"])
def API_update_profile_picture_url():
    if request.method=="POST":
        cur = mysql.connection.cursor()
        id = request.form['id']
        image = request.files['image']
        if image.filename.strip() != "":
                query = "UPDATE files SET filename='"+image.filename.strip()+"' WHERE type='profile' and link_id="+str(id)
                print(query)
                cur.execute(query)
                mysql.connection.commit()

                image.save(os.path.join(app.config['UPLOAD_FOLDER'], image.filename))
        return "Updated"

@app.route("/API_community_post", methods=["POST"])
def API_community_post():
    if request.method=="POST":
        user_id = request.form['user_id']
        caption = request.form['caption']
        mydate = datetime.datetime.now()
        date = mydate.strftime("%d/%m/%Y %I:%M %p")
        query = "INSERT into community (user_id, caption, date) values("+str(user_id)+",'"+caption.replace("'","''")+"','"+date+"')"
        cur = mysql.connection.cursor()
        cur.execute(query)
        mysql.connection.commit()

        getLastPost = "SELECT id from community order by id DESC LIMIT 1"
        cur.execute(getLastPost)
        link_id = cur.fetchone()[0]

        if "attachment" in request.files:
            f = request.files['attachment']
            if f.filename.strip() != "":
                query = "INSERT into files (filename, type, link_id) values ('" + f.filename + "','community'," + str(link_id) + ")"
                cur.execute(query)
                mysql.connection.commit()

                f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))

        return jsonify({"message":"Post uploaded successfully"})

@app.route("/API_community_get", methods=['GET'])
def API_community_get():
    if request.method == "GET":
        user_id = request.args['user_id']
        if "id" in request.args:
            id = request.args['id']
            query = "SELECT * FROM community WHERE id < "+str(id)+" order by id DESC LIMIT 5"
        else:
            query = "SELECT * FROM community order by id DESC LIMIT 5"
        cur = mysql.connection.cursor()
        cur.execute(query)
        results = cur.fetchall()
        all_posts = []
        if len(results)==0:
            return jsonify({"message":"No more post"})
        for i in results:
            record = {"id": i[0], 'user_id': i[1], 'caption': i[2], 'date': i[3]}
            userQuery = "SELECT name from enrollment WHERE id="+str(record['user_id'])
            cur.execute(userQuery)
            res = cur.fetchone()
            if res is not None:
                record['username'] = res[0]
            fileQuery = "SELECT filename from files WHERE type='community' AND link_id=" + str(record['id'])
            cur.execute(fileQuery)
            res = cur.fetchone()
            if res is not None:
                findQuery = "SELECT COUNT(*) from community_likes WHERE post_id=" + str(
                    record['id'])
                cur.execute(findQuery)
                likesRes =  cur.fetchone()
                if likesRes is None:
                    record['likes'] = "0"
                else:
                    record['likes'] = str(likesRes[0])

                findSelfQuery = "SELECT COUNT(*) from community_likes WHERE user_id="+ str(user_id) +" AND post_id=" + str(
                    record['id'])
                cur.execute(findSelfQuery)
                likesRes = cur.fetchone()
                if int(likesRes[0]) == 0:
                    record['likedBySelf'] = "0"
                else:
                    record['likedBySelf'] = "1"

                record['filename'] = res[0]
                all_posts.append(record)

        return jsonify(all_posts)

@app.route("/API_like_post", methods=['POST'])
def API_like_post():
    if request.method=="POST":
        post_id = request.form['post_id']
        user_id = request.form['user_id']
        mydate = datetime.datetime.now()
        date = mydate.strftime("%d/%m/%Y %I:%M %p")

        cur = mysql.connection.cursor()
        findQuery = "SELECT COUNT(*) from community_likes WHERE post_id="+str(post_id)+" AND user_id="+str(user_id)
        cur.execute(findQuery)
        res  = cur.fetchone()
        if int(res[0]) == 0:

            query = "INSERT into community_likes (post_id, user_id, date) values("+str(post_id)+","+str(user_id)+",'"+date+"')"
            cur.execute(query)
            mysql.connection.commit()

            return jsonify({"like": "+1"})

        else:

            query = "DELETE from community_likes WHERE post_id="+str(post_id)+" AND user_id="+str(user_id)
            cur.execute(query)
            mysql.connection.commit()

            return jsonify({"like": "-1"})


@app.route("/API_confirm_arrival", methods=['POST'])
def confirm_arrival():
    if request.method == "POST":
        userid = request.form['user_id']
        type = request.form['type']
        mydate = datetime.datetime.now()
        time = mydate.strftime("%A %d/%m/%Y %H:%M %p")
        cur = mysql.connection.cursor()
        query = "INSERT into arrival_logs(user_id, type, time) values("+str(userid)+",'"+type+"','"+time+"')"
        cur.execute(query)
        mysql.connection.commit()
        return jsonify({"message": "confirmed"})

@app.route("/API_get_slots_for_faculty", methods=['POST'])
def API_get_slots_for_faculty():
    if request.method == "POST":
        userid = request.form['user_id']
        day = request.form['day']
        slotsQuery = "SELECT slot_id from faculty_slots WHERE faculty_id="+str(userid)
        cur = mysql.connection.cursor()
        cur.execute(slotsQuery)
        records = cur.fetchall()
        faculty_slots = {}
        for i in records:
            slotQuery = 'SELECT * from slots WHERE recurring=1 AND id=' + str(i[0])
            cur.execute(slotQuery)
            result = cur.fetchone()
            if day in result[2]:
                faculty_slots[i[0]] = result[2] + " " + result[3]
        if len(faculty_slots)==0:
            return jsonify({"slots":"No slots today"})
        else:
            return jsonify({'slots': faculty_slots})


@app.route("/API_get_student_list", methods=['GET'])
def API_get_student_list():
    class_id = request.args['class_id']
    cur = mysql.connection.cursor()
    query = "SELECT student_id from student_slots WHERE slot_id="+str(class_id)
    cur.execute(query)
    records = cur.fetchall()
    mydate = datetime.datetime.now()
    mydate = mydate.strftime("%d/%m/%Y")
    all_students = {}
    class_completed = False
    for i in records:
        studentQuery = "SELECT name from enrollment WHERE id="+str(i[0])
        cur.execute(studentQuery)
        result = cur.fetchone()
        if result is not None:
            attendance = "SELECT id, status, reason from attendance WHERE slot_id="+str(class_id)+" AND student_id="+str(i[0])+" AND date_and_day LIKE '%"+mydate+"%'"
            cur.execute(attendance)
            res = cur.fetchone()
            if res is not None:
                class_completed = True
                all_students[i[0]] = [result[0],res[1],res[2]]
            else:
                all_students[i[0]] = [result[0], 'Absent',""]

    return jsonify({"students": all_students, "class_completed": class_completed})

@app.route("/API_get_attendance", methods=['GET'])
def API_get_attendance():
    if request.method=="GET":
        id = request.args['id']
        cur = mysql.connection.cursor()
        query = "SELECT date_and_day, faculty_id, status, reason from attendance WHERE student_id="+str(id)
        cur.execute(query)
        res = cur.fetchall()
        response = []
        if res is not None:
            for i in res:
                facultyQuery = "SELECT fullname from users where id="+str(i[1])
                cur.execute(facultyQuery)
                facRes = cur.fetchone()
                response.append({
                    "date_and_day": i[0],
                    "faculty": facRes[0],
                    "status": i[2],
                    "reason": i[3]
                })
        return jsonify(response)




@app.route("/API_mark_attendance", methods=['GET','POST'])
def API_mark_attendance():
    if request.method=="POST":
        student_id = request.form['student_id']
        faculty_id = request.form['faculty_id']
        slot_id = request.form['slot_id']
        date_and_day = request.form['date_and_day']
        cur = mysql.connection.cursor()
        check = "SELECT id from attendance WHERE student_id="+str(student_id)+" AND date_and_day='"+str(date_and_day)+"'"
        cur.execute(check)
        res = cur.fetchone()
        if res is not None:
            query = "UPDATE attendance set status='Absent' WHERE id="+str(res[0])
            cur.execute(query)
            mysql.connection.commit()
            return jsonify({"message": "success","marked":"Absent"})
        else:
            query = "INSERT into attendance (slot_id, date_and_day, student_id, faculty_id) values("+ \
                    str(slot_id)+ ",'" +str(date_and_day)+ "'," +str(student_id)+ ","+str(faculty_id)+")"
            cur.execute(query)
            mysql.connection.commit()
            return jsonify({"message":"success", "marked":"Present"})

@app.route("/API_fees", methods=['POST'])
def API_fees():
    if request.method=="POST":
        id = request.form['id']
        cur = mysql.connection.cursor()
        query = "SELECT date, product_name, product_price from sales where student_id="+id
        cur.execute(query)
        res = cur.fetchall()
        records = []
        for i in res:
            records.append({"name": i[1], "date": i[0], "price": i[2]})
        return jsonify(records)

@app.route("/API_promote_to_next_lesson", methods=['GET','POST'])
def API_promote_to_next_lesson():
    if request.method=="POST":
        id = request.form['student_id']
        current_lesson = "SELECT lesson_id from progress WHERE student_id="+str(id)
        cur = mysql.connection.cursor()
        cur.execute(current_lesson)
        res = cur.fetchone()
        current_lesson_id = str(res[0])
        next_lesson = "SELECT id from lessons WHERE id>"+str(current_lesson_id)+" LIMIT 1"
        cur.execute(next_lesson)
        res = cur.fetchone()
        if res is not None:
            next_lesson_id = str(res[0])
            update_lessons = "UPDATE progress SET lesson_id="+str(next_lesson_id)+" WHERE student_id="+str(id)
            cur.execute(update_lessons)
            mysql.connection.commit()
            return jsonify({"message":"Student lesson updated successfully"})
        else:
            return jsonify({"message":"Student already on last lesson"})

@app.route("/API_class_actions", methods=['GET','POST'])
def API_class_actions():
    if request.method=="POST":
        student_id = request.form['student_id']
        faculty_id = request.form['faculty_id']
        slot_id = request.form['slot_id']
        date_and_day = request.form['date_and_day']
        status = request.form['status']
        attendance = request.form['attendance']
        reason = request.form['reason']
        cur = mysql.connection.cursor()
        if attendance=="Present":
            query = "INSERT into attendance (slot_id, date_and_day, student_id, faculty_id, status) values(" + \
                    str(slot_id) + ",'" + str(date_and_day) + "'," + str(student_id) + "," + str(faculty_id) + ",'Present')"
            cur.execute(query)
        else:
            query = "INSERT into attendance (slot_id, date_and_day, student_id, faculty_id, status, reason) values(" + \
                    str(slot_id) + ",'" + str(date_and_day) + "'," + str(student_id) + "," + str(
                faculty_id) + ",'Absent','"+reason+"')"
            cur.execute(query)
        if status == "Promote":
            current_lesson = "SELECT lesson_id from progress WHERE student_id=" + str(student_id)
            cur.execute(current_lesson)
            res = cur.fetchone()
            current_lesson_id = str(res[0])
            next_lesson = "SELECT id from lessons WHERE id>" + str(current_lesson_id) + " LIMIT 1"
            cur.execute(next_lesson)
            res = cur.fetchone()
            if res is not None:
                next_lesson_id = str(res[0])
                update_lessons = "UPDATE progress SET lesson_id=" + str(next_lesson_id) + " WHERE student_id=" + str(student_id)
                cur.execute(update_lessons)
        mysql.connection.commit()
        return jsonify({"message": "success"})

@app.route("/API_studio_sessions", methods=['GET'])
def API_studio_sessions():
    if request.method=='GET':
        id = request.args['id']
        query = "SELECT song, details, scheduled_on, completed from studio WHERE student_id="+str(id)+" ORDER by id"
        cur = mysql.connection.cursor()
        cur.execute(query)
        records = []
        res = cur.fetchall()
        if res is not None:
            for i in res:
                records.append({"song": i[0],"details": i[1], "scheduled": i[2], "completed": i[3]})
        return jsonify(records)

@app.route("/API_current_lesson", methods=['GET'])
def API_current_lesson():
    id = request.args['id']
    current_lesson = "SELECT lesson_id from progress WHERE student_id=" + str(id)
    cur = mysql.connection.cursor()
    cur.execute(current_lesson)
    res = cur.fetchone()
    if res is not None:
        lesson_id = res[0]
        lessonQuery = "SELECT title, description, image, level from lessons WHERE id="+str(lesson_id)
        cur.execute(lessonQuery)
        res = cur.fetchone()
        if res is not None:
            return jsonify({"title": res[0], "description": res[1], "image": res[2], "level": res[3]})
        else:
            return jsonify({})
    else:
        return jsonify({})


@app.route("/API_new_enquiry", methods=['POST'])
def new_enquiry():
    name = request.form["name"]
    phone = request.form["phone"]
    course = request.form["course"]
    instrument = request.form['instrument']
    email = request.form['email']
    goal = request.form["goal"]

    cur = mysql.connection.cursor()
    checkQuery = "SELECT COUNT(id), id, closed from leads where phone='"+phone+"'"
    cur.execute(checkQuery)
    count = cur.fetchone()
    if count[0]!=0:
        if bool(count[2]):
            return jsonify({"message": "success", "type": "closed", "id": count[1], "queue_no": count[0]})
        else:
            return jsonify({"message": "success", "type": "old", "id": count[1], "queue_no": count[0]})


    query  = "INSERT into leads (name, phone, email, enquiry_for, note) values('"+name+"','"+phone+"','"+email+"','"+instrument+" "+course+"','"+goal+"')"
    cur.execute(query)
    mysql.connection.commit()
    id = cur.lastrowid
    waitingListQuery = "SELECT COUNT(id) from leads where closed=0"
    cur.execute(waitingListQuery)
    count = cur.fetchone()
    if count[0]!=0:
        password = "WOMSTU"+str(id)
        password = hashlib.sha3_256(password.encode()).hexdigest()
        updatePw = "Update leads SET password='"+password+"' WHERE id="+str(id)
        cur.execute(updatePw)
        mysql.connection.commit()
        return jsonify({"message": "success","type": "new", "id": id, "queue_no": count[0]})
    else:
        return jsonify({"message": "success"})

if __name__ == '__main__':
    app.run(debug=True)
