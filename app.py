from flask import Flask, render_template, flash, url_for, redirect

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired

import psycopg2

from jobs.submit_job import submitJob

app = Flask(__name__)
# needed for form csrf_token
app.config['SECRET_KEY'] = 'secretkey'

class DescriptionForm(FlaskForm):
    description = StringField('Description', validators=[InputRequired()])

def getResults():
    postgres_conn = psycopg2.connect(
        dbname='playqueue',
        user='lemonade',
        password='supersecureadminpassword',
        host='localhost',
        port="5432",
    )
    cur = postgres_conn.cursor()
    
    cur.execute("SELECT * FROM results ORDER BY id ASC;")
    rows = cur.fetchall()
    
    cur.close()
    postgres_conn.close()
    return rows
    

@app.route('/', methods=['GET', 'POST']) 
def dashboard():
    rows = getResults()
    print(rows)
    
    form = DescriptionForm()
    if form.validate_on_submit():
        # actually submit
        submitJob(form.description.data)
        
        flash(f"Successfully submitted description: {form.description.data}", "success")  
        
        return redirect(url_for('dashboard'))
            
    return render_template('index.html', rows=rows, form=form)
    
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)