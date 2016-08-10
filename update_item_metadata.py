import httplib
import json
import settings
from syslogger import logger

def update_field(item, field_id, field_value, auth=settings.auth):
	headers = {'content-type': 'application/json'}
 	headers.update(auth)
	post_body = json.dumps({field_id: field_value})
	try:
		conn = httplib.HTTPConnection(settings.url, settings.port)
		conn.request("POST", "/v0/item/{}/metadata".format(item), post_body, headers)
		response = conn.getresponse()
		data = response.read()
		logger.info("Updating metadata for {}/v0/item/{}/metadata with {}".format(settings.url, item, post_body))

	except Exception as e:
		logger.warning("[Errno {0}] {1}".format(e.errno, e.strerror))