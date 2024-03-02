from inboxes import Inboxes
from uber import Uber
from user import User
from time import sleep
from selenium.common.exceptions import TimeoutException
import random
import os

sleep(3)

credentials = []


n = int(input('how many accounts you want to create: '))
    
for i in range(1, n+1):
    if i > 1:
        print('waiting 5 seconds before next account creation')  
    try: 
        user = User.create()
        print(user.email)
        print(user.password)

        inbox_manager = Inboxes("4c79d83e70msh2df6e098b5f94e0p1b14e3jsn42c3ea6154df")
        inbox_manager.activate_inbox(user.email)

        uber = Uber.signup(user.first_name, user.last_name, user.email, user.password, inbox_manager)

    except TimeoutException: 
            print('something unpredictable occured, retrying...')
            i -= 1
            sleep(5)
    

