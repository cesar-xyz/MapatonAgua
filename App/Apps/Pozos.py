import streamlit as st
import pandas as pd
import plotly.express as px
import math

def app():
    st.title('Rastreo del agua de Nuevo León')
    st.markdown("**Rastreo del agua en Nuevo León** es una iniciativa de mapeo a través de datos y cartografía social de los acuíferos del estado la cual es impulsada desde LABNL Lab Cultural Ciudadano. La intención es visibilizar la distribución de los acuíferos que se encuentran dentro de la entidad, las personas (físicas o morales) dueñas de los títulos para la explotación de los mismos, los pozos de los que se extrae el agua y gráficas que nos permitan visibilizarlo de forma más menos compleja.")
    union = pd.read_csv("files/UnionRegiosDOFShape.csv")
    
    my_expander = st.expander(label='Filtros para aplicar en el mapa')
    with my_expander:
        st.markdown("#### Filtrar datos georreferenciados.", unsafe_allow_html=True)
        
        filtro = st.radio("Coincidencia respecto al pozo de interés y su georreferencia con el manto acuífero al que pertenece.",('Sí, quiero ver los pozos y su correspondencia real.', 'No, quiero ver los datos crudos.'))

        if filtro != 'No, quiero ver los datos crudos.':
            union = union[union['Filtro'] == 'Coincide']
            
        union = union.sort_values(by='VOLUMEN DE EXTRACCIÓN ANUAL DE APROVECHAMIENTOS SUBTERRÁNEOS EN m3')

        crecimiento = int(union.shape[0] / 200)
        group = []
        minRango = 0
        maxRango = crecimiento

        for i in range(1, 201):
            for k in range(minRango, maxRango):
                group.append(i)
            minRango = (crecimiento * i) + 1
            maxRango = (crecimiento * (i + 1)) + 1 if i < 199 else union.shape[0] + 1

        union['Extraccion_Grupo'] = group

        st.markdown("#### Filtrar por cantidad de agua extraída  anualmente ($$m^3$$, metros cúbicos).", unsafe_allow_html=True)
        # st.write("Los datos que observarás a continuación corresponden a los pozos que se encuentran en el estado de Nuevo León. De los cerca de 9000 que se encuentran en la entidad se decidió crear un filtro en 200 segmentos que agrupan los pozos por cantidad de agua extraída.")
        st.write("Esta barra deslizadora funciona como un termómetro, siéntete libre de moverla de un lado a otro, te darás cuenta de que el mapa modifica los datos que muestra a medida que lo haces.")
        QRatio = st.slider('0 es la el grupo de pozos que presentan menor extracción y 200 aquellos que presentan mayor cantidad de extracción.', 0, 200)
        
        unionF = union[union['Extraccion_Grupo'] == QRatio][
            "VOLUMEN DE EXTRACCIÓN ANUAL DE APROVECHAMIENTOS SUBTERRÁNEOS EN m3"]
        unionFmin = 0 if math.isnan(unionF.min()) else unionF.min()
        st.write("El rango del volumen de extracción anual en m3 es mayor y/o igual a {} m3.".format(unionFmin))

        st.markdown("#### Selecciona el filtro de los datos para clasificarlos.", unsafe_allow_html=True)
        
        option = st.selectbox('Estos datos fueron agregados por la comunidad puede que exista un posible error.', ('si es público, privado o ejidal','por el uso del acuífero', 'por el nombre del acuífero'))
        
    mapSelector = {
        "por el nombre del acuífero": "NOMBRE DE ACUIFERO HOMOLOGADO",
        'por el uso del acuífero': "USO QUE AMPARA EL TITULO",
        'si es público, privado o ejidal':"PubPrivEjid"
    }
    st.header("Mapa de pozos de agua clasificados {}".format(option))
    data = union[union['Extraccion_Grupo'] >= QRatio]
    fig = px.scatter_mapbox(data,
                            lon=data['Longitud'],
                            lat=data['Latitud'],
                            zoom=6,
                            hover_name="TITULAR",
                            hover_data=["TITULO", "VOLUMEN DE EXTRACCIÓN ANUAL DE APROVECHAMIENTOS SUBTERRÁNEOS EN m3"],
                            color=data[mapSelector[option]],
                            )
   
    color = st.sidebar.radio(
        'Color del mapa',
        ("Claro", "Obscuro")
    )
    mapColor = {
        "Claro": "carto-positron",
        "Obscuro": "carto-darkmatter"
    }
    st.sidebar.write("[Documentación](https://sites.google.com/view/acuiferosnl/inicio)")

    fig.update_layout(mapbox_style=mapColor[color])
    fig.update_layout(margin={"r": 0, "t": 40, "l": 0, "b": 10})
    st.plotly_chart(fig, use_container_width=True)

