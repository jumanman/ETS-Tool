import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from xml_parser import parse_xml


class XMLHandler(FileSystemEventHandler):
    """文件系统事件处理器"""
    def __init__(self, app):
        self.app = app
        self.last_result = None

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".xml"):
            self._process_file(event.src_path)

    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith(".xml"):
            self._process_file(event.src_path)

    def _process_file(self, file_path):
        results = parse_xml(file_path)
        if results != self.last_result:
            self.app.update_results(results)
            self.last_result = results


class XMLMonitor:
    """XML文件监控器"""
    def __init__(self, app):
        self.app = app
        self.observer = None
        self.event_handler = None
        self.is_monitoring = False
        self.watch_dir = None
    
    def start(self, directory):
        """开始监控"""
        if self.is_monitoring:
            return False
        
        self.watch_dir = directory
        self.event_handler = XMLHandler(self.app)
        self.observer = Observer()
        
        try:
            self.observer.schedule(self.event_handler, self.watch_dir, recursive=False)
            self.observer.start()
            self.is_monitoring = True
            return True
        except Exception as e:
            print(f"启动监控失败: {e}")
            return False
    
    def stop(self):
        """停止监控"""
        if self.observer:
            self.observer.stop()
            self.observer.join()
        
        self.is_monitoring = False
        self.observer = None
        self.event_handler = None
