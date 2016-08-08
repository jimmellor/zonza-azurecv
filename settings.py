# Watch for files added here
watch_location = "/Users/mellor/Development/zonza-azurecv"

# ZONZA Bork Auth token
auth = {
    'Bork-Token': "ZGM1ZmJhMDktZjY4YS00YjQwLThlNmYtYjNjYTAwNzFmM2U5",
    'Bork-Username': "jim.mellor@hogarthww.com",
}

# Azure subscription key
subscription_key = "1aa6ae8b25d7436388e872bc9bea55b2"

# Only tag assets with Azure CV confidence great than this threshold
confidence_threshold = 0.4

# ZONZA Config:
# ZONZA API URL
url = 'api.zonza.tv'
port = 8080

# for testing bork
test_item = 'VX-750794'
test_field_id = 'demo_keywords'
test_field_value = 'test, testing, 123'

# type of image files to expect in the watch location
source_image_ext = ".jpeg"

# field for tags
tags_field = 'demo_keywords'

#field for detected celebrities
celebrities_field = 'demo_featured_celebrities'

#field for detected text       
text_field = 'demo_detected_text'

#field for detected language
lang_field = 'demo_detected_lang'

# test source image
test_source_image_bin = "jayz.jpg"