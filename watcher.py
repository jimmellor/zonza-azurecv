import sys, os
import time
import settings
from vidixmlparser import get_item_id
import azure_cv_analyse
import update_item_metadata

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

def get_source_image(event_file_path):
    return os.path.splitext(event_file_path)[0] + settings.source_image_ext

def clean_up(event_file_path):
    os.remove(event_file_path)
    os.remove(get_source_image(event_file_path))

def handle_file(event_file_path):
    try:
        item_id = get_item_id(event_file_path)

        source_image = get_source_image(event_file_path)

        detected_data = azure_cv_analyse.analyse_image(source_image)

        print(detected_data)

        print("about to update ZONZA")

        if detected_data["tags"] != "":
            update_item_metadata.update_field(item_id, settings.tags_field, detected_data["tags"])

        if detected_data["celebrities"] != "":
            update_item_metadata.update_field(item_id, settings.celebrities_field, detected_data["celebrities"])
            
    except Exception, e:
        print e


class XMLHandler(PatternMatchingEventHandler):
    patterns=["*.xml"]

    def process(self, event):
        handle_file(event.src_path)

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)


if __name__ == '__main__':
    args = sys.argv[1:]
    observer = Observer()
    observer.schedule(XMLHandler(), path=settings.watch_location)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()