from flask import Flask, render_template, redirect, request, session, flash, jsonify, send_from_directory
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL
import datetime
import time
from time import mktime
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
        cur = mysql.connection.cursor()
        query = "SELECT * FROM users WHERE name='" + username + "' OR email='" + username + "' AND organization_id=2"
        cur.execute(query)
        records = cur.fetchall()
        if len(records) > 0:
            if records[0][4] == password:
                session['username'] = records[0][2]
                session['logged_in'] = True
                flash("Logged in successfully", "success")
                return redirect('/dashboard')
        flash("Incorrect credentials", "danger")
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
            phone = ""
            fatherName = request.form['fatherName']
            fatherPhone = request.form['fatherPhone']
            fatherEmail = request.form['fatherEmail']
            fatherOccupation = request.form['fatheroccupation']
            motherName = request.form['motherName']
            motherPhone = request.form['motherPhone']
            motherEmail = request.form['motherEmail']
            motherOccupation = request.form['motheroccupation']
            type = 'Student'
            email = ''
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
        mysql.connection.commit()
        flash("Fee paid", "success")
        return redirect("/payment")


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
    if month_number == 12:
        month_number = 0

    feeMonth = time.strptime(str(month_number + 1), "%m")
    feeMonth = time.strftime("%B", feeMonth)
    if last_fee_paid == feeMonth:
        status = "Paid"
    else:
        status = "Due"

    return jsonify({"name": name, "status": status, "month": feeMonth})


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
        query = "SELECT id, name, gender, instrument, course from enrollment"
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
            return render_template("student_dashboard.html", data=data)


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


# Mobile app APIs

@app.route("/API_login", methods=["POST"])
def API_login():
    if request.method == "POST":
        studentID = request.form["student_id"]
        query = "SELECT name, age, instrument, course from enrollment WHERE id="+str(studentID)
        cur = mysql.connection.cursor()
        cur.execute(query)
        result = cur.fetchone()
        if result is not None:
            return jsonify({
                "message": "Login successful",
                "id": studentID,
                "name": result[0],
                "age": result[1],
                "instrument": result[2],
                "course": result[3]
            })
        else:
            return jsonify({
                "message": "Login failed",
            })
@app.route("/API_get_next_class", methods=["POST"])
def API_get_next_class():
    if request.method == "POST":
        id = request.form['student_id']
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


if __name__ == '__main__':
    app.run(debug=True)
