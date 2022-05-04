from flask import Flask , render_template,request,session,flash,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
import sqlite3 as sql

cor = Flask(__name__)


cor.config['SECRET_KEY'] = '311ac8e910401b8bc4fb'
cor.config['SQLALCHEMY_TRACK_MODIFICATIONS '] = False
cor.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sub.db'

db = SQLAlchemy(cor)

class Student(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	student_name = db.Column(db.String(30), nullable=False)
	registration_number = db.Column(db.Integer, nullable=False)
	email = db.Column(db.String(30), nullable=False)
	class_bach = db.Column(db.String(20), nullable=False)
	password = db.Column(db.String(40), nullable=False)
	confirm_password = db.Column(db.String(40), nullable=False)



@cor.route("/act", methods=['POST', 'GET'])
def act():
	if request.method=="POST":
		c = sql.connect('sub.db')
		a =  c.cursor() 
		a.execute(
			    'INSERT INTO Student (student_name,registration_number,email,class_bach,password,confirm_password) values (?,?,?,?,?,?)',
			    (
			        request.form.get('student_name', type=str),
			        request.form.get('registration_number', type=int),
			        request.form.get('email', type=str),
			        request.form.get('class_bach', type=str),
			        request.form.get('password', type=str),
			        request.form.get('confirm_password', type=str)

			    )
			)
		c.commit()
		
		return 'send'



@cor.route('/about_page')
def about_page():
	c = sql.connect('sub.db')
	a = c.cursor()
	a.execute('SELECT * FROM Student')

	return render_template('about.html', data = a.fetchall())



@cor.route('/update/<int:num>', methods=['GET','POST'])
def update_student(num):
	conn = sql.connect('sub.db')
	cur = conn.cursor()
	if request.method == 'POST':
		_id = num
		student_name = request.form['student_name']
		registration_number = request.form['registration_number']
		email = request.form['email']
		class_bach = request.form['class_bach']
		password = request.form['password']
		confirm_password = request.form['confirm_password']

		cur.execute("UPDATE Student SET student_name = ?, registration_number = ?, email = ?, class_bach = ?, password = ?, confirm_password = ? WHERE id = ?",
                    (student_name, registration_number, email, class_bach, password, confirm_password, _id))
		conn.commit()
		flash("Updating Successfully")
	cur.execute("SELECT * FROM Student WHERE id = ?", (num,))
	item = cur.fetchone()
	conn.close()
	#return render_template("edit.html", item=item)
	return render_template("update.html", Student=Student, item=item)


@cor.route('/delete_student/<int:num>', methods=['POST', 'GET'])
def delete_student(num):

    conn = sql.connect('sub.db')
    cur = conn.cursor()
        
    cur.execute("DELETE FROM Student WHERE id = ?", (num,))

    conn.commit()

    conn.close()
    flash('Student Removed Successfully')
    return redirect(url_for('about_page'))



	
@cor.route("/home")
def home():
	return render_template("home.html", Student = Student )




@cor.route("/pagination")
def pagination():
	c = sql.connect('sub.db')
	a = c.cursor()
	a.execute('SELECT * FROM Student')
	return render_template("pagination.html",data=a.fetchall())
























if __name__ == '__main__':
	cor.run(debug=True)