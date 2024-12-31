import os
from collections import defaultdict
import datetime
import logging

import shutil

logger = logging.getLogger(__file__)


class HTMLExporter(object):

    def __init__(self, **kwargs):
        self.filename = kwargs['filename']
        self.group_headers = kwargs.get('group_headers', False)
        if 'template' in kwargs:
            self.template = kwargs['template']
        else:
            self.template = os.path.join(os.path.dirname(__file__), self.default_template_filename())

    def default_template_filename(self):
        return 'htmlexporter.html'

    def load_template(self):
        with open(self.template) as template_file:    
            data = template_file.read()
            return data

    def group_start(self, groupname):
        return ""

    def group_end(self, groupname):
        return ""

    def no_groups_start(self):
        return ""

    def no_groups_end(self):
        return ""

    def item_entry(self, service_name, service_state, service_state_checker_type,
                   service_info, service_info_type, service_exporter_hints):
        return ""

    def additional_files(self):
        pass

    def export_additional_files(self):
        if not self.additional_files():
            return
        # write out additional files
        dir_to_write_to = os.path.dirname(self.filename)
        logger.debug(f"dir {dir_to_write_to}.")
        for filename in self.additional_files():
            src = os.path.join(os.path.dirname(__file__), filename)
            dst = os.path.join(dir_to_write_to, filename)
            logger.debug(f"copy {src} to {dst}.")
            shutil.copyfile(src, dst)

    def export(self, service_info_array):

        template = self.load_template()
        content_lines = []

        res = defaultdict(list)
        for i in service_info_array: 
            res[i['service_group']].append(i)

        if not self.group_headers:
            content_lines.append(self.no_groups_start())

        for service_group in res:
            if self.group_headers:
                content_lines.append(self.group_start(service_group))

            for item in res[service_group]:
                service_name = item['service_name']
                service_state = item['service_state']
                service_info = item.get('service_info', "no info available")
                service_state_checker_type = item['checker_type']
                service_info_type = item.get('info_type', "no type available")
                service_exporter_hints = item['service_config'].get('exporter_hints', None)

                content_lines.append(self.item_entry(service_name, service_state, service_state_checker_type, service_info, service_info_type, service_exporter_hints))

            if self.group_headers:
                content_lines.append(self.group_end(service_group))

        if not self.group_headers:
            content_lines.append(self.no_groups_end())

        content_text = "\n".join(content_lines)

        now = datetime.datetime.now()
        current_time = now.strftime("%d.%m.%Y %H:%M")

        file_text = template.format(content=content_text, updated=current_time)
        with open(self.filename, 'w') as outfile:
            outfile.write(file_text)

        self.export_additional_files()
