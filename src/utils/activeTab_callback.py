from dash import Output, Input, callback, dcc
import dash


"""
    Created to store current tab location.
    Also, meant to retrieve current routing page
"""


# Store the current pathname when the page changes
@callback(
    Output("active-tab", "data"),
    Input("url", "pathname")
)
def update_active_tab(pathname):
    return pathname  # Save the current route 


# Restore the active tab on refresh
@callback(
    Output("nav-1", "className"),
    Output("nav-2", "className"),
    Output("nav-3", "className"),
    Output("opt-1", "className"),
    # Output("opt-2", "className"),
    Output("opt-3", "className"),
    Input("active-tab", "data")  # Get the stored route
)
def restore_active_tab(activeTab):
    return [
        "item-ctn active" if activeTab == "/" else "item-ctn",
        "item-ctn active" if activeTab == "/analytics" else "item-ctn",
        "item-ctn active" if activeTab == "/school-level" else "item-ctn",
        "item-ctn active" if activeTab == "/updates" else "item-ctn",
        # "item-ctn active" if activeTab == "/help" else "item-ctn",
        "item-ctn active" if activeTab == "/settings" else "item-ctn",
    ]