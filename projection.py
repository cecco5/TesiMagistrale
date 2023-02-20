import pathlib
import geopandas as gpd
from IPython.display import display
import matplotlib.pyplot as plt
import pyproj

# impostazione del path (cartella di lavoro e dei dati)
WORKING_DIRECTORY = pathlib.Path().resolve()
DATA_DIRECTORY = WORKING_DIRECTORY / "data_projection"
# dati da https://www.naturalearthdata.com/downloads/10m-cultural-vectors/,
# risoluzione 10m dei confini dei paesi del mondo

# Leggiamo il nostro dataset all'interno di un GeoDataFrame di geopandas
nazioni_del_mondo = gpd.read_file(DATA_DIRECTORY/"ne_10m_admin_0_countries.zip")

# vediamo il CRS dei dati, contenuto all'interno del file .prj del nostro dataset shapefile
display(nazioni_del_mondo.crs)
# EPSG:4326 -> WGS84
# possiamo vedere il CRS tramite un oggetto pyproj.CRS in WKT 2:
crs = pyproj.CRS(nazioni_del_mondo.crs)
display(crs)

# GEOGCRS["WGS 84",
#         ENSEMBLE["World Geodetic System 1984 ensemble",
#                  MEMBER["World Geodetic System 1984 (Transit)"],
#                  MEMBER["World Geodetic System 1984 (G730)"],
#                  MEMBER["World Geodetic System 1984 (G873)"],
#                  MEMBER["World Geodetic System 1984 (G1150)"],
#                  MEMBER["World Geodetic System 1984 (G1674)"],
#                  MEMBER["World Geodetic System 1984 (G1762)"],
#                  MEMBER["World Geodetic System 1984 (G2139)"],
#                  ELLIPSOID["WGS 84",6378137,298.257223563,
#                            LENGTHUNIT["metre",1]],
#                  ENSEMBLEACCURACY[2.0]],
#         PRIMEM["Greenwich",0,
#                ANGLEUNIT["degree",0.0174532925199433]],
#         CS[ellipsoidal,2],
#         AXIS["geodetic latitude (Lat)",
#              north,
#              ORDER[1],
#              ANGLEUNIT["degree",0.0174532925199433]],
#         AXIS["geodetic longitude (Lon)",
#              east,
#              ORDER[2],
#              ANGLEUNIT["degree",0.0174532925199433]],
#         USAGE[
#             SCOPE["Horizontal component of 3D system."],
#             AREA["World."],
#             BBOX[-90,-180,90,180]],
#         ID["EPSG",4326]]

display(nazioni_del_mondo.geometry.head())

# 0    MULTIPOLYGON (((117.70361 4.16341, 117.70361 4...
# 1    MULTIPOLYGON (((117.70361 4.16341, 117.69711 4...
# 2    MULTIPOLYGON (((-69.51009 -17.50659, -69.50611...
# 3    POLYGON ((-69.51009 -17.50659, -69.51009 -17.5...
# 4    MULTIPOLYGON (((-69.51009 -17.50659, -69.63832...
# Name: geometry, dtype: geometry

# Adesso facciamo una stampa della mappa del dataset con il titolo che mostri il CRS:
nazioni_del_mondo.plot()
plt.title(nazioni_del_mondo.crs.name)  # WGS84
# Possiamo riproiettare la mappa in un nuovo sistema di riferimento, in questo caso EPSG: 3395, che
# offre una visione eurocentrica del mondo escludendo le latitudini delle zone polari
# rimuoviamo preliminarmente il continente antartico
nazioni_del_mondo_no_ant = nazioni_del_mondo[(nazioni_del_mondo.ADMIN != "Antarctica") & (nazioni_del_mondo.ADMIN != "French Southern and Antarctic Lands")]
nazioni_del_mondo_EPSG3395 = nazioni_del_mondo_no_ant.to_crs("EPSG:3395")
nazioni_del_mondo_EPSG3395.plot()
plt.title(nazioni_del_mondo_EPSG3395.crs.name)

# Ora possiamo attuare una nuova proiezione
# ortografica (che rappresenta un emisfero come appare dallo spazio), centrata in Italia.

# crs in forma di stringa proj4 (latitudine e longitudine sono quelle di Roma):
new_ortho_crs = '+proj=ortho +lat_0=41.8992 +lon_0=12.5450 +x_0=0 +y_0=0 +a=6370997 +b=6370997 +units=m +no_defs'

# stampo la nuova mappa
nazioni_del_mondo_ortho = nazioni_del_mondo.to_crs(new_ortho_crs)
nazioni_del_mondo_ortho.plot()
plt.axis("off")

# ---------------------------------------------------------Reprojecting a GeoDataFrame---#












# permette di fare il plot di tutte le stampe precedenti
plt.show()

