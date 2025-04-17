from dash import Output, Input, callback, ctx, dcc
from src.components.location_filter import Location_filter
from src.components.seniorhigh_filter import Seniorhigh_filter
from src.components.offering_filter import Offering_filter
from src.components.subclass_filter import Subclass_filter


"""
    Created to get selected primary filter
"""

# # Get the primary filter
@callback(
    Output("location", "className"),
    Output("senior-high", "className"),
    Output("subclass", "className"),
    Output("offering", "className"),
    Input("location", "n_clicks"),
    Input("senior-high", "n_clicks"),
    Input("subclass", "n_clicks"),
    Input("offering", "n_clicks"),
)
def clicked_tab_identifier(n1, n2, n3, n4):
    triggered_id = ctx.triggered_id or "location" # By default location
    active_class = "active tab-btn"
    inactive_class = "tab-btn"

    return tuple(
        active_class if id == triggered_id else inactive_class
        for id in ["location", "senior-high", "subclass", "offering"]
    )
    
    
# reflect which primary filter is selected
@callback(
    Output("filter-header", "children"),
    Output("filter-options", "children"),
    Input("location", "className"),
    Input("senior-high", "className"),
    Input("subclass", "className"),
    Input("offering", "className"),
)
def reflect(in1, in2, in3, in4):
    opt = ["Location", "Senior High", "Subclassification", "Offering"]
    filter = [Location_filter, Seniorhigh_filter, Subclass_filter, Offering_filter]
    
    for idx, val in enumerate([in1, in2, in3, in4]):
        if val.split(" ")[0] == 'active':
            return f"Filter by {opt[idx]}:", filter[idx]()