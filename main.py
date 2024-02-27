import mysql.connector
import datetime
import random


try:
    db= mysql.connector.connect(host="localhost",user="root",password="root")

    # Create a cursor object
    curs= db.cursor()

    # SQL commands to create the database and tables
    commands = [
        "CREATE DATABASE tamil_ecommerse_1;",
        "USE tamil_ecommerse_1;",
        """
        CREATE TABLE user_table (
            customer_id INT,
            mail_id VARCHAR(50) PRIMARY KEY,
            passwords VARCHAR(50) NOT NULL
        );
        """,
        """
        CREATE TABLE customer_table (
            customer_id INT PRIMARY KEY AUTO_INCREMENT,
            customer_name VARCHAR(50) NOT NULL,
            phno INT(15) NOT NULL,
            mail_id VARCHAR(50),
            FOREIGN KEY (mail_id) REFERENCES user_table(mail_id)
        );
        """,
        """
        CREATE TABLE customer_address(
            customer_id INT,				
            customer_zip_code INT(6),			
            customer_city VARCHAR(25),			
            customer_state VARCHAR(25),
            customer_drno_st VARCHAR(100),
            FOREIGN KEY (customer_id) REFERENCES customer_table(customer_id)
        );
        """,
        """
        CREATE TABLE product_table (
            product_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
            product_category VARCHAR(25),
            product_subcategory VARCHAR(50) NOT NULL,
            product_name VARCHAR(100) NOT NULL,
            product_description VARCHAR(250),
            price INT NOT NULL,
            quantity INT(8) NOT NULL
        );
        """,
        """
        CREATE TABLE payment_table (				
            payment_id INT PRIMARY KEY AUTO_INCREMENT,					
            payment_type VARCHAR(25),					
            order_value INT,
            payment_status VARCHAR(10)
        );
        """,
        """
        CREATE TABLE order_table(
            order_id INT PRIMARY KEY AUTO_INCREMENT,
            order_date DATETIME,
            customer_id INT ,
            product_id INT,
            Quantity INT ,
            order_value INT ,
            payment_id INT,
            FOREIGN KEY (customer_id) REFERENCES customer_table(customer_id),
            FOREIGN KEY (product_id) REFERENCES product_table(Product_id),
            FOREIGN KEY (payment_id) REFERENCES payment_table(payment_id)
        );
        """,
        """
        CREATE TABLE cancel_table( 
            order_id INT ,
            cancel_date DATETIME,
            customer_id INT ,
            product_id INT,
            Quantity INT,
            payment_id INT,					
            payment_type VARCHAR(25),					
            order_value INT,
            refund_status VARCHAR(10),
            FOREIGN KEY (customer_id) REFERENCES customer_table(customer_id),
            FOREIGN KEY (product_id) REFERENCES product_table(Product_id)
        );
        """,
        """
        CREATE TABLE employee_account_table(
            Employee_id INT PRIMARY KEY AUTO_INCREMENT,
            mail_id VARCHAR(50) NOT NULL UNIQUE,
            passwords VARCHAR(50) NOT NULL
        );
        """,
        """
        CREATE TABLE Employee_table (
            Employee_id INT NOT NULL ,
            Employee_name VARCHAR(50) NOT NULL,
            phno INT(15) NOT NULL,
            address VARCHAR(80) NOT NULL,
            designation VARCHAR(15) NOT NULL,
            age INT(15) NOT NULL,
            FOREIGN KEY (Employee_id) REFERENCES employee_account_table(Employee_id)
        );
        """,
        """INSERT INTO user_table VALUES (1,"tamil","12345");""",
        """INSERT INTO customer_table VALUES (1,"tamil",12345,"tamil");""",
        """INSERT INTO customer_address VALUES (1,123456,"chennai","tamil nadu","12345 vbnm");""",
        """INSERT INTO employee_account_table VALUES (1,'tamil','tamil'),(2,'rj',"rj");""",
        """INSERT INTO Employee_table VALUES (1,"tamil",12345,"tamil","manager",23),(2,"raj",67345,"dfgh","manager",27);""",
        """INSERT INTO product_table VALUES (1,"Mattress and Accessories","Mattress","Orthopedic Memory Foam Mattress Single 72 x 30x 6","Orthopedic Memory Foam Mattress Single 72 x 30x 6",13999,30);""",
        """INSERT INTO payment_table VALUES (1,"upi",13999,"success");"""
    ]

    # Execute each command
    for command in commands:
        curs.execute(command)

    # Close the cursor and connection
    curs.close()
    db.close()
