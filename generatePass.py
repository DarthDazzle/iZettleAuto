import pickle
import requests
import json
import os

from cryptography.fernet import Fernet
from shutil import copyfileobj
from bs4 import BeautifulSoup
from datetime import datetime
# Simple dict with user name : user id
from iZettleUsers import *

def main():
	file = open('key','rb')
	key = pickle.load(file)
	print('Enter password:')
	passWord = input()
	f = Fernet(key)
	token = f.encrypt(passWord.encode())
	with open("pass",'wb') as handle:
		pickle.dump(token, handle)



if __name__ == '__main__':
	main()
            