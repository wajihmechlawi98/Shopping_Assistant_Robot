import http.server
import socketserver
import json
from std_msgs.msg import String
import rospy
from random import randint
import qrcode
from PIL import Image
import webbrowser


posePublisher = rospy.Publisher('desired_Pose', String, queue_size=1)
rospy.init_node('webInterface', anonymous=True)

# Create a dictionary to map paths to desired poses
pose_mapping = {
    '/position1': 'position1',
    '/position2': 'position2',
    '/position3': 'position3'
}


class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/':
            self.path = 'gui.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        # Handle the POST request
        if self.path in pose_mapping:
            desired_pose = pose_mapping[self.path]

            rospy.loginfo("desired_pose: %s" % desired_pose)
            posePublisher.publish(desired_pose)

            # Read the request body
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)

            # Parse the JSON data
            data = json.loads(body)

            # Extract the value from the JSON data
            value = data.get('value')

            # Process the value as needed
            response = str(value)

            # Send the response back to the client
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(response.encode())

# Data to be encoded
 
# Encoding data using make() function
# if __name__ == '__main__':
# Create an object of the above class
try:
    handler_object = MyHttpRequestHandler
    PORT = randint(1000,8000)
    port_str = str(PORT)

    link = "http://10.42.0.1:"+port_str
    img = qrcode.make(link)
    img.save('qr_link.png')

    imgDisp = Image.open("qr_link.png")
    imgDisp.show()
    my_server = socketserver.TCPServer(("10.42.0.1", PORT), handler_object)
    print("starting webserver at ip: http://10.42.0.1:%s" % port_str)
    webbrowser.open('http://10.42.0.1:%s' % port_str)
    
        # Star the server
    my_server.serve_forever()
except KeyboardInterrupt:
    print("KeyboardInterrupt detected, shutting down...")
    my_server.server_close()
    my_server.shutdown()