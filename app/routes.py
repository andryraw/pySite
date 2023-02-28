from app import app, db, mail, ts
from itsdangerous import SignatureExpired
from flask import render_template, url_for, redirect, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from flask_mail import Message
from app.forms import RegistrationForm, LoginForm, EditForm,\
    AddFilmForm, AddFilmGenre, AddFilmDirector,\
    AddGenre, AddDirector
from app.models import User, Film, Director, Genre


# main page
@app.route('/')
@app.route('/index')
def index():
    if current_user.is_anonymous:
        return redirect(url_for('login'))
    return render_template('index.html', title='Home page')


# user page
@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


# registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        u = User(first_name=form.first_name.data, last_name=form.last_name.data,
                username=form.username.data, email=form.email.data,
                about_me=form.about_me.data)
        u.set_password(form.password_1.data)
        db.session.add(u)
        db.session.commit()
        token = ts.dumps(u.email, salt='email-confirm')
        link = url_for('confirm_email', token=token, _external=True)
        msg = Message('Confirm your email', recipients=[u.email])
        msg.body = f"Please confirm your email \n {link}"
        mail.send(msg)
        flash('You are registered! Now confirm your email')
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', form=form)


@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = ts.loads(token, salt='email-confirm', max_age=30)
    except SignatureExpired:
        flash('The token is expired!')
        return redirect(url_for('index'))
    confirm_user = User.query.filter_by(email=email).first()
    if confirm_user.confirm:
        flash('Your address has already been verified')
    else:
        confirm_user.confirm = True
        db.session.commit()
        flash('Your email is successfully confirmed!')
    return redirect(url_for('index'))


# edit profile
@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditForm()
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        current_user.set_password(form.password_1.data)
        db.session.commit()
        flash('Profile changes have been saved')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me
    return render_template('edit.html', title='Edit profile', form=form)


# login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        l_user = User.query.filter_by(username=form.username.data).first() # get uname from db
        if l_user is None or not l_user.check_password(form.password.data):
            flash('Invalid username or password!')
            return redirect(url_for('login'))
        if l_user.confirm:
            login_user(l_user, remember=form.remember_me.data)
            return redirect(url_for('index'))
        else:
            flash("Your account hasn't been verified")
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


# delete account
@app.route('/delete')
@login_required
def delete():
    user_id = current_user.get_id()
    u = User.query.get(user_id)
    db.session.delete(u)
    db.session.commit()
    flash('Your account has been deleted')
    return redirect(url_for('index'))


# -------------------- film section --------------------

@app.route('/film/list')
@login_required
def film_list():
    list_of_films = Film.query.all()
    return render_template('film_list.html', title='Film list', list_of_films=list_of_films)


@app.route('/film/add_film', methods=['GET', 'POST'])
@login_required
def add_film():
    form = AddFilmForm()
    if form.validate_on_submit():
        f = Film(name=form.name.data, type=form.type.data, duration=form.duration.data,
                 year=form.year.data, country=form.country.data)
        db.session.add(f)
        db.session.commit()
        flash('Film successfully added!')
    return render_template('add_film.html', title='Add new film', form=form)


# film info
@app.route('/film/<id>')
@login_required
def film_info(id):
    film = Film.query.filter_by(id=id).first_or_404()
    return render_template('film_info.html', title=film, film=film)


# add genres to film
@app.route('/film/<id>/genres', methods=['GET', 'POST'])
@login_required
def film_genres(id):
    form = AddFilmGenre()
    if form.validate_on_submit():
        film = Film.query.filter_by(id=id).first_or_404()
        genre = Genre.query.filter_by(name=form.genres.data).first()
        film.genres.append(genre)
        db.session.commit()
        flash('Genre added!')
    return render_template('add_film_genres.html', title='Add film genre', form=form)


# add director to film
@app.route('/film/<id>/director', methods=['GET', 'POST'])
@login_required
def film_director(id):
    form = AddFilmDirector()
    if form.validate_on_submit():
        film = Film.query.filter_by(id=id).first_or_404()
        director = Director.query.filter_by(name=form.director.data).first_or_404()
        film.director = director
        db.session.commit()
        flash('Director added!')
    return render_template('add_film_director.html', title='Add film director', form=form)


# film edit
@app.route('/film/<id>/edit')
@login_required
def film_edit(id):
    film = Film.query.filter_by(id=id).first_or_404()
    return render_template('film_info.html', film=film)


# -------------------- director and genre --------------------

@app.route('/genre_add', methods=['GET', 'POST'])
@login_required
def add_genre():
    form = AddGenre()
    if form.validate_on_submit():
        genre = Genre(name=form.name.data)
        db.session.add(genre)
        db.session.commit()
        flash('Genre added!')
        return redirect(url_for('add_genre'))
    return render_template('/add_genre.html', title='New genre', form=form)


@app.route('/director_add', methods=['GET', 'POST'])
@login_required
def add_director():
    form = AddDirector()
    if form.validate_on_submit():
        director = Director(name=form.name.data)
        db.session.add(director)
        db.session.commit()
        flash('Director added!')
        return redirect(url_for('add_director'))
    return render_template('/add_director.html', title='New director', form=form)
