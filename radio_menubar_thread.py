import sys
import os
import urllib
import pygst
pygst.require("0.10")
import gst
from PyQt4 import QtGui, QtCore
import AddStationDialog


#music stations on a dictionary
music_stations = {'Rythmos 94.9':'http://rythmos.live24.gr:80/rythmos','Music 89.2':'http://mfile.akamai.com/6495/live/reflector:52713.asx?bkup=58044','Sfera Fm':'http://sfera.live24.gr/sfera4132'
,'Skai Radio':'http://skai.live24.gr:80/skai1003','Novasports fm':'mms://sportfm.live24.gr/sportfm7712','Mad Radio':'http://media.mad.gr/madradio','Real Thessalonikh':'http://realfm.megabyte.gr:8999'
,'Real Fm':'http://realfm.live24.gr/real','Kiss FM':'http://kissfm.live24.gr/kiss2111','Cosmoradio 95,1 Thessaloniki':'http://80.86.82.101:8130','Sohos FM 88.7':'http://85.17.121.228:8418'
,'Radio Polis 99.4':'http://85.17.121.103:8088','Venus FM 105,1':'http://62.212.82.142:8171','EllinikosFM.com':'http://159.253.149.12:9398','Laika Fm':'http://s3.onweb.gr:8474'
,'Our Boys radio':'http://83.136.86.53:8688','Relaidio FM!!!':'http://95.154.254.153:3885','ERA Sports':'http://72.91.227.18:8000','Nitro Radio':'http://nitro.live24.gr:80/nitro4555'}

#creates a playbin (plays media form an uri) 
player = gst.element_factory_make("playbin", "player")

#create volume
threads = []

	
class Radio(QtGui.QMainWindow):
		
	def __init__(self):
		super(Radio, self).__init__()
		
		self.timers = []
		self.initUI()
		
	def initUI(self):

		my_timer = QtCore.QTimer()
		self.timers.append(my_timer)
		# my_timer.timeout.connect(self.stop_dwn)
		my_timer.singleShot(1000, self.timer)

		# Buttons
		play_button = QtGui.QPushButton("Play", self)
		play_button.clicked.connect(self.play)
		stop_button = QtGui.QPushButton("Stop", self)
		stop_button.clicked.connect(self.stop_radio)
		rec_button = QtGui.QPushButton("Rec", self)
		rec_button.clicked.connect(self.Rec)
		quit_button = QtGui.QPushButton("Quit", self)
		quit_button.clicked.connect(QtCore.QCoreApplication.instance().quit)
		stop_download = QtGui.QPushButton("Stop Dwn", self)
		stop_download.clicked.connect(self.stop_dwn)
		
		#Menubar
		add_Action = QtGui.QAction('&Add Station', self)
		add_Action.setShortcut('Ctrl+A')
		add_Action.setStatusTip('Add a new radio station')
		add_Action.triggered.connect(self.add_radio)
		quit_Action = QtGui.QAction('&Quit', self)
		quit_Action.setShortcut('Ctrl+Q')
		quit_Action.setStatusTip('Quit')
		quit_Action.triggered.connect((QtCore.QCoreApplication.instance().quit))
		menubar = self.menuBar()
		fileMenu = menubar.addMenu('&File')
		fileMenu.addAction(add_Action)
		fileMenu.addAction(quit_Action)
		
		self.combo = QtGui.QComboBox(self)
		for i in music_stations:
			self.combo.addItem(i)
		
		# Layout
		hbox = QtGui.QHBoxLayout()
		hbox.addWidget(self.combo)
		hbox.addWidget(play_button)
		hbox.addWidget(stop_button)
		hbox.addWidget(rec_button)
		hbox.addWidget(stop_download)
		hbox.addWidget(quit_button)
		hbox.addStretch(1)
		
		vbox = QtGui.QVBoxLayout()
		vbox.addStretch(1)
		vbox.addLayout(hbox)
		
		widget = QtGui.QWidget()
		widget.setLayout(vbox)
		self.setCentralWidget(widget)
		
		
		self.setGeometry(300, 300, 300, 150)
		self.setWindowTitle("Radio")
		self.show()

		
		
	def play(self):

		player.set_state(gst.STATE_NULL)
		print music_stations[str(self.combo.currentText())]
		#set the uri
		music_stream_uri=music_stations[str(self.combo.currentText())]
		player.set_property('uri', music_stream_uri)
		#start playing
		player.set_state(gst.STATE_PLAYING)
	
	

	def stop_radio(self):

		print "Radio stops"
		player.set_state(gst.STATE_NULL)



	def Rec(self):

		self.rec = self.rec_thread(self.combo.currentText())
		threads.append(self.rec)
		self.rec.start()
				

				
	def add_radio(self):

		self.dialog = AddStationDialog.AddStationDialog(self)
		# self.dialog.setParent(self)
		self.dialog.setWindowTitle("Add a radio station")
		self.connect(self.dialog, QtCore.SIGNAL(self.dialog.signal), self.addstation_accepted)
		self.dialog.show()



	def stop_dwn(self):

		self.rec.terminate()



	def addstation_accepted(self):

		radio_name = str(self.dialog.radio_name.text())
		radio_adress = str(self.dialog.radio_adress.text())	
		print radio_name, radio_adress
		self.dialog.hide()


	def timer(self):
		
		print "Works"

	class rec_thread(QtCore.QThread):
		def __init__(self, name):
			QtCore.QThread.__init__(self)
			self.name = name
	  
		def run(self):
			print "Recording Now"
			music_stream_uri = music_stations[str(self.name)]
			urllib.urlretrieve(music_stream_uri, "/home/mike/record_0.mp3")



def main():
	app = QtGui.QApplication(sys.argv)
	radio = Radio()
	sys.exit(app.exec_())
	
	
if __name__ == '__main__':
	main()