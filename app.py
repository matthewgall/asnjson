#!/usr/bin/env python

import os, sys, argparse, logging, json, base64
import requests, redis
from functools import lru_cache
from bottle import route, request, response, redirect, default_app, view, template, static_file
from cymruwhois import Client
from classes.address import Address

def enable_cors(fn):
	def _enable_cors(*args, **kwargs):
		response.headers['Access-Control-Allow-Origin'] = '*'
		response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
		response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

		if request.method != 'OPTIONS':
			return fn(*args, **kwargs)
	return _enable_cors

def return_error(status=404, message=''):
	log.error(message)
	output = {
		'success': False,
		'message': message
	}
	response.status = status
	return json.dumps(output)

@route('/static/<filepath:path>')
def static(filepath):
	return static_file(filepath, root='views/static')

@route('/<ip>', method=('OPTIONS', 'GET'))
@route('/<ip>/<contentType>', method=('OPTIONS', 'GET'))
@enable_cors
def process(ip, contentType='html'):

	if ip in ["favicon.ico", "robots.txt"]:
		return ""

	output = {
		"success": True,
		"results": [],
		"results_info": {
			"count": 0,
			"cached": 0
		}
	}

	uri = ip
	lookups = []
	for ip in ip.split(','):
		try:
			Address(ip)
			if r.get(ip):
				output['results'].append(json.loads(r.get(ip)))
				output['results_info']['cached'] = output['results_info']['cached'] + 1
			else:
				lookups.append(ip)
		except AttributeError:
			return return_error(400, "{} is not a valid IP address".format(ip))

		for address in Client().lookupmany(lookups):
			data = {
				"ip": address.ip,
				"asn": address.asn,
				"prefix": address.prefix,
				"owner": address.owner,
				"cc": address.cc
			}

			# Now we push it to redis
			r.set(address.ip, json.dumps(data), ex=84600)
			output['results'].append(json.loads(r.get(address.ip)))

	output['results_info']['count'] = len(output['results'])
	if contentType in ['json']:
		response.headers['Content-Type'] = 'application/json'
		return json.dumps(output)
	else:
		response.headers['Content-Type'] = 'text/html'
		return template("rec", uri=uri, data=output['results'])

@route('/cache')
def cache():
	try:
		output = {}
		for key in r.scan_iter('*'):
			output[key.decode("utf-8")] = json.loads(r.get(key))
		response.headers['Content-Type'] = 'application/json'
		return json.dumps(output)
	except:
		return return_error(403, "Unable to load keys from redis for display. Please try again later.")

@route('/ping')
def ping():
	response.content_type = "text/plain"
	return "pong"

@route('/', ('GET', 'POST'))
def index():
	if request.method == "POST":
		if request.forms.get('address', '') != '':
			return redirect("/{}".format(request.forms.get('address')))
	return template("home")

if __name__ == '__main__':

	parser = argparse.ArgumentParser()

	# Server settings
	parser.add_argument("-i", "--host", default=os.getenv('HOST', '127.0.0.1'), help="server ip")
	parser.add_argument("-p", "--port", default=os.getenv('PORT', 5000), help="server port")

	# Redis settings
	parser.add_argument("--redis", default=os.getenv('REDIS', 'redis://localhost:6379/0'), help="redis connection string")

	# Verbose mode
	parser.add_argument("--verbose", "-v", help="increase output verbosity", action="store_true")
	args = parser.parse_args()

	if args.verbose:
		logging.basicConfig(level=logging.DEBUG)
	else:
		logging.basicConfig(level=logging.INFO)
	log = logging.getLogger(__name__)

	try:
		if args.redis:
			r = redis.from_url(args.redis)
	except:
		log.fatal("Unable to connect to redis: {}".format(args.redis))

	try:
		app = default_app()
		app.run(host=args.host, port=args.port, server='tornado')
	except:
		log.error("Unable to start server on {}:{}".format(args.host, args.port))
