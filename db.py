#from sqlalchemy import create_engine
#from sqlalchemy.orm import scoped_session, sessionmaker
#from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy

#engine = create_engine('sqlite:///test.db', convert_unicode=True)
#db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
db = SQLAlchemy()

#Base = declarative_base()
#Base.query = db_session.query_property()


#def init_db():
#    import models
#    Base.metadata.create_all(bind=engine)