except:
    pass



db=mysql.connector.connect(host="localhost",user="root",password="root",port="3306",database="ecommerse_5")

curs=db.cursor()
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

if db:
    print("working connection")
else:
    print("error")

current_datetime = datetime.datetime.now().replace(microsecond=0)
timedate=(current_datetime)

"""
order_id,order_date,customer_id,product_id,Quantity,order_value,payment_id=1,timedate,1,1,2,13999,1
order_statement = ("insert into order_table (order_date,customer_id,product_id,Quantity,order_value,payment_id) values(%s,%s,%s,%s,%s,%s)")
valu_1= (timedate,customer_id,product_id,Quantity,order_value,payment_id)
curs.execute(order_statement, valu_1)
db.commit()
"""

def mail_statement(subject_statement,body_statement,customer_id):
    second_query = ("select * from customer_table where mail_id = %s")
    curs.execute(second_query, [customer_id])
    container_cidd = curs.fetchone()
    mail_id = container_cidd[3]
    customer_name = container_cidd[1]
    sender = "tamilselvan.foruppo@gmail.com"
    receiver = "mail_id"
    password = "PASSWORD" #ENTER
    subject = ("{}".format(subject_statement))
    body = ("{}".format(body_statement))

    msg = MIMEMultipart()
    msg['from'] = sender
    msg['To'] = receiver
    msg['Subject'] = subject



    msg.attach(MIMEText(body, 'plain'))
    filename = 'ghu.csv'
    with open(filename, 'rb') as f:
        attachment = MIMEApplication(f.read(), _subtype='csv')
        attachment.add_header('content-Disposition', 'attachment', filename=filename)
        msg.attach(attachment)
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login(sender, password)
        smtp.send_message(msg)


def creataccount(mail_id,passwords):
    OTP= str(random.randint(1000, 9999))
    from_addr = "tamiltonny@gmail.com"    #ENTER MAIL
    to_addr = mail_id
    password = "PASSWORD"          #enterpassword
    subject = "VERIFY YOUR OTP"
    message = ("{}".format(OTP))
    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_addr,password)
    text = msg.as_string()
    server.sendmail(from_addr, to_addr, text)
    server.quit()



    """msg = MIMEMultipart()
    msg['from'] = sender
    msg['To'] = receiver
    msg['Subject'] = subject
    msg.set_content(body)

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login(sender, password)
        smtp.send_message(sender,receiver,body)
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(sender,password)
    server.sendmail(sender,receiver,body)"""

    stp= str(input("enter otp"))
    if stp == OTP:
        phno = input("enter customer phno: ")
        while len(phno) != 10:
            print("invalid phno")
            phno = input("enter customer phno: ")
        customer_zip_code = input("enter zip_code: ")
        while len(customer_zip_code) != 6:
            print("invalid zip code")
            customer_zip_code = input("enter zip_code: ")
        customer_city = input("enter city: ")
        customer_state = input("enter state: ")
        customer_drno_st = input("enter drnumber and street: ")

        first_query = "select max(customer_id) from customer_table"
        curs.execute(first_query)
        v1 = curs.fetchone()
        customer_idd = int(v1[0])
        customer_id = customer_idd + 1

        mail_statement = ("insert into user_table(customer_id,mail_id,passwords) values(%s,%s,%s)")
        exe_curs = (customer_id, mail_id, passwords)
        curs.execute(mail_statement, exe_curs)
        db.commit()

        customer_statement = ("insert into customer_table(customer_name, phno,mail_id) values(%s,%s,%s)")
        value = (customer_name,phno,mail_id)
        curs.execute(customer_statement,value)
        db.commit()

        print("Account created succesfully")
        address_statement = ("insert into customer_address(customer_id,customer_zip_code,customer_city,customer_state,customer_drno_st) values(%s,%s,%s,%s,%s)")
        ex_curs= (customer_id,customer_zip_code,customer_city,customer_state,customer_drno_st)
        curs.execute(address_statement, ex_curs)
        db.commit()
    else:
        print("wrong otp")


