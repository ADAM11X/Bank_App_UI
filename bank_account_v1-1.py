from flask import Flask ,render_template,request,session
import random
import json

app = Flask(__name__)
app.secret_key="secret"

try:
    with open("bank.txt", "r") as f:
       
        data = json.load(f)
except FileNotFoundError:
    data = {}


def save_data():
  with open("bank.txt", "w") as f:  
    json.dump(data, f, indent=4) 


try :
   with open("transaction.txt", "r") as s :
     transactions=json.load(s)
   
except:
      transactions={}


def save_transaction():

  with open("transaction.txt", "w") as s :
       json.dump(transactions,s,indent=4)

@app.route("/")
def home():
    if "user" in session:
        user= session["user"]
        return render_template("home.html")
    return render_template("login.html")


@app.route("/create_account" ,methods=['POST','GET'])
def create_account():
    if "user" in session:
        return render_template("home.html")
    else:
        if request.method == 'POST':
            user=request.form["user"]
            mdp=request.form["mot_de_passe"]
            if user not in data.keys():
                data[user]={}
                data[user]["balance"]=0
                data[user]["password"]=str(mdp)
                RIB=[]
                for i in range(24):
                    RIB.append(str(random.randint(0,9)))
                data[user]['RIB']=RIB

                save_data()
                message=f'your account is created succefully'
                return render_template("login.html",message=message)
            else:
                message=f'this account is already created'
                return render_template("login.html", message=message)
        return render_template("create_account.html")
    

@app.route("/log_in", methods=["GET","POST"])
def log_in():
    if request.method == "POST":
        user=request.form["user"]
        mdp=request.form["mot_de_passe"]
        session["user"]=user
        if user in data and mdp == data[user]["password"]:
            message="you logged in successfully"
            return render_template("home.html",message=message)
        
    return render_template("login.html")

@app.route("/log_out")
def log_out():
    session.pop("user", None)
    message="you logged out"
    return render_template("login.html",message=message)

@app.route("/deposit", methods=["GET", "POST"])
def deposit():
    if "user" in session:
        user= session["user"]
        if request.method== 'POST':
            deposit_balnce= int(request.form["amount"])
            data[user]["balance"] += abs(deposit_balnce) 
            message=f"the deposit of {abs(deposit_balnce)} is completed successfully"
            save_data()
            return render_template("deposit.html", message=message)
        return render_template("deposit.html")
    else :
        return render_template("login.html")

@app.route("/transaction",methods=['GET','POST'])
def transaction():
    if "user" in session:
        user= session["user"]
        if request.method=='POST':
            receiver_user=request.form["receiver_user"]
            amount=int (request.form["amount"])
            if data[user]['balance'] >= amount :
                data[user]['balance']-= amount
                data[receiver_user]['balance']+= amount
                save_data()
                transactions[user]={"receveiver":receiver_user,"amount":amount}
                save_transaction()
                message="your transaction was made properly"
                return render_template("transaction.html",message=message)
            else: 
                message="this amount is not avaible in your balance"
                return render_template("transaction.html",message=message)
        else:
            return render_template("transaction.html")
    else :
        return render_template("login.html")


@app.route("/balance")
def balance():
        if "user" in session:
            user= session["user"]
            balance=data[user]['balance']
            message=f'your balance is {balance}'
            return render_template("balance.html",message=message)
        else :
            return render_template("login.html")
        
@app.route("/show_rib")
def show_rib():
    if "user" in session:
        user= session["user"]
        RIB =  data[user]['RIB']
        message= " ".join(RIB) 
        message2=data[user]["balance"]
        return render_template("show_rib.html", message=message,message2=message2)
    else :
        return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)

