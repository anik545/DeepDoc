from fbchat import Client, log
from fbchat.models import *
import json
import os

class EchoBot(Client):
    def __init__(self, username, password):
        super(EchoBot, self).__init__(username, password)
        self.list_= ["chest", "head", "shoulders", "knee", "toe", "heart", "stomach", "eye", "back", "arm"]
        try:
            with open(os.path.join(os.pardir, "web_app","data.json"), "r") as d:
                print('yes')
                self.jsonFile = json.load(d)
                print(self.jsonFile)
        except:
            print('no',os.path.join(os.pardir, "web_app","data.json"))
            self.jsonFile = {} # {author_id:{name:name,pains:[{q:a},{q:a}]}}
        self.states = {}


    def GetPhrases(sentence):
        uri = 'westus.api.cognitive.microsoft.com'
        path = '/text/analytics/v2.0/keyPhrases'
        accessKey = '----'


        documents = {'documents':[
            {'id':'1','text':sentence}
        ]}

        headers = {'Ocp-Apim-Subscription-Key': accessKey}
        conn = httplib.HTTPSConnection(uri)
        body = json.dumps(documents)
        conn.request("POST", path, body, headers)
        response = conn.getresponse()
        return json.loads(response.read())["documents"]["keyPhrases"]

    def GetSentiment(sentence):
        uri = 'westus.api.cognitive.microsoft.com'
        path = '/text/analytics/v2.0/keyPhrases'
        accessKey = '----'


        documents = {'documents':[
            {'id':'1','text':sentence}
        ]}

        headers = {'Ocp-Apim-Subscription-Key': accessKey}
        conn = httplib.HTTPSConnection(uri)
        body = json.dumps(documents)
        conn.request("POST", path, body, headers)
        response = conn.getresponse()
        return json.loads(response.read())["documents"]["keyPhrases"]

    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        self.markAsDelivered(author_id, thread_id)
        self.markAsRead(author_id)
        log.info(self.states)
        if self.states.get(author_id,0) == 0 and author_id != self.uid:
            self.thread_id = thread_id
            self.send(Message(text = "Hello, welcome to deepdoc. What is your name?"), thread_id=thread_id, thread_type=thread_type)
            self.states[author_id] = 1

        elif self.states.get(author_id,0) == 1 and author_id != self.uid:
            self.HandleReplyName(message_object, thread_id, thread_type, author_id)
            self.states[author_id] = 2

        elif self.states.get(author_id,0) == 2 and author_id != self.uid:
            self.HandleReplyMatter(message_object, thread_id, thread_type,author_id)

        elif self.states.get(author_id,0) == 3 and author_id != self.uid:
            self.HandleReplyScale(message_object, thread_id, thread_type,author_id)

        elif self.states.get(author_id,0) == 4 and author_id != self.uid:
            self.HandleReplyTime(message_object, thread_id, thread_type,author_id)


        elif author_id != self.uid:
            self.send(Message(text = "The doctor is busy and talking to someone else. Try again in 5 minuites."), thread_id=thread_id, thread_type=thread_type)


    def HandleReplyName(self, message_object, thread_id, thread_type, author_id):

        log.info("{} from {} in {}".format(message_object, thread_id, thread_type.name))
        self.send(Message(text ="Hi " + message_object.text +". My name is chatbot.\nWhat's the matter?"), thread_id=thread_id, thread_type=thread_type)
        name = message_object.text
        if self.jsonFile.get(author_id,None) is None:
            self.jsonFile[author_id] = {"name":name,"pains":[]}

    
    def HandleReplyMatter(self, message_object, thread_id, thread_type, author_id):
        matter = message_object.text
        log.info(matter)
        if matter == "no":
            self.states[author_id] = 0
            self.save_json()
            return None
        log.info("matter of person= " + matter)
        #see if matter is in keywords
        isFound=False
        for l in self.list_:
            if l in matter.lower():
                word = l
                isFound = True
                log.info(word)
                self.jsonFile[author_id]["pains"].append({"pain":word,"scale":0,"time":0})
                self.send(Message(text ="Your pain point is the " + word +". On a scale of 1 to 10, what is the severity of the problem?"), thread_id=thread_id, thread_type=thread_type)
                self.states[author_id] = 3
        if not isFound:
            # if self.GetSentiment(matter) < 0.5:
            #     word = self.GetPhrases(matter)[0]
                
            self.states[author_id] = 2
            self.send(Message(text = "Sorry we dont know about your pain point, What's the matter?"), thread_id=thread_id, thread_type=thread_type)
            # Make json file of what data was inputted by user

    def HandleReplyScale(self, message_object, thread_id, thread_type, author_id):
        try:
            scale = int(message_object.text)
            log.info(scale)
            if scale <0 or scale >10:
                self.send(Message(text = "How long have you had this problem for?"), thread_id=thread_id, thread_type=thread_type)
            else:
                self.jsonFile[author_id]["pains"][-1] = {x:scale for x in self.jsonFile[author_id]["pains"][-1]}
                self.send(Message(text = "How long have you had this pain for?"), thread_id=thread_id, thread_type=thread_type)
                self.states[author_id] = 4
        except ValueError:
            self.send(Message(text = "This is not a number. Try again."), thread_id=thread_id, thread_type=thread_type)

    def HandleReplyTime(self, message_object, thread_id, thread_type, author_id):
        painTime = message_object.text
        self.jsonFile[author_id]["pains"][-1]["time"] = painTime
        self.states[author_id] = 2
        self.send(Message(text = "Any other pains? Type no to finish"), thread_id=thread_id, thread_type=thread_type)

    def save_json(self):
        print('a')
        with open(os.path.join(os.pardir, "web_app","data.json"), "w") as d:
            log.info(self.jsonFile)
            log.info(d)
            json.dump(self.jsonFile, d)

    def welcome():
        pass




client = EchoBot("deepdocproject@gmail.com", "deepdoc@oxford")
client.listen()