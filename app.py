from flask import Flask, request, redirect,url_for,render_template,make_response
import os
from datetime import datetime
app=Flask(__name__)
users = {} #user data storage
statements={} #transaction statements storage
@app.route('/')
def home():
    return render_template('welcome.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        print(request.form)
        username =request.form['username']
        email =request.form['email']
        phone_no =request.form['ph_no']
        upassword =request.form['password']
        if username not in users:
            users[username]={'email':email,'phone_no':phone_no ,'password':upassword ,'amount':0}
            if username not in statements:
                statements[username]={'deposit_statement':[],'withdraw_statement':[]}
            return redirect(url_for('login'))
        else:
            return 'User already existed '
    return render_template('register.html')
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        login_username=request.form['uname']
        login_password=request.form['password']
        if login_username in users:
            stored_password=users[login_username]['password']
            if stored_password == login_password:
                # return "dashboard"
                # return redirect(url_for('dashboard'))
                resp = make_response(redirect(url_for('dashboard')))
                resp.set_cookie('user',login_username)
                return resp
            else:
                return 'incorrect password'
        else:
            return 'username not found pls check'
    return render_template('login.html')
@app.route('/dashboard')
def dashboard():
    if request.cookies.get('user'):
        username=request.cookies.get('user')
        return render_template('dashboard.html',username=username)
    else:
        return 'please login first to see dashboard'

@app.route('/deposit',methods=['GET','POST'])  
def deposit():
    if request.cookies.get('user'):
        if request.method=='POST':
            deposit_amount=int(request.form['amount'])
            if deposit_amount>0:
                if deposit_amount<=50000:
                    if deposit_amount%100==0:
                        username=request.cookies.get('user')#user data in cookie
                        users[username]['amount']=users[username]['amount']+deposit_amount 
                        deposit_time=datetime.now()
                        deposit_data=(deposit_amount,deposit_time)
                        statements[username]['deposit_statement'].append(deposit_data)
                        return redirect(url_for('balance'))
                    else:
                        return 'Amount should be multiple of 100'
                else:
                    return 'Amount exceeded than 50000'
            else:
                return 'Amount should be positive value'     
        return render_template('deposit.html')
    else:
        return 'please login first'

@app.route('/withdraw',methods=['GET','POST'])
def withdraw():
    if request.cookies.get('user'):
        if request.method=='POST':
            withdraw_amount=int(request.form['amount'])
            username=request.cookies.get('user')
            balance_amount=users[username]['amount']
            if withdraw_amount>0:
                if withdraw_amount%100 == 0:
                    if balance_amount>=withdraw_amount:
                        users[username]['amount']=balance_amount-withdraw_amount 
                        withdraw_time = datetime.now()
                        withdraw_data = (withdraw_amount,withdraw_time)
                        statements[username]['withdraw_statement'].append(withdraw_data)
                        return redirect(url_for('balance'))
                    else:
                        return 'insufficient balance amount'       
                else:
                    return 'Amount should be multiple of 100'
            else:
                return 'Amount should be positive value'   
        return render_template('withdraw.html')
    else:
        return 'please login first'
    
@app.route('/balance',methods=['GET'])
def balance():
    if request.cookies.get('user'):
        balance_amount=users[request.cookies.get('user')]['amount']
        return render_template('balance.html',balance_amount=balance_amount)
    else:
        return 'please re -login to see the balance amount'
    

@app.route('/statement',methods=['GET'])
def statement():
    if request.cookies.get('user'):
        username=request.cookies.get('user')
        deposit_statement_info=statements[username]['deposit_statement']
        withdraw_statement_info=statements[username]['withdraw_statement']
        return render_template('statements.html',deposit_statement_info=deposit_statement_info,withdraw_statement_info=withdraw_statement_info)
    else:
        return 'pls login to check statements'
    
@app.route('/logout')
def logout():
    if request.cookies.get('user'):
        resp=make_response(redirect(url_for('login')))
        resp.delete_cookie('user')
        return resp
    else:
        return 'please login to logout '

@app.route('/accountdelete')
def accountdelete():
    username = request.cookies.get('user')

    if not username:
        return "User not logged in"

    users.pop(username, None)
    statements.pop(username, None)

    resp = make_response(redirect(url_for('home')))
    resp.delete_cookie('user')
    return resp
# @app.route('/profile')
# def profile():
#     if request.cookies.get('user'):
#         username=request.cookies.get('user')
#         return render_template('profile.html',username=username,users=users)
#     else:
#         return 'please login to see profile'
# @app.route('/dummy')
# def dummy():
#     data = users
#     return render_template('dummy.html',data=data)
# @app.route('/register')
# # @app.route('/templates/register.html')
# def register():
#     return render_template('register.html')




if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)