#!/usr/bin/env python

import sys, os
import time
import settings
from syslogger import logger

from vidixmlparser import get_item_id
import azure_cv_analyse
import azure_cv_ocr
import update_item_metadata

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

def get_source_image(event_file_path):
    return os.path.splitext(event_file_path)[0] + settings.source_image_ext

def clean_up(event_file_path):
    os.remove(event_file_path)
    os.remove(get_source_image(event_file_path))

def handle_file(event_file_path):
    if os.path.isfile(event_file_path):
        try:
            item_id = get_item_id(event_file_path)

            source_image = get_source_image(event_file_path)

            logger.debug("Analysing {} using Azure CV".format(source_image))

            analysis_data = azure_cv_analyse.analyse_image(source_image)
            ocr_data = azure_cv_ocr.ocr_image(source_image)

            logger.debug("Analyse detected {}, OCR detected {}".format(analysis_data, ocr_data))

            if analysis_data != None:
                if analysis_data["tags"] != "":
                    logger.debug("Updating ZONZA:")
                    update_item_metadata.update_field(item_id, settings.tags_field, analysis_data["tags"])

                if analysis_data["celebrities"] != "":
                    logger.debug("Updating ZONZA:")
                    update_item_metadata.update_field(item_id, settings.celebrities_field, analysis_data["celebrities"])

            if ocr_data != None:
                if ocr_data["language"] != "" and ocr_data["language"] != "unk":
                    logger.debug("Updating ZONZA:")
                    update_item_metadata.update_field(item_id, settings.lang_field, ocr_data["language"])

                if ocr_data["text"] != "":
                    logger.debug("Updating ZONZA:")
                    update_item_metadata.update_field(item_id, settings.text_field, ocr_data["text"])

            # keep it tidy
            clean_up(event_file_path)

        except Exception, e:
            logger.warning(e)


class XMLHandler(PatternMatchingEventHandler):
    patterns=["*.xml"]

    def process(self, event):
        handle_file(event.src_path)

    def on_modified(self, event):
        self.process(event)

    # def on_created(self, event):
    #     self.process(event)


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