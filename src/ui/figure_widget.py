# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 11:07:37 2020

@author: vvyloi02
"""

from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
#from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT
from matplotlib.figure import Figure

#def add_logo(fig, color=None):
#    if color is None:
#        color = (0., 108./255, 177./255)
#    width = 6.
#    height = 4.21
#    thickness = 1.58
#    thickness_l = 1.24
#    thickness_r = 1.71
#    gap = 0.35
#    height_in = 2.64
#    
#    logo = [[0, 0],
#            [0.5*(width-thickness), height],
#            [0.5*(width+thickness), height],
#            [width, 0],
#            [width-thickness_r, 0],
#            [0.5*width, height_in], #(0.5*width-thickness_r)*height/(0.5*(width-thickness))
#            [0.5*width - (height_in-thickness_l)*(0.5*width-thickness_r)/height_in, thickness_l],
#            [width-thickness_r-gap-thickness_l*(0.5*width-thickness_r)/height_in, thickness_l],
#            [width-thickness_r-gap, 0],
#            [0, 0]]
#    ax = fig.add_axes([0.92, 0.92, 0.07, 0.07], zorder=100)
##    ax.set_aspect("equal")
#    ax.axis("off")
#    ax.fill([val[0] for val in logo],[val[1] for val in logo], color=color, linewidth=0)
#    return ax

class FigureWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(FigureWidget, self).__init__(parent)
        self.figure = Figure()
#        self.logo_ax = add_logo(self.figure)
        self.canvas = FigureCanvasQTAgg(self.figure)
#        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        
        layout = QtWidgets.QVBoxLayout()
#        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        
        