def creataccount_employee(Employee_mail):
    #Employee_id = input("employee id ")
    passwords = input("employee id password ")
    check_query = ("select passwords from employee_account_table where mail_id = %s")
    curs.execute(check_query, [Employee_mail])
    container1_values = curs.fetchone()
    existing_employer_pass = container1_values[0]
    print(existing_employer_pass)
    print("login succesfull")
    print(existing_employer_pass)
    if passwords == existing_employer_pass:
        print("loged in")
    # bellow orginal query  above verification query
        new_mail_id= (input("Enter new employee Mail Id:"))
        passwordss = None
        reenter = 1
        while passwordss != reenter:
            passwordss = (input("Enter you Password:"))
            reenter = (input("Re-Enter your Password:"))
            if passwordss != reenter:
                print("password dosn't match")
            else:
                Employee_name = input("enter yor name")
                phno = input("enter yor ph no")
                address = input("enter yor adress")
                designation = input("enter employee designation: ")
                age = int(input("enter employee age: "))

                mailll_statement = ("insert into employee_account_table (mail_id,passwords) values(%s,%s)")
                valu_11 = (new_mail_id, passwordss)
                curs.execute(mailll_statement, valu_11)
                db.commit()
                f_query = "select max(Employee_id) from employee_account_table"
                curs.execute(f_query)
                v11 = curs.fetchone()
                e_id = int(v11[0])
                emp_statement = ("insert into employee_table(Employee_id,Employee_name,phno,address,designation,age) values(%s,%s,%s,%s,%s,%s)")
                valu = (e_id,Employee_name, phno, address, designation, age)
                curs.execute(emp_statement, valu)
                db.commit()


def login_verify(mail_id, passwords):
    first_query = ("select passwords from user_table where mail_id = %s")
    curs.execute(first_query, [mail_id])
    container_values = curs.fetchone()
    #print(container_values)
    customer_pass = container_values[0]
    #print(customer_pass)
    #print("login succesfull")
    #print(customer_pass)
    while passwords != customer_pass:
        passwords = (input("Enter you Password:"))
        if passwords != customer_pass:
            print("password dosn't match")
        else:
            print("loged in")



def login_verify_employee(mail_id, passwords):
    first_query = ("select passwords from employee_account_table where mail_id = %s")
    curs.execute(first_query, [mail_id])
    container_values = curs.fetchone()
    customer_pass = container_values[0]
    if passwords == customer_pass:
        print("loged in")


def fetch_customer_id(mail_id):
    second_query = ("select * from customer_table where mail_id = %s")
    curs.execute(second_query, [mail_id])
    container_cidd = curs.fetchone()
    customer_id = container_cidd[0]
    customer_name = container_cidd[1]
    print(customer_id)
    return customer_id,customer_name


def view_booking(customer_id):
    first_query = ("select * from order_table where customer_id = %s")
    curs.execute(first_query, [customer_id])
    container = curs.fetchall()
    print(container)
    """price = container[1]
    Quantity = container[2]
    product_id = container[4]
    print("product id: {}, quantity: {},total price: {} ".format(product_id,Quantity,price))
"""

def payment_type():
    inptr = None
    while inptr not in("1","2"):
        inptr =(input("enter your payment method \n \npress 1 for upi    \npress 2 for card transaction"))
        if inptr == "1":
            payment="upi"
            return payment
        else:
            payment = "card"
            return payment


def order_product(customer_id,timedate,customer_name):


    # getting product id
    product_id =(input("Enter product id:"))
    Quantity = int((input("Enter quantity:")))

    # getting product price
    second_query = ("select * from product_table where product_id= %s")
    curs.execute(second_query, [product_id])
    container_price = curs.fetchone()
    price = container_price[5]
    product_name = container_price[3]
    total_price = price * Quantity
    payment_ty = (payment_type())
    inptr = None
    while inptr not in ("1", "2"):
        inptr = (input("press 1 to success     \n press 2 to fail"))
        if inptr in "1":
            payment_status = "success"
            payment_statement = ("insert into payment_table (payment_type,order_value,payment_status) values(%s,%s,%s)")
            valu = (payment_ty, total_price, payment_status)
            curs.execute(payment_statement, valu)
            db.commit()

            st_query ="select max(payment_id) from payment_table"
            curs.execute(st_query)
            v1 = curs.fetchone()
            payment_id= int(v1[0])
            print(payment_id)

            order_statement = ("insert into order_table (order_date,customer_id,product_id,Quantity,order_value,payment_id) values(%s,%s,%s,%s,%s,%s)")
            valu_1 = (timedate, customer_id, product_id, Quantity, total_price, payment_id)
            curs.execute(order_statement, valu_1)
            db.commit()

            first_query = ("select quantity from product_table where product_id = %s")
            curs.execute(first_query, [product_id])
            v1 = curs.fetchone()
            v2 = v1[0]
            v3 = v2 - Quantity
            product_decrase = (v3)
            change_statement = ("UPDATE product_table SET quantity=%s WHERE product_id=%s")
            valuem = (product_decrase, product_id)
            curs.execute(change_statement, valuem)
            db.commit()

            fi_query = ("select order_id from order_table where payment_id = %s")
            curs.execute(fi_query, [payment_id])
            v1 = curs.fetchone()
            order_id= v1[0]

            #message = ("Hi {},\nThanks for your order!\nYour Order number {}\nproductpayment_id {}\n total price of the product {}\nOrder Date {}\n product name\nquantity {}\nThanks,".format(customer_name, order_id, payment_id, total_price, timedate, product_name, Quantity))

