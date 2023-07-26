from PySide2 import QtCore, QtWidgets, QtGui
import os, subprocess
import numpy as np
from herptest import canvas_interface

class CanvasUploadPage(canvas_interface.AbstractCanvasInterface):

    def __init__(self, user_type):
        super().__init__(user_type=user_type)
        self.fileReady = False

    def createControls(self):
        #this method gets called during the parent class's createUI method and injects the necessary controls
        self.uploadContainer = QtWidgets.QGridLayout()
        self.csvLabel = QtWidgets.QLabel("Select CSV to Upload")
        self.csvLabel.setMaximumHeight(50)
        self.csvPathField = QtWidgets.QLineEdit()
        self.csvSelect = QtWidgets.QPushButton("Browse")
        self.csvSelect.setFixedWidth(100)
        self.csvSelect.clicked.connect(self.uploadFilePicker)

        self.uploadButton = QtWidgets.QPushButton("Upload")
        self.uploadButton.setFixedWidth(100)
        self.uploadButton.setFixedHeight(50)
        self.uploadButton.clicked.connect(self.handleUpload)
        self.uploadButton.setEnabled(False)

        self.lateLabel = QtWidgets.QLabel("Specify late policy as days/%points deducted single-spaced list")
        self.lateLabel.setMaximumHeight(20)
        self.lateField = QtWidgets.QLineEdit()


        self.uploadContainer.addWidget(self.csvLabel,0,0)
        self.uploadContainer.addWidget(self.csvPathField,1,0)
        self.uploadContainer.setAlignment(self.csvPathField, QtCore.Qt.AlignTop)
        self.uploadContainer.addWidget(self.csvSelect,1,1)
        self.uploadContainer.setAlignment(self.csvSelect, QtCore.Qt.AlignTop)
        self.uploadContainer.addWidget(self.uploadButton,3,1)
        self.uploadContainer.setAlignment(self.uploadButton, QtCore.Qt.AlignTop)
        self.uploadContainer.addWidget(self.lateLabel,3,0)
        self.uploadContainer.addWidget(self.lateField,3,0)
        self.uploadContainer.setAlignment(self.lateLabel, QtCore.Qt.AlignTop)
        self.uploadContainer.setAlignment(self.lateField, QtCore.Qt.AlignBottom)
        # self.uploadContainer.setContentsMargins(10, 10, 10, 20)

        #self.layout is the reference to the layout manager that WE control, not the .layout() that returns the layout
        #   manager tracked by QT
        self.layout.setAlignment(self.uploadContainer, QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        self.layout.addLayout(self.uploadContainer)



    def onSelect(self):
        #called in the handleSelect method of the parent, we need to invoke approveUpload()
        self.approveUpload()



    def approveUpload(self):
        if self.fileReady and self.assignmentReady:
            self.uploadButton.setEnabled(True)
        else:
            self.uploadButton.setEnabled(False)



    def uploadFilePicker(self):
        dialog = QtWidgets.QFileDialog(self)
        dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        dialog.setWindowTitle("Select File to Upload")
        dialog.setNameFilter("CSV (*.csv)")

        if dialog.exec_():
            self.uploadPath = dialog.selectedFiles()[0]
            self.csvPathField.setText(self.uploadPath)
            self.fileReady = True
        self.approveUpload()
   


    def handleUpload(self):
        #this method uses the canvasWrapper attributes of the parent class
        try:
            self.late_policy = list(map(float, self.lateField.text().split()))
            self.canvasWrapper.push_grades(self.currentCourse, self.currentAssignment, self.uploadPath, self.late_policy)
            success_dialog = QtWidgets.QMessageBox()
            success_dialog.setText('Grades successfully uploaded!')
            success_dialog.setWindowTitle('Success!')
            success_dialog.exec_()
        except ValueError:
            print("-=- Invalid late policy (check for non-space, non-float values). Please input again.-=-")
            late_dialog = QtWidgets.QMessageBox()
            late_dialog.setText('Check for non-space, non-float values in the late policy input box.')
            late_dialog.setWindowTitle('Invalid late policy!')
            late_dialog.exec_()
