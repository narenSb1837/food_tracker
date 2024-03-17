from flask import Flask,render_template,url_for,request,g
from database import get_db
from datetime import datetime

app=Flask(__name__)
import secrets
secret_key = secrets.token_hex(16)
app.config['DEBUG']=True
app.config['SECRET_KEY']=secret_key
@app.teardown_appcontext
def close_db(error):
    if hasattr(g,'sqlite_db'):
        g.sqlite_db.close()

    
@app.route('/')
@app.route('/home',methods=['GET','POST'])
def home():
    db=get_db()
    cur=db.cursor()
    if request.method=='POST':
        date=request.form['date']
        date=datetime.strptime(date, '%Y-%m-%d')
        dt=datetime.strftime(date,'%Y-%m-%d')
        db.execute('insert into log_date_table(log_date) values (?)',[dt])
        db.commit()
        #db.execute('insert into food_table (date,food_id)')
        cur.execute('select log_date from log_date_table')
        res=cur.fetchall()

        calories=list(dict())
        #print(res['log_date'])
        for dates in res:
            cur.execute(""" SELECT date,sum(fats) as fats ,sum(carbs) as carbs ,sum(protein) as protein from food_date join Food on food_date.food_id=Food.id where date=(?) group by date """,[dates['log_date']])

            res=cur.fetchall()
            if res==[]:
                calories.append([{'date':dates['log_date'],'carbs':0,'fats':0,'protein':0}])
            else:
                calories.append(res)

        return render_template('home.html',calories=calories)
    else:
        cur.execute('select log_date from log_date_table')
        res=cur.fetchall()

        calories=list(dict())
        #print(res['log_date'])
        for dates in res:
            cur.execute(""" SELECT date,sum(fats) as fats ,sum(carbs) as carbs ,sum(protein) as protein from food_date join Food on food_date.food_id=Food.id where date=(?) group by date order by date desc """,[dates['log_date']])
            res=cur.fetchall()
            if res==[]:
                calories.append([{'date':dates['log_date'],'carbs':0,'fats':0,'protein':0}])
            else:
                calories.append(res)

        return render_template('home.html',calories=calories)

        
@app.route('/additem',methods=['GET','POST'])
def additem():
    
    db=get_db()
    cur=db.cursor()

    if request.method=='GET':
        cur.execute('select * from Food')
        result=cur.fetchall()
        return render_template('additem.html',result=result)
    else:
        name=request.form['name']
        protein=request.form['protein']
        carbs=request.form['carbs']
        fats=request.form['fats']

        db.execute("""insert into Food (name,protein,fats,carbs) values (?,?,?,?)""",[name,protein,fats,carbs])
        db.commit()
        cur.execute('select * from Food')
        result=cur.fetchall()
        return render_template('additem.html',result=result)
@app.route('/viewdetails/<date>',methods=['GET','POST'])
def viewdetails(date):
    db=get_db()
    cur=db.cursor()
    if request.method=='POST':
        name=request.form['food']
        cur.execute('select id from Food where name=(?)',[name])
        id=cur.fetchone()['id']
        db.execute('insert into food_date (date,food_id) values (?,?) ',[str(date),int(id)])
        db.commit()
    cur.execute('select name from Food')
    food=cur.fetchall()
    cur.execute('select Food.name,Food.carbs,Food.protein,Food.fats from Food join food_date on Food.id=food_date.food_id where food_date.date=(?)',[date])
    
    food_list=cur.fetchall()
    total_calories=0
    for i in food_list:
        total_calories+=i['carbs']+i['fats']+i['protein']
    return render_template('viewdetails.html',food_names=food,date=date,food_list=food_list,total_calories=total_calories)

        
        
        
        

if __name__=='__main__':
    app.run()
