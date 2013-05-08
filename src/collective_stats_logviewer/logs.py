import datetime
import re
from collective_stats_logviewer.model import Log


def do_it(file='log.log'):
    first_request_time = None
    last_request_time = None
    total_rendering_time = 0
    total_rss_change = 0
    num_requests = 0
    drawer = {}
    with open(file, 'rb') as logfile:
        for line in logfile.readlines():
            num_requests += 1 # This should perhaps do some checking, when zope throws an error, it's counting requests that aren't actually taking place
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
