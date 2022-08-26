import streamlit as st
import base64
import pandas as pd
import plotly.express as px


def app():
    st.title("Graficas")

    st.image("Graficas/Comparativa Georreferencia.svg")
    st.image("Graficas/% pozos por Tipo Concesión .svg")
    st.image("Graficas/% pozos por USOS.svg")
    st.image("Graficas/% Acuíferos por uso.svg")
