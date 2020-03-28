import os
from collections import defaultdict
import datetime

from . htmlexporter import HTMLExporter

class HTMLMetroExporter(HTMLExporter):

    BG_CLASSES = ['bg-cyan', 'bg-brown', 'bg-teal', 'bg-indigo']

    def __init__(self, **kwargs):
        super(HTMLMetroExporter, self).__init__(**kwargs)
        if 'template' in kwargs:
            self.template = kwargs['template']
        else:
            ############################ TODO ###########################
            self.template = os.path.dirname(__file__) + '/htmlmetroexporter.html'
        self.bg_tile_class_ind = 0

    def _bg_tile_class(self):
        return self.BG_CLASSES[self.bg_tile_class_ind]
        
    def _bg_tile_class_inc(self):
        self.bg_tile_class_ind += 1
        self.bg_tile_class_ind = self.bg_tile_class_ind%len(self.BG_CLASSES)
    
    def group_start(self, groupname):
        self.bg_tile_class_ind = 0
        return '<div class="tiles-grid tiles-group size-2" data-group-title="{}">'.format(groupname)
        
    def group_end(self, groupname):
        return '</div>'

    def no_groups_start(self):
        return '<div class="tiles-grid tiles-group size-2" data-group-title="Services">'
        
    def no_groups_end(self):
        return '</div>'
        
    def _create_state_string(self, val):
        if val==True:
            return '<span class="tally success"><span class="mif-checkmark"></span> online</span>'
        elif val==False:
            return '<span class="tally alert"><span class="mif-blocked"></span> offline</span>'
        else:
            return '<span class="tally warning"><span class="mif-question"></span> error</span>'
    
    def item_entry(self, service_name, service_state, service_state_checker_type, service_info, service_info_type, service_exporter_hints):

        tile_class = self._bg_tile_class()
        self._bg_tile_class_inc()
        
        pre_content = ''
        post_content = ''
        tile_content = f'<p class="text-center text-small">{service_info}</p>'
        if service_exporter_hints and service_exporter_hints.get('metro_tile_icon'):
            tile_content = '<span class="{icon} icon"></span>'.format(icon=service_exporter_hints['metro_tile_icon'])
            pre_content = f'<span data-role="hint" data-hint-text="{service_info}" data-cls-hint="{tile_class} fg-white drop-shadow">'
            post_content = '</span>'

        service_state_string = self._create_state_string(service_state)
        
        return f'''
        <div data-role="tile" data-hint-text="{service_info}" class="{tile_class}">
            {pre_content}
            <h5 class="text-center">{service_name}</h5>
            
            {tile_content}
            
            <span class="branding-bar">
                {service_state_string}
            </span>
            {post_content}
         </div>
        '''
