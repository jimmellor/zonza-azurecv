import httplib, urllib, base64, json, sys, settings

def get_language(data):
    return data["language"]

def get_text(data):
    text = ""
    for region in data["regions"]:
        region_text = u""
        for line in data["regions"][0]["lines"]:
            line_text = u""
            for word in line["words"]:
                if line_text != u"":
                    line_text = u"{0} {1}".format(line_text, word["text"])
                else:
                    line_text = word["text"]
            if region_text != "":
                print region_text
                print line_text
                region_text = u"{0}\n{1}".format(region_text.encode('utf-8'), line_text)
            else:
                region_text = line_text
        if text != "":
            text = u"{0}\n\n{1}".format(text, region_text)
        else:
            text = region_text
    return text.encode('utf-8')

def ocr_image(source_image, az_subs_key=settings.subscription_key):

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

    #try:
    # Read the file into memory
    f = open(source_image, 'r')
    post_body = f.read()
    f.close()

    conn = httplib.HTTPSConnection('api.projectoxford.ai')
    conn.request("POST", "/vision/v1.0/ocr?%s" % params, post_body, headers)
    response = conn.getresponse()
    js_data = response.read()
    data = json.loads(js_data)
    #print get_text(data)
    # pretty print all the data returned by azure cv
    #print(json.dumps(data, sort_keys=True, indent=4))
    conn.close()
    return { 'language' : get_language(data), 'text' : get_text(data) }
    #except Exception as e:
    #    print e

if __name__ == "__main__":
    print analyse_image(settings.test_source_image_bin)


