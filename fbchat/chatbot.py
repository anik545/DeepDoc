from fbchat import Client, log
from fbchat.models import *
import json

class EchoBot(Client):
    def __init__(self, username, password):
        super(EchoBot, self).__init__(username, password)
        self.state =0
        self.painlist = []
        self.list_= ["chest", "head", "shoulders", "knee", "toe", "heart",
            "stomach", "eye", "back", "arm"]

    #onMessage is called every time a message is detected.
    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        self.markAsDelivered(author_id, thread_id)
        self.markAsRead(author_id)

        #This is a FSA design, where action on message varies based on the automata's internal state
        #Initial state, look for a greeting
        if self.state == 0 and author_id != self.uid:
            self.thread_id = thread_id
            self.send(Message(text = "Hello, welcome to deepdoc. What is your name?"), thread_id=thread_id, thread_type=thread_type)
            self.state +=1

        #Look for a name
        elif self.state == 1 and author_id != self.uid and self.thread_id==thread_id:
            log.info("{} from {} in {}".format(message_object, thread_id, thread_type.name))
            self.send(Message(text ="Your name is " + message_object.text +". My name is chatbot.\nWhat's the matter?"), thread_id=thread_id, thread_type=thread_type)
            self.name = message_object.text

            log.info("name of person= " + self.name)
            self.state +=1

        #Look for a type of pain. If one is not given, end session
        elif self.state == 2 and author_id != self.uid and self.thread_id==thread_id:
            matter = message_object.text
            log.info("matter of person= " + matter)

            #see if matter is in keywords
            #
            word=''
            mat_word = matter.split(' ')
            isFound=False
            for l in self.list_:
                if l in mat_word:
                    word = l
                    isFound = True
                    self.pain = word
                    log.info(word)
                    self.send(Message(text ="Your pain point is the " + word +". On a scale of 1 to 10, how much does it hurt?"), thread_id=thread_id, thread_type=thread_type)
                    self.state += 1
                    self.list_.remove(word)
            if not isFound:
                self.state = 5
                self.send(Message(text = "Sorry we dont know about your pain point"), thread_id=thread_id, thread_type=thread_type)
                # Make json file of what data was inputted by user
                dic = {'name' : self.name, 'pains' : self.painlist}
                jsonFile = json.dumps(dic)
                log.info(jsonFile)

        #If pain was given, look for scale of pain (0-10)
        elif self.state == 3 and author_id != self.uid and self.thread_id==thread_id:
            try:
                scale = int(message_object.text)
                log.info(scale)
                if scale <0 or scale >10:
                    self.send(Message(text = "This is not a number. Try again."), thread_id=thread_id, thread_type=thread_type)
                else:
                    self.scale = scale
                    self.state = 4
                    self.send(Message(text = "How long can you say you've had this pain?"), thread_id=thread_id, thread_type=thread_type)
            except ValueError:
                self.send(Message(text = "This is not a number. Try again."), thread_id=thread_id, thread_type=thread_type)
                    
        #If pain and scale were given, look for how long the pain has been happening (just natural language)
        elif self.state == 4 and author_id != self.uid and self.thread_id==thread_id:
            painTime = int(message_object.text)
            log.info(painTime)
            self.painlist.append({'pain' : self.pain, 'scale' : self.scale, 'time' : painTime})
            self.state = 2
            self.send(Message(text = "What other pain are you experiencing?"), thread_id=thread_id, thread_type=thread_type)
            
        elif author_id != self.uid or author_id != self.clientId:
            self.send(Message(text = "The doctor is busy and talking to someone else. Try again in 5 minuites."), thread_id=thread_id, thread_type=thread_type)






client = EchoBot("deepdocproject@gmail.com", "deepdoc@oxford")
client.listen()