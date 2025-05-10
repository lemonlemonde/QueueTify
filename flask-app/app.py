from flask import Flask, jsonify, render_template, flash, url_for, redirect, request

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired

from flask_socketio import SocketIO, emit

import psycopg2

from submit_job import submitJob

app = Flask(__name__)
# needed for form csrf_token
app.config['SECRET_KEY'] = 'secretkey'
socketio = SocketIO(app)

@socketio.on('connect_success')
def handle_connect_success(json):
    print('Successfully connected with browser: ' + str(json))

class DescriptionForm(FlaskForm):
    description = StringField('Description', validators=[InputRequired()])

@app.route('/results', methods=['GET'])
def getResults():
    postgres_conn = psycopg2.connect(
        dbname='playqueue',
        user='lemonade',
        password='supersecureadminpassword',
        host='postgres',
        port="5432",
    )
    cur = postgres_conn.cursor()
    
    cur.execute("SELECT * FROM results ORDER BY id ASC;")
    rows = cur.fetchall()
    
    cur.close()
    postgres_conn.close()
    return jsonify(rows)

@app.route('/notify', methods=['POST'])
def notify():
    data = request.json
    status = data.get('status')
    
    print(data)
    
    if status == 'success':
        # worker sucessfully pushed to db
        socketio.emit('new_result', {'data': "success"})
        
    elif status == 'interrupt':
        # worker was keyboard interrupted
        socketio.emit('error', {'data': "interrupt"})
        
    elif status == 'error':
        # worker ran into error while pushing to db
        error = data.get('error')
        socketio.emit('error', {'data': str(error)})
    
    return '', 200

@app.route('/', methods=['GET', 'POST']) 
def dashboard():
    form = DescriptionForm()
    if form.validate_on_submit():
        # actually submit
        submitJob(form.description.data)
        
        flash(f"Successfully submitted description: `{form.description.data}`", "success")  
        
        return redirect(url_for('dashboard'))
            
    return render_template('index.html', form=form)
    
    
if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=5000, debug=True)
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)