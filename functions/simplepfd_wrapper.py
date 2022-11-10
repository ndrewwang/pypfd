import functions.simplepfd as simplepfd
#Wrapper for simplepdf package from https://github.com/aslake/simplepfd
import datetime
from bs4 import BeautifulSoup

from IPython.display import display, update_display
MIMETYPE = "application/x-drawio"
#USES https://github.com/deathbeds/ipydrawio

def nth_repl(s, sub, repl, n): #Replacing the label with empty string in XML without duplicating block tags
    find = s.find(sub)
    i = find != -1
    while find != -1 and i != n:
        find = s.find(sub, find + 1)
        i += 1
    if i == n:
        return s[:find] + repl + s[find+len(sub):]
    return s

def xmllabel(texts): #XML labels with multiple lines where the first line is bolded. takes a list
    for i,t in enumerate(texts):
    
        if i == 0:
            xmlt = '&lt;b&gt;'+t+'&lt;/b&gt;'
        else:
            xmlt = xmlt + '&lt;br&gt;' + t
    return xmlt

def Unit(label, **kwargs):
    x = simplepfd.Unit(xmllabel(label),'box')  
    if 'show' in kwargs.keys():
        if kwargs['show']==False:
            x.xml = nth_repl(x.xml,x.tag,'',2)       
    return x

def In(label, **kwargs):
    x = simplepfd.Unit(xmllabel(label),'text')
    if 'show' in kwargs.keys():
        if kwargs['show']==False:
            x.xml = nth_repl(x.xml,x.tag,'',2)  
    return x

def Out(label, **kwargs):
    x = simplepfd.Unit(xmllabel(label),'text')
    if 'show' in kwargs.keys():
        if kwargs['show']==False:
            x.xml = nth_repl(x.xml,x.tag,'',2)  
    return x

def Flow(label, unit1, unit2, **kwargs):
    hide = False
    if 'show' in kwargs.keys():
        if kwargs['show']==False:
            hide = True
            
    x = simplepfd.Flow(xmllabel(label), unit1.tag, unit2.tag, width=1, dashed=False, color='black', nolabel=hide)
    return x

def Components(component_list): #compile list of component values, taking into account sub routines
    a = list()
    for i in component_list:
        a = a + list(i.values())
    return a

def write_pfd(filename, components):
    xmlstr = simplepfd.write_pfd(filename, components)
    return xmlstr
    
def write_xml(components):
    # Build component xml and tag dictionary
    # Build component xml and tag dictionary
    xml = ""
    tags = {}
    for tag in components:
        xml = tag.xml + xml
        if tag.type == "Line":
            source = tag.source
            target = tag.target
            style = tag.style
        else:
            source = None
            target = None
            style = None
        tags[tag.tag] = [tag.xml, source, target, style, tag.type] # Tag dictionary with xml and info on flows

    
    pfd = f'<?xml version="1.0" encoding="UTF-8"?><mxfile host="app.diagrams.net" modified="{datetime.datetime.now()}" agent="pchemeng.tools.simplepfd" etag="Ym8JUHmCbybyuN_C31Ly" version="12.9.13" type="device"><diagram id="S1Gz87AjEctzsXtTaDJA" name="Page-1"><mxGraphModel dx="1422" dy="757" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="850" pageHeight="1100" math="0" shadow="0"><root><mxCell id="0" /><mxCell id="1" parent="0" />{xml}</root></mxGraphModel></diagram></mxfile>'
    soup = BeautifulSoup(pfd, "xml")

    # Position all units in an inital diagonal pattern without overlap
    i = 0
    for id in soup.find_all('mxCell'):
        if id.get('type') == "Unit":
            x = y = i = i + 30
            id.find('mxGeometry')['x'] = x
            id.find('mxGeometry')['y'] = y

        return pfd

def Display(xml, height):
    """ Send some xml to the frontend
    
    Get a handle to update later by calling `display_drawio` with `display_id=True` 
    """
    return display({MIMETYPE: xml}, raw=True, metadata={MIMETYPE: dict(height=height, drawioUrlParams=dict(ui="dark", chrome=1))})
