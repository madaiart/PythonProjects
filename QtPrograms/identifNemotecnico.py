# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 17:14:50 2019

@author: juana hernández
"""

from ui_IdentifNemotecnico import *


def get_voltage(voltage):
    if voltage == "0 V":
        return "E"
    elif voltage == "120 V – 121 V – 127 V":
        return "C"
    elif voltage == "240/120 V – 220/127 V":
        return "D"
    elif voltage == "6,3 kV":
        return "S"
    elif voltage == "13,8 kV GRDy / 7,96 kV – 13,2 kV GRDy / 7,62 kV":
        return "T"
    elif voltage == "22 kV GRDy / 12,7 kV - 22,8 kV GRDy / 13,2 kV":
        return "V"


def get_tipo_seccionamiento(tipo):
    if tipo == 0:
        return "C"
    elif tipo == 1:
        return "T"
    elif tipo == 2:
        return "P"
    elif tipo == 3:
        return "B"
    elif tipo == 4:
        return "F"
    elif tipo == 5:
        return "D"
    elif tipo == 6:
        return "I"
    elif tipo == 7:
        return "E"
    elif tipo == 8:
        return "N"


def get_tipo_transformacion(tipo):
    if tipo == 0:
        return "M"
    elif tipo == 1:
        return "S"
    elif tipo == 2:
        return "D"
    elif tipo == 3:
        return "P"
    elif tipo == 4:
        return "V"
    elif tipo == 5:
        return "I"


def get_nivel_piso(alto, largo, ancho):
    l = float(largo)
    a = float(alto)
    p = float(ancho)

    if l <= 3 and a <= 4 and p >= 2.5:
        return "A"
    elif 3 < l <= 6 and 4 < a <= 7 and p >= 2.5:
        return "B"
    elif l > 6 and a > 7 and p >= 2.5:
        return "C"


def get_tabla_pozo(alto, largo, ancho):
    l = float(largo)
    a = float(alto)
    p = float(ancho)

    if l == 0.9 and a == 0.9 and p == 0.9:
        return "A"
    elif l == 1.20 and a == 1.20 and p == 1.20:
        return "B"
    elif l == 0.6 and a == 0.6 and p == 0.75:
        return "C"
    elif l == 1.6 and a == 1.2 and p == 1.5:
        return "D"
    elif l == 2.5 and a == 2.0 and p == 2.0:
        return "E"

    elif l <= 0.4 and a <= 0.4 and p < 0.6:
        return "X"
    elif 0.9 < l <= 0.8 and 0.4 < a <= 0.8 and p <= 1.0:
        return "Y"
    elif l > 0.8 and a > 0.8 and p > 1.0:
        return "Z"


class MainWindow(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, *args, **kwargs):
        QtWidgets.QDialog.__init__(self, *args, **kwargs)
        self.setupUi(self)

        # Adding functionality to buttons
        self.btn_generar.clicked.connect(self.btn_generar_fun)
        self.btn_limpiar.clicked.connect(self.btn_limpiar_fun)

        self.ss_cb_tipoSeccionamiento.currentIndexChanged.connect(self.ss_item_selected)
        self.tu_cb_tipoTransformacion.currentIndexChanged.connect(self.tu_item_selected)
        self.tu_btn_calcular.clicked.connect(self.tu_btn_calcular_fun)

        self.eu_rb_subterraneo.toggled.connect(lambda: self.eu_radios(self.eu_rb_subterraneo))
        self.eu_rb_nivelPiso.toggled.connect(lambda: self.eu_radios(self.eu_rb_nivelPiso))

    def btn_generar_fun(self):
        if self.tabIdentificadorNemotecnico.currentIndex() == 1:
            self.txt_Codigo.setText("EU" + self.estructuras())
        elif self.tabIdentificadorNemotecnico.currentIndex() == 2:
            self.txt_Codigo.setText("TU" + self.transformadores())
        elif self.tabIdentificadorNemotecnico.currentIndex() == 3:
            self.txt_Codigo.setText("SS" + self.seccionamiento())
        elif self.tabIdentificadorNemotecnico.currentIndex() == 4:
            self.txt_Codigo.setText("TS" + self.transicion())
        elif self.tabIdentificadorNemotecnico.currentIndex() == 5:
            self.txt_Codigo.setText("TD" + self.tableros())

    def estructuras(self):
        voltage = get_voltage(self.eu_cb_voltaje.currentText())

        fases = "0"

        if self.tabTiposEstructuras.currentIndex() == 0:  # Camara
            tipo = "C"
            camara_base = ""
            if self.eu_rb_subterraneo.isChecked():
                camara_base = "S"
                return voltage + "-" + fases + tipo + camara_base
            elif self.eu_rb_nivelPiso.isChecked():
                camara_base = "N"
                valor_nivel_piso = get_nivel_piso(self.eu_txt_piso_alto.text(), self.eu_txt_piso_largo.text(),
                                                  self.eu_txt_piso_ancho.text())
                return voltage + "-" + fases + tipo + camara_base + valor_nivel_piso

        elif self.tabTiposEstructuras.currentIndex() == 1:  # Zanja
            tipo = "Z"
            # TODO FALTA
            return voltage + "-" + fases + tipo + "()"

        elif self.tabTiposEstructuras.currentIndex() == 2:  # Pozo
            tipo = "P"
            valor_tabla_pozo = get_tabla_pozo(self.eu_txt_pozo_alto.text(), self.eu_txt_pozo_largo.text(),
                                              self.eu_txt_pozo_ancho.text())
            return voltage + "-" + fases + tipo + valor_tabla_pozo

    def transformadores(self):
        voltage = get_voltage(self.tu_cb_voltaje.currentText())

        fases = ""
        if self.tu_rb_fase1.isChecked():
            fases = "1"
        elif self.tu_rb_fase2.isChecked():
            fases = "2"
        elif self.tu_rb_fase3.isChecked():
            fases = "3"

        tipo_trans = get_tipo_transformacion(self.tu_cb_tipoTransformacion.currentIndex())

        if self.tu_txt_especificacionTecnica.isEnabled():
            capacidad = self.tu_txt_especificacionTecnica.text()
        else:
            capacidad = self.tu_txt_resultado.text()

        return voltage + "-" + fases + tipo_trans + capacidad

    def seccionamiento(self):
        voltage = get_voltage(self.ss_cb_voltaje.currentText())

        fases = ""
        if self.ss_rb_fases1.isChecked():
            fases = "1"
        elif self.ss_rb_fases2.isChecked():
            fases = "2"
        elif self.ss_rb_fases3.isChecked():
            fases = "3"

        tipo_secc = get_tipo_seccionamiento(self.ss_cb_tipoSeccionamiento.currentIndex())

        if tipo_secc == "C" or tipo_secc == "T" or tipo_secc == "P":
            # Get values
            capacidad_corriente = self.ss_txt_capacidadCorriente.text()
            bil = self.ss_txt_bil.text()
            return voltage + "-" + fases + tipo_secc + capacidad_corriente + "_" + bil

        elif tipo_secc == "B" or tipo_secc == "I":
            # Get values
            numero_vias = self.ss_txt_numeroVias.text()
            capacidad_corriente = self.ss_txt_capacidadCorriente.text()
            bil = self.ss_txt_bil.text()
            return voltage + "-" + fases + tipo_secc + numero_vias + "_" + capacidad_corriente + "_" + bil

        elif tipo_secc == "F" or tipo_secc == "N":
            capacidad_corriente = self.ss_txt_capacidadCorriente.text()
            return voltage + "-" + fases + tipo_secc + capacidad_corriente

        elif tipo_secc == "D":
            voltage_max = self.ss_txt_voltajeMaximo.text()
            bil = self.ss_txt_bil.text()
            return voltage + "-" + fases + tipo_secc + voltage_max + "_" + bil

        elif tipo_secc == "E":
            numero_vias = self.ss_txt_numeroVias.text()  # TODO is not used
            tipo_cel = ""
            if self.ss_rb_compacto.isChecked():
                tipo_cel = "C"
            elif self.ss_rb_modular.isChecked():
                tipo_cel = "M"
            capacidad_corriente = self.ss_txt_capacidadCorriente.text()
            bil = self.ss_txt_bil.text()
            return voltage + "-" + fases + tipo_secc + tipo_cel + capacidad_corriente + "_" + bil

    def transicion(self):
        voltage = get_voltage(self.ts_cb_voltaje.currentText())

        fases = ""
        if self.ts_rb_fase1.isChecked():
            fases = "1"
        elif self.ts_rb_fase2.isChecked():
            fases = "2"
        elif self.ts_rb_fase3.isChecked():
            fases = "3"

        dispocicion = ""
        if self.ts_rb_semicentrada.isChecked():
            dispocicion = "S"
        elif self.ts_rb_volado.isChecked():
            dispocicion = "V"

        bajo_voltaje = ""
        if self.ts_rb_redDesnuda.isChecked():
            bajo_voltaje = "D"
        elif self.ts_rb_redPreensablada.isChecked():
            bajo_voltaje = "P"
        elif self.ts_rb_bornesTransformador.isChecked():
            bajo_voltaje = "B"
        elif self.ts_rb_fusiblesNH.isChecked():
            bajo_voltaje = "F"

        ess_tec = "0"

        return voltage + "-" + fases + dispocicion + bajo_voltaje + ess_tec

    def tableros(self):
        voltage = get_voltage(self.td_cb_voltaje.currentText())

        fases = "0"

        dispocicion = ""
        if self.td_rb_exterior.isChecked():
            dispocicion = "E"
        elif self.td_rb_interior.isChecked():
            dispocicion = "I"

        # Especificacion Técnica
        c_nominal = self.td_txt_capacidadCorriente.text()
        n_circuitos = self.td_txt_numeroCircuito.text()

        return voltage + "-" + fases + dispocicion + c_nominal + "_" + n_circuitos

    def eu_radios(self, item):
        if item.text() == "Subterraneo":
            self.eu_txt_piso_ancho.setDisabled(True)
            self.eu_txt_piso_largo.setDisabled(True)
            self.eu_txt_piso_alto.setDisabled(True)
        elif item.text() == "Nivel de piso":
            self.eu_txt_piso_ancho.setDisabled(False)
            self.eu_txt_piso_largo.setDisabled(False)
            self.eu_txt_piso_alto.setDisabled(False)

    def tu_item_selected(self, item):
        if item == 4:
            self.tu_txt_cap3.setDisabled(True)
            self.tu_txt_cap2.setDisabled(False)
            self.tu_txt_cap1.setDisabled(False)
            # self.tu_txt_resultado.setDisabled(False)
            self.tu_btn_calcular.setDisabled(False)
            self.tu_txt_especificacionTecnica.setDisabled(True)
        elif item == 5:
            self.tu_txt_cap3.setDisabled(False)
            self.tu_txt_cap2.setDisabled(False)
            self.tu_txt_cap1.setDisabled(False)
            # self.tu_txt_resultado.setDisabled(False)
            self.tu_btn_calcular.setDisabled(False)
            self.tu_txt_especificacionTecnica.setDisabled(True)
        elif item == 0 or item == 1 or item == 2 or item == 3:
            self.tu_txt_cap3.setDisabled(True)
            self.tu_txt_cap2.setDisabled(True)
            self.tu_txt_cap1.setDisabled(True)
            # self.tu_txt_resultado.setDisabled(True)
            self.tu_btn_calcular.setDisabled(True)
            self.tu_txt_especificacionTecnica.setDisabled(False)

    def tu_btn_calcular_fun(self):
        if self.tu_txt_cap3.isEnabled():
            val3 = self.tu_txt_cap3.text()
            val2 = self.tu_txt_cap2.text()
            val1 = self.tu_txt_cap1.text()
            self.tu_txt_resultado.setText(str(int(val3) + int(val2) + int(val1)))
        else:
            val2 = self.tu_txt_cap2.text()
            val1 = self.tu_txt_cap1.text()
            self.tu_txt_resultado.setText(str(int(val2) + int(val1)))

    def ss_item_selected(self, item):
        if item == 0 or item == 1 or item == 2:
            self.ss_txt_capacidadCorriente.setDisabled(False)
            self.ss_txt_bil.setDisabled(False)
            self.ss_txt_numeroVias.setDisabled(True)
            self.ss_txt_voltajeMaximo.setDisabled(True)
            self.ss_rb_compacto.setDisabled(True)
            self.ss_rb_modular.setDisabled(True)

        elif item == 3 or item == 6:
            self.ss_txt_capacidadCorriente.setDisabled(False)
            self.ss_txt_bil.setDisabled(False)
            self.ss_txt_numeroVias.setDisabled(False)
            self.ss_txt_voltajeMaximo.setDisabled(True)
            self.ss_rb_compacto.setDisabled(True)
            self.ss_rb_modular.setDisabled(True)

        elif item == 4 or item == 8:
            self.ss_txt_capacidadCorriente.setDisabled(False)
            self.ss_txt_bil.setDisabled(True)
            self.ss_txt_numeroVias.setDisabled(True)
            self.ss_txt_voltajeMaximo.setDisabled(True)
            self.ss_rb_compacto.setDisabled(True)
            self.ss_rb_modular.setDisabled(True)

        elif item == 5:
            self.ss_txt_capacidadCorriente.setDisabled(True)
            self.ss_txt_bil.setDisabled(False)
            self.ss_txt_numeroVias.setDisabled(True)
            self.ss_txt_voltajeMaximo.setDisabled(False)
            self.ss_rb_compacto.setDisabled(True)
            self.ss_rb_modular.setDisabled(True)

        elif item == 7:
            self.ss_txt_capacidadCorriente.setDisabled(False)
            self.ss_txt_bil.setDisabled(False)
            self.ss_txt_numeroVias.setDisabled(False)
            self.ss_txt_voltajeMaximo.setDisabled(True)
            self.ss_rb_compacto.setDisabled(False)
            self.ss_rb_modular.setDisabled(False)

    def btn_limpiar_fun(self):
        # region Clear table
        self.eu_tbl_zanja.clear()
        self.eu_tbl_zanja.setHorizontalHeaderLabels(["Fila", "Columna", "Diametro del ducto [mm]"])
        self.eu_tbl_zanja.horizontalHeader().setStyleSheet("::section {""background-color: lightgray; }")
        self.eu_tbl_zanja.verticalHeader().setStyleSheet("::section {""background-color: lightgray; }")
        # endregion

        # region Clear text
        self.txt_Codigo.setText("")
        self.eu_txt_piso_largo.setText("")
        self.eu_txt_piso_ancho.setText("")
        self.eu_txt_piso_alto.setText("")
        self.eu_txt_pozo_largo.setText("")
        self.eu_txt_pozo_ancho.setText("")
        self.eu_txt_pozo_alto.setText("")
        self.tu_txt_especificacionTecnica.setText("")
        self.ss_txt_capacidadCorriente.setText("")
        self.ss_txt_bil.setText("")
        self.ss_txt_numeroVias.setText("")
        self.ss_txt_voltajeMaximo.setText("")
        self.td_txt_capacidadCorriente.setText("")
        self.td_txt_numeroCircuito.setText("")
        # endregion

        # region Clear combo box
        self.eu_cb_voltaje.setCurrentIndex(0)
        self.tu_cb_voltaje.setCurrentIndex(0)
        self.tu_cb_tipoTransformacion.setCurrentIndex(0)
        self.ss_cb_voltaje.setCurrentIndex(0)
        self.ss_cb_tipoSeccionamiento.setCurrentIndex(0)
        self.ts_cb_voltaje.setCurrentIndex(0)
        self.td_cb_voltaje.setCurrentIndex(0)
        # endregion

        # region Clear radio button
        self.eu_rb_subterraneo.setAutoExclusive(False)
        self.eu_rb_subterraneo.setChecked(False)
        self.eu_rb_subterraneo.setAutoExclusive(True)

        self.eu_rb_nivelPiso.setAutoExclusive(False)
        self.eu_rb_nivelPiso.setChecked(False)
        self.eu_rb_nivelPiso.setAutoExclusive(True)

        self.tu_rb_fase1.setAutoExclusive(False)
        self.tu_rb_fase1.setChecked(False)
        self.tu_rb_fase1.setAutoExclusive(True)

        self.tu_rb_fase2.setAutoExclusive(False)
        self.tu_rb_fase2.setChecked(False)
        self.tu_rb_fase2.setAutoExclusive(True)

        self.tu_rb_fase3.setAutoExclusive(False)
        self.tu_rb_fase3.setChecked(False)
        self.tu_rb_fase3.setAutoExclusive(True)

        self.ss_rb_fases1.setAutoExclusive(False)
        self.ss_rb_fases1.setChecked(False)
        self.ss_rb_fases1.setAutoExclusive(True)

        self.ss_rb_fases2.setAutoExclusive(False)
        self.ss_rb_fases2.setChecked(False)
        self.ss_rb_fases2.setAutoExclusive(True)

        self.ss_rb_fases3.setAutoExclusive(False)
        self.ss_rb_fases3.setChecked(False)
        self.ss_rb_fases3.setAutoExclusive(True)

        self.ss_rb_modular.setAutoExclusive(False)
        self.ss_rb_modular.setChecked(False)
        self.ss_rb_modular.setAutoExclusive(True)

        self.ss_rb_compacto.setAutoExclusive(False)
        self.ss_rb_compacto.setChecked(False)
        self.ss_rb_compacto.setAutoExclusive(True)

        self.ts_rb_fase1.setAutoExclusive(False)
        self.ts_rb_fase1.setChecked(False)
        self.ts_rb_fase1.setAutoExclusive(True)

        self.ts_rb_fase2.setAutoExclusive(False)
        self.ts_rb_fase2.setChecked(False)
        self.ts_rb_fase2.setAutoExclusive(True)

        self.ts_rb_fase3.setAutoExclusive(False)
        self.ts_rb_fase3.setChecked(False)
        self.ts_rb_fase3.setAutoExclusive(True)

        self.ts_rb_semicentrada.setAutoExclusive(False)
        self.ts_rb_semicentrada.setChecked(False)
        self.ts_rb_semicentrada.setAutoExclusive(True)

        self.ts_rb_volado.setAutoExclusive(False)
        self.ts_rb_volado.setChecked(False)
        self.ts_rb_volado.setAutoExclusive(True)

        self.ts_rb_redDesnuda.setAutoExclusive(False)
        self.ts_rb_redDesnuda.setChecked(False)
        self.ts_rb_redDesnuda.setAutoExclusive(True)

        self.ts_rb_redPreensablada.setAutoExclusive(False)
        self.ts_rb_redPreensablada.setChecked(False)
        self.ts_rb_redPreensablada.setAutoExclusive(True)

        self.ts_rb_bornesTransformador.setAutoExclusive(False)
        self.ts_rb_bornesTransformador.setChecked(False)
        self.ts_rb_bornesTransformador.setAutoExclusive(True)

        self.ts_rb_fusiblesNH.setAutoExclusive(False)
        self.ts_rb_fusiblesNH.setChecked(False)
        self.ts_rb_fusiblesNH.setAutoExclusive(True)

        self.td_rb_interior.setAutoExclusive(False)
        self.td_rb_interior.setChecked(False)
        self.td_rb_interior.setAutoExclusive(True)

        self.td_rb_exterior.setAutoExclusive(False)
        self.td_rb_exterior.setChecked(False)
        self.td_rb_exterior.setAutoExclusive(True)
        # endregion


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
