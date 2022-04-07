from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import json
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import ast

origin_coor = dict(baquedano=[-33.4369,-70.6344],
                   dominicos=[-33.4079,-70.5451],
                   tobalaba=[-33.4183,-70.6015],
                   nunoa=[-33.4561,-70.5938],
                   puentealto=[-33.6095,-70.5759],
                   cisterna=[-33.5374,-70.6643],
                   maipu=[-33.5100,-70.7570],
                   sanpablo=[-33.4442,-70.7233],
                   loslibertadores=[-33.3671,-70.6874],
                   lovalledor=[-33.478247, -70.680678],
                   vicentevaldes=[-33.5263,-70.5968]
                  )
origin_names = dict(baquedano='Plaza Baquedano',
                    dominicos='Plaza Los Dominicos',
                    tobalaba='Metro Tobalaba',
                    nunoa='Plaza Ñuñoa',
                   puentealto='Plaza Puente Alto',
                   cisterna='Metro La Cisterna',
                    maipu='Plaza Maipu',
                    sanpablo='Metro San Pablo',
                    loslibertadores='Metro Los Libertadores',
                    lovalledor='Metro Lo Valledor',
                    vicentevaldes='Metro Vicente Valdes'
                   )


# all_df_times = {}
######################## Load all Data ##################################
def load_data(origin):
    
    # all_df_times[origin] = pd.read_csv('assets/'+origin+'_database.csv')
    return pd.read_pickle('assets/'+origin+'_database.zip')

# for origin in origin_names:
#     load_data(origin)
########################################################################
        

available_maps = dict(both='Bici y Transporte Publico',bike='Bicicleta',transit='Transporte Publico')
color_column = dict(both='diff',bike='time_bike',transit='time_transit')
suffix = dict(both=' hr',bike=' hr',transit=' hr')

current_map = dict(map_type='both')
current_origin = dict(origin='baquedano')
selection = []
hover_keys = ['time_transit','time_bike','vel_perc']

def make_base_map(map_type='both',origin='baquedano'):
    df = load_data(origin)
    df['diff'] = df.time_transit-df.time_bike
    df['vel_perc'] =  df.apply(lambda x: np.round(x['vel_perc'],2),axis=1)
    fig = px.choropleth_mapbox(df, geojson="assets/largegrid3_new.json",locations='id',
                               color=color_column[map_type],
                               mapbox_style='basic',
                               zoom=10.3, 
                               center = {"lat": -33.4909, "lon": -70.6593},
                               featureidkey="properties.id",
                               opacity=0.8,
                               color_continuous_scale = [(0, "red"),  
                                                         (get_white_point(df,map_type), "white"),
                                                         (1, "blue")] if map_type=='both' else px.colors.cyclical.HSV,
                               range_color=get_range_lims(df,map_type),
                               hover_name='end_address',
                               hover_data={key:(True if key in hover_keys else False) for key in list(df.columns)},
                               labels={'vel_perc':'% Mas Rapido (o Lento)','%Gain':'% de Ganancia/Tardanza',
                                       'time_bike':'Bicicleta (hr)','time_transit':'Transp. Pub. (hr)',
                                       'diff':'Tiempo Ahorrado con Bicicleta (hr)'},
                              )
    fig.update_layout(margin={"r":10,"t":20,"l":20,"b":0})
    fig.update_layout(height=750,width=800)
    fig.update_layout(title={
        'text': "Haz click en el mapa y compara las rutas",
        'y':0.99,
        'x':0.01,
        'font':{'color':'blue','size':14},
        'xanchor': 'left',
        'yanchor': 'top'})
    fig.update_traces(marker_line_width=0)
    fig.update_coloraxes(colorbar_ticksuffix=suffix[map_type])
    fig.update_coloraxes(colorbar_title_side='right')
    return fig

def get_range_lims(df,map_type):
    
    if map_type=='both':
        arr = df['diff']
        std = arr.std()
        mean = arr.mean()
        return [mean-3*std,mean+3*std]
    elif map_type=='bike':
        arr = df['time_bike']
        return [0,arr.mean()+3*arr.std()]
    elif map_type=='transit':
        arr = df['time_transit']
        return [0,arr.mean()+3*arr.std()]


def get_white_point(df,map_type):
          
    lims = get_range_lims(df,map_type)
    diff = lims[1]-lims[0]
    return (-lims[0]/diff)
    
