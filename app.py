from flask import Flask, render_template, request, jsonify, json
from wtforms import StringField, Form
from wtforms.validators import DataRequired, Length
from flask_sqlalchemy import SQLAlchemy
from flask_table import Table, Col, LinkCol
#import babel
#babel.default_locale('LC_TIME')
#babel.dates.format_datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'

db = SQLAlchemy(app)


class SearchForm(Form):  # create form
    #autocomplete = StringField('autocomplete', validators=[DataRequired(), Length(max=40)],
    #                           render_kw={"placeholder": "autocomplete"})
    pass

class AddressTable(Table):
    classes = ['AddressTable']
    id = Col('id')
    name = Col('name')


class Country(db.Model):
    __tablename__ = 'address'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True, nullable=False)
    name_lower = db.Column(db.Text, unique=True, nullable=False)

    @staticmethod
    def clean_search(search):
        return str(search).lower().replace('  ', ' ').replace(' ', '% %')

    @staticmethod
    def search(search):
        search = Country.clean_search(search)
        return db.session.query(Country.id, Country.name).filter(Country.name_lower.like('%' + search + '%')).all()

    @staticmethod
    def select(search):
        return db.session.query(Country.id, Country.name).filter(Country.name_lower.like('%' + search + '%')).all()

@app.route('/')
def index():
    form = SearchForm(request.form)
    return render_template('index.html')

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    search = request.args.get('q')

    results = [str(mv[0]) + "_" + str(mv[1]) for mv in Country.search(search)]
    return jsonify(matching_results=results)

@app.route('/process')
def process():
    result = Country.select(request.args.get('autocomplete'))
    print(len(result))
    table = AddressTable(result)

    return render_template('index.html',table=table)


if __name__ == '__main__':
    app.run(debug=True)
