import json 
import requests
from urllib.request import urlopen
import pandas as pd 
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import dash_bootstrap_components as dbc
import dash
from dash.dependencies import Input, Output
import dash_auth

USERNAME_PASSWORD_PAIRS = [['username','password'],['kopisusu','1998']]

def pprint(string):
  print(json.dumps(string, indent=2))

result = requests.get("http://192.168.18.110:14240/restpp/query/MyGraph/hobby_param")

hasil = json.loads(result.text)
pprint(hasil)
interest =[]
avg_age = []

for item in hasil["results"][0]["tmp"]: 
    interest.append(item['attributes']['interest'])
    avg_age.append(item['attributes']['@avg'])

print (interest,avg_age)


dff = pd.DataFrame({
    "rata2umur": avg_age,
    "hobby": interest,
    
})

#params= {'id':"\"\"error\"\""}

# req =  requests.get("http://192.168.1.90:14240/restpp/query/mygraph/ip_tracking",params=params)


########### INI UNTUK MENGAMBIL DATA DARI RESPP API TIGERGRAPH ###############

with urlopen("http://192.168.18.110:14240/restpp/query/MyGraph/most_followers") as response: 
    data = response.read() 


########### LALU DATA TERSEBUT KITA MASUKAN KEDALAM VARIABLE PYTHON ##################
source = json.loads(data)
f_name=[]
num_follower =[]
print (source)

############# DIMANA KITA HARUS MENGGUNAKAN LOGIC LOOPING UNTUK MEMBUATNYA ############

for a in source['results'][0]['followers']:
    f_name.append(a['attributes']['first_name'])
    num_follower.append (a['attributes']['@num_followers'])
    # print(f_name,num_follower)


############## SETELAH ITU DATA TERSEBUT DI MASUKAN KEDALAM DATAFRAME PANDAS #############
df1 = pd.DataFrame({
    "first_name": f_name,
    "count_follow": num_follower,
    
})


######### INI UNTUK MENGECEK APAKAH DATA TERSEBUT UDAH SIAP UNTUK KITA INPUT KEDALAM PARAMETER DASH ############# 
# print (df1)

print ('===========================================')

def pprint(string):
  print(json.dumps(string, indent=2))

############# INI QUERY KE DUA YANG MEMAKAI PARAMETER DIDALAMNYA ############# 


params = {
  "v_type": "users",
  "e_type": "reffered_by",
  "max_change": 0.001,
  "max_iter": 25,
  "damping": 0.85,
  "top_k": 100,
  "print_accum": True,
  "result_attr": "",
  "file_path": "",
  "display_edges": False 
}

req = requests.get("http://192.168.18.110:14240/restpp/query/MyGraph/pagerank",params=params) 
    
data2 = json.loads(req.text)


q1= data2['results'][0]['@@topScores']
vertex_id= []
score = []

# print (q1)
for i in q1:
    vertex_id.append(i['Vertex_ID'])
    score.append(i['score'])
    # print (vertex_id,score)

df = pd.DataFrame({
    "v_id": vertex_id,
    "val_score": score,
})

print(df)
print(df1)
# df=pd.DataFrame(q1)

# df = pd.DataFrame(req)
# print (df)


############ INI KITA MEMASUKAN DATA YANG SUDAH KITA BUAT KEDALAM DATAFRAME UNTUK SIAP DI VISUALISASIKAN ######


fig = px.bar(df1, x="first_name", y="count_follow", color="first_name")
fig1 = px.bar( df, x = "v_id", y= "val_score", )
fig3= px.pie (dff,values= "rata2umur",color_discrete_map= "hobby",names="hobby",)


###### MULAI DARI SINI KITA MEMBUAT LAYOUT UNTUK MEMBUAT SEBUAH VISUALISASI ##########


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO],suppress_callback_exceptions=True)
# app = dash.Dash(__name__)
auth = dash_auth.BasicAuth(app,USERNAME_PASSWORD_PAIRS)
# 

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

