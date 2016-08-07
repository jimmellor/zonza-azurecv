import httplib, urllib, base64, json, sys, settings

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
    for celeb in data["categories"][0]["detail"]["celebrities"]:
        if float(celeb["confidence"]) >= conf_threshold:
            if celeb_str != "":
                celeb_str = "{0}, {1}".format(celeb_str, celeb["name"])
            else:
                celeb_str = celeb["name"]
    return celeb_str

def analyse_image(source_image, az_subs_key=settings.subscription_key):

    print(source_image)

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
        # Read the file into memory. It will never be big.
        f = open(source_image, 'r')
        post_body = f.read()
        f.close()

        conn = httplib.HTTPSConnection('api.projectoxford.ai')
        conn.request("POST", "/vision/v1.0/analyze?%s" % params, post_body, headers)
        response = conn.getresponse()
        js_data = response.read()
        data = json.loads(js_data)
        # print get_tags(data)
        # # pretty print all the data returned by azure cv
        # print(json.dumps(data, sort_keys=True, indent=4))
        conn.close()
        return { 'tags' : get_tags(data), 'celebrities' : get_celebrities(data) }
    except Exception as e:
        print e

if __name__ == "__main__":
    print analyse_image(settings.test_source_image_bin)

