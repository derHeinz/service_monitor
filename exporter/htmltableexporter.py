from . htmlexporter import HTMLExporter


class HTMLTableExporter(HTMLExporter):

    TABLE_GROUP_CONTENT = '<tr><th colspan="3">{group}</th></tr>'
    TABLE_ROW_CONTENT = '<tr><td>{column_1}</td><td title="{column_2_tooltip}">{column_2}</td><td title="{column_3_tooltip}">{column_3}</td></tr>'

    def __init__(self, **kwargs):
        super(HTMLTableExporter, self).__init__(**kwargs)

    def default_template_filename(self):
        return 'htmltableexporter.html'

    def create_state_string(self, val):
        if val is True:
            return "<b style=\"color:green;\">{text}</b>".format(text="online")
        elif val is False:
            return "<b style=\"color:red;\">{text}</b>".format(text="offline")
        else:
            return "<b style=\"color:orange;\">{text}</b>".format(text=str(val))

    def group_start(self, groupname):
        return self.TABLE_GROUP_CONTENT.format(group=groupname)

    def item_entry(self, service_name, service_state, service_state_checker_type, service_info, service_info_type, service_exporter_hints):
        service_state_string = self.create_state_string(service_state)
        return self.TABLE_ROW_CONTENT.format(column_1=service_name, column_2=service_state_string, column_2_tooltip=service_state_checker_type, column_3=service_info, column_3_tooltip=service_info_type)
