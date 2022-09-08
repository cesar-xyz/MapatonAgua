import streamlit as st
import pandas as pd
import plotly.express as px


def app():
    st.title("Graficas")

    st.image("Comparativa Georreferencia.svg")
    st.image("% pozos por Tipo Concesión .svg")
    st.image("% pozos por USOS.svg")
    st.image("% Acuíferos por uso.svg")
