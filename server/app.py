#!/usr/bin/env python3

from flask import Flask, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Newsletter

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newsletters.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

# Home route
class Home(Resource):
    def get(self):
        response_dict = {
            "message": "Welcome to the Newsletter RESTful API",
        }
        return make_response(response_dict, 200)

api.add_resource(Home, '/')

# All newsletters GET & POST
class Newsletters(Resource):
    def get(self):
        newsletters = Newsletter.query.all()
        response_dict_list = [n.to_dict() for n in newsletters]
        return make_response(response_dict_list, 200)

    def post(self):
        new_record = Newsletter(
            title=request.form['title'],
            body=request.form['body'],
        )
        db.session.add(new_record)
        db.session.commit()
        return make_response(new_record.to_dict(), 201)

api.add_resource(Newsletters, '/newsletters')

# Single newsletter by ID
class NewsletterByID(Resource):
    def get(self, id):
        newsletter = Newsletter.query.filter_by(id=id).first()
        if newsletter:
            return make_response(newsletter.to_dict(), 200)
        else:
            return make_response({"error": "Newsletter not found"}, 404)

api.add_resource(NewsletterByID, '/newsletters/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
