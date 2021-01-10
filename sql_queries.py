class Queries:
	"""
	Contains the queries used for each endpoint
	"""	

	# Number of profiles: /NumOfProfiles
	numOfProfiles = """SELECT COUNT(*) AS numberOfProfiles FROM profiles"""

	# Total counts for each Occupation: /OccupationCounts
	occupationCounts = """SELECT job AS occupation, COUNT(job) AS occupationCounts FROM profiles GROUP BY job"""

	# Occupation with the most counts: /TopOccupation
	topOccupationCount = """
							SELECT job AS occupation, count FROM (
								SELECT job, count(job) AS count 
								FROM profiles 
								GROUP BY job) AS b 
							WHERE count = (
								SELECT max(count)
								FROM (SELECT job, count(job) AS count 
									  FROM profiles 
									  GROUP BY job) AS a)
						 """
	
	# Total counts for each birth year: /BirthYearCounts
	birthYearCounts = """
						SELECT SUBSTRING_INDEX(birthdate, '-', 1) AS birthYear, 
							   count(*) AS count
							   FROM profiles 
							   GROUP BY birthYear
					  """
