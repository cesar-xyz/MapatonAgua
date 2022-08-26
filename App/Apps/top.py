import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

def app():
    st.title("Principales dueños de pozos.")
    union = pd.read_csv("files/UnionRegiosDOFShape.csv")
    titulares = np.unique(union["TITULAR"], return_counts=True)
    titulares = dict(zip(titulares[0], titulares[1]))
    print({k: v for k, v in sorted(titulares.items(), key=lambda item: item[1])})
    st.title("Principales extractores.")