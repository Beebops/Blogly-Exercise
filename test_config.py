class TestingConfig(object):
    SQLALCHEMY_DATABASE_URI = 'postgresql:///blogly_test_db'
    SQLALCHEMY_ECHO = False
    TESTING = True
    DEBUG_TB_HOSTS = ['dont-show-debug-toolbar']