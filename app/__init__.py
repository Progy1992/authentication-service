from flask import Flask, jsonify, request
import logging
from .database import session_instance
from .schemas import User, UserSession
from .helper import generate_jwt_token

app = Flask(__name__)

# Create a logger instance specific to the current module
logger = logging.getLogger(__name__)

# Define a log formatter with a specific format
log_formatter = logging.Formatter(
    "%(asctime)s %(levelname)s %(name)s %(message)s"
)

# Set the logging level for the logger to capture messages of severity ERROR and above
logger.setLevel(logging.INFO)


@app.route('/ping')
def ping():
    return jsonify({'message': 'pong'})


@app.route('/login', methods=['POST'])
def login():
    try:
        login_data = request.json
        logger.info(login_data)
        username = login_data['username']
        password = login_data['password']
        generated_token = login_opertion(username, password)
        return jsonify({'generated_token': generated_token, 'message': 'User is now signed in'})
    except Exception as e:
        logger.error(e)
        return jsonify({'message': 'login is unsuccessful'}), 400


@app.route('/logout', methods=['POST'])
def logout():
    try:
        auth_header = request.headers.get('Authorization')
        # if auth_header and auth_header.startswith('Bearer '):
        auth_header = auth_header.split(' ')[1]
        logger.error(auth_header)
        result = logout_operation(auth_header)
        return jsonify({'message': result}), 200

    except Exception as e:
        logger.error(e)
        return jsonify({'message': 'logout is unsuccessful'}), 400


@app.route('/checkaccess', methods=['POST'])
def checkTokenValidity():
    try:
        auth_header = request.headers.get('Authorization')
        # if auth_header and auth_header.startswith('Bearer '):
        auth_header = auth_header.split(' ')[1]
        logger.error(auth_header)
        result = check_token_validity(auth_header)
        if result is True:
            return jsonify({'message': 'Token is valid'}), 200
        else:
            return jsonify({'message': 'Token is not valid'}), 404

    except Exception as e:
        logger.error(e)
        return jsonify({'message': 'logout is unsuccessful'}), 400


def login_opertion(username, password):
    try:
        user = session_instance.query(
            User).filter_by(username=username, password=password).first()
        logger.info(user)
        if user is not None:
            return create_session_data(user)
        else:
            raise Exception(
                'Could not find user with provided username and password')
    except Exception as e:
        raise Exception(e)


def create_session_data(userObject):
    try:
        generated_token = generate_jwt_token(userObject)
        userSessionObject = UserSession(
            user_id=userObject.user_id,
            session_token=generated_token
        )
        session_instance.add(userSessionObject)
        session_instance.commit()
        return generated_token
    except Exception as e:
        raise Exception(e)


def logout_operation(jwt_token):
    try:
        userSessionObject = session_instance.query(
            UserSession).filter_by(session_token=jwt_token, is_active=1).first()
        if userSessionObject is not None:
            userSessionObject.is_active = 0
            session_instance.add(userSessionObject)
            session_instance.commit()
            return 'Logout is successful'
        else:
            return 'Logout is not successful'
    except Exception as e:
        logger.error(e)
        raise Exception(e)


def check_token_validity(jwt_token):
    try:
        userSessionObject = session_instance.query(
            UserSession).filter_by(session_token=jwt_token, is_active=1).first()
        if userSessionObject is not None:
            return True

        else:
            return False
    except Exception as e:
        logger.error(e)
        raise Exception(e)
