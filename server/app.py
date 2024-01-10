from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        messages =  Message.query.all()
        messages_list = [message.to_dict() for message in messages]
        response = make_response(
            messages_list,
            200
        )
        return response
    elif request.method == 'POST':
        print(request.json.get('body'))
        new_message = Message(
            body=request.json.get('body'),
            username=request.json.get('username')
        )
        db.session.add(new_message)
        db.session.commit()

        return make_response(new_message.to_dict(), 201)


@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def message_by_id(id):
    message = Message.query.filter(Message.id == id).first()
    if message == None:
        response = {
            "message" : "No message found"
        }

        return make_response(response, 404)
    
    elif request.method == 'PATCH':
        for attr in request.json:
            setattr(message, attr, request.json.get(attr))
        db.session.add(message)
        db.session.commit()

        mess_dict = message.to_dict()
        return make_response(mess_dict, 200)
    
    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()
        
        response = {
            "delete_successful" : True,
            "message" : "Message deleted"
        }

        return make_response(response, 200)

if __name__ == '__main__':
    app.run(port=5555)
