#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 22:07:15 2021

@author: lucia
"""

# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import pandas as pd
import plotly.express as px  # (version 4.7.0)
#import matplotlib.pyplot as plt 
import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.io as pio


pio.renderers.default='browser'

import geopandas as gpd
import math


#archivo_escuelas = "escuelas.geojson"
archivo_escuelas ="https://raw.githubusercontent.com/lupipedraza/Escuelas_Covid19/main/Casos_positivos_de_Covid-19_reportados.csv"#"Casos_positivos_de_Covid-19_reportados.csv"
escuelas = gpd.read_file(archivo_escuelas)
escuelas = escuelas.assign(positivos=0, sospechosos=0, burbujas_aisladas=0, escuela_cerrada=False)

'''
def suma_sin_nulls(valores):
  res = 0
  for valor in valores:
    if not math.isnan(valor):
      res += valor
  return res

def valor_a_booleano(valor):
  return valor == "Sí"

datos_denuncias_archivo = "denuncias_covid.csv"
datos_denuncias = pd.read_csv(datos_denuncias_archivo)

for indice, denuncia in datos_denuncias.iterrows():
  cui_escuela = denuncia[2]
  if math.isnan(cui_escuela):
    continue
  
  cui_escuela = int(cui_escuela)

  filtro = (escuelas['cui'] == cui_escuela) # Ojo acá hay que filtrar los anexos. TODO
  fila_con_cui_escuela = escuelas[filtro]

  escuelas.loc[filtro, 'positivos'] = suma_sin_nulls(denuncia[3:7])
  escuelas.loc[filtro, 'sospechosos'] = suma_sin_nulls(denuncia[7:11])
  escuelas.loc[filtro, 'escuela_cerrada'] = valor_a_booleano(denuncia[11])
  escuelas.loc[filtro, 'burbujas_aisladas'] = suma_sin_nulls(denuncia[12:13])

escuelas_infectadas=escuelas[escuelas['burbujas_aisladas']>0]
coordenada_x=[a[0].x for a in escuelas_infectadas.geometry]
coordenada_y=[a[0].y for a in escuelas_infectadas.geometry]

escuelas_infectadas['lon']=coordenada_x
escuelas_infectadas['lat']=coordenada_y
'''
#%%
'''
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
#Ploteo estático
#Cargamos los barrios

archivo_barrios = "barrios.geojson"
barrios = gpd.read_file(archivo_barrios)

#fig=plt.figure(figsize=(150,150))
base = barrios.plot(color='white', edgecolor='black',linewidth=0.5)


#medida='Cantidad_de_casos_positivos_de_covid_19__Docentes'
#medida='Cantidad_de_casos_positivos_de_covid_19__Alumnxs'
medida='Cantidad_de_casos_positivos_de_covid_19__Trabajadorxs_no_docent'
#medida='Cantidad_de_Docentes_aislados'
#medida='Cantidad_de_trabajadorxs_no_docentes_aislados'

dff = escuelas.copy()


tamaños=[float(a)*10 if a!="" else 0    for a in escuelas[medida] ]
escuelas[medida]=[float(a) if a!="" else 0    for a in escuelas[medida] ]

escuelas_infectadas=escuelas[escuelas[medida]>0]
tamaños=[float(a)*10 if a!="" else 0    for a in escuelas_infectadas[medida] ]

escuelas_infectadas.plot(ax=base,column=medida, cmap='Greens',markersize=tamaños,vmax=1,vmin=0,alpha=0.8,figsize=(15,15))
#escuelas_infectadas.plot(ax=base,column=medida2, cmap='PuBu',s=30,vmax=2,vmin=0,alpha=0.5)

#plt.title(medida)
plt.xticks([])
plt.yticks([])

plt.savefig('mapa'+str(medida)+'.pdf')



dff[dic_nom[medida]]=[float(a) if a!="" else 0 for a in dff[medida]]
dff=dff.rename(columns={"Distrito_Escolar":"Distrito Escolar","__rea_Nivel_Modalidad":'Nivel y Modalidad'})
dff["Distrito Escolar"]=[int(float(de)) for de in dff["Distrito Escolar"]]
    #fig = px.scatter(x=[0, 1, 2, 3, 4], y=[0, 1, 4, 9, 16])
graf2=pd.DataFrame()
indice=dic_nom[medida]
graf2['fecha']=pd.to_datetime(escuelas['Fecha_de_confirmaci__n'],dayfirst=True)
graf2[indice]=[float(a) if a!='' else 0 for a in escuelas[medida]]

    
graf2=graf2.groupby([pd.Grouper(freq='D',key='fecha')]).sum()
graf2=graf2.cumsum()
#graf2=graf2.reset_index()

ax=graf2.plot.area(alpha=0.6,color='g',fontsize=12,linewidth=3)
ax.legend(fontsize=15)
ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
ax.xaxis.set_minor_locator(mdates.DayLocator(interval=30))

# set formatter
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))
ax.tick_params(axis='x', rotation=90)
plt.xlabel('Fecha',fontsize=15)
plt.savefig('Acum_'+str(medida)+'.pdf')

'''

#%%


0#%%


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#app = dash.Dash(__name__)




app.layout = html.Div( children=[
    html.H1(children='Visualización de casos de COVID19 en las aulas de CABA'),


    html.Label('Opciones'),
    
    dcc.Dropdown( id="lista",
        options=[
            {'label': 'Casos positivxs docentes', 'value': 'Cantidad_de_casos_positivos_de_covid_19__Docentes'},
            {'label': u'Casos positivxs alumnxs', 'value': 'Cantidad_de_casos_positivos_de_covid_19__Alumnxs'},
            {'label': 'Casos positivxs no docentes', 'value': 'Cantidad_de_casos_positivos_de_covid_19__Trabajadorxs_no_docent'},
            {'label': 'Docentes aisladxs', 'value': 'Cantidad_de_alumnxs_aislados'},
            {'label': u'Alumnxs aisladxs', 'value': 'Cantidad_de_Docentes_aislados'},
            {'label': 'No docentes aisladxs', 'value': 'Cantidad_de_trabajadorxs_no_docentes_aislados'}

            
        ],
        value='Cantidad_de_casos_positivos_de_covid_19__Docentes'
    ),


    html.Div([
        html.Div([
            html.H2('Mapa de las escuelas'),
            dcc.Graph(
                    id='mapa',
                    figure={}
                    )
        


        ], className="six columns"),

        html.Div([
            html.H2('Evolución'),
            dcc.Graph(
                    id='grafico',
                    figure={}
                    )
        ], className="six columns"),
    ], className="row"),     

    
    #html.Br(),
    #html.Div(id='output_container', children=[])
html.Div(children='Visualización desarrollada por Ideas de Pie en base a la información recolectada por UTE - Secretaría de CyMAT')
])

# Connect the Plotly graphs with Dash Components
@app.callback(
   [Output(component_id='mapa', component_property='figure')],
   [Output(component_id='grafico', component_property='figure')],
    [Input(component_id='lista', component_property='value')]
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    dic_col={'Cantidad_de_casos_positivos_de_covid_19__Docentes':'red',
             'Cantidad_de_casos_positivos_de_covid_19__Alumnxs':'blue',
             'Cantidad_de_casos_positivos_de_covid_19__Trabajadorxs_no_docent':'violet',
             'Cantidad_de_alumnxs_aislados':'red',
             'Cantidad_de_Docentes_aislados':'blue',
             'Cantidad_de_trabajadorxs_no_docentes_aislados':'violet'}

    dic_nom={'Cantidad_de_casos_positivos_de_covid_19__Docentes':'Docentes positivxs',
             'Cantidad_de_casos_positivos_de_covid_19__Alumnxs':'Alumnxs positivxs',
             'Cantidad_de_casos_positivos_de_covid_19__Trabajadorxs_no_docent':'No docentes positivxs',
             'Cantidad_de_alumnxs_aislados':'Docentes aisladxs',
             'Cantidad_de_Docentes_aislados':'Alumnos aisladxs',
             'Cantidad_de_trabajadorxs_no_docentes_aislados':'No docentes aisladxs'}

    #container = "Escuelas por {}".format(option_slctd)
    dff = escuelas.copy()
    #dff=escuelas[escuelas['burbujas_aisladas']>0]
    coordenada_x=[a.x for a in dff.geometry]
    coordenada_y=[a.y for a in dff.geometry]
    dff['lon']=coordenada_x
    dff['lat']=coordenada_y

    dff[dic_nom[option_slctd]]=[float(a) if a!=""  else 0 for a in dff[option_slctd]]
    dff=dff.rename(columns={"Distrito_Escolar":"Distrito Escolar","__rea_Nivel_Modalidad":'Nivel y Modalidad'})
    dff["Distrito Escolar"]=[int(float(de)) for de in dff["Distrito Escolar"]]
    #fig = px.scatter(x=[0, 1, 2, 3, 4], y=[0, 1, 4, 9, 16])
    graf2=pd.DataFrame()
    indice=dic_nom[option_slctd]
    graf2['fecha']=pd.to_datetime(escuelas['Fecha_de_confirmaci__n'],dayfirst=True)
    graf2[indice]=[float(a) if a!='' else 0 for a in escuelas[option_slctd]]

    
    graf2=graf2.groupby([pd.Grouper(freq='D',key='fecha')]).sum()
    graf2=graf2.cumsum()
    graf2=graf2.reset_index()
    #graf2['color']=dic_col[option_slctd]

    fig2=px.area(graf2,x='fecha',y=indice,hover_data={"fecha": "|%B %d, %m"},color_discrete_sequence=[dic_col[option_slctd]],height=400,width=600)#,color=dic_col[option_slctd])
    fig2.update_xaxes(
    dtick="D",
    tickformat="%d %b")

    
    fig = px.scatter_mapbox(dff, lat="lat", lon="lon", hover_name="Name", hover_data=["Distrito Escolar", "Nivel y Modalidad"],
                                color_discrete_sequence=[dic_col[option_slctd]], zoom=10, height=400,width=300,size=dic_nom[option_slctd])
    
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    

    return ([fig,fig2])

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
