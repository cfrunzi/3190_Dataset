#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from vega_datasets import data
import boto3


import s3fs

countries = alt.topo_feature(data.world_110m.url, "countries")

# Create connection object.
# `anon=False` means not anonymous, i.e. it uses access keys to pull data.
fs = s3fs.S3FileSystem(anon=False)

# Retrieve file contents.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def read_file(filename):
    with fs.open(filename) as f:
        return pd.read_csv(f) #f.read().decode("utf-8")

data = read_file("plastic-waste-data/data_cleaned.csv")
# Print results


# LOADS THE DATA
#data = pd.read_csv(content)


# DISPLAYS APP TITLE AND DESCRIPTION
row1, row2 = st.columns((2, 3))

with row1:
    st.title("Mismanaged Plastic Waste (2010 vs 2019)")

with row2:
    st.write(
        """
        ##
        This dataset compares the volume of mismanaged plastic waste in the years 2010 and 2019. It includes total mismanaged plastic waste
        in millions of tons and total mismanaged plastic waste per capita in kilograms.
    """)


client = boto3.client('lambda', region_name="us-east-1")
def send_email(email):
    response = client.invoke(
        FunctionName="plastic-waste-emailer",
        InvocationType="RequestResponse",
        Payload="{ \"email\" : \"" + email + "\" }"
    )
    print(response)

text = st.text_input(label="Enter your email to receive a more detailed report on plastic waste!", placeholder="email")
st.button(label="Send me the detailed report!", on_click=lambda : send_email(text))

# SHOWS SIDEBAR FUNCTIONS
# show the data in a table
if st.sidebar.checkbox('Show Raw Dataset'):
    st.subheader('Plastic Waste Data')
    st.write(data)


# show charts
if st.sidebar.checkbox('Show 2010 Total Waste Heatmap'):
    st.subheader('2010 Total Waste Heatmap')
    c = alt.Chart(countries).mark_geoshape(stroke='white').encode(
        color='Total_MismanagedPlasticWaste_2010 (millionT):Q',
        tooltip=['Country:N', 'Total_MismanagedPlasticWaste_2010 (millionT):Q']
    ).project(
        'naturalEarth1'
    ).properties(
        width=600, height=400
    ).transform_lookup(
        lookup='id',
        from_=alt.LookupData(data, 'id', [
            'Country',
            'Total_MismanagedPlasticWaste_2010 (millionT)',
            'Total_MismanagedPlasticWaste_2019 (millionT)',
            'Mismanaged_PlasticWaste_PerCapita_2010 (kg per year) ',
            'Mismanaged_PlasticWaste_PerCapita_2019 (kg per year) '])
    ).configure_view(stroke=None)

    st.altair_chart(c)

if st.sidebar.checkbox('Show 2019 Total Waste Heatmap'):
    st.subheader('2019 Total Waste Heatmap')
    c = alt.Chart(countries).mark_geoshape(stroke='white').encode(
        color='Total_MismanagedPlasticWaste_2019 (millionT):Q',
        tooltip=['Country:N', 'Total_MismanagedPlasticWaste_2019 (millionT):Q']
    ).project(
        'naturalEarth1'
    ).properties(
        width=600, height=400
    ).transform_lookup(
        lookup='id',
        from_=alt.LookupData(data, 'id', [
            'Country',
            'Total_MismanagedPlasticWaste_2010 (millionT)',
            'Total_MismanagedPlasticWaste_2019 (millionT)',
            'Mismanaged_PlasticWaste_PerCapita_2010 (kg per year) ',
            'Mismanaged_PlasticWaste_PerCapita_2019 (kg per year) '])
    ).configure_view(stroke=None)

    st.altair_chart(c)

if st.sidebar.checkbox('Show 2010 Per Capita Waste Heatmap'):
    st.subheader('2010 Per Capita Waste Heatmap')
    c = alt.Chart(countries).mark_geoshape(stroke='white').encode(
        color='Mismanaged_PlasticWaste_PerCapita_2010 (kg per year) :Q',
        tooltip=['Country:N',
                 'Mismanaged_PlasticWaste_PerCapita_2010 (kg per year) :Q']
    ).project(
        'naturalEarth1'
    ).properties(
        width=600, height=400
    ).transform_lookup(
        lookup='id',
        from_=alt.LookupData(data, 'id', [
            'Country',
            'Total_MismanagedPlasticWaste_2010 (millionT)',
            'Total_MismanagedPlasticWaste_2019 (millionT)',
            'Mismanaged_PlasticWaste_PerCapita_2010 (kg per year) ',
            'Mismanaged_PlasticWaste_PerCapita_2019 (kg per year) '])
    ).configure_view(stroke=None)

    st.altair_chart(c)

if st.sidebar.checkbox('Show 2019 Per Capita Waste Heatmap'):
    st.subheader('2019 Per Capita Waste Heatmap')
    c = alt.Chart(countries).mark_geoshape(stroke='white').encode(
        color='Mismanaged_PlasticWaste_PerCapita_2019 (kg per year) :Q',
        tooltip=['Country:N',
                 'Mismanaged_PlasticWaste_PerCapita_2019 (kg per year) :Q']
    ).project(
        'naturalEarth1'
    ).properties(
        width=600, height=400
    ).transform_lookup(
        lookup='id',
        from_=alt.LookupData(data, 'id', [
            'Country',
            'Total_MismanagedPlasticWaste_2010 (millionT)',
            'Total_MismanagedPlasticWaste_2019 (millionT)',
            'Mismanaged_PlasticWaste_PerCapita_2010 (kg per year) ',
            'Mismanaged_PlasticWaste_PerCapita_2019 (kg per year) '])
    ).configure_view(stroke=None)

    st.altair_chart(c)
