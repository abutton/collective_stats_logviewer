from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.orm import sessionmaker
import datetime
import re


engine = create_engine('sqlite:///stats.db', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

def do_it(file='log.log'):
    first_request_time = None
    last_request_time = None
    total_rendering_time = 0
    total_rss_change = 0
    num_requests = 0
    drawer = {}
    with open(file, 'rb') as logfile:
        for line in logfile.readlines():
            num_requests += 1
            if line.count('INFO collective.stats'):
                pattern = re.compile("^(?P<access_time>\d+-\d+-\w+:\d+:\d+) INFO collective\.stats \| (?P<publisher_time>\d+\.\d+) (?P<traverse_time>\d+\.\d+) (?P<commit_time>\d+\.\d+) (?P<transform_time>\d+\.\d+) (?P<setstate_time>\d+\.\d+) (?P<total_object_loads>\d+) (?P<object_loads_from_cache>\d+) (?P<objects_modified>\d+) \| (?P<action>\w+:)(?P<url>.*) \| .* \| RSS\: (?P<start_RSS>\d+) - (?P<end_RSS>\d+)")
                match_result = re.match(pattern, line)
                if match_result:
                    result =  match_result.groupdict()

                    if not first_request_time:
                        request_time = datetime.datetime.strptime(result['access_time'], 
                                            "%Y-%m-%dT%H:%M:%S")
                    else:
                        request_time = datetime.datetime.strptime(result['access_time'], 
                                            "%Y-%m-%dT%H:%M:%S")             
                    id = result['url']
                    l = Log(request_time, result['publisher_time'], result['traverse_time'], result['commit_time'], result['transform_time'],
                        result['setstate_time'], result['total_object_loads'], result['object_loads_from_cache'], result['objects_modified'],
                        result['action'], result['url'], result['start_RSS'], result['end_RSS'])
                    
                    session.add(l)
                    session.commit()


class Log(Base):
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

Base.metadata.create_all(engine)

def main():
    do_it()
main()