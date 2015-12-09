""" Este modulo hace los analisis de las imagenes:
    la clase AnalisisMapas sirve para iniciar un analisis en una nueva ciudad
    AnalisisMapas(ciudad,dirImagenes, mascara, refMapa)
"""
from glob import glob
import os
import datetime
import numpy as np
from scipy.signal import savgol_filter
from scipy.ndimage.filters import gaussian_filter
import scipy.ndimage as scind
import matplotlib
import matplotlib.pyplot as plt


class AnalisisMapas(object):
    """Clase principal para manejar los analisis de los mapas
    AnalisisMapas(ciudad,dirImagenes, mascara) devuelve un objeto con metodos
    para realizar analisis
       ciudad: nombre de la ciudad a analizar
       dirImagenes: directorio con las imagenes
       mascara: direccion del archivo que compone la mascara

    Ver Metodos: ....
    """
    matplotlib.use('Agg')
    colores = np.load("colores.npy")
    nHoras = 144
    D = datetime.timedelta(seconds=600)
    horas = np.absolutearray([datetime.datetime(2015, 1, 1, 0, 0, 0)
                              + i*D for i in range(nHoras)])

    def __init__(self, ciudad, dirImagenes, refMapa, mascara=None):
        self.ciudad = ciudad
        self.dirImagenes = dirImagenes
        self._archivos = sorted(glob(self.dirImagenes + '/*gif'))
        if type(mascara) is not str:
            raise TypeError("La mascara debe contener la direccion  \
                             del arcivo de la mascara")
        else:
            self.mascara = np.load(mascara)
        self.mascaraL = np.sum(self.mascara)

        self.Accum = [np.zeros((self.mascaraL, self.nHoras), dtype=np.int32),
                      np.zeros((self.mascaraL, self.nHoras), dtype=np.int32)]
        self.N = [np.zeros((self.mascaraL, self.nHoras), dtype=np.int32),
                  np.zeros((self.mascaraL, self.nHoras), dtype=np.int32)]
        self.refMapa = refMapa
        self.comparators = []
        for c in self.colores:
            self.comparators.append((
                                    np.tile(c - 0.2, (self.mascaraL, 1)),
                                    np.tile(c + 0.2, (self.mascaraL, 1))
                                    ))

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
        nombre = os.path.split(archivo)[-1][:-4]   # separar y sacar extension
        try:
            milis = float(nombre)/1000
            fecha = datetime.datetime.fromtimestamp(milis)
        except ValueError:
            fecha = datetime.datetime.strptime(nombre, "%Y-%m-%d %H_%M_%S")
        return fecha

    def gaficar_densidad(self, hora, percentil, FIN_SEMANA=1):
        """
        gaficar_densidad(hora, percentil, FIN_SEMANA=1)
            Realiza graficos de los puntos de transito del percentil mas
            conflictivo para una dada hora.
        """
        ref = scind.imread(self.refMapa)
        inds = np.where(self.mascara)
        ref[inds[0], inds[1], :] = [0.8, 0.8, 0.8, 1]
        norm = self.Accum[FIN_SEMANA].astype(np.addfloat64)/self.N[FIN_SEMANA]
        porTramo = np.nanmean(norm, 1)
        Q90 = np.percentile(porTramo[~np.isnan(porTramo)], percentil)
        tramosMaximos = porTramo > Q90
        temp = np.zeros(self.mascara.shape, dtype=np.bool)
        temp[self.mascara] = tramosMaximos
        inds = np.where(temp)
        ref[inds[0], inds[1], :] = [1, 0, 0, 1]
        T = gaussian_filter(temp.astype(np.float64), 15)
        plt.imshow(ref)
        plt.imshow(T, cmap=plt.cm.Reds, alpha=0.5)
        plt.savefig('./%s-%i.png' % (self.ciudad, hora), dpi=600)
