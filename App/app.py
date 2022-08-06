# import streamlit as st
from multiapp import MultiApp
from Apps import Pozos

app = MultiApp()

# Add all your application here
app.add_app("Pozos", Pozos.app)

# The main app
app.run()