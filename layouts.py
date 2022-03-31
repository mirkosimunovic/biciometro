from dash import html
import dash_bootstrap_components as dbc


about_layout = html.Div([dbc.Col([
                        html.Br(),html.Br(),html.Br(),html.Br(),
                        html.H1('Información',style={'textAlign':'left'}),
                        html.Br(),
                        html.Div(html.P(['Esta aplicación usa datos de ',html.A(href='https://developers.google.com/maps/documentation/directions/overview',
                                                                               children='Google Directions API'),
                                         ' para comparar las rutas de viaje entre Bicicleta y Transporte Público en Santiago.'])),
                        html.Br(),
                        html.Div(html.P(['El diseño web está hecho con ',html.A(href='https://dash.plotly.com',
                                                                                children='Dash'),
                                         ', un open-source framework (con Flask por debajo) en Python.'])),
                        html.Br(),
                        html.Div(html.P(['Los elementos de visualización de datos están programados en Python con la librería ',
                                         html.A(href='https://plotly.com/python/',children='Plotly.')]))
                        ],width={'offset':3})
                        ])

contact_layout = html.Div([dbc.Col([
                        html.Br(),html.Br(),html.Br(),html.Br(),    
                        html.H1('Contacto',style={'textAlign':'center'}),
                        html.Br(),
                        html.P(['Puedes revisar el codigo en mi ',html.A(href='http://www.github.com/mirkosimunovic/biciometro',children='Github.')],style={'textAlign':'center'}),
                        html.Br(),
                        html.P(['Me puedes encontrar en ',html.A(href='http://www.linkedin.com/in/mirko-simunovic/',children='LinkedIn.')],style={'textAlign':'center'}),
                        html.Br(),
                        html.P(['Email: ',html.A(href='mailto:mirko.simunovic@gmail.com',children='mirko.simunovic@gmail.com')],style={'textAlign':'center'})

                        ],width={'offset':0})
                        ])