def get_routes(response_list):
    lat = []
    lng = []
    json_list = ast.literal_eval(response_list)
    for loc in json_list:
        lat.append(loc['start_location']['lat'])
        lat.append(loc['end_location']['lat'])
        lng.append(loc['start_location']['lng'])
        lng.append(loc['end_location']['lng'])  
    return lat,lng

def get_starts(response_list):
    lat,lng = [],[]
    json_list = ast.literal_eval(response_list)
    for loc in json_list:
        lat.append(loc['start_location']['lat'])
        lng.append(loc['start_location']['lng'])
    return lat,lng    

def new_trace(name,color,lat,lng):
    fig.add_trace(go.Scattermapbox(mode='lines',
                                  lat=lat,
                                  lon=lng, 
                                  line = {'width': 5,'color':color},
                                  hoverinfo='none',
                                  below="",
                                  name=name,
                                  )
                 )    

def add_origin(fig,origin='baquedano'):
    fig.add_trace(go.Scattermapbox(
                                  mode='markers+text',
                                  lat=[origin_coor[origin][0]],
                                  lon=[origin_coor[origin][1]], 
                                  marker = {'size': 14,'color':'purple','symbol':'marker'},
                                  text=[origin_names[origin]],
                                  hoverinfo='none',
                                  textposition="top center",
                                  below="",
                                  textfont={'color':'black','size':17,'family':'Arial'},
                                  )
                 )
                        
    
def add_symbol(lat,lng,symbol_list):       
    fig.add_trace(go.Scattermapbox(mode='markers',
                                  lat=lat,
                                  lon=lng, 
                                  marker = {'size': 20, 'symbol': symbol_list},
                                  hoverinfo='none',
                                  showlegend=False,
                                  below="",
                                   )
                 )   

    
def get_symbol_transit(response_transit):
    symbol_list = []
    symbol_names = dict(SUBWAY='rail',BUS='bus',TRAM='rail-light')
    json_list = ast.literal_eval(response_transit)
    for json in json_list:
        if json['travel_mode']=='WALKING':
            symbol_list.append('arrow')
        if json['travel_mode']=='TRANSIT':
            type_ = json['type']
            symbol_list.append(symbol_names[type_])
    return symbol_list

def get_base_barplot(origin='baquedano',id_=60):
    
    df = load_data(origin)
    data_dict = {}
    json_list = ast.literal_eval(df.loc[df['id']==id_]['json_transit'].iloc[0])
    type_dict = {'BUS':'Bus','WALKING':'Caminar','SUBWAY':'Metro','TRAM':'Tram'}
    for json in json_list:
        if json['travel_mode']=='WALKING':
            key = type_dict[json['travel_mode']]
            if key in data_dict:
                time_list = data_dict[key]
                time_list += [json['duration']['value']/60.,]
            else:
                data_dict[key] = [json['duration']['value']/60.,]
        if json['travel_mode']=='TRANSIT':
            key = type_dict[json['type']]
            if key in data_dict:
                time_list = data_dict[key]
                time_list += [json['duration']['value']/60.,]
            else:
                data_dict[key] = [json['duration']['value']/60.,]
    cols = ['Type','Bicicleta']+list(data_dict.keys())
    df_route = pd.DataFrame(columns=cols)
    df_route.loc[0,'Type'] = 'Bici'
    df_route.loc[0,'Bicicleta'] = df.loc[df['id']==id_]['time_bike'].values[0]*60.
    df_route.loc[1,'Type'] = 'T. Publico'    
    for key in data_dict:
        df_route.loc[1,key] = sum(data_dict[key])  
    total_transit = df.loc[df['id']==id_]['time_transit'].values[0]*60.
    df_route.loc[1,'Transbordo'] = total_transit-df_route.iloc[1,1:].sum(axis=0)
    df_route = df_route.fillna(0)
    df_route = df_route.round(2)
    
    barfig = px.bar(df_route,
                    x="Type",
                    y=df_route.columns.values[1:],
                    labels={'Type':'','value':'Tiempo (minutos)'},
                    hover_data = {'Type':False}
                   )
    barfig.update_layout(title={'font':{'size':12}},
                         legend_title="",
                        )
    return barfig

        
