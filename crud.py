import mysql.connector
from flask import Flask, jsonify, request, Response
import jsonpickle


errors = {'ProgrammingError': 400,
'InternalError': 422,
'NotSupportedError': 406,
'OperationalError': 409,
'IntegrityError': 406,
'DatabaseError': 408,
'InterfaceError': 404,
'PoolError': 401
          }
errors_list = (mysql.connector.errors.ProgrammingError,
mysql.connector.errors.InternalError,
mysql.connector.errors.NotSupportedError,
mysql.connector.errors.OperationalError,
mysql.connector.errors.IntegrityError,
mysql.connector.errors.DatabaseError,
mysql.connector.errors.InterfaceError,
mysql.connector.errors.PoolError)

print(errors_list[0])
def get_connection_to_db():
    connection = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='api')
    return connection


class User:
    def __init__(self, user_id, user_name, user_city):
        self.user_id = user_id
        self.user_name = user_name
        self.user_city = user_city


app = Flask("CRUD app with Flask")


@app.route('/users/', defaults={'start': 0, 'stop': 20, 'name_beginning': '', 'city': ''}, methods=['GET'])
@app.route('/users/<start>/<stop>', defaults={'name_beginning': '', 'city': ''}, methods=['GET'])
@app.route('/users/<start>/<stop>/<name_beginning>', defaults={'city': ''}, methods=['GET'])
@app.route('/users/<start>/<stop>/<name_beginning>/<city>', methods=['GET'])
def get_users(start, stop, name_beginning, city):

    users = []
    query_data = {'start': int(start), "stop": int(stop), 'name_beginning': name_beginning, 'city': city}
    query_data['name_beginning'] += '%'
    try:
        connection = get_connection_to_db()
        if name_beginning == '' and city == '' and start == 0:
            query = 'SELECT * FROM users'
        elif name_beginning == '' and city == '':
            query = 'SELECT * FROM users limit %(start)s, %(stop)s'
        elif city == '':
            query = 'SELECT * FROM users where username like %(name_beginning)s  limit %(start)s, %(stop)s'
        else:
            query = '''SELECT * FROM users where username
             like %(name_beginning)s and city = %(city)s  limit %(start)s, %(stop)s'''

        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, query_data)
        for row in cursor:
            users.append(User(row['id'], row['username'], row['city']))

    except errors_list as err:
        return jsonify(detail=err.msg), errors[err.__class__.__name__]
    except Exception as err:
        return jsonify(detail='Other error'), 400
    finally:
        try:
            connection.close()
        except UnboundLocalError:
            return jsonify(detail='Connection to DB is not established. Check if server is running '), 400
        response = Response(jsonpickle.encode(users, unpicklable=False), mimetype='application/json')
        response.headers['new_header'] = 'new header'
    return response, 200


@app.route('/users', methods=['POST'])
def adduser():
    request_data = request.get_json()
    try:
        connection = get_connection_to_db()
        query = "INSERT into users values (null, %(username)s, %(city)s)"
        cursor = connection.cursor(dictionary=True)
        if type(request_data['username']) != str:
            request_data["user_id"] = []
            for i in range(len(request_data['username'])):
                cursor.execute(query, {'username': request_data['username'][i], 'city': request_data['city'][i]})
                connection.commit()
                request_data["user_id"].append(cursor.lastrowid)
        else:
            cursor.execute(query, request_data)
            connection.commit()
            request_data["user_id"] = cursor.lastrowid

    except errors_list as err:
        return jsonify(detail=err.msg), errors[err.__class__.__name__]
    except Exception as err:
        return jsonify(detail='Other error'), 400
    finally:
        try:
            connection.close()
        except UnboundLocalError:
            return jsonify(detail='Connection to DB is not established. Check if server is running '), 400
    return request_data, 201


@app.route('/users/<user_id>', methods=["PUT"])
def update_user(user_id):
    request_data = request.get_json()
    request_data['user_id'] = user_id
    try:
        connection = get_connection_to_db()
        query = "select * from users where id=%(user_id)s"
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, request_data)
        if cursor.fetchall() == []:
            return jsonify(detail='There is no user with id number {0}'.format(user_id))

        query = "UPDATE users SET username = %(username)s, city= %(city)s WHERE id=%(user_id)s"
        cursor.execute(query, request_data)
        connection.commit()
    except errors_list as err:
        return jsonify(detail=err.msg), errors[err.__class__.__name__]
    except Exception as err:
        return jsonify(detail='Other error'), 400
    finally:
        try:
            connection.close()
        except UnboundLocalError:
            return jsonify(detail='Connection to DB is not established. Check if server is running '), 400
    return request_data


@app.route('/users/username/<user_id>', methods=["PATCH"])
def update_user_username(user_id):
    request_data = request.get_json()
    request_data['user_id'] = user_id
    try:
        connection = get_connection_to_db()
        query = "select * from users where id=%(user_id)s"
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, request_data)
        if cursor.fetchall() == []:
            return jsonify(detail='There is no user with id number {0}'.format(user_id))

        query = "UPDATE users SET username = %(username)s WHERE id=%(user_id)s"
        cursor.execute(query, request_data)
        connection.commit()
    except errors_list as err:
        return jsonify(detail=err.msg), errors[err.__class__.__name__]
    except Exception as err:
        return jsonify(detail='Other error'), 400
    finally:
        try:
            connection.close()
        except UnboundLocalError:
            return jsonify(detail='Connection to DB is not established. Check if server is running '), 400
    return request_data


@app.route('/users/city/<user_id>', methods=["PATCH"])
def update_user_city(user_id):
    request_data = request.get_json()
    request_data['user_id'] = user_id
    try:
        connection = get_connection_to_db()
        query = "select * from users where id=%(user_id)s"
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, request_data)
        if cursor.fetchall() == []:
            return jsonify(detail='There is no user with id number {0}'.format(user_id))

        query = "UPDATE users SET city= %(city)s WHERE id=%(user_id)s"
        cursor.execute(query, request_data)
        connection.commit()
    except errors_list as err:
        return jsonify(detail=err.msg), errors[err.__class__.__name__]
    except Exception as err:
        return jsonify(detail='Other error'), 400
    finally:
        try:
            connection.close()
        except UnboundLocalError:
            return jsonify(detail='Connection to DB is not established. Check if server is running '), 400
    return request_data


@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    request_data = {'user_id': user_id}
    try:
        connection = get_connection_to_db()
        query = "select * from users where id=%(user_id)s"
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, request_data)
        if cursor.fetchall() == []:
            return jsonify(detail='There is no user with id number  {0}'.format(user_id))
        query = "delete from users WHERE id=%(user_id)s"
        cursor.execute(query, request_data)
        connection.commit()
    except errors_list as err:
        return jsonify(detail=err.msg), errors[err.__class__.__name__]
    except Exception as err:
        return jsonify(detail='Other error'), 400
    finally:
        try:
            connection.close()
        except UnboundLocalError:
            return jsonify(detail='Connection to DB is not established. Check if server is running '), 400
    return jsonify()


@app.route('/users/delete/all', methods=['DELETE'])
def delete_all_users():
    try:
        connection = get_connection_to_db()
        query = "delete from users"
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query)
        connection.commit()
    except errors_list as err:
        return jsonify(detail=err.msg), errors[err.__class__.__name__]
    except Exception as err:
        return jsonify(detail='Other error'), 400
    finally:
        try:
            connection.close()
        except UnboundLocalError:
            return jsonify(detail='Connection to DB is not established. Check if server is running '), 400
    return jsonify()


app.run()
