import glob
import pathlib
import geopandas as gpd
from IPython.display import display
import matplotlib.pyplot as plt


#-------------------------------------------------Read and explore geo-spatial data_geopandas sets--#

# impostazione del path (cartella di lavoro e dei dati)
# il dataset è il dataset topografico della
# zona a nord-ovest di Helsinki, Finlandia
# link: (https://www.maanmittauslaitos.fi/en/maps-and-spatial-data/expert-users/product-descriptions/topographic-database)
WORKING_DIRECTORY = pathlib.Path().resolve()
DATA_DIRECTORY = WORKING_DIRECTORY / "data_geopandas"

#pd.set_option('display.max_columns', None)

''' i dati nel database seguono la seguente convenzione nei metadati:

Coordinate Reference System: ETRS89 / ETRS-TM35FIN (EPSG:3067)

L - traffic networks                        
J - pipelines
M - landscape/1
N - landscape/2
R - buildings
K - elevation
S - protected objects
E - special use areas
H - administrative division
U - densly populated areas

a - areas
k - objects (lines, borders of areas, symbols and texts)
v - lines
s - points
t - texts
p - polygons

'''

# creo e stampo una lista di tutti i file .shp del dataset che mi servono (landascape1 - poligoni):
lista_l1_poligoni = glob.glob(f"{DATA_DIRECTORY}/m*p.shp")
print(lista_l1_poligoni)  # 1 file in lista : m_L4132R_p.shp
# assegno il file a una variabile
input_filename = lista_l1_poligoni[0]
# uso geopandas per leggere il file all'interno di un GeoDataFrame
data = gpd.read_file(input_filename)
# stampo tutti i campi (colonne) del GeoDataFrame
#display(data_geopandas.columns)

# Ci sono molte colonne e peraltro i loro nomi sono in finlandese: selezioniamo solo i campi
# 'group' e 'class', oltre a geometry, rinominandoli in italiano:
data = data[["RYHMA", "LUOKKA", "geometry"]]
# per rinominare le colonne uso un dizionario da passare al GeoDataFrame nel metodo rename
data = data.rename(
    columns={
        "RYHMA": "GRUPPO",
        "LUOKKA": "CLASSE"
    }
)
#display(data_geopandas)

#----------------------------------------Explore the data_geopandas set in a map----#

#data_geopandas.plot()

#-------------------------------------------GEOMETRIES IN GEOPANDAS--#
# Geopandas takes advantage of shapely’s geometry objects. Geometries are stored in a column called geometry.

# la colonna geometries contiene stringhe WKT (well-known-text)
# sono oggetti del modulo shapely.geometry che vengono stampati in  WKT.
#display(data_geopandas.geometry.head())

# Si possono usare quindi i metodi del package shapely per gestire le geometrie in geopandas
# Il valore della colonna 'geometry' alla riga 0 sarà un poligono nel nostro dataset:
poligono = data.at[0, "geometry"]
x, y = poligono.exterior.xy
#plt.plot(x, y)

# siccome è noto il SR del dataset, questo definisce anche l' unità di misura (nel file .prj), in questo caso metri. Per cui
# possiamo calcolare l'area del poligono:
# Print information about the area
#print(f"Area: {round(data_geopandas.at[0, 'geometry'].area)} m².")
# Area: 76 m².

# le colonne del GeoDataFrame sono ti tipo GeoSeries

# Posso iterare sulle prime 5 righe del dataset per mostrare l'area dei poligoni
# for index, row in data_geopandas[:5].iterrows():
#     area_poligono = row["geometry"].area
#     print(f"Il poligono alla riga {index} misura un'area di {area_poligono:0.1f} m².")

# Il poligono alla riga 0 misura un'area di 76.0 m².
# Il poligono alla riga 1 misura un'area di 2652.1 m².
# Il poligono alla riga 2 misura un'area di 1406.7 m².
# Il poligono alla riga 3 misura un'area di 3185.6 m².
# Il poligono alla riga 4 misura un'area di 3980.7 m².

# NB: geopandas eredita tutte le funzionalità di pandas, tra cui iterrows()

# in realtà GeoDataFrame ha una proprietà area molto più conveniente da usare:
#display(data_geopandas.area)

