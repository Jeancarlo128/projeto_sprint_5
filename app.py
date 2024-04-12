import pandas as pd
import plotly.express as px
import streamlit as st

# Ler os dados
car_data = pd.read_csv('vehicles.csv')

# Criar um cabeçalho
st.header('Análise de Dados de Veículos')

# Data Viewer
st.subheader('Data Viewer')

# Adicionar um checkbox para incluir fabricantes com menos de 100 anúncios
include_less_than_100 = st.checkbox(
    'Incluir fabricantes com menos de 100 anúncios')

# Filtrar os dados se o checkbox estiver marcado
if include_less_than_100:
    # Filtrar fabricantes com menos de 100 anúncios
    car_data_filtered = car_data.groupby(
        'model').filter(lambda x: len(x) < 100)
else:
    car_data_filtered = car_data

# Exibir uma amostra dos dados filtrados
st.write(car_data_filtered.head(23))

# Criar um cabeçalho
st.header('Vehicle Types by Manufacturer')

# Calcular o número de tipos de veículos por fabricante
vehicle_types = car_data.groupby(
    ['model', 'type']).size().reset_index(name='count')

# Plotar o gráfico de barras
fig = px.bar(vehicle_types, x='model', y='count', color='type',
             title='Tipos de Veículos por Fabricante')
st.plotly_chart(fig, use_container_width=True)

# Gráfico de dispersão
st.subheader('Histogram of Condition vs Model Year')
fig_histogram = px.histogram(car_data, x='model_year',
                             y='price', color='condition')
st.plotly_chart(fig_histogram, use_container_width=True)

# Gráfico de dispersão
st.subheader('Scatter Plot: Odometer vs Price')
fig_scatter = px.scatter(car_data, x='odometer', y='price', color='condition')
st.plotly_chart(fig_scatter, use_container_width=True)

# Criar um cabeçalho
st.header('Compare price distribution between manufactures')

# Caixas de seleção para escolher os fabricantes
manufacturer_1 = st.selectbox(
    'Select manufacturer 1:', car_data['model'].unique())
manufacturer_2 = st.selectbox(
    'Select manufacturer 2:', car_data['model'].unique())

# Filtrar os dados para os fabricantes selecionados
filtered_data_manufacturer_1 = car_data[car_data['model'] == manufacturer_1]
filtered_data_manufacturer_2 = car_data[car_data['model'] == manufacturer_2]

normalize_checkbox = st.checkbox('Normalize Histogram')

# Plotar os gráficos de barras sobrepostas
fig_comparison = px.histogram(filtered_data_manufacturer_1, x='price',
                              histnorm='percent', opacity=0.75)

fig_comparison.add_histogram(x=filtered_data_manufacturer_2['price'], histnorm='percent', opacity=0.75,
                             name=manufacturer_2)
fig_comparison.update_layout(barmode='overlay', xaxis_title='Price',
                             yaxis_title='Percente', legend_title='Manufacturer')
st.plotly_chart(fig_comparison, use_container_width=True)
