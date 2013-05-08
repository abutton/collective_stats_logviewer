from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/stats.db'
db = SQLAlchemy(app)
Base = declarative_base()

def init_db():
	db.create_all()

class Log(db.Model):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True)
    access_time = Column(DateTime)
    publisher_time = Column(Float)
    traverse_time = Column(Float)
    commit_time = Column(Float)
    transform_time = Column(Float)
    setstate_time = Column(Float)
    total_object_loads = Column(Integer)
    object_loads_from_cache = Column(Integer)
    objects_modified = Column(Integer)
    action = Column(String)
    url = Column(String)
    start_RSS = Column(Float)
    end_RSS = Column(Float)

    def __init__(self, access_time, publisher_time, traverse_time, commit_time, transform_time, setstate_time, total_object_loads, object_loads_from_cache, objects_modified, action, url, start_RSS, end_RSS):
        self.access_time = access_time
        self.publisher_time = publisher_time
        self.traverse_time = traverse_time
        self.commit_time = commit_time
        self.transform_time = transform_time
        self.setstate_time = setstate_time
        self.total_object_loads = total_object_loads
        self.object_loads_from_cache = object_loads_from_cache
        self.objects_modified = objects_modified
        self.action = action
        self.url = url
        self.start_RSS = start_RSS
        self.end_RSS = end_RSS
