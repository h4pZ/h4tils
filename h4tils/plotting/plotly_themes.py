import plotly.graph_objects as go
import plotly.io as pio

hibm = dict(layout=go.Layout(font=dict(family="IBM Plex Mono", size=12, color="#ffffff"),
                             title_font=dict(color="#ffffff"),
                             colorway=['#f60157',
                                       '#0157f6',
                                       '#fcfc50',
                                       '#99ffcc',
                                       '#00C3F1',
                                       '#FFFFFF',
                                       '#607889',
                                       '#70396a'],
                             paper_bgcolor="#171616",
                             plot_bgcolor="#171616",
                             xaxis=dict(zerolinecolor="#ffffff",
                                        gridcolor="#272829"),
                             yaxis=dict(zerolinecolor="#ffffff",
                                        gridcolor="#272829")))

pio.templates["hibm"] = go.layout.Template(hibm)

