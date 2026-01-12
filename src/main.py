#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Line Trim - Python app dedicated to trimming of paraglider line length
"""

from PyQt5 import QtGui, QtWidgets, QtMultimedia
from ui.line_trim_ui import Ui_LineTrim
import os, pickle, sys, time

from ui.figure_widget import FigureWidget
import numpy as np

import matplotlib
import matplotlib.pyplot as plt

version_number = "0.1"
root = os.path.sep.join(os.path.abspath(__file__).split(os.path.sep)[:-2])

# Maximum allowed difference to consider the measurement valid
valid_difference = 800.

# Colorbar definition
tolerance = 24.
cmap = plt.cm.get_cmap('jet')
dev_style = lambda x : dict(ec=cmap((x+tolerance)/(2*tolerance))[:3], fc=cmap((x+tolerance)/(2*tolerance))[:3], pad=2)

# Style of the value on figure
th_style = dict(ec=(0., 0., 0.), fc=(0.9, 0.9, 0.9), pad=3)
meas_style = dict(ec=(1.,1.,1.), fc=(1.,1.,1.), pad=2)
active_style = dict(facecolor='tomato', pad = 2)

# Sides of the wing
side_list = ["Left", "Right"]
side_icon_list = ["toggle-left.png", "toggle-right.png"]

# Evolution mode
evo_list = [("Center to tip", (0, 1)),
            ("Tip to center", (0, -1)),
            ("Leading to trailing edge", (1, 0)),
            ("Trailing  to leading edge", (-1, 0)),]
evo_icon_list = ["maximize-2.png", "minimize-2.png", "arrow-up-left.png", "arrow-down-right.png"]
evo_dict = dict()
for name, val in evo_list: evo_dict[name] = val
min_val_back = 1000.    # Value considered as cancellation


# Graph dimensions
w, h = 1600, 900
w_margin = 0.01*w
h_margin = 0.01*h

# Sound settings
sound_dict = {True:"Turn sound off", False:"Turn sound on"}

class LineTrim(Ui_LineTrim):
    def __init__(self, main_window, version_number):
        super(Ui_LineTrim, self).__init__()
        self.version_number = version_number
        self.main_window = main_window
        self.project_filename = None

        self.setupUi(main_window)
        self.lineEdit_Identification.setText("Glider name, size, serial number")
        
        self.line_length = dict()
        self.row_size = list()
        self.row_names = list()
        self.offset = 0.
        self.active = ""
        self.cancel_last = False
        self.sound = False
        
        # Initialize sounds
        self.go_next = QtMultimedia.QSound(os.path.join(root, "resources", "sounds", "go_next.wav"))
        self.wrong = QtMultimedia.QSound(os.path.join(root, "resources", "sounds", "wrong.wav"))
        self.go_back = QtMultimedia.QSound(os.path.join(root, "resources", "sounds", "go_back.wav"))
        
        self.switchSound()
        
        self.measured_line_length = dict()
        self.profile = np.loadtxt(os.path.join(root, "resources", "profiles", "Profile.txt")) 
        
        self.main_window.setWindowTitle("Line Trim - version %s"%self.version_number) 
        self.main_window.setWindowIcon(QtGui.QIcon(os.path.join(root, "resources", "images", "feather.png")))
        
        self.figure_widget = FigureWidget(self.widget)
        self.widgetLayout = QtWidgets.QHBoxLayout(self.widget)
        self.widgetLayout.addWidget(self.figure_widget)
        self.figure_widget.figure.clf()
        self.ax = self.figure_widget.figure.add_axes((0.0,0.0,1.,1.), frameon=False)
        self.ax.get_xaxis().set_visible(False)
        self.ax.get_yaxis().set_visible(False)

        self.comboBox_Row.addItems(["-",])
        self.comboBox_Number.addItems(["-",])
        
        self.setLineLength()

        self.comboBox_Side.addItems(side_list)
        for i, filename in enumerate(side_icon_list):
            self.comboBox_Side.setItemIcon(i, QtGui.QIcon(os.path.join(root, "resources", "images", filename)))
        self.comboBox_Direction.addItems([evo[0] for evo in evo_list])
        for i, filename in enumerate(evo_icon_list):
            self.comboBox_Direction.setItemIcon(i, QtGui.QIcon(os.path.join(root, "resources", "images", filename)))


        self.updateView()
        
        self.actionLoad_project.triggered.connect(self.openProject)
        self.actionLoad_project.setIcon(QtGui.QIcon(os.path.join(root, "img", "file.png")))
        self.actionLoad_line_length.triggered.connect(self.setLineLength)
        self.actionLoad_line_length.setIcon(QtGui.QIcon(os.path.join(root, "resources", "images", "database.png")))
        self.actionSaveAs_project.triggered.connect(self.saveProjectAs)
        self.actionSaveAs_project.setIcon(QtGui.QIcon(os.path.join(root, "resources", "images", "save.png")))
        self.actionSave_project.triggered.connect(self.saveProject)
        self.actionSave_project.setIcon(QtGui.QIcon(os.path.join(root, "resources", "images", "save.png")))
        self.actionExportPDFReport.triggered.connect(self.exportPDFReport)
        self.actionExportPDFReport.setIcon(QtGui.QIcon(os.path.join(root, "resources", "images", "camera.png")))
        self.actionSound.triggered.connect(self.switchSound)

        self.comboBox_Side.currentIndexChanged.connect(self.updateView)
        self.comboBox_Row.currentIndexChanged.connect(self.updateView)
        self.comboBox_Number.currentIndexChanged.connect(self.updateView)       

        self.lineEdit_Measurement.returnPressed.connect(self.updateMeasurement)
            
    def switchSound(self):
        self.sound = not self.sound
        self.actionSound.setText(sound_dict[self.sound])
        self.actionSound.setIcon(QtGui.QIcon(os.path.join(root, "resources", "images", {True:"bell-off.png", False:"bell.png"}[self.sound])))

        
    def saveProjectAs(self):
        prefered_filename = "%s-%s.ltf"%(time.strftime("%Y-%m-%d"), self.lineEdit_Identification.text().replace(" ", "_"))
        filename = str(QtWidgets.QFileDialog.getSaveFileName(self.main_window, "Save as", os.path.join(root, "projects", prefered_filename), filter="*.ltf")[0])
        if len(filename) > 0:
            self.project_filename = filename
            self.saveProject()
        else : 
            self.printStatus("Save as failed.")


    def saveProject(self):
        if self.project_filename is None:
            self.saveProjectAs()
        elif not self.project_filename is None:
            project = dict(line_length=self.line_length,
                           measured_line_length = self.measured_line_length,
                           row_size = self.row_size,
                           row_names = self.row_names,
                           identification = self.lineEdit_Identification.text())
            with open(self.project_filename, "wb") as f: pickle.dump(project, f)
        else:
            self.printStatus("You should save your project!")


    def openProject(self, **kwargs):
        if not "filename" in kwargs:
            filename = str(QtWidgets.QFileDialog.getOpenFileName(self.main_window, "Select a LTF project file", os.path.join(root, "projects"), filter="*.ltf")[0])
        else:
            filename = kwargs["filename"]
        if len(filename) > 0:
            self.project_filename = filename
        with open(self.project_filename, "rb") as f: project = pickle.load(f)
        
        self.line_length = project["line_length"]
        self.measured_line_length = project["measured_line_length"]
        self.row_size = project["row_size"]
        self.row_names = project["row_names"]
        self.lineEdit_Identification.setText(project["identification"])
        self.updateView()


    def printStatus(self, message, dt=None):
        if dt is None:
            self.statusbar.showMessage(message)
        else:
            self.statusbar.showMessage(message, dt)


    def setLineLength(self, **kwargs):
        if not "filename" in kwargs:
            filename = str(QtWidgets.QFileDialog.getOpenFileName(self.main_window, "Select a file with theoretical line length", os.path.join(root, "data", "gliders"), filter="*.txt")[0])
        else:
            filename = kwargs["filename"]
        if os.path.isfile(filename):
            self.line_length = dict()
            try:
                with open(filename, "r") as f: content = f.readlines()
                self.row_size = list()
                self.row_names = list()
                num = 0
                for line in content:
                    if line.startswith("*"):
                        if num > 0:
                            self.row_size.append(num)
                        row_name = line.lstrip("*").rstrip("\n")
                        self.row_names.append(row_name)
                        num = 0
                    elif len(line.rstrip("\n")) > 0:
                        num += 1
                        key = "%s%02i"%(row_name.replace(" ","_"), num)
                        self.line_length[key] = float(line.lstrip("\n"))
                        for side in side_list:
                            self.measured_line_length["%s_%s"%(key, side)] = 0. # +np.random.normal(self.line_length[key], 5)
                    self.row_size.append(num)
                if self.project_filename is None:
                    default_filename = "%s_%s.ltf"%(time.strftime("%Y-%m-%d"), filename.split("/")[-1][:-4])
                    self.project_filename = os.path.join(root, "projects", "autosave", default_filename)
                    self.lineEdit_Identification.setText("%s - Serial number..."%filename.split("/")[-1][:-4].replace("_", " "))
            except:
                self.printStatus("The file '%s' is not readable"%filename)
        else:
            self.printStatus("The file '%s' is not recognized"%filename)
        self.comboBox_Row.clear()
        self.comboBox_Row.addItems(self.row_names)
        self.comboBox_Number.clear()
        if len(self.row_size) > 0:
            self.comboBox_Number.addItems([str(i+1) for i in range(max(self.row_size))])
        self.updateView()


    def computeDeviation(self):
        self.deviation_line_length = dict()
        total = 0.
        n_dev = 0
        for key in self.line_length:
            for side in side_list:
                skey = "%s_%s"%(key, side)
                if not self.measured_line_length[skey] == 0:
                    self.deviation_line_length[skey] = self.measured_line_length[skey] - self.line_length[key]
                    total += self.deviation_line_length[skey]
                    n_dev += 1
        if n_dev > 0:
            self.offset = total / n_dev
            for key in self.deviation_line_length:
                self.deviation_line_length[key] -= self.offset


    def exportPDFReport(self):
        prefered_filename = "%s-%s.pdf"%(time.strftime("%Y-%m-%d"), self.lineEdit_Identification.text().replace(" ", "_"))
        filename = str(QtWidgets.QFileDialog.getSaveFileName(self.main_window, "Export PDF report as.", os.path.join(root, "reports", prefered_filename), filter="*.pdf")[0])
        if len(filename) > 0:
            if not filename.endswith(".pdf"): filename += ".pdf"
            matplotlib.rc('font', **{'size'   : 7})
            fig = plt.figure(figsize=(297./25.4, 210./25.4))
            ax = fig.add_subplot(1,1,1, frameon=False)
            ax.get_xaxis().set_visible(False)
            ax.get_yaxis().set_visible(False)
            self.updateView(ax = ax)
            fig.subplots_adjust(left=10./297, right=287./297, bottom=10./210, top=200./210 )
            fig.savefig(filename)
            plt.close(fig=fig)
            matplotlib.rc('font', **{'size'   : 10})
        self.printStatus("Report %s generated."%filename)
    
    
    def updateView(self, **kwargs):
        if "ax" in kwargs:
            ax = kwargs["ax"]
            display_active = False
        else:
            ax = self.ax
            display_active = True
            self.computeDeviation()
            self.saveProject()
        try:
            number = int(self.comboBox_Number.currentText())
        except:
            number = 0
        self.active = "%s%02i_%s"%(self.comboBox_Row.currentText(), number, self.comboBox_Side.currentText(), )

        ax.cla()
        ax.set_xlim(0,w)
        ax.set_ylim(0,h)

        # Plot background glider
        ax.fill_between(self.profile[:,0], self.profile[:,1], self.profile[:,2], color=(0.95,0.95,0.95,))
        ax.plot(self.profile[:,0], self.profile[:,1:], color="k", linewidth=1.)
        for i in range(0, self.profile.shape[0]):
            ax.plot([self.profile[i,0], self.profile[i,0]], [self.profile[i,1], self.profile[i,2]], color="k", linewidth={True:0.25, False:1.}[0<i<self.profile.shape[0]-1])

        ax.text(w_margin, h_margin, "%s leading edge"%side_list[0], ha="left", va="bottom", fontsize="large", fontweight="bold", bbox=meas_style)
        ax.text(w-w_margin, h_margin, "%s leading edge"%side_list[1], ha="right", va="bottom", fontsize="large", fontweight="bold", bbox=meas_style)

        ax.text(w_margin, h-h_margin, "%s trailing edge"%side_list[0], ha="left", va="top", fontsize="large", fontweight="bold", bbox=meas_style)
        ax.text(w-w_margin, h-h_margin, "%s trailing edge"%side_list[1], ha="right", va="top", fontsize="large", fontweight="bold", bbox=meas_style)


        ax.text(w/2, h-h_margin, "%s - %s"%(time.strftime("%d-%m-%Y"), self.lineEdit_Identification.text()), ha="center", va="top", fontsize="x-large", fontweight="bold", bbox=meas_style)


        ax.plot([w/2, w/2], [0., h], linestyle="--", color="k", linewidth=2.)
        if len(self.row_size) > 0: n = max(self.row_size)
        else: n = 2
        w_eff = 0.5*w-w_margin
        h_step = w_eff*1./(n)
        h_eff = h-2*h_margin
        v_step = h_eff*1./ (len(self.row_names)+1)
        v_space = 0.15*v_step
        for i, row_name in enumerate(self.row_names):
            for j in range(1, n+1):
                key = "%s%02i"%(row_name, j)
                if key in self.line_length:
                    x = {side_list[0]:0.5*w - (j-0.3)*h_step, side_list[1]:0.5*w + (j-0.3)*h_step}
                    y = h_margin+(i+1)*v_step
                    th_length = self.line_length[key]
                    for side in side_list:
                        skey = "%s_%s"%(key, side)
                        active = display_active and self.active==skey
                        if active:
                            ax.plot([0, w], [y, y], linestyle ="--", linewidth=2, color="tomato")
                            ax.plot([x[side], x[side]], [0, h], linestyle ="--", linewidth=2, color="tomato")
                            bbox_style = active_style
                        else:
                            bbox_style = meas_style
                        measured = self.measured_line_length[skey]
                        ax.text(x[side], y+v_space, "%s-%s\n%i"%(key, side[0], th_length), ha="center", va="bottom", fontsize="small", fontstyle="italic", bbox=th_style)
                        if not measured==0:
                            deviation = self.deviation_line_length[skey]
                            ax.text(x[side], y, "%i"%measured, ha="center", va="center", bbox=bbox_style)
                            ax.text(x[side], y-v_space, "%s=%i"%(r"$\Delta$", deviation), ha="center", va="top", fontweight="bold", bbox=dev_style(deviation))
                        elif active:
                            ax.text(x[side], y, "--", ha="center", va="center", bbox=bbox_style)

        ax.text(w/2, h_margin, "Offset = %0.1f mm"%self.offset, ha="center", va="bottom", bbox=meas_style)
        
        self.figure_widget.figure.canvas.draw_idle()


    def updateMeasurement(self):
        evo_row, evo_number = evo_dict[self.comboBox_Direction.currentText()]
        try:
            val = float(self.lineEdit_Measurement.text()) 
            if val< 10:
                val *= 1e3
        except:
            val = -1.

        if 0. < val < min_val_back and self.cancel_last:
            self.comboBox_Row.setCurrentIndex(self.comboBox_Row.currentIndex()-evo_row)
            self.comboBox_Number.setCurrentIndex(self.comboBox_Number.currentIndex()-evo_number)
            if self.sound: self.go_back.play()
            self.cancel_last = False
        elif 0. < val < min_val_back:
            self.cancel_last = True
            if self.sound: self.wrong.play()

        if self.active in self.measured_line_length:
            # Get the theoretical length
            for side in side_list:
                if self.active.endswith("_%s"%side) : ref = self.line_length[self.active[:-(len(side)+1)]]
            if np.abs(val-ref) < valid_difference:
                # Assign value
                self.measured_line_length[self.active] = val
                # Move to next point
                self.comboBox_Row.setCurrentIndex(self.comboBox_Row.currentIndex()+evo_row)
                self.comboBox_Number.setCurrentIndex(self.comboBox_Number.currentIndex()+evo_number)
                if self.sound: self.go_next.play()

        self.lineEdit_Measurement.setText("")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mw = QtWidgets.QMainWindow()
    lt = LineTrim(mw, version_number)
    mw.showMaximized()    
#    lt.lineEdit_Identification.setText("Supair Savage S SA-SAV-S-2007-145")
#    lt.setLineLength(ask_for_filename = False, filename = "Savage/LineLength_Savage_S.txt")
#    sys.exit()   
    app.exec_()
