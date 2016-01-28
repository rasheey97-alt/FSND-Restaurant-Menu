from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant
import datetime
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()    

class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                restaurants = session.query(Restaurant).order_by(Restaurant.name)
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<p><a href='restaurants/new'>Add a Restaurant</a></p>"
                output += "<h1>All Restaurants</h1>"
                for restaurant in restaurants:
                    output += "<h3 style='margin-bottom: 0px;'> %s </h3>" % restaurant.name
                    output += "<a href='#'>edit</a> - <a href='#'>delete</a>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Add a New Restaurant</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><h2>What's the name?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            ctype, pdict = cgi.parse_header(
                self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                newInput = fields.get('message')
                newRestaurant = Restaurant(name = newInput[0])
                session.add(newRestaurant)
                session.commit()
            output = ""
            output += "<html><body>"
            output += "<h2> You added </h2>"
            output += "<h1> %s </h1>" % newInput[0]
            output += "<p><a href='/restaurants'>Go Back to the List</a></p>"
            output += "</body></html>"
            self.wfile.write(output)
            print output
        except:
            pass

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()