import os

import logging

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
	'sqlite:///' + os.path.join(basedir, 'doraemon.db')

	SQLALCHEMY_TRACK_MODIFICATIONS = True

	AVA_UPLOAD_DIR = os.path.join(basedir, 'static/uploaded_AVA')
	AVATARS_SAVE_PATH = os.path.join(basedir, 'static/commodity')


	# logging.basicConfig(filename="record.log", level=logging.INFO, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')




