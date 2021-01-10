import flask
import pymysql
from config import Config
from sql_queries import Queries

HOST = Config.dev_host 
USER = Config.dev_user
PASSWORD = Config.dev_password
DATABASE = Config.dev_database
PORT = Config.dev_port

app = flask.Flask(__name__)
app.config["DEBUG"] = True

DB = pymysql.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE, port=PORT, charset='utf8')
CUR = DB.cursor(pymysql.cursors.DictCursor)


@app.route("/", methods=['GET'])
def readme():
	"""
	Landing page that serves as the README Page
	"""
	html =  \
		"""
			<title>README</title>
			<body>
				<h1>README</h1>
				<hr/>
				<h2>Statement of Purpose</h2>
				<div style="margin-left:30px">
					<p style="font-size:20px">
						This project serves as an exercise in using the Flask framework.<br/>
						Using simulated data from the Faker Library, this project demonstrates<br/>
						the ability to use Flask to access data from a mysql database as well
						as from AWS S3<br/> via the following endpoints:
					</p>
					<p><b>Base URL: http://127.0.0.1:5000/</b></p>
					<ul>
						<li><b>/</b> - Landing page that serves as the README Page</li>
						<li><b>/NumOfProfiles</b> - Returns the number of Profiles</li>
						<li><b>/TopOccupation</b> - Returns the occupation with the most counts</li>
						<li><b>/OccupationCounts</b> - Returns the count for each occupation</li>
						<li><b>/BirthYearCounts</b> - Returns the count for each birth year</li>
					<ul>
				</div>
			</body>
		"""
	return html 

@app.route("/NumOfProfiles", methods=['GET'])
def numOfProfiles():
	"""
	Returns the number of Profiles
	"""
	results = {}
	try:
		CUR.execute(Queries.numOfProfiles)
		dbResults = CUR.fetchall()
		results["data"] = dbResults
		results["status"] = 200
	except pymysql.Error as e:
		results["message"] = "Error with retrieving data - " + str(e)
		results["status"] = 500 
	return results 

@app.route("/TopOccupation", methods=['GET'])
def topOccupation():
	"""
	Returns the occupation with the most counts
	"""
	results = {}
	try:
		CUR.execute(Queries.topOccupationCount)
		dbResults = CUR.fetchall()
		results["data"] = dbResults
		results["status"] = 200
	except pymysql.Error as e:
		results["message"] = "Error with retrieving data - " + str(e)
		results["status"] = 500 
	return results 

@app.route("/OccupationCounts", methods=['GET'])
def occupationCounts():
	"""
	Returns the count for each occupation
	"""
	results = {}
	try:
		CUR.execute(Queries.occupationCounts)
		dbResults = CUR.fetchall()
		results["data"] = dbResults
		results["status"] = 200
	except pymysql.Error as e:
		results["message"] = "Error with retrieving data - " + str(e)
		results["status"] = 500 
	return results 

@app.route("/BirthYearCounts", methods=['GET'])
def birthYearCounts():
	"""
	Returns the count for each birthday year
	"""
	results = {}
	try:
		CUR.execute(Queries.birthYearCounts)
		dbResults = CUR.fetchall()
		results["data"] = dbResults
		results["status"] = 200
	except pymysql.Error as e:
		results["message"] = "Error with retrieving data - " + str(e)
		results["status"] = 500 
	return results 


def main():
	try:
		app.run()
	except KeyboardInterrupt as e:
		print("Closing Connection to Database")
		cur.close()
		db.close()
		

if __name__ == '__main__':
	main()
