from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys

from PyQt4.QtCore import QPoint, QTimer
from PyQt4.QtGui import QApplication, QImage, QPainter, QWidget
import socket

image_update = False

############################################################################################
def recvall(sock, count):
   buf = b''
   while count:
       newbuf = sock.recv(count)
       if not newbuf: return None
       buf += newbuf
       count -= len(newbuf)
   return buf

class camera_thread(QThread):

    send_qimage=pyqtSignal(QImage)
    def __init__(self, portnum = None, host = None):
        super(camera_thread,self).__init__()
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = portnum
        self.max_size = 8192
        self.check = True
        self.QImage = None
        self.running = True

    def setup(self,thread_no):
        self.thread_no=thread_no

    def set_portnum(self,portnum):
        self.port=portnum

    def set_host(self,host):
        self.host=host

    def stop(self):
        self.running = False

    def run(self):
        self.client.connect((self.host,self.port))
        while self.running:
            try:
                length=self.client.recv(6)
                if length[-1] == '\n':
                    length = length[0 : 5]
                else:
                    self.client.recv(1)
                stringData=recvall(self.client,int(length))
                self.QImage = QImage()#stringData, 220, 170, QImage.Format_RGB888)
                self.QImage.loadFromData(stringData)
                self.send_qimage.emit(self.QImage)
            except:
                continue

    def get_image(self):
        return self.Qimage

class img_obj(QObject):
    send_qimage = pyqtSignal(QImage)

    def __init__(self):
        self.QImage = None


    # all files come from robocopy will be saved in temp folder
    # after sending transfer the image format, send_qimage
    def read_send(self):
        pass



#QPushButton on which video_button _image is drawn
class video_button(QPushButton):
    def __init__(self, name = None,parent = None):
        super(video_button, self).__init__(parent)

        #Construct a video_source object
        #the object will read video file and emit each frame as QImage to be drawn on this button
        self.video_name = name
        self.mirrored = False

        #this stores the pixmap to be updated everytime the button receives a QImage
        #initialize it to be the very first _image(frame) of the video source
        self.image = QImage("test.png")
        self.pixmap = QPixmap.fromImage(self.image)
        self.pixmap = self.pixmap.scaled(self.size(), Qt.KeepAspectRatio)
        self.Transform = QTransform()
        self.Transform.rotate(180)

    # this method handles the QImage received from video_source
    # stores QImgage in self.pixmap and call self.update to draw the _image on button
    # the received QImage is still in its original resolution
    def set_image(self, mQImage):
        if self.mirrored:
            mQImage = mQImage.mirrored()
        self.image = mQImage
        self.pixmap = QPixmap.fromImage(mQImage)
        self.update()

    def set_mirrored(self):
        self.mirrored = True


    def restart(self):
        self.video_source.restart_video()
    #will be called automatically everytime self.update is called
    def paintEvent(self, event):
        painter = QPainter(self)
        # resize self.pixmap to fit the button size
        # and keep its aspect ratio
        self.pixmap = self.pixmap.scaled(self.size(), Qt.KeepAspectRatio)
        #calculate x and y coordinate of the pixmap to make sure
        #the picture is drawn on center of the button
        new_width = self.pixmap.width()
        new_height = self.pixmap.height()
        x = self.width()/2 - new_width/2
        y = self.height()/2 - new_height/2
        painter.drawPixmap(x, y, new_width, new_height, self.pixmap)

    #this will disconnect self.set_image with the signal of the original video source
    #and reconnect it with a new signal
    def set_source(self,new_signal):
        # self.video_source.send_qimage.disconnect(self.set_image)
        self.video_source = new_signal
        self.video_source.send_qimage.connect(self.set_image)


#QFrame containing video_button button; border responds to mouse over event
class VideoFrame(QFrame):

    def __init__(self,parent):
        super(VideoFrame, self).__init__(parent)
        self.setStyleSheet('')
    def enterEvent(self, QEvent):
            self.setStyleSheet('VideoFrame{border: 2px solid #525252; border-radius: 5px}')
            return QFrame.enterEvent(self, QEvent)
    def leaveEvent(self, QEvent):
            self.setStyleSheet('')
            return QFrame.leaveEvent(self, QEvent)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    source = video_button()
    source.show()
    sys.exit(app.exec_())