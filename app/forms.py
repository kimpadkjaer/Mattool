from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, TextAreaField, SelectField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, NumberRange, InputRequired
from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Brugernavn', validators=[DataRequired("Du skal vælge et brugernavn.")])
    email = StringField('Email', validators=[DataRequired("Du skal indtaste din email adresse."), Email("Du har ikke indtastet en gyldig email adresse.")])
    password = PasswordField('Kodeord', validators=[DataRequired("Du skal vælge et kodeord")])
    password2 = PasswordField('Gentag kodeordet', validators=[DataRequired("Du skal gentage kodeordet"), EqualTo('password', "Kodeordene er ikke ens")])

    school = SelectField('Hvilken kommune arbejder du i?',
    choices=[('København','København'), ('Frederikberg','Frederikberg'), ('Gentofte','Gentofte'), ('Gladsaxe','Gladsaxe'), ('Helsingør','Helsingør'),
    ('Rudersdal','Rudersdal'), ('Lyngby-Taarbæk','Lyngby-Taarbæk'), ('Hvidore','Hvidore'), ('Hillerød','Hillerød'), ('Høje-Taastrup','Høje-Taastrup'), ('Ballerup','Ballerup'),
    ('Frederikssund','Frederikssund'), ('Tårnby','Tårnby'), ('Egedal','Egedal'), ('Gribskov','Gribskov'), ('Furesø','Furesø'), ('Fredensborg','Fredensborg'),
    ('Rødovre','Rødovre'), ('Brøndby','Brøndby'), ('Herlev','Herlev'), ('Albertslund','Albertslund'), ('Allerød','Allerød'), ('Hørsholm','Hørsholm'), ('Ishøj','Ishøj'),
    ('Glostrup','Glostrup'), ('Vallensbæk','Vallensbæk'), ('Dragør','Dragør'), ('Aarhus','Aarhus'), ('Randers','Randers'), ('Viborg','Viborg'), ('Silkeborg','Silkeborg'),
    ('Horsens','Horsens'), ('Herning','Herning'), ('Skanderborg','Skanderborg'), ('Holstebro','Holstebro'), ('Rinkøbing-skjern','Ringkøbing-skjern'), ('Favrskov','Farvskov'),
    ('Hedensted','Hedensted'), ('Skive','Skive'), ('Syddjurs','Syddjurs'), ('Norddjurs','Norddjurs'), ('Ikast-Brande','Ikast-Brande'), ('Odder','Odder'), ('Struer','Struer'),
    ('Lemvig','Lemvig'), ('Samsø','Samsø'), ('Aalborg','Aalborg'), ('Hjørring','Hjørring'), ('Frederikshavn','Frederikshavn'), ('Thisted','Thisted'), ('Mariagerfjord','Mariagerfjord'),
    ('Jammerbugt','Jammerbugt'), ('Vesthimmerland','Vesthimmerland'), ('Brønderslev','Brønderslev'), ('Rebild','Rebild'), ('Morsø','Morsø'), ('Læsø','Læsø'), ('Roskilde','Roskilde'),
    ('Næstved','Næstved'), ('Slagelse','Slagelse'), ('Holbæk','Holbæk'), ('Guldborgsund','Guldborgsund'), ('Køge','Køge'), ('Greve','Greve'), ('Kalundborg','Kalundborg'),
    ('Vordingborg','Vordringborg'), ('Lolland','Lolland'), ('Faxe','Faxe'), ('Ringsted','Ringsted'), ('Odsherred','Odsherred'), ('Sorø','Sorø'), ('Lejre','Lejre'),
    ('Stevns','Stevns'), ('Solrød','Solrød'), ('Odense','Odense'), ('Halsnæs','Halsnæs'), ('Bornholm','Bornholm'), ('Esbjerg','Esbjerg'), ('Vejle','Vejle'), ('Kolding','Kolding'),
    ('Sønderborg','Sønderborg'), ('Aabenraa','Aabenraa'), ('Svendborg','Svendborg'), ('Haderslev','Haderslev'), ('Faaborg/Midtfyn','Faaborg/Midtfyn'), ('Fredericia','Fredericia'),
    ('Varde','Varde'), ('Vejen','Vejen'), ('Assens','Assens'), ('Middelfart','Middelfart'), ('Tønder','Tønder'), ('Nyborg','Nyborg'), ('Nordfyn','Nordfyn'), ('Billund','Billund'),
    ('Kerteminde','Kerteminde'), ('Langeland','Langeland'), ('Ærø','Ærø'), ('Fanø','Fanø')])

    submit = SubmitField('Opret')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Brugernavnet er allerede taget. Vælg venligst et andet brugernavn...')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Den indtastede email adresse er allerede registreret. Indtast venligst en anden eller log ind')

