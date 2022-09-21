import pandas as pd
import plotly.express as px

union = pd.read_csv("files/UnionRegiosDOFShape.csv")


def dinamico(etiqueta, DF=union):
    tabla = pd.merge(pd.pivot_table(data=DF, index=[etiqueta], aggfunc=pd.Series.nunique)['Column1'],
                     pd.pivot_table(data=DF, index=[etiqueta], aggfunc='sum')['VOLUMEN ANUAL EN m3'], on=etiqueta)
    tabla.reset_index(inplace=True)
    return tabla


def app():
    # Filtro, PubPrivEjid, USO QUE AMPARA EL TITULO, AUTORIDAD QUE EMITE EL ACTO, NOMBRE DE ACUIFERO HOMOLOGADO,NOMBRE DE MUNICIPIO
    table1 = dinamico('Filtro')
    table2 = dinamico('PubPrivEjid')
    table3 = dinamico('USO QUE AMPARA EL TITULO')

    table4 = dinamico('NOMBRE DE MUNICIPIO')
    table5 = dinamico('NOMBRE DE ACUIFERO HOMOLOGADO')

    fig1 = px.pie(table1,
                  values='Column1',
                  names='Filtro',
                  title="Comparativa georreferencia")
    fig2 = px.pie(table2,
                  values='Column1',
                  names='PubPrivEjid',
                  title="Porcentaje de pozos por tipo de concesión.")
    fig3 = px.pie(table3,
                  values='Column1',
                  names='USO QUE AMPARA EL TITULO',
                  title="Porcentaje de pozos por usos.")
    fig1.show()
    fig2.show()
    fig3.show()
    fig4 = px.bar(table4,
                  y="NOMBRE DE MUNICIPIO",
                  x="Column1",
                  title="Cantidad de pozos concesionados por municipio.",
                  height=900,
                  labels={  # replaces default labels by column name
                      "Column1": "Concesiones"
                  }, )
    fig4.show()
    fig5 = px.bar(table4,
                  y="NOMBRE DE MUNICIPIO",
                  x="VOLUMEN ANUAL EN m3",
                  title="Volumen de agua extraido de pozos concesionados por municipio.",
                  height=900,
                  labels={  # replaces default labels by column name
                      "Column1": "Concesiones"
                  }, )
    fig5.show()

    ano = pd.DatetimeIndex(union['FECHA DE REGISTRO']).year
    union['ano'] = ano
    pri = union['PubPrivEjid'] == 'PRIVADO'
    pub = union['PubPrivEjid'] == 'PUBLICO'
    eji = union['PubPrivEjid'] == 'EJIDAL'
    data = [union["NOMBRE DE ACUIFERO HOMOLOGADO"], union['Column1'], union["VOLUMEN ANUAL EN m3"], union['ano'], pri,
            pub,
            eji]
    data = pd.concat(data, axis=1,
                     keys=['Nombre de acuifero', 'Column1', 'VOLUMEN ANUAL EN m3', 'AÑO', 'PRIVADO', 'PUBLICO',
                           'EJIDAL'])
    TAB = dinamico("AÑO", data)
    TAB = pd.merge(TAB, pd.pivot_table(data=data, index=["AÑO"], aggfunc='sum')['PRIVADO'], on="AÑO")
    TAB = pd.merge(TAB, pd.pivot_table(data=data, index=["AÑO"], aggfunc='sum')['PUBLICO'], on="AÑO")
    TAB = pd.merge(TAB, pd.pivot_table(data=data, index=["AÑO"], aggfunc='sum')['EJIDAL'], on="AÑO")
    ConFig = px.bar(TAB,
                    y="AÑO",
                    x=["PRIVADO", "PUBLICO", "EJIDAL"],
                    title="Concesiones otorgadas por año y por tipo.",
                    orientation='h',
                    height=900,
                    labels={  # replaces default labels by column name
                        "AÑO": "Año", "value": "Numero de conceciones", "variable": "Tipo de conceción"
                    }, )
    ConFig.show()

    data2 = [union["NOMBRE DE ACUIFERO HOMOLOGADO"], union['Column1'], union["VOLUMEN ANUAL EN m3"], pri, pub, eji]
    data2 = pd.concat(data2, axis=1,
                      keys=['Nombre de acuifero', 'Column1', 'VOLUMEN ANUAL EN m3', 'PRIVADO', 'PUBLICO', 'EJIDAL'])
    TAB2 = pd.merge(pd.pivot_table(data=data2, index=["Nombre de acuifero"], aggfunc='sum')['PRIVADO'],
                    pd.pivot_table(data=data2, index=["Nombre de acuifero"], aggfunc='sum')['PUBLICO'],
                    on="Nombre de acuifero")
    TAB2 = pd.merge(TAB2, pd.pivot_table(data=data2, index=["Nombre de acuifero"], aggfunc='sum')['EJIDAL'],
                    on="Nombre de acuifero")
    TAB2.reset_index(inplace=True)

    VolFig = px.bar(TAB2,
                    y="Nombre de acuifero",
                    x=["PRIVADO", "PUBLICO", "EJIDAL"],
                    title="Volumen de agua concesionado por acuifero y por tipo.",
                    orientation='h',
                    height=900,
                    labels={  # replaces default labels by column name
                        "value": "Volumen de agua", "variable": "Tipo de conceción"
                    }, )
    VolFig.show()
