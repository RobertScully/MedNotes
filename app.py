from flask import Flask, render_template, json, request, redirect, url_for, session
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
from PIL import Image
import pytesseract


#Pointing pytesseract to tesseract installation
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'


mysql = MySQL()
app = Flask(__name__)
app.secret_key = 'This is a secretive key'


# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'MedNotes'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


#Main Route
@app.route('/')
def main():
    if session.get('user'):
        return render_template('userHome.html')
    else:
        return redirect(url_for('showSignIn'))


#Signin route
@app.route('/showSignIn')
def showSignIn():
    return render_template('signin.html')


#Home Route
@app.route('/userHome')
def userHome():
    if session.get('user'):
        return render_template('userHome.html')
    else:
        return render_template('error.html', error='Error No Access Please Sign In')


@app.route('/showSuccess')
def showSuccess():
    if session.get('user'):
        return render_template('success.html', success='Record Added Successfully to the Database')
    else:
        return render_template('error.html', error='Error No Access Please Sign In')


#Route to log out user
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


#Login Validation route. If successful redirects to user home. If details do not match rerouted to error screen.
@app.route('/validateLogin', methods=['POST'])
def validateLogin():
    try:
        _staffid = request.form['inputStaffId']
        _password = request.form['inputPassword']

        # connect to mysql
        connVL = mysql.connect()
        cursor = connVL.cursor()
        #Calling stored procedure to validate login details
        cursor.callproc('sp_validateLogin', (_staffid,))
        data = cursor.fetchall()

        if len(data) > 0:
            #Comparing hashed password from database 
            if check_password_hash(str(data[0][2]),_password):
                #Creating session variable containing users first and last name
                session['user'] = data[0][3] + ' ' + data[0][4]
                #Creating session variable containing users id
                session['user_id'] = data[0][1]
                return redirect('/userHome')
            else:
                return render_template('error.html', error='Wrong Email Address or Password.')
        else:
            return render_template('error.html', error='Wrong Email Address or Password.')
 
    except Exception as e:
        return render_template('error.html', error=str(e))
    finally:
        cursor.close()
        connVL.close()

#Route to add an employee. No link in web application to this route but usable for adding additional employees
@app.route('/showAddEmployee')
def showAddEmployee():
    if session.get('user'):
        return render_template('addEmployee.html')
    else:
        return render_template('error.html', error='Error No Access Please Sign In')


@app.route('/addEmployee', methods=['POST', 'GET'])
def addEmployee():
    try:
        _staffid = request.form['inputStaffId']
        _firstname = request.form['inputFirstName']
        _surname = request.form['inputSurname']
        _email = request.form['inputEmail']
        _job = request.form['inputJob']
        _password = request.form['inputPassword']

        # validating received values
        if _staffid and _firstname and _surname and _email and _job and _password:
            
            # Connecting to mysql server
            connSU = mysql.connect()
            cursor = connSU.cursor()
            _hashed_password = generate_password_hash(_password)
            #Calling procedure to create new employee user
            cursor.callproc('sp_createEmployee', (_staffid, _firstname, _surname, _email, _job, _hashed_password))
            data = cursor.fetchall()

            if len(data) is 0:
                connSU.commit()
                return redirect('/userHome')
            else:
                return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})
    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close() 
        connSU.close()

#Route to connect to db and retrieve employees in order to fill list of employees table
@app.route('/showAddPatient')
def showAddPatient():
    if session.get('user'):
        connPL = mysql.connect()
        cursor = connPL.cursor()
        #Procedure to select all employees
        cursor.callproc('sp_selectEmployees')
        data = cursor.fetchall()
        #Routing to view of addpatient form in html. Passing contents of cursor which contains employee details to employees variable.
        return render_template('addPatient.html', employees=data)
    else:
        return render_template('error.html', error ='Error No Access Please Sign In')

