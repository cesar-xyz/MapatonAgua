# import streamlit as st
from multiapp import MultiApp
from Apps import Pozos, Graficas, top
import streamlit as st

app = MultiApp()

st.set_page_config(page_title='Agua NL', layout = 'wide', page_icon = 'files/logo-labnl.png', initial_sidebar_state = 'auto')
# Add all your application here
app.add_app("Pozos", Pozos.app)
#app.add_app("Graficas", Graficas.app)
#app.add_app("Principales extractores de agua.", top.app)

# The main app
app.run()