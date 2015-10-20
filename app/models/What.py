
from system.core.model import Model
import re
class What(Model):
	def __init__(self):
		super(What, self).__init__()

	def create_users(self, new_user):
		error=[]
		PHONE_REGEX = re.compile(r'^[0-9]*$')
		DATE_REGEX = re.compile(r'^[0-9][0-9]+/[0-9]+/[0-9][0-9][0-9][0-9]$')
		if len(new_user["name"])<1:
			error.append("Name cannot be empty")

		if len(new_user["number"])<1:
			error.append("Phone number cannot be empty")
		elif len(new_user["number"])<10:
			error.append("Phone number must be at least 10 number long")
		elif not PHONE_REGEX.match(new_user["number"]):
			error.append('Phone number can be only number')

		if len(new_user["password"])<1:
			error.append("password cannot be empty")
		elif new_user["password"] != new_user["pwd"]:
			error.append('Password and confirmation must match!')


		if error:
			return {"status":False, "error":error}
		user_id=self.get_user_id_from_number(new_user["number"])
		print "This is my id",user_id
		if user_id is not None:
			error.append("Number already exist")
			return {"status":False, "error":error}
		else:
			hashed_pw = self.bcrypt.generate_password_hash(new_user["password"])


		query = 'INSERT INTO users (name, phone, password) VALUES (%s,%s,%s)'
		data =[new_user['name'], new_user['number'], hashed_pw]

		self.db.query_db(query,data)
		user_id=self.get_user_id_from_number(new_user['number'])
		print user_id
		return {"status":True, "userid": str(user_id)}

	def get_user_id_from_number(self, number):
		query= "select id from users where phone='"+number+"'"
		user_id=self.db.query_db(query)
		if len(user_id)>0:
			return user_id[0]["id"]
		else:
			return None

	def get_events(self, userid):
		query= 'select * from users  join events on events.user_id = users.id where users.id='+userid
		return self.db.query_db(query)

	def create_event(self, input_events, userid):
		query = "insert into events(event_name,date,time,place, user_id) values('"+input_events["event_name"]+"', '"+input_events["date"]+"','"+input_events["time"]+"','"+input_events["place"]+"',"+str(userid)+")"
		print query
		return self.db.query_db(query)

	def login(self,userlist):

			query="SELECT * from users where phone='" + userlist["number"] +"'"
			error=[]
			users = self.db.query_db(query)
			if users:
				if self.bcrypt.check_password_hash(users[0]['password'], userlist["password"]):

					return {"status":True, "userlogin":users}
			else:
				error.append("Invaliad username and password")
				return {"status":False, "error":error}
			