class Edit_userForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired("Du skal indtaste en email adresse."), Email("Du har ikke indtastet en gyldig email adresse.")])

    school = SelectField('Hvilken kommune arbejder du?',
    choices=[('København','København'), ('Frederikberg','Frederikberg'), ('Gentofte','Gentofte'), ('Gladsaxe','Gladsaxe'), ('Helsingør','Helsingør'),
    ('Rudersdal','Rudersdal'), ('Lyngby-Taarbæk','Lyngby-Taarbæk'), ('Hvidore','Hvidore'), ('Hillerød','Hillerød'), ('Høje-Taastrup','Høje-Taastrup'), ('Ballerup','Ballerup'),
    ('Frederikssund','Frederikssund'), ('Tårnby','Tårnby'), ('Egedal','Egedal'), ('Gribskov','Gribskov'), ('Furesø','Furesø'), ('Fredensborg','Fredensborg'),
    ('Rødovre','Rødovre'), ('Brøndby','Brøndby'), ('Herlev','Herlev'), ('Albertslund','Albertslund'), ('Allerød','Allerød'), ('Hørsholm','Hørsholm'), ('Ishøj','Ishøj'),
    ('Glostrup','Glostrup'), ('Vallensbæk','Vallensbæk'), ('Dragør','Dragør'), ('Aarhus','Aarhus'), ('Randers','Randers'), ('Viborg','Viborg'), ('Silkeborg','Silkeborg'),
    ('Horsens','Horsens'), ('Herning','Herning'), ('Skanderborg','Skanderborg'), ('Holstebro','Holstebro'), ('Rinkøbing-skjern','Ringkøbing-skjern'), ('Favrskov','Farvskov'),
    ('Hedensted','Hedensted'), ('Skive','Skive'), ('Syddjurs','Syddjurs'), ('Norddjurs','Norddjurs'), ('Ikast-Brande','Ikast-Brande'), ('Odder','Odder'), ('Struer','Struer'),
    ('Lemvig','Lemvig'), ('Samsø','Samsø'), ('Aalborg','Aalborg'), ('Hjørring','Hjørring'), ('Frederikshavn','Frederikshavn'), ('Thisted','Thisted'), ('Mariagerfjord','Mariagerfjord'),
    ('Jammerbugt','Jammerbugt'), ('Vesthimmerland','Vesthimmerland'), ('Brønderslev','Brønderslev'), ('Rebild','Rebild'), ('Morsø','Morsø'), ('Læsø','Læsø'), ('Roskilde','Roskilde'),
    ('Næstved','Næstved'), ('Slagelse','Slagelse'), ('Holbæk','Holbæk'), ('Guldborgsund','Guldborgsund'), ('Køge','Køge'), ('Greve','Greve'), ('Kalundborg','Kalundborg'),
    ('Vordingborg','Vordringborg'), ('Lolland','Lolland'), ('Faxe','Faxe'), ('Ringsted','Ringsted'), ('Odsherred','Odsherred'), ('Sorø','Sorø'), ('Lejre','Lejre'),
    ('Stevns','Stevns'), ('Solrød','Solrød'), ('Odense','Odense'), ('Halsnæs','Halsnæs'), ('Bornholm','Bornholm'), ('Esbjerg','Esbjerg'), ('Vejle','Vejle'), ('Kolding','Kolding'),
    ('Sønderborg','Sønderborg'), ('Aabenraa','Aabenraa'), ('Svendborg','Svendborg'), ('Haderslev','Haderslev'), ('Faaborg/Midtfyn','Faaborg/Midtfyn'), ('Fredericia','Fredericia'),
    ('Varde','Varde'), ('Vejen','Vejen'), ('Assens','Assens'), ('Middelfart','Middelfart'), ('Tønder','Tønder'), ('Nyborg','Nyborg'), ('Nordfyn','Nordfyn'), ('Billund','Billund'),
    ('Kerteminde','Kerteminde'), ('Langeland','Langeland'), ('Ærø','Ærø'), ('Fanø','Fanø')])

    submit = SubmitField('Tilføj ændringer')


