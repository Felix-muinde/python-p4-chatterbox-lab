from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json['JSONIFY_PRETTYPRINT_REGULAR'] = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        # Retrieve all messages from the database
        messages = Message.query.all()
        message_list = [{'id': message.id, 'body': message.body, 'username': message.username} for message in messages]
        return jsonify(message_list)
    
    if request.method == 'POST':
        data = request.get_json()
        body = data.get('body')
        username = data.get('username')
        
        if body and username:
            # Create a new message and save it to the database
            new_message = Message(body=body, username=username)
            db.session.add(new_message)
            db.session.commit()
            return jsonify({'message': 'Message added successfully'})
        else:
            return jsonify({'message': 'Both body and username are required'}), 400

@app.route('/messages/<int:id>', methods=['GET', 'DELETE'])
def messages_by_id(id):
    if request.method == 'GET':
        # Retrieve a specific message by its ID
        message = Message.query.get(id)
        if message:
            return jsonify({'id': message.id, 'body': message.body, 'username': message.username})
        else:
            return jsonify({'message': 'Message not found'}), 404
    
    if request.method == 'DELETE':
        # Delete a message by its ID
        message = Message.query.get(id)
        if message:
            db.session.delete(message)
            db.session.commit()
            return jsonify({'message': 'Message deleted successfully'})
        else:
            return jsonify({'message': 'Message not found'}), 404

if __name__ == '__main__':
    app.run(port=5555)
