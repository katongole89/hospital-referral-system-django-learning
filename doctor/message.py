def send_message(message, contact):
	import africastalking
	username = "kamogaedmund"
	api_key = "b9e82a793a16246c7627af8e5e2052ff32caec5b43872f4ec01b1ff41fe36ef9"
	africastalking.initialize(username, api_key)
	sms = africastalking.SMS
	response = sms.send(message, contact)

