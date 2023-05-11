import sqlite3
from flask import render_template, request, Flask

app = Flask(__name__) #create a flask object

@app.route('/') #root path
def home():
    return render_template('start.html') #open HTML file

@app.route('/register/', methods=['POST']) #route to register path using POST method
def register():
    submission = request.form['register']  #read the button value in the HTML file
    if submission == "Generate AM Session": #button value is "Generate AM Session"
        data = report("AM")
        return render_template("result.html", arts=data[0], cultural=data[1], sports=data[2], session = "AM")
    elif submission == "Generate PM Session": #button value is "Generate PM Session"
        data = report("PM")
        return render_template("result.html", arts=data[0], cultural=data[1], sports=data[2], session = "PM")
    else:                       #button value is "Register"
        insert(request.form)
        return 'data inserted'

def report(session): #create the arts, cultural & sports data list for AM/PM session
    conn=sqlite3.connect('register.db')
    cursor = conn.execute('''SELECT Registration.StudentID, Type, Venue,
                                    Arts.Performance, Cultural.Race, Sports.Contact, Sports.Cost 
                            FROM Registration
                            LEFT OUTER JOIN Arts ON Registration.StudentID=Arts.StudentID
                            LEFT OUTER JOIN Cultural ON Registration.StudentID=Cultural.StudentID
                            LEFT OUTER JOIN Sports ON Registration.StudentID=Sports.StudentID
                            WHERE Session=?''',(session,))
    data = []
    for record in cursor:   #store all types of activities for required AM/PM session into data list
        data.append(record)
    conn.close()
    arts=[]
    cultural = []
    sports = []
    for i in range(len(data)):
        if data[i][1] == 'A':  #check for Arts type
            arts.append([data[i][0],data[i][2],data[i][3]]) #store StudentID, Venue, Performance
        elif data[i][1] == 'C':  #check for Cultural type
            cultural.append([data[i][0],data[i][2],data[i][4]]) #store StudentID, Venue, Race
        elif data[i][1] == 'S':  #check for Sports type
            sports.append([data[i][0],data[i][2],data[i][5],data[i][6]]) #store StudentID, Venue, Contact, Cost
    return (arts,cultural,sports)

def insert(data):
    conn = sqlite3.connect('register.db')
    reg_type = data['type'].strip() #get rid of any lead and end spaces
    tobeInserted = (data['studentid'],reg_type,data['venue'],data['session'])
    conn.execute('INSERT INTO Registration(StudentID, Type, Venue, Session) VALUES (?,?,?,?)',tobeInserted)
    if reg_type == 'A': #insert specific data for Arts
        specialInsert = (data['studentid'], data['performance'])
        conn.execute('INSERT INTO Arts(StudentID, Performance) VALUES(?,?)',specialInsert)
    elif reg_type == 'C': #insert specific data for Cultural
        specialInsert = (data['studentid'], data['race'])
        conn.execute('INSERT INTO Cultural(StudentID, Race) VALUES(?,?)',specialInsert)
    elif reg_type == 'S': #insert specific data for Sports
        specialInsert = (data['studentid'], data['contact'], data['cost'])
        conn.execute('INSERT INTO Sports(StudentID, Contact, Cost) VALUES(?,?,?)',specialInsert)
    conn.commit()
    conn.close()

#reset database, delete any existing tables in database
conn=sqlite3.connect('register.db') 
file = open("TASK1.sql","r") #SQL code will drop all existing tables and create new tables
commands = file.read().split(';')
file.close()
for each in commands:
    conn.execute(each)
conn.commit()
conn.close()

if __name__ == '__main__':
    app.run()
