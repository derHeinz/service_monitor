import unittest
import json

from . compoundexporter import CompoundExporter

class TestCompoundExporter(unittest.TestCase):

    def test_instantiate_others(self):
    
        cfg_str = '''
        {
        "exporters": {
                "HTMLDefaultExporter": {
                    "type": "exporter.htmltableexporter.HTMLTableExporter",
                    "args": {
                        "filename": "service_states.html",
                        "group_headers": true
                    }
                },
                "HTMLMetroExporter": {
                    "type": "exporter.htmlmetroexporter.HTMLMetroExporter",
                    "args": {
                        "filename": "service_states2.html",
                        "group_headers": true
                    }
                }
            }
        }
        '''
        cfg = json.loads(cfg_str)
        t = CompoundExporter(**cfg)
        
        