#ask


            from_addr = "tamiltonny@gmail.com"
            to_addr = mail_id
            password = "zqhz wbhc bvoe znbr"
            subject = "purchase invoice"
            """message = ("Hi {},\nThanks for your order!\nYour Order number {}\nproductpayment_id {}\n total price of the product {}\nOrder Date {}\n product name\nquantity {}\nThanks,".format(customer_name,order_id,payment_id,total_price,timedate,product_name,Quantity))
            msg = MIMEMultipart()
            msg['From'] = from_addr
            msg['To'] = to_addr
            msg['Subject'] = subject"""


            """

            msg.attach(MIMEText(message, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(from_addr, password)
            text = msg.as_string()
            server.sendmail(from_addr, to_addr, text)
            server.quit()
"""

            message = (
                "Hi {},\nThanks for your order!\n"
                "Your Order number {}\n"
                "productpayment_id {}\n"
                "total price of the product {}\n"
                "Order Date {}\n"
                "product name {}\n"
                "quantity {}\n"
                "Thanks,".format(customer_name, order_id, payment_id, total_price, timedate, product_name, Quantity)
            )

            msg = MIMEMultipart()
            msg['From'] = from_addr
            msg['To'] = to_addr
            msg['Subject'] = subject

            msg.attach(MIMEText(message, 'plain'))

            try:
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(from_addr, password)
                text = msg.as_string()
                server.sendmail(from_addr, to_addr, text)
                server.quit()
                print("Email sent successfully")
            except Exception as e:
                print("Email could not be sent:", str(e))


        else:
            payment_status = "failed"
            payment_statement = ("insert into payment_table (payment_type, payment_value, payment_status) values(%s,%s,%s)")
            valu = (payment_type, total_price, payment_status)
            curs.execute(payment_statement, valu)
            db.commit()


#order_product(customer_id,timedate,customer_name)



def update_account(customer_id):
    customer_name = input("enter new name ")

    phno = input("enter customer phno: ")
    while len(phno) != 10:
        print("invalid phno")
        phno = input("enter customer phno: ")
    customer_zip_code= input("enter zip_code: ")
    while len(customer_zip_code) != 6:
        print("invalid zip code")
        customer_zip_code = input("enter zip_code: ")
    customer_city = input("enter city: ")
    customer_state = input("enter state: ")
    customer_drno_st = input("enter drnumber and street: ")

    inptr = (input("press 1 to password update    \n press 2 to personal information update"))
    if inptr in "1":
         mail_statement = ("update user_table set  passwords=%s where customer_id=%s")
         exe_curs = (passwords,customer_id)
         curs.execute(mail_statement, exe_curs)
         db.commit()
    else:
        customer_statement = ("update customer_table set customer_name=%s ,phno=%s where customer_id=%s")
        value = (customer_name,phno,customer_id)
        curs.execute(customer_statement,value)
        db.commit()

        print("Account created succesfully")
        address_statement = ("update customer_address set customer_zip_code=%s ,customer_city=%s ,customer_state=%s ,customer_drno_st=%s where customer_id=%s")
        ex_curs= (customer_zip_code,customer_city,customer_state,customer_drno_st,customer_id)
        curs.execute(address_statement, ex_curs)
        db.commit()



