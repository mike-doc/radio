from PyQt4 import QtGui, QtCore

class AddStationDialog(QtGui.QDialog):
	def __init__(self, parent):

		QtGui.QDialog.__init__(self)
		self.signal = "addstation"
		# parent.setEnabled(False)
		self.setParent(parent)

		self.radio_name = QtGui.QLineEdit()
		self.radio_adress = QtGui.QLineEdit()
		self.radio_name.setPlaceholderText("Give the name of the radio station")
		self.radio_adress.setPlaceholderText("Give the address of the radio station")
		self.radio_label = QtGui.QLabel()
		self.radio_name_label = QtGui.QLabel()
		self.radio_name_label.setText("Give the name of the radio:      ")
		self.radio_adress_label = QtGui.QLabel("Give the address of the radio: ")

		buttonbox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
		buttonbox.accepted.connect(self.accept)
		buttonbox.rejected.connect(self.reject)

		vbox = QtGui.QVBoxLayout()
		hbox = QtGui.QHBoxLayout()
		hbox1 = QtGui.QHBoxLayout()
		hbox2 = QtGui.QHBoxLayout()
		hbox1.addWidget(self.radio_name_label)
		hbox1.addWidget(self.radio_name)
		hbox2.addWidget(self.radio_adress_label)
		hbox2.addWidget(self.radio_adress)
		vbox.addLayout(hbox1)
		vbox.addLayout(hbox2)
		hbox.addWidget(self.radio_label)
		hbox.addWidget(buttonbox)
		vbox.addLayout(hbox)
		self.setLayout(vbox)
		self.setFixedSize(450, 100)

		self.setWindowFlags(QtCore.Qt.Dialog)


	def accept(self):

		if self.radio_name.text() == "" or self.radio_adress.text() == "":

			self.radio_label.setText("You must fill both fields")


		if self.radio_name.text() != "" and self.radio_adress.text() != "":

			self.emit(QtCore.SIGNAL(self.signal))



	def reject(self):
		self.hide()