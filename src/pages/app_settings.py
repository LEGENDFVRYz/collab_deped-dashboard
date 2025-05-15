import dash
import base64
import os, sys
from dash import dcc, html
from dash import Input, Output, State, callback
from pipelines.log_store import log_messages
from src.data import enrollment_db_engine, smart_filter
from src.server import cache

# --  Shared Components
from src.components.card import Card
from pipelines.pipeline import mine_data



# Landing page
dash.register_page(__name__, path="/settings", suppress_callback_exceptions=True)  

layout = html.Div([
    html.Div(
        [
            ## -- Standard: Page Content Header
            html.Div([
                html.H1('DashApp Settings')
            ], className='page-header'),
            
            
            html.Div([
                
                ## DROP FILES
                html.Div([Card(
                    [
                        html.H3("Upload Flatfiles:"),
                        
                        dcc.Upload(
                            id='upload-data',
                            children=html.A([
                                'Drag and Drop or Select Files'
                            ]),
                            # Allow multiple files to be uploaded
                            multiple=True
                        ),
                        html.Div(id='upload-status', children='Waiting for upload...'),
                        html.Div(id='output-upload'),
                        
                        # Confirmation Details
                        html.Div([
                            html.Button('PROCEED', id='push-upload'),
                        ], className='confirm-upload')
                    ]
                , padding='1.5em')], className='drop-section'),
                
                ## REPORT UPLOADING AND CONTROLS
                html.Div(
                    [
                        # html.Div([
                            dcc.Interval(id="log-interval", interval=1000, n_intervals=0, disabled=False),
                            html.Pre(
                                id="log-output",
                                style={
                                    "whiteSpace": "pre-wrap",
                                    "border": "1px solid #ccc",
                                    "padding": "20px",
                                    "backgroundColor": "#f9f9f9",
                                    "color": "#333",  # dark gray text
                                    "fontFamily": "monospace",
                                    "fontSize": "14px",
                                    "borderRadius": "5px",
                                    "flex": "1",
                                    "overflowY": "auto",
                                    "maxHeight": "700px",  # corrected syntax
                                    "minHeight": "150px",
                                    "display": "flex",
                                    "flexDirection": "column",
                                }
                            )
                        # ])
                        
                    ]
                , className='report-section'),
            
            ], className='content-wrap')
        ]
    , className='content'),
], className='app-settings container')


@callback(
    Output('output-upload', 'children'),
    Output('upload-status', 'children'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    prevent_initial_call=True
)
def handle_upload(contents, filenames):
    if contents:
        # for content, name in zip(contents, filenames):
        #     save_file(name, content)
        return (
            html.Ul([html.Li(f"{name} uploaded.") for name in filenames]),
            "✅ File uploaded!"
        )
    return "", "Waiting for upload..."




@callback(
    Output('output-upload', 'children', True),
    Output('upload-status', 'children', True),
    Input('push-upload', 'n_clicks'),
    State('upload-data', 'contents'),
    State('upload-data', 'filename'),
    prevent_initial_call=True
)
def upload_file(n_clicks, contents, filenames):
    if not contents or not filenames:
        return "", "⚠️ No file selected."

    # Ensure contents and filenames are lists
    if isinstance(contents, str):
        contents = [contents]
        filenames = [filenames]

    saved_files = []
    upload_dir = os.path.join(os.getcwd(), "database", "raw")
    os.makedirs(upload_dir, exist_ok=True)

    for content, filename in zip(contents, filenames):
        data = content.split(',')[1]
        filepath = os.path.join(upload_dir, filename)
        with open(filepath, 'wb') as f:
            f.write(base64.b64decode(data))
        saved_files.append(filename)

    mine_data()
    cache.delete_memoized(smart_filter, filter_info={}, _engine=enrollment_db_engine)

    return (
        html.Ul([html.Li(f"✅ {name} uploaded to /src/data") for name in saved_files]),
        "✅ File(s) uploaded!"
    )
    
    


@callback(
    Output("log-output", "children"),
    Input("log-interval", "n_intervals")
)
def update_log(n):
    return "\n".join(log_messages)