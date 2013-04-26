from app import db
import datetime
import re
import StringIO
from sqlalchemy import func


class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    access_time = db.Column(db.DateTime)
    publisher_time = db.Column(db.Float)
    traverse_time = db.Column(db.Float)
    commit_time = db.Column(db.Float)
    transform_time = db.Column(db.Float)
    setstate_time = db.Column(db.Float)
    total_object_loads = db.Column(db.Integer)
    object_loads_from_cache = db.Column(db.Integer)
    objects_modified = db.Column(db.Integer)
    action = db.Column(db.String)
    url = db.Column(db.String)
    start_RSS = db.Column(db.Float)
    end_RSS = db.Column(db.Float)

    def __init__(self, access_time, publisher_time, traverse_time, commit_time,
                 transform_time, setstate_time, total_object_loads,
                 object_loads_from_cache, objects_modified, action, url,
                 start_RSS, end_RSS):
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

    def __repr__(self):
        return '<Log %r>' % (self.id)


def do_it(thelog):
    first_request_time = None
    last_request_time = None
    total_rendering_time = 0
    total_rss_change = 0
    num_requests = 0
    thelog = StringIO.StringIO(thelog)
    count_beg = db.session.query(func.count(Log.id)).scalar()
    for line in thelog.readlines():
        num_requests += 1
         # print line
        if line.count('INFO collective.stats'):
            pattern = re.compile("^(?P<access_time>\d+-\d+-\w+:\d+:\d+) INFO collective\.stats \| (?P<publisher_time>\d+\.\d+) (?P<traverse_time>\d+\.\d+) (?P<commit_time>\d+\.\d+) (?P<transform_time>\d+\.\d+) (?P<setstate_time>\d+\.\d+) (?P<total_object_loads>\d+) (?P<object_loads_from_cache>\d+) (?P<objects_modified>\d+) \| (?P<action>\w+:)(?P<url>.*) \| .* \| RSS\: (?P<start_RSS>\d+) - (?P<end_RSS>\d+)")
            match_result = re.match(pattern, line)
            if match_result:    
                result = match_result.groupdict()
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

                db.session.add(l)
                db.session.commit()
    # import pdb; pdb.set_trace()
    count_after = db.session.query(func.count(Log.id)).scalar()
    # print count_after; print count_beg
    if count_after > count_beg:
        return True
    else:
        return False
        