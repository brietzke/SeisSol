##
# @file
# This file is part of SeisSol.
#
# @author Carsten Uphoff (c.uphoff AT tum.de, http://www5.in.tum.de/wiki/index.php/Carsten_Uphoff,_M.Sc.)
#
# @section LICENSE
# Copyright (c) 2015, SeisSol Group
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from this
#    software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# @section DESCRIPTION
#

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import os
import scipy.signal
import copy

import Tecplot
import Waveform

class Navigation(QWidget):
  activeItemChanged = pyqtSignal(name='activeItemChanged')

  def __init__(self, parent = None):
    super(Navigation, self).__init__(parent)
    
    self.currentFolder = ''

    openIcon = QIcon.fromTheme('folder-open')
    openButton = QPushButton(openIcon, '', self)
    openButton.clicked.connect(self.selectFolder)
    refreshIcon = QIcon.fromTheme('view-refresh')
    refreshButton = QPushButton(refreshIcon, '', self)
    refreshButton.clicked.connect(self.refreshFolder)
    
    self.receiverList = QListView(self)
    self.model = QStandardItemModel()
    self.receiverList.setModel(self.model)
    self.receiverList.clicked.connect(self.activeItemChanged)
    
    buttonLayout = QHBoxLayout()
    buttonLayout.addWidget(openButton)
    buttonLayout.addWidget(refreshButton)
    buttonLayout.addStretch()
    
    enableLowpassLabel = QLabel('Lowpass', self)
    self.enableLowpass = QCheckBox(self)
    self.enableLowpass.stateChanged.connect(self.activeItemChanged)
    lowpassOrderLabel = QLabel('Order', self)
    self.lowpassOrder = QSpinBox(self)
    self.lowpassOrder.setValue(8)
    self.lowpassOrder.valueChanged.connect(self.activeItemChanged)
    attenuationLabel = QLabel('Attenuation (dB)', self)
    self.attenuation = QDoubleSpinBox(self)
    self.attenuation.setValue(40.0)
    self.attenuation.valueChanged.connect(self.activeItemChanged)
    cutoffLabel = QLabel('Cutoff (Hz)', self)
    self.cutoff = QDoubleSpinBox(self)
    self.cutoff.setValue(3.0)
    self.cutoff.valueChanged.connect(self.activeItemChanged)

    filterLayout = QFormLayout()
    filterLayout.addRow(enableLowpassLabel, self.enableLowpass)
    filterLayout.addRow(lowpassOrderLabel, self.lowpassOrder)
    filterLayout.addRow(attenuationLabel, self.attenuation)
    filterLayout.addRow(cutoffLabel, self.cutoff)

    layout = QVBoxLayout(self)
    layout.addLayout(buttonLayout)
    layout.addWidget(self.receiverList)
    layout.addLayout(filterLayout)

  def selectFolder(self):
    folder = QFileDialog.getExistingDirectory(self, 'Open directory', self.currentFolder, QFileDialog.ShowDirsOnly)
    if not folder.isEmpty():
      self.currentFolder = str(folder)
      self.readFolder(self.currentFolder)
      
  def readFolder(self, folder):
    if len(folder) != 0:
      self.model.clear()
      files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder,f))]
      files.sort()
      for f in files:
        wf = Tecplot.read(os.path.join(folder,f))
        item = QStandardItem(f)
        item.setData(wf)
        self.model.appendRow(item)
    
  def getActiveWaveforms(self):      
    waveforms = []
    for index in self.receiverList.selectedIndexes():
      wf = self.model.itemFromIndex(index).data().toPyObject()
      if self.enableLowpass.checkState() == Qt.Checked:
        wf = copy.deepcopy(wf)
        Fs = 1.0 / (wf.time[1] - wf.time[0])
        fc = self.cutoff.value() * 2.0 / Fs
        b, a = scipy.signal.cheby2(self.lowpassOrder.value(), self.attenuation.value(), fc)
        for name in wf.names:
          wf.waveforms[name] = scipy.signal.lfilter(b, a, wf.waveforms[name])
      waveforms.append(wf)
    return waveforms
    
  def refreshFolder(self):
    self.readFolder(self.currentFolder)
    self.activeItemChanged.emit()
    
  def lowpassChanged(self, status):
    self.activeItemChanged.emit()
      
    


