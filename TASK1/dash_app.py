import json
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output


external_stylesheets = [dbc.themes.SLATE, 'https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# ---------- Import data
with open('india_states.json') as f:
    india_states = json.load(f)


df = pd.read_csv('final_state_count.csv', parse_dates=['Date'])
df['dt_str'] = df['Date'].apply(lambda x: x.strftime('%b %Y'))
df.fillna(0, inplace=True)
df['Infection_Count_norm'] = df['Infection_Count'].apply(lambda x: np.sqrt(x))

pdf = pd.read_csv('total_case_class.csv')

periods = ['Mar 2020 - Apr 2020', 'Apr 2020 - May 2020', 'May 2020 - Jun 2020', 'Jun 2020 - Jul 2020', 
            'Jul 2020 - Aug 2020', 'Aug 2020 - Sep 2020', 'Sep 2020 - Oct 2020', 'Oct 2020 - Nov 2020', 
            'Nov 2020 - Dec 2020', 'Dec 2020 - Jan 2021', 'Jan 2021 - Feb 2021', 'Feb 2021 - Mar 2021']


max_count = df['Infection_Count_norm'].max()
max_count += 2

colors = {'background': '#141414', 'header-text': '#FF7F0E', 'text': '#ffdab9'}
cont_color = px.colors.sequential.Oranges


scatter_fig = px.scatter(
    pdf, 
    x='total_cases_capita', 
    y='pdf', 
    size='total_cases_capita', 
    hover_data=['statecode'],
    labels={'total_cases_capita': 'Total Cases Per Capita', 'pdf': 'Probability Distribution Function'},
    color='Category',
    color_discrete_map={'Low': '#fecc5c', 'Mid': '#fd8d3c', 'High': '#e31a1c'},
    title = 'Distribution of States',
    template='plotly_dark')

med = pdf['total_cases_capita'].median()
std = pdf['total_cases_capita'].std()
scatter_fig.add_vline(x=med,line_width=0.5, line_dash='dash',annotation_text='Median')
scatter_fig.add_vline(x=med+std,line_width=0.5, line_dash='dash',annotation_text='Median + Sigma',)
scatter_fig.add_vline(x=med+std+std,line_width=0.5, line_dash='dash', annotation_text='Median + 2Sigma')

scatter_fig.update_layout(
    title_font_color=colors['text'],
    title = {'x':0.5}, 
    font = {"family" : "courier"})


# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1('Covid-19 Virus Outbreak in INDIA', style={'text-align': 'center', 'color': 'white', 'margin-bottom': '0px'}),
    html.H6('[ Mar 2020 - Mar 2021 ]', style={'text-align': 'center', 'color': colors['text']}),

    dcc.Markdown('''
        *"The bigger the crisis, the bolder the changes needed to develop our societies."*
    ''', style={'text-align': 'center', 'color': colors['text'], 'font-family': 'Helvetica','margin-bottom': '50px'}),

    

    dbc.Row([
        dcc.Markdown(id='as_of', style={'color': colors['text']})
        ], style={'margin-left':'50px', 'margin-right':'50px'}),

    dbc.Row([
        dbc.Col([
            html.H2(id='all_count', style={'text-align': 'center', 'color': 'white', 'margin-bottom': '0px'}),
            html.H6('Total Confirmed Cases', style={'text-align': 'center', 'color': colors['text']})
        ],style={'backgroundColor':colors['background']}),
        dbc.Col([
            html.H2(id='overall_change' ,style={'text-align': 'center', 'color': 'white', 'margin-bottom': '0px'}),
            html.H6('Overall change', style={'text-align': 'center', 'color': colors['text']})
        ],style={'backgroundColor':colors['background']}),
        dbc.Col([
            html.H2(id='max_state', style={'text-align': 'center', 'color': 'white', 'margin-bottom': '0px'}),
            html.H6('State with highest infection', style={'text-align': 'center', 'color': colors['text']})
        ],style={'backgroundColor':colors['background']}),
        dbc.Col([
            html.H2(id='min_state', style={'text-align': 'center', 'color': 'white', 'margin-bottom': '0px'}),
            html.H6('State with lowest infection', style={'text-align': 'center', 'color': colors['text']})
        ],style={'backgroundColor':colors['background']}),
    ], style={'margin-left':'50px', 'margin-right':'50px'}),

    html.Br(),

    dbc.Row([
        html.Div(
            dcc.Graph(id='choro1')
        , style={'width': '48%', 'display': 'inline-block'}),
        html.Div(
            dcc.Graph(id='choro2')
        , style={'width': '38%', 'display': 'inline-block'}),
        dbc.Col([
            html.H4('Pick a period:', style={'color': colors['text']}),
            dcc.RadioItems(
                id='periods',
                options=[{'label': i, 'value': i} for i in periods],
                value=periods[3],
                style={'color': 'white'}, 
                inputStyle={'margin-right': '10px', 'margin-bottom': '30px'})
        ], width='auto'),
    ], style={'margin-left':'100px', 'margin-right':'100px', 'backgroundColor':colors['background']}),

    html.Br(),
    html.Br(),

    dbc.Row([
        dbc.Col(html.H4('Pick a State:', style={'color': colors['text']}), width='auto'),
        dbc.Col(dcc.Dropdown(id='select_state',
                 options=[{'label': st, 'value': st} for st in df['State'].unique()],
                 multi=False,
                 value=df['State'].unique()[0],
                 style={'backgroundColor': colors['text'], 'color': colors['background']})
        , width=3)
    ], style={ 'width': '58%', 'margin-left':'150px', 'margin-right':'150px', 'margin-bottom': '0px'}),

    dbc.Row([
        html.Div(
            dcc.Graph(id='line_state')
        , style={'width': '100%'})
    ], style={'margin-left':'150px', 'margin-right':'150px'}),

    html.Br(),
    html.Br(),

    dbc.Row([
        html.Div(
            dcc.Graph(id='scatter_pdf', figure=scatter_fig)
        , style={'width': '100%'})
    ], style={'margin-left':'200px', 'margin-right':'200px'}),

    dcc.Markdown('''
        *Powered by Dash + Plotly*
    ''', style={'text-align': 'center', 'color': colors['text'],'margin-bottom': '20px', 'margin-top': '20px'}),
    
])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components

