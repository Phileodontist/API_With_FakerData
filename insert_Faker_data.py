import pymysql
from config import Config
from faker import Faker
from faker.providers import *

fake = Faker()
fake.add_provider(internet)

HOST = Config.dev_host
USER = Config.dev_user
PASSWORD = Config.dev_password
DATABASE = Config.dev_database
PORT = Config.dev_port
TABLE = "profiles"
NUM_RECORDS = 50000 # Controlls the number of records inserted

def insertFakerData():
	"""
	Generates fake profiles and inserts into into database
	"""
	try:
		db = pymysql.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE, port=PORT, charset='utf8')
		cur = db.cursor(pymysql.cursors.DictCursor)
		for _ in range(NUM_RECORDS):
			profile = fake.profile()
			profile["current_location"] = ",".join([str(profile["current_location"][0]), str(profile["current_location"][0])])
			profile["website"] = ",".join(profile["website"])
			profile["birthdate"] = profile["birthdate"].strftime("%Y-%m-%d")

			columns = ", ".join(profile.keys())
			placeHolders = ", ".join(["%s"] * len(profile))

			print("INSERT into {} ({}) values ({})".format(TABLE, columns, placeHolders), list(profile.values()))
			cur.execute("INSERT into {} ({}) values ({})".format(TABLE, columns, placeHolders), list(profile.values()))
			db.commit()
	except pymysql.Error as e:
		print("Error Occurred - " + str(e))
	finally:
		cur.close()
		db.close()

def main():
	insertFakerData()

if __name__ == "__main__":
	main()
