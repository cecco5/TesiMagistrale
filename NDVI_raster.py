import pathlib
import rioxarray
import earthpy.plot as ep
import earthpy.spatial as es
from IPython.display import display
import matplotlib.pyplot as plt

WORKING_DIRECTORY = pathlib.Path().resolve()
DATA_DIRECTORY = WORKING_DIRECTORY / "data_raster" / "m_3910505_nw_13_1_20150919_crop.tif"

# dati del 2015 che rappresentano la località Cold Spring, Colorado USA,  ottenuti da: https://www.usgs.gov/centers/eros/science/usgs-eros-archive-aerial-photography-
# national-agriculture-imagery-program-naip


# leggo il tiff in input all'interno di un oggetto DataArray di xarray e stampo il contenuto
tiff = rioxarray.open_rasterio(DATA_DIRECTORY)
#display(type(tiff))
#display(tiff)

# <xarray.DataArray (band: 4, y: 2312, x: 4377)>
# [40478496 values with dtype=int16]
# Coordinates:
#   * band         (band) int32 1 2 3 4
#   * x            (x) float64 4.572e+05 4.572e+05 ... 4.615e+05 4.615e+05
#   * y            (y) float64 4.427e+06 4.427e+06 ... 4.425e+06 4.425e+06
#     spatial_ref  int32 0
# Attributes:
#     AREA_OR_POINT:       Area
#     STATISTICS_MAXIMUM:  239
#     STATISTICS_MEAN:     nan
#     STATISTICS_MINIMUM:  32
#     STATISTICS_STDDEV:   nan
#     _FillValue:          -32768
#     scale_factor:        1.0
#     add_offset:          0.0

# calcolo l' NDVI = (NIR - Red) / (NIR + Red), usando la funzione in es:

# tiff[0] band 1 = coastal aerosol
# tiff[1] band 2 = blue
# tiff[2] band 3 = green
# tiff[3] band 4 = red
# tiff[4] band 5 = NIR

NDVI = es.normalized_diff(tiff[3], tiff[0])     # (NIR - Red) / (NIR + Red)

ep.plot_bands(NDVI,
              cmap='PiYG',
              scale=False,
              vmin=-1, vmax=1,
              title="NAIP Derived NDVI\n 19 September 2015 - Cold Springs Fire, Colorado")

#------------------------------------------------------------View Distribution of NDVI Values---#
ep.hist(NDVI.values,
        figsize=(12, 6),
        title=["NDVI: Distribution of pixels\n NAIP 2015 Cold Springs fire site"])

# permette di fare il plot di tutte le stampe precedenti
plt.show()

