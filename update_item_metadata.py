import httplib
import json
import settings
import logging

# setup logging
logging.basicConfig(filename=settings.log_file,level=logging.DEBUG)


def update_field(item, field_id, field_value, auth=settings.auth):
	headers = {'content-type': 'application/json'}
 	headers.update(auth)
	post_body = json.dumps({field_id: field_value})
	try:
		conn = httplib.HTTPConnection(settings.url, settings.port)
		conn.request("POST", "/v0/item/{}/metadata".format(item), post_body, headers)
		response = conn.getresponse()
		data = response.read()
		logging.info("Updating metadata for: {}/v0/item/{}/metadata".format(settings.url, item))
		logging.info(post_body)

	except Exception as e:
		logging.warning("[Errno {0}] {1}".format(e.errno, e.strerror))

if __name__ == "__main__":
	print "Updating metadata for {}".format(settings.test_item)
	update_field(settings.test_item, settings.test_field_id, settings.test_field_value)