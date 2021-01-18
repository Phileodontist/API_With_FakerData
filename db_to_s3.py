import sys
import boto3
import json
import pymysql
from config import Config

HOST = Config.dev_host
USER = Config.dev_user
PASSWORD = Config.dev_password
DATABASE = Config.dev_database
PORT = Config.dev_port
KEY_ID = Config.access_key
ACCESS_KEY = Config.secret_key
TABLE = "profiles"
BUCKETNAME = "faker-data"
FILENAME = "faker_data.json"

def insert2s3(jsonFile, s3File):
	"""
	Reads and writes a json file to a S3 Bucket
	"""
	s3 = boto3.resource('s3',
    region_name='us-west-1',
    aws_access_key_id=KEY_ID,
    aws_secret_access_key=ACCESS_KEY)    

	s3.Bucket(BUCKETNAME).upload_file(jsonFile, s3File)


def createJSONFile():
	"""
	Reads from DB and creates a json file
	"""
	try:
		db = pymysql.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE, port=PORT, charset='utf8')
		cur = db.cursor(pymysql.cursors.DictCursor)
		cur.execute("select * from {}".format(TABLE))
		rows = cur.fetchall()
	
		with open(FILENAME, 'w') as jsonFile:
			for row in rows:
				jsonFile.write(json.dumps(row, default=str) + "\n")
	except pymysql.Error as e:
		print("Error Occurred - " + str(e))
	finally:
		cur.close()
		db.close()
	
def main():
	if (len(sys.argv) == 1):
		print("Please provide a command: [createfile, insert {filename}.json]")
		return

	command = sys.argv[1]
	if command == "createfile":
		print("Creating JSON file ...")
		createJSONFile()
		print("Finished creating JSON file")
	elif command == "insert":
		if (len(sys.argv) < 3):
			print("No JSON file was specified")
			return

		if (len(sys.argv) > 5):
			print("To many arguments")
			return

		jsonFile = sys.argv[2]
		s3File = sys.argv[3]

		print("Inserting json file into s3")
		insert2s3(jsonFile, s3File)
		print("Finished inserting json file into s3")
	else:
		print("Please enter a valid command: [createfile, insert {filename}.json]")
		return 

if __name__ == "__main__":
	main()
