
from system.core.controller import *
import json
class Whats(Controller):
	def __init__(self, action):
		super(Whats, self).__init__(action)
		self.load_model('What')
	def index(self):  
		categories=self.getValueCategory()
		session["userid"]= 1
		return self.load_view('index.html',categories=categories)

	
	def getValueCategory(self):
		category=[]
		url = "http://api.eventful.com/json/categories/list?app_key=jk5zHMNmqkqjb6jS"
		
		res = json.loads(requests.get(url).content)

		for dictvalue in res["category"]:
			category.append({"id": dictvalue["id"], "name":dictvalue["name"].replace('&amp;','&')})
		
		return category

	def getallgeocode(self):
		url="http://api.eventful.com/json/events/search?app_key=jk5zHMNmqkqjb6jS&location=san%20jose,%20CA&page_size=10"
		res = requests.get(url).content
		return jsonify(res=res)

	def getcategorygeocode(self,categoryid):
		url="http://api.eventful.com/json/events/search?app_key=jk5zHMNmqkqjb6jS&location=san%20jose,%20CA&page_size=20"


		url+=str(categoryid)
		res = requests.get(url).content
		return jsonify(res=res)

	def event(self):
		if "number" in session:
			events= self.models['What'].get_events(session["id"])
			return self.load_view('events.html', events=events)
		else:
			flash("User did not login")
		return redirect("/")  

	def login_user(self):
		users_details={"number":request.form["number"],"password":request.form["pwd"]}
		login_status=self.models['What'].login(users_details)
		if login_status["status"]==True:
			print login_status
			session["name"]=str(login_status["userlogin"][0]["name"])
			session["id"]=str(login_status["userlogin"][0]["id"])
			session["number"]=str(login_status["userlogin"][0]["phone"])

		else:
			session.clear()
			for message in login_status['error']:
				flash(message, 'login_errors')

		return redirect("/")   
	        
	def create_user(self):
		users = {'name' : request.form['name'],'number' : request.form['number'],'password' : request.form['pwd'], 'pwd' : request.form['cpwd']}
		store_user=self.models['What'].create_users(users)

		if store_user["status"]==True:
			session["id"] = store_user["userid"]
			session["name"]= request.form["name"]
			session["number"]= request.form["number"]
			
		else:
			session.clear()
			for message in store_user['error']:
				flash(message)
			
		return redirect("/") 

	
	def create_event(self):
	
		input_events={"event_name":request.form["event_name"],"date":request.form["start_time"].split(" ")[0],"time":request.form["start_time"].split(" ")[1],"place":request.form["venue_name"]}
		self.models['What'].create_event(input_events, session["id"])

		return redirect('/')

	def logout(self):
		print 'logout'
		session.clear()
		return redirect ('/')


