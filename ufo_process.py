"""
This module contains API methods to access and manage the UFO sightings database
"""
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from datetime import datetime

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'ufo_admin'
app.config['MYSQL_PASSWORD'] = 'jiza_MA!_9182'
app.config['MYSQL_DB'] = 'ufo_sightings'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

#Adds a record to the database 
@app.route('/data', methods=['POST'])
def create_data():
    data = request.json
    try:
        cur = mysql.connection.cursor()
        query = "INSERT INTO sighting (time_stamp, city, state, country, shape, duration, summary, posted, image) " \
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (data['time_stamp'], data['city'], data['state'], data['country'], data['shape'],
                  data['duration'], data['summary'], data['posted'], data['image'])
        cur.execute(query, values)
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": "Data created successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

#Retrieves all records from the database
@app.route('/data', methods=['GET'])
def get_all_data():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM sighting")
        data = cur.fetchall()
        cur.close()
        return jsonify(data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

#Makes updates to a particular record (currently not used)
@app.route('/data/<int:data_id>', methods=['PUT'])
def update_data(data_id):
    data = request.json
    try:
        cur = mysql.connection.cursor()
        query = "UPDATE sighting SET time_stamp=%s, city=%s, state=%s, country=%s, shape=%s, " \
                "duration=%s, summary=%s, posted=%s, images=%s WHERE id=%s"
        values = (data['time_stamp'], data['city'], data['state'], data['country'], data['shape'],
                  data['duration'], data['summary'], data['posted'], data['images'], data_id)
        cur.execute(query, values)
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": "Data updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


#Searches the database for sightings based on conditions and retrieves matching records
@app.route('/data/search', methods=['GET'])
def search_data():
    try:
        query_params = request.args.to_dict()
        conditions = []
        values = []

        for key in ['time_stamp', 'city', 'state', 'country']:
            if key in query_params:
                if key == 'time_stamp':
                    # Check if 'time_stamp' is in mm/dd/yy format
                    date_format = "%m/%d/%y"
                    try:
                        datetime.strptime(query_params[key], date_format)
                        # If it's a valid date format, convert it to a MySQL date format
                        conditions.append(f"DATE({key}) = DATE(%s)")
                    except ValueError:
                        return jsonify({"error": "Invalid date format"}), 400
                else:
                    conditions.append(f"{key} = %s")
                values.append(query_params[key])

        if not conditions:
            return jsonify({"message": "Please provide search parameters"}), 400

        condition_str = " AND ".join(conditions)
        cur = mysql.connection.cursor()
        query = f"SELECT * FROM sighting WHERE {condition_str}"
        cur.execute(query, tuple(values))
        data = cur.fetchall()
        cur.close()
        return jsonify(data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500




if __name__ == '__main__':
    app.run(debug=True)
