""" Este modulo hace los analisis de las imagenes:
    la clase AnalisisMapas sirve para iniciar un analisis en una nueva ciudad
    AnalisisMapas(ciudad,dirImagenes, mascara)
"""
from glob import glob
import os
import datetime
import numpy as np
from scipy.signal import savgol_filter
import scipy.ndimage as scind


class AnalisisMapas(object):
    """Clase principal para manejar los analisis de los mapas
    AnalisisMapas(ciudad,dirImagenes, mascara) devuelve un objeto con metodos
    para realizar analisis
       ciudad: nombre de la ciudad a analizar
       dirImagenes: directorio con las imagenes
       mascara: direccion del archivo que compone la mascara

    Ver Metodos: ....
    """
    def __init__(self, ciudad, dirImagenes, mascara=None,
                 archColores="colores.npy"):
        self.ciudad = ciudad
        self.dirImagenes = dirImagenes
        self._archivos = sorted(glob(self.dirImagenes + '/*gif'))
        self.colores = np.load(archColores)
        if type(mascara) is not str:
            raise TypeError("La mascara debe contener la direccion  \
                             del arcivo de la mascara")
        else:
            self.mascara = np.load(mascara)
        self.mascaraL = np.sum(self.mascara)
        self.comparators = []
        for c in self.colores:
            self.comparators.append((
                                    np.tile(c - 0.2, (self.mascaraL, 1)),
                                    np.tile(c + 0.2, (self.mascaraL, 1))
                                    ))
        nHoras = 144
        D = datetime.timedelta(seconds=600)
        self.horas = np.absolutearray([datetime.datetime(2015, 1, 1, 0, 0, 0)
                                       + i*D for i in range(nHoras)])
        self.Accum = [np.zeros((self.mascaraL, nHoras), dtype=np.int32),
                      np.zeros((self.mascaraL, nHoras), dtype=np.int32)]
        self.N = [np.zeros((self.mascaraL, nHoras), dtype=np.int32),
                  np.zeros((self.mascaraL, nHoras), dtype=np.int32)]

    def agregar_imagenes_nuevas(self):
        """ Busca imagenes nuevas en el directorio y las analiza."""
        nuevosArch = sorted(glob(self.dirImagenes + '/*gif'))
        for A, i in zip(nuevosArch, range(len(nuevosArch))):
            if A not in self._archivos:   # Si la imagen es nueva agregarla.
                print "Agregando imagen %i de %i" % (i, len(nuevosArch))
                self.analizar_imagen(A)
        return 1

    def analizar_imagen(self, archivo):
        fecha = self._calcular_fecha(archivo)
        dayFLAG = 1 if fecha.weekday() < 5 else 0
        fecha = fecha.replace(year=2015, day=1, month=1)
        idxHora = np.absflatnonzero(self.horas < fecha)[-1]
        im = scind.imread(archivo)
        im = im[self.mascara]
        if im.shape[1] > 3:
            im = im[:, :3]
        i = 0
        for cDown, cUp in self.comparators:
            p = np.alltrue(np.logical_and(im < cUp, im > cDown), 1)
            self.Accum[dayFLAG][p, idxHora] = \
                self.Accum[dayFLAG][p, idxHora] + i
            self.N[dayFLAG][p, idxHora] = self.N[dayFLAG][p, idxHora] + 1
            i = i + 1

    def _calcular_fecha(archivo):
        fecha = os.path.split(archivo)[-1][:-4]   # separar y sacar extension
        try:
            fecha = float(fecha)/1000
            fecha = datetime.datetime.fromtimestamp(fecha)
        except ValueError:
            fecha = datetime.datetime.strptime(fecha, "%Y-%m-%d %H_%M_%S")
        return fecha