fig3.update_layout (
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

fig.update_layout (
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

fig1.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

PLOTLY_LOGO = "https://i.ibb.co/9Vp8QKx/Untitled-design-9-1.png"
titlecard = dbc.Card([
  dbc.CardBody([
    dbc.Row([dbc.Col(html.Center(html.H1("VISUALISASI VIRTUAL-BOX")),style={'fontColor':'text'}),
    dbc.Col(html.Img(src=PLOTLY_LOGO, width="225px" ,style={"right":0,"margin-bottom": "14px",}))]),
  ])
], color="#ff9100",
   style={
     "width":"70rem",
     "margin-top":"1rem",
     "margin-bottom":"1rem",
     "margin-right":"0rem"

   })


piechartcard = dbc.Card([
  dbc.CardBody([
    html.H1("Rata-Rata Umur hobby", className='card-title'),
    html.P("", className='card-body'),
    html.Label(['Choose column:'],style={'font-weight': 'bold'}),
    dbc.DropdownMenuItem(dcc.Dropdown(id="dropdown",multi= True,
       options=[{'label':x,'value': x}for x in sorted(dff.hobby)],
       value= ["running","karaoke"],),style={"width":"65rem","color":"#014c63"}),
    html.Br(),
    dcc.Graph(id='graph', figure= {},),
  ])
],
  outline=True,
  color='secondary',
  style={
    "width":"71rem",
    "margin-right":"0rem",
    "margin-left":"1rem",
    "margin-bottom":"1rem"
  }
)

markdown = ''' Most Follower
            Grafik Diatas merupakan hasil Dari algoritma Query
            untuk menghitung berapa user account yang mempunyai follower terbanyak 
            Grafik ini merupakan hasil dari Graph Schema social media
            yang dimana merepresentasikan keterhubungan antar user account
  '''
# piechartcard = dbc.Card([
#   dbc.CardBody([  
#     html.H1("Rata-Rata Umur hobby", className='card-title'),
#     html.P("", className='card-body'),
#     dcc.Graph(id='graph', figure= fig3)
#   ])
# ],
#   outline=True,
#   color='secondary',
#   style={
#     "width":"70rem",
#     "margin-right":"0rem",
#     "margin-left":"2rem",
#     "margin-bottom":"1rem"
#   }
# )

bar = html.Div([html.Header("Most Followers"),
                dcc.Graph(id='bar', figure= fig)
              ])

bar1 = html.Div([html.Header("PageRank"),
                 dcc.Graph(id='barchart' ,figure=fig1)
])

barchartcard = dbc.Card([
  dbc.CardBody([
    html.H1("Most Followers", className='card-title'),
    html.P("", className='card-body'),
    dcc.Graph(id='bar', figure= fig)
  ])
],
  outline=True,
  color='secondary',
  style={
    "width":"35rem",
    "margin-right":"0rem",
    "margin-left":"1rem",
    "margin-bottom":"1rem"
  }
)

barchartcard1 = dbc.Card([
  dbc.CardBody([
    html.H1("Algoritma Pagerank", className='card-title'),
    html.P("", className='card-body'),
    dcc.Graph(id='barchart', figure= fig1)
  ])
],
  outline=True,
  color='secondary',
  style={
    "width":"35rem",
    "margin-right":"0rem",
    "margin-left":"1rem",
    "margin-bottom":"1rem"
  }
)
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#424242",
}

WHITE = "#fffff8"
TG_LOGO = "https://i.pinimg.com/originals/98/c7/e9/98c7e95ea1207eef6f70f0ae9e694e67.png"
sidebar =dbc.Card([html.Div(
    [
        html.H2("Main Menu", className="display-5"),
        html.Hr(),
        html.Label(
            "TigerGraph as a GraphDatabase", className="display-6"
        ),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Page 1", href="/page-1", active="exact"),
                dbc.NavLink("Page 2", href="/page2", active="exact"),
                dbc.NavLink("Page 3", href="/page3", active="exact"),
            ],
            vertical=True,
            pills=True,
            
        ),
        html.Hr(),
        html.Li(html.A("Inroduction to Graphs", href='https://www.tigergraph.com/blog/what-is-a-graph-database-and-why-should-you-care/', target="_blank", style={'color':WHITE}), style={'color':WHITE}),
        html.Br(),
        html.Li(html.A("Introduction to Dash", href='https://www.youtube.com/watch?v=e4ti2fCpXMI', target="_blank", style={'color':WHITE}), style={'color':WHITE}),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Label(["Achmad Irfandi Darmawan"],style= {"fontcolor":"black"})
    ],
    style=SIDEBAR_STYLE,
    className="card"
)])


