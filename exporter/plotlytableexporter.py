import plotly.graph_objects as go
import logging

class PlotlyTableExporter(object):

    def __init__(self, **kwargs):
        self.filename = kwargs['filename']

    def create_state_string(self, val):
        if val:
            return "<b style=\"color:green;\">{text}</b>".format(text="online")
        else:
            return "<b style=\"color:red;\">{text}</b>".format(text="offline")

    def export(self, service_names, service_states):
        # calculate text for states
        service_states_display = list(map(lambda ss: self.create_state_string(ss), service_states))
        fig = go.Figure(data=[go.Table(header=dict(values=['<b>Servicename</b>', '<b>State</b>']), cells=dict(values=[service_names, service_states_display]))])
        logging.debug("attempting to write file '{}'".format(self.filename))
        fig.write_html(self.filename, auto_open=True)
