from flask import render_template, redirect, url_for, flash, abort
from . import students
from .forms import StudentForm
from ..import db
from ..models import Student
from flask.ext.login import current_user, login_required


@students.route('/add', methods=['GET', 'POST'])
@login_required
def student_detail():
    form = StudentForm()
    if form.validate_on_submit():
        student = Student(surname=form.surname.data, first_name=form.first_name.data,
                          second_name=form.second_name.data,
                          email=form.email.data, admin_no=form.admin_no.data, phone_no=form.phone_no.data,
                          collegeprogram_id=1)

        db.session.add(student)
        db.session.commit()
        flash('The student info has been saved.')
        return redirect(url_for('main.index'))

    return render_template('student_detail.html', form=form)


@students.route('/profile/<first_name>', methods=['GET', 'POST'])
@login_required
def student_profile(first_name):
    student = Student.query.filter_by(first_name=first_name).first()
    if student is None:
        abort(404)
    return render_template('student_profile.html', student=student)


@students.route('/all', methods=['GET', 'POST'])
@login_required
def view_students():
    students = Student.query.order_by('first_name').all()
    return render_template('view_students.html', students=students)


@students.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_student():
    form = StudentForm()
    student = Student.query.filter_by(email=current_user.email).first()
    if not form.validate_on_submit:

        student.surname = form.surname.data
        student.first_name = form.first_name.data
        student.second_name = form.second_name.data
        student.admin_no = form.admin_no.data
        student.phone_no = form.phone_no.data
        student.email = form.email.data
        # db.session.add(Student(surname=current_user.surname, first_name=current_user.first_name,
        #                        second_name=current_user.second_name,
        #                        email=current_user.email, admin_no=current_user.admin_no, phone_no=current_user.phone_no,
        #                        collegeprogram_id=1))
        db.session.add(student)
        flash('Your profile has been updated.')
        return redirect(url_for('main.index'))

    form.surname.data = student.surname
    form.first_name.data = student.first_name
    form.email.data = student.email
    form.admin_no.data = student.admin_no
    form.phone_no.data = student.phone_no
    form.second_name.data = student.second_name
    return render_template('student_detail.html', form=form)
