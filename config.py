# format: (user):(password)@(db_identifier).amazonaws.com:3306/(db_name)

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://flask:flask123@flasktest.cxjmfdpcmp7l.ap-southeast-1.rds.amazonaws.com:3306/flaskdb'

# Uncomment the line below if you want to work with a local DB
#SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'

SQLALCHEMY_POOL_RECYCLE = 3600

WTF_CSRF_ENABLED = True
SECRET_KEY = 'oJuy3vDaEnnKLjfEYZ88lJtt4wDEBvmfFTLBbnjU'
