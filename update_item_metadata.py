import httplib
import json
import settings

def update_field(item, field_id, field_value, auth=settings.auth):
	headers = {'content-type': 'application/json'}
 	headers.update(auth)
	post_body = json.dumps({field_id: field_value})
	print post_body
	try:
		conn = httplib.HTTPConnection(settings.url, settings.port)
		conn.request("POST", "/v0/item/{}/metadata".format(item), post_body, headers)
		response = conn.getresponse()
		data = response.read()
		print "Updating metadata for: " + "{}/v0/item/{}/metadata".format(settings.url, item)
	except Exception as e:
		print("[Errno {0}] {1}".format(e.errno, e.strerror))

if __name__ == "__main__":
	print "Updating metadata for {}".format(settings.test_item)
	update_field(settings.test_item, settings.test_field_id, settings.test_field_value)