""" Este modulo hace los analisis de las imagenes:
    la clase AnalisisMapas sirve para iniciar un analisis en una nueva ciudad
    AnalisisMapas(ciudad,dirImagenes, mascara)
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
    self.colores = np.load(archColores)
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

    def __init__(self, ciudad, dirImagenes, mascara=None,
                 archColores="colores.npy", refMapa):
        self.ciudad = ciudad
        self.dirImagenes = dirImagenes
        self._archivos = sorted(glob(self.dirImagenes + '/*gif'))
        if type(mascara) is not str:
            raise TypeError("La mascara debe contener la direccion  \
                             del arcivo de la mascara")
        else:
            self.mascara = np.load(mascara)
        self.mascaraL = np.sum(self.mascara)

        self.Accum = [np.zeros((self.mascaraL, nHoras), dtype=np.int32),
                      np.zeros((self.mascaraL, nHoras), dtype=np.int32)]
        self.N = [np.zeros((self.mascaraL, nHoras), dtype=np.int32),
                  np.zeros((self.mascaraL, nHoras), dtype=np.int32)]
        self.refMapa = refMapa

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

    def gaficar_densidad(self, hora, FIN_SEMANA=1, percentil):
        ref = scind.imread(self.refMapa)
        inds = np.where(self.mascara)
        ref[inds[0], inds[1], :] = [0.8, 0.8, 0.8, 1]
        norm = Accum[FIN_SEMANA].astype(float64)/N[FIN_SEMANA]
        porTramo = np.nanmean(norm, 1)
        Q90 = np.percentile(porTramo[~isnan(porTramo)], percentil)
        tramosMaximos = porTramo > Q90
        temp = np.zeros(self.mascara.shape, dtype=bool)
        temp[mascara] = tramosMaximos
        inds = np.where(temp)
        ref[inds[0], inds[1], :] = [1, 0, 0, 1]
        T = gaussian_filter(temp.astype(float64), 15)
        imshow(ref)
        imshow(T, cmap=cm.Reds, alpha=0.5)
        savefig('./%s-%i.png' % (self.ciudad, hora), dpi=600)
