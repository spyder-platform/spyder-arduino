#!/usr/bin/python
# coding=utf-8

import RPi.GPIO as GPIO
import time
import os
import request
import getpass


class Spyder:
    GPIO_PINR = 17

    def __init__(self):
        self.token = None
        self.user_id = None
        self.previous_state = 0
        self.current_state = 0

    def run(self):
        GPIO.setmode(GPIO.BCM)

        print "Lancement... (CTRL-C pour quitter)"

        GPIO.setup(self.GPIO_PINR, GPIO.IN)

        self.authenticate_user()

        try:
            print "Attente detection..."
            while GPIO.input(self.GPIO_PINR) == 1:
                pass
            print " Pret"

            self.loop()

        except KeyboardInterrupt:
            print " Quit"

        GPIO.cleanup()

    def authenticate_user(self):
        if os.path.isfile('preferences'):
            preferences = open('preferences', 'r')
            token_line = preferences.readline().split(':')
            user_id_line = preferences.readline().split(':')
            self.token = token_line[1].split('\n')[0]
            self.user_id = user_id_line[1].split('\n')[0]

        while self.token is None or self.user_id is None:
            email = raw_input('E-mail: ')
            password = getpass.getpass('Password: ')

            login_response = request.login(email, password)

            if login_response['success']:
                preferences = open('preferences', 'w')
                preferences.write('token:' + login_response['data']['_id'] + '\n')
                preferences.write('userId:' + login_response['data']['user'] + '\n')
                self.token = login_response['data']['_id']
                self.user_id = login_response['data']['user']
            else:
                print "Erreur: " + login_response['message'].encode('UTF-8')

    def loop(self):
        while True:
            self.current_state = GPIO.input(self.GPIO_PINR)

            if self.current_state == 1 and self.previous_state == 0:
                print " Mouvement detecte !"

                # Prise de la photo
                filename = time.strftime("%d-%m-%Y@%Hh%Mm%Ss") + ".jpg"
                os.system("raspistill -vf -hf -o " + filename)

                # Upload de la photo
                movement_response = request.create_movement(filename, self.token)
                if movement_response['success']:
                    print "  Le fichier à été envoyé avec succès ! (" + movement_response['data']['_id'].encode('UTF-8') + ")"
                else:
                    print "  Erreur lors de l'envoi du fichier."
                    print "  " + movement_response['message'].encode('UTF-8')

                # Tempo
                time.sleep(5)
                self.previous_state = 1

            elif self.current_state == 0 and self.previous_state == 1:
                print " Pret "
                self.previous_state = 0

            time.sleep(1)





