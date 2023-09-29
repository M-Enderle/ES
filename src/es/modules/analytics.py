from es.utils.database_old import Session, RechnungLieferant
import streamlit as st
import os
import webbrowser
import plotly.express as px
import plotly.graph_objects as go
from typing import List


def open_streamlit():
    webbrowser.open("http://localhost:8501")


def main():
    st.title("Enderle Solutions Statistiken")


if __name__ == "__main__":
    main()
