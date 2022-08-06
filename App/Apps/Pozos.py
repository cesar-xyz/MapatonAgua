import streamlit as st
import pandas as pd
import plotly.express as px


def app():
    st.title('Rastreo del agua de Nuevo León')
    st.markdown("**Rastreo del agua en Nuevo León** es una iniciativa de mapeo a través de datos y cartografía social de los acuíferos del estado a llevarse a cabo en LABNL Lab Cultural Ciudadano. Esta información será trasladada a un mapa abierto consultable por y para la ciudadanía neolonesa. ---")
    union = pd.read_csv("files/UnionRegiosDOFShape.csv")
    
    my_expander = st.expander(label='Filtros para aplicar en el mapa')
    with my_expander:
        st.markdown("##### ¿Quieres filtrar los datos respecto a su posición geografica?", unsafe_allow_html=True)
        
        filtro = st.radio("Los datos filtrados si coincidian o no con el acuifero al cual estaban referenciados.",('Si, filtrar', 'No'))

        if filtro != 'No':
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

        st.markdown("##### Selecciona el filtro por la extracción anual por $$m^3$$", unsafe_allow_html=True)
        QRatio = st.slider('El 0 es la cantidad minima y 200 es la cantidad maxima.', 0, 200)
        
        unionF = union[union['Extraccion_Grupo'] == QRatio][
            "VOLUMEN DE EXTRACCIÓN ANUAL DE APROVECHAMIENTOS SUBTERRÁNEOS EN m3"]
        st.write("El rango del volumen de extracción anual en m3 es mayor y/o igual a {} m3".format(unionF.min()))

        st.markdown("##### Selecciona el filtro de los datos para clasificarlos ", unsafe_allow_html=True)
        
        option = st.selectbox('Estos datos fueron agregados por la comunidad puede que exista un posible error.', ('si es publico, privado o ejidal','por el uso del acuifero', 'por el nombre del acuifero'))
        
    mapSelector = {
        "por el nombre del acuifero": "NOMBRE DE ACUIFERO HOMOLOGADO",
        'por el uso del acuifero': "USO QUE AMPARA EL TITULO",
        'si es publico, privado o ejidal':"PubPrivEjid"
    }
    st.subheader("Mapa de pozos de agua clasificados {}".format(option))
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


    fig.update_layout(mapbox_style=mapColor[color])
    fig.update_layout(margin={"r": 0, "t": 40, "l": 0, "b": 10})
    st.plotly_chart(fig, use_container_width=True)
