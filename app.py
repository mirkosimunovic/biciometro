import plotly
import plotly.express as px
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
MAPBOX_API_TOKEN = 'pk.eyJ1IjoibWlya29zbSIsImEiOiJjbDBjd2I4bG8wM2J3M2htdXFxdDBmcDAyIn0.Zds7BTRxavj0D-tueWGekg'
plotly.express.set_mapbox_access_token(MAPBOX_API_TOKEN)
from app_functions import *
from layouts import *

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.QUARTZ])
server = app.server
app.title = 'BicioMetro'


#################### components
nav = dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink("Mapa", active='exact',href="/")),
        dbc.NavItem(dbc.NavLink("Info", active='exact',href="/about")),
        dbc.NavItem(dbc.NavLink("Contacto", active='exact',href="/contact"))
    ],
    pills=True,
    horizontal = 'center'
    )

main_layout = html.Div([
                        html.Br(),
                        nav,
                        dcc.Location(id='location'),
                        html.Div(id='main_content'),
                        html.Footer([html.P(['© 2022 Bici o Metro - Creado por Mirko Simunovic - ' ,
                                     html.A(href='http://www.linkedin.com/in/mirko-simunovic/',children=[html.Img(src=app.get_asset_url('linkedin.png'), height="20px")]),
                                     html.A(href='http://www.github.com/mirkosimunovic',children=[html.Img(src=app.get_asset_url('github.png'), height="20px")]),
                                            ])],style={'position':'relative','bottom':0,'width':'100%','textAlign':'center'}
                                    )             
                        ])


app_layout = html.Div(
    [
    dbc.Row(dbc.Col(html.Div([html.Br()]))),    
    dbc.Row(
        [
        dbc.Col([

                html.Div([html.H1('Bici o Metro',style={'textAlign': 'left'}),
                html.H3('Compara los tiempos de viaje entre Bicicleta y Transporte Público en Santiago.',style={'textAlign':'left'}),
                dcc.Dropdown(
                        id='map_type',
                        options=[{'label': val, 'value': keys} for keys,val in available_maps.items()],
                        value='both',
                        style= { 'color': '#212121'}, 
                            )]),
                html.Br(),
                html.Div([html.H4('Elige tu Punto de Origen:',style={'textAlign':'left'}),
                dcc.Dropdown(id='origin_item',
                                options=[{'label':val,'value':key} for key,val in origin_names.items()],
                                value='baquedano',
                                style= { 'color': '#212121'},                                  
                            )]),
                html.Br(),
                dcc.Loading([html.Div(id='infotext')]),
                html.Br(),
                dcc.Loading([dcc.Graph(id='infoplot')]),
                html.Br()
                ],lg={'size':3,'offset':1},md={'size':10,'offset':1},sm={'size':10,'offset':1}
                ),  
        dbc.Col(
                [html.Div(dcc.Loading([dcc.Graph(id='choropleth')])),
                html.Br()]
                ,lg=5,md={'size':11,'offset':1},sm={'size':11,'offset':1}
                ),              
        ],justify='center')
    ])

app.validation_layout = html.Div([main_layout,
                                  app_layout,
                                  about_layout,
                                  contact_layout
                                 ])

app.layout = main_layout

#-------------------------------#
@app.callback(
    Output('main_content','children'),
    Input('location','pathname')
    )
def display_content(pathname):
    path = pathname
    if path=='/':
        return app_layout
    elif path=='/about':
        return about_layout
    elif path=='/contact':
        return contact_layout

@app.callback(
    Output('choropleth', 'figure'),
    Output('infoplot','figure'),
    Output('infotext','children'),
    Input('choropleth', 'clickData'),
    Input('map_type','value'),
    Input('origin_item','value'),
    )
def update_figure(clickData,map_type,origin):    
    
    if clickData is not None:  
        location = clickData['points'][0]['location']
        selection.append(location)
            
    return get_fig(map_type,origin),get_infoplot(origin),get_infotext(origin)



#-------------------------------#   
if __name__=='__main__':
    app.run_server(debug=False)
