from cassandra.cluster import Cluster
import json,csv,sys,os,psycopg2
from netaddr import EUI

create = "CREATE TABLE {0} (time_stamp INT, class_id INT, level INT, PRIMARY KEY(time_stamp)) ;"
insert = "INSERT INTO {0} (time_stamp, class_id,level) VALUES ({1},{2},{3}) ;"
drop = "DROP TABLE {0}"

create1= """CREATE TABLE {0} (start_timestamp INT, end_timestamp INT, PRIMARY KEY(start_timestamp)) ; """
insert1="INSERT INTO {0} (start_timestamp,end_timestamp	) VALUES ({1},{2})	;"

create2= """CREATE TABLE {0} (time_stamp INT, activity INT, PRIMARY KEY(time_stamp)) ; """
insert2="INSERT INTO {0} (time_stamp, activity) VALUES ({1},{2})	;"

create3= """CREATE TABLE {0} (time_stamp INT, audio INT, PRIMARY KEY(time_stamp)) ; """
insert3="INSERT INTO {0} (time_stamp, audio) VALUES ({1},{2})	;"

create4= """CREATE TABLE {0} (start_timestamp INT, end_timestamp INT, PRIMARY KEY(start_timestamp)) ; """
insert4="INSERT INTO {0} (start_timestamp,end_timestamp	) VALUES ({1},{2})	;"

create5= """CREATE TABLE {0} (time_stamp INT, latitude FLOAT, longitude FLOAT, travelstate INT, PRIMARY KEY(time_stamp)) ; """
insert5="INSERT INTO {0} (time_stamp,latitude,longitude,travelstate	) VALUES ({1},{2},{3},{4})	;"


usersadded=['u00','u24','u08','u57','u52','u51','u36','u59','u19','u46','u16','u44','u02','u49','u10','u32','u33','u43']


def dbInsertBTscan(csvfile,cur,tableName):
	uid=(csvfile.split('_'))[1][0:3] +tableName
	cur.execute(create.format(uid))
	print(create.format(uid))
	with open(csvfile,'rb') as inCsv:
			parsed = csv.DictReader(inCsv , delimiter = ',' , quotechar='"')
			for record in parsed:
				#print(uid)
				#data=[str(uid), record['time'],record['MAC'],record['class_id'],record['level']]
				a = EUI(record['MAC'])
				#data=(uid,record['time'],str(record['MAC']),record['class_id'],record['level'],)
				insertQ = insert.format(uid,record['time'],record['class_id'],record['level'])
				cur.execute(insertQ)
				


cluster = Cluster()

session = cluster.connect('demo')
directory = os.path.dirname(os.path.abspath(__file__)) + '/dataset/sensing/bluetooth'
tableName = 'bt'
for filename in os.listdir(directory):
	filename = directory +'/'+ filename
	dbInsertBTscan(filename,session,tableName)
	a = raw_input()


# TODO: replicate all my postgresql inserts > cassandra cql
# IMPORTANT: primary key needs to be specified, not assigned automatically