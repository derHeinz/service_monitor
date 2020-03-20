import os
from collections import defaultdict
import datetime

class HTMLTableExporter(object):

    TABLE_GROUP_CONTENT = '<tr><th colspan="3">{group}</th></tr>'
    TABLE_ROW_CONTENT = '<tr><td>{column_1}</td><td>{column_2}</td><td>{column_3}</td></tr>'

    def __init__(self, **kwargs):
        self.filename = kwargs['filename']
        self.group_headers = kwargs.get('group_headers', False)
        if 'template' in kwargs:
            self.template = kwargs['template']
        else:
            ############################ TODO ###########################
            self.template = os.path.dirname(__file__) + '/htmltableexporter.html'
            
    def load_template(self):
        with open(self.template) as template_file:    
            data = template_file.read()
            return data

    def create_state_string(self, val):
        if val:
            return "<b style=\"color:green;\">{text}</b>".format(text="online")
        else:
            return "<b style=\"color:red;\">{text}</b>".format(text="offline")
    
    def create_group_header(self, groupname):
        return self.TABLE_GROUP_CONTENT.format(group=groupname)
    
    def create_table_row(self, service_name, service_state, service_info):
        return self.TABLE_ROW_CONTENT.format(column_1=service_name, column_2=service_state, column_3=service_info)

    def export(self, service_info_array):
    
        template = self.load_template()
        content_lines = []
        
        res = defaultdict(list)
        for i in service_info_array: res[i['service_group']].append(i)

        for service_group in res:
            if self.group_headers:
                content_lines.append(self.create_group_header(service_group))
            for item in res[service_group]:
                service_name = item['service_name']
                service_state = self.create_state_string(item['service_state'])
                service_info = item.get('service_info', None)
                content_lines.append(self.create_table_row(service_name, service_state, service_info))

        content_text = "\n".join(content_lines)
        
        now = datetime.datetime.now()
        current_time = now.strftime("%d.%m.%Y %H:%M")
        
        file_text = template.format(content=content_text, updated=current_time)
        with open(self.filename, 'w') as outfile:
            outfile.write(file_text)
        