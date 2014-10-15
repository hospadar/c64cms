from __future__ import print_function
import watchdog, os
from watchdog.observers import Observer
try:
    import SimpleHTTPServer
except:
    import http.server as SimpleHTTPServer

try:
    import SocketServer
except:
    import socketserver as SocketServer
    
from argparse import ArgumentParser
from generator import generate
import traceback


class EventHanlder(watchdog.events.FileSystemEventHandler):
    in_path = ""
    out_path = ""
    template_dir = ""
    base_dir = ""
    def on_any_event(self, event):
        try:
            print("File changed, regenerating")
            os.chdir(self.base_dir)
            generate(self.in_path, self.out_path, self.template_dir)
            os.chdir(self.out_path)
        except:
            traceback.print_exc()
        
def dev_server(in_path, out_path, template_dir, port):
    current_dir = os.getcwd()
    observer = Observer()
    event_handler  = EventHanlder()
    event_handler.in_path = os.path.abspath(in_path)
    event_handler.out_path = os.path.abspath(out_path)
    event_handler.template_dir = os.path.abspath(template_dir)
    event_handler.base_dir = os.path.abspath(current_dir)
    observer.schedule(event_handler, os.path.abspath(in_path), recursive=True)
    observer.schedule(event_handler, os.path.abspath(template_dir), recursive=True)
    observer.start()
    
    os.chdir(out_path)
    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    httpd = SocketServer.TCPServer(("", port), Handler)
    try:
        print("Serving on http port " + str(port))
        httpd.serve_forever()
    except KeyboardInterrupt:
        observer.stop()
        #t_observer.stop()
    observer.join()
    #t_observer.join()
    
if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("in_path", nargs="?", help="input directory", default="source")
    parser.add_argument("out_path", nargs="?", help="output directory", default="output")
    parser.add_argument("-d", "--dev-server", help="Run dev server instead of just generating output", action="store_true")
    parser.add_argument("-p", "--port", help="port for dev server", default=8000, type=int)
    parser.add_argument("-t", "--template-dir", default="templates", help="Directory to find templates")
    
    options = parser.parse_args()
    
    generate(options.in_path, options.out_path, options.template_dir)
    if options.dev_server:
        dev_server(options.in_path, options.out_path, options.template_dir, options.port)