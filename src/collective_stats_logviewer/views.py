from flask import render_template
from flask import Flask
from flask import jsonify
from flask import request
from model import db
from model import query_reqs_sec, query_time_per_request, query_optimal_requests, query_current_capacity
import logs


class _DefaultSettings(object):
    USERNAME = 'world'
    SECRET_KEY = 'development key'
    DEBUG = True

app.config.from_object(_DefaultSettings)
del _DefaultSettings

@app.route('/')
@app.route('/index/')
def index():
    """Renders the index pages of collective stats. Queries the db to pull
    overall server load stats, as well as basic stats for each offending url.
    More detailed stats for each url are queried and served by
    response_time_details() using an ajax request"""
    # Assignment
    #reqs_sec = query_reqs_sec()
    #time_per_request = query_time_per_request()
    #optimal_requests = query_optimal_requests()
    #current_capacity = query_current_capacity()

    data_store = {}
    data_store['instance_stats'] = {'reqs_sec': 20, 'time_per_request': 12, 'optimal_requests': 10, 'cc_percentage': 30}
    data_store['slow_pages'] = [{'url': '/newscenter/inthenewsview', 'avg_time': 38.88},
                                {'url': '/departments/name', 'avg_time': 31.25}]
    data_store['server_chokers'] = [{'url': '/departments/name/', 'total_server_time': 246.88},
                                   {'url': '/departments/ners/', 'total_server_time': 166.87}]
    data_store['memory_hogs'] = [{'url': '/departments/cheme/', 'memory_used': 8.76},
                                 {'url': '/departments/name/', 'memory_used': 8.59}]
    return render_template("index.html", data=data_store)


@app.route('/response_time_details/', methods=['GET'])
def response_time_details():
    """Queries db for detailed stats for a specific url. This function is
    called from an ajax request, which sends the url as a GET request
    and returns a json object with details about rendering time, num hits, etc
    for that url. This also returns the data necessary to render the graph for
    that url."""

    url = request.args.get('url', '')

    graph_data = [
       { "timestamp": "2013-02-18T20:18:15",
           "render_time": "0.7223",
       },
       { "timestamp": "2013-02-18T20:18:25",
           "render_time": "1.4157",
       },
       { "timestamp": "2013-02-18T20:21:14",
           "render_time": "4.567",
       }
    ]

    stats_data = {'overall': 42.77, 'num_hits': 14, 'cached_benefit': 1.0003, 'avg': 2.3}
    return jsonify(url=url, graph_data=graph_data, stats_data=stats_data)

@app.route('/super_url/', methods=['POST'])
def super_url():
	line = request.form["line"] 
	line_number = request.form["line_number"]	
	do_it(line)
	return jsonify(line=None, line_number=line_number)

@app.route('/receive_json/', methods=['POST'])
def receive_json():
    pass