#Routing for handling of adding of a patient logic when user hits create patient.
@app.route('/addPatient', methods=['POST', 'GET'])
def addPatient():
    try:        
        _employees = request.form['inputEmployeeString']
        _number = request.form['inputPatientNumber']
        _firstname = request.form['inputFirstName']
        _surname = request.form['inputSurname']

        #Splitting employee string into a new list by removing redundant txt from between the numbers
        _splitemployees = _employees.split('&inputEmployees=')

        if _number and _firstname and _surname:
            for i in range(1, len(_splitemployees)):
                #insert into our patient / customer matching table
                _patient_number = _number
                _employee_number = _splitemployees[i]
                connAccess = mysql.connect()
                cursor = connAccess.cursor()
                #Calling stored procedure for inserting details to the patient access table
                cursor.callproc('sp_insertAccess',(_patient_number, _employee_number))

        # validating received values
        if _number and _firstname and _surname:
            # Connecting to mysql server
            connAP = mysql.connect()
            cursor = connAP.cursor()
            cursor.callproc('sp_createPatient', (_number, _firstname, _surname))
            data = cursor.fetchall()
            cursor.close()

            if len(data) is 0:
                connAP.commit()
                connAP.close()
                return redirect(url_for('showSuccess'))#Fix
            else:
                return json.dumps({'error': str(data[0])})
        else:
                return json.dumps({'html': '<span>Please enter all of the required fields</span>'})
    except Exception as e:
        return json.dumps({'error': str(e)})

#Route to return a list of patients depending on which employee is attempting to view the list
@app.route('/getPatients')
def getPatients():
    try:
        if session.get('user'):
            _user = session.get('user_id')
 
            connGP = mysql.connect()
            cursor = connGP.cursor()
            #stored procedure to select all patient details where the user currently loggeds id matches in the patient_access table
            cursor.callproc('sp_GetPatientByAccess', (_user,))
            data = cursor.fetchall()
            #return html view of list of patients and pass contents of select from sp to patients var
            return render_template('showPatients.html', patients=data)
        else:
            return render_template('error.html',error='Error No Access Please Sign In')
    except Exception as e:
        return render_template('error.html', error=str(e))

#route for adding a note to the currently selected patient
@app.route('/addNote/<string:pat_note>')
def addNote(pat_note):
    try:
        _patientId = pat_note
        #setting a session variable that contains the most recently accessed patients id
        session['patient_id'] = _patientId
        #display html page of the add note function
        return render_template('addNote.html')
        
    except Exception as e:
        return json.dumps({'error': str(e)})

#route to display currently selected patients notes
@app.route('/showAddedNotes/<string:pat_number>')
def showAddedNotes(pat_number):
    if session.get('user'):
        #creating another session variable to handle the patients number
        session['patient_id'] = pat_number

        _note = session.get('patient_id')
        connGP = mysql.connect()
        cursor = connGP.cursor()
        #calling stored procedure to select all notes from the note table for the current patient
        cursor.callproc('sp_GetNotesByPatient', (_note,))
        data2 = cursor.fetchall()
        cursor.close()
        #display patient details through html page. notes contains all note details which is iterated through to display in webpage
        return render_template('showPatient.html', notes=data2)
    else:
        return render_template('error.html', error='Error No Access Please Sign In')

#route to insert a note
@app.route('/insertNote', methods=['POST'])
def insertNote():
    try:
        if session.get('user'):
            _notetitle = request.form['inputNoteTitle']
            _notecontent = request.form['inputNoteContent']
            _user = session.get('user')
            _patient = session.get('patient_id')

            if _notetitle and _notecontent:
                # connect to mysql
                connIN = mysql.connect()
                cursor = connIN.cursor()
                cursor.callproc('sp_addNote', (_notetitle, _notecontent, _user, _patient))
                data3 = cursor.fetchall()

                if len(data3) is 0:
                    connIN.commit()

                else:
                    return render_template('error.html', error='An error occurred!')
            else:
                return json.dumps({'html': '<span>Please enter all of the required fields</span>'})

        else:
            return render_template('error.html', error='Unauthorized Access')
    except Exception as e:
        return render_template('error.html', error=str(e))

#Route for displaying test cases of OCR results
@app.route('/tesseract')
def process_image():
    im = Image.open("static/Uploads/hand1.jpg")
    text = pytesseract.image_to_string(im, lang='eng')
    return render_template('tesseractResult.html', data=text)


if __name__ == "__main__":
    app.run(port=5000)