# posso creare una nuova colonna Area
data["Area"] = data.area
# display(data_geopandas)

# se voglio la media delle aree di tutti i poligoni
media_aree = data["Area"].mean()
area_minima = data["Area"].min()
area_massima = data["Area"].max()
dev_std_area = data["Area"].std()
#display(f"La media delle aree è {media_aree} m²\n"+f"L'area minima è {area_minima} m² \n"+f"L'area massima è "
#        f"{area_massima} m²\n"+f"La deviazione standard delle aree è {dev_std_area} m²\n")

# se voglio una statistica descrittiva di base di tutti gli attributi:
#statistiche_descrittive = data_geopandas.describe()
#display(statistiche_descrittive)

#--------------------------------------------------------Grouping data_geopandas---#
# Un metodo utile dei (geo)pandas data_geopandas frames è la funzione di raggruppamento: groupby()
# questa può dividere i dati in gruppi in base ad un criterio, applicando una funzione individualmente
# su ciascun gruppo e combinare i risultati di tale operazione all'interno di una struttura dati comune.
# Qui possiamo raggruppare per dividere i nostri dati di input in sotto-insiemi relativi a ciascuna classe
# di uso del terreno, salvando infine ogni sottoinsieme in un file separato.

#display(data_geopandas.head())

# la colonna CLASSE contiene l'informazione sulla copertura del suolo del rispettivo poligono (sottoforma di codice)
# posso usare il metodo pandas unique per mostrare una lista di tutte le classi di uso del terreno presenti nel dataset
#print(data_geopandas["CLASSE"].unique())

# raggruppo i dati in base alla classe creando un nuovo oggetto dataframe raggruppato di tipo DataFrameGroupBy
grouped_data = data.groupby("CLASSE")
#display(grouped_data.groups)
#for key, group in grouped_data:
#    print(f"Classe di uso del terreno {key} ha {len(group)} righe (poligoni).")

# Siamo interessati alla classe 36200, ovvero i LAGHI dell'area selezionata
# laghi è un GeoDataFrame
#laghi = grouped_data.get_group(36200)
#display(type(laghi))
#display(laghi)

# -----------------------------------------------------Scrivere i dati raggruppati in file separati---#
# Possiamo dividere i dati di input in dataset separati per ciascuna classe di uso del suolo
# scrivendo inoltre ciascun dataset in un proprio shapefile separato
display(grouped_data.groups)
# # Itero sui dati in input raggruppati per classe
# for key, group in data_geopandas.groupby("CLASSE"):
#     # salvo ogni gruppo in un nuovo shapefile
#     group.to_file(DATA_DIRECTORY / f"terrain_{key}.shp")

#-----------------------------------------------salvare il report delle statistiche descrittive in un file CSV--#

# Un'applicazione interessante è quella di salvare le statistiche descrittive di base
# di un dataset geospaziale all'interno di un file CSV. Per esempio, è possibile calcolare e visualizzare
# l'area totale di ciscuna classe di copertura del suolo
# Raggruppando i dati in input usando l'attributo "CLASSE", e successivamente calcolare
# la somma delle aree per ciascuna classe. Tutto questo con la seguente linea di codice:

area_per_classe = data.groupby("CLASSE").Area.sum()
display(area_per_classe)

# output
# CLASSE
# 32200    1.057368e+05
# 32417    1.026678e+02
# 32421    8.155664e+05
# 32500    7.014429e+04
# 32611    1.301907e+07
# 32612    5.711131e+04
# 32800    1.141102e+06
# 32900    7.278411e+05
# 33000    6.683503e+05
# 33100    3.214700e+06
# 34100    1.150530e+07
# 34300    8.171606e+03
# 34700    2.785751e+03
# 35300    1.315198e+06
# 35411    4.257255e+05
# 35412    4.616916e+06
# 35421    9.728931e+04
# 35422    1.837270e+03
# 36200    9.989886e+06
# 36313    3.464017e+04
# Name: Area, dtype: float64


# E' possibile salvare la tabella risultante in un file CSV separato usando
# l'approccio standard di pandas (metodo to:csv)

# area_per_classe.to_csv(DATA_DIRECTORY / "area_by_terrain_class.csv")



display(data.crs)




# permette di fare il plot di tutte le stampe precedenti
plt.show()



