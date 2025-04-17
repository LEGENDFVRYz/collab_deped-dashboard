from dash import Output, Input, callback, ctx, dcc


# reflect which primary filter is selected
@callback(
    Output("analytics-sub-tracker", "data"),
    Input("location", "className"),
    Input("senior-high", "className"),
    Input("subclass", "className"),
    Input("offering", "className"),
)
def save_analytic_tabs(in1, in2, in3, in4):
    opt = ["Location", "Senior High", "Subclassification", "Offering"]
    
    for idx, val in enumerate([in1, in2, in3, in4]):
        if val.split(" ")[0] == 'active':
            print(opt[idx])
            return opt[idx]