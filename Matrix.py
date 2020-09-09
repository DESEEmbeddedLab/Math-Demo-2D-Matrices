from OpenGL import GL, GLU, GLUT

from PyQt5 import QtCore, QtWidgets, uic

import qdarkstyle

import traceback, sys, os, shutil, math

import numpy as np

class openGLDisplay(QtWidgets.QOpenGLWidget):

    def __init__(self, *args):

        super(openGLDisplay, self).__init__(*args)
        self.zoom = 1
        self.prev_x = 0.0
        self.prev_y = 0.0
        self.updateflag = 0
        self.coordinateflag = 0
        self.center = np.array([0.0, 0.0, 0.0])
        self.front = np.array([0.0, 0.0, 1.0])
        self.up = np.array([0.0, 1.0, 0.0])
        self.matrix = np.array([[1.0, 0.0], [0.0, 1.0]])

    def paint_axis(self):
        origin = self.center

        GL.glColor3f(1.0, 0.0, 0.0)   

        GL.glBegin(GL.GL_LINES)
        GL.glVertex3f(origin[0], origin[1], origin[2])
        GL.glVertex3f(origin[0] + 0.5, origin[1], origin[2])
        GL.glEnd()        

        GL.glColor3f(0.0, 1.0, 0.0)   

        GL.glBegin(GL.GL_LINES)
        GL.glVertex3f(origin[0], origin[1], origin[2])
        GL.glVertex3f(origin[0], origin[1] + 0.5, origin[2])
        GL.glEnd()  

        GL.glColor3f(0.0, 0.0, 1.0)

        GL.glBegin(GL.GL_LINES)
        GL.glVertex3f(origin[0], origin[1], origin[2])
        GL.glVertex3f(origin[0], origin[1], origin[2] + 0.5)
        GL.glEnd()  

    def paint_coordinates(self, x, y):
        string = '(' + str(x) + ',' + str(y) + ')'
        length = len(string) - 3

        GL.glRasterPos3f(x - (0.25 + length * 0.07), y - 0.15, 0.0)
        for i in range(0, len(string)):
            GLUT.glutBitmapCharacter(GLUT.GLUT_BITMAP_HELVETICA_18, ord(string[i]))

    def paint_identity(self):
        GL.glColor3f(0.5, 0.0, 0.5)   
        GL.glBegin(GL.GL_LINES)
        for i in range(-99, 100):
            GL.glVertex3f(-100, i, 0)
            GL.glVertex3f(100, i, 0)
        GL.glEnd()

        GL.glColor3f(0.0, 0.5, 0.5)   
        GL.glBegin(GL.GL_LINES)
        for i in range(-99, 100):
            GL.glVertex3f(i, -100, 0)
            GL.glVertex3f(i, 100, 0) 
        GL.glEnd()

        GL.glColor3f(0.0, 0.0, 0.0)   
        x = int(self.center[0])
        y = int(self.center[1])

        self.paint_coordinates(0, 0)
        
        for i in range(x - 20, x + 20):
            self.paint_coordinates(i, y)

        for i in range(y - 20, y + 20):
            self.paint_coordinates(x, i)

    def paint_matrix(self, matrix):
        GL.glEnable(GL.GL_LINE_STIPPLE)

        x = matrix.dot(np.array([1.0, 0.0]))
        y = matrix.dot(np.array([0.0, 1.0]))

        GL.glColor3f(0.5, 0.0, 0.5)  
        GL.glBegin(GL.GL_LINES)
        for i in range(-99, 100):
            GL.glVertex3f(i * y[0] + x[0] * -100, i * y[1] + x[1] * -100, 0)
            GL.glVertex3f(i * y[0] + x[0] * 100, i * y[1] + x[1] * 100, 0)
        GL.glEnd()

        GL.glColor3f(0.0, 0.5, 0.5)   
        GL.glBegin(GL.GL_LINES)
        for i in range(-99, 100):
            GL.glVertex3f(i * x[0] + y[0] * -100, i * x[1] + y[1] * -100, 0)
            GL.glVertex3f(i * x[0] + y[0] * 100, i * x[1] + y[1] * 100, 0)
        GL.glEnd()

        GL.glDisable(GL.GL_LINE_STIPPLE)

        GL.glColor4f(0.4, 0.4, 0.4, 0.5)   

        GL.glBegin(GL.GL_POLYGON)
        GL.glVertex3f(0.0 , 0.0, 0.0)
        GL.glVertex3f(x[0], x[1], 0.0)
        GL.glVertex3f(x[0] + y[0], x[1] + y[1], 0.0)
        GL.glVertex3f(y[0], y[1], 0.0)
        GL.glEnd()

        w, v = np.linalg.eig(self.matrix)
        eig1 = w[0] * v[:, 0]
        eig2 = w[1] * v[:, 1]

        GL.glColor3f(0.0, 0.0, 0.0)   
        GL.glLineWidth(4)

        if(np.iscomplexobj(eig1) == False):
            GL.glBegin(GL.GL_LINES)
            GL.glVertex3f(0.0 , 0.0, 0.01)
            GL.glVertex3f(eig1[0], eig1[1], 0.01)
            GL.glEnd()

        if(np.iscomplexobj(eig2) == False):
            GL.glBegin(GL.GL_LINES)
            GL.glVertex3f(0.0 , 0.0, 0.01)
            GL.glVertex3f(eig2[0], eig2[1], 0.01)
            GL.glEnd()
        
        GL.glLineWidth(2)

    def paintGL(self):
        self.loadScene()

        GLUT.glutInit()
        GL.glClearColor(0.7, 0.7, 0.7, 0)		
        GL.glClearDepth(1)
        GL.glLineWidth(2)

        if(self.coordinateflag):
            self.paint_axis()

        self.paint_identity()

        self.paint_matrix(self.matrix)

    def initializeGL(self):
        print("\033[4;30;102m INITIALIZE GL\033[0m")
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_LINE_SMOOTH)
        GL.glHint(GL.GL_LINE_SMOOTH_HINT, GL.GL_NICEST)
        GL.glLineStipple(1, 0xAA00)

    def loadScene(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        _, _, width, height = GL.glGetDoublev(GL.GL_VIEWPORT)
        GLU.gluPerspective(
            45,
            width / float(height or 1), 
            .25, 
            200, 
        )

        cam_pos = self.center + self.front * 10
        GLU.gluLookAt(cam_pos[0], cam_pos[1], cam_pos[2], self.center[0], self.center[1], self.center[2], self.up[0], self.up[1], self.up[0])

    def mousePressEvent(self, event):
        self.prev_x = event.x()
        self.prev_y = event.y()
        self.coordinateflag = 1
        self.updateflag = 1
        self.setFocus()

    def mouseReleaseEvent(self, event):
        self.coordinateflag = 0
        self.updateflag = 1

    def mouseMoveEvent(self, event):
        x = (self.prev_x - event.x()) * math.pi / 950.0
        y = (event.y() - self.prev_y) * math.pi / 950.0

        up = self.up
        self.up = up * math.cos(y) - self.front * math.sin(y)
        self.up /= np.linalg.norm(self.up)
        self.front = self.front * math.cos(y) + up * math.sin(y)
        self.front /= np.linalg.norm(self.front)

        right = np.cross(self.up, self.front)
        self.front = self.front * math.cos(x) + right * math.sin(x)
        self.front /= np.linalg.norm(self.front)

        self.prev_x = event.x()
        self.prev_y = event.y()

        self.updateflag = 1

    def wheelEvent(self, event):
        delta = event.angleDelta().y() / 2400.0
        self.center += self.front * delta
        self.updateflag = 1

    def keyPressEvent(self, event):
        x = 0
        if(event.key() == QtCore.Qt.Key_Left):
            x = -0.1
        elif(event.key() == QtCore.Qt.Key_Right):
            x = 0.1

        self.center += x * self.zoom * np.cross(self.up, self.front)

        y = 0
        if(event.key() == QtCore.Qt.Key_Up):
            y = 0.1
        elif(event.key() == QtCore.Qt.Key_Down):
            y = -0.1

        self.center += y * self.zoom * self.up

        if(event.key() == QtCore.Qt.Key_R):
            self.front = np.array([0.0, 0.0, 1.0])
            self.up = np.array([0.0, 1.0, 0.0])
        
        if(event.key() == QtCore.Qt.Key_T):
            self.center = np.array([0.0, 0.0, 0.0])

        self.updateflag = 1

class mainWindow(QtWidgets.QMainWindow):
    
    def __init__(self):

        super(mainWindow, self).__init__()
        uic.loadUi('MatrixUI.ui', self)
        self.threadpool = QtCore.QThreadPool()

        #Tabs
        self.Tabs = self.findChild(QtWidgets.QTabWidget, 'tabWidget')
        self.Tabs.setCurrentIndex(0)

        #Display Matrix
        self.Displaymatrixbox1 = self.findChild(QtWidgets.QDoubleSpinBox, 'Displaymatrixbox1')
        self.Displaymatrixbox2 = self.findChild(QtWidgets.QDoubleSpinBox, 'Displaymatrixbox2')
        self.Displaymatrixbox3 = self.findChild(QtWidgets.QDoubleSpinBox, 'Displaymatrixbox3')
        self.Displaymatrixbox4 = self.findChild(QtWidgets.QDoubleSpinBox, 'Displaymatrixbox4')
        self.Displaymatrixbutton = self.findChild(QtWidgets.QPushButton, 'Displaymatrixbutton')

        self.Eigenvalue1box = self.findChild(QtWidgets.QLineEdit, 'Eigenvalue1box')
        self.Eigenvector11box = self.findChild(QtWidgets.QLineEdit, 'Eigenvector11box')
        self.Eigenvector12box = self.findChild(QtWidgets.QLineEdit, 'Eigenvector12box')
        self.Eigenvalue2box = self.findChild(QtWidgets.QLineEdit, 'Eigenvalue2box')
        self.Eigenvector21box = self.findChild(QtWidgets.QLineEdit, 'Eigenvector21box')
        self.Eigenvector22box = self.findChild(QtWidgets.QLineEdit, 'Eigenvector22box')
        self.Displaymatrixbutton.clicked.connect(self.Displaymatrixbuttonclicked)

        #Rotation Matrix
        self.Rotationmatrixbox = self.findChild(QtWidgets.QDoubleSpinBox, 'Rotationmatrixbox')
        self.Rotationmatrixbox.valueChanged.connect(self.Matrixboxchanged)
     
        #Scaling Matrix
        self.Scalematrixbox = self.findChild(QtWidgets.QDoubleSpinBox, 'Scalematrixbox')
        self.Scalematrixbox.valueChanged.connect(self.Matrixboxchanged)
     
        #Shear Matrix
        self.Shearmatrixbox = self.findChild(QtWidgets.QDoubleSpinBox, 'Shearmatrixbox')
        self.Shearmatrixbox.valueChanged.connect(self.Matrixboxchanged)

        #Inverse Matrix
        self.Displayinversematrixbox1 = self.findChild(QtWidgets.QDoubleSpinBox, 'Displayinversematrixbox1')
        self.Displayinversematrixbox2 = self.findChild(QtWidgets.QDoubleSpinBox, 'Displayinversematrixbox2')
        self.Displayinversematrixbox3 = self.findChild(QtWidgets.QDoubleSpinBox, 'Displayinversematrixbox3')
        self.Displayinversematrixbox4 = self.findChild(QtWidgets.QDoubleSpinBox, 'Displayinversematrixbox4')

        self.Displayadjointmatrixbox1 = self.findChild(QtWidgets.QDoubleSpinBox, 'Displayadjointmatrixbox1')
        self.Displayadjointmatrixbox2 = self.findChild(QtWidgets.QDoubleSpinBox, 'Displayadjointmatrixbox2')
        self.Displayadjointmatrixbox3 = self.findChild(QtWidgets.QDoubleSpinBox, 'Displayadjointmatrixbox3')
        self.Displayadjointmatrixbox4 = self.findChild(QtWidgets.QDoubleSpinBox, 'Displayadjointmatrixbox4')

        self.Displayinvmatrixbox1 = self.findChild(QtWidgets.QDoubleSpinBox, 'Displayinvmatrixbox1')
        self.Displayinvmatrixbox2 = self.findChild(QtWidgets.QDoubleSpinBox, 'Displayinvmatrixbox2')
        self.Displayinvmatrixbox3 = self.findChild(QtWidgets.QDoubleSpinBox, 'Displayinvmatrixbox3')
        self.Displayinvmatrixbox4 = self.findChild(QtWidgets.QDoubleSpinBox, 'Displayinvmatrixbox4')

        self.Displaydeterminantbox = self.findChild(QtWidgets.QDoubleSpinBox, 'Displaydeterminantbox')

        self.Displayinversematrixbutton = self.findChild(QtWidgets.QPushButton, 'Displayinversematrixbutton')

        #Cramer's Matrix
        self.Displaycramersmatrixbox1 = self.findChild(QtWidgets.QDoubleSpinBox, 'Displaycramersmatrixbox1')
        self.Displaycramersmatrixbox2 = self.findChild(QtWidgets.QDoubleSpinBox, 'Displaycramersmatrixbox2')
        self.Displaycramersmatrixbox3 = self.findChild(QtWidgets.QDoubleSpinBox, 'Displaycramersmatrixbox3')
        self.Displaycramersmatrixbox4 = self.findChild(QtWidgets.QDoubleSpinBox, 'Displaycramersmatrixbox4')

        self.Displaycramers1matrixbox1 = self.findChild(QtWidgets.QDoubleSpinBox, 'Displaycramers1matrixbox1')
        self.Displaycramers1matrixbox2 = self.findChild(QtWidgets.QDoubleSpinBox, 'Displaycramers1matrixbox2')
        self.Displaycramers1matrixbox3 = self.findChild(QtWidgets.QDoubleSpinBox, 'Displaycramers1matrixbox3')
        self.Displaycramers1matrixbox4 = self.findChild(QtWidgets.QDoubleSpinBox, 'Displaycramers1matrixbox4')

        self.Displaycramers2matrixbox1 = self.findChild(QtWidgets.QDoubleSpinBox, 'Displaycramers2matrixbox1')
        self.Displaycramers2matrixbox2 = self.findChild(QtWidgets.QDoubleSpinBox, 'Displaycramers2matrixbox2')
        self.Displaycramers2matrixbox3 = self.findChild(QtWidgets.QDoubleSpinBox, 'Displaycramers2matrixbox3')
        self.Displaycramers2matrixbox4 = self.findChild(QtWidgets.QDoubleSpinBox, 'Displaycramers2matrixbox4')

        self.Displaycramersdeterminantbox = self.findChild(QtWidgets.QDoubleSpinBox, 'Displaycramersdeterminantbox')

        self.Displaycramersmatrixbutton = self.findChild(QtWidgets.QPushButton, 'Displaycramersmatrixbutton')
        self.Calculatecramersbutton = self.findChild(QtWidgets.QPushButton, 'Calculatecramersbutton')


    def setupUI(self):
        print("\033[1;101m SETUP UI \033[0m")

        self.openGLWidget = openGLDisplay(self.centralwidget)
        self.openGLWidget.setGeometry(QtCore.QRect(0, 0, 1200, 950))
        self.openGLWidget.setObjectName("openGLWidget1")

        self.windowsHeight = self.openGLWidget.height()
        self.windowsWidth = self.openGLWidget.width()
        self.openGLWidget.resizeGL(self.windowsWidth, self.windowsHeight)

        self.matrix = np.array([[2.0, 0.0], [0.0, 2.0]])
        self.openGLWidget.matrix = self.matrix
        self.Displaymatrix()
        self.Displaymatrixeigen()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.updateopenGLWidget)
        self.timer.start(17)

    def updateopenGLWidget(self):
        if(self.openGLWidget.updateflag):
            self.openGLWidget.updateflag = 0
            self.openGLWidget.update()

    def mousePressEvent(self, event):
        self.setFocus()

    def Displaymatrix(self):
        self.Displaymatrixbox1.setValue(self.matrix[0,0])
        self.Displaymatrixbox2.setValue(self.matrix[0,1])
        self.Displaymatrixbox3.setValue(self.matrix[1,0])
        self.Displaymatrixbox4.setValue(self.matrix[1,1])

    def Displaymatrixbuttonclicked(self):
        self.matrix = np.array([[self.Displaymatrixbox1.value(), self.Displaymatrixbox2.value()], \
            [self.Displaymatrixbox3.value(), self.Displaymatrixbox4.value()]])
        self.openGLWidget.matrix = self.matrix
        self.openGLWidget.updateflag = 1
        self.Displaymatrixeigen()

    def Displaymatrixeigen(self):
        w, v = np.linalg.eig(self.matrix)

        if(np.iscomplexobj(w)):
            self.Eigenvalue1box.setText(str("{:.2f}".format(w[0].real)) + "+" + str("{:.2f}".format(w[0].imag)) + 'j')
            self.Eigenvalue2box.setText(str("{:.2f}".format(w[1].real)) + "+" + str("{:.2f}".format(w[1].imag)) + 'j')
        else:
            self.Eigenvalue1box.setText(str("{:.2f}".format(w[0])))
            self.Eigenvalue2box.setText(str("{:.2f}".format(w[1])))

        if(np.iscomplexobj(v)):
            self.Eigenvector11box.setText(str("{:.2f}".format(v[0, 0].real)) + "+" + str("{:.2f}".format(v[0, 0].imag)) + 'j')
            self.Eigenvector12box.setText(str("{:.2f}".format(v[1, 0].real)) + "+" + str("{:.2f}".format(v[1, 0].imag)) + 'j')
            self.Eigenvector21box.setText(str("{:.2f}".format(v[0, 1].real)) + "+" + str("{:.2f}".format(v[0, 1].imag)) + 'j')
            self.Eigenvector22box.setText(str("{:.2f}".format(v[1, 1].real)) + "+" + str("{:.2f}".format(v[1, 1].imag)) + 'j')
        else:
            self.Eigenvector11box.setText(str("{:.2f}".format(v[0, 0])))
            self.Eigenvector12box.setText(str("{:.2f}".format(v[1, 0])))
            self.Eigenvector21box.setText(str("{:.2f}".format(v[0, 1])))
            self.Eigenvector22box.setText(str("{:.2f}".format(v[1, 1])))

    def Matrixboxchanged(self):
        factor = self.Shearmatrixbox.value()
        shear = np.array([[1.0, factor], [0.0, 1.0]])

        factor = self.Scalematrixbox.value()
        scale = np.array([[factor, 0.0], [0.0, factor]])

        angle = self.Rotationmatrixbox.value() * math.pi / 180.0
        rotation = np.array([[math.cos(angle), -1 * math.sin(angle)], [math.sin(angle), math.cos(angle)]])

        self.matrix = rotation.dot(scale.dot(shear))
        self.Displaymatrix()
        self.Displaymatrixeigen()

app = QtWidgets.QApplication(sys.argv)
app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
window = mainWindow()
window.setupUI()
window.show()
sys.exit(app.exec_())