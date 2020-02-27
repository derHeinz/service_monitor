import os
import datetime

class HTMLTableExporter(object):

    TABLE_ROW_CONTENT = '<tr><td>{column_1}</td><td>{column_2}</td></tr>'

    def __init__(self, **kwargs):
        self.filename = kwargs['filename']
        if 'template' in kwargs:
            self.template = kwargs['template']
        else:
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
    
    def create_table_row(self, service_name, service_state):
        return self.TABLE_ROW_CONTENT.format(column_1=service_name, column_2=service_state)
        

    def export(self, service_names, service_states):
    
        template = self.load_template()
        # replacer = 'rows' and 'updated'
        all_rows = []
    
        for i in range(len(service_names)):
            curr_name = service_names[i]
            curr_state = service_states[i]
            state_string = self.create_state_string(curr_state)
            single_row = self.create_table_row(curr_name, state_string)
            all_rows.append(single_row)
            
        rows_text = "\n".join(all_rows)
        
        now = datetime.datetime.now()
        current_time = now.strftime("%d.%m.%Y %H:%M")
        
        file_text = template.format(rows=rows_text, updated=current_time)
        with open(self.filename, 'w') as outfile:
            outfile.write(file_text)
        