class LoginForm(FlaskForm):
    username = StringField('Brugernavn', validators=[DataRequired("Du mangler at indtaste dit brugernavn.")])
    password = PasswordField('Kodeord', validators=[DataRequired("Du mangler at indtaste dit password.")])
    remember_me = BooleanField('Husk mig')
    submit_l = SubmitField('Log ind')

class KontaktForm(FlaskForm):
    navn = StringField('Navn', validators=[InputRequired('Du skal indtaste dit navn')])
    email = StringField('Email', validators=[InputRequired('Du skal indtaste en email adresse'), Email('Det indtastede minder ikke om en email adresse....')])
    besked = TextAreaField('Besked')
    submit = SubmitField('Send besked')


class Mat1Form(FlaskForm):
    title = StringField('Testens navn', validators=[DataRequired("Du skal give prøven et navn.")])
    klasse = StringField('Klasse', validators=[(DataRequired("Du skal angive en klasse."))])
    beskrivelse = TextAreaField('Kommentarer')
    submit = SubmitField('Tilføj test')

class Mat1testsForm(FlaskForm):
    elev = StringField('Elevens navn', validators=[DataRequired("Skriv elevens navn")])
    a1 = IntegerField('A1', validators=[InputRequired("Indtast en talværdi mellem 0 og 29"), NumberRange(0, 29, 'Indtast en talværdi mellem 0 og 29')])
    b1 = IntegerField('B1', validators=[InputRequired("Indtast en talværdi mellem 0 og 23"), NumberRange(0, 23, "Indtast en talværdi mellem 0 og 23")])
    b2 = IntegerField('B2', validators=[InputRequired("Indtast en talværdi mellem 0 og 23"), NumberRange(0, 23, "Indtast en talværdi mellem 0 og 23")])
    c1 = IntegerField('C1', validators=[InputRequired("Indtast en talværdi mellem 0 og 10"), NumberRange(0, 10, "Indtast en talværdi mellem 0 og 10")])
    d1 = IntegerField('D1', validators=[InputRequired("Indtast en talværdi mellem 0 og 6"), NumberRange(0, 6, "Indtast en talværdi mellem 0 og 6")])
    d2 = IntegerField('D2', validators=[InputRequired("Indtast en talværdi mellem 0 og 5"), NumberRange(0, 5, "Indtast en talværdi mellem 0 og 5")])
    d3 = IntegerField('D3', validators=[InputRequired("Indtast en talværdi mellem 0 og 6"), NumberRange(0, 6, "Indtast en talværdi mellem 0 og 6")])
    d4 = IntegerField('D4', validators=[InputRequired("Indtast en talværdi mellem 0 og 10"), NumberRange(0, 10, "Indtast en talværdi mellem 0 og 10")])
    e1 = IntegerField('E1', validators=[InputRequired("Indtast en talværdi mellem 0 og 5"), NumberRange(0, 5, "Indtast en talværdi mellem 0 og 5")])
    comments = TextAreaField('Bemærkninger')
    submit = SubmitField('Tilføj elev')

