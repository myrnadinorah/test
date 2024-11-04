#!/usr/bin/env python
# coding: utf-8

# In[1]:


import yfinance as yf
import panel as pn
import plotly.graph_objects as go
import pandas as pd

# Configurar Panel
pn.extension("plotly")

# Lista de tickers para el portafolio
tickers = ["AAPL", "MSFT", "GOOGL", "AMZN"]

# Descargar datos históricos usando yfinance
def get_data(ticker):
    data = yf.download(ticker, period="1y", interval="1d")
    data["Returns"] = data["Adj Close"].pct_change()
    return data

# Crear gráficos de precios ajustados y rendimientos
def create_graph(ticker):
    data = get_data(ticker)
    fig = go.Figure()

    # Gráfico de precios ajustados
    fig.add_trace(
        go.Scatter(
            x=data.index, 
            y=data["Adj Close"], 
            mode="lines", 
            name=f"Precio Ajustado ({ticker})"
        )
    )

    # Gráfico de rendimientos diarios
    fig.add_trace(
        go.Scatter(
            x=data.index, 
            y=data["Returns"], 
            mode="lines", 
            name=f"Rendimiento Diario ({ticker})",
            yaxis="y2"
        )
    )

    fig.update_layout(
        title=f"{ticker} - Precio Ajustado y Rendimiento",
        yaxis=dict(title="Precio Ajustado"),
        yaxis2=dict(title="Rendimiento Diario", overlaying="y", side="right"),
        xaxis_title="Fecha",
    )
    return fig

# Widget de selección de ticker
ticker_select = pn.widgets.Select(name="Seleccionar Ticker", options=tickers)

# Panel interactivo para mostrar gráficos
@pn.depends(ticker_select)
def view_portfolio(ticker):
    return pn.Column(
        f"### Datos financieros para {ticker}",
        create_graph(ticker)
    )

# Estructura de la interfaz
app = pn.Column(
    "# Portafolio Financiero Interactivo",
    "Seleccione un ticker para ver su rendimiento y precio ajustado.",
    ticker_select,
    view_portfolio
)

# Ejecutar la aplicación de Panel
app.servable()

