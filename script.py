import pandas as pd
import plotly.express as px
import dash
from dash import  dcc
from dash import  html
from dash.dependencies import Input, Output


df = pd.read_csv('/home/ubuntu/Scrap/resultat.txt', sep=';', header=None, names = ['Timestamp', 'Price'])

df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%Y-%m-%d %H:%M:%S')
df['Price'] = df['Price'].str.replace(',', '.').astype(float)


# Filtrer les données pour ne conserver que celles du dernier jour

last_day = df.loc[df['Timestamp'].dt.date == df['Timestamp'].dt.date.unique()[-2]]

# Calculer la moyenne, le min, le max et la volatilité
mean_price = last_day['Price'].mean()
min_price = last_day['Price'].min()
max_price = last_day['Price'].max()
volatility = last_day['Price'].std()
first_price = last_day['Price'].iloc[0]
last_price = last_day['Price'].iloc[-1]
spread_price = round ( max_price - min_price, 4) 


EURtoUSD = "1 € = " + str(round(mean_price,4)) + " $"
USDtoEUR = "1 $ = " + str(round (1/ mean_price , 4 )) + " €"

pr = "EUR/USD SPOT : " + str(df['Price'].iloc[-1])
dsd = "Daily summary : " + last_day['Timestamp'].iloc[1].strftime("%A %d %B %Y")


# Define colors for the app
colors = {
    'background': '#F0F0F0',
    'text': '#333333',
    'primary': '#006699',
    'secondary': '#cccccc'
}

# Create the Dash app
app = dash.Dash(__name__)
app.title = 'EUR/USD Dashboard'
app.layout = html.Div( style={ 'fontFamily': 'Arial'}, children=[    
    html.H1(children='Exchange Rate Euro Dollar', style={'textAlign': 
                                                        'center', 
                                                        'color': colors['primary'], 
                                                        'marginTop':'50px', 
                                                        'marginBottom':'10px'}),
   html.H3(children= pr  , style={'textAlign':'center',
                                             'color': colors['primary'],

                                               'marginTop':'0px',
                                               'marginBottom':'0px'}),

    html.Div([        
        html.H2("Graphique", style={'color': colors['primary'], 
                                    'borderBottom': '2px solid ' + colors['primary'], 
                                    'paddingBottom': '10px'}),
        dcc.Graph(id='graphique'),
        dcc.Interval(id='interval-component', interval=5*60*1000, n_intervals=0),
    ], style={'margin': '30px'}),

    
    html.Div([        
        html.H2(dsd , style={'color': colors['primary'], 
                                        'borderBottom': '2px solid ' + colors['primary'], 
                                        'paddingBottom': '10px', 
                                        'marginTop': '0px'
                                        }),
        html.Table(children=[
            html.Td(children=[
        html.Table(children=[            
            html.Tr(children=[                
                html.Td(children='Average', style={'borderBottom': '1px solid ' + colors['secondary'], 
                                                   'padding': '10px'}),
                html.Td(children=round(mean_price, 4), style={'borderBottom': '1px solid ' + colors['secondary'], 
                                                              'padding': '10px'}),
                
                
                
                ]),
            html.Tr(children=[                
                html.Td(children='Lowest', style={'borderBottom': '1px solid ' + colors['secondary'], 
                                                   'padding': '10px'}),
                html.Td(children=round(min_price, 4), style={'borderBottom': '1px solid ' + colors['secondary'], 
                                                             'padding': '10px'})
                ]),
            html.Tr(children=[                
                html.Td(children='Highest', style={'borderBottom': '1px solid ' + colors['secondary'], 
                                                                                 'padding': '10px'}),
                html.Td(children=round(max_price, 4), style={'borderBottom': '1px solid ' + colors['secondary'], 
                                                             'padding': '10px'})
                ]),
            
            
            html.Tr(children=[                
                html.Td(children='Volatility', style={'padding': '10px'}),                
                html.Td(children=round(volatility, 4), style={'padding': '10px'})
                ]),
            
            ] , style={'padding-left': '300px', 'padding-right': '130px'} ,className='six columns' ),
        ]),
         html.Td(children=[
        html.Table(children=[            
            html.Tr(children=[                
                html.Td(children='Open', style={'textAlign':'center','borderBottom': '1px solid ' + colors['secondary'], 
                                                   'padding': '10px'}),
                html.Td(children=first_price, style={'textAlign':'center','borderBottom': '1px solid ' + colors['secondary'], 
                                                              'padding': '10px'}),
                
               
                
                ]),
            html.Tr(children=[                
                html.Td(children='Closed', style={'textAlign':'center', 'borderBottom': '1px solid ' + colors['secondary'], 
                                                   'padding': '10px'}),
                html.Td(children= last_price , style={'textAlign':'center','borderBottom': '1px solid ' + colors['secondary'], 
                                                             'padding': '10px'})
                ]),
            html.Tr(children=[                
                html.Td(children='Spread', style={'textAlign':'center','borderBottom': '1px solid ' + colors['secondary'], 
                                                                                 'padding': '10px'}),
                html.Td(children=spread_price , style={'textAlign':'center','borderBottom': '1px solid ' + colors['secondary'], 
                                                             'padding': '10px'})
                ] ),
            
            
            html.Tr(children=[                
                html.Td(children= EURtoUSD , style={'padding': '10px'}),                
                html.Td(children= USDtoEUR , style={'padding': '10px'})
                ]),
            
           ], style={'padding-left': '130px', 'padding-right': '100px'}, className='six columns'),
        
        
        ])
         ])
        
    ] , style={'margin': '30px'} ), 
    
])

@app.callback(
    Output(component_id='graphique', component_property='figure'),
    [Input(component_id='interval-component', component_property='n_intervals')]
)

def update_graph(n):
    # Read the CSV file inside the update_graph function
    df = pd.read_csv('/home/ubuntu/Scrap/resultat.txt', sep=';', header=None, names=['Timestamp', 'Price'])

    # Filtrer les données pour ne conserver que celles du dernier jour
    last_day = df.loc[df['Timestamp'].dt.date == df['Timestamp'].dt.date.unique()[-2]]
    # Calculer la moyenne, le min, le max et la volatilité
    mean_price = last_day['Price'].mean()
    min_price = last_day['Price'].min()
    max_price = last_day['Price'].max()
    volatility = last_day['Price'].std()
    first_price = last_day['Price'].iloc[0]
    last_price = last_day['Price'].iloc[-1]
    spread_price = round(max_price - min_price, 4)

    EURtoUSD = "1 € = " + str(round(mean_price, 4)) + " $"
    USDtoEUR = "1 $ = " + str(round(1 / mean_price, 4)) + " €"

    pr = "EUR/USD SPOT : " + str(df['Price'].iloc[-1])
    dsd = "Daily summary : " + last_day['Timestamp'].iloc[1].strftime("%A %d %B %Y")


    # Update the layout
    fig.update_layout(
        xaxis=dict(
            rangeslider=dict(visible=True),
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all")
                ])
            )
        )
    )

    return fig

if __name__ == '__main__':
    app.run_server(host = "0.0.0.0",port = 8050, debug=True )

