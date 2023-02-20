import pathlib
import folium
from IPython.display import display
import geopandas as gpd
#-------------------------------------------------------Create a simple interactive web map---#
# impostazione del path (cartella di lavoro e dei dati)
WORKING_DIRECTORY = pathlib.Path().resolve()
DATA_DIRECTORY = WORKING_DIRECTORY / "data_map"
# directory per esportare pagine html
HTML_DIRECTORY = WORKING_DIRECTORY / "html"

# utilizziamo il package folium per creare mappe interattive leaflet con i dati contenuti in GeoDataFrame
# creiamo una base_map interattiva con location = Roma (latitudine, longitudine) dal server di OpenStreetMap
mappa = folium.Map(
    location=(41.8, 12.5),
    zoom_start=10,
    control_scale=True
)

#-----------------------------------------------------Add a point marker---#
# posso aggiungere alla mappa un segnaposto tramite un oggetto folium.Marker. Fornendo anche una icona
# folium.Icon al segnaposto creato. Inseriamo per esempio il segnaposto sul Colosseo, inserendone le coordinate
# nel sistema di riferimento del dataset (WGS84).

colosseo = folium.Marker(
    location=(41.8902, 12.492),
    tooltip="COLOSSEO",
    icon=folium.Icon(color="green", icon="ok-sign")
)
colosseo.add_to(mappa)

#-----------------------------------------------Add a layer of points---#
# Folium also supports to add entire layers, for instance, as geopandas.GeoDataFrames.
# Folium implements Leaflet’s geoJSON layers in its folium.features.GeoJson class.
# We can initialise such a class (and layer) with a geo-data frame, and add it to a map.

# leggiamo in un GeoDataFrame il dataset con un sottoinsieme dei monumenti di roma (shapefile) scaricato da
# http://www.datiopen.it/it/opendata/Mappa_dei_monumenti_in_Italia
monumenti_roma = gpd.read_file(DATA_DIRECTORY / "monumenti_roma.zip")
display(monumenti_roma.columns)

# creo il geoJSON supportato da leaflet per la mappa dei monumenti
monumenti_layer = folium.features.GeoJson(
    monumenti_roma,
    name="Monumenti pubblici Roma"
)
monumenti_layer.add_to(mappa)



# salvo la mappa, di tipo folium.Map, in un file html, usando il metodo folium.Map.save()
mappa.save(HTML_DIRECTORY / "base-map.html")