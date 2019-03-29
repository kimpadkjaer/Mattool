from app import app, db, mail
from flask import render_template, url_for, redirect, flash, request
from app.models import Mat1, User, Mat1tests
from app.forms import Mat1Form, KontaktForm, Mat1testsForm, LoginForm, RegistrationForm, Edit_userForm
from sqlalchemy.sql.expression import case, and_
from flask_login import current_user, login_user, logout_user, login_required
from app.functions import redirect_url, random_bg_picture, procent
import logging
from flask_mail import Message


@app.route('/')
@app.route('/index')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('user', username=current_user.username))

    form=RegistrationForm()
    l_form=LoginForm()

    return render_template('index.html', title="MAT | retteværktøj: Forside", form=form, l_form=l_form)


@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))


    form=RegistrationForm()
    l_form = LoginForm()

    if request.method == 'POST':

        if form.validate_on_submit():
            user = User(username=form.username.data, email=form.email.data, school=form.school.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Tillykke, du er nu oprettet som bruger! Du kan logge ind nedenfor.')
            return redirect(url_for('index'))



    return render_template('index.html', title="MAT | retteværktøj: Forside", l_form=l_form, form=form)


@app.route('/edit_user', methods=['GET', 'POST'])
@login_required
def edit_user():
    form = Edit_userForm()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.school = form.school.data
        db.session.commit()
        return redirect(url_for('user', username=current_user.username))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.school.data = current_user.school

    random_bg = random_bg_picture()

    title = "MAT | Ændringer for bruger {}".format(current_user.username)

    return render_template('edit_user.html', title=title, form=form, random_bg=random_bg)


@app.route('/login', methods=['GET', 'POST'])
def login(*args, **kwargs):
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form=RegistrationForm()
    l_form = LoginForm()

    logger = logging.getLogger(__name__)

    if request.method == 'POST':
        if l_form.validate_on_submit():
            user = User.query.filter_by(username=l_form.username.data).first()
            if user is None or not user.check_password(l_form.password.data):
                flash('Forkert brugernavn eller kodeord')
                logger.warn(f"Brugeren '{l_form.username.data}' forsøger at logge ind, men fejler")
                return redirect(url_for('index'))
            login_user(user, remember=l_form.remember_me.data)
            return redirect('index')

    return render_template('index.html', title="MAT | retteværktøj: Forside", l_form=l_form, form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('Du er nu logget ud...')
    return redirect(url_for('index'))

@app.route('/user/<username>')
@login_required
def user(username):

    mat1_tests = Mat1.query.filter_by(user_id=current_user.id).all()

    random_bg = random_bg_picture()

    title = "MAT | Min side: {}".format(current_user.username)

    return render_template('user.html', title=title, user=user, mat1_tests=mat1_tests, random_bg=random_bg)


@app.route('/kontakt', methods=['POST', 'GET'])
def kontakt():

    form = KontaktForm()

    if form.validate_on_submit():
        msg = Message('Email fra Mat | Retteværktøj', sender="siri.padkjaer@gmail.com", recipients=['siri.padkjaer@gmail.com', 'padbassen@hotmail.com'])
        msg.body = "Email fra: {}, {}. \n \nBesked:\n{}".format(form.navn.data, form.email.data, form.besked.data)
        mail.send(msg)

        flash('Beskeden er blevet sendt. Jeg svarer hurtigst muligt.')

        return redirect(url_for('kontakt'))

    return render_template('kontakt.html', title='MAT | Kontakt', form=form)


@app.route('/version')
def version():
    return render_template('version.html')




@app.route('/log')
def log_test():

    logger = logging.getLogger(__name__)
    logger.info('Testing')
    return "Hello"



# MAT1 test logic ----------------------------------------------------------- start --->

@app.route('/mat1_test_show/<int:id>', methods=['GET', 'POST'])
@login_required
def mat1_test_show(id):
    mat1_show = Mat1.query.filter_by(id=id).first_or_404()

    if not current_user.id == mat1_show.user_id:
        return redirect('mat1')

    mat1_get_id = mat1_show.id

    form = Mat1testsForm()

    if form.validate_on_submit():
        mat1test_add = Mat1tests(elev=form.elev.data, a1=form.a1.data, b1=form.b1.data, b2=form.b2.data, c1=form.c1.data, d1=form.d1.data, d2=form.d2.data, d3=form.d3.data, d4=form.d4.data, e1=form.e1.data, comments=form.comments.data,
        mat1_sum=form.a1.data + form.b1.data + form.b2.data + form.c1.data + form.d1.data + form.d2.data + form.d3.data + form.d4.data + form.e1.data,
        mat1_id=mat1_get_id)

        db.session.add(mat1test_add)
        db.session.commit()

        flash('Eleven er blevet tilføjet')

        return redirect(url_for('mat1_test_show', id=id))


    mat1_elev_id = Mat1tests.id.label("id")
    elevname = Mat1tests.elev.label('elev')
    a_1 = Mat1tests.a1.label('a1')
    b_1 = Mat1tests.b1.label('b1')
    b_2 = Mat1tests.b2.label('b2')
    c_1 = Mat1tests.c1.label('c1')
    d_1 = Mat1tests.d1.label('d1')
    d_2 = Mat1tests.d2.label('d2')
    d_3 = Mat1tests.d3.label('d3')
    d_4 = Mat1tests.d4.label('d4')
    e_1 = Mat1tests.e1.label('e1')
    mat1_summen = Mat1tests.mat1_sum.label('sum')
    comments = Mat1tests.comments.label('comments')

    csum = db.func.sum(Mat1tests.a1 + Mat1tests.b1 + Mat1tests.b2 + Mat1tests.c1 + Mat1tests.d1 + Mat1tests.d2 + Mat1tests.d3 + Mat1tests.d4 + Mat1tests.e1).label("summen")

    from_0_to_33 = and_(csum >=0, csum <=33)
    from_34_to_63 = and_(csum >=34, csum <=63)
    from_64_to_79 = and_(csum >=64, csum <=79)
    from_80_to_88 = and_(csum >=80, csum <=88)
    from_89_to_96 = and_(csum >=89, csum <=96)
    from_97_to_101 = and_(csum >=97, csum <=101)
    from_102_to_105 = and_(csum >=102, csum <=105)
    from_106_to_109 = and_(csum >=106, csum <=109)
    from_110_to_111 = and_(csum >=110, csum <=11)
    from_112_to_117 = and_(csum >=112, csum <=117)

    csum_cases = case([
        (from_0_to_33, "C0"),
        (from_34_to_63, "C1"),
        (from_64_to_79, "C2"),
        (from_80_to_88, "C3"),
        (from_89_to_96, "C4"),
        (from_97_to_101, "C5"),
        (from_102_to_105, "C6"),
        (from_106_to_109, "C7"),
        (from_110_to_111, "C8"),
        (from_112_to_117, "C9-C10")
    ]).label("csum")

    c_score = db.session.query(csum_cases, mat1_elev_id, elevname, a_1, b_1, b_2, c_1, d_1, d_2, d_3, d_4, e_1, mat1_summen, comments).filter(Mat1tests.mat1_id == mat1_show.id).group_by(Mat1tests.id).all()

    #------------ diagram data start ---------------->

    c_null_value = db.session.query(Mat1tests).filter(and_(Mat1tests.mat1_sum >=0, Mat1tests.mat1_sum <=33)).filter(Mat1tests.mat1_id == mat1_show.id).count()
    c_one_value = db.session.query(Mat1tests).filter(and_(Mat1tests.mat1_sum >=34, Mat1tests.mat1_sum <=63)).filter(Mat1tests.mat1_id == mat1_show.id).count()
    c_two_value = db.session.query(Mat1tests).filter(and_(Mat1tests.mat1_sum >=64, Mat1tests.mat1_sum <=79)).filter(Mat1tests.mat1_id == mat1_show.id).count()
    c_three_value = db.session.query(Mat1tests).filter(and_(Mat1tests.mat1_sum >=80, Mat1tests.mat1_sum <=88)).filter(Mat1tests.mat1_id == mat1_show.id).count()
    c_four_value = db.session.query(Mat1tests).filter(and_(Mat1tests.mat1_sum >=89, Mat1tests.mat1_sum <=96)).filter(Mat1tests.mat1_id == mat1_show.id).count()
    c_five_value = db.session.query(Mat1tests).filter(and_(Mat1tests.mat1_sum >=97, Mat1tests.mat1_sum <=101)).filter(Mat1tests.mat1_id == mat1_show.id).count()
    c_six_value = db.session.query(Mat1tests).filter(and_(Mat1tests.mat1_sum >=102, Mat1tests.mat1_sum <=105)).filter(Mat1tests.mat1_id == mat1_show.id).count()
    c_seven_value = db.session.query(Mat1tests).filter(and_(Mat1tests.mat1_sum >=106, Mat1tests.mat1_sum <=109)).filter(Mat1tests.mat1_id == mat1_show.id).count()
    c_eight_value = db.session.query(Mat1tests).filter(and_(Mat1tests.mat1_sum >=110, Mat1tests.mat1_sum <=111)).filter(Mat1tests.mat1_id == mat1_show.id).count()
    c_nine_value = db.session.query(Mat1tests).filter(and_(Mat1tests.mat1_sum >=112, Mat1tests.mat1_sum <=117)).filter(Mat1tests.mat1_id == mat1_show.id).count()

    labels = ["C0","C1","C2","C3","C4","C5","C6","C7","C8","C9-10"]
    values = []

    values.insert(0, c_null_value)
    values.insert(1, c_one_value)
    values.insert(2, c_two_value)
    values.insert(3, c_three_value)
    values.insert(4, c_four_value)
    values.insert(5, c_five_value)
    values.insert(6, c_six_value)
    values.insert(7, c_seven_value)
    values.insert(8, c_eight_value)
    values.insert(9, c_nine_value)

    #------------ diagram data slut ---------------->

    #------------ c-niveau elever start ---------------->

    c_level_null = Mat1tests.query.filter(and_(Mat1tests.mat1_sum >=0, Mat1tests.mat1_sum <=33)).filter(Mat1tests.mat1_id == mat1_show.id).all()
    c_level_one = db.session.query(Mat1tests).filter(and_(Mat1tests.mat1_sum >=34, Mat1tests.mat1_sum <=63)).filter(Mat1tests.mat1_id == mat1_show.id).all()
    c_level_two = db.session.query(Mat1tests).filter(and_(Mat1tests.mat1_sum >=64, Mat1tests.mat1_sum <=79)).filter(Mat1tests.mat1_id == mat1_show.id).all()
    c_level_three = db.session.query(Mat1tests).filter(and_(Mat1tests.mat1_sum >=80, Mat1tests.mat1_sum <=88)).filter(Mat1tests.mat1_id == mat1_show.id).all()
    c_level_four = db.session.query(Mat1tests).filter(and_(Mat1tests.mat1_sum >=89, Mat1tests.mat1_sum <=96)).filter(Mat1tests.mat1_id == mat1_show.id).all()
    c_level_five = db.session.query(Mat1tests).filter(and_(Mat1tests.mat1_sum >=97, Mat1tests.mat1_sum <=101)).filter(Mat1tests.mat1_id == mat1_show.id).all()
    c_level_six = db.session.query(Mat1tests).filter(and_(Mat1tests.mat1_sum >=102, Mat1tests.mat1_sum <=105)).filter(Mat1tests.mat1_id == mat1_show.id).all()
    c_level_seven = db.session.query(Mat1tests).filter(and_(Mat1tests.mat1_sum >=106, Mat1tests.mat1_sum <=109)).filter(Mat1tests.mat1_id == mat1_show.id).all()
    c_level_eight = db.session.query(Mat1tests).filter(and_(Mat1tests.mat1_sum >=110, Mat1tests.mat1_sum <=111)).filter(Mat1tests.mat1_id == mat1_show.id).all()
    c_level_nine = db.session.query(Mat1tests).filter(and_(Mat1tests.mat1_sum >=112, Mat1tests.mat1_sum <=117)).filter(Mat1tests.mat1_id == mat1_show.id).all()


    #------------ c-niveau elever slut ---------------->

    elev_antal = Mat1tests.query.filter(Mat1tests.mat1_id == mat1_show.id).count()

    #------------ opmærksomhedspunkter elever start ---------------->

    #------------- ikke indlært---------

    a1_red = Mat1tests.query.filter(and_(Mat1tests.a1 >=0, Mat1tests.a1 <=19)).filter(Mat1tests.mat1_id == mat1_show.id).all()
    b1_red = Mat1tests.query.filter(and_(Mat1tests.b1 >=0, Mat1tests.b1 <=17)).filter(Mat1tests.mat1_id == mat1_show.id).all()
    b2_red = Mat1tests.query.filter(and_(Mat1tests.b2 >=0, Mat1tests.b2 <=11)).filter(Mat1tests.mat1_id == mat1_show.id).all()
    c1_red = Mat1tests.query.filter(and_(Mat1tests.c1 >=0, Mat1tests.c1 <=4)).filter(Mat1tests.mat1_id == mat1_show.id).all()
    d1_red = Mat1tests.query.filter(and_(Mat1tests.d1 >=0, Mat1tests.d1 <=3)).filter(Mat1tests.mat1_id == mat1_show.id).all()
    d2_red = Mat1tests.query.filter(and_(Mat1tests.d2 >=0, Mat1tests.d2 <=1)).filter(Mat1tests.mat1_id == mat1_show.id).all()
    d3_red = Mat1tests.query.filter(and_(Mat1tests.d3 >=0, Mat1tests.d3 <=2)).filter(Mat1tests.mat1_id == mat1_show.id).all()
    d4_red = Mat1tests.query.filter(and_(Mat1tests.d4 >=0, Mat1tests.d4 <=5)).filter(Mat1tests.mat1_id == mat1_show.id).all()
    e1_red = Mat1tests.query.filter(and_(Mat1tests.e1 >=0, Mat1tests.e1 <=3)).filter(Mat1tests.mat1_id == mat1_show.id).all()

    a1_red_count = Mat1tests.query.filter(and_(Mat1tests.a1 >=0, Mat1tests.a1 <=19)).filter(Mat1tests.mat1_id == mat1_show.id).count()
    b1_red_count = Mat1tests.query.filter(and_(Mat1tests.b1 >=0, Mat1tests.b1 <=17)).filter(Mat1tests.mat1_id == mat1_show.id).count()
    b2_red_count = Mat1tests.query.filter(and_(Mat1tests.b2 >=0, Mat1tests.b2 <=11)).filter(Mat1tests.mat1_id == mat1_show.id).count()
    c1_red_count = Mat1tests.query.filter(and_(Mat1tests.c1 >=0, Mat1tests.c1 <=4)).filter(Mat1tests.mat1_id == mat1_show.id).count()
    d1_red_count = Mat1tests.query.filter(and_(Mat1tests.d1 >=0, Mat1tests.d1 <=3)).filter(Mat1tests.mat1_id == mat1_show.id).count()
    d2_red_count = Mat1tests.query.filter(and_(Mat1tests.d2 >=0, Mat1tests.d2 <=1)).filter(Mat1tests.mat1_id == mat1_show.id).count()
    d3_red_count = Mat1tests.query.filter(and_(Mat1tests.d3 >=0, Mat1tests.d3 <=2)).filter(Mat1tests.mat1_id == mat1_show.id).count()
    d4_red_count = Mat1tests.query.filter(and_(Mat1tests.d4 >=0, Mat1tests.d4 <=5)).filter(Mat1tests.mat1_id == mat1_show.id).count()
    e1_red_count = Mat1tests.query.filter(and_(Mat1tests.e1 >=0, Mat1tests.e1 <=3)).filter(Mat1tests.mat1_id == mat1_show.id).count()

    #------------- usikkert indlært---------

    a1_yellow = Mat1tests.query.filter(and_(Mat1tests.a1 >=20, Mat1tests.a1 <=22)).filter(Mat1tests.mat1_id == mat1_show.id).all()
    b1_yellow = Mat1tests.query.filter(and_(Mat1tests.b1 >=18, Mat1tests.b1 <=20)).filter(Mat1tests.mat1_id == mat1_show.id).all()
    b2_yellow = Mat1tests.query.filter(and_(Mat1tests.b2 >=12, Mat1tests.b2 <=18)).filter(Mat1tests.mat1_id == mat1_show.id).all()
    c1_yellow = Mat1tests.query.filter(and_(Mat1tests.c1 >=5, Mat1tests.c1 <=6)).filter(Mat1tests.mat1_id == mat1_show.id).all()
    d1_yellow = Mat1tests.query.filter(Mat1tests.d1 ==3).filter(Mat1tests.mat1_id == mat1_show.id).all()
    d2_yellow = Mat1tests.query.filter(Mat1tests.d2 ==2).filter(Mat1tests.mat1_id == mat1_show.id).all()
    d3_yellow = Mat1tests.query.filter(Mat1tests.d3 ==3).filter(Mat1tests.mat1_id == mat1_show.id).all()
    d4_yellow = Mat1tests.query.filter(Mat1tests.d4 ==6).filter(Mat1tests.mat1_id == mat1_show.id).all()
    e1_yellow = Mat1tests.query.filter(Mat1tests.e1 ==4).filter(Mat1tests.mat1_id == mat1_show.id).all()

    a1_yellow_count = Mat1tests.query.filter(and_(Mat1tests.a1 >=20, Mat1tests.a1 <=22)).filter(Mat1tests.mat1_id == mat1_show.id).count()
    b1_yellow_count = Mat1tests.query.filter(and_(Mat1tests.b1 >=18, Mat1tests.b1 <=20)).filter(Mat1tests.mat1_id == mat1_show.id).count()
    b2_yellow_count = Mat1tests.query.filter(and_(Mat1tests.b2 >=12, Mat1tests.b2 <=18)).filter(Mat1tests.mat1_id == mat1_show.id).count()
    c1_yellow_count = Mat1tests.query.filter(and_(Mat1tests.c1 >=5, Mat1tests.c1 <=6)).filter(Mat1tests.mat1_id == mat1_show.id).count()
    d1_yellow_count = Mat1tests.query.filter(Mat1tests.d1 ==3).filter(Mat1tests.mat1_id == mat1_show.id).count()
    d2_yellow_count = Mat1tests.query.filter(Mat1tests.d2 ==2).filter(Mat1tests.mat1_id == mat1_show.id).count()
    d3_yellow_count = Mat1tests.query.filter(Mat1tests.d3 ==3).filter(Mat1tests.mat1_id == mat1_show.id).count()
    d4_yellow_count = Mat1tests.query.filter(Mat1tests.d4 ==6).filter(Mat1tests.mat1_id == mat1_show.id).count()
    e1_yellow_count = Mat1tests.query.filter(Mat1tests.e1 ==4).filter(Mat1tests.mat1_id == mat1_show.id).count()

    #------------- ikke og usikkert indlært sum ---------

    a1_red_yellow_sum = a1_red_count + a1_yellow_count
    b1_red_yellow_sum = b1_red_count + b1_yellow_count
    b2_red_yellow_sum = b2_red_count + b2_yellow_count
    c1_red_yellow_sum = c1_red_count + c1_yellow_count
    d1_red_yellow_sum = d1_red_count + d1_yellow_count
    d2_red_yellow_sum = d2_red_count + d2_yellow_count
    d3_red_yellow_sum = d3_red_count + d3_yellow_count
    d4_red_yellow_sum = d4_red_count + d4_yellow_count
    e1_red_yellow_sum = e1_red_count + e1_yellow_count

    #------------- ikke og usikkert procenter ---------


    a1_procent = procent(a1_red_yellow_sum, elev_antal)
    b1_procent = procent(b1_red_yellow_sum, elev_antal)
    b2_procent = procent(b2_red_yellow_sum, elev_antal)
    c1_procent = procent(c1_red_yellow_sum, elev_antal)
    d1_procent = procent(d1_red_yellow_sum, elev_antal)
    d2_procent = procent(d2_red_yellow_sum, elev_antal)
    d3_procent = procent(d3_red_yellow_sum, elev_antal)
    d4_procent = procent(d4_red_yellow_sum, elev_antal)
    e1_procent = procent(e1_red_yellow_sum, elev_antal)


    #------------ opmærksomhedspunkter elever slut ---------------->

    title = "MAT1 | {}".format(mat1_show.title)

    return render_template('mat_test_show.html', elev_antal=elev_antal,
    a1_procent=a1_procent, b1_procent=b1_procent, b2_procent=b2_procent, c1_procent=c1_procent, d1_procent=d1_procent, d2_procent=d2_procent, d3_procent=d3_procent, d4_procent=d4_procent, e1_procent=e1_procent,
    a1_red_yellow_sum=a1_red_yellow_sum, b1_red_yellow_sum=b1_red_yellow_sum, b2_red_yellow_sum=b2_red_yellow_sum, c1_red_yellow_sum=c1_red_yellow_sum, d1_red_yellow_sum=d1_red_yellow_sum, d2_red_yellow_sum=d2_red_yellow_sum, d3_red_yellow_sum=d3_red_yellow_sum, d4_red_yellow_sum=d4_red_yellow_sum, e1_red_yellow_sum=e1_red_yellow_sum,
    a1_yellow=a1_yellow, b1_yellow=b1_yellow, b2_yellow=b2_yellow, c1_yellow=c1_yellow, d1_yellow=d1_yellow, d2_yellow=d2_yellow, d3_yellow=d3_yellow, d4_yellow=d4_yellow, e1_yellow=e1_yellow,
    a1_red = a1_red, b1_red=b1_red, b2_red=b2_red, c1_red=c1_red, d1_red=d1_red, d2_red=d2_red, d3_red=d3_red, d4_red=d4_red, e1_red=e1_red,
    c_level_null=c_level_null, c_level_one=c_level_one, c_level_two=c_level_two, c_level_three=c_level_three, c_level_four=c_level_four, c_level_five=c_level_five, c_level_six=c_level_six, c_level_seven=c_level_seven, c_level_eight=c_level_eight, c_level_nine=c_level_nine,
    c_nine_value=c_nine_value, c_null_value=c_null_value, c_one_value=c_one_value, c_two_value=c_two_value, c_three_value=c_three_value, c_four_value=c_four_value, c_five_value=c_five_value, c_six_value=c_six_value, c_seven_value=c_seven_value, c_eight_value=c_eight_value,
    form=form, mat1_show=mat1_show, c_score=c_score, labels=labels, values=values, title=title)


@app.route('/mat1', methods=['GET', 'POST'])
@login_required
def mat1():
    form = Mat1Form()
    if form.validate_on_submit():
        add_mat1 = Mat1(title=form.title.data, klasse=form.klasse.data, beskrivelse=form.beskrivelse.data, mat1=current_user)

        db.session.add(add_mat1)
        db.session.commit()

        flash('Prøven er blevet tilføjet.')

        return redirect(url_for('mat1'))

    mat1_test_id = Mat1.id.label("mat1_test_id")
    mat1_tests = Mat1.query.filter_by(user_id=current_user.id).all()

    title = "MAT1 | prøver oprettet af {}".format(current_user)


    return render_template('mat1.html', mat1_tests=mat1_tests, form=form, title=title)


@app.route('/mat1_delete_test/<int:mat1_id>/delete', methods=['POST'])
@login_required
def mat1_delete_test(mat1_id):
    test = Mat1.query.get_or_404(mat1_id)
    db.session.delete(test)
    db.session.commit()
    flash('Peøven er blevet slettet.')

    return redirect(url_for('mat1'))


@app.route('/mat1_delete_elev/<int:mat1tests_id>/delete', methods=['POST'])
@login_required
def mat1_delete_elev(mat1tests_id):
    elev = Mat1tests.query.get_or_404(mat1tests_id)
    db.session.delete(elev)
    db.session.commit()
    flash('Eleven er blevet slettet')

    return redirect(redirect_url())


# MAT1 test logic ----------------------------------------------------------- end --->
