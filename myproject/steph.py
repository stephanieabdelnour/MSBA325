from email import header
from gettext import install
from lib2to3.pgen2.pgen import DFAState
from turtle import color, title
from matplotlib import markers
from pyrsistent import freeze
import streamlit as st
import pandas as pd
from PIL import Image
from streamlit_option_menu import option_menu
import plotly.graph_objs as go
st.set_page_config(
    page_title="MSBA325 - Stephanie Abdelnour",
    page_icon="🧊",
    layout="wide",
)
font = "monospace"
st.subheader("MSBA325 - Stephanie Abdelnour")
st.title("COVID-19 World Vaccination Progress Dataset")
menu = option_menu(None, ["Home","Dataset","Dashboard"],icons=['house',"cloud","bar-chart-line"],menu_icon="cast", default_index=0, orientation="horizontal", styles={"container": {"padding": "0!important", "background-color": "#fafafa"},"icon": {"color": "black", "font-size": "25px"}, "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},"nav-link-selected": {"background-color": "#FF3366"},})

if menu=="Dataset": st.write("The data contains the following information: Country, Total number of vaccinations, Total number of people vaccinated, Daily vaccinations, Total vaccinations per hundred, Total number of people vaccinated per hundred, Total number of people fully vaccinated per hundred, Number of vaccinations per day, Daily vaccinations per million, Vaccines used in the country.")
if menu=="Home": st.image("covid-19-vaccination-1500-991-2.jpg")

#Dataset
col1, col2= st.columns(2)
if menu=="Dataset":col1.metric("Countries", "77")
if menu=="Dataset":col2.metric("Type or Combination of vaccines", "14")
import pandas as pd
import numpy as np
df= pd.read_csv("output.csv")
if menu=="Dataset": st.write(df)

#Visu1
#Most type of Vaccin used
import altair as alt
fig1 = alt.Chart(df).mark_point().encode(
    y='total_vaccinations',
    x='vaccines',
    #color='vaccines',
   # column='vaccines',
    
).properties(
    width=500,
    height=500,
    title= "Total number of vaccine sold under each brand"
)
fig1.configure_header(
    titleColor='Set1[7]',
    titleFontSize=14,
    labelColor='#FF4B4B',
    labelFontSize=12
)
if menu=="Dashboard":col2.write(fig1)


#Visu2
#Total vaccination per country
fig2 = alt.Chart(df).mark_point().encode(
    y='total_vaccinations',
    x='country',
    #color='vaccines',
   # column='vaccines',
    
).properties(
    width=1000,
    height=500,
    title= "Total number of vaccine in each country"
)
fig1.configure_header(
    titleColor='#FF4B4B',
    titleFontSize=14,
    labelColor='#FF4B4B',
    labelFontSize=12
)
if menu=="Dashboard":col1.write(fig2)

#Visu3
#Progress of vaccination
import plotly.express as px
fig = px.scatter(df, x="daily_vaccinations", y="total_vaccinations", animation_frame="date", animation_group="iso_code",
           hover_name="iso_code", text='iso_code',range_x=[0,1500000], range_y=[0,175000000], title="The Progress of Vaccination")
if menu=="Dashboard":col1.write(fig)

#Visu4
#Total vaccinated per 10,000 population around the globe (GIS)
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
fig = go.Choropleth(locations = df["country"],locationmode = 'country names',z = df['daily_vaccinations'],
                                         text= df['country'],
                    colorbar = dict(title= "Daily vaccinations"),reversescale =True,colorscale = 'viridis')
data = [fig]

layout = go.Layout(title = 'Daily Vaccinations according to each Country')
fig = dict(data = data,layout = layout)
if menu=="Dashboard":col2.write(fig)

#Vis5
#The daily vaccination drive around the globe
dates = df['date'].unique().tolist()
# countries without repetition use 'unique'
countries = df['country'].unique().tolist()
short = df[['date', 'country', 'daily_vaccinations']]
# i.e we want to make sure we have some data for each, even if it is 0 
keys= list(zip(short.date.tolist(), short.country.tolist()))
for date in dates:
    for country in countries:
        idx = (date, country)
        if idx not in keys:
            if date == min(dates):
                # this means there's no entry for {country} on the earliest date 
                short = short.append({
                    "date": date, 
                    "country": country, 
                    "daily_vaccinations": 0
                }, ignore_index=True)
            else:
                # entry for {country} is missing on a date other than the earliest
                short = short.append({
                    "date": date, 
                    "country": country, 
                    "daily_vaccinations": pd.NA
                }, ignore_index=True)

#fill missing values with previous day values (this is OK since it is cumulative)
short = short.sort_values(['country', 'date'])

short.daily_vaccinations = short.daily_vaccinations.fillna(method='ffill')

# scale the number by log to make the color transitions smoother
vaccines = short.sort_values('date')
vaccines['log_scale'] = vaccines['daily_vaccinations']#.apply(lambda x:math.log2(x+1))

fig =px.choropleth(vaccines, locations="country", 
                    locationmode='country names',
                    color="log_scale", 
                    hover_name="country", 
                    hover_data=['log_scale', "daily_vaccinations"],
                    animation_frame="date",
                    color_continuous_scale="blues",
                    title='Vaccination Drive around the world'
                   )

fig.update_layout(coloraxis={"cmax":25,"cmin":0})
if menu=="Dashboard": st.write(fig)