def cancel(timedate,order_id):
    od=(order_id,)

    first_query = ("select * from order_table where order_id =%s")
    curs.execute(first_query,od)
    container_values = curs.fetchone()
    customer_id=(container_values[2])
    product_id=(container_values[3])
    Quantity=(container_values[4])
    payment_id =(container_values[6])

    second_query = ("select * from payment_table where payment_id =%s")
    curs.execute(second_query,[payment_id])
    container1_values = curs.fetchone()
    payment_type=(container1_values[1])
    payment_value=(container1_values[2])
    refund_status="refunded"

    refund_change_statement = ("UPDATE payment_table SET payment_status=%s WHERE payment_id=%s")
    val = (refund_status, payment_id)
    curs.execute(refund_change_statement, val)
    db.commit()
#storing in cancel tabel
    customer_statement = ("insert into cancel_table (order_id,cancel_date,customer_id,product_id,Quantity,payment_id,payment_type,order_value,refund_status) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)")
    valllu = (order_id,timedate,customer_id,product_id,Quantity,payment_id,payment_type,payment_value,refund_status)
    curs.execute(customer_statement, valllu)
    db.commit()

    delete_statement ="delete from order_table where order_id = %s"
    curs.execute(delete_statement, od)
    db.commit()
    print("Order cancelled succesfully")

#restocing the canceled item to product table
    first_query = ("select quantity from product_table where product_id = %s")
    curs.execute(first_query, [product_id])
    v1 = curs.fetchone()
    v2=v1[0]
    v3 = v2 + Quantity
    product_decrase =(v3)


    change_statement = ("UPDATE product_table SET quantity=%s WHERE product_id=%s")
    valuem = (product_decrase, product_id)
    curs.execute(change_statement, valuem)
    db.commit()


    second_qu = ("select product_name from product_table where product_id= %s")
    curs.execute(second_qu, [product_id])
    container_price = curs.fetchone()
    product_name = container_price[0]


    from_addr = "tamiltonny@gmail.com"
    to_addr = mail_id
    password = "zqhz wbhc bvoe znbr"
    subject = "Canceled order"

    message = ("Hi {},\nThanks for your order!Your order has been succesfully cancelled and payment 'Refunded'\nYour Order number {}\nproductpayment_id {}\n total price of the product {}\ncancel Date ()\n product name\nquantity {}\nThanks,".format(customer_name, order_id, payment_id, payment_value, timedate, product_name, Quantity))

    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_addr, password)
        text = msg.as_string()
        server.sendmail(from_addr, to_addr, text)
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print("Email could not be sent:", str(e))


def add_new_product():
    product_category=input("enter the product category: ")
    product_subcategory=input("enter the product subcategory: ")
    product_name=input("enter the product name: ")
    product_description=input("enter the product_description: ")
    price=input("enter the product price : ")
    quantity =input("enter the product Quantity : ")
    change_statement = ("insert into product_table(product_category,product_subcategory,product_name,product_description,price,quantity) values(%s,%s,%s,%s,%s,%s)")
    valu_1 = (product_category,product_subcategory,product_name,product_description,price,quantity)
    curs.execute(change_statement, valu_1)
    db.commit()



def delete_product():
    product_id = input("enter product id to remove ")
    delete_statement = "delete from product_table where product_id=%s"
    curs.execute(delete_statement,[product_id])
    db.commit()
    print("product deleted succesfully")


def update_product():
    product_id = input("enter the product id to upload:")
    q3 = int(input("enter the product quantity to upload:"))
    first_query = ("select * from product_table where product_id= %s")
    curs.execute(first_query,[product_id])
    container_values = curs.fetchone()
    q1 = container_values[6]
    #q2 =q1[0]
    quantity =q1 + q3
    change_statement = ("UPDATE product_table SET quantity=%s WHERE product_id=%s")
    value = (quantity, product_id)
    curs.execute(change_statement, value)
    db.commit()
    print("stock updated succesfully")

while True:
    inptr = None
    #print("Are you a:\n         (a)Customer \n         (b)Employee  \n         (c)Employer \n Enter 'E' to EXIT")
    while inptr not in("a","b","c","e","A","B","C","E"):
        inptr =(input("Are you a:\n         (a)Customer \n         (b)support \n         (c)Employer \n Enter 'E' to EXIT  \n\nenter value:"))
        if inptr in "aA":
            inptr = None
            # ___
            #print("This is a customer side \n Are you a:\n         (1)creat new user \n         (2)sign in to existing user  \n Enter 'E' to EXIT")
            while inptr not in ("e", "2", "1", "E"):
                inptr = (input("This is a customer side \n Are you a:\n         (1)creat new user \n         (2)sign in to existing user  \n Enter 'E' to EXIT \n\nenter value:"))
                if inptr in "1":
                    mail_id =(input("Enter your Mail Id:"))
                    passwords = None
                    reenter = 1
                    while passwords != reenter:
                        passwords = (input("Enter you Password:"))
                        reenter = (input("Re-Enter your Password:"))
                        if passwords != reenter:
                            print("password dosn't match")
                        else:
                            customer_name = input("enter customer Name: ")
                            creataccount(mail_id,passwords)
                elif inptr in "2":
                    print("Login your account")
                    mail_id = input("Enter your mail id: ")
                    passwords = input("Enter your password: ")
                    login_verify(mail_id, passwords)
