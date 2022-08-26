# import streamlit as st
from multiapp import MultiApp
from Apps import Pozos, Graficas, top

app = MultiApp()

# Add all your application here
app.add_app("Pozos", Pozos.app)
#app.add_app("Graficas", Graficas.app)
#app.add_app("Principales extractores de agua.", top.app)

# The main app
app.run()