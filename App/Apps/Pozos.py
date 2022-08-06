import streamlit as st
import pandas as pd
import plotly.express as px


def app():
    union = pd.read_csv("files/UnionRegiosDOFShape.csv")

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

    QRatio = st.slider('value', 200, 0)
    unionF = union[union['Extraccion_Grupo'] == QRatio][
        "VOLUMEN DE EXTRACCIÓN ANUAL DE APROVECHAMIENTOS SUBTERRÁNEOS EN m3"]
    st.write("El rango del volumen de extracción anual en m3 es mayor y/o igual a {} m3".format(unionF.min()))

    option = st.selectbox(
        'Que mapa quieres',
        ('NOMBRE DE ACUIFERO HOMOLOGADO', 'USO QUE AMPARA EL TITULO', 'PubPrivEjid'))
    # 160000000

    data = union[union['Extraccion_Grupo'] >= QRatio]
    fig = px.scatter_mapbox(data,
                            lon=data['Longitud'],
                            lat=data['Latitud'],
                            zoom=6,
                            hover_name="TITULAR",
                            hover_data=["TITULO", "VOLUMEN DE EXTRACCIÓN ANUAL DE APROVECHAMIENTOS SUBTERRÁNEOS EN m3"],
                            color=data[option],
                            title="Pozos de agua en NL dividido por su uso."
                            )
    fig.update_layout(mapbox_style="carto-darkmatter")
    fig.update_layout(margin={"r": 0, "t": 40, "l": 0, "b": 10})
    st.plotly_chart(fig, use_container_width=False)
