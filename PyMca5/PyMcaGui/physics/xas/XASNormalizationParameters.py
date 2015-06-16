#/*##########################################################################
#
# The PyMca X-Ray Fluorescence Toolkit
#
# Copyright (c) 2004-2015 European Synchrotron Radiation Facility
#
# This file is part of the PyMca X-ray Fluorescence Toolkit developed at
# the ESRF by the Software group.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
#############################################################################*/
__author__ = "V. Armando Sole - ESRF Data Analysis"
__contact__ = "sole@esrf.fr"
__license__ = "MIT"
__copyright__ = "European Synchrotron Radiation Facility, Grenoble, France"
from PyMca5.PyMcaGui import PyMcaQt as qt
from PyMca5.PyMcaGui import PyMca_Icons
from PyMca5.PyMcaGui import XASNormalizationWindow
IconDict = PyMca_Icons.IconDict

class NormalizationParameters(qt.QGroupBox):
    sigNormalizationParametersSignal = qt.pyqtSignal(object)
    def __init__(self, parent=None):
        super(NormalizationParameters, self).__init__(parent)
        self.setTitle("Normalization")
        self._dialog = None
        self._energy = None
        self._mu = None
        self.build()

    def build(self):
        self.mainLayout = qt.QGridLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(2)

        # the setup button
        self.setupButton = qt.QPushButton(self)
        self.setupButton.setText("SETUP")
        self.setupButton.setAutoDefault(False)

        # the E0 value
        self.e0CheckBox = qt.QCheckBox(self)
        self.e0CheckBox.setText("Auto E0:")
        self.e0CheckBox.setChecked(True)
        self.e0SpinBox = qt.QDoubleSpinBox(self)
        self.e0SpinBox.setDecimals(2)
        self.e0SpinBox.setSingleStep(0.2)
        self.e0SpinBox.setEnabled(False)

        # the jump
        jumpLabel = qt.QLabel(self)
        jumpLabel.setText("Jump:")
        self.jumpLine = qt.QLineEdit(self)
        self.jumpLine.setEnabled(False)

        # the pre-edge
        preEdgeLabel = qt.QLabel(self)
        preEdgeLabel.setText("Pre-Edge")
        self.preEdgeSelector = XASNormalizationWindow.PolynomSelector(self)

        # pre-edge regions
        preEdgeStartLabel = qt.QLabel(self)
        preEdgeStartLabel.setText("Begin:")
        self.preEdgeStartBox = qt.QDoubleSpinBox(self)
        self.preEdgeStartBox.setDecimals(2)
        self.preEdgeStartBox.setMinimum(-2000.0)
        self.preEdgeStartBox.setMaximum(-5.0)
        self.preEdgeStartBox.setValue(-100)
        self.preEdgeStartBox.setSingleStep(5.0)
        self.preEdgeStartBox.setEnabled(True)

        preEdgeEndLabel = qt.QLabel(self)
        preEdgeEndLabel.setText("End:")
        self.preEdgeEndBox = qt.QDoubleSpinBox(self)
        self.preEdgeEndBox.setDecimals(2)
        self.preEdgeEndBox.setMinimum(-200.0)
        self.preEdgeEndBox.setMaximum(-1.0)
        self.preEdgeEndBox.setValue(-40)
        self.preEdgeEndBox.setSingleStep(5.0)
        self.preEdgeEndBox.setEnabled(True)

        # the post-edge
        postEdgeLabel = qt.QLabel(self)
        postEdgeLabel.setText("Post-Edge")
        self.postEdgeSelector = XASNormalizationWindow.PolynomSelector(self)

        # post-edge regions
        postEdgeStartLabel = qt.QLabel(self)
        postEdgeStartLabel.setText("Begin:")
        self.postEdgeStartBox = qt.QDoubleSpinBox(self)
        self.postEdgeStartBox.setDecimals(2)
        self.postEdgeStartBox.setMinimum(1.0)
        self.postEdgeStartBox.setMaximum(3000.0)
        self.postEdgeStartBox.setValue(10)
        self.postEdgeStartBox.setSingleStep(5.0)
        self.postEdgeStartBox.setEnabled(True)

        postEdgeEndLabel = qt.QLabel(self)
        postEdgeEndLabel.setText("End:")
        self.postEdgeEndBox = qt.QDoubleSpinBox(self)
        self.postEdgeEndBox.setDecimals(2)
        self.postEdgeEndBox.setMinimum(10.0)
        self.postEdgeEndBox.setMaximum(2000.0)
        self.postEdgeEndBox.setValue(300)
        self.postEdgeEndBox.setSingleStep(5.0)
        self.postEdgeEndBox.setEnabled(True)

        # arrange everything
        self.mainLayout.addWidget(self.setupButton, 0, 0, 1, 2)
        self.mainLayout.addWidget(self.e0CheckBox, 1, 0)
        self.mainLayout.addWidget(self.e0SpinBox, 1, 1)
        self.mainLayout.addWidget(jumpLabel, 2, 0)
        self.mainLayout.addWidget(self.jumpLine, 2, 1)

        self.mainLayout.addWidget(preEdgeLabel, 3, 0)
        self.mainLayout.addWidget(self.preEdgeSelector, 3, 1)
        self.mainLayout.addWidget(preEdgeStartLabel, 4, 0)
        self.mainLayout.addWidget(self.preEdgeStartBox, 4, 1)
        self.mainLayout.addWidget(preEdgeEndLabel, 5, 0)
        self.mainLayout.addWidget(self.preEdgeEndBox, 5, 1)

        self.mainLayout.addWidget(postEdgeLabel, 6, 0)
        self.mainLayout.addWidget(self.postEdgeSelector, 6, 1)
        self.mainLayout.addWidget(postEdgeStartLabel, 7, 0)
        self.mainLayout.addWidget(self.postEdgeStartBox, 7, 1)
        self.mainLayout.addWidget(postEdgeEndLabel, 8, 0)
        self.mainLayout.addWidget(self.postEdgeEndBox, 8, 1)

        # connect
        self.setupButton.clicked.connect(self._setupClicked)
        self.e0CheckBox.toggled.connect(self._e0Toggled)
        self.e0SpinBox.valueChanged[float].connect(self._e0Changed)
        self.preEdgeSelector.activated[int].connect(self._preEdgeChanged)
        self.preEdgeStartBox.valueChanged[float].connect(self._preEdgeStartChanged)
        self.preEdgeEndBox.valueChanged[float].connect(self._preEdgeEndChanged)
        self.postEdgeSelector.activated[int].connect(self._postEdgeChanged)
        self.postEdgeStartBox.valueChanged[float].connect(self._postEdgeStartChanged)
        self.postEdgeEndBox.valueChanged[float].connect(self._postEdgeEndChanged)

    def _setupClicked(self):
        if self._energy is None:
            print("SETUP CLICKED BUT IGNORED")
            return
        if self._dialog is None:
            self._dialog = XASNormalizationWindow.XASNormalizationDialog(self,
                                                                         mu,
                                                                         energy=energy)
        else:
            self._dialog.setSpectrum(energy, mu)
        print("RECOVER CURRENT PARAMETERS AND UPDATE DIALOG")
        ret = self._dialog.exec_()
        if ret:
            print("RECOVER PARAMETERS FROM DIALOG AND UPDATE")

    def setSpectrum(self, energy, mu):
        self._energy = energy
        self._mu = mu
        self._update()

    def _e0Toggled(self, state):
        print("CURRENT STATE = ", state)
        print("STATE from call = ", self.e0CheckBox.isChecked())
        if state:
            print("E0 to be calculated")
            self.e0SpinBox.setEnabled(False)
        else:
            self.e0SpinBox.setEnabled(True)

    def _e0Changed(self, value):
        pars = self._dialog.getParameters()
        if self._dialog is None:
            print

    def _preEdgeChanged(self, value):
        print("Current pre-edge value = ", value)

    def _preEdgeStartChanged(self, value):
        print("pre start changed", value)

    def _preEdgeEndChanged(self, value):
        print("pre end changed", value)

    def _postEdgeChanged(self, value):
        print("Current post-edge value = ", value)

    def _postEdgeStartChanged(self, value):
        print("post start changed", value)

    def _postEdgeEndChanged(self, value):
        print("post end changed", value)

    def _update(self):
        print("THIS IS TO UPDATE E0 IF AUTO")
        print("UPDATE REGION LIMITS ON CHANGE")

    def getParameters(self):
        print("GET PARAMETERS")

    def setParameters(self, ddict):
        print("SET PARAMETERS")
            
if __name__ == "__main__":
    app = qt.QApplication([])
    w = NormalizationParameters()
    w.show()
    app.exec_()