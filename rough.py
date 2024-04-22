from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Shraddha@2004",
    database="food_db"
)
mycursor = mydb.cursor(buffered=True)
@app.route("/home")
def home():
    return render_template("index.html")
@app.route("/")
def Login():
    return render_template("index.html")

@app.route("/About")
def About():
    return render_template("About.html")

@app.route("/Contact")
def Contact():
    return render_template("Contact.html")


@app.route("/register")
def register():
    return render_template("login_register.html")

#login page
@app.route("/")
def index():
    return render_template('index.html')
donor_id=0;
ngo_id=0
admin_username=""
ngo_username=""
donor_username=""
@app.route("/load_login")
def load_login():
    return render_template('login_register.html')

@app.route("/load_login",methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    mycursor.execute("select username,password from admin")
    flag = False
    global ngo_username,admin_username,donor_username
    for x in mycursor:
        if ((x[0] == username) and (x[1] == password)):
            flag = True
            admin_username=x[0]
            break

    if (flag == True):
        print("Login Done")
        return render_template('admin_dashboard.html',val=1)
    else:
        mycursor.execute("select donor_id,username,password from donor")
        global donor_id;
        for x in mycursor:
            if ((x[1] == username) and (x[2] == password)):
                flag = True
                donor_id=x[0]
                donor_username=x[1]
                break
        if(flag==True):
            return render_template('donor_dashboard.html',donor_username=donor_username,success=True)
        else:
            mycursor.execute("select ngo_id,username,password from ngo")
            global ngo_id
            for x in mycursor:
                if ((x[1] == username) and (x[2] == password)):
                    flag = True
                    ngo_id=x[0]
                    ngo_username=x[1]
                    print(ngo_id)
                    break
            if(flag==True):
                return render_template('ngo_dashboard.html',ngo_username=ngo_username,val=1)

    return render_template('login_register.html',error=1)



#Admin Page
#@app.route("/donor")
#def view_donor():
 #   global mycursor
  #  list1 = []
   # mycursor.execute("select donor_id,name,phno,colony,city,username,password from Donor")
    #myresult = mycursor.fetchall()

#    for x in myresult:
 #       list1.append(x)
  #  return render_template('admin_donor_details.html',list1=list1)

#Admin Page
@app.route("/donor")
def view_donor():
    global mycursor
    list1 = []
    mycursor.callproc("donor_details")#Procedure Call
    for result in mycursor.stored_results():
        rows = result.fetchall()
        for row in rows:
            list1.append(row)
    return render_template('admin_donor_details.html',list1=list1)

#Food_Item
#@app.route("/Food")
#def Food():
 #   global mycursor
  #  list1 = []
   # mycursor.execute("select food_id,foodtype,quantity from fooditem")
    #myresult = mycursor.fetchall()

    #for x in myresult:
     #   list1.append(x)
    #return render_template('admin_food_details.html',list1=list1)

#Food_Item
@app.route("/Food")
def Food():
    global mycursor
    list1 = []
    mycursor.callproc("food_details")#Procedure Call
    for result in mycursor.stored_results():
        rows = result.fetchall()
        for row in rows:
            list1.append(row)
    return render_template('admin_food_details.html',list1=list1)

#Admin_NGO
#@app.route("/NGO")
#def receive():
 #   global mycursor
  #  list1 = []
   # mycursor.execute("select ngo_id,name,phno,status,task,username,password from NGO")
   # myresult = mycursor.fetchall()

    #for x in myresult:
     #   list1.append(x)
    #return render_template('admin_ngo_details.html',list1=list1)

#Admin_NGO
@app.route("/NGO")
def receive():
    global mycursor
    list1 = []
    mycursor.callproc("ngo_details")#Procedure Call
    for result in mycursor.stored_results():
        rows = result.fetchall()
        for row in rows:
            list1.append(row)
    return render_template('admin_ngo_details.html',list1=list1)
#Admin_Needy
#@app.route("/Needy")
#def view_needy():
 #   global mycursor
  #  list1 = []
   # mycursor.execute("select needy_id,name,phno,income,colony,city,username,password from Needy_People")
    #myresult = mycursor.fetchall()


    #for x in myresult:
     #   list1.append(x)
    #return render_template('admin_needy_details.html',list1=list1)

#Admin_Needy
@app.route("/Needy")
def view_needy():
    global mycursor
    list1 = []
    mycursor.callproc("needy_details") #Procedure Call
    for result in mycursor.stored_results():
        rows = result.fetchall()
        for row in rows:
            list1.append(row)
    return render_template('admin_needy_details.html',list1=list1)

@app.route("/admin_ngo_count")
def admin_ngo_count():
    global mycursor
    list1 = []
    mycursor.execute("select name from donor_ngo_view")
    myresult = mycursor.fetchall()

    for x in myresult:
        list1.append(x)
    return render_template('admin_ngo_count.html',list1=list1)


@app.route("/check_ngo_count",methods=['POST'])
def check_ngo_count():
    print("ngo count")
    global mycursor
    ngoname=request.form.get('ngo_name')
    print(ngoname)
    list1=[]
    sql="select ngo_id from ngo where name=%s"
    mycursor.execute(sql,(ngoname,))
    myresult=mycursor.fetchall()
    ngo_id = 0;
    for x in myresult:
        ngo_id = x[0]
    print(ngo_id)
    sql = "select distinct food_id from receive where ngo_id=%s"
    mycursor.execute(sql, (ngo_id,))
    myresult = mycursor.fetchall()
    food_id, donor_id = [], [];
    for x in myresult:
        food_id.append(x[0])
    print(food_id)
    for i in food_id:
        sql = "SELECT DISTINCT donor_id FROM donation WHERE food_id = %s"
        mycursor.execute(sql, (i,))
        myresult = mycursor.fetchall()
        for x in myresult:
            donor_id.append(x[0])
    print(donor_id)
    dname = []
    phno = []
    colony=[]
    city=[]
    list1=[]
    for i in donor_id:
        sql = "SELECT name,phno,colony,city FROM donor WHERE donor_id = %s"
        mycursor.execute(sql, (i,))
        myresult = mycursor.fetchall()

        # Extract donor_ids from the query results and append to donor_ids list
        for x in myresult:
            dname.append(x[0])
            phno.append(x[1])
            colony.append(x[2])
            city.append(x[3])
            list1.append(x)
    print(dname, phno)
    cnt= len(list1)
    #return render_template("show_details_donor.html",dname=dname,phno=phno,colony=colony,city=city)
    return render_template("show_details_donor.html",list1=list1,cnt=cnt)


@app.route("/register_ngo")
def register_ngo():
    return render_template('ngo_register.html')

@app.route("/register_needy")
def register_needy():
    return render_template('needy_register.html')

@app.route("/register_donor")
def register_donor():
    print("Donor Register form")
    return render_template("donor_register.html")
#Sign up page donor

#@app.route("/donor_insert",methods=['POST'])
#def donor_insert():
 #   print("Donor Register form")
  #  name = request.form.get('dname')
   # phno = request.form.get('phno')
    #password = request.form.get('password')
   # colony = request.form.get('colony')
   # city = request.form.get('city')
   # username = request.form.get('username')
        # Add other form fields as needed (e.g., email)

    #mycursor = mydb.cursor()
    #query="INSERT INTO donor (name,phno,password,colony,city,username) VALUES (%s, %s, %s,%s,%s,%s);"
    #val=(name,phno,password,colony,city,username)
    #count=mycursor.execute(query,val)

    #query="call insert_donor(%s, %s, %s,%s,%s,%s);"
    #val=(name,phno,password,colony,city,username)
    #count=mycursor.execute(query,val)
   # mydb.commit()
   # print("Signup Successful!")
    #return render_template('login_register.html')
    #return redirect(url_for('load_login'))

#function
@app.route("/donor_insert",methods=['POST'])
def donor_insert():
    dname=request.form.get('dname')
    phno=request.form.get('phno')
    city=request.form.get('city')
    colony=request.form.get('colony')
    uname=request.form.get('uname')
    psw=request.form.get('psw');
    val=(dname,phno,colony,city,uname,psw)
    print(val)
    mycursor.execute("SELECT insert_donor_details1(%s,%s,%s,%s,%s,%s)", val)

    success = mycursor.fetchone()[0]

    if success == 1:
        print("Data inserted successfully!")
    else:
        print("Failed to insert data.")
    mydb.commit()
    #return render_template("load_login.html")
    return redirect(url_for('load_login'))

#Sign up page ngo

#@app.route("/ngo_insert",methods=['POST'])
#def ngo_insert():
 #   print("ngo Register form")
  #  name = request.form.get('nname')
   # phno = request.form.get('phno')
   # status = request.form.get('status')
   # task = request.form.get('task')
   # username = request.form.get('username')
   # password = request.form.get('password')
        # Add other form fields as needed (e.g., email)

    #mycursor = mydb.cursor()
    #query="INSERT INTO ngo (name,phno,status,task,username,password) VALUES (%s, %s, %s,%s,%s,%s);"
    #val=(name,phno,status,task,username,password)
    #count=mycursor.execute(query,val)

    #mydb.commit()
    ##print("Signup Successful!")
    #return render_template('login_register.html')
    #return redirect(url_for('load_login'))

@app.route("/ngo_insert",methods=['POST'])
def ngo_insert():
    name=request.form.get('name')
    phno=request.form.get('phno')
    status=request.form.get('status')
    task=request.form.get('task')
    uname = request.form.get('uname')
    pwd=request.form.get('password')

    val=(name,phno,status,task,uname,pwd)
    print(val)
    mycursor.execute("SELECT insert_ngo_details(%s,%s,%s,%s,%s,%s)", val) # function
    success = mycursor.fetchone()[0]

    if success == 1:
        print("Data inserted successfully!")
    else:
        print("Failed to insert data.")
    mydb.commit()
    #return render_template("load_login.html")
    return redirect(url_for('load_login'))

#sign up form for needy people
@app.route("/needy_people_insert",methods=['POST'])
def needy_people_insert():
    print("Needy_people Register form")
    name = request.form.get('needname')
    phno = request.form.get('phno')
    city = request.form.get('city')
    colony = request.form.get('colony')
    income = request.form.get('income')
        # Add other form fields as needed (e.g., email)

    mycursor = mydb.cursor()
    query="INSERT INTO needy_people (name,phno,city,colony,income) VALUES (%s, %s, %s,%s,%s);"
    val=(name,phno,city,colony,income)
    count=mycursor.execute(query,val)

    mydb.commit()
    print("Signup Successful!")
   # return render_template('login_register.html')
    return redirect(url_for('load_login'))




#Donor
#@app.route("/donor_ngo")
#def donor_ngo():
 #   global mycursor
  #  list1 = []
   # mycursor.execute("select ngo_id,name,phno,status,task from NGO")
   # myresult = mycursor.fetchall()

   # for x in myresult:
    #    list1.append(x)
    #return render_template('donor_ngo.html',list1=list1)

#view
#Donor
@app.route("/donor_ngo")
def donor_ngo():
    global mycursor
    list1 = []
    mycursor.execute("select * from donor_ngo_view")
    myresult = mycursor.fetchall()

    for x in myresult:
        list1.append(x)
    return render_template('donor_ngo.html',list1=list1)

#@app.route("/donate")
#def donate():
 #   global mycursor
  #  list1 = []
   # mycursor.execute("select name from NGO")
   # myresult = mycursor.fetchall()

    #for x in myresult:
     #   list1.append(x)
    #return render_template('donate.html',list1=list1)

#view
@app.route("/donate")
def donate():
    global mycursor
    list1 = []
    mycursor.execute("select name from donor_ngo_view")
    myresult = mycursor.fetchall()

    for x in myresult:
        list1.append(x)
    return render_template('donate.html',list1=list1)


''''@app.route("/donate",methods=['POST'])
def donate_info():
    global mycursor,donor_id,donor_username;
    print(donor_id)
    type = request.form['type']
    quantity = request.form['quantity']
    ngo_name=request.form['ngo_name']
    print(ngo_name)
    print(type,quantity)
    sql = "INSERT INTO fooditem (foodtype,quantity) VALUES (%s,%s)"
    val = (type,quantity)
    mycursor.execute(sql, val)
    mycursor.execute("select food_id from fooditem order by food_id desc limit 1")
    for x in mycursor:
        food_id=x[0]
        print(x)

    sql = "INSERT INTO Donation (food_id,donor_id) VALUES (%s,%s)"
    val = (food_id,donor_id);
    print(food_id,donor_id)
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")
    return render_template('donor_dashboard.html')'''

@app.route("/donate",methods=['POST'])
def donate_info():
    global mycursor,donor_id,donor_username;
    print(donor_id)
    type = request.form['type']
    quantity = request.form['quantity']
    ngo_name=request.form['ngo_name']
    print(ngo_name)
    print(type,quantity)
    val=(type,quantity,donor_id)
    mycursor.execute("SELECT donate(%s,%s,%s)", val)  # function call

    success = mycursor.fetchone()[0]

    if success == 1:
        print("Data inserted successfully!")
    else:
        print("Failed to insert data.")
    mydb.commit()

    mydb.commit()
    print(mycursor.rowcount, "record inserted.")
    return render_template('donor_dashboard.html')


#donor_history

'''@app.route("/donation_history")
def donation_history():
    global mycursor
    list1 = []
    global donor_id;
    #sql="select name,phno,colony,city from donor where donor_id in(select donor_id from donation where food_id in(select food_id from receive where ngo_id =%s))"
    sql="select foodtype,quantity from fooditem where food_id in(select food_id from donation where donor_id=%s)"
    mycursor.execute(sql,(donor_id,))
    myresult = mycursor.fetchall()

    for x in myresult:
        list1.append(x)
    print(list1)
    return render_template('donar_history.html',list1=list1)'''

@app.route("/donation_history")
def donation_history():
    global mycursor
    list1 = []
    global donor_id;
    mycursor.callproc("donation_history",(donor_id,))  # Procedure Call
    for result in mycursor.stored_results():
        rows = result.fetchall()
        for row in rows:
            list1.append(row)
    return render_template('donor_history.html',list1=list1)
#NGO : View donor
'''@app.route("/ngo_view_donor")
def ngo_view_donor():
    global mycursor
    list1 = []
    global ngo_id;
    sql="select name,phno,colony,city from donor where donor_id in(select donor_id from donation where food_id in(select food_id from receive where ngo_id =%s))"

    mycursor.execute(sql,(ngo_id,))
    myresult = mycursor.fetchall()

    for x in myresult:
        list1.append(x)
    print(list1)
    return render_template('ngo_donor.html',list1=list1)'''

#NGO : View donor
@app.route("/ngo_view_donor")
def ngo_view_donor():
    global mycursor
    list1 = []
    global ngo_id;
    mycursor.callproc("view_donor", (ngo_id,))  # Procedure Call
    for result in mycursor.stored_results():
        rows = result.fetchall()
        for row in rows:
            list1.append(row)
    return render_template('ngo_donor.html',list1=list1)

#NGO
'''@app.route("/receive_donation")
def receive_donation():
    list1 = []
    list2=[]
    try:
        mycursor.execute("SELECT food_id,foodtype from FoodItem where food_id not in(select food_id from receive)")
        myresult = mycursor.fetchall()

        for x in myresult:
            list1.append(x[0])
            list2.append(x[1])
    except mysql.connector.Error as error:
        # Handle MySQL errors
        print("MySQL Error: {}".format(error))

    return render_template('receive_donation.html', list1=list1,list2=list2)'''

#NGO
@app.route("/receive_donation")
def receive_donation():
    list1 = []
    list2=[]

    try:
        mycursor.execute("SELECT food_id,foodtype from FoodItem where food_id not in(select food_id from receive)")
        myresult = mycursor.fetchall()

        for x in myresult:
            list1.append(x[0])
            list2.append(x[1])
    except mysql.connector.Error as error:
        # Handle MySQL errors
        print("MySQL Error: {}".format(error))

    return render_template('receive_donation.html', list1=list1,list2=list2)




'''@app.route("/receive_food",methods=['POST'])
def receive_food():
    global mycursor,ngo_id
    print(ngo_id)
    food_id = int(request.form.get('food_id'))
    print(food_id)
    sql="insert into receive(food_id,ngo_id) values(%s,%s)"
    val=(food_id,ngo_id)
    print(val)
    mycursor.execute(sql,val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")
    return render_template('ngo_dashboard.html')'''

@app.route("/receive_food",methods=['POST'])
def receive_food():
    global mycursor,ngo_id
    print(ngo_id)
    food_id = int(request.form.get('food_id'))
    print(food_id)
    """sql="insert into receive(food_id,ngo_id) values(%s,%s)"
    sql="receive_food"
    val=(food_id,ngo_id)
    print(val)
    mycursor.execute(sql,val)"""
    mycursor.execute("SELECT receive_food(%s,%s)", (food_id,ngo_id))

    success = mycursor.fetchone()[0]

    if success == 1:
        print("Data inserted successfully!")
    else:
        print("Failed to insert data.")

    mydb.commit()
    print(mycursor.rowcount, "record inserted.")
    return render_template('ngo_dashboard.html')


#NGO_History

'''@app.route("/ngo_history")
def ngo_history():
    global mycursor
    list1 = []
    global ngo_id;
    #sql="select name,phno,colony,city from donor where donor_id in(select donor_id from donation where food_id in(select food_id from receive where ngo_id =%s))"
    sql="select foodtype, quantity from fooditem where food_id in (select food_id from receive where ngo_id=%s)"
    mycursor.execute(sql,(ngo_id,))
    myresult = mycursor.fetchall()

    for x in myresult:
        list1.append(x)
    print(list1)
    return render_template('ngo_history.html',list1=list1)'''

#NGO_History

@app.route("/ngo_history")
def ngo_history():
    global mycursor
    list1 = []
    global ngo_id;
    #sql="select name,phno,colony,city from donor where donor_id in(select donor_id from donation where food_id in(select food_id from receive where ngo_id =%s))"
    sql="select foodtype, quantity from fooditem where food_id in (select food_id from receive where ngo_id=%s)"
    mycursor.execute(sql,(ngo_id,))
    myresult = mycursor.fetchall()

    for x in myresult:
        list1.append(x)
    print(list1)
    return render_template('ngo_history.html',list1=list1)


'''@app.route("/ngo_profile")
def ngo_profile():
    global mycursor
    list1 = []
    global ngo_id;
    sql="select name,phno,status,task from ngo where ngo_id=%s"
    mycursor.execute(sql,(ngo_id,))
    myresult = mycursor.fetchall()
    name,status,task="","",""
    phno=""
    for x in myresult:
        name=x[0]
        phno=x[1]
        status=x[2]
        task=x[3]
    print(list1)
    return render_template('ngo_profile.html', name=name,phno=phno,status=status,task=task)'''

@app.route("/ngo_profile")
def ngo_profile():
    global mycursor
    list1 = []
    global ngo_id;
    sql="select name,phno,status,task from ngo where ngo_id=%s"
    mycursor.execute(sql,(ngo_id,))
    myresult = mycursor.fetchall()
    name,status,task="","",""
    phno=""
    for x in myresult:
        name=x[0]
        phno=x[1]
        status=x[2]
        task=x[3]
    print(list1)
    return render_template('ngo_profile.html', name=name,phno=phno,status=status,task=task)


'''@app.route("/update_ngo",methods=['POST'])
def update_ngo():
    global mycursor,donor_username
    list1 = []
    global donor_id;
    name= request.form.get('nname')
    phno = request.form.get('phno')
    status = request.form.get('status')
    task = request.form.get('task')
    print(name,phno,status,task)
    sql="update ngo set name=%s,phno=%s,status=%s,task=%s where ngo_id=%s"
    val=(name,phno,status,task,ngo_id)
    mycursor.execute(sql,val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")
    return render_template('ngo_dashboard.html', ngo_username=ngo_username)
    print(ngo_id)'''

@app.route("/update_ngo",methods=['POST'])
def update_ngo():
    global mycursor,donor_username
    list1 = []
    global donor_id;
    name= request.form.get('nname')
    phno = request.form.get('phno')
    status = request.form.get('status')
    task = request.form.get('task')
    print(name,phno,status,task)
    sql="update ngo set name=%s,phno=%s,status=%s,task=%s where ngo_id=%s"
    val=(name,phno,status,task,ngo_id)
    mycursor.execute(sql,val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")
    return render_template('ngo_dashboard.html', ngo_username=ngo_username)
    print(ngo_id)


'''@app.route("/donor_profile")
def donor_profile():
    global mycursor
    list1 = []
    global donor_id;
    print(donor_id)
    sql="select name,phno,colony,city from donor where donor_id=%s"
    mycursor.execute(sql,(donor_id,))
    myresult = mycursor.fetchall()
    name,colony,city="","",""
    phno=""
    for x in myresult:
        name=x[0]
        phno=x[1]
        colony=x[2]
        city=x[3]
    print(list1)
    return render_template('donor_profile.html', name=name,phno=phno,colony=colony,city=city)'''

@app.route("/donor_profile")
def donor_profile():
    global mycursor
    list1 = []
    global donor_id;
    print(donor_id)
    sql="select name,phno,colony,city from donor where donor_id=%s"
    mycursor.execute(sql,(donor_id,))
    myresult = mycursor.fetchall()
    name,colony,city="","",""
    phno=""
    for x in myresult:
        name=x[0]
        phno=x[1]
        colony=x[2]
        city=x[3]
    print(list1)
    return render_template('donor_profile.html', name=name,phno=phno,colony=colony,city=city)


'''@app.route("/update_donor",methods=['POST'])
def update_donor():
    global mycursor,donor_username
    list1 = []
    global donor_id;
    name= request.form.get('dname')
    phno = request.form.get('phno')
    colony = request.form.get('colony')
    city = request.form.get('city')
    print(name,phno,colony,city)
    sql="update donor set name=%s,phno=%s,colony=%s,city=%s where donor_id=%s"
    val=(name,phno,colony,city,donor_id)
    mycursor.execute(sql,val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")
    return redirect(url_for('donor_dashboard.html', donor_username=donor_username,success=False))
    print(donor_id)'''

@app.route("/update_donor",methods=['POST'])
def update_donor():
    global mycursor,donor_username
    list1 = []
    global donor_id;
    name= request.form.get('dname')
    phno = request.form.get('phno')
    colony = request.form.get('colony')
    city = request.form.get('city')
    print(name,phno,colony,city)
    sql="update donor set name=%s,phno=%s,colony=%s,city=%s where donor_id=%s"
    val=(name,phno,colony,city,donor_id)
    mycursor.execute(sql,val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")
    return redirect(url_for('donor_dashboard.html', donor_username=donor_username,success=False))
    print(donor_id)


@app.route('/logout')
def logout():
    return redirect(url_for('login'))
if __name__ == '__main__':
    app.run(debug=True)
