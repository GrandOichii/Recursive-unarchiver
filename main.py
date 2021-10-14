from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QLabel, QPushButton, QLineEdit, QProgressBar, QMessageBox

from os.path import exists

import sys

from unarchivers import is_rar_file, is_zip_file, unrar, unzip

class UnarchiveWorker(QThread):
    finished = pyqtSignal()

    def __init__(self, from_path, to_path):
        super(QThread, self).__init__()
        self.from_path = from_path
        self.to_path = to_path

    def run(self):
        if is_rar_file(self.from_path):
            try:
                unrar(self.from_path, self.to_path)
            except Exception as e:
                print(e)
                self.finished.emit()
                return

        if is_zip_file(self.from_path):
            try:
                unzip(self.from_path, self.to_path)
            except Exception as e:
                print(e)
                self.finished.emit()
                return
        self.finished.emit()


def window():
    app = QApplication([])
    win = UnarchiverWindow()
    win.show()
    sys.exit(app.exec_())

class UnarchiverWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.setGeometry(0, 0, 460, 300)
        self.setWindowTitle('Recursive unarchiver')
        self.initUI()
        self.show()

    def initUI(self):
        self.funnyFont = QFont('Comic Sans MS', 14)

        self.archive_path_label = QLabel(self)
        self.archive_path_label.setText('Path to archive:')
        self.archive_path_label.setFont(self.funnyFont)
        self.archive_path_label.setGeometry(10, 10, 400, 40)

        self.archive_path_line_edit = QLineEdit(self)
        self.archive_path_line_edit.setGeometry(10, 50, 400, 40)
        self.archive_path_line_edit.setFont(self.funnyFont)
        if len(sys.argv) == 3:
            self.archive_path_line_edit.setText(sys.argv[1])

        self.archive_path_button = QPushButton(self)
        self.archive_path_button.setText('...')
        self.archive_path_button.setFont(self.funnyFont)
        self.archive_path_button.setGeometry(415, 50, 40, 40)
        self.archive_path_button.clicked.connect(self.set_archive_path)

        self.destination_path_label = QLabel(self)
        self.destination_path_label.setText('Destination path:')
        self.destination_path_label.setFont(self.funnyFont)
        self.destination_path_label.setGeometry(10, 110, 400, 40)

        self.destination_path_line_edit = QLineEdit(self)
        self.destination_path_line_edit.setGeometry(10, 150, 400, 40)
        self.destination_path_line_edit.setFont(self.funnyFont)
        if len(sys.argv) == 3:
            self.destination_path_line_edit.setText(sys.argv[2])

        self.destination_path_button = QPushButton(self)
        self.destination_path_button.setText('...')
        self.destination_path_button.setFont(self.funnyFont)
        self.destination_path_button.setGeometry(415, 150, 40, 40)
        self.destination_path_button.clicked.connect(self.set_destination_path)

        self.unarchive_button = QPushButton(self)
        self.unarchive_button.setText('Unarchive')
        self.unarchive_button.setFont(self.funnyFont)
        self.unarchive_button.setGeometry((460 - 100) / 2, 220, 100, 40)
        self.unarchive_button.clicked.connect(self.begin_unarchiving)

    def showMB(self, text, title):
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def set_archive_path(self):
        fname = QFileDialog.getOpenFileName(self, 'Open archive file', '', "Archive files (*.zip *.rar)")
        self.archive_path_line_edit.setText(fname[0])

    def set_destination_path(self):
        file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.destination_path_line_edit.setText(file)

    def begin_unarchiving(self):
        archive_path = self.archive_path_line_edit.text()

        if len(archive_path) == 0:
            self.showMB('Select the archive file path!', 'Error')
            return

        if not exists(archive_path):
            self.showMB('File ' + archive_path + " doesn't exist!", 'Error')
            return

        if len(self.destination_path_line_edit.text()) == 0:
            self.showMB('Select the destination folder path!', 'Error')
            return

        if not exists(self.destination_path_line_edit.text()):
            self.showMB('Folder ' + self.destination_path_line_edit.text() + " doesn't exist!", 'Error')
            return

        if not is_rar_file(archive_path) and not is_zip_file(archive_path):
            self.showMB('File ' + archive_path + ' is not an archive!', 'Error')
            return        

        # all good, proceeding to unarchiving
        self.thread = QThread()
        self.worker = UnarchiveWorker(self.archive_path_line_edit.text(), self.destination_path_line_edit.text())
        self.worker.moveToThread(self.thread)
        
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)

        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        

        self.set_enabled_elements(False)
        self.thread.start()

        
        self.thread.finished.connect(lambda: print('done!'))
        self.thread.finished.connect(lambda: self.set_enabled_elements(True))
        self.thread.finished.connect(lambda: self.showMB("Done!", "Recursive unarchiver"))

             

    def set_enabled_elements(self, value):
        self.archive_path_button.setEnabled(value)
        self.archive_path_line_edit.setEnabled(value)
        self.destination_path_button.setEnabled(value)
        self.destination_path_line_edit.setEnabled(value)
        self.unarchive_button.setEnabled(value)
        
window()