page = html.Center(html.Div([
  titlecard,
  dbc.Row([barchartcard,
    barchartcard1,piechartcard
  ],justify='center'),
  
]
, style={"width":"90rem"}))


# page1 = html.Center(html.Div([
#   titlecard,
#   dbc.Row(dbc.Col([
#     bar
#   ],width={'size': 12, "offset": 0}),)
  
# ]
# , ))



page1 =dbc.Card([
        dbc.CardBody([
        html.H1("Most Follower", className='card-title'),
        html.P("", className='card-body'),
        bar,
        html.Div([html.Label(dcc.Markdown(children=markdown),className="display-5")])
          ])
        ],outline=True,
  color='info',
  style={
    "width":"89rem",
    "margin-right":"1rem",
    "margin-left":"18rem",
    "margin-bottom":"1rem",
    "margin-top":"5rem"
  }),

page2 =dbc.Card([
        dbc.CardBody([
        html.H1("PageRank", className='card-title'),
        html.P("", className='card-body'),
        bar1,
        html.Div()
          ])
        ],outline=True,
  color='info',
  style={
    "width":"89rem",
    "margin-right":"1rem",
    "margin-left":"18rem",
    "margin-bottom":"1rem",
    "margin-top":"5rem"
  }),
dcc.Markdown('''# Most Follower

               ## Grafik Diatas merupakan hasil Dari algoritma Queri
               untuk menghitung berapa user account yang mempunyai 
               follower terbanyak 

               ## Grafik ini merupakan hasil dari Graph Schema social media
               yang dimana merepresentasikan keterhubungan antar user account
  ''')

# page2= html.Center(html.Div([
#   titlecard,
#   dbc.Row([
#     barchartcard1,
#   ],justify='center'),
  
# ]
# , style={"width":"90rem"}))

page3= html.Center(html.Div([
  
  dbc.Row([
    piechartcard,
  ],justify='center'),
  
]
, style={"width":"90rem"}))




CONTENT_STYLE = {
    "margin-left": "2rem",
    "margin-right": "0rem",
    "padding": "1rem 1rem",
}

# app.layout= html.Div([
#   sidebar,
#   html.Div(page),
  
  
# ])


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    sidebar, 
    html.Div(id='page-content', style=CONTENT_STYLE)
])



@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')],suppress_callback_exceptions=True)

def display_page(pathname):
  if pathname == "/": 
    return page
  elif pathname == "/page-1": 
    return page1
  elif pathname == "/page2": 
    return page2
  elif pathname == "/page3": 
    return page3


@app.callback(Output(component_id="graph", component_property='figure'),
[Input(component_id='dropdown', component_property='value')],suppress_callback_exceptions=True)

def update_my_graph(val_chosen):
  if len(val_chosen)>0:
    print(f"value user choose:{val_chosen}")
    print (type(val_chosen))
    dff1 = dff[dff["hobby"].isin(val_chosen)]
    pig = px.pie(dff1,values="rata2umur", names="hobby")
    pig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)
    return pig


# style= CONTENT_STYLE

if __name__ == '__main__':
    app.run_server(debug=True)

