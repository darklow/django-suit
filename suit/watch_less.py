import sys
import os
import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent


class LessCompiler(FileSystemEventHandler):

    def __init__(self, source):
        self.source = source
        FileSystemEventHandler.__init__(self)

    def compile_css(self):
        if len(sys.argv) < 3:
            destination = self.source.replace('less', 'css')
        else:
            destination = sys.argv[2]
        cmd = 'lessc %s > %s -x' % (source, os.path.abspath(destination))
        print(cmd)
        os.system(cmd)

    def on_any_event(self, event):
        if '__' not in event.src_path and isinstance(event, FileModifiedEvent):
            self.compile_css()


if __name__ == "__main__":

    if len(sys.argv) < 2:
        sys.stderr.write(
            'Usage: %s source [destination=../css/$1.css]\n' % sys.argv[0])
        sys.exit(1)

    source = os.path.abspath(sys.argv[1])
    event_handler = LessCompiler(source)
    # Run once at startup
    event_handler.compile_css()
    observer = Observer()
    observer.schedule(event_handler, os.path.dirname(source), recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
