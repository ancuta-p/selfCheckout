import threading

import speech_recognition as sr
import pyttsx3


class SpeechRocognition:
    def __init__(self, form):
        self.form = form

    def _speechToText(self, recognizer, microphone):
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        response = {"success": True,
                    "error": None,
                    "transcription": None}
        try:
            response["transcription"] = recognizer.recognize_google(audio)
        except sr.RequestError:
            response["success"] = False
            response["error"] = "API unavailable"
        except sr.UnknownValueError:
            response["success"] = False
            response["error"] = "Unable to recognize speech"
        return response

    def _textToSpeech(self, engine, myText):
        engine.say(myText)
        engine.runAndWait()

    def _runCmd(self, text):
        if text == "hello" or text == "start":
            self.form.clickStart()
        if text == "enter":
            self.form.clickEnter()
        if text == "search item":
            self.form.clickSearch()
        if text == "back":
            self.form.clickBack()
        if text.find("finish") != -1 or text.find("pay") != -1:
            self.form.clickFinish()
        if text == "exit":
            self.form.close()

    def run(self):
        engine = pyttsx3.init()
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()

        action = 'Listening'
        print(action)
        self._textToSpeech(engine, action)

        quitFlag = True
        while (quitFlag):
            text = self._speechToText(recognizer, microphone)
            if not text["success"] and text["error"] == "API unavailable":
                print("ERROR: {}\nclose program".format(text["error"]))
                break
            while not text["success"]:
                print("I didn't catch that. What did you say?\n")
                text = self._speechToText(recognizer, microphone)

            self._runCmd(text["transcription"].lower())

            if text["transcription"].lower() == "exit":
                quitFlag = False

            print(text["transcription"].lower())
            self._textToSpeech(engine, text["transcription"].lower())
