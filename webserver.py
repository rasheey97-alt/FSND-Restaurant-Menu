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
                    output += "<a href='restaurants/%s/edit'>edit</a> - <a href='#'>delete</a>" % restaurant.id
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
                output += '''<form method='POST' enctype='multipart/form-data' 
                    action='/restaurants/new'><h2>What's the name?</h2>
                    <input name="message" type="text" >
                    <input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/edit"):
                restaurantIDPath = self.path.split("/")[2]
                restaurant = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
                if restaurant != []:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = ""
                    output += "<html><body>"
                    output += "<h2>Rename %s</h2>" % restaurant.name
                    output += '''<form method='POST' enctype='multipart/form-data' 
                        action='/restaurants/%s/edit'>
                        <h2>What's the new name?</h2>
                        <input name="message" type="text" >
                        <input type="submit" value="Submit"> </form>''' % restaurant.id
                    output += "</body></html>"
                    self.wfile.write(output)
                    print output
                    return


        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                newInput = fields.get('message')
                
                # Create new Restaurant Class
                newRestaurant = Restaurant(name = newInput[0])
                session.add(newRestaurant)
                session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
            
            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                        fields = cgi.parse_multipart(self.rfile, pdict)
                        newInput = fields.get('message')
                        restaurantIDPath = self.path.split("/")[2]

                        restaurant = session.query(Restaurant).filter_by(id = 
                            restaurantIDPath).one()

                        if restaurant != []:
                            restaurant.name = newInput[0]
                            session.add(restaurant)
                            session.commit()

                            self.send_response(301)
                            self.send_header('Content-type', 'text/html')
                            self.send_header('Location', '/restaurants')
                            self.end_headers()

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