# Base choropleth layer --------------#
def get_fig(map_type,origin):
    
    if map_type != current_map['map_type'] or origin != current_origin['origin']:
        current_map['map_type'] = map_type
        current_origin['origin'] = origin
        selection.clear()
        global fig
        fig = make_base_map(map_type,origin)
        add_origin(fig,origin)
    
    if len(selection) > 0:
        for idx in range(0,len(fig.data)):
            if idx==0: continue
            fig.data[idx].visible=False
        
        #######################  Bike Route ########################
        df = load_data(origin)
        lat,lng = get_routes(df.loc[df['id']==selection[-1]]['json_bike'].iloc[0])
        new_trace('Ruta Bici','blue',lat,lng)     
        #######################  Metro Route ########################
        lat,lng = get_routes(df.loc[df['id']==selection[-1]]['json_transit'].iloc[0])
        new_trace('Ruta Transporte Publico','red',lat,lng)
        lats,lngs = get_starts(df.loc[df['id']==selection[-1]]['json_transit'].iloc[0])
        add_symbol(lats,lngs,get_symbol_transit(df.loc[df['id']==selection[-1]]['json_transit'].iloc[0]))        
        
        fig.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01))        
        
    return fig

def get_infoplot(origin):
    
    if len(selection)>0:
        fig = get_base_barplot(origin,selection[-1])
    else:
        fig = get_linefig(origin,rolling=200)
    fig.update_layout(margin={"r":20,"l":20,"b":20,"t":20},
                      width=400,
                      height=250
                     )
    return fig

def get_linefig(origin='baquedano',rolling=100):
    
    df_ = load_data(origin)
    df = df_[['dist_meters','time_bike','time_transit']].sort_values('dist_meters').rolling(rolling).median()
    std = df_[['dist_meters','time_bike','time_transit']].sort_values('dist_meters').rolling(rolling).std()
    x,y = df.dist_meters/1000,df.time_transit
    y_up, y_low = y+std.time_transit, y-std.time_transit
    y2  = df.time_bike
    y2_up, y2_low = y2+std.time_bike, y2-std.time_bike
        
    linefig = go.Figure([go.Scatter(x=x,y=y,mode='lines',hoverinfo="skip",name='T. Publico',line=dict(color='red')),
                    go.Scatter(
                        x=list(x)+list(x[::-1]), # x, then x reversed
                        y=list(y_up)+list(y_low[::-1]), # upper, then lower reversed
                        fill='toself',
                        fillcolor='rgba(100,10,0,0.2)',
                        line=dict(color='rgba(255,255,255,0)'),
                        hoverinfo="skip",
                        showlegend=False
                    ),
                     go.Scatter(x=x,y=y2,mode='lines',hoverinfo="skip",name='Bicicleta',line=dict(color='blue')),
                    go.Scatter(
                        x=list(x)+list(x[::-1]), # x, then x reversed
                        y=list(y2_up)+list(y2_low[::-1]), # upper, then lower reversed
                        fill='toself',
                        fillcolor='rgba(10,0,100,0.2)',
                        line=dict(color='rgba(255,255,255,0)'),
                        hoverinfo="skip",
                        showlegend=False
                    )
                    ])

    linefig.update_layout(
                        legend=dict(
                            x=0.02,
                            y=.97),
                        xaxis_title='Distancia (Km)',
                        yaxis_title='Tiempo Viaje (hr)',
                     )
    return linefig

def get_infotext(origin='baquedano'):
    
    df = load_data(origin)
    if len(selection)>0:
        address_text = df['end_address'].loc[df['id']==selection[-1]].iloc[0]
        t_bike = df['time_bike'].loc[df['id']==selection[-1]].iloc[0]
        t_transit = df['time_transit'].loc[df['id']==selection[-1]].iloc[0]        
        return dbc.Card([
                        dbc.CardBody([
                                    html.P(['Desde: ',html.B(origin_names[origin]),html.Br(),
                                    'Hasta: ',html.B(address_text),html.Br(),
                                    dbc.Row([
                                       dbc.Col(html.P(['Bici: ',html.B(html.H5(str(t_bike)+' hr'))])),
                                       dbc.Col(html.P(['Trans. Publico: ',html.B(html.H5(str(t_transit)+' hr'))]))
                                            ])
                                            ],className='card-text')
                                    ])
                        ],style={'width':'25rem','height':'10rem'})                         
    else:
        ratio = df['time_bike']-df['time_transit']
        perc = round(((sum(ratio<0))/len(ratio))*100.,2)
        return dbc.Card([
                        dbc.CardBody([
                            html.P(['Desde: ',html.B(origin_names[origin]),html.Br(),
                                   'Ruta en Bici es Mas Rapida en el',html.Br(),
                                    html.B(html.H4(str(perc)+'%')),' del Area Urbana'
                                   ])
                                    ],className='card-text')
                        ],style={'width':'25rem','height':'10rem'})
                            
fig = make_base_map()
add_origin(fig)