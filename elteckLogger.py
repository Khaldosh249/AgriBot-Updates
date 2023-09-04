from logging import Handler, LogRecord 
import requests
import os
import dotenv
dotenv.load_dotenv()


class EltechHandler(Handler):
    def __init__(self, level = 0 , server ='Not Set') -> None:
        self.server = server
        super().__init__(level)
    
    def emit(self, record: LogRecord) -> None:
        requests.post(
		"https://api.mailgun.net/v3/eltech.sd/messages",
		auth=("api", os.getenv('ELTECH_API_KEY') ),
		data={"from": "ISE <ise@eltech.sd>",
			"to": ['kha091288@yahoo.com' , 'almstfym870@gmail.com' , 'kha09128857@gmail.com'], 
			"subject": f"[Important] ERROR caught in {self.server} ",
			"text": f"""
Hello Developer!

Error Place : {record.message}
Error : {record.exc_text}

حل المشكلة دي سريع يازول!
قوم شوف شغلك يا عاطل!"""})
        return super().emit(record)