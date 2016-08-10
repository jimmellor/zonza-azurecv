import ConfigParser

config = ConfigParser.ConfigParser()
config.read("settings.ini")

#Azure
subscription_key = config.get("Azure", "Subscription Key")

# ZONZA
url = config.get("ZONZA API", "Host")
port = config.get("ZONZA API", "Port")

auth = {
    'Bork-Token': config.get("ZONZA API", "Token"),
    'Bork-Username': config.get("ZONZA API", "Username"),
}

# General
log_file = config.get("General", "Log file location")
log_format = "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"
log_date_format = "%m-%d %H:%M"

# Watch for files added here
watch_location = config.get("General", "Watch folder location")

# Ignore values that are below this threshold
confidence_threshold = float(config.get("General", "Confidence Threshold"))

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