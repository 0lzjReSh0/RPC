from xmlrpc.server import SimpleXMLRPCServer
import xml.etree.ElementTree as ET
import requests
import xml.dom.minidom
import sys
import re
from datetime import datetime
from socketserver import ThreadingMixIn

class ThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass

def prettiXml(content):
    init = ET.tostring(content, 'utf-8')
    reparsed = xml.dom.minidom.parseString(init)
    p_xml = reparsed.toprettyxml(indent="  ")
    p_xml = re.sub(r'^\s*\n', '', p_xml, flags=re.MULTILINE)
    return p_xml

class NoteServer:
    def __init__(self):
        self.xmldb = "db.xml"
        try:
            self.tree = ET.parse(self.xmldb)
            self.root = self.tree.getroot() 
            
        except Exception as ex:
            print("Exception:",ex)
            root = ET.Element("data")
            self.tree = ET.ElementTree(root)
            self.root = root
            self.tree.write(self.xmldb)
            

    
    def add_note(self, topic, text, timestamp):
        
        for i in self.root.findall('topic'):
            
            if i.get('name') == topic:
                
                new_note = ET.SubElement(i, "note")
                new_note.set('name', text[:25])
                ET.SubElement(new_note, "text").text = text
                ET.SubElement(new_note, "timestamp").text = timestamp
                with open(self.xmldb, "w+") as f:
                    f.write(prettiXml(self.root))
                return True
                

        new_topic = ET.SubElement(self.root, "topic")
        new_topic.set('name', topic)
        
        new_note = ET.SubElement(new_topic, "note")
        new_note.set('name', text[:25])
        
        ET.SubElement(new_note, "text").text = text
        ET.SubElement(new_note, "timestamp").text = timestamp
        
        with open(self.xmldb, "w+") as f:
            f.write(prettiXml(self.root))
        return True
        
    
    def get_notes(self, topic):
        
        notes = []
        for elem in self.root.findall('topic'):
            if elem.get('name') == topic:
                for note in elem.findall('note'):
                    notes.append({'text': note.find('text').text,
                                  'timestamp': note.find('timestamp').text})
        return notes

    def add_wiki(self, topic):
        try:
            url = "https://en.wikipedia.org/w/api.php"
            params = {
                "action": "opensearch",
                "namespace": 0,
                "search": topic,
                "limit": 1,
                "format": "json"
            }

            res = requests.get(url, params=params)
            result = res.json()
            print(result[0])

            if result[1]:
                time = datetime.now().strftime("%m/%d/%Y - %H:%M:%S")
                return self.add_note(topic, result[3][0], time)
            else:
                return False
            
        except requests.RequestException as e:
            print(f"Failed to fetch from wikipedia:{e}")
            return False

def main():
    if len(sys.argv) >= 2:
        port = int(sys.argv[1])
    else: 
        port = 3000
        
    server = ThreadedXMLRPCServer(('localhost', port))

    server_instance = NoteServer()
    server.register_instance(server_instance)

    print(f"Server side listening on port {port}:")
    server.serve_forever()
    
    
if __name__ == "__main__":
    main()