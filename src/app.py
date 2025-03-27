import plotly.express as px
import dash
from dash import Dash, dcc, html, Output, Input

# Main Applications
app = Dash(__name__, use_pages=True)

app.layout = html.Div(
    children=[
        # navigation style
        html.Div([
            
        ], className='nav-header'),
        
        # output: layout pages
        html.Div([
            dash.page_container
        ], className='content-wrapper')
    ],
    
    className= "app-container"
)

# Run the script
if __name__ == '__main__':
    app.run(debug=True)