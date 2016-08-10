import httplib
import urllib
import base64
import json
import sys
import settings
import logging

# setup logging
logging.basicConfig(filename=settings.log_file,format=settings.log_format,datefmt=settings.log_date_format,level=logging.DEBUG)


def get_tags(data, conf_threshold=settings.confidence_threshold):
    tag_str = ""
    for tag in data["tags"]:
        if float(tag["confidence"]) >= conf_threshold:
            if tag_str != "":
                tag_str = "{0}, {1}".format(tag_str, tag["name"])
            else:
                tag_str = tag["name"]
    return tag_str

def get_celebrities(data, conf_threshold=settings.confidence_threshold):
    celeb_str = ""

    for category in data["categories"]:
        if "detail" in category.keys():
            print "got detail"
            celebrities = category["detail"]["celebrities"]
            for celeb in celebrities:
                if celeb["confidence"] >= conf_threshold:
                    if celeb_str != "":
                        celeb_str = "{0}, {1}".format(celeb_str, celeb["name"])
                    else:
                        celeb_str = celeb["name"]
    return celeb_str

def analyse_image(source_image, az_subs_key=settings.subscription_key):

    headers = {
        # Request headers
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': az_subs_key,
    }

    params = urllib.urlencode({
        # Request parameters
        'visualFeatures': 'Tags, Description',
        'details': 'Celebrities',
    })

    try:
        # Read the file into memory
        f = open(source_image, 'r')
        post_body = f.read()
        f.close()

        conn = httplib.HTTPSConnection('api.projectoxford.ai')
        conn.request("POST", "/vision/v1.0/analyze?%s" % params, post_body, headers)
        response = conn.getresponse()
        js_data = response.read()
        logging.debug("Azure Analyse returned {}".format(js_data))
        data = json.loads(js_data)
        conn.close()
        return { 'tags' : get_tags(data), 'celebrities' : get_celebrities(data) }
    except Exception as e:
        logging.warning(e)