# cid statement is below
                    """def fetch_customer_id(mail_id):
                        second_query = ("select customer_id from user_table where mail_id = %s")
                        curs.execute(second_query, [mail_id])
                        container_cidd = curs.fetchone()
                        customer_id = container_cidd[0]
                        return customer_id
                        """
                    customer_id,customer_name= fetch_customer_id(mail_id)

                    inptr = None
                    print("choose one:\n         (a)View Bookings \n         (b)book a product  \n         (c)Update/change personal Details \n         (d)Cancel Bookings  \n Enter 'M' to Main window")
                    while inptr not in ("a", "b", "c", "e", "A", "B", "C", "E" "m", "M"):
                        inptr = (input("enter value:"))
                        if inptr in "aA":
                            print("View Booking")
                            view_booking(customer_id)
                        elif inptr in "bB":
                            print("Book a Product")
                            order_product(customer_id,timedate,customer_name)
                        elif inptr in "Cc":
                            update_account(customer_id)
                        elif inptr in "dD":
                            order_id=int(input("cancel order id"))
                            cancel(timedate,order_id)
                        elif inptr in "Ee":
                            print("E is working")
                        elif inptr in "rR":
                            print("R is working")
                        else:
                            break
        elif inptr in "bB":
            print("B is work")
            mail_id = input("Enter your mail id: ")
            passwords = input("Enter your password: ")
            login_verify_employee(mail_id, passwords)
            print("B is working")
            customer_id = input("enter_customer_id:")
            inptr = None
            #print("you are in the Employer site :\n         (a)View Bookings \n         (b)book a product  \n         (c)Update customer Details \n         (d)Cancel Bookings  \n Enter 'M' to Main window")
            while inptr not in ("a", "b", "c", "e", "A", "B", "C", "E"):
                inptr = (input("you are in the Employer site :\n         (a)View Bookings \n         (b)book a product  \n         (c)Update customer Details \n         (d)Cancel Bookings  \n Enter 'M' to Main window  \n\nenter value:"))
                try:
                    customer_name="ram"


                    if inptr in "aA":
                        print("View Booking")
                        view_booking(customer_id)
                    elif inptr in "bB":
                        print("Book a Product")
                        order_product(customer_id,timedate,customer_name)
                    elif inptr in "Cc":
                        update_account(customer_id)
                    elif inptr in "dD":
                        order_id = int(input("cancel order id"))
                        cancel(order_id,timedate)
                    elif inptr in "Ee":
                        print("EXIT")
                    elif inptr in "rR":
                        print("R is working")
                except:
                    print("some thing went wrong")

        elif inptr in "Cc":
            print("cc is work")
            mail_id = input("Enter your mail id: ")
            passwords = input("Enter your password: ")
            login_verify_employee(mail_id, passwords)
            inptr = None
            #print("Are you a:\n         (a)Add NEW product         \n         (b)upload stock \n         (c)Delete product\n         (d)creat new employee account         \n Enter 'M' to Main window")
            while inptr not in ("a", "b", "c", "m", "d", "D" "A", "B", "C", "M"):
                inptr = (input("Are you a:\n         (a)Add NEW product         \n         (b)upload stock \n         (c)Delete product\n         (d)creat new employee account         \n Enter 'M' to Main window  \n\nenter value:"))
                try:
                    if inptr in "aA":
                        print("add product")
                        add_new_product()
                    elif inptr in "bB":
                        update_product()
                    elif inptr in "Cc":
                        delete_product()
                        print("product is deleted")
                    elif inptr in "dD":
                        Employee_mail = mail_id
                        creataccount_employee(Employee_mail)
                    elif inptr in "Mm":
                        print("R is working")
                    else:
                        break
                except:
                    print("some thing went wrong")
    else:
        print("exit is working")

