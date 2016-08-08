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

def get_celebrities(data, conf_threshold=settings.confidence_threshold):
    celeb_str = ""

    for category in data["categories"]:
        if "people" in category["name"]:
            celebrities = category["detail"]["celebrities"]
            for celeb in celebrities:
                if float(celeb["confidence"]) >= conf_threshold:
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

    # try:
    # Read the file into memory
    f = open(source_image, 'r')
    post_body = f.read()
    f.close()

    conn = httplib.HTTPSConnection('api.projectoxford.ai')
    conn.request("POST", "/vision/v1.0/analyze?%s" % params, post_body, headers)
    response = conn.getresponse()
    js_data = response.read()
    data = json.loads(js_data)
    logging.info(data)
    conn.close()
    return { 'tags' : get_tags(data), 'celebrities' : get_celebrities(data) }
    # except Exception as e:
        # logging.warning(e)

if __name__ == "__main__":
    print analyse_image(settings.test_source_image_bin)


