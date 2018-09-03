from flask import Flask, render_template, json, request, redirect, url_for, session
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
from PIL import Image
import pytesseract

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


@app.route('/')
def main():
    if session.get('user'):
        return render_template('userHome.html')
    else:
        return redirect(url_for('showSignIn'))


@app.route('/showSignIn')
def showSignIn():
    return render_template('signin.html')


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


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


@app.route('/validateLogin', methods=['POST'])
def validateLogin():
    try:
        _staffid = request.form['inputStaffId']
        _password = request.form['inputPassword']

        # connect to mysql
        connVL = mysql.connect()
        cursor = connVL.cursor()
        cursor.callproc('sp_validateLogin', (_staffid,))
        data = cursor.fetchall()

        if len(data) > 0:
            if check_password_hash(str(data[0][2]),_password):
                session['user'] = data[0][3] + ' ' + data[0][4]
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


@app.route('/showAddPatient')
def showAddPatient():
    if session.get('user'):
        connPL = mysql.connect()
        cursor = connPL.cursor()
        cursor.callproc('sp_selectEmployees')
        data = cursor.fetchall()
        return render_template('addPatient.html', employees=data)
    else:
        return render_template('error.html', error ='Error No Access Please Sign In')


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


@app.route('/getPatients')
def getPatients():
    try:
        if session.get('user'):
            _user = session.get('user_id')
 
            connGP = mysql.connect()
            cursor = connGP.cursor()
            cursor.callproc('sp_GetPatientByAccess', (_user,))
            data = cursor.fetchall()

            return render_template('showPatients.html', patients=data)
        else:
            return render_template('error.html',error='Error No Access Please Sign In')
    except Exception as e:
        return render_template('error.html', error=str(e))


@app.route('/addNote/<string:pat_note>')
def addNote(pat_note):
    try:
        _patientId = pat_note
        session['patient_id'] = _patientId
        return render_template('addNote.html')
        
    except Exception as e:
        return json.dumps({'error': str(e)})


@app.route('/showAddedNotes/<string:pat_number>')
def showAddedNotes(pat_number):
    if session.get('user'):
        session['patient_id'] = pat_number

        _note = session.get('patient_id')
        connGP = mysql.connect()
        cursor = connGP.cursor()
        cursor.callproc('sp_GetNotesByPatient', (_note,))
        data2 = cursor.fetchall()
        cursor.close()
        return render_template('showPatient.html', notes=data2)
    else:
        return render_template('error.html', error='Error No Access Please Sign In')


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


@app.route('/tesseract')
def process_image():
    im = Image.open("static/Uploads/hand1.jpg")
    text = pytesseract.image_to_string(im, lang='eng')
    return render_template('tesseractResult.html', data=text)


if __name__ == "__main__":
    app.run(port=5000)
