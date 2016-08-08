import httplib, urllib, base64, json, sys, settings

import logging

# setup logging
logging.basicConfig(filename=settings.log_file,level=logging.DEBUG)

def get_tags(data, conf_threshold=settings.confidence_threshold):
    tag_str = ""
    for tag in data["tags"]:
        if float(tag["confidence"]) >= conf_threshold:
            if tag_str != "":
                tag_str = "{0}, {1}".format(tag_str, tag["name"])
            else:
                tag_str = tag["name"]
    return tag_str

def detect_image_tags(source_image=settings.test_source_image, az_subs_key=settings.subscription_key):

    post_body = "{\"url\":\"%s\"}" % source_image

    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': az_subs_key,
    }

    params = urllib.urlencode({
        # Request parameters
        'visualFeatures': 'Tags, Description',
        #'details': 'Celebrities',
    })

    try:
        conn = httplib.HTTPSConnection('api.projectoxford.ai')
        conn.request("POST", "/vision/v1.0/analyze?%s" % params, post_body, headers)
        response = conn.getresponse()
        js_data = response.read()
        data = json.loads(js_data)
        # print get_tags(data)
        # pretty print all the data returned by azure cv
        # print(json.dumps(data, sort_keys=True, indent=4))
        conn.close()
        return get_tags(data)
    except Exception as e:
        logging.warning("[Errno {0}] {1}".format(e.errno, e.strerror))

if __name__ == "__main__":
    print detect_image_tags()