@app.callback(
    [Output(component_id='as_of', component_property='children'),
    Output(component_id='all_count', component_property='children'),
    Output(component_id='overall_change', component_property='children'),
    Output(component_id='max_state', component_property='children'),
    Output(component_id='min_state', component_property='children')],
    [Input(component_id='periods', component_property='value')]
)
def update_stats(radio_selected):
    dur = radio_selected.split(' - ')

    as_of = ' ###### *As of '+dur[1]+':* '

    dff_1 = df[df['dt_str'] == dur[0]]
    dff_2 = df[df['dt_str'] == dur[1]]

    sum1 = dff_1['Infection_Count'].sum()
    sum2 = dff_2['Infection_Count'].sum()

    _change = ((sum2-sum1)/sum1)*100
    _change_str = str(round(_change,2))+'%'

    max_state = dff_2[dff_2['Infection_Count'] == dff_2['Infection_Count'].max()].iloc[0]['State']
    min_state = dff_2[dff_2['Infection_Count'] == dff_2['Infection_Count'].min()].iloc[0]['State']

    return as_of,sum2, _change_str,max_state,min_state


@app.callback(
    [Output(component_id='choro1', component_property='figure'),
     Output(component_id='choro2', component_property='figure')],
    [Input(component_id='periods', component_property='value')]
)
def update_choros(radio_selected):
    dur = radio_selected.split(' - ')

    dff_1 = df[df['dt_str'] == dur[0]]

    choro1 = px.choropleth_mapbox(
    data_frame=dff_1,
    geojson=india_states,
    locations='State',
    color='Infection_Count_norm',
    hover_data=['State', 'Infection_Count'],
    color_continuous_scale=cont_color,
    template='plotly_dark',
    range_color=(0, max_count),
    featureidkey='properties.state_name',
    mapbox_style='carto-darkmatter',
    center = {'lat': 24, 'lon': 82},
    zoom=3.7,
    opacity=0.9,
    title=dur[0])

    choro1.update_geos(fitbounds='locations', visible=False)
    choro1.update_layout(height=700, margin={'r':20,'t':40,'l':20,'b':20})
    choro1.update_layout(
        title_font_color=colors['text'],
        title = {'x':0.5}, 
        font = {"family" : "courier"})


    dff_2 = df[df['dt_str'] == dur[1]]

    choro2 = px.choropleth_mapbox(
        data_frame=dff_2,
        geojson=india_states,
        locations='State',
        color='Infection_Count_norm',
        hover_data=['State', 'Infection_Count'],
        color_continuous_scale=cont_color,
        template='plotly_dark',
        range_color=(0, max_count),
        featureidkey='properties.state_name',
        mapbox_style='carto-darkmatter',
        center = {'lat': 24, 'lon': 82},
        zoom=3.7,
        opacity=0.9,
        title=dur[1])

    choro2.update_geos(fitbounds='locations', visible=False)
    choro2.update_layout(height=700, margin={'r':20,'t':40,'l':20,'b':20}, coloraxis_showscale=False)
    choro2.update_layout(
        title_font_color=colors['text'],
        title = {'x':0.5}, 
        font = {"family" : "courier"})


    return choro1, choro2


@app.callback(
    Output(component_id='line_state', component_property='figure'),
    [Input(component_id='select_state', component_property='value')]
)
def update_line_graph(option_slctd):

    df_state = df[df['State'] == option_slctd]

    fig = px.line(df_state, 
        x="Date", 
        y="Infection_Count_norm",
        template='plotly_dark',
        color_discrete_map={'Infection_Count_norm': colors['header-text']},
        title = ' State Trend Line for '+option_slctd,
        labels={'Infection_Count_norm': 'Normalized Infection Count'},
    )

    fig.update_traces(mode='lines+markers')
    fig.update_xaxes(dtick='M1')
    fig.update_layout(title_font_color=colors['text'],
                    title = {'x':0.5}, 
                    font = {"family" : "courier"})

    return fig


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(use_reloader=True)
