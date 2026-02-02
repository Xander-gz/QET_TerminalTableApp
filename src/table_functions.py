"""
Copyright (C) 2026 xanderhopp; xanderhopp@gmail.com

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, version 3.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
"""

import xml.etree.ElementTree as ElementTree
import uuid as uuidly


# ident = createId.createUuid()
def create_ident():
    ident = '{' + uuidly.uuid1().urn[9:] + '}'
    return ident


def diagram_template(xmltree):
    try:
        template = []
        tree = xmltree.getroot()
        newdiagrams = tree.find("newdiagrams")
        inset = newdiagrams.find("inset")
        template.append(inset.get("author"))
        template.append(inset.get("titleblocktemplate"))
        template.append(inset.get("titleblocktemplateCollection"))
        template.append(inset.get("displayAt"))
        return template
    except(IndentationError, TypeError) as e:
        print("Something went wrong!", e.args[0])


def new_diagram(xmltree):
    try:
        new_diagram_data = []
        tree = xmltree.getroot()
        newdiagrams = tree.find("newdiagrams")
        for propertys in newdiagrams.iter("property"):
            new_diagram_data.append([propertys.get("name"), propertys.text])
        return new_diagram_data
    except(IndentationError, TypeError) as e:
        print("Something went wrong!", e.args[0])


# ------------------------------------------------------------------------------
# die Seite der Tabelle wird erstellt  ...  the page of a table is to be createt
# ------------------------------------------------------------------------------


def create_category():
    category = ElementTree.Element("category", {"name":"Klemmenplaene"})
    names = ElementTree.SubElement(category, "names")
    name = ElementTree.SubElement(names, "name", {"lang":"de"})
    name.text = "Klemmenpläne"
    name = ElementTree.SubElement(names, "name", {"lang":"en"})
    name.text = "terminal diagrams"
    name = ElementTree.SubElement(names, "name", {"lang":"fr"})
    name.text = "Schémas de terminaux"
    return category


def create_page(terminal_row_obj, pagenumberP, originPages, template, diagramData, dateP, part, identstr):
    qetElementName = "terminal_strip_" + terminal_row_obj.terminal_name + str(part) + ".elmt"
    qetElementTitle = _("Terminal strip ") + terminal_row_obj.terminal_name + " / " + str(part)
    diagram = ElementTree.Element("diagram", {"order": str(pagenumberP), "displayAt":"bottom",
                                 "height":"1070", "colsize":"200", "displaycols":"true",
                                 "author": template[0], "plant":terminal_row_obj.plant, "rows":"6",
                                 "displayrows":"true",
                                 "title": qetElementTitle,
                                 "folio":"K" + str(pagenumberP - originPages), "rowsize":"175", "cols":"8",
                                 "freezeNewElement":"true", "filename":"", "version":"%{version}",
                                 "freezeNewConductor":"false", "auto_page_num":"",
                                 "titleblocktemplateCollection":"embedded",
                                 "titleblocktemplate":template[1], "date": dateP,
                                 "indexrev":"", "locmach":terminal_row_obj.locmach, })
    print(template[0::])
    properties1 =ElementTree.SubElement(diagram, "properties")
    for i in diagramData[0::]:
        if i[0] == "art-unterlage":
            i[1] = "V"
        property1 = ElementTree.SubElement(properties1, "property", {"name":i[0], "show":"1"})
        property1.text = i[1]

        print(i[0],i[1])

    defaultconductor = ElementTree.SubElement(diagram, "defaultcoductor", {"vertical-alignment":"AlignRight",
                                                    "onetextperfolio":"0",
                                                    "color2":"#000000", "horizontal-alignment":"AlignBottom",
                                                    "formula":"", "cable":"", "conductor_section":"",
                                                    "dash-size":"2", "horizrotatetext":"0",
                                                    "bicolor":"false", "conductor_color":"",
                                                    "vertirotatetext":"270", "displaytext":"1",
                                                    "function":"", "type":"multi", "bus":"",
                                                    "condsize":"1", "numsize":"7", "num":"",
                                                    "tension_protocol":"", "text_color":"#000000"})
    elements1 = ElementTree.SubElement(diagram, "elements")
    element1 = ElementTree.SubElement(elements1, "element", {"y":"30", "z":"10", "uuid": identstr,
                                                            "orientation":"0", "frezelabel":"true",
                                                        "x":"70", "prefic":"", "type":"embed://import/Klemmenplaene/" + qetElementName})
    terminals = ElementTree.SubElement(element1, "terminals")
    inputs = ElementTree.SubElement(element1, "inputs")
    elementInformations1 = ElementTree.SubElement(element1, "elementInformations")
    elementInformation1 = ElementTree.SubElement(elementInformations1, "elementInfomation")
    dynamic_texts = ElementTree.SubElement(element1, "dynamic_texts")
    texts_groups = ElementTree.SubElement(element1, "texts_groups")
    return diagram



# ------------------------------------------------------------------------------
# der Rahmen der Tabelle wird erstellt  ...  the frame of a table is to be createt
# ------------------------------------------------------------------------------


def create_table(terminal_row_obj, part, parts, identstr):
    qet_element_name = "terminal_strip_" + terminal_row_obj.terminal_name + str(part) + ".elmt"
    qet_elemtnt_title = _("Terminal strip") + " " + terminal_row_obj.terminal_name + " / " + str(part)

    element = ElementTree.Element("element", {"name": qet_element_name})
    definition = ElementTree.SubElement(element, "definition", {"link_type": "simple",
                                                                "hotspot_y": "10", "height": "1060",
                                                                "version": "%{version}", "hotspot_x": "2",
                                                                "width": "1560", "type": "element"})
    uuid = ElementTree.SubElement(definition, "uuid", {"uuid": identstr})
    names = ElementTree.SubElement(definition, "names")
    name = ElementTree.SubElement(names, "name", {"lang": "de"})
    name.text = qet_elemtnt_title
    element_informations = ElementTree.SubElement(definition, "elementInformations")
    informations = ElementTree.SubElement(definition, "informations")
    informations.text = ""
    description = ElementTree.SubElement(definition, "description")

    # rectangles: 0 = pageframe, 1 = cablelistframe, 2 = chosenterminalframe, 3 = nameterminalstripframe
    # [y-pos, width, x-pos, height]
    rectangles = (["-5", "1555", "0", "1050"],
                  ["-5", "600", "0", "180"],
                  ["-5", "600", "955", "180"],
                  ["-5", "355", "600", "60"])
    for s in rectangles:
        rect = ElementTree.SubElement(description, "rect",
                                      {"y": s[0], "width": s[1], "antialias": "false",
                                       "ry": "0", "x": s[2], "rx": "0",
                                       "style": "line-style:normal;line-weight:normal;filling:none;color:black",
                                       "height": s[3]})
    # lines
    lines = (["15", "0", "600", "15", "thin"],  # Unter Überschrift Kabelliste
             ["35", "0", "600", "35", "thin"],  # Zeilen Kabelliste
             ["55", "0", "600", "55", "thin"],
             ["75", "0", "600", "75", "thin"],
             ["95", "0", "600", "95", "thin"],
             ["115", "0", "600", "115", "thin"],
             ["135", "0", "600", "135", "thin"],
             ["155", "0", "600", "155", "thin"],
             ["242", "0", "1555", "242", "normal"],  # Unter Überschrift Klemmentabelle 2 Linien
             ["245", "0", "1555", "245", "normal"],
             ["215", "80", "80", "245", "normal"],  # senkrechte Trennlinien / nach Planverweis
             ["215", "290", "290", "245", "normal"], # nach Zuordnungstabelle
             ["215", "580", "580", "245", "normal"], # nach Ziehlbezeichnung
             ["215", "980", "980", "245", "normal"], # vor Ziehlbezeichnung
             ["215", "1270", "1270", "245", "normal"], # vor Zuordnungstabelle
             ["215", "1480", "1480", "245", "normal"], # vor Planverweis
             ["235", "110", "110", "245", "thin"],  # zwischenlinien Kabelzuordnung
             ["235", "140", "140", "245", "thin"],
             ["235", "170", "170", "245", "thin"],
             ["235", "200", "200", "245", "thin"],
             ["235", "230", "230", "245", "thin"],
             ["235", "260", "260", "245", "thin"],
             ["242", "600", "600", "245", "thin"],
             ["235", "690", "690", "245", "thin"],
             # ["235", "865", "865", "245", "thin"], kein Planverweis für die Klemme
             ["242", "960", "960", "245", "thin"],
             ["235", "1300", "1300", "245", "thin"],
             ["235", "1330", "1330", "245", "thin"],
             ["235", "1360", "1360", "245", "thin"],
             ["235", "1390", "1390", "245", "thin"],
             ["235", "1420", "1420", "245", "thin"],
             ["235", "1450", "1450", "245", "thin"],
             ["220", "810", "810", "245", "hight"],  # dicke linien an Klemmennummern
             ["220", "870", "870", "245", "hight"],
             ["15", "955", "1555", "15", "normal"])  # unter Überschrift Rahmen verwendete Klemme
    for s in lines:
        line = ElementTree.SubElement(description, "line",
                                      {"y1": s[0],
                                       "style": f"line-style:normal;line-weight:{s[4]};filling:none;color:black",
                                       "Length1": "1.5", "x1": s[1], "end1": "none", "antialias": "false",
                                       "x2": s[2], "length2": "1.5", "y2": s[3], "end2": "none"})
    text = ElementTree.SubElement(description, "text",
                                  {"font": "Sans Serif,28,-1,5,75,0,0,0,0,0",
                                   "rotation": "0", "y": "40", "color": "#000000",
                                   "x": "770", "text": terminal_row_obj.terminal_name})  # Rahmen 4 / Klemmleistenbezeichnung
    text = ElementTree.SubElement(description, "text",
                                  {"font": "Sans Serif,9,-1,5,75,0,0,0,0,0",
                                   "rotation": "0", "y": "80", "color": "#000000",
                                   "x": "615",
                                   "text": "Blatt " + str(part) + " von " + str(parts)})  # Blatt-NR / Anzahl Blätter

    texts = (["9", "75", "15", "10", _("Cables or single wires used")],  # Texte im Rahmen Kabelliste
             ["9", "50", "20", "30", _("Designation")],
             ["9", "50", "120", "30", _("Ziehl")],
             ["9", "50", "190", "30", _("Type")],
             ["9", "50", "300", "30", _("Cross-section")],
             ["9", "50", "380", "30", _("Number of wires")],
             ["9", "50", "480", "30", _("Voltage/protocol")],
             ["9", "75", "5", "50", "1"],
             ["9", "75", "5", "70", "2"],
             ["9", "75", "5", "90", "3"],
             ["9", "75", "5", "110", "4"],
             ["9", "75", "5", "130", "5"],
             ["9", "75", "5", "150", "6"],
             ["9", "75", "5", "170", "7"],
             ["9", "75", "615", "25", _("Terminal strip:")],  # Überschrift
             ["9", "75", "970", "10", _("Terminal used:")],
             ["9", "75", "1300","10", _("Comments:")],
             ["9", "50", "10", "220", _("Plan-")],  # Spaltenüberschriften rechts
             ["9", "50", "10", "235", _("reference")],
             ["9", "75", "120", "215", _("Cable")],
             ["9", "50", "170", "215", _("Wire nr.  /  Color")],
             ["9", "75", "92", "235", "1"],
             ["9", "75", "122", "235", "2"],
             ["9", "75", "152", "235", "3"],
             ["9", "75", "182", "235", "4"],
             ["9", "75", "212", "235", "5"],
             ["9", "75", "242", "235", "6"],
             ["9", "75", "272", "235", "7"],
             ["9", "75", "415", "215", _("Ziehl")],
             ["9", "50", "295", "235", _("= Plant / + Location / - Device tag / : Connection")],
             # ["9", "50", "360", "235", _("+ Location /")], # so ist die Gesamtläne übersichtlicher
             # ["9", "50", "405", "235", _("- Device tag /")],
             # ["9", "50", "495", "235", _(": Connection")],
             ["9", "50", "700", "235", _("Function")],
             ["9", "50", "592", "235", _("Bridge / Socket")],
             ["9", "50", "510", "215", _("externaly")],
             ["11", "75", "810", "200", _("Terminal")],
             ["9", "50", "1012", "215", _("internaly")],
             # ["9", "50", "813", "220", "Plan-"],  # aus Platzgründen verworfen
             # ["9", "50", "813", "235", "verweis"],
             ["9", "50", "880", "235", _("Bridge / Socket")],
             ["9", "50", "1490", "220", _("Plan-")],
             ["9", "50", "1490", "235", _("reference")],
             ["9", "75", "1097", "215", _("Ziehl")],
             ["9", "50", "985", "235", _("= Plant / + Location / - Device tag / : Connection")],
             # ["9", "50", "1050", "235", _("+ Location /")],
             # ["9", "50", "1095", "235", _("- Device tag /")],
             # ["9", "50", "1185", "235", _(": Connection")],
             ["9", "75", "1310", "215", _("Cable")],
             ["9", "50", "1360", "215", _("Wire nr.  /  Color")],
             ["9", "75", "1282", "235", "1"],
             ["9", "75", "1312", "235", "2"],
             ["9", "75", "1342", "235", "3"],
             ["9", "75", "1372", "235", "4"],
             ["9", "75", "1402", "235", "5"],
             ["9", "75", "1432", "235", "6"],
             ["9", "75", "1462", "235", "7"])
    for s in texts:
        text = ElementTree.SubElement(description, "text",
                                      {"font": f"Sans Serif,{s[0]},-1,5,{s[1]},0,0,0,0,0",
                                       "rotation": "0", "y": s[3], "color": "#000000",
                                       "x": s[2], "text": s[4]})
    return element


# --------------------------------------------------------------------------------
# Erstellen der Tabellenzeile ... create the tablecol
# --------------------------------------------------------------------------------


def create_row_outer(connection_obj, conductor_obj, element_obj, connected_cables,
                     terminal_counter, rows_per_terminal, sf, give_feedback):
    try:
        x = 239 + (terminal_counter * 20) + (rows_per_terminal[1].index(connection_obj.eet_name) * 20)
    except:
        give_feedback(_("Is this terminal internally and externally reversed?") + connection_obj.terminal_name + ":" + connection_obj.ei_terminal_nr)
    c = 0
    print (connected_cables)
    # check if cables are in the cable list, if, than set the place, where the colorlabel has to be in the table
    if conductor_obj.cable != "":
        c = 83
        for i in connected_cables:
            if conductor_obj.cable in i[0]:
                break
            else:
                c += 30
    else:
        c = 83
        give_feedback(_("Attention! No cables stored! \nWires are stored in column 1."))

    if "-X" in element_obj.label:
        element_obj.connectionpoint = str(element_obj.x_nr) + " " + str(element_obj.connectionpoint)
        element_obj.plant = element_obj.x_plant
        element_obj.location = element_obj.x_locmach

    description = ElementTree.Element("description")
    text = ElementTree.SubElement(description, "text",
                                  {"font": "Sans Serif,9,-1,5,50,0,0,0,0,0",
                                   "rotation": "0", "y": str(x), "color": "#000000",
                                   "x": "8", "text": sf.reference(element_obj)} ) # Seitenverweis
    if conductor_obj.conductor_color != "":
        text = ElementTree.SubElement(description, "text",
                                      {"font": "Sans Serif,9,-1,5,50,0,0,0,0,0",
                                       "rotation": "0", "y": str(x), "color": "#000000",
                                       "x": str(c), "text": conductor_obj.conductor_color})
    text = ElementTree.SubElement(description, "text",
                                  {"font": "Sans Serif,9,-1,5,50,0,0,0,0,0",
                                   "rotation": "0", "y": str(x), "color": "#000000",
                                   "x": "295", "text": ("="+element_obj.plant)})
    text = ElementTree.SubElement(description, "text",
                                  {"font": "Sans Serif,9,-1,5,50,0,0,0,0,0",
                                   "rotation": "0", "y": str(x), "color": "#000000",
                                   "x": "370", "text": ("+"+element_obj.location)})
    text = ElementTree.SubElement(description, "text",
                                  {"font": "Sans Serif,9,-1,5,50,0,0,0,0,0",
                                   "rotation": "0", "y": str(x), "color": "#000000",
                                   "x": "440", "text": element_obj.label})
    text = ElementTree.SubElement(description, "text",
                                  {"font": "Sans Serif,9,-1,5,50,0,0,0,0,0",
                                   "rotation": "0", "y": str(x), "color": "#000000",
                                   "x": "530", "text": (":"+element_obj.connectionpoint)})
    return description


def create_row_inner(connection_obj, conductor_obj, element_obj, connected_cables, terminal_counter,
                     rows_per_terminal, sf, give_feedback):

    x = 239 + (terminal_counter * 20) + (rows_per_terminal[2].index(connection_obj.eet_name) * 20)
    c = 0
    if conductor_obj.cable != "":
        c = 1273
        for i in connected_cables:
            if conductor_obj.cable not in i[0]:
                c += 30
            else:
                break
    else:
        c = 1273
        give_feedback(_("Attention! No cables stored! \nWires are stored in column 1."))

    if "-X" in element_obj.label:
        element_obj.connectionpoint = str(element_obj.x_nr) + " " + str(element_obj.connectionpoint)
        element_obj.plant = element_obj.x_plant
        element_obj.location = element_obj.x_locmach

    if element_obj.label == "-X%":
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    description = ElementTree.Element("description")
    text = ElementTree.SubElement(description, "text",
                                  {"font": "Sans Serif,9,-1,5,50,0,0,0,0,0",
                                   "rotation": "0", "y": str(x), "color": "#000000",
                                   "x": "1490", "text": sf.reference(element_obj)})  # Seitenverweis
    if conductor_obj.conductor_color != "":
        text = ElementTree.SubElement(description, "text",
                                      {"font": "Sans Serif,9,-1,5,50,0,0,0,0,0",
                                       "rotation": "0", "y": str(x), "color": "#000000",
                                       "x": str(c), "text": conductor_obj.conductor_color})
    text = ElementTree.SubElement(description, "text",
                                  {"font": "Sans Serif,9,-1,5,50,0,0,0,0,0",
                                   "rotation": "0", "y": str(x), "color": "#000000",
                                   "x": "985", "text": ("="+element_obj.plant)})
    text = ElementTree.SubElement(description, "text",
                                  {"font": "Sans Serif,9,-1,5,50,0,0,0,0,0",
                                   "rotation": "0", "y": str(x), "color": "#000000",
                                   "x": "1060", "text": ("+"+element_obj.location)})
    text = ElementTree.SubElement(description, "text",
                                  {"font": "Sans Serif,9,-1,5,50,0,0,0,0,0",
                                   "rotation": "0", "y": str(x), "color": "#000000",
                                   "x": "1130", "text": element_obj.label})
    text = ElementTree.SubElement(description, "text",
                                  {"font": "Sans Serif,9,-1,5,50,0,0,0,0,0",
                                   "rotation": "0", "y": str(x), "color": "#000000",
                                   "x": "1220", "text": (":"+element_obj.connectionpoint)})
    return description


def create_terminal(terminal_obj, linepos, rows, list_of_connectionpoints ):
    x = 240 + (linepos * 20) + ((rows-1) * 10)
    y = 239 + linepos * 20

    description = ElementTree.Element("description")
    text = ElementTree.SubElement(description, "text",
                                  {"font": "Sans Serif,11,-1,5,75,0,0,0,0,0",
                                   "rotation": "0", "y": str(x), "color": "#000000",
                                   "x": "820", "text": terminal_obj.terminal_nr})
    # auf den Verweis wird aus Platzgründen verzichtet
    # text = ElementTree.SubElement(description, "text",
    #                               {"font": "Sans Serif,9,-1,5,50,0,0,0,0,0",
    #                                "rotation": "0", "y": str(x), "color": "#000000",
    #                                "x": "812", "text": sf.reference(terminal_obj)})
    text = ElementTree.SubElement(description, "text",
                                  {"font": "Sans Serif,9,-1,5,50,0,0,0,0,0",
                                   "rotation": "0", "y": str(x), "color": "#000000",
                                   "x": "695", "text": terminal_obj.function})
    zo = 0
    zi = 0
    for lc in list_of_connectionpoints:
        if lc[1] == "Outer":
            text = ElementTree.SubElement(description, "text",
                                          {"font": "Sans Serif,9,-1,5,75,0,0,0,0,0",
                                           "rotation": "0", "y": str(y + zo * 20), "color": "#000000",
                                           "x": "585", "text": lc[0]})
            zo += 1
        if lc[1] == "Inner":
            text = ElementTree.SubElement(description, "text",
                                          {"font": "Sans Serif,9,-1,5,75,0,0,0,0,0",
                                           "rotation": "0", "y": str(y + zi * 20), "color": "#000000",
                                           "x": "965", "text": lc[0]})
            zi += 1

    created_terminal = terminal_obj.terminal_name, terminal_obj.terminal_nr, x
    return description, created_terminal


def create_terminal_bridge(bridges, number_of_terminals, terminal_counter, give_feedback):
    description = ElementTree.Element("description")
    xb = None
    for b in bridges:
        # select, where the bridge has to be
        print("Brücke b: ", b)
        if b[3] == "e":
            xb = 585+30*int(b[2])
        if b[3] == "i":
            xb = 945-30*int(b[2])

        if xb == None:
            give_feedback(_("Error! The ‘position designation’ is incorrect at a bridge at terminal") + ": " + str(b[4]) + ". " + _("It must be (1-3)e or (1-3)i."))

        # a bridge could be drawed from lower terminal to upper terminal or the other way
        if int(b[0]) < int(b[1]):
            y_start = int(b[0]) - 9
            y_end = int(b[1]) - 1
            y2_start = y_start + 11
            y2_end = y_end - 11
        else:
            y_start = int(b[1]) - 9
            y_end = int(b[0]) - 1
            y2_start = y_start + 11
            y2_end = y_end - 11

        # if the bridge is going to rise over the end of the page, there must be no circle at the end of the bridge
        # and te drawing should end at the last terminal
        end_start = "circle"
        end_end = "circle"
        if y_start == -9:
            end_start = "none"
            y_start = 247
            y2_start = 247
        if y_end == 9998:
            end_end = "none"
            y_end = 223 + 20 * terminal_counter
            y2_end = 223 + 20 * terminal_counter




        line = ElementTree.SubElement(description, "line",
                                      {"x1": str(xb),
                                       "style": "line-style:normal;line-weight:eleve;filling:black;color:black",
                                       "length2": "4.0", "y1": str(y_start), "end1": end_start, "antialias": "false",
                                       "y2": str(y_end), "length1": "4.0", "x2": str(xb),
                                       "end2": end_end})  # sehr dicker Strich mit gefüllten Kreis-Enden
        line = ElementTree.SubElement(description, "line",
                                      {"x1": str(xb),
                                       "style": "line-style:normal;line-weight:heigh;filling:white;color:white",
                                       "length2": "4.0", "y1": str(y2_start), "end1": "none", "antialias": "false",
                                       "y2": str(y2_end), "length1": "4.0", "x2": str(xb),
                                       "end2": "none"})  # dicker weißer Strich
    return description


def create_lines(linepos, rows):
    x = 245 + (linepos * 20)
    if rows > 1:
        x = 245 + (linepos * 20)
    description = ElementTree.Element("description")
    while rows > 1:
        line = ElementTree.SubElement(description, "line",
                                      {"y1": str(x-12),
                                       "style": "line-style:normal;line-weight:normal;filling:none;color:black",
                                       "Length2": "1.5", "x1": "900", "end1": "none", "antialias": "false",
                                       "x2": "900", "length2": "1.5", "y2": str(x-8),
                                       "end2": "none"})  # Andeuten Fach für Steckbrücke
        line = ElementTree.SubElement(description, "line",
                                      {"y1": str(x-12),
                                       "style": "line-style:normal;line-weight:normal;filling:none;color:black",
                                       "Length2": "1.5", "x1": "930", "end1": "none", "antialias": "false",
                                       "x2": "930", "length2": "1.5", "y2": str(x-8),
                                       "end2": "none"})  # Andeuten Fach für Steckbrücke
        line = ElementTree.SubElement(description, "line",
                                      {"y1": str(x),
                                       "style": "line-style:dashed;line-weight:thin;filling:none;color:black",
                                       "Length2": "1.5", "x1": "0", "end1": "none", "antialias": "false",
                                       "x2": "600", "length2": "1.5", "y2": str(x),
                                       "end2": "none"})  # Trennstrich gestrichelt
        line = ElementTree.SubElement(description, "line",
                                      {"y1": str(x-12),
                                       "style": "line-style:normal;line-weight:normal;filling:none;color:black",
                                       "Length2": "1.5", "x1": "630", "end1": "none", "antialias": "false",
                                       "x2": "630", "length2": "1.5", "y2": str(x-8),
                                       "end2": "none"})  # Andeuten Fach für Steckbrücke
        line = ElementTree.SubElement(description, "line",
                                      {"y1": str(x-12),
                                       "style": "line-style:normal;line-weight:normal;filling:none;color:black",
                                       "Length2": "1.5", "x1": "660", "end1": "none", "antialias": "false",
                                       "x2": "660", "length2": "1.5", "y2": str(x-8),
                                       "end2": "none"})  # Andeuten Fach für Steckbrücke

        line = ElementTree.SubElement(description, "line",
                                      {"y1": str(x),
                                       "style": "line-style:dashed;line-weight:thin;filling:none;color:black",
                                       "Length2": "1.5", "x1": "960", "end1": "none", "antialias": "false",
                                       "x2": "1555", "length2": "1.5", "y2": str(x),
                                       "end2": "none"})  # Trennstrich gestrichelt

        lines = (["215", "80", "80", "1045", "normal"],  # senkrechte Trennlinien / nach Planverweis
                ["215", "290", "290", "1045", "normal"], # nach Zuordnungstabelle
                ["215", "580", "580", "1045", "normal"], # nach Ziehlbezeichnung
                ["215", "980", "980", "1045", "normal"], # vor Ziehlbezeichnung
                ["215", "1270", "1270", "1045", "normal"], # vor Zuordnungstabelle
                ["215", "1480", "1480", "1045", "normal"], # vor Planverweis
                ["235", "110", "110", "1045", "thin"],  # zwischenlinien Kabelzuordnung
                ["235", "140", "140", "1045", "thin"],
                ["235", "170", "170", "1045", "thin"],
                ["235", "200", "200", "1045", "thin"],
                ["235", "230", "230", "1045", "thin"],
                ["235", "260", "260", "1045", "thin"],
                ["242", "600", "600", "1045", "thin"],
                ["235", "690", "690", "1045", "thin"],
                # ["235", "865", "865", "1045", "thin"], kein Planverweis für die Klemme
                ["242", "960", "960", "1045", "thin"],
                ["235", "1300", "1300", "1045", "thin"],
                ["235", "1330", "1330", "1045", "thin"],
                ["235", "1360", "1360", "1045", "thin"],
                ["235", "1390", "1390", "1045", "thin"],
                ["235", "1420", "1420", "1045", "thin"],
                ["235", "1450", "1450", "1045", "thin"],
                ["220", "810", "810", "1044", "hight"],  # dicke linien an Klemmennummern
                ["220", "870", "870", "1044", "hight"])

        for s in lines:
            line = ElementTree.SubElement(description, "line",
        {"y1": str(x - 20),
         "style": f"line-style:normal;line-weight:{s[4]};filling:none;color:black",
         "Length1": "1.5", "x1": s[1], "end1": "none", "antialias": "false",
         "x2": s[2], "length2": "1.5", "y2": str(x), "end2": "none"})

        x += 20
        rows -= 1
    line = ElementTree.SubElement(description, "line",
                                  {"y1": str(x - 12),
                                   "style": "line-style:normal;line-weight:normal;filling:none;color:black",
                                   "Length2": "1.5", "x1": "900", "end1": "none", "antialias": "false",
                                   "x2": "900", "length2": "1.5", "y2": str(x - 8),
                                   "end2": "none"})  # Andeuten Fach für Steckbrücke
    line = ElementTree.SubElement(description, "line",
                                  {"y1": str(x - 12),
                                   "style": "line-style:normal;line-weight:normal;filling:none;color:black",
                                   "Length2": "1.5", "x1": "930", "end1": "none", "antialias": "false",
                                   "x2": "930", "length2": "1.5", "y2": str(x - 8),
                                   "end2": "none"})  # Andeuten Fach für Steckbrücke
    line = ElementTree.SubElement(description, "line",
                                  {"y1": str(x - 12),
                                   "style": "line-style:normal;line-weight:normal;filling:none;color:black",
                                   "Length2": "1.5", "x1": "630", "end1": "none", "antialias": "false",
                                   "x2": "630", "length2": "1.5", "y2": str(x-8),
                                   "end2": "none"})  # Andeuten Fach für Steckbrücke
    line = ElementTree.SubElement(description, "line",
                                  {"y1": str(x - 12),
                                   "style": "line-style:normal;line-weight:normal;filling:none;color:black",
                                   "Length2": "1.5", "x1": "660", "end1": "none", "antialias": "false",
                                   "x2": "660", "length2": "1.5", "y2": str(x-8),
                                   "end2": "none"})  # Andeuten Fach für Steckbrücke
    line = ElementTree.SubElement(description, "line",
                                  {"y1": str(x),
                                   "style": "line-style:normal;line-weight:normal;filling:none;color:black",
                                   "Length2": "1.5", "x1": "0", "end1": "none", "antialias": "false",
                                   "x2": "1555", "length2": "1.5", "y2": str(x), "end2": "none"})  # Trennstrich normal

    lines = (["215", "80", "80", "1045", "normal"],  # senkrechte Trennlinien / nach Planverweis
            ["215", "290", "290", "1045", "normal"], # nach Zuordnungstabelle
            ["215", "580", "580", "1045", "normal"], # nach Ziehlbezeichnung
            ["215", "980", "980", "1045", "normal"], # vor Ziehlbezeichnung
            ["215", "1270", "1270", "1045", "normal"], # vor Zuordnungstabelle
            ["215", "1480", "1480", "1045", "normal"], # vor Planverweis
            ["235", "110", "110", "1045", "thin"],  # zwischenlinien Kabelzuordnung
            ["235", "140", "140", "1045", "thin"],
            ["235", "170", "170", "1045", "thin"],
            ["235", "200", "200", "1045", "thin"],
            ["235", "230", "230", "1045", "thin"],
            ["235", "260", "260", "1045", "thin"],
            ["242", "600", "600", "1045", "thin"],
            ["235", "690", "690", "1045", "thin"],
            # ["235", "865", "865", "1045", "thin"], kein Planverweis für die Klemme
            ["242", "960", "960", "1045", "thin"],
            ["235", "1300", "1300", "1045", "thin"],
            ["235", "1330", "1330", "1045", "thin"],
            ["235", "1360", "1360", "1045", "thin"],
            ["235", "1390", "1390", "1045", "thin"],
            ["235", "1420", "1420", "1045", "thin"],
            ["235", "1450", "1450", "1045", "thin"],
            ["220", "810", "810", "1044", "hight"],  # dicke linien an Klemmennummern
            ["220", "870", "870", "1044", "hight"])

    for s in lines:
        line = ElementTree.SubElement(description, "line",
    {"y1": str(x - 20),
     "style": f"line-style:normal;line-weight:{s[4]};filling:none;color:black",
     "Length1": "1.5", "x1": s[1], "end1": "none", "antialias": "false",
     "x2": s[2], "length2": "1.5", "y2": str(x), "end2": "none"})

    return description



def create_cablelist_part(a):
    y = 30
    description = ElementTree.Element("description")
    for i in a:
        y += 20
        text = ElementTree.SubElement(description, "text",  # Bezeichnung
                                      {"font": "Sans Serif,9,-1,5,50,0,0,0,0,0",
                                       "rotation": "0", "y": str(y), "color": "#000000",
                                       "x": "25", "text": str(i[0])})
        # text = ElementTree.SubElement(description, "text",  # Ziehl
        #                               {"font": "Sans Serif,9,-1,5,50,0,0,0,0,0",
        #                                "rotation": "0", "y": str(y), "color": "#000000",
        #                                "x": "110", "text": str(i[3])})
        text = ElementTree.SubElement(description, "text",  # Querschnitt
                                      {"font": "Sans Serif,9,-1,5,50,0,0,0,0,0",
                                       "rotation": "0", "y": str(y), "color": "#000000",
                                       "x": "330", "text": str(i[2])})
        text = ElementTree.SubElement(description, "text",  # Spannung/Potential
                                      {"font": "Sans Serif,9,-1,5,50,0,0,0,0,0",
                                       "rotation": "0", "y": str(y), "color": "#000000",
                                       "x": "485", "text": str(i[1])})
    return description


eTableaccessories = ("""
                    <category name="accesories">
                        <names>
                            <name lang="de">Zubehör</name>
                            <name lang="en">accesories</name>
                            <name lang="fr">accessoires</name>
                        </names>
                        <element name="test_socked_bl.elmt">
                            <definition type="element" link_type="simple" hotspot_x="5" hotspot_y="15" width="20" height="20" version="0.100.0">
                                <uuid uuid="{3d2aeebf-183e-496e-bb2b-d8f9d3d0ddd0}"/>
                                <names>
                                    <name lang="de">Steckbuchse blau</name>
                                    <name lang="en">Test socket blue</name>
                                    <name lang="fr">Prise de test bleue</name>
                                </names>
                                <elementInformations/>
                                <description>
                                    <arc x="-3" y="-13" antialias="true" style="line-style:normal;line-weight:hight;filling:none;color:blue" start="183.938" width="16" height="16" angle="355.875"/>
                                    <line end1="none" end2="none" y1="-12" antialias="false" y2="2" style="line-style:normal;line-weight:eleve;filling:none;color:white" x1="5" length1="1.5" length2="1.5" x2="5"/>
                                </description>
                            </definition>
                        </element>
                        <element name="test_socked_gn.elmt">
                            <definition type="element" link_type="simple" hotspot_x="5" hotspot_y="15" width="20" height="20" version="0.100.0">
                                <uuid uuid="{6532a278-8cf5-4a98-a0a1-e6502bcc000c}"/>
                                <names>
                                    <name lang="de">Steckbuchse grün</name>
                                    <name lang="en">Test socket green</name>
                                    <name lang="fr">Prise de test verte</name>
                                </names>
                                <elementInformations/>
                                <description>
                                    <arc x="-3" y="-13" antialias="true" style="line-style:normal;line-weight:hight;filling:none;color:HTMLGreenLimeGreen" start="183.938" width="16" height="16" angle="355.875"/>
                                    <line end1="none" end2="none" y1="-12" antialias="false" y2="2" style="line-style:normal;line-weight:eleve;filling:none;color:white" x1="5" length1="1.5" length2="1.5" x2="5"/>
                                </description>
                            </definition>
                        </element>
                        <element name="test_socked_vt.elmt">
                            <definition type="element" link_type="simple" hotspot_x="5" hotspot_y="15" width="20" height="20" version="0.100.0">
                                <uuid uuid="{5c892802-2018-487f-aa96-e5a25b9cb60c}"/>
                                <names>
                                    <name lang="de">Steckbuchse violet</name>
                                    <name lang="en">Test socket violet</name>
                                    <name lang="fr">Prise de test violette</name>
                                </names>
                                <elementInformations/>
                                <description>
                                    <arc x="-3" y="-13" antialias="true" style="line-style:normal;line-weight:hight;filling:none;color:purple" start="183.938" width="16" height="16" angle="355.875"/>
                                    <line end1="none" end2="none" y1="-12" antialias="false" y2="2" style="line-style:normal;line-weight:eleve;filling:none;color:white" x1="5" length1="1.5" length2="1.5" x2="5"/>
                                </description>
                            </definition>
                        </element>
                        <element name="test_socked_yo.elmt">
                            <definition type="element" link_type="simple" hotspot_x="5" hotspot_y="15" width="20" height="20" version="0.100.0">
                                <uuid uuid="{fcede7ff-0e01-480f-a484-5eff8e8b0beb}"/>
                                <names>
                                    <name lang="de">Steckbuchse gelb</name>
                                    <name lang="en">Test socket yellow</name>
                                    <name lang="fr">Prise de test jaune</name>
                                </names>
                                <elementInformations/>
                                <description>
                                    <arc x="-3" y="-13" antialias="true" style="line-style:normal;line-weight:hight;filling:none;color:yellow" start="183.938" width="16" height="16" angle="355.875"/>
                                    <line end1="none" end2="none" y1="-12" antialias="false" y2="2" style="line-style:normal;line-weight:eleve;filling:none;color:white" x1="5" length1="1.5" length2="1.5" x2="5"/>
                                </description>
                            </definition>
                        </element>
                        <element name="test_socket_bk.elmt">
                            <definition type="element" link_type="simple" hotspot_x="5" hotspot_y="15" width="20" height="20" version="0.100.0">
                                <uuid uuid="{6c2e58f6-d811-4a67-8ed7-c1e5d2487785}"/>
                                <names>
                                    <name lang="de">Steckbuchse schwarz</name>
                                    <name lang="en">Test socket black</name>
                                    <name lang="fr">Prise de test noire</name>
                                </names>
                                <elementInformations/>
                                <description>
                                    <arc x="-3" y="-13" antialias="true" style="line-style:normal;line-weight:hight;filling:none;color:black" start="183.938" width="16" height="16" angle="355.875"/>
                                    <line end1="none" end2="none" y1="-12" antialias="false" y2="2" style="line-style:normal;line-weight:eleve;filling:none;color:white" x1="5" length1="1.5" length2="1.5" x2="5"/>
                                </description>
                            </definition>
                        </element>
                        <element name="test_socket_gy.elmt">
                            <definition type="element" link_type="simple" hotspot_x="5" hotspot_y="15" width="20" height="20" version="0.100.0">
                                <uuid uuid="{9d3ea151-e6e3-4354-bb9c-53716e5d8a8b}"/>
                                <names>
                                    <name lang="de">Steckbuchse grau</name>
                                    <name lang="en">Test socket gray</name>
                                    <name lang="fr">Prise de test grise</name>
                                </names>
                                <elementInformations/>
                                <description>
                                    <arc x="-3" y="-13" antialias="true" style="line-style:normal;line-weight:hight;filling:none;color:gray" start="183.938" width="16" height="16" angle="355.875"/>
                                    <line end1="none" end2="none" y1="-12" antialias="false" y2="2" style="line-style:normal;line-weight:eleve;filling:none;color:white" x1="5" length1="1.5" length2="1.5" x2="5"/>
                                </description>
                            </definition>
                        </element>
                        <element name="test_socket_rd.elmt">
                            <definition type="element" link_type="simple" hotspot_x="5" hotspot_y="15" width="20" height="20" version="0.100.0">
                                <uuid uuid="{d6827121-2d8a-4edf-9e4a-dfb2b86f7fcd}"/>
                                <names>
                                    <name lang="de">Steckbuchse rot</name>
                                    <name lang="en">Test socket red</name>
                                    <name lang="fr">Prise de test rouge</name>
                                </names>
                                <elementInformations/>
                                <description>
                                    <arc x="-3" y="-13" antialias="true" style="line-style:normal;line-weight:hight;filling:none;color:red" start="183.938" width="16" height="16" angle="355.875"/>
                                    <line end1="none" end2="none" y1="-12" antialias="false" y2="2" style="line-style:normal;line-weight:eleve;filling:none;color:white" x1="5" length1="1.5" length2="1.5" x2="5"/>
                                </description>
                            </definition>
                        </element>
                        <element name="end cover.elmt">
                            <definition type="element" link_type="simple" hotspot_x="205" hotspot_y="0" width="410" height="10" version="0.90">
                                <uuid uuid="{d8d22eae-0626-4648-bb73-217d5b5b2ad1}"/>
                                <names>
                                    <name lang="de">End-Deckel / Trennplatte</name>
                                    <name lang="fr">Capuchon / Rondelle de déconnexion</name>
                                    <name lang="en">End cap / Disconnect washer</name>
                                </names>
                                <elementInformations/>
                                <informations/>
                                <description>
                                    <line end1="diamond" end2="diamond" y1="5" antialias="false" y2="5" style="line-style:normal;line-weight:eleve;filling:black;color:black" x1="-200" length1="1.5" length2="1.5" x2="200"/>
                                    <line end1="none" end2="none" y1="5" antialias="false" y2="5" style="line-style:dashed;line-weight:hight;filling:none;color:white" x1="-200" length1="1.5" length2="1.5" x2="200"/>
                                </description>
                            </definition>
                        </element>
                        <category name="installationsklemme">
                            <names>
                                <name lang="de">Installationsklemme</name>
                            </names>
                            <element name="installationsklemme_phoenix_pti-2-5-pe-l-n.elmt">
                                <definition type="element" link_type="simple" hotspot_x="165" hotspot_y="38" width="330" height="80" version="0.90">
                                    <uuid uuid="{8ad4fd82-177d-48e1-814c-31ac3e85ea5b}"/>
                                    <names>
                                        <name lang="de">Phönix PTI-2,5-PE-L-N</name>
                                    </names>
                                    <elementInformations/>
                                    <informations/>
                                    <description>
                                        <ellipse x="130" y="13.4819" antialias="false" style="line-style:normal;line-weight:normal;filling:none;color:black" width="8" height="7.26389"/>
                                        <ellipse x="122" y="2.5861" antialias="false" style="line-style:normal;line-weight:normal;filling:none;color:black" width="8" height="7.26389"/>
                                        <ellipse x="121.2" y="16.3875" antialias="false" style="line-style:normal;line-weight:normal;filling:none;color:black" width="1.6" height="1.45278"/>
                                        <line end1="none" end2="none" y1="36.6759" antialias="false" y2="30.4747" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="54.1623" length2="1.5" x2="54.1623"/>
                                        <ellipse x="138" y="24.3778" antialias="false" style="line-style:normal;line-weight:normal;filling:none;color:black" width="8" height="7.26389"/>
                                        <ellipse x="113.2" y="16.3875" antialias="false" style="line-style:normal;line-weight:normal;filling:none;color:black" width="1.6" height="1.45278"/>
                                        <line end1="none" end2="none" y1="29.9236" antialias="false" y2="30.189" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="52.2441" length2="1.5" x2="53.2411"/>
                                        <line end1="none" end2="none" y1="29.9236" antialias="false" y2="32.7615" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="52.2441" length2="1.5" x2="48.6906"/>
                                        <line end1="none" end2="none" y1="29.9639" antialias="false" y2="32.8018" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="53.5229" length2="1.5" x2="49.9694"/>
                                        <line end1="none" end2="none" y1="29.9236" antialias="false" y2="24.9551" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="52.2441" length2="1.5" x2="52.2441"/>
                                        <line end1="none" end2="none" y1="26.261" antialias="false" y2="20.0641" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="50.6088" length2="1.5" x2="50.6088"/>
                                        <line end1="none" end2="none" y1="26.4311" antialias="false" y2="26.261" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="49.9694" length2="1.5" x2="50.6088"/>
                                        <line end1="none" end2="none" y1="32.7615" antialias="false" y2="25.7907" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="48.6906" length2="1.5" x2="48.6906"/>
                                        <line end1="none" end2="none" y1="4.35049" antialias="false" y2="2.45701" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="45.9789" length2="1.5" x2="44.7824"/>
                                        <line end1="none" end2="none" y1="2.74148" antialias="false" y2="2.45701" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="44.0327" length2="1.5" x2="44.7824"/>
                                        <line end1="none" end2="none" y1="26.1311" antialias="false" y2="26.4311" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="49.9694" length2="1.5" x2="49.9694"/>
                                        <line end1="none" end2="none" y1="2.45701" antialias="false" y2="5.29499" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="44.7824" length2="1.5" x2="41.2289"/>
                                        <line end1="none" end2="none" y1="4.22013" antialias="false" y2="4.71608" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="45.1175" length2="1.5" x2="44.4965"/>
                                        <line end1="none" end2="none" y1="4.76369" antialias="false" y2="4.35049" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="45.4614" length2="1.5" x2="45.9789"/>
                                        <line end1="none" end2="none" y1="4.22013" antialias="false" y2="4.76369" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="45.1175" length2="1.5" x2="45.4614"/>
                                        <line end1="none" end2="none" y1="11.1086" antialias="false" y2="4.35049" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="43.3507" length2="1.5" x2="45.9789"/>
                                        <line end1="none" end2="none" y1="2.74148" antialias="false" y2="5.57947" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="44.0327" length2="1.5" x2="40.4792"/>
                                        <line end1="none" end2="none" y1="4.71608" antialias="false" y2="5.48008" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="44.4965" length2="1.5" x2="44.5638"/>
                                        <line end1="none" end2="none" y1="23.1519" antialias="false" y2="24.681" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="46.7873" length2="1.5" x2="46.1928"/>
                                        <line end1="none" end2="none" y1="24.1095" antialias="false" y2="24.4953" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="44.6512" length2="1.5" x2="45.3337"/>
                                        <line end1="none" end2="none" y1="25.7907" antialias="false" y2="26.1311" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="48.6906" length2="1.5" x2="49.9694"/>
                                        <line end1="none" end2="none" y1="11.5219" antialias="false" y2="4.76369" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="42.8332" length2="1.5" x2="45.4614"/>
                                        <line end1="none" end2="none" y1="11.2645" antialias="false" y2="4.22013" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="42.3786" length2="1.5" x2="45.1175"/>
                                        <line end1="none" end2="none" y1="12.9945" antialias="false" y2="12.9638" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="41.0714" length2="1.5" x2="40.4647"/>
                                        <line end1="none" end2="none" y1="13.6158" antialias="false" y2="6.8577" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="40.2112" length2="1.5" x2="42.8388"/>
                                        <line end1="none" end2="none" y1="6.84128" antialias="false" y2="6.2211" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="38.9044" length2="1.5" x2="40.5386"/>
                                        <line end1="none" end2="none" y1="5.71322" antialias="false" y2="6.84128" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="38.192" length2="1.5" x2="38.9044"/>
                                        <line end1="none" end2="none" y1="13.6158" antialias="false" y2="13.9464" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="40.2112" length2="1.5" x2="39.7972"/>
                                        <line end1="none" end2="none" y1="15.8025" antialias="false" y2="13.6158" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="44.0757" length2="1.5" x2="40.2112"/>
                                        <line end1="none" end2="none" y1="12.3331" antialias="false" y2="12.9945" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="41.8994" length2="1.5" x2="41.0714"/>
                                        <line end1="none" end2="none" y1="5.29499" antialias="false" y2="5.57947" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="41.2289" length2="1.5" x2="40.4792"/>
                                        <line end1="none" end2="none" y1="5.57947" antialias="false" y2="6.26926" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="40.4792" length2="1.5" x2="40.5429"/>
                                        <line end1="none" end2="none" y1="5.48008" antialias="false" y2="6.14131" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="44.5638" length2="1.5" x2="43.7358"/>
                                        <line end1="none" end2="none" y1="13.4451" antialias="false" y2="12.9032" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="44.391" length2="1.5" x2="45.0692"/>
                                        <line end1="none" end2="none" y1="13.3105" antialias="false" y2="12.9306" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="43.3339" length2="1.5" x2="43.4817"/>
                                        <line end1="none" end2="none" y1="13.3105" antialias="false" y2="12.7686" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="43.3339" length2="1.5" x2="44.0125"/>
                                        <line end1="none" end2="none" y1="12.7686" antialias="false" y2="13.1744" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="44.0125" length2="1.5" x2="44.7299"/>
                                        <line end1="none" end2="none" y1="13.7764" antialias="false" y2="12.9032" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="46.6125" length2="1.5" x2="45.0692"/>
                                        <line end1="none" end2="none" y1="11.2645" antialias="false" y2="11.3596" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="42.3786" length2="1.5" x2="42.3417"/>
                                        <line end1="none" end2="none" y1="12.3886" antialias="false" y2="11.3596" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="44.1601" length2="1.5" x2="42.3417"/>
                                        <line end1="none" end2="none" y1="11.5219" antialias="false" y2="13.7086" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="42.8332" length2="1.5" x2="46.6976"/>
                                        <line end1="none" end2="none" y1="14.3205" antialias="false" y2="13.9407" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="42.0691" length2="1.5" x2="42.2169"/>
                                        <line end1="none" end2="none" y1="13.9407" antialias="false" y2="14.4148" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="42.2169" length2="1.5" x2="41.6232"/>
                                        <line end1="none" end2="none" y1="7.18837" antialias="false" y2="6.8577" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="42.4248" length2="1.5" x2="42.8388"/>
                                        <line end1="none" end2="none" y1="7.18837" antialias="false" y2="5.29499" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="42.4248" length2="1.5" x2="41.2289"/>
                                        <line end1="none" end2="none" y1="14.5234" antialias="false" y2="14.3205" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="41.8152" length2="1.5" x2="42.0691"/>
                                        <line end1="none" end2="none" y1="14.9292" antialias="false" y2="14.4552" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="42.5324" length2="1.5" x2="43.1262"/>
                                        <line end1="none" end2="none" y1="14.7555" antialias="false" y2="15.107" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="45.3866" length2="1.5" x2="46.0191"/>
                                        <line end1="none" end2="none" y1="17.267" antialias="false" y2="17.3873" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="46.0283" length2="1.5" x2="45.8777"/>
                                        <line end1="none" end2="none" y1="13.4451" antialias="false" y2="13.825" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="44.391" length2="1.5" x2="44.2432"/>
                                        <line end1="none" end2="none" y1="12.7686" antialias="false" y2="12.3886" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="44.0125" length2="1.5" x2="44.1601"/>
                                        <line end1="none" end2="none" y1="12.3886" antialias="false" y2="12.9306" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="44.1601" length2="1.5" x2="43.4817"/>
                                        <line end1="none" end2="none" y1="14.7555" antialias="false" y2="15.8025" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="45.3866" length2="1.5" x2="44.0757"/>
                                        <line end1="none" end2="none" y1="23.6358" antialias="false" y2="24.0612" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="44.7372" length2="1.5" x2="44.5718"/>
                                        <line end1="none" end2="none" y1="23.3678" antialias="false" y2="23.2213" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="47.1588" length2="1.5" x2="46.9"/>
                                        <line end1="none" end2="none" y1="23.2213" antialias="false" y2="21.7639" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="46.9" length2="1.5" x2="47.7821"/>
                                        <line end1="none" end2="none" y1="20.0641" antialias="false" y2="19.0595" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="50.6088" length2="1.5" x2="48.8332"/>
                                        <line end1="none" end2="none" y1="19.0595" antialias="false" y2="24.1886" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="48.8332" length2="1.5" x2="46.8391"/>
                                        <line end1="none" end2="none" y1="22.5164" antialias="false" y2="17.3873" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="43.8839" length2="1.5" x2="45.8777"/>
                                        <line end1="none" end2="none" y1="17.267" antialias="false" y2="22.9031" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="46.0283" length2="1.5" x2="43.8372"/>
                                        <line end1="none" end2="none" y1="12.3331" antialias="false" y2="5.48008" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="41.8994" length2="1.5" x2="44.5638"/>
                                        <line end1="none" end2="none" y1="17.3873" antialias="false" y2="13.9464" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="45.8777" length2="1.5" x2="39.7972"/>
                                        <line end1="none" end2="none" y1="32.8018" antialias="false" y2="33.1019" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="49.9694" length2="1.5" x2="49.9694"/>
                                        <line end1="none" end2="none" y1="33.3126" antialias="false" y2="32.8018" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="50.6088" length2="1.5" x2="49.9694"/>
                                        <line end1="none" end2="none" y1="33.1019" antialias="false" y2="32.7615" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="49.9694" length2="1.5" x2="48.6906"/>
                                        <line end1="none" end2="none" y1="39.5138" antialias="false" y2="33.3126" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="50.6088" length2="1.5" x2="50.6088"/>
                                        <line end1="none" end2="none" y1="32.9754" antialias="false" y2="31.5142" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="5.45448" length2="1.5" x2="-0.03412"/>
                                        <line end1="none" end2="none" y1="27.7868" antialias="false" y2="27.4551" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-0.71239" length2="1.5" x2="-1.02289"/>
                                        <line end1="none" end2="none" y1="27.4551" antialias="false" y2="25.3913" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-1.02289" length2="1.5" x2="-2.28651"/>
                                        <line end1="none" end2="none" y1="26.7321" antialias="false" y2="31.5142" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-0.90421" length2="1.5" x2="-0.03412"/>
                                        <line end1="none" end2="none" y1="26.6219" antialias="false" y2="26.7321" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-0.76621" length2="1.5" x2="-0.90421"/>
                                        <line end1="none" end2="none" y1="26.6219" antialias="false" y2="26.3714" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-0.76621" length2="1.5" x2="2.84272"/>
                                        <line end1="none" end2="none" y1="26.4291" antialias="false" y2="26.7321" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="3.46142" length2="1.5" x2="-0.90421"/>
                                        <line end1="none" end2="none" y1="24.0923" antialias="false" y2="25.3913" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-0.65972" length2="1.5" x2="-2.28651"/>
                                        <line end1="none" end2="none" y1="25.3913" antialias="false" y2="24.9159" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-2.28651" length2="1.5" x2="0.99973"/>
                                        <line end1="none" end2="none" y1="26.3714" antialias="false" y2="25.8772" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="2.84272" length2="1.5" x2="3.46142"/>
                                        <line end1="none" end2="none" y1="24.9505" antialias="false" y2="26.4291" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="3.46142" length2="1.5" x2="3.46142"/>
                                        <line end1="none" end2="none" y1="24.6295" antialias="false" y2="24.9159" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="1.35841" length2="1.5" x2="0.99973"/>
                                        <line end1="none" end2="none" y1="24.8114" antialias="false" y2="24.926" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="2.93909" length2="1.5" x2="2.47196"/>
                                        <line end1="none" end2="none" y1="23.1053" antialias="false" y2="23.4973" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-3.47032" length2="1.5" x2="-4.06786"/>
                                        <line end1="none" end2="none" y1="4.48841" antialias="false" y2="4.6087" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="30.613" length2="1.5" x2="30.4625"/>
                                        <line end1="none" end2="none" y1="11.3307" antialias="false" y2="11.7167" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="29.2353" length2="1.5" x2="29.9174"/>
                                        <line end1="none" end2="none" y1="9.73783" antialias="false" y2="4.6087" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="28.4681" length2="1.5" x2="30.4625"/>
                                        <line end1="none" end2="none" y1="24.9505" antialias="false" y2="23.1053" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="3.46142" length2="1.5" x2="-3.47032"/>
                                        <line end1="none" end2="none" y1="24.9159" antialias="false" y2="26.3714" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="0.99973" length2="1.5" x2="2.84272"/>
                                        <line end1="none" end2="none" y1="24.926" antialias="false" y2="23.2752" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="2.47196" length2="1.5" x2="-3.7293"/>
                                        <line end1="none" end2="none" y1="23.4231" antialias="false" y2="26.261" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="54.1623" length2="1.5" x2="50.6088"/>
                                        <line end1="none" end2="none" y1="30.4747" antialias="false" y2="33.3126" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="54.1623" length2="1.5" x2="50.6088"/>
                                        <line end1="none" end2="none" y1="29.9639" antialias="false" y2="30.4747" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="53.5229" length2="1.5" x2="54.1623"/>
                                        <line end1="none" end2="none" y1="36.6759" antialias="false" y2="39.5138" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="54.1623" length2="1.5" x2="50.6088"/>
                                        <line end1="none" end2="none" y1="-4.79799" antialias="false" y2="-2.62199" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-66.4146" length2="1.5" x2="-69.1393"/>
                                        <line end1="none" end2="none" y1="-5.04043" antialias="false" y2="-2.86444" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-66.2874" length2="1.5" x2="-69.0121"/>
                                        <line end1="none" end2="none" y1="-7.47814" antialias="false" y2="-1.84781" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-65.0086" length2="1.5" x2="-67.9622"/>
                                        <line end1="none" end2="none" y1="-2.76089" antialias="false" y2="-3.07777" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="12.7627" length2="1.5" x2="13.1595"/>
                                        <line end1="none" end2="none" y1="-0.734963" antialias="false" y2="-2.76089" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="16.343" length2="1.5" x2="12.7627"/>
                                        <line end1="none" end2="none" y1="-3.07777" antialias="false" y2="0.930964" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="13.1595" length2="1.5" x2="20.2441"/>
                                        <line end1="none" end2="none" y1="-6.14944" antialias="false" y2="-5.72421" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-0.120025" length2="1.5" x2="-0.28528"/>
                                        <line end1="none" end2="none" y1="-2.76089" antialias="false" y2="0.325889" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="12.7627" length2="1.5" x2="11.5625"/>
                                        <line end1="none" end2="none" y1="-6.63346" antialias="false" y2="-5.10424" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="1.93066" length2="1.5" x2="1.33622"/>
                                        <line end1="none" end2="none" y1="-6.4175" antialias="false" y2="-6.56396" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="2.30107" length2="1.5" x2="2.04232"/>
                                        <line end1="none" end2="none" y1="-5.14649" antialias="false" y2="-6.42604" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-43.8911" length2="1.5" x2="-50.7876"/>
                                        <line end1="none" end2="none" y1="-1.078" antialias="false" y2="-1.21066" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-60.4917" length2="1.5" x2="-61.206"/>
                                        <line end1="none" end2="none" y1="0.358288" antialias="false" y2="3.44507" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="18.2753" length2="1.5" x2="17.0751"/>
                                        <line end1="none" end2="none" y1="1.3747" antialias="false" y2="0.358288" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="20.0716" length2="1.5" x2="18.2753"/>
                                        <line end1="none" end2="none" y1="-0.239782" antialias="false" y2="-0.556658" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="9.60598" length2="1.5" x2="10.0027"/>
                                        <line end1="none" end2="none" y1="0.178998" antialias="false" y2="0.08399" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="24.9249" length2="1.5" x2="24.9618"/>
                                        <line end1="none" end2="none" y1="1.54195" antialias="false" y2="1.16192" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="26.6534" length2="1.5" x2="26.801"/>
                                        <line end1="none" end2="none" y1="1.74477" antialias="false" y2="1.54195" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="26.3994" length2="1.5" x2="26.6534"/>
                                        <line end1="none" end2="none" y1="1.16192" antialias="false" y2="1.63608" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="26.801" length2="1.5" x2="26.2074"/>
                                        <line end1="none" end2="none" y1="0.997623" antialias="false" y2="0.124379" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="31.197" length2="1.5" x2="29.6538"/>
                                        <line end1="none" end2="none" y1="2.15064" antialias="false" y2="1.67647" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="27.1167" length2="1.5" x2="27.7103"/>
                                        <line end1="none" end2="none" y1="0.579828" antialias="false" y2="0.08399" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="24.3408" length2="1.5" x2="24.9618"/>
                                        <line end1="none" end2="none" y1="0.178998" antialias="false" y2="0.215776" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="24.9249" length2="1.5" x2="25.6555"/>
                                        <line end1="none" end2="none" y1="0.607082" antialias="false" y2="0.178998" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="24.3888" length2="1.5" x2="24.9249"/>
                                        <line end1="none" end2="none" y1="0.666408" antialias="false" y2="1.04644" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="28.9752" length2="1.5" x2="28.8274"/>
                                        <line end1="none" end2="none" y1="0.929869" antialias="false" y2="3.02388" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="31.282" length2="1.5" x2="28.66"/>
                                        <line end1="none" end2="none" y1="3.02388" antialias="false" y2="0.579828" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="28.66" length2="1.5" x2="24.3408"/>
                                        <line end1="none" end2="none" y1="-0.0101425" antialias="false" y2="-0.390066" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="28.5967" length2="1.5" x2="28.7445"/>
                                        <line end1="none" end2="none" y1="-0.390066" antialias="false" y2="0.151962" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="28.7445" length2="1.5" x2="28.0658"/>
                                        <line end1="none" end2="none" y1="0.120877" antialias="false" y2="0.215776" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="25.6925" length2="1.5" x2="25.6555"/>
                                        <line end1="none" end2="none" y1="0.215776" antialias="false" y2="-0.445451" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="25.6555" length2="1.5" x2="26.4835"/>
                                        <line end1="none" end2="none" y1="-0.390066" antialias="false" y2="-1.41907" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="28.7445" length2="1.5" x2="26.9259"/>
                                        <line end1="none" end2="none" y1="-0.0101425" antialias="false" y2="0.395722" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="28.5967" length2="1.5" x2="29.314"/>
                                        <line end1="none" end2="none" y1="0.666408" antialias="false" y2="0.124379" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="28.9752" length2="1.5" x2="29.6538"/>
                                        <line end1="none" end2="none" y1="0.531886" antialias="false" y2="0.151962" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="27.9181" length2="1.5" x2="28.0658"/>
                                        <line end1="none" end2="none" y1="0.531886" antialias="false" y2="-0.0101425" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="27.9181" length2="1.5" x2="28.5967"/>
                                        <line end1="none" end2="none" y1="-0.540349" antialias="false" y2="-0.445451" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="26.5205" length2="1.5" x2="26.4835"/>
                                        <line end1="none" end2="none" y1="-0.967667" antialias="false" y2="-1.41907" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="26.3607" length2="1.5" x2="26.9259"/>
                                        <line end1="none" end2="none" y1="-1.01813" antialias="false" y2="-1.51407" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="26.3418" length2="1.5" x2="26.9628"/>
                                        <line end1="none" end2="none" y1="0.08399" antialias="false" y2="0.120877" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="24.9618" length2="1.5" x2="25.6925"/>
                                        <line end1="none" end2="none" y1="0.120877" antialias="false" y2="-0.540349" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="25.6925" length2="1.5" x2="26.5205"/>
                                        <line end1="none" end2="none" y1="-0.540349" antialias="false" y2="-1.01813" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="26.5205" length2="1.5" x2="26.3418"/>
                                        <line end1="none" end2="none" y1="-1.51407" antialias="false" y2="0.929869" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="26.9628" length2="1.5" x2="31.282"/>
                                        <line end1="none" end2="none" y1="4.6087" antialias="false" y2="-0.329646" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="30.4625" length2="1.5" x2="21.7349"/>
                                        <line end1="none" end2="none" y1="1.46916" antialias="false" y2="-0.734963" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="13.583" length2="1.5" x2="16.343"/>
                                        <line end1="none" end2="none" y1="0.358288" antialias="false" y2="2.56263" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="18.2753" length2="1.5" x2="15.5153"/>
                                        <line end1="none" end2="none" y1="2.56263" antialias="false" y2="4.46159" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="15.5153" length2="1.5" x2="18.8714"/>
                                        <line end1="none" end2="none" y1="-0.556658" antialias="false" y2="1.46916" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="10.0027" length2="1.5" x2="13.583"/>
                                        <line end1="none" end2="none" y1="-5.81341" antialias="false" y2="-2.97532" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-66.1846" length2="1.5" x2="-69.7381"/>
                                        <line end1="none" end2="none" y1="18.538" antialias="false" y2="18.6451" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="52.1923" length2="1.5" x2="52.3855"/>
                                        <line end1="none" end2="none" y1="15.5981" antialias="false" y2="15.9108" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-40.0408" length2="1.5" x2="-40.4322"/>
                                        <line end1="none" end2="none" y1="7.48817" antialias="false" y2="7.66199" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-38.4572" length2="1.5" x2="-38.675"/>
                                        <line end1="none" end2="none" y1="4.48841" antialias="false" y2="10.1245" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="30.613" length2="1.5" x2="28.4216"/>
                                        <line end1="none" end2="none" y1="10.8572" antialias="false" y2="11.2825" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="29.3215" length2="1.5" x2="29.156"/>
                                        <line end1="none" end2="none" y1="14.7458" antialias="false" y2="16.1308" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-36.2148" length2="1.5" x2="-37.9494"/>
                                        <line end1="none" end2="none" y1="17.5539" antialias="false" y2="16.9152" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-37.2534" length2="1.5" x2="-36.8744"/>
                                        <line end1="none" end2="none" y1="14.5475" antialias="false" y2="15.0287" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-37.3468" length2="1.5" x2="-37.9494"/>
                                        <line end1="none" end2="none" y1="8.14162" antialias="false" y2="10.1909" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-37.3017" length2="1.5" x2="-39.8677"/>
                                        <line end1="none" end2="none" y1="10.3732" antialias="false" y2="11.9024" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="31.372" length2="1.5" x2="30.7775"/>
                                        <line end1="none" end2="none" y1="10.5892" antialias="false" y2="10.4427" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="31.7425" length2="1.5" x2="31.4837"/>
                                        <line end1="none" end2="none" y1="10.4427" antialias="false" y2="8.98521" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="31.4837" length2="1.5" x2="32.366"/>
                                        <line end1="none" end2="none" y1="8.51805" antialias="false" y2="8.47284" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="34.6175" length2="1.5" x2="34.7365"/>
                                        <line end1="none" end2="none" y1="6.72592" antialias="false" y2="6.34129" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="34.2041" length2="1.5" x2="34.6858"/>
                                        <line end1="none" end2="none" y1="2.99258" antialias="false" y2="2.60674" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="35.593" length2="1.5" x2="34.911"/>
                                        <line end1="none" end2="none" y1="8.47284" antialias="false" y2="6.72592" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="34.7365" length2="1.5" x2="34.2041"/>
                                        <line end1="none" end2="none" y1="9.67927" antialias="false" y2="8.51805" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="35.3509" length2="1.5" x2="34.6175"/>
                                        <line end1="none" end2="none" y1="6.28087" antialias="false" y2="11.41" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="33.4175" length2="1.5" x2="31.4233"/>
                                        <line end1="none" end2="none" y1="17.1996" antialias="false" y2="19.3003" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-53.8071" length2="1.5" x2="-39.2995"/>
                                        <line end1="none" end2="none" y1="20.0641" antialias="false" y2="18.6451" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="50.6088" length2="1.5" x2="52.3855"/>
                                        <line end1="none" end2="none" y1="-34.0215" antialias="false" y2="-34.8878" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-52.0517" length2="1.5" x2="-52.1319"/>
                                        <line end1="none" end2="none" y1="-34.8878" antialias="false" y2="-35.6043" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-52.1319" length2="1.5" x2="-51.2349"/>
                                        <line end1="none" end2="none" y1="-6.42604" antialias="false" y2="-12.3777" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-50.7876" length2="1.5" x2="-50.7876"/>
                                        <line end1="none" end2="none" y1="-12.3777" antialias="false" y2="-13.0813" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-50.7876" length2="1.5" x2="-50.1182"/>
                                        <line end1="none" end2="none" y1="-34.0219" antialias="false" y2="-33.1753" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-52.053" length2="1.5" x2="-48.873"/>
                                        <line end1="none" end2="none" y1="-13.0813" antialias="false" y2="-12.5119" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-50.1182" length2="1.5" x2="-47.9791"/>
                                        <line end1="none" end2="none" y1="-13.0813" antialias="false" y2="-15.2579" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-50.1182" length2="1.5" x2="-47.3927"/>
                                        <line end1="none" end2="none" y1="-33.1753" antialias="false" y2="-32.4039" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-48.873" length2="1.5" x2="-49.839"/>
                                        <line end1="none" end2="none" y1="-12.5613" antialias="false" y2="-11.4883" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-45.2667" length2="1.5" x2="-41.236"/>
                                        <line end1="none" end2="none" y1="-14.4044" antialias="false" y2="-14.5" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-45.0145" length2="1.5" x2="-45.095"/>
                                        <line end1="none" end2="none" y1="-14.1042" antialias="false" y2="-13.5455" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-43.3347" length2="1.5" x2="-41.236"/>
                                        <line end1="none" end2="none" y1="-14.2155" antialias="false" y2="-14.4044" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-44.3047" length2="1.5" x2="-45.0145"/>
                                        <line end1="none" end2="none" y1="-14.1664" antialias="false" y2="-14.4162" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-41.236" length2="1.5" x2="-44.5753"/>
                                        <line end1="none" end2="none" y1="-14.1042" antialias="false" y2="-12.5613" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-43.3347" length2="1.5" x2="-45.2667"/>
                                        <line end1="none" end2="none" y1="-14.9141" antialias="false" y2="-15.2579" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-46.1009" length2="1.5" x2="-47.3927"/>
                                        <line end1="none" end2="none" y1="-12.5119" antialias="false" y2="-12.2278" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-47.9791" length2="1.5" x2="-47.74"/>
                                        <line end1="none" end2="none" y1="-14.5845" antialias="false" y2="-12.5119" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-45.3839" length2="1.5" x2="-47.9791"/>
                                        <line end1="none" end2="none" y1="-14.1543" antialias="false" y2="-12.6114" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-44.7651" length2="1.5" x2="-46.6971"/>
                                        <line end1="none" end2="none" y1="-33.1753" antialias="false" y2="-32.1468" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-48.873" length2="1.5" x2="-48.873"/>
                                        <line end1="none" end2="none" y1="-24.9334" antialias="false" y2="-25.2935" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-25.4257" length2="1.5" x2="-25.8645"/>
                                        <line end1="none" end2="none" y1="-24.8636" antialias="false" y2="-24.9334" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-25.7103" length2="1.5" x2="-25.4257"/>
                                        <line end1="none" end2="none" y1="-23.6673" antialias="false" y2="-24.8636" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-25.0903" length2="1.5" x2="-25.7103"/>
                                        <line end1="none" end2="none" y1="-25.2868" antialias="false" y2="-23.6673" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-18.479" length2="1.5" x2="-25.0903"/>
                                        <line end1="none" end2="none" y1="-16.7909" antialias="false" y2="-17.4521" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-3.78588" length2="1.5" x2="-2.95788"/>
                                        <line end1="none" end2="none" y1="-16.8858" antialias="false" y2="-16.7909" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-3.74885" length2="1.5" x2="-3.78588"/>
                                        <line end1="none" end2="none" y1="-16.8858" antialias="false" y2="-17.5471" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-3.74885" length2="1.5" x2="-2.92085"/>
                                        <line end1="none" end2="none" y1="-16.0089" antialias="false" y2="-16.8822" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="1.75574" length2="1.5" x2="0.21244"/>
                                        <line end1="none" end2="none" y1="-15.5375" antialias="false" y2="-17.7416" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-15.8584" length2="1.5" x2="-13.0984"/>
                                        <line end1="none" end2="none" y1="-17.5633" antialias="false" y2="-15.5375" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-19.4388" length2="1.5" x2="-15.8584"/>
                                        <line end1="none" end2="none" y1="-19.1704" antialias="false" y2="-17.2443" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-4.96198" length2="1.5" x2="-5.71098"/>
                                        <line end1="none" end2="none" y1="-17.2466" antialias="false" y2="-17.5633" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-19.8355" length2="1.5" x2="-19.4388"/>
                                        <line end1="none" end2="none" y1="-19.7676" antialias="false" y2="-16.6808" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-16.6788" length2="1.5" x2="-17.8789"/>
                                        <line end1="none" end2="none" y1="-16.8277" antialias="false" y2="-16.7909" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-4.51659" length2="1.5" x2="-3.78588"/>
                                        <line end1="none" end2="none" y1="-16.3996" antialias="false" y2="-16.8277" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-5.05249" length2="1.5" x2="-4.51659"/>
                                        <line end1="none" end2="none" y1="-16.8277" antialias="false" y2="-16.9227" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-4.51659" length2="1.5" x2="-4.47956"/>
                                        <line end1="none" end2="none" y1="-16.4267" antialias="false" y2="-16.9227" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-5.10056" length2="1.5" x2="-4.47956"/>
                                        <line end1="none" end2="none" y1="-16.9227" antialias="false" y2="-16.8858" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-4.47956" length2="1.5" x2="-3.74885"/>
                                        <line end1="none" end2="none" y1="-13.9828" antialias="false" y2="-16.4267" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-0.78139" length2="1.5" x2="-5.10056"/>
                                        <line end1="none" end2="none" y1="-18.7916" antialias="false" y2="-17.1786" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-3.78324" length2="1.5" x2="-4.41033"/>
                                        <line end1="none" end2="none" y1="-15.6319" antialias="false" y2="-16.6484" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-9.36971" length2="1.5" x2="-11.1661"/>
                                        <line end1="none" end2="none" y1="-18.6328" antialias="false" y2="-17.4407" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-5.83806" length2="1.5" x2="-6.30162"/>
                                        <line end1="none" end2="none" y1="-17.9609" antialias="false" y2="-17.7906" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-6.47642" length2="1.5" x2="-6.54266"/>
                                        <line end1="none" end2="none" y1="-17.3363" antialias="false" y2="-20.1743" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-7.70646" length2="1.5" x2="-4.15296"/>
                                        <line end1="none" end2="none" y1="-19.7676" antialias="false" y2="-20.0844" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-16.6788" length2="1.5" x2="-16.282"/>
                                        <line end1="none" end2="none" y1="-17.7416" antialias="false" y2="-19.7676" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-13.0984" length2="1.5" x2="-16.6788"/>
                                        <line end1="none" end2="none" y1="-16.6484" antialias="false" y2="-14.4441" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-11.1661" length2="1.5" x2="-13.9261"/>
                                        <line end1="none" end2="none" y1="-16.6484" antialias="false" y2="-13.5615" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-11.1661" length2="1.5" x2="-12.3663"/>
                                        <line end1="none" end2="none" y1="-14.4441" antialias="false" y2="-12.5451" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-13.9261" length2="1.5" x2="-10.57"/>
                                        <line end1="none" end2="none" y1="-18.5208" antialias="false" y2="-18.4257" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-2.47856" length2="1.5" x2="-2.51559"/>
                                        <line end1="none" end2="none" y1="-16.3403" antialias="false" y2="-15.9604" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-0.46629" length2="1.5" x2="-0.61395"/>
                                        <line end1="none" end2="none" y1="-17.5471" antialias="false" y2="-18.0248" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-2.92085" length2="1.5" x2="-3.09956"/>
                                        <line end1="none" end2="none" y1="-17.0167" antialias="false" y2="-17.3967" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-0.84464" length2="1.5" x2="-0.696865"/>
                                        <line end1="none" end2="none" y1="-17.3967" antialias="false" y2="-16.8547" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-0.696865" length2="1.5" x2="-1.37548"/>
                                        <line end1="none" end2="none" y1="-17.5471" antialias="false" y2="-17.4521" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-2.92085" length2="1.5" x2="-2.95788"/>
                                        <line end1="none" end2="none" y1="-18.0248" antialias="false" y2="-18.5208" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-3.09956" length2="1.5" x2="-2.47856"/>
                                        <line end1="none" end2="none" y1="-17.9743" antialias="false" y2="-18.4257" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-3.0807" length2="1.5" x2="-2.51559"/>
                                        <line end1="none" end2="none" y1="-16.4749" antialias="false" y2="-16.8547" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-1.52314" length2="1.5" x2="-1.37548"/>
                                        <line end1="none" end2="none" y1="-16.4749" antialias="false" y2="-17.0167" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-1.52314" length2="1.5" x2="-0.84464"/>
                                        <line end1="none" end2="none" y1="-17.3967" antialias="false" y2="-18.4257" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-0.696865" length2="1.5" x2="-2.51559"/>
                                        <line end1="none" end2="none" y1="-16.3403" antialias="false" y2="-16.8822" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-0.46629" length2="1.5" x2="0.21244"/>
                                        <line end1="none" end2="none" y1="-16.611" antialias="false" y2="-17.0167" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-0.12727" length2="1.5" x2="-0.84464"/>
                                        <line end1="none" end2="none" y1="-18.5208" antialias="false" y2="-16.0768" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-2.47856" length2="1.5" x2="1.84061"/>
                                        <line end1="none" end2="none" y1="-12.5412" antialias="false" y2="-13.1186" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="7.59325" length2="1.5" x2="8.31637"/>
                                        <line end1="none" end2="none" y1="-14.0141" antialias="false" y2="-10.7" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="6.1515" length2="1.5" x2="4.86304"/>
                                        <line end1="none" end2="none" y1="-14.3999" antialias="false" y2="-10.801" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="5.46967" length2="1.5" x2="4.07034"/>
                                        <line end1="none" end2="none" y1="-11.3717" antialias="false" y2="-8.53373" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="8.84848" length2="1.5" x2="5.29498"/>
                                        <line end1="none" end2="none" y1="-6.56396" antialias="false" y2="-8.02148" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="2.04232" length2="1.5" x2="2.92471"/>
                                        <line end1="none" end2="none" y1="-14.0141" antialias="false" y2="-14.3999" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="6.1515" length2="1.5" x2="5.46967"/>
                                        <line end1="none" end2="none" y1="-10.2808" antialias="false" y2="-10.6654" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="4.76287" length2="1.5" x2="5.2445"/>
                                        <line end1="none" end2="none" y1="-10.7258" antialias="false" y2="-10.8461" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="3.97627" length2="1.5" x2="4.12681"/>
                                        <line end1="none" end2="none" y1="-16.0768" antialias="false" y2="-13.9828" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="1.84061" length2="1.5" x2="-0.78139"/>
                                        <line end1="none" end2="none" y1="-15.4647" antialias="false" y2="-15.8447" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-2.78791" length2="1.5" x2="-2.64025"/>
                                        <line end1="none" end2="none" y1="-15.262" antialias="false" y2="-15.4647" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-3.04206" length2="1.5" x2="-2.78791"/>
                                        <line end1="none" end2="none" y1="-15.8447" antialias="false" y2="-15.3705" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-2.64025" length2="1.5" x2="-3.234"/>
                                        <line end1="none" end2="none" y1="-14.856" antialias="false" y2="-15.3302" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-2.32469" length2="1.5" x2="-1.73106"/>
                                        <line end1="none" end2="none" y1="-12.5183" antialias="false" y2="-12.398" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="1.17165" length2="1.5" x2="1.021"/>
                                        <line end1="none" end2="none" y1="-16.1857" antialias="false" y2="-12.1014" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-9.15443" length2="1.5" x2="-10.7425"/>
                                        <line end1="none" end2="none" y1="-13.1186" antialias="false" y2="-11.3717" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="8.31637" length2="1.5" x2="8.84848"/>
                                        <line end1="none" end2="none" y1="-1.78487" antialias="false" y2="-0.171919" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="25.6581" length2="1.5" x2="25.031"/>
                                        <line end1="none" end2="none" y1="-3.16752" antialias="false" y2="-2.01692" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="25.2884" length2="1.5" x2="23.8403"/>
                                        <line end1="none" end2="none" y1="-2.1637" antialias="false" y2="-0.237483" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="24.4793" length2="1.5" x2="23.7304"/>
                                        <line end1="none" end2="none" y1="-1.51407" antialias="false" y2="-1.41907" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="26.9628" length2="1.5" x2="26.9259"/>
                                        <line end1="none" end2="none" y1="-9.47867" antialias="false" y2="-11.7118" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="13.1981" length2="1.5" x2="11.7876"/>
                                        <line end1="none" end2="none" y1="-12.5183" antialias="false" y2="-6.88204" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="1.17165" length2="1.5" x2="-1.01979"/>
                                        <line end1="none" end2="none" y1="-20.0844" antialias="false" y2="-16.0757" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-16.282" length2="1.5" x2="-9.19721"/>
                                        <line end1="none" end2="none" y1="-20.1743" antialias="false" y2="-13.1186" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-4.15296" length2="1.5" x2="8.31637"/>
                                        <line end1="none" end2="none" y1="-14.4044" antialias="false" y2="-12.2278" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-45.0145" length2="1.5" x2="-47.74"/>
                                        <line end1="none" end2="none" y1="-12.6114" antialias="false" y2="-11.1576" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-46.6971" length2="1.5" x2="-41.236"/>
                                        <line end1="none" end2="none" y1="-30.9795" antialias="false" y2="-34.8878" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-37.4504" length2="1.5" x2="-52.1319"/>
                                        <line end1="none" end2="none" y1="-35.6043" antialias="false" y2="-31.6066" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-51.2349" length2="1.5" x2="-36.2182"/>
                                        <line end1="none" end2="none" y1="-12.2278" antialias="false" y2="-10.4964" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-47.74" length2="1.5" x2="-41.236"/>
                                        <line end1="none" end2="none" y1="2.60674" antialias="false" y2="6.20567" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="34.911" length2="1.5" x2="33.5117"/>
                                        <line end1="none" end2="none" y1="3.88804" antialias="false" y2="5.63496" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="37.7576" length2="1.5" x2="38.29"/>
                                        <line end1="none" end2="none" y1="2.99258" antialias="false" y2="6.3067" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="35.593" length2="1.5" x2="34.3044"/>
                                        <line end1="none" end2="none" y1="-3.16752" antialias="false" y2="3.88804" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="25.2884" length2="1.5" x2="37.7576"/>
                                        <line end1="none" end2="none" y1="16.4333" antialias="false" y2="23.4973" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-30.6032" length2="1.5" x2="-4.06786"/>
                                        <line end1="none" end2="none" y1="-11.8601" antialias="false" y2="-10.9243" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-63.0125" length2="1.5" x2="-56.5495"/>
                                        <line end1="none" end2="none" y1="-10.9865" antialias="false" y2="-8.36331" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-58.5539" length2="1.5" x2="-58.3112"/>
                                        <line end1="none" end2="none" y1="-10.9865" antialias="false" y2="-10.8837" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-58.5539" length2="1.5" x2="-57.8422"/>
                                        <line end1="none" end2="none" y1="-10.9243" antialias="false" y2="-10.6378" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-56.5495" length2="1.5" x2="-56.9079"/>
                                        <line end1="none" end2="none" y1="-10.8837" antialias="false" y2="-8.56" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-57.8422" length2="1.5" x2="-57.6273"/>
                                        <line end1="none" end2="none" y1="-10.0552" antialias="false" y2="-7.96117" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-54.6101" length2="1.5" x2="-57.2321"/>
                                        <line end1="none" end2="none" y1="-7.93829" antialias="false" y2="-9.94255" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-57.1093" length2="1.5" x2="-54.5998"/>
                                        <line end1="none" end2="none" y1="-8.66574" antialias="false" y2="-8.00987" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-66.753" length2="1.5" x2="-66.3128"/>
                                        <line end1="none" end2="none" y1="-9.02224" antialias="false" y2="-8.66574" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-66.566" length2="1.5" x2="-66.753"/>
                                        <line end1="none" end2="none" y1="-8.00987" antialias="false" y2="-8.25232" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-66.3128" length2="1.5" x2="-66.1857"/>
                                        <line end1="none" end2="none" y1="-8.18862" antialias="false" y2="-8.00987" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-66.089" length2="1.5" x2="-66.3128"/>
                                        <line end1="none" end2="none" y1="-8.25232" antialias="false" y2="-7.47814" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-66.1857" length2="1.5" x2="-65.0086"/>
                                        <line end1="none" end2="none" y1="-8.51326" antialias="false" y2="-8.63356" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-63.0519" length2="1.5" x2="-62.9013"/>
                                        <line end1="none" end2="none" y1="-5.77051" antialias="false" y2="-5.81341" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-65.9045" length2="1.5" x2="-66.1846"/>
                                        <line end1="none" end2="none" y1="-7.57041" antialias="false" y2="-8.09755" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-54.9152" length2="1.5" x2="-54.964"/>
                                        <line end1="none" end2="none" y1="-8.09755" antialias="false" y2="-7.64538" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-54.964" length2="1.5" x2="-55.5301"/>
                                        <line end1="none" end2="none" y1="-8.1815" antialias="false" y2="-8.06132" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-59.8171" length2="1.5" x2="-59.9677"/>
                                        <line end1="none" end2="none" y1="-7.57041" antialias="false" y2="-7.53866" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-54.9152" length2="1.5" x2="-54.955"/>
                                        <line end1="none" end2="none" y1="-1.62616" antialias="false" y2="-0.434067" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="23.6033" length2="1.5" x2="23.1398"/>
                                        <line end1="none" end2="none" y1="-0.954204" antialias="false" y2="-0.78378" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="22.965" length2="1.5" x2="22.8987"/>
                                        <line end1="none" end2="none" y1="-0.329646" antialias="false" y2="0.82096" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="21.7349" length2="1.5" x2="20.2868"/>
                                        <line end1="none" end2="none" y1="-2.01692" antialias="false" y2="0.82096" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="23.8403" length2="1.5" x2="20.2868"/>
                                        <line end1="none" end2="none" y1="0.82096" antialias="false" y2="4.90533" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="20.2868" length2="1.5" x2="18.6989"/>
                                        <line end1="none" end2="none" y1="4.90533" antialias="false" y2="-0.239782" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="18.6989" length2="1.5" x2="9.60598"/>
                                        <line end1="none" end2="none" y1="-5.67594" antialias="false" y2="-5.2901" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-0.20593" length2="1.5" x2="0.47602"/>
                                        <line end1="none" end2="none" y1="-5.08454" antialias="false" y2="-8.06132" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-43.9235" length2="1.5" x2="-59.9677"/>
                                        <line end1="none" end2="none" y1="-1.98288" antialias="false" y2="-8.06132" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-59.4054" length2="1.5" x2="-59.9677"/>
                                        <line end1="none" end2="none" y1="-8.51326" antialias="false" y2="-2.55719" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-63.0519" length2="1.5" x2="-62.5007"/>
                                        <line end1="none" end2="none" y1="-8.51326" antialias="false" y2="-9.02224" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-63.0519" length2="1.5" x2="-66.566"/>
                                        <line end1="none" end2="none" y1="-7.96117" antialias="false" y2="-7.12185" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-57.2321" length2="1.5" x2="-52.7079"/>
                                        <line end1="none" end2="none" y1="-8.63356" antialias="false" y2="-2.06256" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-62.9013" length2="1.5" x2="-62.2933"/>
                                        <line end1="none" end2="none" y1="-11.8601" antialias="false" y2="-9.02224" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-63.0125" length2="1.5" x2="-66.566"/>
                                        <line end1="none" end2="none" y1="-9.8552" antialias="false" y2="-10.9243" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-50.7876" length2="1.5" x2="-56.5495"/>
                                        <line end1="none" end2="none" y1="11.7187" antialias="false" y2="12.6102" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-68.1857" length2="1.5" x2="-64.8366"/>
                                        <line end1="none" end2="none" y1="9.80492" antialias="false" y2="11.7187" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-65.7894" length2="1.5" x2="-68.1857"/>
                                        <line end1="none" end2="none" y1="8.44055" antialias="false" y2="9.80503" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-37.3244" length2="1.5" x2="-37.926"/>
                                        <line end1="none" end2="none" y1="10.4618" antialias="false" y2="10.4949" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-38.4821" length2="1.5" x2="-38.5324"/>
                                        <line end1="none" end2="none" y1="11.1517" antialias="false" y2="12.4942" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-39.0885" length2="1.5" x2="-39.6805"/>
                                        <line end1="none" end2="none" y1="10.6946" antialias="false" y2="11.7187" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-68.1857" length2="1.5" x2="-68.1857"/>
                                        <line end1="none" end2="none" y1="-2.97532" antialias="false" y2="-2.52195" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-69.7381" length2="1.5" x2="-69.976"/>
                                        <line end1="none" end2="none" y1="-2.86444" antialias="false" y2="-2.97532" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-69.0121" length2="1.5" x2="-69.7381"/>
                                        <line end1="none" end2="none" y1="-2.62199" antialias="false" y2="-2.86444" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-69.1393" length2="1.5" x2="-69.0121"/>
                                        <line end1="none" end2="none" y1="-1.84781" antialias="false" y2="-2.62199" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-67.9622" length2="1.5" x2="-69.1393"/>
                                        <line end1="none" end2="none" y1="7.48598" antialias="false" y2="7.55165" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-38.1322" length2="1.5" x2="-37.8858"/>
                                        <line end1="none" end2="none" y1="-1.2968" antialias="false" y2="-2.20847" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-59.6307" length2="1.5" x2="-60.2066"/>
                                        <line end1="none" end2="none" y1="-2.47269" antialias="false" y2="-2.20847" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-60.2727" length2="1.5" x2="-60.2066"/>
                                        <line end1="none" end2="none" y1="-2.20847" antialias="false" y2="-2.06114" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-60.2066" length2="1.5" x2="-59.4125"/>
                                        <line end1="none" end2="none" y1="-2.52195" antialias="false" y2="12.6102" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-69.976" length2="1.5" x2="-64.8366"/>
                                        <line end1="none" end2="none" y1="4.46553" antialias="false" y2="3.88804" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="37.0345" length2="1.5" x2="37.7576"/>
                                        <line end1="none" end2="none" y1="6.28087" antialias="false" y2="6.16057" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="33.4175" length2="1.5" x2="33.5682"/>
                                        <line end1="none" end2="none" y1="6.72592" antialias="false" y2="6.28087" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="34.2041" length2="1.5" x2="33.4175"/>
                                        <line end1="none" end2="none" y1="5.63496" antialias="false" y2="8.47284" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="38.29" length2="1.5" x2="34.7365"/>
                                        <line end1="none" end2="none" y1="18.6451" antialias="false" y2="17.2262" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="52.3855" length2="1.5" x2="54.1623"/>
                                        <line end1="none" end2="none" y1="11.1086" antialias="false" y2="17.2262" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="43.3507" length2="1.5" x2="54.1623"/>
                                        <line end1="none" end2="none" y1="23.4231" antialias="false" y2="17.2262" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="54.1623" length2="1.5" x2="54.1623"/>
                                        <line end1="none" end2="none" y1="13.7086" antialias="false" y2="14.7555" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="46.6976" length2="1.5" x2="45.3866"/>
                                        <line end1="none" end2="none" y1="11.1086" antialias="false" y2="11.5219" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="43.3507" length2="1.5" x2="42.8332"/>
                                        <line end1="none" end2="none" y1="15.2204" antialias="false" y2="17.5539" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-34.3316" length2="1.5" x2="-37.2534"/>
                                        <line end1="none" end2="none" y1="15.8344" antialias="false" y2="18.6723" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-34.6738" length2="1.5" x2="-38.2273"/>
                                        <line end1="none" end2="none" y1="15.7713" antialias="false" y2="15.3855" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="51.009" length2="1.5" x2="50.327"/>
                                        <line end1="none" end2="none" y1="15.7713" antialias="false" y2="19.0854" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="51.009" length2="1.5" x2="49.7198"/>
                                        <line end1="none" end2="none" y1="19.0595" antialias="false" y2="18.9392" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="48.8332" length2="1.5" x2="48.9838"/>
                                        <line end1="none" end2="none" y1="15.3855" antialias="false" y2="18.9844" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="50.327" length2="1.5" x2="48.9275"/>
                                        <line end1="none" end2="none" y1="6.14131" antialias="false" y2="5.8183" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="43.7358" length2="1.5" x2="43.1165"/>
                                        <line end1="none" end2="none" y1="16.0344" antialias="false" y2="14.0505" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-38.7262" length2="1.5" x2="-38.7262"/>
                                        <line end1="none" end2="none" y1="14.8907" antialias="false" y2="16.3552" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-38.468" length2="1.5" x2="-38.763"/>
                                        <line end1="none" end2="none" y1="16.0078" antialias="false" y2="16.0344" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-38.6931" length2="1.5" x2="-38.7262"/>
                                        <line end1="none" end2="none" y1="15.0119" antialias="false" y2="16.4171" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-35.1149" length2="1.5" x2="-36.8744"/>
                                        <line end1="none" end2="none" y1="16.4171" antialias="false" y2="16.1308" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-36.8744" length2="1.5" x2="-37.9494"/>
                                        <line end1="none" end2="none" y1="14.7323" antialias="false" y2="16.1027" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-36.1649" length2="1.5" x2="-31.0172"/>
                                        <line end1="none" end2="none" y1="16.9152" antialias="false" y2="16.4171" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-36.8744" length2="1.5" x2="-36.8744"/>
                                        <line end1="none" end2="none" y1="14.6835" antialias="false" y2="14.8425" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-37.1765" length2="1.5" x2="-36.5789"/>
                                        <line end1="none" end2="none" y1="14.8425" antialias="false" y2="14.7323" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-36.5789" length2="1.5" x2="-36.1649"/>
                                        <line end1="none" end2="none" y1="15.1364" antialias="false" y2="16.9152" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-34.6471" length2="1.5" x2="-36.8744"/>
                                        <line end1="none" end2="none" y1="14.2829" antialias="false" y2="15.6844" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-40.0408" length2="1.5" x2="-40.0408"/>
                                        <line end1="none" end2="none" y1="16.3552" antialias="false" y2="15.9108" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-38.763" length2="1.5" x2="-40.4322"/>
                                        <line end1="none" end2="none" y1="16.1027" antialias="false" y2="16.4333" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-31.0172" length2="1.5" x2="-30.6032"/>
                                        <line end1="none" end2="none" y1="15.6844" antialias="false" y2="16.0344" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-40.0408" length2="1.5" x2="-38.7262"/>
                                        <line end1="none" end2="none" y1="16.1308" antialias="false" y2="15.0287" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-37.9494" length2="1.5" x2="-37.9494"/>
                                        <line end1="none" end2="none" y1="14.3528" antialias="false" y2="14.6835" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-37.5905" length2="1.5" x2="-37.1765"/>
                                        <line end1="none" end2="none" y1="13.9464" antialias="false" y2="7.18837" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="39.7972" length2="1.5" x2="42.4248"/>
                                        <line end1="none" end2="none" y1="14.0505" antialias="false" y2="14.3528" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-38.7262" length2="1.5" x2="-37.5905"/>
                                        <line end1="none" end2="none" y1="15.0287" antialias="false" y2="14.8907" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-37.9494" length2="1.5" x2="-38.468"/>
                                        <line end1="none" end2="none" y1="14.3121" antialias="false" y2="14.8907" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-37.7435" length2="1.5" x2="-38.468"/>
                                        <line end1="none" end2="none" y1="10.2828" antialias="false" y2="10.4618" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-38.2579" length2="1.5" x2="-38.4821"/>
                                        <line end1="none" end2="none" y1="10.2471" antialias="false" y2="10.4949" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-38.2222" length2="1.5" x2="-38.5324"/>
                                        <line end1="none" end2="none" y1="10.5794" antialias="false" y2="10.2128" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-38.6492" length2="1.5" x2="-38.1901"/>
                                        <line end1="none" end2="none" y1="9.47809" antialias="false" y2="12.8947" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-69.9785" length2="1.5" x2="-69.9785"/>
                                        <line end1="none" end2="none" y1="6.62522" antialias="false" y2="8.89873" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-66.8692" length2="1.5" x2="-69.7159"/>
                                        <line end1="none" end2="none" y1="9.00885" antialias="false" y2="10.6302" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-66.0597" length2="1.5" x2="-68.0898"/>
                                        <line end1="none" end2="none" y1="9.67927" antialias="false" y2="6.84128" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="35.3509" length2="1.5" x2="38.9044"/>
                                        <line end1="none" end2="none" y1="11.3596" antialias="false" y2="11.4334" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="42.3417" length2="1.5" x2="42.2492"/>
                                        <line end1="none" end2="none" y1="5.8183" antialias="false" y2="6.31414" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="43.1165" length2="1.5" x2="42.4955"/>
                                        <line end1="none" end2="none" y1="5.8183" antialias="false" y2="6.7338" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="43.1165" length2="1.5" x2="42.7606"/>
                                        <line end1="none" end2="none" y1="6.26926" antialias="false" y2="6.16813" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="40.5429" length2="1.5" x2="40.8095"/>
                                        <line end1="none" end2="none" y1="6.16813" antialias="false" y2="7.32935" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="40.8095" length2="1.5" x2="41.543"/>
                                        <line end1="none" end2="none" y1="6.8577" antialias="false" y2="6.31414" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="42.8388" length2="1.5" x2="42.4955"/>
                                        <line end1="none" end2="none" y1="7.32935" antialias="false" y2="9.67927" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="41.543" length2="1.5" x2="35.3509"/>
                                        <line end1="none" end2="none" y1="12.8947" antialias="false" y2="17.1996" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-69.9785" length2="1.5" x2="-53.8071"/>
                                        <line end1="none" end2="none" y1="6.14131" antialias="false" y2="12.9945" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="43.7358" length2="1.5" x2="41.0714"/>
                                        <line end1="none" end2="none" y1="-33.3881" antialias="false" y2="-34.0219" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-54.5025" length2="1.5" x2="-53.709"/>
                                        <line end1="none" end2="none" y1="-34.0219" antialias="false" y2="-34.0219" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-52.053" length2="1.5" x2="-53.709"/>
                                        <line end1="none" end2="none" y1="-32.7662" antialias="false" y2="-33.4827" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-54.7884" length2="1.5" x2="-53.8914"/>
                                        <line end1="none" end2="none" y1="-33.3881" antialias="false" y2="-32.9946" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-54.5025" length2="1.5" x2="-54.5025"/>
                                        <line end1="none" end2="none" y1="-33.1914" antialias="false" y2="-33.3881" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-54.256" length2="1.5" x2="-54.5025"/>
                                        <line end1="none" end2="none" y1="-32.7662" antialias="false" y2="-17.3992" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-54.7884" length2="1.5" x2="-53.3663"/>
                                        <line end1="none" end2="none" y1="-29.4735" antialias="false" y2="-31.6066" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-24.7208" length2="1.5" x2="-36.2182"/>
                                        <line end1="none" end2="none" y1="-28.51" antialias="false" y2="-29.4221" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-31.8897" length2="1.5" x2="-30.7474"/>
                                        <line end1="none" end2="none" y1="-28.0534" antialias="false" y2="-29.5595" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-13.9462" length2="1.5" x2="-14.7266"/>
                                        <line end1="none" end2="none" y1="-29.9224" antialias="false" y2="-29.9906" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-15.8172" length2="1.5" x2="-15.5389"/>
                                        <line end1="none" end2="none" y1="-29.4735" antialias="false" y2="-26.6356" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-24.7208" length2="1.5" x2="-28.2743"/>
                                        <line end1="none" end2="none" y1="-28.1314" antialias="false" y2="-29.4735" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-22.311" length2="1.5" x2="-24.7208"/>
                                        <line end1="none" end2="none" y1="-29.9224" antialias="false" y2="-27.0845" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-15.8172" length2="1.5" x2="-19.3707"/>
                                        <line end1="none" end2="none" y1="-29.9906" antialias="false" y2="-27.1527" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-15.5389" length2="1.5" x2="-19.0924"/>
                                        <line end1="none" end2="none" y1="-29.5595" antialias="false" y2="-26.7217" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-14.7266" length2="1.5" x2="-18.2801"/>
                                        <line end1="none" end2="none" y1="-10.208" antialias="false" y2="-14.17" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-41.236" length2="1.5" x2="-41.236"/>
                                        <line end1="none" end2="none" y1="-10.0552" antialias="false" y2="-9.94255" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-54.6101" length2="1.5" x2="-54.5998"/>
                                        <line end1="none" end2="none" y1="-9.94255" antialias="false" y2="-9.64964" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-54.5998" length2="1.5" x2="-53.0205"/>
                                        <line end1="none" end2="none" y1="-7.46861" antialias="false" y2="-7.92089" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-54.5777" length2="1.5" x2="-54.0114"/>
                                        <line end1="none" end2="none" y1="-8.58058" antialias="false" y2="-9.10761" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-53.6503" length2="1.5" x2="-53.6992"/>
                                        <line end1="none" end2="none" y1="-9.64964" antialias="false" y2="-9.1225" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-53.0205" length2="1.5" x2="-52.9718"/>
                                        <line end1="none" end2="none" y1="-9.64964" antialias="false" y2="-9.10761" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-53.0205" length2="1.5" x2="-53.6992"/>
                                        <line end1="none" end2="none" y1="-9.05245" antialias="false" y2="-9.1225" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-52.5945" length2="1.5" x2="-52.9718"/>
                                        <line end1="none" end2="none" y1="-9.1225" antialias="false" y2="-8.58058" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-52.9718" length2="1.5" x2="-53.6503"/>
                                        <line end1="none" end2="none" y1="-7.92647" antialias="false" y2="-7.81406" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-52.2871" length2="1.5" x2="-52.2768"/>
                                        <line end1="none" end2="none" y1="-7.58486" antialias="false" y2="-7.81406" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-52.1282" length2="1.5" x2="-52.2768"/>
                                        <line end1="none" end2="none" y1="-7.6178" antialias="false" y2="-7.92647" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-52.0869" length2="1.5" x2="-52.2871"/>
                                        <line end1="none" end2="none" y1="-5.08454" antialias="false" y2="-10.208" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-43.9235" length2="1.5" x2="-41.236"/>
                                        <line end1="none" end2="none" y1="-7.92647" antialias="false" y2="-8.58769" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-52.2871" length2="1.5" x2="-51.4591"/>
                                        <line end1="none" end2="none" y1="-7.12185" antialias="false" y2="-7.6178" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-52.7079" length2="1.5" x2="-52.0869"/>
                                        <line end1="none" end2="none" y1="-9.47287" antialias="false" y2="-9.23535" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-52.0682" length2="1.5" x2="-50.7876"/>
                                        <line end1="none" end2="none" y1="-8.93095" antialias="false" y2="-9.47287" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-52.7467" length2="1.5" x2="-52.0682"/>
                                        <line end1="none" end2="none" y1="-9.34601" antialias="false" y2="-10.0552" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-50.7876" length2="1.5" x2="-54.6101"/>
                                        <line end1="none" end2="none" y1="-8.58769" antialias="false" y2="-8.70569" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-51.4591" length2="1.5" x2="-50.7876"/>
                                        <line end1="none" end2="none" y1="-30.9795" antialias="false" y2="-29.5743" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-37.4504" length2="1.5" x2="-39.2099"/>
                                        <line end1="none" end2="none" y1="-29.5551" antialias="false" y2="-30.5174" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-37.6897" length2="1.5" x2="-36.4847"/>
                                        <line end1="none" end2="none" y1="-28.7687" antialias="false" y2="-31.6066" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-39.7717" length2="1.5" x2="-36.2182"/>
                                        <line end1="none" end2="none" y1="-28.0534" antialias="false" y2="-25.7586" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-13.9462" length2="1.5" x2="-14.8385"/>
                                        <line end1="none" end2="none" y1="-28.0534" antialias="false" y2="-25.2155" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-13.9462" length2="1.5" x2="-17.4997"/>
                                        <line end1="none" end2="none" y1="-26.5052" antialias="false" y2="-27.5902" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-21.5368" length2="1.5" x2="-22.0989"/>
                                        <line end1="none" end2="none" y1="-28.1314" antialias="false" y2="-27.7714" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-22.311" length2="1.5" x2="-21.8722"/>
                                        <line end1="none" end2="none" y1="-27.7714" antialias="false" y2="-24.9334" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-21.8722" length2="1.5" x2="-25.4257"/>
                                        <line end1="none" end2="none" y1="-28.1314" antialias="false" y2="-25.2935" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-22.311" length2="1.5" x2="-25.8645"/>
                                        <line end1="none" end2="none" y1="-26.5052" antialias="false" y2="-23.6673" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-21.5368" length2="1.5" x2="-25.0903"/>
                                        <line end1="none" end2="none" y1="-26.5052" antialias="false" y2="-27.0356" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-21.5368" length2="1.5" x2="-19.3717"/>
                                        <line end1="none" end2="none" y1="-25.2935" antialias="false" y2="-26.6356" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-25.8645" length2="1.5" x2="-28.2743"/>
                                        <line end1="none" end2="none" y1="-27.1527" antialias="false" y2="-27.0845" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-19.0924" length2="1.5" x2="-19.3707"/>
                                        <line end1="none" end2="none" y1="-27.0845" antialias="false" y2="-26.4135" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-19.3707" length2="1.5" x2="-19.3836"/>
                                        <line end1="none" end2="none" y1="-25.2155" antialias="false" y2="-26.7217" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-17.4997" length2="1.5" x2="-18.2801"/>
                                        <line end1="none" end2="none" y1="-25.7586" antialias="false" y2="-24.1687" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-14.8385" length2="1.5" x2="-14.6939"/>
                                        <line end1="none" end2="none" y1="-25.7586" antialias="false" y2="-22.9207" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-14.8385" length2="1.5" x2="-18.392"/>
                                        <line end1="none" end2="none" y1="-26.4832" antialias="false" y2="-25.2868" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-19.0988" length2="1.5" x2="-18.479"/>
                                        <line end1="none" end2="none" y1="-26.4135" antialias="false" y2="-26.4832" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-19.3836" length2="1.5" x2="-19.0988"/>
                                        <line end1="none" end2="none" y1="-22.9207" antialias="false" y2="-25.2155" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-18.392" length2="1.5" x2="-17.4997"/>
                                        <line end1="none" end2="none" y1="-24.1687" antialias="false" y2="-21.3308" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-14.6939" length2="1.5" x2="-18.2474"/>
                                        <line end1="none" end2="none" y1="-20.0844" antialias="false" y2="-24.1687" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-16.282" length2="1.5" x2="-14.6939"/>
                                        <line end1="none" end2="none" y1="-21.3308" antialias="false" y2="-22.9207" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-18.2474" length2="1.5" x2="-18.392"/>
                                        <line end1="none" end2="none" y1="-17.2466" antialias="false" y2="-21.3308" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-19.8355" length2="1.5" x2="-18.2474"/>
                                        <line end1="none" end2="none" y1="-20.1743" antialias="false" y2="-19.0236" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-4.15296" length2="1.5" x2="-5.60093"/>
                                        <line end1="none" end2="none" y1="-17.3363" antialias="false" y2="-16.1857" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-7.70646" length2="1.5" x2="-9.15443"/>
                                        <line end1="none" end2="none" y1="-14.2652" antialias="false" y2="-14.5497" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="14.5912" length2="1.5" x2="15.3411"/>
                                        <line end1="none" end2="none" y1="-10.2808" antialias="false" y2="-10.7258" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="4.76287" length2="1.5" x2="3.97627"/>
                                        <line end1="none" end2="none" y1="-8.48875" antialias="false" y2="-8.53373" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="5.17619" length2="1.5" x2="5.29498"/>
                                        <line end1="none" end2="none" y1="-11.2933" antialias="false" y2="-10.1654" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="8.7505" length2="1.5" x2="9.46316"/>
                                        <line end1="none" end2="none" y1="-11.7118" antialias="false" y2="-11.4273" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="11.7876" length2="1.5" x2="11.0377"/>
                                        <line end1="none" end2="none" y1="-10.7374" antialias="false" y2="-10.8386" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="11.1016" length2="1.5" x2="11.3682"/>
                                        <line end1="none" end2="none" y1="-11.4273" antialias="false" y2="-10.7374" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="11.0377" length2="1.5" x2="11.1016"/>
                                        <line end1="none" end2="none" y1="-0.329646" antialias="false" y2="-3.16752" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="21.7349" length2="1.5" x2="25.2884"/>
                                        <line end1="none" end2="none" y1="-0.239782" antialias="false" y2="-9.47867" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="9.60598" length2="1.5" x2="13.1981"/>
                                        <line end1="none" end2="none" y1="-10.8386" antialias="false" y2="-9.67733" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="11.3682" length2="1.5" x2="12.1017"/>
                                        <line end1="none" end2="none" y1="-9.67733" antialias="false" y2="-7.32752" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="12.1017" length2="1.5" x2="5.90966"/>
                                        <line end1="none" end2="none" y1="-7.32752" antialias="false" y2="-8.48875" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="5.90966" length2="1.5" x2="5.17619"/>
                                        <line end1="none" end2="none" y1="-8.53373" antialias="false" y2="-10.2808" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="5.29498" length2="1.5" x2="4.76287"/>
                                        <line end1="none" end2="none" y1="-10.1654" antialias="false" y2="-10.7855" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="9.46316" length2="1.5" x2="11.0972"/>
                                        <line end1="none" end2="none" y1="-10.7258" antialias="false" y2="-5.5968" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="3.97627" length2="1.5" x2="1.98206"/>
                                        <line end1="none" end2="none" y1="-7.26885" antialias="false" y2="-12.398" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-0.97321" length2="1.5" x2="1.021"/>
                                        <line end1="none" end2="none" y1="-12.398" antialias="false" y2="-17.3363" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="1.021" length2="1.5" x2="-7.70646"/>
                                        <line end1="none" end2="none" y1="-12.3165" antialias="false" y2="-14.5497" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="16.7516" length2="1.5" x2="15.3411"/>
                                        <line end1="none" end2="none" y1="-12.1014" antialias="false" y2="-17.2466" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-10.7425" length2="1.5" x2="-19.8355"/>
                                        <line end1="none" end2="none" y1="-19.0236" antialias="false" y2="-16.1857" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-5.60093" length2="1.5" x2="-9.15443"/>
                                        <line end1="none" end2="none" y1="-10.1654" antialias="false" y2="-7.32752" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="9.46316" length2="1.5" x2="5.90966"/>
                                        <line end1="none" end2="none" y1="-14.5497" antialias="false" y2="-11.7118" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="15.3411" length2="1.5" x2="11.7876"/>
                                        <line end1="none" end2="none" y1="-14.2652" antialias="false" y2="-11.4273" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="14.5912" length2="1.5" x2="11.0377"/>
                                        <line end1="none" end2="none" y1="-12.3165" antialias="false" y2="-9.47867" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="16.7516" length2="1.5" x2="13.1981"/>
                                        <line end1="none" end2="none" y1="-26.6356" antialias="false" y2="-28.7687" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-28.2743" length2="1.5" x2="-39.7717"/>
                                        <line end1="none" end2="none" y1="-28.7687" antialias="false" y2="-32.7662" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-39.7717" length2="1.5" x2="-54.7884"/>
                                        <line end1="none" end2="none" y1="-17.3992" antialias="false" y2="-14.17" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-53.3663" length2="1.5" x2="-41.236"/>
                                        <line end1="none" end2="none" y1="-33.4827" antialias="false" y2="-29.5743" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="-53.8914" length2="1.5" x2="-39.2099"/>
                                        <line end1="none" end2="none" y1="-3.07777" antialias="false" y2="-12.3165" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="13.1595" length2="1.5" x2="16.7516"/>
                                        <line end1="none" end2="none" y1="32.9754" antialias="false" y2="39.5138" style="line-style:normal;line-weight:thin;filling:none;color:black" length1="1.5" x1="5.45448" length2="1.5" x2="50.6088"/>
                                        <text x="-160" y="20" font="Sans Serif,9,-1,5,50,0,0,0,0,0" rotation="0" color="#000000" text="PTI  2,5 PE-L-N"/>
                                        <text x="-160" y="30" font="Sans Serif,6,-1,5,50,0,0,0,0,0" rotation="0" color="#000000" text="3213946"/>
                                        <arc x="78" y="2.5861" antialias="true" style="line-style:normal;line-weight:normal;filling:none;color:black" start="0" width="8" height="7.26389" angle="90"/>
                                        <arc x="78" y="2.5861" antialias="true" style="line-style:normal;line-weight:normal;filling:none;color:black" start="270" width="8" height="7.26389" angle="90"/>
                                        <ellipse x="74" y="13.4819" antialias="false" style="line-style:normal;line-weight:normal;filling:none;color:black" width="8" height="7.26389"/>
                                        <ellipse x="113.2" y="5.4917" antialias="false" style="line-style:normal;line-weight:normal;filling:none;color:black" width="1.6" height="1.45278"/>
                                        <line end1="none" end2="none" y1="6.218" antialias="false" y2="6.218" style="line-style:normal;line-weight:normal;filling:none;color:black" length1="1.5" x1="86" length2="1.5" x2="122"/>
                                        <line end1="none" end2="none" y1="17.1139" antialias="false" y2="17.1139" style="line-style:normal;line-weight:normal;filling:none;color:black" length1="1.5" x1="82" length2="1.5" x2="130"/>
                                        <line end1="none" end2="none" y1="28.0097" antialias="false" y2="28.0097" style="line-style:normal;line-weight:normal;filling:none;color:black" length1="1.5" x1="138" length2="1.5" x2="122"/>
                                        <line end1="none" end2="none" y1="28.0097" antialias="false" y2="31.6417" style="line-style:normal;line-weight:normal;filling:none;color:black" length1="1.5" x1="122" length2="1.5" x2="122"/>
                                        <line end1="none" end2="none" y1="31.6417" antialias="false" y2="31.6417" style="line-style:normal;line-weight:normal;filling:none;color:black" length1="1.5" x1="118" length2="1.5" x2="126"/>
                                        <line end1="none" end2="none" y1="33.8208" antialias="false" y2="33.8208" style="line-style:normal;line-weight:normal;filling:none;color:black" length1="1.5" x1="119.6" length2="1.5" x2="124.4"/>
                                        <line end1="none" end2="none" y1="36" antialias="false" y2="36" style="line-style:normal;line-weight:normal;filling:none;color:black" length1="1.5" x1="121.2" length2="1.5" x2="122.8"/>
                                        <text x="64" y="20" font="Sans Serif,9,-1,5,50,0,0,0,0,0" rotation="0" color="#000000" text="a"/>
                                        <text x="141" y="21" font="Sans Serif,7,-1,5,50,0,0,0,0,0" rotation="0" color="#000000" text="L"/>
                                        <text x="133" y="10" font="Sans Serif,7,-1,5,50,0,0,0,0,0" rotation="0" color="#000000" text="N"/>
                                        <text x="149" y="32" font="Sans Serif,7,-1,5,50,0,0,0,0,0" rotation="0" color="#000000" text="PE"/>
                                    </description>
                                </definition>
                            </element>
                            <element name="terminal_1-pol_pe.elmt">
                                <definition type="element" link_type="terminal" hotspot_x="9" hotspot_y="11" width="20" height="30" version="0.90">
                                    <uuid uuid="{9d92bb0b-1dc3-44d7-a6b9-7f90606a3c80}"/>
                                    <names>
                                        <name lang="de">1-Pol  PE-extern</name>
                                    </names>
                                    <kindInformations>
                                        <kindInformation name="type">generic</kindInformation>
                                        <kindInformation name="function">generic</kindInformation>
                                    </kindInformations>
                                    <elementInformations>
                                        <elementInformation name="unity" show="1"/>
                                        <elementInformation name="quantity" show="1"/>
                                        <elementInformation name="plant" show="1"/>
                                        <elementInformation name="comment" show="1"/>
                                        <elementInformation name="manufacturer" show="1"/>
                                        <elementInformation name="designation" show="1"/>
                                        <elementInformation name="label" show="1"/>
                                        <elementInformation name="manufacturer_reference" show="1"/>
                                        <elementInformation name="machine_manufacturer_reference" show="1"/>
                                        <elementInformation name="description" show="1"/>
                                        <elementInformation name="supplier" show="1"/>
                                    </elementInformations>
                                    <informations/>
                                    <description>
                                        <circle x="-2" y="-2" antialias="false" style="line-style:normal;line-weight:normal;filling:black;color:black" diameter="4"/>
                                        <line end1="none" end2="none" antialias="false" y1="2" y2="10" style="line-style:normal;line-weight:normal;filling:none;color:black" length1="1.5" x1="0" length2="1.5" x2="0"/>
                                        <dynamic_text frame="false" Halignment="AlignRight" x="-8" y="-20" z="4" font="Liberation Sans,9,-1,5,50,0,0,0,0,0" rotation="0" text_width="-1" uuid="{72429080-0aa7-40c6-86af-d95be686bd20}" keep_visual_rotation="true" text_from="ElementInfo" Valignment="AlignVCenter">
                                            <text/>
                                            <info_name>label</info_name>
                                        </dynamic_text>
                                        <dynamic_text frame="false" Halignment="AlignLeft" x="0" y="0" z="5" font="Liberation Sans,6,-1,5,50,0,0,0,0,0" rotation="0" text_width="-1" uuid="{915ce65c-8bb7-4d4f-b3cf-296e6d0dd4f6}" keep_visual_rotation="true" text_from="UserText" Valignment="AlignVCenter">
                                            <text>PE</text>
                                        </dynamic_text>
                                        <terminal type="Generic" x="0" y="-3" name="" uuid="{0e10681e-09ea-4cd5-9431-c1c92476a6ce}" orientation="n"/>
                                        <terminal type="Outer" x="0" y="10" name="PE" uuid="{21c9b876-a46a-4ac1-acc8-6bbbbd0b6cae}" orientation="s"/>
                                        <terminal type="Generic" x="-3" y="0" name="" uuid="{f81ea64b-1035-4f89-809b-990d7fbe371d}" orientation="w"/>
                                        <terminal type="Generic" x="0" y="-3" name="" uuid="{ac2b155d-3dff-4223-8afb-d9bdd0446f6d}" orientation="n"/>
                                        <terminal type="Generic" x="3" y="0" name="" uuid="{8c92e7c5-311a-44a2-9476-ee2850be2f98}" orientation="e"/>
                                    </description>
                                </definition>
                            </element>
                            <element name="terminal_1_pol_l_outher.elmt">
                                <definition type="element" link_type="terminal" hotspot_x="9" hotspot_y="14" width="20" height="30" version="0.90">
                                    <uuid uuid="{3e883740-a5c9-4436-af80-95ce1ca42729}"/>
                                    <names>
                                        <name lang="de">2-Pol  L-extern</name>
                                    </names>
                                    <kindInformations>
                                        <kindInformation name="type">generic</kindInformation>
                                        <kindInformation name="function">generic</kindInformation>
                                    </kindInformations>
                                    <elementInformations>
                                        <elementInformation name="plant" show="1"/>
                                        <elementInformation name="machine_manufacturer_reference" show="1"/>
                                        <elementInformation name="description" show="1"/>
                                        <elementInformation name="quantity" show="1"/>
                                        <elementInformation name="manufacturer_reference" show="1"/>
                                        <elementInformation name="label" show="1"/>
                                        <elementInformation name="supplier" show="1"/>
                                        <elementInformation name="unity" show="1"/>
                                        <elementInformation name="comment" show="1"/>
                                        <elementInformation name="designation" show="1"/>
                                        <elementInformation name="manufacturer" show="1"/>
                                    </elementInformations>
                                    <informations/>
                                    <description>
                                        <circle x="-2" y="-2" antialias="false" style="line-style:normal;line-weight:normal;filling:black;color:black" diameter="4"/>
                                        <line end1="none" end2="none" y1="-10" antialias="false" y2="10" style="line-style:normal;line-weight:normal;filling:none;color:black" length1="1.5" x1="0" length2="1.5" x2="0"/>
                                        <dynamic_text frame="false" Halignment="AlignRight" x="-8" y="-20" z="4" font="Liberation Sans,9,-1,5,50,0,0,0,0,0" rotation="0" text_width="-1" uuid="{72429080-0aa7-40c6-86af-d95be686bd20}" keep_visual_rotation="true" text_from="ElementInfo" Valignment="AlignVCenter">
                                            <text/>
                                            <info_name>label</info_name>
                                        </dynamic_text>
                                        <dynamic_text frame="false" Halignment="AlignLeft" x="0" y="0" z="5" font="Liberation Sans,6,-1,5,50,0,0,0,0,0" rotation="0" text_width="-1" uuid="{915ce65c-8bb7-4d4f-b3cf-296e6d0dd4f6}" keep_visual_rotation="true" text_from="UserText" Valignment="AlignVCenter">
                                            <text>L</text>
                                        </dynamic_text>
                                        <dynamic_text frame="false" Halignment="AlignLeft" x="0" y="-20" z="6" font="Liberation Sans,6,-1,5,50,0,0,0,0,0,Regular" rotation="0" text_width="-1" uuid="{4b840d1f-e80b-4f05-a1a1-c98dfeae20b6}" keep_visual_rotation="false" text_from="UserText" Valignment="AlignTop">
                                            <text>a</text>
                                        </dynamic_text>
                                        <terminal type="Outer" x="0" y="10" name="L" uuid="{35271def-cab7-4233-ac19-e266ac1ff062}" orientation="s"/>
                                        <terminal type="Generic" x="-3" y="0" name="" uuid="{8c73d922-158b-428b-9ae5-ec6816fef769}" orientation="w"/>
                                        <terminal type="Generic" x="3" y="0" name="" uuid="{d65afc43-a19d-4c71-a0ca-c70585657e20}" orientation="e"/>
                                        <terminal type="Inner" x="0" y="-10" name="a" uuid="{b7d59af5-c33d-4340-a941-e3410d6a0f93}" orientation="n"/>
                                    </description>
                                </definition>
                            </element>
                            <element name="terminal_1pol_.elmt">
                                <definition type="element" link_type="terminal" hotspot_x="9" hotspot_y="11" width="20" height="30" version="0.90">
                                    <uuid uuid="{5c95c94a-b287-4fd9-970d-ac8b3c241d7a}"/>
                                    <names>
                                        <name lang="de">1-Pol  L-extern</name>
                                    </names>
                                    <kindInformations>
                                        <kindInformation name="type">generic</kindInformation>
                                        <kindInformation name="function">generic</kindInformation>
                                    </kindInformations>
                                    <elementInformations>
                                        <elementInformation name="unity" show="1"/>
                                        <elementInformation name="quantity" show="1"/>
                                        <elementInformation name="plant" show="1"/>
                                        <elementInformation name="comment" show="1"/>
                                        <elementInformation name="manufacturer" show="1"/>
                                        <elementInformation name="label" show="1"/>
                                        <elementInformation name="designation" show="1"/>
                                        <elementInformation name="manufacturer_reference" show="1"/>
                                        <elementInformation name="machine_manufacturer_reference" show="1"/>
                                        <elementInformation name="description" show="1"/>
                                        <elementInformation name="supplier" show="1"/>
                                    </elementInformations>
                                    <informations/>
                                    <description>
                                        <circle x="-2" y="-2" antialias="false" style="line-style:normal;line-weight:normal;filling:black;color:black" diameter="4"/>
                                        <line end1="none" end2="none" antialias="false" y1="-1" y2="10" style="line-style:normal;line-weight:normal;filling:none;color:black" length1="1.5" x1="0" length2="1.5" x2="0"/>
                                        <dynamic_text frame="false" Halignment="AlignRight" x="-8" y="-20" z="4" font="Liberation Sans,9,-1,5,50,0,0,0,0,0" rotation="0" text_width="-1" uuid="{72429080-0aa7-40c6-86af-d95be686bd20}" keep_visual_rotation="true" text_from="ElementInfo" Valignment="AlignVCenter">
                                            <text/>
                                            <info_name>label</info_name>
                                        </dynamic_text>
                                        <dynamic_text frame="false" Halignment="AlignLeft" x="0" y="0" z="5" font="Liberation Sans,6,-1,5,50,0,0,0,0,0" rotation="0" text_width="-1" uuid="{915ce65c-8bb7-4d4f-b3cf-296e6d0dd4f6}" keep_visual_rotation="true" text_from="UserText" Valignment="AlignVCenter">
                                            <text>L</text>
                                        </dynamic_text>
                                        <terminal type="Generic" x="0" y="-3" name="" uuid="{c0e51d7b-ec26-47fa-967f-9257fa77cfb3}" orientation="n"/>
                                        <terminal type="Outer" x="0" y="10" name="L" uuid="{af632175-30f3-43a0-9af9-b3d189aa8d72}" orientation="s"/>
                                        <terminal type="Generic" x="-3" y="0" name="" uuid="{a0b4a59a-3302-4e8e-b912-fe2705aaaf56}" orientation="w"/>
                                        <terminal type="Generic" x="3" y="0" name="" uuid="{0a503f13-eaad-4653-b8db-d83927ca3367}" orientation="e"/>
                                    </description>
                                </definition>
                            </element>
                            <element name="terminal_1pol_n_intern.elmt">
                                <definition type="element" link_type="terminal" hotspot_x="9" hotspot_y="11" width="20" height="30" version="0.90">
                                    <uuid uuid="{8c46c230-f511-4ba4-96d3-78a59b7dce7d}"/>
                                    <names>
                                        <name lang="de">1-Pol  a-intern</name>
                                    </names>
                                    <kindInformations>
                                        <kindInformation name="type">generic</kindInformation>
                                        <kindInformation name="function">generic</kindInformation>
                                    </kindInformations>
                                    <elementInformations>
                                        <elementInformation name="comment" show="1"/>
                                        <elementInformation name="description" show="1"/>
                                        <elementInformation name="designation" show="1"/>
                                        <elementInformation name="quantity" show="1"/>
                                        <elementInformation name="plant" show="1"/>
                                        <elementInformation name="manufacturer_reference" show="1"/>
                                        <elementInformation name="label" show="1"/>
                                        <elementInformation name="supplier" show="1"/>
                                        <elementInformation name="machine_manufacturer_reference" show="1"/>
                                        <elementInformation name="manufacturer" show="1"/>
                                        <elementInformation name="unity" show="1"/>
                                    </elementInformations>
                                    <informations/>
                                    <description>
                                        <circle x="-2" y="-2" antialias="false" style="line-style:normal;line-weight:normal;filling:black;color:black" diameter="4"/>
                                        <line end1="none" end2="none" y1="2" antialias="false" y2="10" style="line-style:normal;line-weight:normal;filling:none;color:black" x1="0" length1="1.5" x2="0" length2="1.5"/>
                                        <dynamic_text Halignment="AlignRight" frame="false" x="-10" y="-20" rotation="0" font="Liberation Sans,9,-1,5,50,0,0,0,0,0" z="4" text_width="-1" uuid="{72429080-0aa7-40c6-86af-d95be686bd20}" keep_visual_rotation="true" Valignment="AlignVCenter" text_from="ElementInfo">
                                            <text/>
                                            <info_name>label</info_name>
                                        </dynamic_text>
                                        <dynamic_text Halignment="AlignLeft" frame="false" x="0" y="0" rotation="0" font="Liberation Sans,6,-1,5,50,0,0,0,0,0" z="5" text_width="-1" uuid="{915ce65c-8bb7-4d4f-b3cf-296e6d0dd4f6}" keep_visual_rotation="true" Valignment="AlignVCenter" text_from="UserText">
                                            <text>a</text>
                                        </dynamic_text>
                                        <terminal type="Generic" x="3" y="0" name="" uuid="{8cdc5e8c-0b0b-438d-b563-f281786659fa}" orientation="e"/>
                                        <terminal type="Inner" x="0" y="10" name="a" uuid="{a83e4ef0-fe46-4960-9a68-f995adb3ab4c}" orientation="s"/>
                                        <terminal type="Generic" x="-3" y="0" name="" uuid="{612920a8-eb0c-4ee5-ab5a-26c45d6086d6}" orientation="w"/>
                                        <terminal type="Generic" x="0" y="-3" name="" uuid="{758d97df-8af7-4aff-a253-5b8e657e1bbf}" orientation="n"/>
                                    </description>
                                </definition>
                            </element>
                            <element name="terminal_1pol_n_outher.elmt">
                                <definition type="element" link_type="terminal" hotspot_x="9" hotspot_y="11" width="20" height="30" version="0.90">
                                    <uuid uuid="{53d01af1-c525-4f5d-8dfc-b984763ac461}"/>
                                    <names>
                                        <name lang="de">1-Pol  N-extern</name>
                                    </names>
                                    <kindInformations>
                                        <kindInformation name="type">generic</kindInformation>
                                        <kindInformation name="function">generic</kindInformation>
                                    </kindInformations>
                                    <elementInformations>
                                        <elementInformation name="description" show="1"/>
                                        <elementInformation name="designation" show="1"/>
                                        <elementInformation name="label" show="1"/>
                                        <elementInformation name="machine_manufacturer_reference" show="1"/>
                                        <elementInformation name="quantity" show="1"/>
                                        <elementInformation name="plant" show="1"/>
                                        <elementInformation name="manufacturer" show="1"/>
                                        <elementInformation name="supplier" show="1"/>
                                        <elementInformation name="manufacturer_reference" show="1"/>
                                        <elementInformation name="comment" show="1"/>
                                        <elementInformation name="unity" show="1"/>
                                    </elementInformations>
                                    <informations/>
                                    <description>
                                        <circle x="-2" y="-2" antialias="false" style="line-style:normal;line-weight:normal;filling:black;color:black" diameter="4"/>
                                        <line end1="none" end2="none" antialias="false" y1="2" y2="10" style="line-style:normal;line-weight:normal;filling:none;color:black" length1="1.5" x1="0" length2="1.5" x2="0"/>
                                        <dynamic_text Halignment="AlignRight" frame="false" x="-8" y="-20" z="4" rotation="0" font="Liberation Sans,9,-1,5,50,0,0,0,0,0" text_width="-1" uuid="{72429080-0aa7-40c6-86af-d95be686bd20}" keep_visual_rotation="true" text_from="ElementInfo" Valignment="AlignVCenter">
                                            <text/>
                                            <info_name>label</info_name>
                                        </dynamic_text>
                                        <dynamic_text Halignment="AlignLeft" frame="false" x="0" y="0" z="5" rotation="0" font="Liberation Sans,6,-1,5,50,0,0,0,0,0" text_width="-1" uuid="{915ce65c-8bb7-4d4f-b3cf-296e6d0dd4f6}" keep_visual_rotation="true" text_from="UserText" Valignment="AlignVCenter">
                                            <text>N</text>
                                        </dynamic_text>
                                        <terminal type="Generic" x="0" y="-3" name="" uuid="{833a6733-150f-415f-9122-8912dddfacf0}" orientation="n"/>
                                        <terminal type="Generic" x="3" y="0" name="" uuid="{d65afc43-a19d-4c71-a0ca-c70585657e20}" orientation="e"/>
                                        <terminal type="Outer" x="0" y="10" name="N" uuid="{35271def-cab7-4233-ac19-e266ac1ff062}" orientation="s"/>
                                        <terminal type="Generic" x="-3" y="0" name="" uuid="{8c73d922-158b-428b-9ae5-ec6816fef769}" orientation="w"/>
                                    </description>
                                </definition>
                            </element>
                        </category>
                        <category name="terminals_with_name">
                            <names>
                                <name lang="de">Klemmen</name>
                                <name lang="en">terminals</name>
                                <name lang="fr">bornes</name>
                            </names>
                            <element name="klemme_phoenix_st2-5_quattro-mt.elmt">
                                <definition type="element" link_type="simple" hotspot_x="19" hotspot_y="94" width="360" height="110" version="0.90">
                                    <uuid uuid="{69c17832-f83e-49ee-b9d5-879a8baff55b}"/>
                                    <names>
                                        <name lang="de">ST 2,5-QUATTRO-MT - Messertrennklemme</name>
                                    </names>
                                    <elementInformations>
                                        <elementInformation name="quantity" show="1"/>
                                        <elementInformation name="machine_manufacturer_reference" show="1"/>
                                        <elementInformation name="description" show="1"/>
                                        <elementInformation name="label" show="1"/>
                                        <elementInformation name="plant" show="1"/>
                                        <elementInformation name="designation" show="1"/>
                                        <elementInformation name="manufacturer_reference" show="1"/>
                                        <elementInformation name="supplier" show="1"/>
                                        <elementInformation name="unity" show="1"/>
                                        <elementInformation name="manufacturer" show="1"/>
                                        <elementInformation name="comment" show="1"/>
                                    </elementInformations>
                                    <informations>Created using dxf2elmt!</informations>
                                    <description>
                                        <circle x="308" y="-22" antialias="false" style="line-style:normal;line-weight:normal;filling:none;color:black" diameter="8"/>
                                        <circle x="276" y="-30" antialias="false" style="line-style:normal;line-weight:normal;filling:none;color:black" diameter="4"/>
                                        <circle x="266" y="-20" antialias="false" style="line-style:normal;line-weight:normal;filling:black;color:black" diameter="4"/>
                                        <polygon closed="false" antialias="false" y1="-74.0499" y2="-76.4079" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="55.5407" x2="58.2641"/>
                                        <circle x="296" y="-30" antialias="false" style="line-style:normal;line-weight:normal;filling:none;color:black" diameter="4"/>
                                        <circle x="234" y="-22" antialias="false" style="line-style:normal;line-weight:normal;filling:none;color:black" diameter="8"/>
                                        <circle x="328" y="-22" antialias="false" style="line-style:normal;line-weight:normal;filling:none;color:black" diameter="8"/>
                                        <polygon closed="false" antialias="false" y1="-75.8957" y2="-76.2315" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="93.1059" x2="93.779"/>
                                        <polygon closed="false" antialias="false" y1="-75.6586" y2="-74.4352" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="94.3349" x2="98.5739"/>
                                        <polygon closed="false" antialias="false" y1="-74.4154" y2="-67.1157" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="105.504" x2="105.504"/>
                                        <polygon closed="false" antialias="false" y1="-75.9959" y2="-73.6379" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="58.1442" x2="55.4222"/>
                                        <polygon closed="false" antialias="false" y1="-74.0725" y2="-65.7554" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="54.457" x2="54.457"/>
                                        <polygon closed="false" antialias="false" y1="-74.0725" y2="-74.0499" y3="-73.6379" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="54.457" x2="55.5407" x3="55.4222"/>
                                        <polygon closed="false" antialias="false" y1="-68.6877" y2="-68.8726" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="82.8457" x2="83.0602"/>
                                        <polygon closed="false" antialias="false" y1="-72.6614" y2="-73.6379" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="57.1762" x2="55.4222"/>
                                        <polygon closed="false" antialias="false" y1="-66.5005" y2="-66.4511" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="84.5432" x2="84.7126"/>
                                        <polygon closed="false" antialias="false" y1="-66.6289" y2="-62.1021" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="104.939" x2="104.939"/>
                                        <polygon closed="false" antialias="false" y1="-66.6289" y2="-67.1157" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="104.939" x2="105.504"/>
                                        <polygon closed="false" antialias="false" y1="-64.2512" y2="-64.0028" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="113.172" x2="114.035"/>
                                        <polygon closed="false" antialias="false" y1="-63.2338" y2="-62.7455" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="101.019" x2="100.456"/>
                                        <polygon closed="false" antialias="false" y1="-61.23" y2="-64.35" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="128.607" x2="130.177"/>
                                        <polygon closed="false" antialias="false" y1="-65.5297" y2="-67.1397" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="137.564" x2="137.564"/>
                                        <polygon closed="false" antialias="false" y1="-63.8123" y2="-64.0706" y3="-62.2545" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="119.663" x2="118.767" x3="118.767"/>
                                        <text x="213" y="7" font="Arial,10,-1,5,50,0,0,0,0,0,Standard" rotation="0" color="#000000" text="a"/>
                                        <polygon closed="false" antialias="false" y1="-63.8123" y2="-67.8382" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="119.663" x2="118.092"/>
                                        <text x="329" y="7" font="Arial,10,-1,5,50,1,0,0,0,0,Italic" rotation="0" color="#000000" text="b"/>
                                        <polygon closed="false" antialias="false" y1="-63.7248" y2="-65.5297" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="135.48" x2="137.564"/>
                                        <text x="308" y="7" font="Arial,10,-1,5,50,0,0,0,0,0,Standard" rotation="0" color="#000000" text="d"/>
                                        <polygon closed="false" antialias="false" y1="-61.072" y2="-64.35" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="141.534" x2="130.177"/>
                                        <text x="233" y="7" font="Arial,10,-1,5,50,0,0,0,0,0,Standard" rotation="0" color="#000000" text="c"/>
                                        <polygon closed="false" antialias="false" y1="-65.0852" y2="-66.6289" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="110.286" x2="104.939"/>
                                        <polygon closed="false" antialias="false" y1="-61.69" y2="-63.2338" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="106.366" x2="101.019"/>
                                        <polygon closed="false" antialias="false" y1="-64.127" y2="-67.1397" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="134.085" x2="137.564"/>
                                        <polygon closed="false" antialias="false" y1="-65.0852" y2="-61.69" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="110.286" x2="106.366"/>
                                        <polygon closed="false" antialias="false" y1="-67.1157" y2="-64.6534" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="105.504" x2="114.035"/>
                                        <polygon closed="false" antialias="false" y1="-64.35" y2="-68.7216" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="130.177" x2="135.225"/>
                                        <polygon closed="false" antialias="false" y1="-64.6788" y2="-66.6261" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="130.557" x2="123.814"/>
                                        <polygon closed="false" antialias="false" y1="-63.0292" y2="-67.1623" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="144.712" x2="149.484"/>
                                        <polygon closed="false" antialias="false" y1="-64.5645" y2="-67.1397" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="146.485" x2="137.564"/>
                                        <polygon closed="false" antialias="false" y1="-78.0434" y2="-77.3646" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="91.7202" x2="90.3613"/>
                                        <polygon closed="false" antialias="false" y1="-78.0434" y2="-75.8957" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="93.1059" x2="93.1059"/>
                                        <polygon closed="false" antialias="false" y1="-76.4361" y2="-77.3646" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="90.3613" x2="90.3613"/>
                                        <polygon closed="false" antialias="false" y1="-77.7245" y2="-75.6586" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="94.4492" x2="94.3349"/>
                                        <polygon closed="false" antialias="false" y1="-76.2315" y2="-77.6666" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="93.779" x2="93.8594"/>
                                        <polygon closed="false" antialias="false" y1="-77.1699" y2="-76.9851" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="86.6246" x2="86.4101"/>
                                        <polygon closed="false" antialias="false" y1="-78.0434" y2="-75.7927" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="91.7202" x2="91.7202"/>
                                        <polygon closed="false" antialias="false" y1="-75.8957" y2="-76.4361" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="91.4436" x2="90.3613"/>
                                        <polygon closed="false" antialias="false" y1="-76.9851" y2="-67.6576" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="86.4101" x2="86.4101"/>
                                        <polygon closed="false" antialias="false" y1="-70.0438" y2="-62.7455" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="100.456" x2="100.456"/>
                                        <polygon closed="false" antialias="false" y1="-64.2512" y2="-59.7258" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="113.172" x2="113.172"/>
                                        <polygon closed="false" antialias="false" y1="-58.8255" y2="-66.1237" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="114.035" x2="114.035"/>
                                        <polygon closed="false" antialias="false" y1="-62.2545" y2="-66.6261" y3="-67.4078" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="118.767" x2="123.814" x3="123.814"/>
                                        <polygon closed="false" antialias="false" y1="-68.1825" y2="-63.8123" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="124.711" x2="119.663"/>
                                        <polygon closed="false" antialias="false" y1="-61.23" y2="-60.9718" y3="-59.1557" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="128.607" y4="-62.2545" x2="129.503" x3="129.503" x4="118.767"/>
                                        <polygon closed="false" antialias="false" y1="-67.8382" y2="-68.6581" y3="-66.1237" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="118.092" x2="115.255" x3="114.035"/>
                                        <polygon closed="false" antialias="false" y1="-58.8255" y2="-62.7455" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="114.035" x2="100.456"/>
                                        <polygon closed="false" antialias="false" y1="-60.8575" y2="-59.476" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="109.252" x2="114.035"/>
                                        <polygon closed="false" antialias="false" y1="-64.2512" y2="-60.8575" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="113.172" x2="109.252"/>
                                        <polygon closed="false" antialias="false" y1="-74.4352" y2="-77.5326" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="98.5739" x2="102.151"/>
                                        <polygon closed="false" antialias="false" y1="-68.7216" y2="-65.2446" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="135.225" x2="147.269"/>
                                        <polygon closed="false" antialias="false" y1="-10.4653" y2="-8.62097" y3="-7.85474" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="144.851" x2="142.722" x3="142.722"/>
                                        <polygon closed="false" antialias="false" y1="-8.57578" y2="-10.4427" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="144.929" x2="144.929"/>
                                        <polygon closed="false" antialias="false" y1="-8.57578" y2="-8.62076" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="144.929" x2="142.722"/>
                                        <polygon closed="false" antialias="false" y1="-36.9772" y2="-36.9291" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="186.811" x2="186.981"/>
                                        <polygon closed="false" antialias="false" y1="-43.7266" y2="-44.2487" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="193.415" x2="194.15"/>
                                        <polygon closed="false" antialias="false" y1="-44.2078" y2="-43.7266" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="193.295" x2="193.415"/>
                                        <polygon x6="197.038" x7="197.038" closed="false" antialias="false" y1="-44.2078" y2="-44.2444" y3="-33.0713" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="193.295" y4="-33.0348" x2="191.541" y5="-33.5159" x3="194.319" y6="-32.912" x4="196.073" y7="-24.5949" x5="195.955"/>
                                        <polygon closed="false" antialias="false" y1="-4.22677" y2="-0.332105" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="197.038" x2="197.038"/>
                                        <polygon closed="false" antialias="false" y1="-42.7106" y2="-42.7599" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="166.951" x2="166.781"/>
                                        <polygon closed="false" antialias="false" y1="0.772795" y2="-0.332105" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="148.5" x2="197.038"/>
                                        <polygon closed="false" antialias="false" y1="-37.2834" y2="-37.8874" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="202.086" x2="201.001"/>
                                        <polygon closed="false" antialias="false" y1="-37.2834" y2="-28.9664" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="202.086" x2="202.086"/>
                                        <polygon closed="false" antialias="false" y1="-8.59695" y2="-4.70228" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="202.086" x2="202.086"/>
                                        <polygon closed="false" antialias="false" y1="-24.5947" y2="-28.9664" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="197.038" x2="202.086"/>
                                        <polygon closed="false" antialias="false" y1="-37.0901" y2="-38.0482" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="188.165" x2="188.165"/>
                                        <polygon closed="false" antialias="false" y1="-42.8729" y2="-43.8296" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="168.136" x2="168.136"/>
                                        <polygon closed="false" antialias="false" y1="-37.4429" y2="-37.4191" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="199.367" x2="200.462"/>
                                        <polygon closed="false" antialias="false" y1="-37.8874" y2="-33.5158" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="201.001" x2="195.955"/>
                                        <polygon closed="false" antialias="false" y1="-8.59695" y2="-4.22677" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="202.086" x2="197.038"/>
                                        <polygon closed="false" antialias="false" y1="-48.6203" y2="-50.38" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="199.196" x2="198.759"/>
                                        <polygon closed="false" antialias="false" y1="-46.7605" y2="-37.4429" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="197.05" x2="199.367"/>
                                        <polygon closed="false" antialias="false" y1="-44.2487" y2="-48.6203" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="194.15" x2="199.196"/>
                                        <polygon closed="false" antialias="false" y1="-37.4429" y2="-33.0713" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="199.367" x2="194.319"/>
                                        <polygon closed="false" antialias="false" y1="-38.0482" y2="-36.9518" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="188.165" x2="186.9"/>
                                        <polygon closed="false" antialias="false" y1="-38.0482" y2="-38.7651" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="188.165" x2="187.338"/>
                                        <polygon closed="false" antialias="false" y1="-38.7962" y2="-37.8154" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="186.907" x2="185.774"/>
                                        <polygon closed="false" antialias="false" y1="-39.1645" y2="-48.4919" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="185.113" x2="185.113"/>
                                        <polygon closed="false" antialias="false" y1="-48.6768" y2="-39.3507" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="185.328" x2="185.328"/>
                                        <polygon closed="false" antialias="false" y1="-50.1838" y2="-51.9195" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="183.6" x2="183.6"/>
                                        <polygon closed="false" antialias="false" y1="-52.0578" y2="-49.9058" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="182.572" x2="182.572"/>
                                        <polygon closed="false" antialias="false" y1="-41.1823" y2="-38.7651" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="187.338" x2="187.338"/>
                                        <polygon closed="false" antialias="false" y1="-38.7962" y2="-41.0779" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="186.907" x2="186.907"/>
                                        <polygon closed="false" antialias="false" y1="-39.3507" y2="-39.1645" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="185.328" x2="185.113"/>
                                        <polygon closed="false" antialias="false" y1="-39.2124" y2="-40.2609" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="185.332" x2="186.541"/>
                                        <polygon closed="false" antialias="false" y1="-43.9185" y2="-53.2445" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="168.648" x2="168.648"/>
                                        <polygon closed="false" antialias="false" y1="-47.4618" y2="-38.1358" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="188.678" x2="188.678"/>
                                        <polygon closed="false" antialias="false" y1="-47.4618" y2="-46.0098" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="188.678" x2="193.711"/>
                                        <polygon closed="false" antialias="false" y1="-47.6481" y2="-47.4618" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="188.892" x2="188.678"/>
                                        <polygon closed="false" antialias="false" y1="-47.9063" y2="-52.0747" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="191.515" x2="191.515"/>
                                        <polygon closed="false" antialias="false" y1="-48.6768" y2="-48.4919" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="185.328" x2="185.113"/>
                                        <polygon closed="false" antialias="false" y1="-50.3927" y2="-51.3198" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="183.797" x2="184.293"/>
                                        <polygon closed="false" antialias="false" y1="-52.3428" y2="-53.8668" y3="-55.5813" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="182.374" y4="-51.451" x2="184.134" x3="178.193" x4="178.193"/>
                                        <polygon closed="false" antialias="false" y1="-52.0267" y2="-47.9529" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="191.685" x2="191.685"/>
                                        <polygon closed="false" antialias="false" y1="-46.0098" y2="-44.2487" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="193.711" x2="194.15"/>
                                        <polygon closed="false" antialias="false" y1="-54.4581" y2="-54.2732" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="165.298" x2="165.084"/>
                                        <polygon closed="false" antialias="false" y1="-52.0578" y2="-51.9195" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="182.572" x2="183.6"/>
                                        <polygon closed="false" antialias="false" y1="-52.0747" y2="-52.0267" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="191.515" x2="191.685"/>
                                        <polygon closed="false" antialias="false" y1="-51.2605" y2="-52.4839" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="178.856" x2="174.616"/>
                                        <polygon closed="false" antialias="false" y1="-53.4294" y2="-53.2445" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="168.863" x2="168.648"/>
                                        <polygon closed="false" antialias="false" y1="-52.4839" y2="-55.5813" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="174.616" x2="178.193"/>
                                        <polygon closed="false" antialias="false" y1="-54.2732" y2="-44.9472" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="165.084" x2="165.084"/>
                                        <polygon closed="false" antialias="false" y1="-50.5408" y2="-50.8456" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="179.879" x2="179.879"/>
                                        <polygon closed="false" antialias="false" y1="-50.8456" y2="-51.3057" y3="-50.3094" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="179.879" x2="180.126" x3="180.126"/>
                                        <polygon closed="false" antialias="false" y1="-51.3057" y2="-52.0578" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="180.126" x2="182.572"/>
                                        <polygon closed="false" antialias="false" y1="-49.9284" y2="-50.126" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="182.188" x2="180.71"/>
                                        <polygon closed="false" antialias="false" y1="-51.2605" y2="-52.3428" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="178.856" x2="182.374"/>
                                        <polygon closed="false" antialias="false" y1="-55.9651" y2="-57.7022" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="163.571" x2="163.571"/>
                                        <polygon closed="false" antialias="false" y1="-57.1011" y2="-56.174" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="164.264" x2="163.767"/>
                                        <polygon closed="false" antialias="false" y1="-53.2445" y2="-48.4919" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="168.648" x2="185.113"/>
                                        <polygon closed="false" antialias="false" y1="-46.0098" y2="-50.38" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="193.711" x2="198.759"/>
                                        <polygon closed="false" antialias="false" y1="-37.2834" y2="-32.9118" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="202.086" x2="197.038"/>
                                        <polygon closed="false" antialias="false" y1="-4.70228" y2="-0.332105" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="202.086" x2="197.038"/>
                                        <polygon closed="false" antialias="false" y1="-47.7624" y2="-50.4787" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="54.457" x2="54.457"/>
                                        <polygon closed="false" antialias="false" y1="-47.7624" y2="-45.9985" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="54.457" x2="60.5671"/>
                                        <polygon closed="false" antialias="false" y1="-29.7636" y2="-28.186" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="57.0026" x2="57.0026"/>
                                        <polygon closed="false" antialias="false" y1="-36.8531" y2="-37.5262" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="88.7611" x2="89.5372"/>
                                        <polygon closed="false" antialias="false" y1="-31.2735" y2="-28.186" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="60.5671" x2="57.0026"/>
                                        <polygon closed="false" antialias="false" y1="-53.7342" y2="-57.8081" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="171.655" x2="171.655"/>
                                        <polygon closed="false" antialias="false" y1="-57.8574" y2="-53.6876" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="171.486" x2="171.486"/>
                                        <polygon closed="false" antialias="false" y1="-57.8081" y2="-57.8574" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="171.655" x2="171.486"/>
                                        <polygon closed="false" antialias="false" y1="-46.9637" y2="-44.5478" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="167.309" x2="167.309"/>
                                        <polygon closed="false" antialias="false" y1="-44.5789" y2="-46.8607" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="166.877" x2="166.877"/>
                                        <polygon closed="false" antialias="false" y1="-45.132" y2="-54.4581" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="165.298" x2="165.298"/>
                                        <polygon closed="false" antialias="false" y1="-43.8296" y2="-42.7346" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="168.136" x2="166.87"/>
                                        <polygon closed="false" antialias="false" y1="-43.8296" y2="-44.5478" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="168.136" x2="167.309"/>
                                        <polygon closed="false" antialias="false" y1="-44.5789" y2="-43.5968" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="166.877" x2="165.744"/>
                                        <polygon closed="false" antialias="false" y1="-44.9472" y2="-45.132" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="165.084" x2="165.298"/>
                                        <polygon closed="false" antialias="false" y1="-44.9938" y2="-46.0422" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="165.303" x2="166.512"/>
                                        <polygon closed="false" antialias="false" y1="-66.0955" y2="-63.0828" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="150.589" x2="147.11"/>
                                        <polygon closed="false" antialias="false" y1="-63.0489" y2="-66.0955" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="150.259" x2="150.589"/>
                                        <polygon closed="false" antialias="false" y1="-57.8391" y2="-55.6872" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="162.542" x2="162.542"/>
                                        <polygon closed="false" antialias="false" y1="-56.0907" y2="-57.087" y3="-56.6284" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="160.097" x2="160.097" x3="159.85"/>
                                        <polygon closed="false" antialias="false" y1="-57.2323" y2="-61.3641" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="158.164" x2="158.164"/>
                                        <polygon closed="false" antialias="false" y1="-55.9073" y2="-55.7097" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="160.681" x2="162.159"/>
                                        <polygon closed="false" antialias="false" y1="-57.8391" y2="-57.7022" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="162.542" x2="163.571"/>
                                        <polygon closed="false" antialias="false" y1="-58.1241" y2="-59.6481" y3="-61.3641" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="162.345" x2="164.104" x3="158.164"/>
                                        <polygon closed="false" antialias="false" y1="-57.087" y2="-57.8391" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="160.097" x2="162.542"/>
                                        <polygon closed="false" antialias="false" y1="-58.1241" y2="-57.0418" y3="-58.2653" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="162.345" x2="158.826" x3="154.587"/>
                                        <polygon closed="false" antialias="false" y1="-60.1406" y2="-61.7507" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="142.317" x2="142.317"/>
                                        <polygon closed="false" antialias="false" y1="-60.396" y2="-63.0292" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="144.425" x2="144.712"/>
                                        <polygon closed="false" antialias="false" y1="-62.2785" y2="-62.8387" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="154.406" x2="155.054"/>
                                        <polygon closed="false" antialias="false" y1="-61.7507" y2="-61.072" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="142.317" x2="141.534"/>
                                        <polygon closed="false" antialias="false" y1="-63.0828" y2="-62.3928" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="147.11" x2="149.502"/>
                                        <polygon closed="false" antialias="false" y1="-61.3528" y2="-63.0292" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="150.518" x2="144.712"/>
                                        <polygon closed="false" antialias="false" y1="-60.1406" y2="-58.4416" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="142.317" x2="142.317"/>
                                        <polygon closed="false" antialias="false" y1="-58.4416" y2="-57.7615" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="142.317" x2="141.534"/>
                                        <polygon closed="false" antialias="false" y1="-57.7615" y2="-61.072" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="141.534" x2="141.534"/>
                                        <polygon closed="false" antialias="false" y1="-60.7093" y2="-62.2785" y3="-61.7733" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="154.265" x2="154.406" x3="156.159"/>
                                        <polygon closed="false" antialias="false" y1="-61.2117" y2="-60.5329" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="144.185" x2="143.401"/>
                                        <polygon closed="false" antialias="false" y1="-61.2117" y2="-61.1199" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="144.185" x2="144.504"/>
                                        <polygon closed="false" antialias="false" y1="-59.2657" y2="-58.7591" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="150.928" x2="152.679"/>
                                        <polygon closed="false" antialias="false" y1="-60.7093" y2="-60.5654" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="154.265" x2="154.764"/>
                                        <polygon closed="false" antialias="false" y1="-60.5329" y2="-57.2224" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="143.401" x2="143.401"/>
                                        <polygon closed="false" antialias="false" y1="-59.8274" y2="-60.1406" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="143.401" x2="142.317"/>
                                        <polygon closed="false" antialias="false" y1="-58.7055" y2="-59.2657" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="150.28" x2="150.928"/>
                                        <polygon closed="false" antialias="false" y1="-58.9031" y2="-60.7093" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="152.181" x2="154.265"/>
                                        <polygon closed="false" antialias="false" y1="-58.7055" y2="-60.396" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="150.28" x2="144.425"/>
                                        <polygon closed="false" antialias="false" y1="-63.358" y2="-65.5297" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="145.09" x2="137.564"/>
                                        <polygon closed="false" antialias="false" y1="-60.5329" y2="-54.2732" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="143.401" x2="165.084"/>
                                        <polygon closed="false" antialias="false" y1="-65.4055" y2="-62.3928" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="152.981" x2="149.502"/>
                                        <polygon closed="false" antialias="false" y1="-58.7591" y2="-61.7733" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="152.679" x2="156.159"/>
                                        <polygon closed="false" antialias="false" y1="-61.3641" y2="-58.2653" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="158.164" x2="154.587"/>
                                        <polygon closed="false" antialias="false" y1="-61.7507" y2="-64.127" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="142.317" x2="134.085"/>
                                        <polygon closed="false" antialias="false" y1="-61.3528" y2="-65.4859" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="150.518" x2="155.291"/>
                                        <polygon closed="false" antialias="false" y1="-77.692" y2="-74.0725" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="58.6367" x2="54.457"/>
                                        <polygon closed="false" antialias="false" y1="-82.7946" y2="-83.74" y3="-85.2485" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="58.0807" y4="-83.7951" x2="57.3455" x3="57.7844" x4="62.8164"/>
                                        <polygon closed="false" antialias="false" y1="-83.0853" y2="-82.7946" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="58.4165" x2="58.0807"/>
                                        <polygon closed="false" antialias="false" y1="-74.6539" y2="-74.469" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="63.0309" x2="62.8164"/>
                                        <polygon closed="false" antialias="false" y1="-74.6539" y2="-83.9813" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="63.0309" x2="63.0309"/>
                                        <polygon closed="false" antialias="false" y1="-83.2066" y2="-82.7946" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="58.2006" x2="58.0807"/>
                                        <polygon closed="false" antialias="false" y1="-83.2066" y2="-82.2302" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="58.2006" x2="59.9546"/>
                                        <polygon closed="false" antialias="false" y1="-83.7951" y2="-83.9813" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="62.8164" x2="63.0309"/>
                                        <polygon closed="false" antialias="false" y1="-83.7951" y2="-74.469" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="62.8164" x2="62.8164"/>
                                        <polygon closed="false" antialias="false" y1="-72.2818" y2="-72.2324" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="64.5139" x2="64.6833"/>
                                        <polygon closed="false" antialias="false" y1="-68.8726" y2="-78.1986" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="83.0602" x2="83.0602"/>
                                        <polygon closed="false" antialias="false" y1="-78.0138" y2="-68.6877" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="82.8457" x2="82.8457"/>
                                        <polygon closed="false" antialias="false" y1="-80.2179" y2="-83.3153" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="78.5446" x2="82.1218"/>
                                        <polygon closed="false" antialias="false" y1="-85.0298" y2="-80.8995" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="76.1796" x2="76.1796"/>
                                        <polygon closed="false" antialias="false" y1="-81.574" y2="-83.8247" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="71.6909" x2="71.6909"/>
                                        <polygon closed="false" antialias="false" y1="-82.7664" y2="-73.4403" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="66.3808" x2="66.3808"/>
                                        <polygon closed="false" antialias="false" y1="-77.4747" y2="-81.5486" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="89.4172" x2="89.4172"/>
                                        <polygon closed="false" antialias="false" y1="-81.5486" y2="-81.598" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="89.4172" x2="89.2479"/>
                                        <polygon closed="false" antialias="false" y1="-78.1986" y2="-78.0138" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="83.0602" x2="82.8457"/>
                                        <polygon closed="false" antialias="false" y1="-78.0434" y2="-77.6666" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="93.1059" x2="93.8594"/>
                                        <polygon closed="false" antialias="false" y1="-77.7245" y2="-79.2485" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="94.4492" x2="96.2089"/>
                                        <polygon closed="false" antialias="false" y1="-80.2179" y2="-81.4413" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="78.5446" x2="74.3056"/>
                                        <polygon closed="false" antialias="false" y1="-81.598" y2="-77.4281" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="89.2479" x2="89.2479"/>
                                        <polygon closed="false" antialias="false" y1="-81.4075" y2="-83.5058" y3="-81.4413" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="74.4199" x2="74.4199" x3="74.3056"/>
                                        <polygon closed="false" antialias="false" y1="-81.677" y2="-82.2175" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="71.4129" x2="70.332"/>
                                        <polygon closed="false" antialias="false" y1="-83.146" y2="-83.8247" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="70.332" x2="71.6909"/>
                                        <polygon closed="false" antialias="false" y1="-82.9512" y2="-82.7664" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="66.5953" x2="66.3808"/>
                                        <polygon closed="false" antialias="false" y1="-83.8247" y2="-81.677" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="73.0766" x2="73.0766"/>
                                        <polygon closed="false" antialias="false" y1="-73.0283" y2="-72.2099" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="120.302" x2="123.14"/>
                                        <polygon closed="false" antialias="false" y1="-75.6262" y2="-77.7245" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="94.4492" x2="94.4492"/>
                                        <polygon closed="false" antialias="false" y1="-77.6525" y2="-74.4154" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="104.283" x2="105.504"/>
                                        <polygon closed="false" antialias="false" y1="-73.2823" y2="-70.0438" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="99.2371" x2="100.456"/>
                                        <polygon closed="false" antialias="false" y1="-77.5326" y2="-79.2485" y3="-75.1182" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="102.151" x2="96.2089" x3="96.2089"/>
                                        <polygon closed="false" antialias="false" y1="-83.2095" y2="-87.3793" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="69.2172" x2="69.2172"/>
                                        <polygon closed="false" antialias="false" y1="-87.3299" y2="-83.256" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="69.3879" x2="69.3879"/>
                                        <polygon closed="false" antialias="false" y1="-83.146" y2="-82.2175" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="70.332" x2="70.332"/>
                                        <polygon closed="false" antialias="false" y1="-87.3299" y2="-87.3793" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="69.3879" x2="69.2172"/>
                                        <polygon closed="false" antialias="false" y1="-83.4494" y2="-82.0143" y3="-81.677" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="73.8301" x2="73.7497" x3="73.0766"/>
                                        <polygon closed="false" antialias="false" y1="-83.4494" y2="-83.8247" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="73.8301" x2="73.0766"/>
                                        <polygon closed="false" antialias="false" y1="-83.5058" y2="-85.0298" y3="-83.3153" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="74.4199" x2="76.1796" x3="82.1218"/>
                                        <polygon closed="false" antialias="false" y1="-72.2099" y2="-68.1825" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="123.14" x2="124.711"/>
                                        <polygon closed="false" antialias="false" y1="-72.2099" y2="-67.8382" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="123.14" x2="118.092"/>
                                        <polygon closed="false" antialias="false" y1="-73.2823" y2="-76.9851" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="99.2371" x2="86.4101"/>
                                        <polygon closed="false" antialias="false" y1="-78.0138" y2="-82.7664" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="82.8457" x2="66.3808"/>
                                        <polygon closed="false" antialias="false" y1="-73.2823" y2="-77.6525" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="99.2371" x2="104.283"/>
                                        <polygon closed="false" antialias="false" y1="-68.6581" y2="-73.0283" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="115.255" x2="120.302"/>
                                        <polygon closed="false" antialias="false" y1="-74.4154" y2="-70.0438" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="105.504" x2="100.456"/>
                                        <polygon closed="false" antialias="false" y1="-82.2302" y2="-72.6614" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="59.9546" x2="57.1762"/>
                                        <polygon closed="false" antialias="false" y1="-89.6187" y2="-77.6525" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="62.8305" x2="104.283"/>
                                        <polygon closed="false" antialias="false" y1="-89.6187" y2="-85.2485" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="62.8305" x2="57.7844"/>
                                        <polygon closed="false" antialias="false" y1="-66.0955" y2="-65.4055" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="150.589" x2="152.981"/>
                                        <polygon closed="false" antialias="false" y1="-65.4859" y2="-62.8387" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="155.291" x2="155.054"/>
                                        <polygon closed="false" antialias="false" y1="-56.6284" y2="-56.3236" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="159.85" x2="159.85"/>
                                        <polygon closed="false" antialias="false" y1="-58.7055" y2="-61.3528" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="150.28" x2="150.518"/>
                                        <polygon closed="false" antialias="false" y1="-0.0823383" y2="0.772795" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="145.537" x2="148.5"/>
                                        <polygon closed="false" antialias="false" y1="-65.4859" y2="-67.1623" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="155.291" x2="149.484"/>
                                        <polygon closed="false" antialias="false" y1="-45.9985" y2="-27.1573" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="60.5671" x2="60.5671"/>
                                        <polygon closed="false" antialias="false" y1="-26.3756" y2="-31.6376" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="54.457" x2="54.457"/>
                                        <polygon closed="false" antialias="false" y1="-36.2463" y2="-36.6936" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="60.052" x2="60.5671"/>
                                        <polygon closed="false" antialias="false" y1="-36.0967" y2="-36.2463" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="60.5671" x2="60.052"/>
                                        <polygon closed="false" antialias="false" y1="-28.186" y2="-27.1573" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="57.0026" x2="60.5671"/>
                                        <polygon closed="false" antialias="false" y1="-25.5783" y2="-24.3506" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="86.0277" x2="88.2347"/>
                                        <polygon closed="false" antialias="false" y1="-25.5783" y2="-27.4452" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="86.0277" x2="86.0277"/>
                                        <polygon closed="false" antialias="false" y1="-24.3506" y2="-23.5844" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="88.2347" x2="88.2347"/>
                                        <polygon closed="false" antialias="false" y1="-27.4452" y2="-30.8516" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="86.0277" x2="89.9605"/>
                                        <polygon closed="false" antialias="false" y1="-26.1949" y2="-24.3506" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="90.3641" x2="88.2347"/>
                                        <polygon closed="false" antialias="false" y1="-23.5844" y2="-26.003" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="88.2347" x2="91.0287"/>
                                        <polygon closed="false" antialias="false" y1="-27.4452" y2="-36.8531" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="86.0277" x2="88.7611"/>
                                        <polygon closed="false" antialias="false" y1="-28.3568" y2="-25.5783" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="89.2366" x2="86.0277"/>
                                        <polygon closed="false" antialias="false" y1="-26.662" y2="-35.5943" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="88.7441" x2="91.3377"/>
                                        <polygon closed="false" antialias="false" y1="-17.4376" y2="-26.3756" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="85.4195" x2="54.457"/>
                                        <polygon closed="false" antialias="false" y1="-29.8624" y2="-32.8314" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="57.1395" x2="60.5671"/>
                                        <polygon closed="false" antialias="false" y1="-17.4376" y2="-21.8078" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="85.4195" x2="90.4657"/>
                                        <polygon closed="false" antialias="false" y1="-36.901" y2="-32.5294" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="59.877" x2="54.8295"/>
                                        <polygon closed="false" antialias="false" y1="-26.662" y2="-10.4427" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="88.7441" x2="144.929"/>
                                        <polygon closed="false" antialias="false" y1="-62.9925" y2="-50.38" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="155.066" x2="198.759"/>
                                        <polygon x6="92.5795" x7="92.4271" x8="92.2747" closed="false" x9="92.1209" y10="-75.7432" y11="-75.7616" x10="91.9699" y12="-75.787" x11="91.8528" y13="-75.818" x12="91.7399" y14="-75.8533" x13="91.6341" y15="-75.8957" x14="91.5353" x15="91.4436" y1="-75.8957" y2="-75.8533" y3="-75.818" y4="-75.787" y5="-75.7616" y6="-75.7432" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="93.1059" y7="-75.7277" x2="93.0141" antialias="false" y8="-75.7235" x3="92.9154" y9="-75.7277" x4="92.8081" x5="92.6966"/>
                                        <polygon y15="-67.4332" closed="false" y16="-67.5475" y17="-67.6647" y18="-67.7832" x20="83.2069" y19="-67.8848" x21="83.1801" x22="83.1575" x23="83.1279" x24="83.1039" x25="83.0842" x26="83.0757" x27="83.0672" x28="83.0616" x29="83.06" x1="84.5432" x2="84.4685" x3="84.3894" x4="84.3062" x5="84.2173" x6="84.1157" x7="84.0169" x8="83.9209" x9="83.8306" y20="-67.9808" y21="-68.0711" y22="-68.1515" y23="-68.2757" y24="-68.3984" style="line-style:normal;line-weight:thin;filling:none;color:black" antialias="false" y25="-68.5212" y26="-68.596" y27="-68.6807" y28="-68.7738" y29="-68.8726" x10="83.7446" x11="83.6627" x12="83.6119" x13="83.5583" x14="83.5033" x15="83.4482" x16="83.3861" x17="83.3297" x18="83.2789" x19="83.2408" y1="-66.5005" y2="-66.5231" y3="-66.5527" y4="-66.5908" y5="-66.636" y6="-66.6981" y7="-66.7672" y8="-66.8448" y9="-66.9281" y10="-67.0184" y11="-67.1157" y12="-67.1807" y13="-67.2554" y14="-67.3401"/>
                                        <polygon y15="-66.8801" closed="false" y16="-66.7954" y17="-66.7192" y18="-66.6515" x20="84.4162" y19="-66.5922" x21="84.5432" x1="82.8457" x2="82.8499" x3="82.8654" x4="82.888" x5="82.9205" x6="82.9628" x7="83.0136" x8="83.0729" x9="83.1533" y20="-66.5414" y21="-66.5005" style="line-style:normal;line-weight:thin;filling:none;color:black" antialias="false" x10="83.2436" x11="83.3424" x12="83.4524" x13="83.5696" x14="83.6952" x15="83.8066" x16="83.9238" x17="84.0437" x18="84.1651" x19="84.2892" y1="-68.6877" y2="-68.5579" y3="-68.4281" y4="-68.2968" y5="-68.1656" y6="-68.0344" y7="-67.9031" y8="-67.7733" y9="-67.6252" y10="-67.4812" y11="-67.3429" y12="-67.2117" y13="-67.0875" y14="-66.9718"/>
                                        <polygon x6="85.6524" x7="85.5818" x8="85.5155" closed="false" x9="85.4576" y10="-66.4158" y11="-66.4031" x10="85.38" y12="-66.3946" x11="85.2911" y13="-66.393" x12="85.1924" y14="-66.4001" x13="85.0865" y15="-66.4128" x14="84.9793" y16="-66.4297" x15="84.8805" x16="84.7916" y17="-66.4509" x17="84.7126" y1="-66.715" y2="-66.6656" y3="-66.6134" y4="-66.5626" y5="-66.5231" y6="-66.492" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="86.0489" y7="-66.4666" x2="85.9798" antialias="false" y8="-66.4469" x3="85.8993" y9="-66.4327" x4="85.8076" x5="85.7286"/>
                                        <polygon x6="85.627" x7="85.7187" x8="85.8373" closed="false" x9="85.96" y10="-67.1411" y11="-67.2046" x10="86.0885" y12="-67.2597" x11="86.2225" x12="86.3594" y1="-66.406" y2="-66.4737" y3="-66.5414" y4="-66.612" y5="-66.7093" y6="-66.8011" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="85.3165" y7="-66.8871" x2="85.3589" antialias="false" y8="-66.9817" x3="85.4069" y9="-67.0664" x4="85.4591" x5="85.5409"/>
                                        <polygon x6="85.5268" x7="85.4181" x8="85.3067" closed="false" x9="85.1909" y10="-66.3846" y11="-66.3987" x10="85.0738" y12="-66.4199" x11="84.9553" y13="-66.4509" x12="84.8339" x13="84.7126" y1="-66.667" y2="-66.6021" y3="-66.5442" y4="-66.4962" y5="-66.4553" y6="-66.4243" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="85.9967" y7="-66.4003" x2="85.9134" antialias="false" y8="-66.3862" x3="85.8245" y9="-66.3819" x4="85.73" x5="85.6312"/>
                                        <polygon x6="86.3029" x7="86.2563" x8="86.2027" closed="false" x9="86.1406" y10="-66.739" y11="-66.667" x10="86.0715" x11="85.9967" y1="-67.6576" y2="-67.5377" y3="-67.422" y4="-67.3091" y5="-67.2004" y6="-67.096" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="86.4101" y7="-66.9972" x2="86.4059" antialias="false" y8="-66.9055" y9="-66.818" x3="86.3932" x4="86.372" x5="86.341"/>
                                        <polygon x6="90.0776" x7="90.1199" x8="90.1707" closed="false" x9="90.2286" y10="-77.3265" y11="-77.3646" x10="90.2921" x11="90.3612" y1="-76.9004" y2="-76.9512" y3="-77.002" y4="-77.0528" y5="-77.1022" y6="-77.1515" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="89.9774" y7="-77.1981" x2="89.9817" antialias="false" y8="-77.2432" y9="-77.2856" x3="89.9929" x4="90.0141" x5="90.0409"/>
                                        <polygon x6="90.0776" x7="90.041" x8="90.0141" closed="false" x9="89.993" y10="-76.8482" y11="-76.9005" x10="89.9817" x11="89.9775" y1="-76.4361" y2="-76.4742" y3="-76.5138" y4="-76.5575" y5="-76.6013" y6="-76.6493" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="90.3613" y7="-76.6973" x2="90.2921" antialias="false" y8="-76.7466" y9="-76.7974" x3="90.2286" x4="90.1708" x5="90.12"/>
                                        <polygon y15="-6.10918" closed="false" y16="-6.54664" y17="-6.98267" y18="-7.42008" y19="-7.85474" x1="145.537" x2="145.297" x3="145.067" x4="144.846" x5="144.634" x6="144.431" x7="144.239" x8="144.055" x9="143.882" style="line-style:normal;line-weight:thin;filling:none;color:black" antialias="false" x10="143.72" x11="143.566" x12="143.423" x13="143.292" x14="143.171" x15="143.059" x16="142.959" x17="142.869" x18="142.79" x19="142.722" y1="-0.0823383" y2="-0.498581" y3="-0.916305" y4="-1.33821" y5="-1.76297" y6="-2.19054" y7="-2.61948" y8="-3.05128" y9="-3.48594" y10="-3.92054" y11="-4.35801" y12="-4.79541" y13="-5.23288" y14="-5.67034"/>
                                        <polygon x6="188.571" x7="188.524" x8="188.469" closed="false" x9="188.408" y10="-37.2171" y11="-37.1437" x10="188.339" x11="188.263" y1="-38.1358" y2="-38.0158" y3="-37.9001" y4="-37.7872" y5="-37.6786" y6="-37.5741" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="188.678" y7="-37.4754" x2="188.672" antialias="false" y8="-37.3822" y9="-37.2961" x3="188.66" x4="188.638" x5="188.609"/>
                                        <polygon x6="187.794" x7="187.686" x8="187.574" closed="false" x9="187.458" y10="-36.8637" y11="-36.8764" x10="187.341" y12="-36.8991" x11="187.223" y13="-36.9303" x12="187.103" x13="186.981" y1="-37.1437" y2="-37.0788" y3="-37.0224" y4="-36.9743" y5="-36.9335" y6="-36.9012" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="188.264" y7="-36.8785" x2="188.181" antialias="false" y8="-36.8642" x3="188.092" y9="-36.8584" x4="187.999" x5="187.899"/>
                                        <polygon y15="-37.3582" closed="false" y16="-37.2735" y17="-37.1973" y18="-37.1296" x20="186.684" y19="-37.0703" x21="186.811" x1="185.113" x2="185.119" x3="185.133" x4="185.157" x5="185.189" x6="185.23" x7="185.281" x8="185.342" x9="185.421" y20="-37.0195" y21="-36.9772" style="line-style:normal;line-weight:thin;filling:none;color:black" antialias="false" x10="185.511" x11="185.611" x12="185.72" x13="185.837" x14="185.962" x15="186.075" x16="186.191" x17="186.311" x18="186.432" x19="186.558" y1="-39.1645" y2="-39.036" y3="-38.9062" y4="-38.775" y5="-38.6438" y6="-38.5111" y7="-38.3799" y8="-38.2501" y9="-38.1019" y10="-37.9593" y11="-37.8211" y12="-37.6898" y13="-37.5656" y14="-37.45"/>
                                        <polygon y1="-24.5947" y2="-24.1601" y3="-23.7184" y4="-23.2697" y5="-22.8153" y6="-22.3525" y7="-21.884" y8="-21.4099" y9="-20.9286" y30="-10.3622" y31="-9.80631" y32="-9.24751" y33="-8.69008" y34="-8.13128" y35="-7.57248" y36="-7.01368" y37="-6.45488" y38="-5.89751" y39="-5.33871" x10="195.536" x11="195.423" x12="195.323" x13="195.231" x14="195.152" x15="195.088" y40="-4.78271" x16="195.035" y41="-4.22677" x17="194.991" style="line-style:normal;line-weight:thin;filling:none;color:black" x18="194.957" x19="194.933" x20="194.918" x21="194.912" x22="194.918" x23="194.933" x24="194.957" x25="194.991" x26="195.035" x27="195.088" x28="195.152" x29="195.231" y10="-20.4418" y11="-19.9479" y12="-19.4498" y13="-18.9461" y14="-18.4366" y15="-17.9597" y16="-17.4785" y17="-16.9945" y18="-16.5062" y19="-16.0152" closed="false" x30="195.323" x31="195.423" x32="195.536" x33="195.66" x1="197.038" x34="195.794" x2="196.828" x35="195.939" x3="196.629" x36="196.096" x4="196.44" x37="196.262" x5="196.262" x38="196.44" x6="196.096" x39="196.629" x7="195.939" x8="195.794" x9="195.66" y20="-15.5213" y21="-15.0246" y22="-14.525" y23="-14.0213" y24="-13.5175" y25="-13.0095" antialias="false" y26="-12.5001" y27="-11.9878" y28="-11.4742" y29="-10.9182" x40="196.828" x41="197.038"/>
                                        <polygon x6="167.765" x7="167.656" x8="167.545" closed="false" x9="167.429" y10="-42.6456" y11="-42.6583" x10="167.312" y12="-42.6795" x11="167.193" y13="-42.7106" x12="167.073" x13="166.951" y1="-42.9265" y2="-42.8616" y3="-42.8051" y4="-42.7557" y5="-42.7148" y6="-42.6838" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="168.235" y7="-42.6612" x2="168.152" antialias="false" y8="-42.6471" x3="168.063" y9="-42.6414" x4="167.97" x5="167.869"/>
                                        <polygon x6="168.541" x7="168.495" x8="168.44" closed="false" x9="168.379" y10="-42.9984" y11="-42.9265" x10="168.31" x11="168.234" y1="-43.9185" y2="-43.7985" y3="-43.6814" y4="-43.5685" y5="-43.4599" y6="-43.3555" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="168.648" y7="-43.2567" x2="168.643" antialias="false" y8="-43.165" y9="-43.0789" x3="168.63" x4="168.609" x5="168.58"/>
                                        <polygon y15="-43.1396" closed="false" y16="-43.0563" y17="-42.9787" y18="-42.911" x20="166.655" y19="-42.8517" x21="166.782" x1="165.084" x2="165.09" x3="165.104" x4="165.127" x5="165.161" x6="165.201" x7="165.252" x8="165.311" x9="165.392" y20="-42.8009" y21="-42.76" style="line-style:normal;line-weight:thin;filling:none;color:black" antialias="false" x10="165.482" x11="165.582" x12="165.691" x13="165.808" x14="165.934" x15="166.047" x16="166.162" x17="166.282" x18="166.404" x19="166.529" y1="-44.9472" y2="-44.8188" y3="-44.6875" y4="-44.5563" y5="-44.4251" y6="-44.2938" y7="-44.1626" y8="-44.0328" y9="-43.8846" y10="-43.7407" y11="-43.6038" y12="-43.4726" y13="-43.3484" y14="-43.2327"/>
                                        <polygon x6="187.518" x7="187.622" x8="187.725" closed="false" x9="187.832" y10="-36.9785" y11="-37.0224" x10="187.937" y12="-37.0732" x11="188.038" y13="-37.131" x12="188.136" y14="-37.1945" x13="188.229" x14="188.316" y1="-36.9293" y2="-36.9023" y3="-36.8838" y4="-36.8727" y5="-36.8727" y6="-36.8785" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="186.981" y7="-36.8912" x2="187.089" antialias="false" y8="-36.9123" x3="187.196" y9="-36.9404" x4="187.305" x5="187.412"/>
                                        <polygon y15="-37.5925" closed="false" y16="-37.4965" y17="-37.4062" y18="-37.323" x20="186.388" y19="-37.2439" x21="186.491" x22="186.595" x23="186.702" x24="186.811" x1="185.328" x2="185.333" x3="185.344" x4="185.364" x5="185.392" x6="185.426" x7="185.468" x8="185.519" x9="185.576" y20="-37.1734" y21="-37.1113" y22="-37.0576" y23="-37.0137" y24="-36.9772" style="line-style:normal;line-weight:thin;filling:none;color:black" antialias="false" x10="185.641" x11="185.716" x12="185.761" x13="185.812" x14="185.868" x15="185.931" x16="186.012" x17="186.1" x18="186.189" x19="186.287" y1="-39.3507" y2="-39.2124" y3="-39.0699" y4="-38.9245" y5="-38.7764" y6="-38.6296" y7="-38.4843" y8="-38.3375" y9="-38.1936" y10="-38.0511" y11="-37.9114" y12="-37.8352" y13="-37.7561" y14="-37.6743"/>
                                        <polygon closed="false" antialias="false" y1="-40.9241" y2="-41.0045" y3="-41.0779" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="186.416" x2="186.657" x3="186.907"/>
                                        <polygon x6="188.678" closed="false" antialias="false" y1="-41.1823" y2="-41.2316" y3="-41.2739" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="187.338" y4="-41.3093" x2="187.597" y5="-41.3363" x3="187.862" y6="-41.3549" x4="188.13" x5="188.402"/>
                                        <polygon closed="false" antialias="false" y1="-40.2609" y2="-40.4246" y3="-40.5925" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="186.541" y4="-40.7562" x2="186.512" y5="-40.9241" x3="186.479" x4="186.448" x5="186.416"/>
                                        <polygon x6="185.827" x7="185.937" x8="186.052" closed="false" x9="186.17" y10="-40.9894" y11="-40.9216" x10="186.291" x11="186.416" y1="-41.1104" y2="-41.14" y3="-41.1612" y4="-41.1696" y5="-41.1644" y6="-41.1517" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="185.328" y7="-41.1278" x2="185.419" antialias="false" y8="-41.0924" y9="-41.0458" x3="185.515" x4="185.615" x5="185.719"/>
                                        <polygon x6="186.603" x7="186.541" closed="false" antialias="false" y1="-41.0779" y2="-40.9354" y3="-40.7971" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="186.907" y4="-40.6631" x2="186.846" y5="-40.5234" x3="186.788" y6="-40.3893" x4="186.729" y7="-40.2609" x5="186.665"/>
                                        <polygon x6="188.054" x7="188.185" x8="188.314" closed="false" x9="188.438" y10="-39.2928" y11="-39.1306" x10="188.559" x11="188.678" y1="-41.1823" y2="-40.9311" y3="-40.6927" y4="-40.4627" y5="-40.244" y6="-40.0337" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="187.338" y7="-39.8347" x2="187.489" antialias="false" y8="-39.6456" y9="-39.465" x3="187.636" x4="187.779" x5="187.918"/>
                                        <polygon closed="false" antialias="false" y1="-38.7962" y2="-38.7861" y3="-38.765" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="186.907" x2="187.12" x3="187.338"/>
                                        <polygon x6="184.825" x7="184.749" x8="184.681" closed="false" x9="184.622" y10="-49.5234" y11="-49.625" x10="184.573" y12="-49.728" x11="184.532" y13="-49.831" x12="184.501" y14="-49.9341" x13="184.477" y15="-50.0385" x14="184.464" x15="184.459" y1="-48.6768" y2="-48.7628" y3="-48.8517" y4="-48.942" y5="-49.0338" y6="-49.1297" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="185.328" y7="-49.2257" x2="185.211" antialias="false" y8="-49.3245" x3="185.102" y9="-49.4232" x4="185.002" x5="184.909"/>
                                        <polygon x6="182.999" x7="183.123" x8="183.243" closed="false" x9="183.353" y10="-50.0978" y11="-50.1401" x10="183.456" y12="-50.1853" x11="183.534" y13="-50.2333" x12="183.603" y14="-50.2841" x13="183.665" y15="-50.3377" x14="183.718" y16="-50.3927" x15="183.762" x16="183.797" y1="-49.9284" y2="-49.9115" y3="-49.9058" y4="-49.9115" y5="-49.9284" y6="-49.9496" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="182.188" y7="-49.9764" x2="182.357" antialias="false" y8="-50.0117" x3="182.528" y9="-50.0512" x4="182.699" x5="182.868"/>
                                        <polygon y15="-51.4693" closed="false" y16="-51.5639" y17="-51.6528" y18="-51.7375" x20="192.098" y19="-51.8165" x21="191.895" x22="191.685" x1="194.037" x2="194.031" x3="194.016" x4="193.989" x5="193.951" x6="193.904" x7="193.846" x8="193.779" x9="193.7" y20="-51.8913" y21="-51.9618" y22="-52.0267" style="line-style:normal;line-weight:thin;filling:none;color:black" antialias="false" x10="193.612" x11="193.515" x12="193.406" x13="193.278" x14="193.138" x15="192.987" x16="192.828" x17="192.658" x18="192.48" x19="192.294" y1="-49.9891" y2="-50.102" y3="-50.2135" y4="-50.3249" y5="-50.435" y6="-50.5437" y7="-50.6523" y8="-50.7581" y9="-50.8626" y10="-50.9656" y11="-51.0672" y12="-51.166" y13="-51.2704" y14="-51.372"/>
                                        <polygon y1="-47.6481" y2="-47.6382" y3="-47.6382" y4="-47.6466" y5="-47.665" y6="-47.6918" y7="-47.7257" y8="-47.7694" y9="-47.8217" y30="-49.6632" y31="-49.7718" y32="-49.8805" y33="-49.9891" x10="191.425" x11="191.637" x12="191.84" x13="192.037" x14="192.228" x15="192.411" x16="192.586" x17="192.753" style="line-style:normal;line-weight:thin;filling:none;color:black" x18="192.911" x19="193.06" x20="193.2" x21="193.331" x22="193.441" x23="193.543" x24="193.636" x25="193.72" x26="193.793" x27="193.856" x28="193.911" x29="193.956" y10="-47.8823" y11="-47.9388" y12="-47.9995" y13="-48.0658" y14="-48.1363" y15="-48.2111" y16="-48.2902" y17="-48.3748" y18="-48.4623" y19="-48.554" closed="false" x30="193.992" x31="194.016" x32="194.031" x33="194.037" x1="188.892" x2="189.183" x3="189.473" x4="189.763" x5="190.049" x6="190.333" x7="190.614" x8="190.89" x9="191.161" y20="-48.65" y21="-48.7502" y22="-48.8447" y23="-48.9407" y24="-49.0395" y25="-49.1396" antialias="false" y26="-49.2412" y27="-49.3457" y28="-49.4501" y29="-49.5559"/>
                                        <polygon x6="164.796" x7="164.72" x8="164.652" closed="false" x9="164.593" y10="-55.3062" y11="-55.4078" x10="164.544" y12="-55.5094" x11="164.503" y13="-55.6124" x12="164.472" y14="-55.7168" x13="164.448" y15="-55.8198" x14="164.435" x15="164.429" y1="-54.4581" y2="-54.5442" y3="-54.6331" y4="-54.7234" y5="-54.8165" y6="-54.911" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="165.298" y7="-55.007" x2="165.181" antialias="false" y8="-55.1058" x3="165.073" y9="-55.206" x4="164.972" x5="164.879"/>
                                        <polygon closed="false" antialias="false" y1="-50.8456" y2="-50.7963" y3="-50.7455" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="179.879" y4="-50.6932" x2="179.857" x3="179.844" x4="179.839"/>
                                        <polygon closed="false" antialias="false" y1="-51.3198" y2="-51.3621" y3="-51.4044" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="184.293" y4="-51.4468" x2="184.312" x3="184.323" x4="184.328"/>
                                        <polygon x6="184.22" x7="184.175" x8="184.123" closed="false" x9="184.054" y10="-51.8221" y11="-51.8545" x10="183.975" y12="-51.8814" x11="183.89" y13="-51.9025" x12="183.798" y14="-51.9195" x13="183.701" x14="183.599" y1="-51.4468" y2="-51.4919" y3="-51.5385" y4="-51.5822" y5="-51.626" y6="-51.6669" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="184.327" y7="-51.7064" x2="184.322" antialias="false" y8="-51.7445" x3="184.308" y9="-51.7854" x4="184.286" x5="184.258"/>
                                        <polygon x6="179.966" x7="180.02" x8="180.083" closed="false" x9="180.167" y10="-50.2431" y11="-50.205" x10="180.261" y12="-50.1725" x11="180.363" y13="-50.1457" x12="180.473" y14="-50.126" x13="180.59" x14="180.711" y1="-50.6932" y2="-50.6382" y3="-50.5846" y4="-50.531" y5="-50.4787" y6="-50.4294" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="179.84" y7="-50.3814" x2="179.845" antialias="false" y8="-50.3362" x3="179.86" y9="-50.2868" x4="179.886" x5="179.921"/>
                                        <polygon x6="164.191" x7="164.146" x8="164.094" closed="false" x9="164.024" y10="-57.6034" y11="-57.6359" x10="163.945" y12="-57.6627" x11="163.861" y13="-57.6853" x12="163.769" y14="-57.7022" x13="163.672" x14="163.57" y1="-57.2281" y2="-57.2747" y3="-57.3198" y4="-57.3649" y5="-57.4073" y6="-57.4496" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="164.298" y7="-57.4891" x2="164.293" antialias="false" y8="-57.5272" x3="164.278" y9="-57.5681" x4="164.257" x5="164.229"/>
                                        <polygon closed="false" antialias="false" y1="-57.1011" y2="-57.1434" y3="-57.1858" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="164.264" y4="-57.2281" x2="164.283" x3="164.294" x4="164.299"/>
                                        <polygon y1="-53.4294" y2="-53.4209" y3="-53.4209" y4="-53.4294" y5="-53.4463" y6="-53.4731" y7="-53.5084" y8="-53.5522" y9="-53.6044" y30="-55.4459" y31="-55.5532" y32="-55.6618" y33="-55.7719" x10="171.396" x11="171.607" x12="171.811" x13="172.008" x14="172.199" x15="172.382" x16="172.557" x17="172.724" style="line-style:normal;line-weight:thin;filling:none;color:black" x18="172.882" x19="173.031" x20="173.171" x21="173.302" x22="173.412" x23="173.514" x24="173.607" x25="173.69" x26="173.764" x27="173.827" x28="173.882" x29="173.927" y10="-53.6651" y11="-53.7201" y12="-53.7822" y13="-53.8471" y14="-53.9177" y15="-53.9925" y16="-54.0729" y17="-54.1562" y18="-54.2451" y19="-54.3368" closed="false" x30="173.963" x31="173.986" x32="174.002" x33="174.008" x1="168.863" x2="169.153" x3="169.444" x4="169.732" x5="170.02" x6="170.304" x7="170.584" x8="170.861" x9="171.132" y20="-54.4327" y21="-54.5329" y22="-54.6261" y23="-54.7234" y24="-54.8208" y25="-54.921" antialias="false" y26="-55.024" y27="-55.127" y28="-55.2328" y29="-55.3387"/>
                                        <polygon y1="-50.0385" y2="-50.1514" y3="-50.2628" y4="-50.3743" y5="-50.4844" y6="-50.593" y7="-50.7003" y8="-50.8075" y9="-50.912" y30="-52.3908" y31="-52.3851" y32="-52.3696" y33="-52.3456" y34="-52.3103" y35="-52.2652" y36="-52.2116" y37="-52.1481" y38="-52.0747" x10="184.883" x11="184.982" x12="185.089" x13="185.219" x14="185.359" x15="185.509" x16="185.668" x17="185.837" style="line-style:normal;line-weight:thin;filling:none;color:black" x18="186.015" x19="186.203" x20="186.398" x21="186.601" x22="186.811" x23="187.083" x24="187.364" x25="187.652" x26="187.946" x27="188.245" x28="188.548" x29="188.854" y10="-51.015" y11="-51.1152" y12="-51.2139" y13="-51.3198" y14="-51.4214" y15="-51.5187" y16="-51.6119" y17="-51.7022" y18="-51.7854" y19="-51.8659" closed="false" x30="189.163" x31="189.472" x32="189.779" x33="190.082" x1="184.458" x34="190.381" x2="184.464" x35="190.675" x3="184.481" x36="190.963" x4="184.508" x37="191.243" x5="184.545" x38="191.516" x6="184.593" x7="184.649" x8="184.718" x9="184.796" y20="-51.9407" y21="-52.0112" y22="-52.0747" y23="-52.1481" y24="-52.2116" y25="-52.2652" antialias="false" y26="-52.3103" y27="-52.3456" y28="-52.3696" y29="-52.3851"/>
                                        <polygon y1="-28.9664" y2="-28.5317" y3="-28.0901" y4="-27.6413" y5="-27.1855" y6="-26.7241" y7="-26.2542" y8="-25.78" y9="-25.2989" y30="-14.7339" y31="-14.1765" y32="-13.6191" y33="-13.0603" y34="-12.5015" y35="-11.9427" y36="-11.3839" y37="-10.8265" y38="-10.2677" y39="-9.71031" x10="200.583" x11="200.47" x12="200.369" x13="200.278" x14="200.199" x15="200.136" y40="-9.15294" x16="200.082" y41="-8.59695" x17="200.038" style="line-style:normal;line-weight:thin;filling:none;color:black" x18="200.004" x19="199.979" x20="199.965" x21="199.959" x22="199.965" x23="199.979" x24="200.004" x25="200.038" x26="200.082" x27="200.136" x28="200.199" x29="200.278" y10="-24.812" y11="-24.3195" y12="-23.8214" y13="-23.3177" y14="-22.8082" y15="-22.3313" y16="-21.8501" y17="-21.3661" y18="-20.8778" y19="-20.3868" closed="false" x30="200.369" x31="200.47" x32="200.583" x33="200.706" x1="202.086" x34="200.841" x2="201.876" x35="200.987" x3="201.677" x36="201.143" x4="201.488" x37="201.31" x5="201.31" x38="201.488" x6="201.143" x39="201.677" x7="200.987" x8="200.841" x9="200.706" y20="-19.8929" y21="-19.3948" y22="-18.8953" y23="-18.3929" y24="-17.8877" y25="-17.3797" antialias="false" y26="-16.8703" y27="-16.3581" y28="-15.8444" y29="-15.2898" x40="201.876" x41="202.086"/>
                                        <polygon x6="54.519" x7="54.4922" x8="54.4725" closed="false" x9="54.4612" y10="-31.6376" x10="54.457" y1="-32.5294" y2="-32.4475" y3="-32.3544" y4="-32.2528" y5="-32.1427" y6="-32.0496" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="54.8295" y7="-31.9522" x2="54.7448" antialias="false" y8="-31.8506" y9="-31.7448" x3="54.67" x4="54.6065" x5="54.5529"/>
                                        <polygon y1="-29.8624" y2="-29.9358" y3="-30.0148" y4="-30.1023" y5="-30.1954" y6="-30.2956" y7="-30.4015" y8="-30.5115" y9="-30.6272" y30="-32.751" y31="-32.7721" y32="-32.7848" y33="-32.7848" y34="-32.7764" y35="-32.7579" y36="-32.7309" y37="-32.6944" y38="-32.6478" y39="-32.5928" x10="57.512" x11="57.5077" x12="57.495" x13="57.4724" x14="57.44" x15="57.4005" y40="-32.5278" x16="57.3511" x17="57.2918" style="line-style:normal;line-weight:thin;filling:none;color:black" x18="57.2156" x19="57.1296" x20="57.035" x21="56.932" x22="56.8205" x23="56.7034" x24="56.5792" x25="56.4663" x26="56.3506" x27="56.2335" x28="56.115" x29="55.995" y10="-30.7457" y11="-30.8671" y12="-30.9899" y13="-31.1127" y14="-31.2382" y15="-31.3624" y16="-31.4852" y17="-31.608" y18="-31.7448" y19="-31.876" closed="false" x30="55.8751" x31="55.7566" x32="55.638" x33="55.5223" x1="57.1395" x34="55.4094" x2="57.2143" x35="55.2994" x3="57.282" x36="55.1949" x4="57.3413" x37="55.0947" x5="57.3921" x38="55.0002" x6="57.4344" x39="54.9113" x7="57.4668" x8="57.4908" x9="57.5063" y20="-32.0017" y21="-32.1216" y22="-32.2331" y23="-32.3375" y24="-32.432" y25="-32.5068" antialias="false" y26="-32.5732" y27="-32.6324" y28="-32.6806" y29="-32.7213" x40="54.8295"/>
                                        <polygon closed="false" antialias="false" y1="-29.7636" y2="-29.8102" y3="-29.8626" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="57.0026" x2="57.0732" x3="57.1395"/>
                                        <polygon x6="88.7611" closed="false" antialias="false" y1="-37.3088" y2="-37.2341" y3="-37.1508" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="89.0461" y4="-37.0591" x2="88.9699" y5="-36.9603" x3="88.9022" y6="-36.8531" x4="88.8457" x5="88.7977"/>
                                        <polygon x6="89.9111" x7="89.801" x8="89.6924" closed="false" x9="89.5866" y10="-37.5175" y11="-37.4937" x10="89.485" y12="-37.4614" x11="89.3862" y13="-37.4191" x12="89.293" y14="-37.3683" x13="89.2056" y15="-37.309" x14="89.1223" x15="89.0461" y1="-37.3116" y2="-37.3709" y3="-37.4201" y4="-37.4625" y5="-37.4947" y6="-37.5175" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="90.4614" y7="-37.5318" x2="90.3542" antialias="false" y8="-37.5376" x3="90.2441" y9="-37.5318" x4="90.1327" x5="90.0226"/>
                                        <polygon y15="-37.0337" closed="false" y16="-37.1141" y17="-37.1875" y18="-37.2538" y19="-37.3116" x1="91.3377" x2="91.3617" x3="91.3744" x4="91.3787" x5="91.373" x6="91.3589" x7="91.3349" x8="91.3025" x9="91.2601" style="line-style:normal;line-weight:thin;filling:none;color:black" antialias="false" x10="91.2107" x11="91.1515" x12="91.0866" x13="91.0132" x14="90.9328" x15="90.8481" x16="90.7578" x17="90.6632" x18="90.5645" x19="90.4614" y1="-35.5943" y2="-35.6917" y3="-35.7919" y4="-35.8963" y5="-36.0035" y6="-36.1122" y7="-36.2223" y8="-36.3324" y9="-36.4424" y10="-36.5496" y11="-36.6541" y12="-36.7557" y13="-36.8531" y14="-36.9462"/>
                                        <polygon y15="-57.262" closed="false" y16="-57.7784" y17="-58.2977" y18="-58.8198" x20="55.5449" y19="-59.3433" x21="55.4984" x22="55.4405" x23="55.3728" x24="55.2937" x25="55.2048" x26="55.1061" x27="54.9974" x28="54.8775" x29="54.7476" x1="54.457" x2="54.6065" x3="54.7476" x4="54.8775" x5="54.9974" x6="55.1061" x7="55.2048" x8="55.2937" x9="55.3728" y20="-59.8711" y21="-60.3989" y22="-60.9294" y23="-61.4614" y24="-61.9948" style="line-style:normal;line-weight:thin;filling:none;color:black" antialias="false" y25="-62.5282" y26="-63.0644" y27="-63.6021" y28="-64.1397" x30="54.6065" x31="54.457" y29="-64.6773" x10="55.4405" x11="55.4984" x12="55.5449" x13="55.5816" x14="55.6084" x15="55.6239" x16="55.6296" x17="55.6239" x18="55.6084" x19="55.5816" y1="-50.4787" y2="-50.9303" y3="-51.3889" y4="-51.8518" y5="-52.3202" y6="-52.7944" y7="-53.2727" y8="-53.7553" y9="-54.2436" y30="-65.2164" y31="-65.7554" y10="-54.7361" y11="-55.2342" y12="-55.7351" y13="-56.2403" y14="-56.7483"/>
                                        <polygon y15="-57.2521" closed="false" y16="-57.3452" y17="-57.4341" y18="-57.5188" x20="172.069" y19="-57.5992" x21="171.865" x22="171.655" x1="174.008" x2="174.002" x3="173.987" x4="173.96" x5="173.921" x6="173.875" x7="173.817" x8="173.749" x9="173.67" y20="-57.674" y21="-57.7431" y22="-57.8081" style="line-style:normal;line-weight:thin;filling:none;color:black" antialias="false" x10="173.583" x11="173.485" x12="173.377" x13="173.248" x14="173.109" x15="172.958" x16="172.798" x17="172.629" x18="172.451" x19="172.265" y1="-55.7718" y2="-55.8833" y3="-55.9962" y4="-56.1063" y5="-56.2163" y6="-56.3264" y7="-56.4336" y8="-56.5409" y9="-56.6453" y10="-56.7483" y11="-56.8485" y12="-56.9473" y13="-57.0531" y14="-57.1547"/>
                                        <polygon x6="168.648" closed="false" antialias="false" y1="-46.9637" y2="-47.0145" y3="-47.0568" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="167.309" y4="-47.0907" x2="167.567" y5="-47.1175" x3="167.833" y6="-47.1359" x4="168.101" x5="168.373"/>
                                        <polygon x6="168.023" x7="168.156" x8="168.284" closed="false" x9="168.408" y10="-45.0756" y11="-44.9133" x10="168.53" x11="168.648" y1="-46.9637" y2="-46.7139" y3="-46.474" y4="-46.244" y5="-46.0253" y6="-45.8164" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="167.309" y7="-45.6175" x2="167.46" antialias="false" y8="-45.427" y9="-45.2463" x3="167.607" x4="167.749" x5="167.889"/>
                                        <polygon y15="-42.8218" closed="false" y16="-42.8726" y17="-42.9248" y18="-42.9756" x1="166.951" x2="167.045" x3="167.138" x4="167.232" x5="167.325" x6="167.387" x7="167.454" x8="167.529" x9="167.611" style="line-style:normal;line-weight:thin;filling:none;color:black" antialias="false" x10="167.696" x11="167.755" x12="167.82" x13="167.891" x14="167.967" x15="168.047" x16="168.137" x17="168.218" x18="168.287" y1="-42.7106" y2="-42.6866" y3="-42.6697" y4="-42.6584" y5="-42.6527" y6="-42.6527" y7="-42.6554" y8="-42.6624" y9="-42.6751" y10="-42.6921" y11="-42.7076" y12="-42.7273" y13="-42.7513" y14="-42.7837"/>
                                        <polygon closed="false" antialias="false" y1="-44.5789" y2="-44.5676" y3="-44.5479" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="166.877" x2="167.09" x3="167.309"/>
                                        <polygon y15="-43.3752" closed="false" y16="-43.3089" y17="-43.2412" y18="-43.172" x20="166.238" y19="-43.1043" x21="166.315" x22="166.388" x23="166.457" x24="166.563" x25="166.672" x26="166.782" x1="165.298" x2="165.304" x3="165.315" x4="165.334" x5="165.362" x6="165.396" x7="165.439" x8="165.489" x9="165.547" y20="-43.0394" y21="-42.9843" y22="-42.9363" y23="-42.8954" y24="-42.8418" style="line-style:normal;line-weight:thin;filling:none;color:black" antialias="false" y25="-42.7967" y26="-42.76" x10="165.612" x11="165.687" x12="165.732" x13="165.783" x14="165.839" x15="165.901" x16="165.956" x17="166.018" x18="166.086" x19="166.159" y1="-45.132" y2="-44.9938" y3="-44.8512" y4="-44.7059" y5="-44.5591" y6="-44.411" y7="-44.2656" y8="-44.1203" y9="-43.9749" y10="-43.8324" y11="-43.6927" y12="-43.6165" y13="-43.5375" y14="-43.4571"/>
                                        <polygon x6="165.798" x7="165.908" x8="166.022" closed="false" x9="166.141" y10="-46.773" y11="-46.7052" x10="166.262" x11="166.386" y1="-46.8917" y2="-46.9228" y3="-46.9425" y4="-46.951" y5="-46.9494" y6="-46.9352" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="165.298" y7="-46.9113" x2="165.39" antialias="false" y8="-46.876" y9="-46.8308" x3="165.486" x4="165.586" x5="165.689"/>
                                        <polygon closed="false" antialias="false" y1="-46.7054" y2="-46.7873" y3="-46.8607" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="166.386" x2="166.628" x3="166.877"/>
                                        <polygon x6="166.574" x7="166.512" closed="false" antialias="false" y1="-46.8607" y2="-46.7167" y3="-46.5784" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="166.877" y4="-46.4458" x2="166.817" y5="-46.3047" x3="166.757" y6="-46.1706" x4="166.7" y7="-46.0422" x5="166.636"/>
                                        <polygon closed="false" antialias="false" y1="-46.0422" y2="-46.2059" y3="-46.3738" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="166.512" y4="-46.5375" x2="166.482" y5="-46.7054" x3="166.45" x4="166.419" x5="166.386"/>
                                        <polygon closed="false" antialias="false" y1="-56.6284" y2="-56.5776" y3="-56.5268" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="159.85" y4="-56.476" x2="159.827" x3="159.815" x4="159.809"/>
                                        <polygon x6="159.937" x7="159.991" x8="160.054" closed="false" x9="160.137" y10="-56.0244" y11="-55.9863" x10="160.232" y12="-55.9539" x11="160.333" y13="-55.927" x12="160.444" y14="-55.9073" x13="160.561" x14="160.682" y1="-56.476" y2="-56.4209" y3="-56.3659" y4="-56.3123" y5="-56.2615" y6="-56.2107" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="159.811" y7="-56.1627" x2="159.816" antialias="false" y8="-56.1175" x3="159.831" y9="-56.0682" x4="159.857" x5="159.892"/>
                                        <polygon x6="163.504" x7="163.427" x8="163.324" closed="false" x9="163.212" y10="-55.7591" y11="-55.7309" x10="163.094" y12="-55.7097" x11="162.968" y13="-55.6928" x12="162.838" y14="-55.6872" x13="162.669" y15="-55.6928" x14="162.498" y16="-55.7097" x15="162.327" x16="162.158" y1="-56.174" y2="-56.119" y3="-56.0667" y4="-56.0159" y5="-55.9679" y6="-55.9214" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="163.767" y7="-55.879" x2="163.732" antialias="false" y8="-55.8339" x3="163.688" y9="-55.793" x4="163.635" x5="163.573"/>
                                        <polygon y15="-56.8741" closed="false" y16="-56.9686" y17="-57.0716" y18="-57.1817" x20="141.609" y19="-57.2762" x21="141.576" x22="141.552" x23="141.538" x24="141.534" x1="143.174" x2="143.107" x3="143.035" x4="142.958" x5="142.876" x6="142.788" x7="142.698" x8="142.605" x9="142.512" y20="-57.3736" y21="-57.471" y22="-57.5683" y23="-57.6657" y24="-57.7616" style="line-style:normal;line-weight:thin;filling:none;color:black" antialias="false" x10="142.417" x11="142.324" x12="142.231" x13="142.141" x14="142.038" x15="141.94" x16="141.851" x17="141.771" x18="141.7" x19="141.651" y1="-56.6778" y2="-56.6284" y3="-56.5875" y4="-56.5564" y5="-56.5352" y6="-56.524" y7="-56.5213" y8="-56.5298" y9="-56.5467" y10="-56.5749" y11="-56.6116" y12="-56.6567" y13="-56.7118" y14="-56.788"/>
                                        <polygon x6="143.309" x7="143.269" x8="143.224" closed="false" x9="143.174" y1="-57.2224" y2="-57.1406" y3="-57.0616" y4="-56.9854" y5="-56.9134" y6="-56.8471" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="143.401" y7="-56.785" antialias="false" x2="143.396" y8="-56.7286" y9="-56.6778" x3="143.387" x4="143.367" x5="143.341"/>
                                        <polygon y15="-58.1636" closed="false" y16="-58.2567" y17="-58.3498" y18="-58.4416" x1="143.401" x2="143.31" x3="143.221" x4="143.133" x5="143.044" x6="142.958" x7="142.873" x8="142.777" x9="142.688" style="line-style:normal;line-weight:thin;filling:none;color:black" antialias="false" x10="142.606" x11="142.533" x12="142.469" x13="142.423" x14="142.386" x15="142.356" x16="142.335" x17="142.323" x18="142.317" y1="-57.2069" y2="-57.2224" y3="-57.2464" y4="-57.2803" y5="-57.3212" y6="-57.3705" y7="-57.427" y8="-57.5032" y9="-57.5893" y10="-57.6824" y11="-57.7826" y12="-57.8884" y13="-57.9787" y14="-58.0704"/>
                                        <polygon y1="-55.8198" y2="-55.9327" y3="-56.0442" y4="-56.1556" y5="-56.2657" y6="-56.3744" y7="-56.483" y8="-56.5889" y9="-56.6933" y30="-58.1721" y31="-58.1679" y32="-58.1524" y33="-58.127" y34="-58.0917" y35="-58.0479" y36="-57.9929" y37="-57.9294" y38="-57.8574" x10="164.854" x11="164.953" x12="165.06" x13="165.19" x14="165.33" x15="165.479" x16="165.639" x17="165.808" style="line-style:normal;line-weight:thin;filling:none;color:black" x18="165.986" x19="166.172" x20="166.368" x21="166.571" x22="166.782" x23="167.054" x24="167.335" x25="167.623" x26="167.916" x27="168.215" x28="168.519" x29="168.825" y10="-56.7963" y11="-56.8979" y12="-56.9967" y13="-57.1011" y14="-57.2027" y15="-57.3015" y16="-57.3946" y17="-57.4835" y18="-57.5682" y19="-57.6472" closed="false" x30="169.134" x31="169.443" x32="169.749" x33="170.053" x1="164.429" x34="170.352" x2="164.435" x35="170.645" x3="164.452" x36="170.933" x4="164.477" x37="171.214" x5="164.515" x38="171.486" x6="164.562" x7="164.62" x8="164.689" x9="164.767" y20="-57.7234" y21="-57.7925" y22="-57.8574" y23="-57.9294" y24="-57.9929" y25="-58.0479" antialias="false" y26="-58.0917" y27="-58.127" y28="-58.1524" y29="-58.1679"/>
                                        <polygon y1="-85.3431" y2="-85.4545" y3="-85.5674" y4="-85.6775" y5="-85.7876" y6="-85.8976" y7="-86.0049" y8="-86.1107" y9="-86.2165" y30="-87.6939" y31="-87.6897" y32="-87.6742" y33="-87.6488" y34="-87.6149" y35="-87.5698" y36="-87.5162" y37="-87.4527" y38="-87.3793" x10="62.5864" x11="62.6837" x12="62.7924" x13="62.9208" x14="63.0605" x15="63.2115" x16="63.371" x17="63.5403" style="line-style:normal;line-weight:thin;filling:none;color:black" x18="63.7181" x19="63.9044" x20="64.1005" x21="64.3037" x22="64.514" x23="64.7863" x24="65.0671" x25="65.355" x26="65.6485" x27="65.9476" x28="66.251" x29="66.5572" y10="-86.3196" y11="-86.4197" y12="-86.5185" y13="-86.6244" y14="-86.726" y15="-86.8233" y16="-86.9165" y17="-87.0054" y18="-87.09" y19="-87.1705" closed="false" x30="66.8663" x31="67.1753" x32="67.4815" x33="67.7849" x1="62.1616" x34="68.0827" x2="62.1673" x35="68.3776" x3="62.1828" x36="68.6654" x4="62.2096" x37="68.9448" x5="62.2477" x38="69.2172" x6="62.2943" x7="62.3521" x8="62.4199" x9="62.4989" y20="-87.2452" y21="-87.3144" y22="-87.3793" y23="-87.4527" y24="-87.5162" y25="-87.5698" antialias="false" y26="-87.6149" y27="-87.6488" y28="-87.6742" y29="-87.6897"/>
                                        <polygon y15="-72.6628" closed="false" y16="-72.5782" y17="-72.502" y18="-72.4328" x20="64.3869" y19="-72.3735" x21="64.5139" x1="62.8164" x2="62.8206" x3="62.8361" x4="62.8587" x5="62.8911" x6="62.9335" x7="62.9843" x8="63.0435" x9="63.124" y20="-72.3227" y21="-72.2818" style="line-style:normal;line-weight:thin;filling:none;color:black" antialias="false" x10="63.2143" x11="63.3131" x12="63.4231" x13="63.5403" x14="63.6644" x15="63.7773" x16="63.8944" x17="64.013" x18="64.1357" x19="64.2599" y1="-74.469" y2="-74.3406" y3="-74.2108" y4="-74.0796" y5="-73.9469" y6="-73.8157" y7="-73.6845" y8="-73.5546" y9="-73.4065" y10="-73.2625" y11="-73.1257" y12="-72.9944" y13="-72.8703" y14="-72.7545"/>
                                        <polygon y15="-73.3303" closed="false" y16="-73.446" y17="-73.5659" y18="-73.6252" x20="63.1776" y19="-73.6915" x21="63.1522" x22="63.1282" x23="63.1127" x24="63.0972" x25="63.0831" x26="63.0676" x27="63.0549" x28="63.0464" x29="63.038" x1="64.5139" x2="64.4392" x3="64.3601" x4="64.2769" x5="64.188" x6="64.1033" x7="64.0257" x8="63.9551" x9="63.8916" y20="-73.7649" y21="-73.8467" y22="-73.9328" y23="-73.9935" y24="-74.0612" style="line-style:normal;line-weight:thin;filling:none;color:black" antialias="false" y25="-74.1346" y26="-74.2164" y27="-74.3025" y28="-74.3773" x30="63.0323" x31="63.0307" y29="-74.462" x10="63.7844" x11="63.6828" x12="63.5883" x13="63.4994" x14="63.4189" x15="63.3568" x16="63.3004" x17="63.2496" x18="63.227" x19="63.203" y1="-72.2818" y2="-72.3058" y3="-72.3354" y4="-72.3721" y5="-72.4172" y6="-72.468" y7="-72.5203" y8="-72.5739" y9="-72.6261" y30="-74.5551" y31="-74.6539" y10="-72.7277" y11="-72.8378" y12="-72.9563" y13="-73.0819" y14="-73.2145"/>
                                        <polygon x6="63.8789" x7="64.0765" x8="64.2811" closed="false" x9="64.4942" y10="-76.4178" y11="-76.4785" x10="64.7468" y12="-76.5307" x11="65.005" y13="-76.5758" x12="65.2703" y14="-76.6111" x13="65.5412" y15="-76.6393" x14="65.8164" y16="-76.6577" x15="66.0972" x16="66.3808" y1="-75.6798" y2="-75.78" y3="-75.8759" y4="-75.9676" y5="-76.0537" y6="-76.1356" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="63.0309" y7="-76.2132" x2="63.1804" antialias="false" y8="-76.2837" x3="63.3413" y9="-76.3501" x4="63.5121" x5="63.6913"/>
                                        <polygon x6="62.5271" x7="62.4523" x8="62.3846" closed="false" x9="62.3253" y10="-84.828" y11="-84.9296" x10="62.2759" y12="-85.0326" x11="62.235" y13="-85.1356" x12="62.2026" y14="-85.2386" x13="62.18" y15="-85.3431" x14="62.1659" x15="62.1616" y1="-83.9813" y2="-84.0674" y3="-84.1549" y4="-84.2452" y5="-84.3384" y6="-84.4329" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="63.0309" y7="-84.5303" x2="62.9137" antialias="false" y8="-84.6276" x3="62.8051" y9="-84.7278" x4="62.7049" x5="62.6118"/>
                                        <polygon x6="65.7233" x7="65.6598" x8="65.5892" closed="false" x9="65.513" y10="-72.2141" y11="-72.1915" x10="65.4283" y12="-72.1774" x11="65.307" y13="-72.1758" x12="65.1828" y14="-72.18" x13="65.0572" y15="-72.1913" x14="64.9641" y16="-72.2082" x15="64.8695" x16="64.7764" y17="-72.2322" x17="64.6833" y1="-72.4977" y2="-72.4483" y3="-72.4074" y4="-72.3721" y5="-72.3439" y6="-72.3171" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="66.0196" y7="-72.2889" x2="65.9533" antialias="false" y8="-72.2621" x3="65.8898" y9="-72.2367" x4="65.8319" x5="65.7783"/>
                                        <polygon x6="83.9082" x7="84.1058" x8="84.3104" closed="false" x9="84.5235" y10="-70.6365" y11="-70.6971" x10="84.7761" y12="-70.7494" x11="85.0343" y13="-70.7931" x12="85.2996" y14="-70.8298" x13="85.5705" y15="-70.8566" x14="85.8471" y16="-70.8764" x15="86.1265" x16="86.4101" y1="-69.8985" y2="-69.9986" y3="-70.0946" y4="-70.1863" y5="-70.2724" y6="-70.3542" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="83.0602" y7="-70.4304" x2="83.2097" antialias="false" y8="-70.5024" x3="83.3706" y9="-70.5673" x4="83.5414" x5="83.7206"/>
                                        <polygon x6="65.4975" x7="65.3888" x8="65.2774" closed="false" x9="65.1616" y10="-72.1675" y11="-72.1802" x10="65.0445" y12="-72.2028" x11="64.926" y13="-72.2324" x12="64.8046" x13="64.6833" y1="-72.4483" y2="-72.3834" y3="-72.327" y4="-72.2776" y5="-72.2381" y6="-72.2056" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="65.966" y7="-72.183" x2="65.8841" antialias="false" y8="-72.1689" x3="65.7952" y9="-72.1632" x4="65.7007" x5="65.6019"/>
                                        <polygon x6="65.5441" x7="65.6132" x8="65.6894" closed="false" x9="65.7727" y10="-72.7969" y11="-72.8477" x10="65.8545" y12="-72.8914" x11="65.9307" y13="-72.9295" x12="66.0041" y14="-72.9676" x13="66.0718" y15="-73.0057" x14="66.1494" y16="-73.041" x15="66.2355" x16="66.3301" y1="-72.1887" y2="-72.255" y3="-72.3242" y4="-72.3933" y5="-72.4582" y6="-72.5274" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="65.2872" y7="-72.5979" x2="65.3296" antialias="false" y8="-72.6685" x3="65.3761" y9="-72.7376" x4="65.4298" x5="65.482"/>
                                        <polygon x6="82.5564" x7="82.4816" x8="82.4139" closed="false" x9="82.3546" y10="-79.0467" y11="-79.1483" x10="82.3052" y12="-79.2499" x11="82.2643" y13="-79.3529" x12="82.2319" y14="-79.4573" x13="82.2093" y15="-79.5603" x14="82.1952" x15="82.1909" y1="-78.1986" y2="-78.2847" y3="-78.3736" y4="-78.4639" y5="-78.557" y6="-78.6516" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="83.0602" y7="-78.7475" x2="82.943" antialias="false" y8="-78.8463" x3="82.8344" y9="-78.9451" x4="82.7342" x5="82.6411"/>
                                        <polygon x6="92.286" x7="92.413" x8="92.54" closed="false" x9="92.667" y10="-78.1492" y11="-78.121" x10="92.7884" y12="-78.0857" x11="92.9027" y13="-78.0434" x12="93.0099" x13="93.1059" y1="-78.0434" y2="-78.0857" y3="-78.121" y4="-78.1492" y5="-78.1704" y6="-78.1831" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="91.7202" y7="-78.1873" x2="91.8161" antialias="false" y8="-78.1831" x3="91.9234" y9="-78.1704" x4="92.0377" x5="92.159"/>
                                        <polygon y15="-80.9926" closed="false" y16="-81.0857" y17="-81.1746" y18="-81.2593" x20="89.8307" y19="-81.3383" x21="89.6275" x22="89.4172" x1="91.7695" x2="91.7639" x3="91.747" x4="91.7201" x5="91.6835" x6="91.6369" x7="91.579" x8="91.5099" x9="91.4323" y20="-81.4145" y21="-81.4837" y22="-81.5486" style="line-style:normal;line-weight:thin;filling:none;color:black" antialias="false" x10="91.3448" x11="91.246" x12="91.1388" x13="91.0089" x14="90.8692" x15="90.7197" x16="90.5602" x17="90.3909" x18="90.2131" x19="90.0268" y1="-79.5109" y2="-79.6238" y3="-79.7353" y4="-79.8468" y5="-79.9569" y6="-80.0655" y7="-80.1742" y8="-80.28" y9="-80.3844" y10="-80.4874" y11="-80.589" y12="-80.6878" y13="-80.7936" y14="-80.8952"/>
                                        <polygon y1="-77.1699" y2="-77.16" y3="-77.16" y4="-77.1699" y5="-77.1868" y6="-77.2137" y7="-77.249" y8="-77.2927" y9="-77.345" y30="-79.185" y31="-79.2937" y32="-79.4024" y33="-79.511" x10="89.1576" x11="89.3678" x12="89.5724" x13="89.77" x14="89.9605" x15="90.1425" x16="90.3175" x17="90.484" style="line-style:normal;line-weight:thin;filling:none;color:black" x18="90.6435" x19="90.7916" x20="90.9328" x21="91.0626" x22="91.1741" x23="91.2757" x24="91.3674" x25="91.4506" x26="91.5254" x27="91.5889" x28="91.644" x29="91.6891" y10="-77.4056" y11="-77.4607" y12="-77.5213" y13="-77.5877" y14="-77.6582" y15="-77.733" y16="-77.812" y17="-77.8967" y18="-77.9842" y19="-78.0773" closed="false" x30="91.723" x31="91.7484" x32="91.7639" x33="91.7695" x1="86.6246" x2="86.9153" x3="87.2046" x4="87.4939" x5="87.7817" x6="88.0654" x7="88.3462" x8="88.6228" x9="88.8923" y20="-78.1733" y21="-78.2721" y22="-78.3666" y23="-78.4626" y24="-78.5613" y25="-78.6615" antialias="false" y26="-78.7645" y27="-78.8675" y28="-78.972" y29="-79.0778"/>
                                        <polygon x6="70.0483" x7="70.0906" x8="70.1414" closed="false" x9="70.1993" y10="-83.1079" y11="-83.146" x10="70.2628" x11="70.3319" y1="-82.6817" y2="-82.7339" y3="-82.7847" y4="-82.8355" y5="-82.8849" y6="-82.9329" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="69.9481" y7="-82.9795" x2="69.9524" antialias="false" y8="-83.0246" y9="-83.0684" x3="69.9636" x4="69.9848" x5="70.0116"/>
                                        <polygon x6="70.0483" x7="70.0116" x8="69.9848" closed="false" x9="69.9637" y10="-82.6309" y11="-82.6817" x10="69.9524" x11="69.9481" y1="-82.2175" y2="-82.2556" y3="-82.2965" y4="-82.3388" y5="-82.3839" y6="-82.4305" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="70.332" y7="-82.4785" x2="70.2628" antialias="false" y8="-82.5293" y9="-82.5787" x3="70.1993" x4="70.1415" x5="70.0907"/>
                                        <polygon x6="72.5488" x7="72.3978" x8="72.2454" closed="false" x9="72.0916" y10="-81.5246" y11="-81.5444" x10="71.9406" y12="-81.5684" x11="71.8235" y13="-81.5994" x12="71.7106" y14="-81.6361" x13="71.6048" y15="-81.677" x14="71.5046" x15="71.4129" y1="-81.677" y2="-81.6361" y3="-81.5994" y4="-81.5684" y5="-81.5444" y6="-81.5246" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="73.0766" y7="-81.5105" x2="72.9848" antialias="false" y8="-81.5049" x3="72.8861" y9="-81.5105" x4="72.7788" x5="72.6673"/>
                                        <polygon x6="66.2736" x7="66.227" x8="66.1734" closed="false" x9="66.1113" y10="-72.5217" y11="-72.4483" x10="66.0422" x11="65.966" y1="-73.4403" y2="-73.3204" y3="-73.2033" y4="-73.0904" y5="-72.9817" y6="-72.8787" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="66.3808" y7="-72.7799" x2="66.3766" antialias="false" y8="-72.6868" y9="-72.6007" x3="66.3639" x4="66.3427" x5="66.3117"/>
                                        <polygon x6="72.2567" x7="72.3837" x8="72.5107" closed="false" x9="72.6377" y10="-83.9319" y11="-83.9037" x10="72.7591" y12="-83.867" x11="72.8734" y13="-83.8247" x12="72.9806" x13="73.0766" y1="-83.8247" y2="-83.867" y3="-83.9037" y4="-83.9319" y5="-83.9517" y6="-83.9644" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="71.6909" y7="-83.9686" x2="71.7868" antialias="false" y8="-83.9644" x3="71.8941" y9="-83.9517" x4="72.0084" x5="72.1297"/>
                                        <polygon y15="-86.7739" closed="false" y16="-86.8671" y17="-86.956" y18="-87.0406" x20="69.8013" y19="-87.1211" x21="69.5981" x22="69.3879" x1="71.7402" x2="71.7346" x3="71.7176" x4="71.6908" x5="71.6541" x6="71.6062" x7="71.5497" x8="71.4806" x9="71.403" y20="-87.1959" y21="-87.2664" y22="-87.3299" style="line-style:normal;line-weight:thin;filling:none;color:black" antialias="false" x10="71.3155" x11="71.2167" x12="71.1094" x13="70.9796" x14="70.8399" x15="70.6903" x16="70.5309" x17="70.3616" x18="70.1838" x19="69.9961" y1="-85.2937" y2="-85.4066" y3="-85.518" y4="-85.6295" y5="-85.7396" y6="-85.8482" y7="-85.9555" y8="-86.0627" y9="-86.1672" y10="-86.2702" y11="-86.3704" y12="-86.4691" y13="-86.575" y14="-86.6766"/>
                                        <polygon y1="-82.9512" y2="-82.9428" y3="-82.9428" y4="-82.9512" y5="-82.9696" y6="-82.995" y7="-83.0303" y8="-83.074" y9="-83.1263" y30="-84.9678" y31="-85.075" y32="-85.1837" y33="-85.2937" x10="69.1283" x11="69.3385" x12="69.5431" x13="69.7407" x14="69.9312" x15="70.1132" x16="70.2882" x17="70.4547" style="line-style:normal;line-weight:thin;filling:none;color:black" x18="70.6142" x19="70.7623" x20="70.9035" x21="71.0333" x22="71.1448" x23="71.2464" x24="71.3381" x25="71.4213" x26="71.4961" x27="71.5596" x28="71.6147" x29="71.6584" y10="-83.187" y11="-83.2434" y12="-83.3041" y13="-83.369" y14="-83.4395" y15="-83.5157" y16="-83.5948" y17="-83.678" y18="-83.7669" y19="-83.8586" closed="false" x30="71.6937" x31="71.7191" x32="71.7346" x33="71.7403" x1="66.5953" x2="66.886" x3="67.1753" x4="67.4646" x5="67.7524" x6="68.0361" x7="68.3169" x8="68.5935" x9="68.863" y20="-83.9546" y21="-84.0548" y22="-84.1493" y23="-84.2453" y24="-84.3441" y25="-84.4443" antialias="false" y26="-84.5459" y27="-84.6489" y28="-84.7547" y29="-84.8605"/>
                                        <polygon y1="-79.5603" y2="-79.6732" y3="-79.7847" y4="-79.8962" y5="-80.0062" y6="-80.1149" y7="-80.2236" y8="-80.3294" y9="-80.4338" y30="-81.9127" y31="-81.9071" y32="-81.8929" y33="-81.8675" y34="-81.8322" y35="-81.7885" y36="-81.7334" y37="-81.6699" y38="-81.598" x10="82.6157" x11="82.7131" x12="82.8217" x13="82.9501" x14="83.0898" x15="83.2408" x16="83.4003" x17="83.5696" style="line-style:normal;line-weight:thin;filling:none;color:black" x18="83.7474" x19="83.9337" x20="84.1298" x21="84.333" x22="84.5433" x23="84.8156" x24="85.0964" x25="85.3843" x26="85.6778" x27="85.977" x28="86.2803" x29="86.5866" y10="-80.5368" y11="-80.6384" y12="-80.7372" y13="-80.8416" y14="-80.9432" y15="-81.0406" y16="-81.1351" y17="-81.224" y18="-81.3087" y19="-81.3877" closed="false" x30="86.8956" x31="87.2046" x32="87.5108" x33="87.8142" x1="82.1909" x34="88.1134" x2="82.1966" x35="88.4069" x3="82.2121" x36="88.6948" x4="82.2389" x37="88.9742" x5="82.277" x38="89.2479" x6="82.3236" x7="82.3814" x8="82.4492" x9="82.5282" y20="-81.4625" y21="-81.5331" y22="-81.598" y23="-81.6699" y24="-81.7334" y25="-81.7885" antialias="false" y26="-81.8322" y27="-81.8675" y28="-81.8929" y29="-81.9071"/>
                                        <polygon x6="60.0478" x7="59.9589" x8="59.877" closed="false" y1="-37.1564" y2="-37.148" y3="-37.1295" y4="-37.1025" y5="-37.066" y6="-37.0194" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="60.5671" y7="-36.9644" antialias="false" x2="60.4542" y8="-36.9009" x3="60.3455" x4="60.2411" x5="60.1409"/>
                                        <polygon x6="91.5438" x7="91.7314" x8="91.9107" closed="false" x9="92.0814" y10="-24.503" y11="-24.8389" x10="92.2409" y12="-25.1803" x11="92.3918" y13="-25.5303" x12="92.5344" x13="92.6656" y1="-21.8078" y2="-22.0773" y3="-22.3539" y4="-22.6375" y5="-22.9296" y6="-23.2302" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="90.4657" y7="-23.5378" x2="90.6999" antialias="false" y8="-23.8525" x3="90.9243" y9="-24.1742" x4="91.1388" x5="91.3462"/>
                                        <polygon y15="-22.0322" closed="false" y16="-22.4117" y17="-22.797" y18="-23.1879" y19="-23.5844" x1="85.4195" x2="85.6594" x3="85.8894" x4="86.111" x5="86.3241" x6="86.5259" x7="86.7192" x8="86.9012" x9="87.0748" style="line-style:normal;line-weight:thin;filling:none;color:black" antialias="false" x10="87.2371" x11="87.3909" x12="87.5334" x13="87.6646" x14="87.7874" x15="87.8975" x16="87.9976" x17="88.088" x18="88.167" x19="88.2347" y1="-17.4376" y2="-17.7142" y3="-17.9992" y4="-18.2941" y5="-18.5961" y6="-18.9065" y7="-19.224" y8="-19.55" y9="-19.8844" y10="-20.2259" y11="-20.5745" y12="-20.9286" y13="-21.2913" y14="-21.6582"/>
                                        <polygon closed="false" antialias="false" y1="-36.0078" y2="-36.0826" y3="-36.1475" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="60.5671" y4="-36.2025" x2="60.4415" y5="-36.2464" x3="60.3131" x4="60.1832" x5="60.052"/>
                                        <polygon closed="false" antialias="false" y1="-2.93936" y2="-2.93936" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="-13.3382" x2="-12.2361"/>
                                        <polygon y15="-1.22486" closed="false" y16="-0.735224" y17="-0.366924" y18="-0.122767" x20="-14" y19="0" x1="-14" x2="-12.3462" x3="-11.7944" x4="-11.4642" x5="-11.3542" x6="-11.3542" x7="-11.4642" x8="-11.6844" x9="-11.9059" y20="0" style="line-style:normal;line-weight:thin;filling:none;color:black" antialias="false" x10="-12.2361" x11="-11.7944" x12="-11.5743" x13="-11.4642" x14="-11.3542" x15="-11.3542" x16="-11.4642" x17="-11.6844" x18="-12.016" x19="-12.3462" y1="-4.8994" y2="-4.8994" y3="-4.77663" y4="-4.53252" y5="-4.16422" y6="-3.7973" y7="-3.429" y8="-3.1849" y9="-3.06213" y10="-2.93936" y11="-2.8166" y12="-2.57249" y13="-2.32696" y14="-1.83727"/>
                                        <polygon y15="-4.28699" closed="false" y16="-4.53252" y17="-4.77663" y18="-4.8994" x20="-8.26665" y19="-4.8994" x21="-7.93645" x22="-7.71632" x23="-7.49477" x24="-7.38471" x25="-7.38471" x1="-7.38471" x2="-7.49477" x3="-7.71632" x4="-7.93645" x5="-8.26665" x6="-8.59827" x7="-8.8184" x8="-9.1486" x9="-9.48021" y20="-4.77663" y21="-4.53252" y22="-4.28699" y23="-3.7973" y24="-3.06213" style="line-style:normal;line-weight:thin;filling:none;color:black" antialias="false" y25="-1.83727" x10="-9.70034" x11="-9.92047" x12="-10.0305" x13="-10.0305" x14="-9.92047" x15="-9.70034" x16="-9.48021" x17="-9.1486" x18="-8.8184" x19="-8.59827" y1="-1.83727" y2="-1.1021" y3="-0.612458" y4="-0.366924" y5="-0.122767" y6="-1.137e-13" y7="-1.137e-13" y8="-0.122767" y9="-0.366924" y10="-0.612458" y11="-1.1021" y12="-1.83727" y13="-3.06213" y14="-3.7973"/>
                                        <polygon closed="false" antialias="false" y1="-2.93936" y2="-2.93936" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="-5.40069" x2="-4.29861"/>
                                        <polygon y15="-1.22486" closed="false" y16="-0.735224" y17="-0.366924" y18="-0.122767" x20="-6.0625" y19="0" x1="-6.0625" x2="-4.40867" x3="-3.85693" x4="-3.52673" x5="-3.41667" x6="-3.41667" x7="-3.52673" x8="-3.74687" x9="-3.967" y20="0" style="line-style:normal;line-weight:thin;filling:none;color:black" antialias="false" x10="-4.29861" x11="-3.85693" x12="-3.6368" x13="-3.52673" x14="-3.41667" x15="-3.41667" x16="-3.52673" x17="-3.74687" x18="-4.07707" x19="-4.40867" y1="-4.8994" y2="-4.8994" y3="-4.77663" y4="-4.53252" y5="-4.16422" y6="-3.7973" y7="-3.429" y8="-3.1849" y9="-3.06213" y10="-2.93936" y11="-2.8166" y12="-2.57249" y13="-2.32696" y14="-1.83727"/>
                                        <polygon y15="-8.53e-14" closed="false" y16="-8.53e-14" y17="-0.122767" y18="-0.366924" x20="-2.09304" y19="-0.735224" x21="-2.09304" x22="-1.98297" x23="-1.76284" x24="-1.32117" x25="-0.109021" x1="-2.09304" x2="-1.98297" x3="-1.76284" x4="-1.43123" x5="-1.10103" x6="-0.439221" x7="-0.109021" x8="0.222592" x9="0.442725" y20="-1.22486" y21="-1.7145" y22="-2.69526" y23="-3.1849" y24="-3.7973" style="line-style:normal;line-weight:thin;filling:none;color:black" antialias="false" y25="-4.8994" x10="0.552792" x11="0.552792" x12="0.442725" x13="0.222592" x14="-0.109021" x15="-0.439221" x16="-1.10103" x17="-1.43123" x18="-1.76284" x19="-1.98297" y1="-1.7145" y2="-2.20419" y3="-2.57249" y4="-2.8166" y5="-2.93936" y6="-2.93936" y7="-2.8166" y8="-2.57249" y9="-2.20419" y10="-1.7145" y11="-1.22486" y12="-0.735224" y13="-0.366924" y14="-0.122767"/>
                                        <polygon x6="4.41218" x7="4.52225" x8="4.52225" closed="false" x9="4.41218" y10="-0.366924" y11="-0.122767" x10="4.19063" y12="-5.68e-14" x11="3.86043" y13="-5.68e-14" x12="3.53023" x13="1.87641" y1="-4.8994" y2="-4.8994" y3="-2.93936" y4="-2.93936" y5="-2.8166" y6="-2.44972" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="4.3007" y7="-1.96003" x2="1.87641" antialias="false" y8="-1.22486" x3="1.87641" y9="-0.735224" x4="3.53023" x5="4.08057"/>
                                        <polygon closed="false" antialias="false" y1="-4.40976" y2="-4.8994" y3="-4.8994" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="5.84446" y4="-1.421e-13" x2="5.84446" x3="8.49029" x4="6.28613"/>
                                        <polygon y15="-8.53e-14" closed="false" y16="-8.53e-14" y17="-0.122767" y18="-0.366924" x20="9.81391" y19="-0.735224" x21="9.81391" x22="9.92398" x23="10.1441" x24="10.5858" x25="11.7979" x1="9.81391" x2="9.92398" x3="10.1441" x4="10.4757" x5="10.8059" x6="11.4677" x7="11.7979" x8="12.1295" x9="12.3497" y20="-1.22486" y21="-1.7145" y22="-2.69526" y23="-3.1849" y24="-3.7973" style="line-style:normal;line-weight:thin;filling:none;color:black" antialias="false" y25="-4.8994" x10="12.4597" x11="12.4597" x12="12.3497" x13="12.1295" x14="11.7979" x15="11.4677" x16="10.8059" x17="10.4757" x18="10.1441" x19="9.92398" y1="-1.7145" y2="-2.20419" y3="-2.57249" y4="-2.8166" y5="-2.93936" y6="-2.93936" y7="-2.8166" y8="-2.57249" y9="-2.20419" y10="-1.7145" y11="-1.22486" y12="-0.735224" y13="-0.366924" y14="-0.122767"/>
                                        <polygon y15="-12.0054" closed="false" y16="-11.5638" y17="-11.2702" y18="-10.83" x20="-11.9331" y19="-10.3883" x21="-12.5949" x22="-13.3879" x23="-14.0497" x24="-14.5789" x25="-14.8442" x1="-11.2712" x2="-11.6692" x3="-12.0657" x4="-12.7275" x5="-13.2567" x6="-13.7858" x7="-14.1824" x8="-14.5789" x9="-14.7115" y20="-10.0948" y21="-9.94802" y22="-9.94802" y23="-10.0948" y24="-10.3883" style="line-style:normal;line-weight:thin;filling:none;color:black" antialias="false" y25="-10.6818" x10="-14.7115" x11="-14.5789" x12="-14.1824" x13="-11.9331" x14="-11.5365" x15="-11.2712" x16="-11.14" x17="-11.14" x18="-11.2712" x19="-11.5365" y1="-15.2397" y2="-15.5332" y3="-15.6799" y4="-15.8267" y5="-15.8267" y6="-15.6799" y7="-15.5332" y8="-15.2397" y9="-14.798" y10="-14.5045" y11="-14.0628" y12="-13.7693" y13="-12.7406" y14="-12.4457"/>
                                        <polygon closed="false" antialias="false" y1="-15.8267" y2="-15.8267" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="-7.69972" x2="-5.84693"/>
                                        <polygon closed="false" antialias="false" y1="-15.8267" y2="-15.8267" y3="-9.94802" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="-9.5511" x2="-7.69972" x3="-7.69972"/>
                                        <polygon x6="2.48709" x7="2.88502" x8="3.1489" closed="false" x9="3.1489" y10="-13.7693" y11="-9.94802" x10="2.88502" y12="-9.94802" x11="-0.0261007" x12="3.1489" y1="-14.9448" y2="-15.3864" y3="-15.6799" y4="-15.8267" y5="-15.8267" y6="-15.6799" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="-0.0261007" y7="-15.3864" x2="0.237779" antialias="false" y8="-14.9448" x3="0.635712" y9="-14.3578" x4="1.16488" x5="1.95792"/>
                                        <polygon x6="4.86905" closed="false" antialias="false" y1="-10.3883" y2="-10.3883" y3="-10.535" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="5.13292" y4="-10.535" x2="5.00169" y5="-9.65311" x3="5.00169" y6="-9.35958" x4="5.13292" x5="5.13292"/>
                                        <polygon x6="9.63154" x7="9.76419" x8="9.76419" closed="false" x9="9.63154" y10="-10.3883" y11="-10.0948" x10="9.36767" y12="-9.94802" x11="8.96973" y13="-9.94802" x12="8.57321" x13="6.58919" y1="-15.8267" y2="-15.8267" y3="-13.4758" y4="-13.4758" y5="-13.329" y6="-12.8874" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="9.4989" y7="-12.2989" x2="6.58919" antialias="false" y8="-11.417" x3="6.58919" y9="-10.83" x4="8.57321" x5="9.23502"/>
                                        <polygon closed="false" antialias="false" y1="-12.0054" y2="-12.0054" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="11.3517" x2="13.9975"/>
                                        <polygon closed="false" antialias="false" y1="-11.1235" y2="-9.94802" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="18.2309" x2="19.2892"/>
                                        <polygon y15="-15.8267" closed="false" y16="-15.6799" y17="-15.3864" y18="-15.0929" x20="19.2892" y19="-14.6512" x21="19.2892" x22="19.158" x23="18.8927" x24="18.6274" x25="18.2309" x1="18.2309" x2="17.8343" x3="17.0399" x4="16.6434" x5="16.2468" x6="15.9815" x7="15.7177" x8="15.585" x9="15.585" y20="-14.0628" y21="-11.7119" y22="-11.1235" y23="-10.6818" y24="-10.3883" style="line-style:normal;line-weight:thin;filling:none;color:black" antialias="false" y25="-10.0948" x10="15.7177" x11="15.9815" x12="16.2468" x13="16.6434" x14="17.0399" x15="17.8343" x16="18.2309" x17="18.6274" x18="18.8927" x19="19.158" y1="-10.0948" y2="-9.94802" y3="-9.94802" y4="-10.0948" y5="-10.3883" y6="-10.6818" y7="-11.1235" y8="-11.7119" y9="-14.0628" y10="-14.6512" y11="-15.0929" y12="-15.3864" y13="-15.6799" y14="-15.8267"/>
                                        <polygon x6="23.5225" x7="23.126" x8="22.333" closed="false" x9="21.935" y10="-10.3883" y11="-10.6818" x10="21.5385" y12="-11.1235" x11="21.2746" y13="-11.7119" x12="21.0093" y14="-15.8267" x13="20.8767" x14="20.8767" y1="-15.8267" y2="-11.7119" y3="-11.1235" y4="-10.6818" y5="-10.3883" y6="-10.0948" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="24.5823" y7="-9.94802" x2="24.5823" antialias="false" y8="-9.94802" x3="24.4496" y9="-10.0948" x4="24.1843" x5="23.9205"/>
                                        <polygon closed="false" antialias="false" y1="-11.7119" y2="-11.7119" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="26.8302" x2="29.7413"/>
                                        <polygon closed="false" antialias="false" y1="-9.94802" y2="-15.8267" y3="-9.94802" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="26.1698" x2="28.2864" x3="30.4031"/>
                                        <polygon closed="false" antialias="false" y1="-15.8267" y2="-15.8267" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="33.842" x2="35.6948"/>
                                        <polygon closed="false" antialias="false" y1="-15.8267" y2="-15.8267" y3="-9.94802" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="31.9906" x2="33.842" x3="33.842"/>
                                        <polygon closed="false" antialias="false" y1="-15.8267" y2="-15.8267" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="39.1351" x2="40.9864"/>
                                        <polygon closed="false" antialias="false" y1="-15.8267" y2="-15.8267" y3="-9.94802" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="37.2823" x2="39.1351" x3="39.1351"/>
                                        <polygon x6="46.0142" x7="46.1469" x8="46.2781" closed="false" x9="46.2781" y10="-13.6225" y11="-13.3291" x10="46.1469" y12="-13.0341" x11="46.0142" y13="-12.8874" x12="45.6177" y14="-12.8874" x13="45.0885" y15="-9.94802" x14="44.6906" x15="46.2781" y1="-12.8874" y2="-12.8874" y3="-15.8267" y4="-15.8267" y5="-15.6799" y6="-15.3864" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="44.6906" y7="-15.0929" x2="42.5739" antialias="false" y8="-14.6512" x3="42.5739" y9="-14.0628" x4="45.0885" x5="45.6177"/>
                                        <polygon closed="false" antialias="false" y1="-9.94802" y2="-12.8874" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="42.5739" x2="42.5739"/>
                                        <polygon y15="-9.94802" closed="false" y16="-10.0948" y17="-10.3883" y18="-10.6818" x20="51.5712" y19="-11.1235" x21="51.5712" x22="51.4385" x23="51.1732" x24="50.9094" x25="50.5128" x1="50.5128" x2="50.1149" x3="49.3219" x4="48.9253" x5="48.5274" x6="48.2635" x7="47.9982" x8="47.867" x9="47.867" y20="-11.7119" y21="-14.0628" y22="-14.6512" y23="-15.0929" y24="-15.3864" style="line-style:normal;line-weight:thin;filling:none;color:black" antialias="false" y25="-15.6799" x10="47.9982" x11="48.2635" x12="48.5274" x13="48.9253" x14="49.3219" x15="50.1149" x16="50.5128" x17="50.9094" x18="51.1732" x19="51.4385" y1="-15.6799" y2="-15.8267" y3="-15.8267" y4="-15.6799" y5="-15.3864" y6="-15.0929" y7="-14.6512" y8="-14.0628" y9="-11.7119" y10="-11.1235" y11="-10.6818" y12="-10.3883" y13="-10.0948" y14="-9.94802"/>
                                        <polygon closed="false" antialias="false" y1="-12.0054" y2="-12.0054" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="53.1587" x2="55.8045"/>
                                        <polygon closed="false" antialias="false" y1="-9.94802" y2="-15.8267" y3="-12.5938" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="57.392" y4="-15.8267" x2="57.392" y5="-9.94802" x3="59.2434" x4="61.0962" x5="61.0962"/>
                                        <polygon closed="false" antialias="false" y1="-15.8267" y2="-15.8267" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="64.5365" x2="66.3878"/>
                                        <polygon closed="false" antialias="false" y1="-15.8267" y2="-15.8267" y3="-9.94802" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="62.6837" x2="64.5365" x3="64.5365"/>
                                        <circle x="256" y="-20" antialias="false" style="line-style:normal;line-weight:normal;filling:black;color:black" diameter="4"/>
                                        <circle x="214" y="-22" antialias="false" style="line-style:normal;line-weight:normal;filling:none;color:black" diameter="8"/>
                                        <line end1="none" end2="none" antialias="false" y1="-38" y2="-29" style="line-style:normal;line-weight:normal;filling:none;color:black" x1="293" length1="1.5" x2="280" length2="1.5"/>
                                        <line end1="none" end2="none" antialias="false" y1="-18" y2="-18" style="line-style:normal;line-weight:normal;filling:none;color:black" x1="222" length1="1.5" x2="234" length2="1.5"/>
                                        <line end1="none" end2="none" antialias="false" y1="-18" y2="-18" style="line-style:normal;line-weight:normal;filling:none;color:black" x1="242" length1="1.5" x2="278" length2="1.5"/>
                                        <line end1="none" end2="none" antialias="false" y1="-18" y2="-26" style="line-style:normal;line-weight:normal;filling:none;color:black" x1="278" length1="1.5" x2="278" length2="1.5"/>
                                        <line end1="none" end2="none" antialias="false" y1="-26" y2="-18" style="line-style:normal;line-weight:normal;filling:none;color:black" x1="298" length1="1.5" x2="298" length2="1.5"/>
                                        <line end1="none" end2="none" antialias="false" y1="-18" y2="-18" style="line-style:normal;line-weight:normal;filling:none;color:black" x1="298" length1="1.5" x2="308" length2="1.5"/>
                                        <line end1="none" end2="none" antialias="false" y1="-18" y2="-18" style="line-style:normal;line-weight:normal;filling:none;color:black" x1="316" length1="1.5" x2="328" length2="1.5"/>
                                    </description>
                                </definition>
                            </element>
                            <element name="klemme_phoenix_stme_6_v.elmt">
                                <definition type="element" link_type="simple" hotspot_x="7" hotspot_y="107" width="390" height="120" version="0.100.0">
                                    <uuid uuid="{07ce5b45-e2a8-497f-9023-73d0b066eff3}"/>
                                    <names>
                                        <name lang="de">
STME 6 HV - Messwandler-Trennklemme
3035693
</name>
                                        <name lang="en">
STME 6 HV - Messwandler-Trennklemme
3035693
</name>
                                    </names>
                                    <elementInformations>
                                        <elementInformation name="manufacturer_reference" show="1"/>
                                        <elementInformation name="quantity" show="1"/>
                                        <elementInformation name="machine_manufacturer_reference" show="1"/>
                                        <elementInformation name="manufacturer" show="1"/>
                                        <elementInformation name="label" show="1"/>
                                        <elementInformation name="supplier" show="1"/>
                                        <elementInformation name="comment" show="1"/>
                                        <elementInformation name="plant" show="1"/>
                                        <elementInformation name="description" show="1"/>
                                        <elementInformation name="designation" show="1"/>
                                        <elementInformation name="unity" show="1"/>
                                    </elementInformations>
                                    <informations>Created using dxf2elmt!</informations>
                                    <description>
                                        <circle x="367" y="-20" antialias="false" style="line-style:normal;line-weight:normal;filling:none;color:black" diameter="8"/>
                                        <circle x="271" y="-18" antialias="false" style="line-style:normal;line-weight:normal;filling:black;color:black" diameter="4"/>
                                        <polygon closed="false" antialias="false" y1="-18.8911" y2="-20.5463" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="100.584" x2="102.495"/>
                                        <circle x="301" y="-28" antialias="false" style="line-style:normal;line-weight:normal;filling:none;color:black" diameter="4"/>
                                        <circle x="350" y="-18" antialias="false" style="line-style:normal;line-weight:normal;filling:black;color:black" diameter="4"/>
                                        <circle x="321" y="-28" antialias="false" style="line-style:normal;line-weight:normal;filling:none;color:black" diameter="4"/>
                                        <circle x="291" y="-18" antialias="false" style="line-style:normal;line-weight:normal;filling:black;color:black" diameter="4"/>
                                        <polygon closed="false" antialias="false" y1="-20.3107" y2="-17.9471" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="103.313" x2="100.584"/>
                                        <circle x="330" y="-18" antialias="false" style="line-style:normal;line-weight:normal;filling:black;color:black" diameter="4"/>
                                        <polygon closed="false" antialias="false" y1="-21.0303" y2="-22.6672" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="99.0559" x2="100.948"/>
                                        <circle x="340" y="-18" antialias="false" style="line-style:normal;line-weight:normal;filling:black;color:black" diameter="4"/>
                                        <line end1="none" end2="none" antialias="false" y1="-16" y2="-16" style="line-style:normal;line-weight:normal;filling:none;color:black" length1="1.5" x1="323" x2="354" length2="1.5"/>
                                        <polygon closed="false" antialias="false" y1="-18.8911" y2="-19.1987" style="line-style:normal;line-weight:thin;filling:none;color:black" y3="-20.9541" x1="100.584" x2="99.0559" x3="101.084"/>
                                        <polygon closed="false" antialias="false" y1="-21.0303" y2="-19.1987" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="99.0559" x2="99.0559"/>
                                        <polygon closed="false" antialias="false" y1="-18.8911" y2="-17.9471" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="100.584" x2="100.584"/>
                                        <polygon closed="false" antialias="false" y1="-87.6475" y2="-90.4993" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="99.1363" x2="99.8362"/>
                                        <polygon closed="false" antialias="false" y1="-87.6475" y2="-74.8247" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="99.1363" x2="101.288"/>
                                        <polygon closed="false" antialias="false" y1="-17.9231" y2="-11.0058" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="105.671" x2="97.6843"/>
                                        <polygon closed="false" antialias="false" y1="-31.2764" y2="-38.6975" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="220.939" x2="220.939"/>
                                        <polygon closed="false" antialias="false" y1="-80.3803" y2="-81.241" style="line-style:normal;line-weight:thin;filling:none;color:black" y3="-74.3252" x1="162.303" x2="160.452" x3="152.465"/>
                                        <polygon closed="false" antialias="false" y1="-81.5021" y2="-81.011" style="line-style:normal;line-weight:thin;filling:none;color:black" y3="-77.7556" x1="163.599" x2="164.654" x3="165.354"/>
                                        <polygon closed="false" antialias="false" y1="-71.4465" y2="-71.8769" style="line-style:normal;line-weight:thin;filling:none;color:black" y3="-74.3252" x1="150.851" x2="149.926" x3="152.465"/>
                                        <polygon closed="false" antialias="false" y1="-71.4465" y2="-69.749" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="150.851" x2="150.536"/>
                                        <polygon closed="false" antialias="false" y1="-74.3252" y2="-72.9987" style="line-style:normal;line-weight:thin;filling:none;color:black" y3="-74.5848" y4="-74.0938" x1="152.465" x2="155.317" y5="-70.8383" x3="155.612" x4="156.667" x5="157.367"/>
                                        <polygon closed="false" antialias="false" y1="-59.7456" y2="-59.2573" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="155.778" x2="155.215"/>
                                        <text x="249" y="9" font="Arial,10,-1,5,50,0,0,0,0,0,Standard" rotation="0" color="#000000" text="a"/>
                                        <polygon closed="false" antialias="false" y1="-60.8505" y2="-49.2681" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="178.847" x2="176.695"/>
                                        <text x="368" y="9" font="Arial,10,-1,5,50,1,0,0,0,0,Italic" rotation="0" color="#000000" text="b"/>
                                        <polygon closed="false" antialias="false" y1="-59.2573" y2="-70.8383" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="155.215" x2="157.367"/>
                                        <polygon closed="false" antialias="false" y1="-52.2046" y2="-49.9595" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="171.993" x2="176.824"/>
                                        <polygon closed="false" antialias="false" y1="-57.2959" y2="-59.7456" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="161.045" x2="155.778"/>
                                        <polygon closed="false" antialias="false" y1="-55.9751" y2="-53.5268" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="163.887" x2="169.151"/>
                                        <polygon closed="false" antialias="false" y1="-53.5635" y2="-61.9159" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="169.194" x2="170.746"/>
                                        <polygon closed="false" antialias="false" y1="-57.6205" y2="-52.2046" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="178.247" x2="171.993"/>
                                        <polygon closed="false" antialias="false" y1="-69.749" y2="-74.6653" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="150.536" x2="139.963"/>
                                        <polygon closed="false" antialias="false" y1="-53.5268" y2="-59.4676" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="169.151" x2="176.011"/>
                                        <polygon closed="false" antialias="false" y1="-74.0938" y2="-81.011" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="156.667" x2="164.654"/>
                                        <polygon closed="false" antialias="false" y1="-81.5021" y2="-74.5848" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="163.599" x2="155.612"/>
                                        <polygon closed="false" antialias="false" y1="-59.2573" y2="-49.2681" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="155.215" x2="176.695"/>
                                        <polygon closed="false" antialias="false" y1="-67.8454" y2="-64.6972" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="189.32" x2="196.091"/>
                                        <polygon closed="false" antialias="false" y1="-55.1919" y2="-43.292" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="197.319" x2="195.107"/>
                                        <polygon closed="false" antialias="false" y1="-59.8599" y2="-64.6972" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="190.504" x2="196.091"/>
                                        <polygon closed="false" antialias="false" y1="-60.4427" y2="-58.4615" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="192.335" x2="191.968"/>
                                        <polygon closed="false" antialias="false" y1="-55.1919" y2="-55.453" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="197.319" x2="197.621"/>
                                        <polygon closed="false" antialias="false" y1="-40.9284" y2="-39.8405" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="196.485" x2="198.824"/>
                                        <polygon closed="false" antialias="false" y1="-59.7216" y2="-60.1435" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="207.86" x2="207.212"/>
                                        <polygon closed="false" antialias="false" y1="-61.8637" y2="-61.2357" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="205.832" x2="205.106"/>
                                        <polygon closed="false" antialias="false" y1="-59.7216" y2="-51.3495" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="207.86" x2="206.305"/>
                                        <polygon closed="false" antialias="false" y1="-51.4003" y2="-60.1435" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="205.588" x2="207.212"/>
                                        <polygon closed="false" antialias="false" y1="-51.6853" y2="-45.087" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="202.842" x2="212.952"/>
                                        <polygon closed="false" antialias="false" y1="-27.3662" y2="-27.1503" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="100.944" x2="100.694"/>
                                        <polygon closed="false" antialias="false" y1="-24.3592" y2="-31.7802" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="212.952" x2="212.952"/>
                                        <polygon closed="false" antialias="false" y1="-51.6853" y2="-51.9478" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="202.842" x2="203.144"/>
                                        <polygon closed="false" antialias="false" y1="-45.9111" y2="-44.5606" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="199.25" x2="199.08"/>
                                        <polygon closed="false" antialias="false" y1="-43.9792" y2="-43.2441" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="199.363" x2="200.015"/>
                                        <polygon closed="false" antialias="false" y1="-43.9792" y2="-43.1029" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="199.363" x2="201.247"/>
                                        <polygon closed="false" antialias="false" y1="-43.9792" y2="-44.5606" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="199.363" x2="199.08"/>
                                        <polygon closed="false" antialias="false" y1="-40.649" y2="-51.6853" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="200.791" x2="202.842"/>
                                        <polygon closed="false" antialias="false" y1="-43.2441" y2="-39.9943" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="200.015" x2="199.411"/>
                                        <polygon closed="false" antialias="false" y1="-40.1015" y2="-41.1909" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="199.126" x2="196.787"/>
                                        <polygon closed="false" antialias="false" y1="-39.8405" y2="-40.1015" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="198.824" x2="199.126"/>
                                        <polygon closed="false" antialias="false" y1="-40.9312" y2="-43.2441" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="197.344" x2="200.015"/>
                                        <polygon closed="false" antialias="false" y1="-43.5545" y2="-43.292" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="195.409" x2="195.107"/>
                                        <polygon closed="false" antialias="false" y1="-41.1909" y2="-40.9284" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="196.787" x2="196.485"/>
                                        <polygon closed="false" antialias="false" y1="-41.8456" y2="-44.5606" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="195.944" x2="199.08"/>
                                        <polygon closed="false" antialias="false" y1="-43.5545" y2="-55.453" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="195.409" x2="197.621"/>
                                        <polygon closed="false" antialias="false" y1="-82.7735" y2="-75.8562" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="149.356" x2="141.369"/>
                                        <polygon closed="false" antialias="false" y1="-82.7735" y2="-86.9321" style="line-style:normal;line-weight:thin;filling:none;color:black" y3="-80.0148" x1="149.356" x2="148.15" x3="140.163"/>
                                        <polygon closed="false" antialias="false" y1="-81.5727" y2="-77.6808" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="147.971" x2="156.34"/>
                                        <polygon closed="false" antialias="false" y1="-85.9471" y2="-82.2133" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="141.183" x2="136.871"/>
                                        <polygon closed="false" antialias="false" y1="-76.3628" y2="-75.8562" style="line-style:normal;line-weight:thin;filling:none;color:black" y3="-80.0148" x1="140.279" x2="141.369" x3="140.163"/>
                                        <polygon closed="false" antialias="false" y1="-75.8661" y2="-74.6653" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="141.348" x2="139.963"/>
                                        <polygon closed="false" antialias="false" y1="-75.3863" y2="-75.9042" style="line-style:normal;line-weight:thin;filling:none;color:black" y3="-79.3219" x1="101.194" x2="96.5864" x3="100.533"/>
                                        <polygon closed="false" antialias="false" y1="-82.226" y2="-82.7552" style="line-style:normal;line-weight:thin;filling:none;color:black" y3="-78.258" x1="100.046" x2="95.339" x3="96.0939"/>
                                        <polygon closed="false" antialias="false" y1="-76.2231" y2="-81.7505" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="93.7444" x2="100.127"/>
                                        <polygon closed="false" antialias="false" y1="-77.726" y2="-77.2377" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="80.3713" x2="79.8083"/>
                                        <polygon closed="false" antialias="false" y1="-77.726" y2="-77.1333" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="80.3713" x2="85.6376"/>
                                        <polygon closed="false" antialias="false" y1="-89.2759" y2="-88.2599" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="114.515" x2="118.04"/>
                                        <polygon closed="false" antialias="false" y1="-88.3784" y2="-87.529" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="107.764" x2="106.783"/>
                                        <polygon closed="false" antialias="false" y1="-88.6578" y2="-89.2759" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="113.801" x2="114.515"/>
                                        <polygon closed="false" antialias="false" y1="-83.0755" y2="-83.6667" style="line-style:normal;line-weight:thin;filling:none;color:black" y3="-84.155" y4="-82.789" x1="92.497" x2="87.2322" x3="87.7952" x4="99.9519"/>
                                        <polygon closed="false" antialias="false" y1="-76.2231" y2="-76.8144" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="93.7444" x2="88.4796"/>
                                        <polygon closed="false" antialias="false" y1="-79.1681" y2="-83.6667" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="87.9857" x2="87.2322"/>
                                        <polygon closed="false" antialias="false" y1="-74.6653" y2="-76.3628" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="139.963" x2="140.279"/>
                                        <polygon closed="false" antialias="false" y1="-84.9847" y2="-88.7185" style="line-style:normal;line-weight:thin;filling:none;color:black" y3="-83.829" x1="131.696" x2="136.009" x3="134.019"/>
                                        <polygon closed="false" antialias="false" y1="-77.2377" y2="-90.0619" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="79.8083" x2="77.6564"/>
                                        <polygon closed="false" antialias="false" y1="-77.1333" y2="-83.0755" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="85.6376" x2="92.497"/>
                                        <polygon closed="false" antialias="false" y1="-82.7552" y2="-76.8144" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="95.339" x2="88.4796"/>
                                        <polygon closed="false" antialias="false" y1="-81.5487" y2="-88.4659" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="136.868" x2="144.856"/>
                                        <polygon closed="false" antialias="false" y1="-70.8383" y2="-77.7556" style="line-style:normal;line-weight:thin;filling:none;color:black" y3="-66.1732" x1="157.367" x2="165.354" x3="163.202"/>
                                        <polygon closed="false" antialias="false" y1="-61.9159" y2="-55.9751" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="170.746" x2="163.887"/>
                                        <polygon closed="false" antialias="false" y1="-57.2959" y2="-63.2367" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="161.045" x2="167.904"/>
                                        <polygon closed="false" antialias="false" y1="-65.6864" y2="-57.334" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="162.639" x2="161.087"/>
                                        <polygon closed="false" antialias="false" y1="-61.9159" y2="-59.4676" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="170.746" x2="176.011"/>
                                        <polygon closed="false" antialias="false" y1="-66.1732" y2="-65.6864" style="line-style:normal;line-weight:thin;filling:none;color:black" y3="-63.2367" x1="163.202" x2="162.639" x3="167.904"/>
                                        <polygon closed="false" antialias="false" y1="-61.0015" y2="-67.8454" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="188.049" x2="189.32"/>
                                        <polygon closed="false" antialias="false" y1="-62.9883" y2="-60.8505" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="180.549" x2="178.847"/>
                                        <polygon closed="false" antialias="false" y1="-60.4794" y2="-59.9742" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="193.661" x2="194.748"/>
                                        <polygon closed="false" antialias="false" y1="-60.4794" y2="-57.897" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="193.661" x2="193.181"/>
                                        <polygon closed="false" antialias="false" y1="-59.5523" y2="-60.4427" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="191.306" x2="192.335"/>
                                        <polygon closed="false" antialias="false" y1="-58.5772" y2="-57.8928" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="191.721" x2="193.193"/>
                                        <polygon closed="false" antialias="false" y1="-59.0104" y2="-59.5523" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="191.206" x2="191.306"/>
                                        <polygon closed="false" antialias="false" y1="-59.4055" y2="-58.2696" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="195.226" x2="195.145"/>
                                        <polygon closed="false" antialias="false" y1="-58.2696" y2="-58.175" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="195.145" x2="195.129"/>
                                        <polygon closed="false" antialias="false" y1="-57.9253" y2="-59.4055" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="194.951" x2="195.226"/>
                                        <polygon closed="false" antialias="false" y1="-55.1919" y2="-62.9883" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="197.319" x2="180.549"/>
                                        <polygon closed="false" antialias="false" y1="-63.0081" y2="-59.8599" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="183.735" x2="190.504"/>
                                        <polygon closed="false" antialias="false" y1="-63.0081" y2="-67.8454" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="183.735" x2="189.32"/>
                                        <polygon closed="false" antialias="false" y1="-69.9056" y2="-61.8637" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="188.536" x2="205.832"/>
                                        <polygon closed="false" antialias="false" y1="-69.9056" y2="-62.9883" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="188.536" x2="180.549"/>
                                        <polygon closed="false" antialias="false" y1="-59.0541" y2="-66.1732" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="178.513" x2="163.202"/>
                                        <polygon closed="false" antialias="false" y1="-24.3592" y2="-31.2764" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="212.952" x2="220.939"/>
                                        <polygon closed="false" antialias="false" y1="-49.5475" y2="-52.0028" style="line-style:normal;line-weight:thin;filling:none;color:black" y3="-45.087" x1="220.939" x2="220.939" x3="212.952"/>
                                        <polygon closed="false" antialias="false" y1="-47.1966" y2="-39.5385" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="218.223" x2="218.223"/>
                                        <polygon closed="false" antialias="false" y1="-38.6975" y2="-31.7802" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="220.939" x2="212.952"/>
                                        <polygon closed="false" antialias="false" y1="-39.5385" y2="-39.1293" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="218.223" x2="219.64"/>
                                        <polygon closed="false" antialias="false" y1="-39.4764" y2="-38.6975" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="220.04" x2="220.939"/>
                                        <polygon closed="false" antialias="false" y1="-39.5385" y2="-32.6212" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="218.223" x2="210.236"/>
                                        <polygon closed="false" antialias="false" y1="-32.5591" y2="-39.4764" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="212.052" x2="220.04"/>
                                        <polygon closed="false" antialias="false" y1="-74.8247" y2="-77.2377" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="101.288" x2="79.8083"/>
                                        <polygon closed="false" antialias="false" y1="-80.6822" y2="-73.5463" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="43.5512" x2="43.5512"/>
                                        <polygon closed="false" antialias="false" y1="-45.087" y2="-42.6316" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="212.952" x2="212.952"/>
                                        <polygon closed="false" antialias="false" y1="-52.0028" y2="-61.8637" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="220.939" x2="205.832"/>
                                        <polygon closed="false" antialias="false" y1="-32.4886" y2="-31.3554" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="47.5052" x2="47.4135"/>
                                        <polygon closed="false" antialias="false" y1="-26.425" y2="-10.4964" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="41.8537" x2="97.0295"/>
                                        <polygon closed="false" antialias="false" y1="-80.9419" y2="-80.6822" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="44.4515" x2="43.5512"/>
                                        <polygon closed="false" antialias="false" y1="-80.4805" y2="-80.9419" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="44.4515" x2="44.4515"/>
                                        <polygon closed="false" antialias="false" y1="-80.5849" y2="-80.8473" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="57.6793" x2="57.9812"/>
                                        <polygon closed="false" antialias="false" y1="-80.3224" y2="-80.5849" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="60.0189" x2="60.3223"/>
                                        <polygon closed="false" antialias="false" y1="-79.6987" y2="-81.5487" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="136.635" x2="136.868"/>
                                        <polygon closed="false" antialias="false" y1="-80.3224" y2="-80.5849" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="60.0189" x2="57.6793"/>
                                        <polygon closed="false" antialias="false" y1="-79.9555" y2="-80.4805" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="46.2676" x2="44.4515"/>
                                        <polygon closed="false" antialias="false" y1="-80.8473" y2="-80.5849" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="57.9812" x2="60.3223"/>
                                        <polygon closed="false" antialias="false" y1="-42.6316" y2="-49.5475" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="212.952" x2="220.939"/>
                                        <polygon closed="false" antialias="false" y1="-35.1781" y2="-26.425" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="41.8537" x2="41.8537"/>
                                        <polygon closed="false" antialias="false" y1="-35.3235" y2="-40.4416" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="43.0122" x2="48.9233"/>
                                        <polygon closed="false" antialias="false" y1="-35.3235" y2="-33.4566" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="43.0122" x2="44.4614"/>
                                        <polygon closed="false" antialias="false" y1="-31.2553" y2="-29.679" style="line-style:normal;line-weight:thin;filling:none;color:black" y3="-32.3587" x1="44.3993" x2="44.3993" x3="47.4953"/>
                                        <polygon closed="false" antialias="false" y1="-34.0761" y2="-31.3554" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="47.6787" x2="44.5362"/>
                                        <polygon closed="false" antialias="false" y1="-29.679" y2="-28.8423" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="44.3993" x2="47.2992"/>
                                        <polygon closed="false" antialias="false" y1="-47.7469" y2="-51.4807" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="43.5512" x2="43.5512"/>
                                        <polygon closed="false" antialias="false" y1="-80.9419" y2="-82.5153" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="44.4515" x2="46.2676"/>
                                        <polygon closed="false" antialias="false" y1="-83.0346" y2="-80.6822" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="46.2676" x2="43.5512"/>
                                        <polygon closed="false" antialias="false" y1="-80.4805" y2="-82.0524" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="44.4515" x2="46.2676"/>
                                        <polygon closed="false" antialias="false" y1="-79.9555" y2="-90.6913" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="46.2676" x2="46.2676"/>
                                        <polygon closed="false" antialias="false" y1="-47.7469" y2="-45.6796" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="43.5512" x2="50.7098"/>
                                        <polygon closed="false" antialias="false" y1="-36.5709" y2="-33.4566" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="48.0569" x2="44.4614"/>
                                        <polygon closed="false" antialias="false" y1="-35.5747" y2="-41.9261" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="42.0202" x2="49.3523"/>
                                        <polygon closed="false" antialias="false" y1="4.94116" y2="-1.9747" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="212.124" x2="220.111"/>
                                        <polygon closed="false" antialias="false" y1="-42.372" y2="-42.6316" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="212.052" x2="212.952"/>
                                        <polygon closed="false" antialias="false" y1="-32.5591" y2="-31.7802" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="212.052" x2="212.952"/>
                                        <polygon x6="212.052" closed="false" antialias="false" y1="-42.372" y2="-42.8334" style="line-style:normal;line-weight:thin;filling:none;color:black" y3="-43.3584" y4="-32.6212" x1="212.052" x2="212.052" y5="-32.0977" x3="210.236" y6="-32.5591" x4="210.236" x5="212.052"/>
                                        <polygon closed="false" antialias="false" y1="-57.7009" y2="-59.9742" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="194.326" x2="194.748"/>
                                        <polygon closed="false" antialias="false" y1="7.13967" y2="6.61614" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="158.126" x2="156.31"/>
                                        <polygon closed="false" antialias="false" y1="1.71959" y2="-1.08146" style="line-style:normal;line-weight:thin;filling:none;color:black" y3="-2.71412" x1="153.458" x2="153.458" x3="155.753"/>
                                        <polygon closed="false" antialias="false" y1="-87.529" y2="-89.7613" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="106.783" x2="106.409"/>
                                        <polygon closed="false" antialias="false" y1="-4.53586" y2="-2.66896" style="line-style:normal;line-weight:thin;filling:none;color:black" y3="-2.7141" y4="-4.55701" x1="157.956" x2="157.956" x3="155.753" x4="157.882"/>
                                        <polygon closed="false" antialias="false" y1="1.71959" y2="6.61614" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="153.458" x2="156.31"/>
                                        <polygon closed="false" antialias="false" y1="-1.08146" y2="-4.64593" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="153.458" x2="157.575"/>
                                        <polygon closed="false" antialias="false" y1="7.13967" y2="-0.587576" style="line-style:normal;line-weight:thin;filling:none;color:black" y3="5.47596" x1="158.126" x2="168.989" x3="210.031"/>
                                        <polygon closed="false" antialias="false" y1="1.17208" y2="-5.74519" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="212.518" x2="220.505"/>
                                        <polygon closed="false" antialias="false" y1="-90.7731" y2="-85.6113" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="133.8" x2="127.84"/>
                                        <polygon closed="false" antialias="false" y1="-94.4462" y2="-96.6786" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="114.77" x2="114.396"/>
                                        <polygon closed="false" antialias="false" y1="-94.4462" y2="-93.5967" style="line-style:normal;line-weight:thin;filling:none;color:black" y3="-89.2759" x1="114.77" x2="113.791" x3="114.515"/>
                                        <polygon closed="false" antialias="false" y1="-96.6786" y2="-97.4166" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="114.396" x2="107.823"/>
                                        <polygon closed="false" antialias="false" y1="-96.9778" y2="-90.0619" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="85.6433" x2="77.6564"/>
                                        <polygon closed="false" antialias="false" y1="-96.9778" y2="-100.099" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="85.6433" x2="83.9415"/>
                                        <polygon closed="false" antialias="false" y1="-100.905" y2="-93.9876" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="51.5381" x2="43.5512"/>
                                        <polygon closed="false" antialias="false" y1="-96.7407" y2="-101.431" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="64.9747" x2="64.1873"/>
                                        <polygon closed="false" antialias="false" y1="-101.383" y2="-96.4698" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="63.5396" x2="64.3637"/>
                                        <polygon closed="false" antialias="false" y1="-102.042" y2="-100.905" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="66.6455" x2="51.5381"/>
                                        <polygon closed="false" antialias="false" y1="-95.0671" y2="-95.3282" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="59.1849" x2="59.4883"/>
                                        <polygon closed="false" antialias="false" y1="-95.0121" y2="-94.7496" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="53.9652" x2="53.6618"/>
                                        <polygon closed="false" antialias="false" y1="-90.7533" y2="-91.5323" style="line-style:normal;line-weight:thin;filling:none;color:black" y3="-93.9876" x1="44.4515" x2="43.5512" x3="43.5512"/>
                                        <polygon closed="false" antialias="false" y1="-91.2162" y2="-90.7533" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="44.4515" x2="44.4515"/>
                                        <polygon closed="false" antialias="false" y1="-90.4993" y2="-89.7613" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="99.8362" x2="106.409"/>
                                        <polygon closed="false" antialias="false" y1="-94.7496" y2="-93.9876" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="53.6618" x2="43.5512"/>
                                        <polygon closed="false" antialias="false" y1="-91.2162" y2="-90.6913" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="44.4515" x2="46.2676"/>
                                        <polygon closed="false" antialias="false" y1="-91.1005" y2="-90.7533" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="44.8509" x2="44.4515"/>
                                        <polygon closed="false" antialias="false" y1="-89.7613" y2="-96.6786" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="106.409" x2="114.396"/>
                                        <polygon closed="false" antialias="false" y1="-97.4166" y2="-90.4993" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="107.823" x2="99.8362"/>
                                        <polygon closed="false" antialias="false" y1="-82.7919" y2="-82.5294" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="56.0156" x2="55.7122"/>
                                        <polygon closed="false" antialias="false" y1="-82.5294" y2="-94.7496" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="55.7122" x2="53.6618"/>
                                        <polygon closed="false" antialias="false" y1="-95.0121" y2="-82.7919" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="53.9652" x2="56.0156"/>
                                        <polygon closed="false" antialias="false" y1="-81.742" y2="-80.6173" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="60.191" x2="60.8458"/>
                                        <polygon closed="false" antialias="false" y1="-81.742" y2="-82.5999" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="60.191" x2="60.0457"/>
                                        <polygon closed="false" antialias="false" y1="-101.383" y2="-101.431" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="63.5396" x2="64.1873"/>
                                        <polygon closed="false" antialias="false" y1="-101.416" y2="-102.042" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="65.9216" x2="66.6455"/>
                                        <polygon closed="false" antialias="false" y1="-99.9877" y2="-94.418" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="73.8379" x2="74.7735"/>
                                        <polygon closed="false" antialias="false" y1="-99.9877" y2="-99.2271" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="73.8379" x2="80.6084"/>
                                        <polygon closed="false" antialias="false" y1="-96.6871" y2="-95.973" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="68.233" x2="68.3529"/>
                                        <polygon closed="false" antialias="false" y1="-95.1828" y2="-96.8084" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="67.4188" x2="67.1464"/>
                                        <polygon closed="false" antialias="false" y1="-96.8084" y2="-96.6871" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="67.1464" x2="68.233"/>
                                        <polygon closed="false" antialias="false" y1="-96.6673" y2="-94.8823" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="66.1488" x2="66.4493"/>
                                        <polygon closed="false" antialias="false" y1="-96.6673" y2="-95.9942" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="66.1488" x2="64.4653"/>
                                        <polygon closed="false" antialias="false" y1="-95.1504" y2="-94.3898" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="68.2527" x2="75.0232"/>
                                        <polygon closed="false" antialias="false" y1="-96.1692" y2="-95.2774" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="68.5787" x2="67.55"/>
                                        <polygon closed="false" antialias="false" y1="-95.0304" y2="-95.9942" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="64.6262" x2="64.4653"/>
                                        <polygon closed="false" antialias="false" y1="-82.4602" y2="-82.5999" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="61.3002" x2="60.0457"/>
                                        <polygon closed="false" antialias="false" y1="-95.0459" y2="-94.8808" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="64.4879" x2="65.9583"/>
                                        <polygon closed="false" antialias="false" y1="-93.1833" y2="-90.0619" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="75.9546" x2="77.6564"/>
                                        <polygon closed="false" antialias="false" y1="-93.1833" y2="-95.0671" style="line-style:normal;line-weight:thin;filling:none;color:black" y3="-81.8916" x1="75.9546" x2="59.1849" x3="61.3961"/>
                                        <polygon closed="false" antialias="false" y1="-95.1504" y2="-99.9877" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="68.2527" x2="73.8379"/>
                                        <polygon closed="false" antialias="false" y1="-94.3898" y2="-99.2271" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="75.0232" x2="80.6084"/>
                                        <polygon closed="false" antialias="false" y1="-100.099" y2="-93.1833" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="83.9415" x2="75.9546"/>
                                        <polygon closed="false" antialias="false" y1="-100.099" y2="-102.042" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="83.9415" x2="66.6455"/>
                                        <polygon closed="false" antialias="false" y1="-96.9778" y2="-84.155" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="85.6433" x2="87.7952"/>
                                        <polygon closed="false" antialias="false" y1="-21.0459" y2="-4.53586" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="100.765" x2="157.956"/>
                                        <polygon x6="105.897" x7="105.671" closed="false" antialias="false" y1="-19.2735" y2="-19.028" style="line-style:normal;line-weight:thin;filling:none;color:black" y3="-18.7895" y4="-18.5595" x1="106.903" x2="106.718" y5="-18.3394" x3="106.526" y6="-18.1263" x4="106.325" y7="-17.9231" x5="106.116"/>
                                        <polygon y15="-27.0572" closed="false" y16="-27.1362" y17="-27.2082" y18="-27.2703" x20="101.542" y19="-27.314" x21="101.46" x22="101.378" x23="101.296" x24="101.216" x25="101.137" x26="101.062" x27="100.99" x28="100.924" x29="100.86" x1="102.194" x2="102.23" x3="102.257" x4="102.276" x5="102.289" x6="102.294" x7="102.289" x8="102.278" x9="102.258" y20="-27.3507" y21="-27.3803" y22="-27.4015" y23="-27.4142" y24="-27.4199" style="line-style:normal;line-weight:thin;filling:none;color:black" antialias="false" y25="-27.4156" y26="-27.4044" y27="-27.3832" y28="-27.3564" x30="100.804" y29="-27.3197" x10="102.23" x11="102.196" x12="102.154" x13="102.105" x14="102.038" x15="101.964" x16="101.883" x17="101.796" x18="101.703" x19="101.624" y1="-25.9227" y2="-25.9876" y3="-26.0567" y4="-26.1301" y5="-26.2091" y6="-26.2896" y7="-26.3728" y8="-26.4589" y9="-26.545" y30="-27.2774" y10="-26.6296" y11="-26.7143" y12="-26.7976" y13="-26.878" y14="-26.9711"/>
                                        <polygon y15="-22.5275" closed="false" y16="-22.1592" y17="-21.7867" y18="-21.4099" y19="-21.0303" x1="100.694" x2="100.521" x3="100.356" x4="100.2" x5="100.055" x6="99.9181" x7="99.7925" x8="99.6753" x9="99.5695" style="line-style:normal;line-weight:thin;filling:none;color:black" antialias="false" x10="99.4721" x11="99.3847" x12="99.3085" x13="99.2421" x14="99.1857" x15="99.1391" x16="99.1026" x17="99.0772" x18="99.0619" x19="99.056" y1="-27.1503" y2="-26.8596" y3="-26.5633" y4="-26.2613" y5="-25.9509" y6="-25.6348" y7="-25.3117" y8="-24.9829" y9="-24.647" y10="-24.3069" y11="-23.9598" y12="-23.6084" y13="-23.2528" y14="-22.893"/>
                                        <polygon closed="false" antialias="false" y1="-27.2773" y2="-27.2181" style="line-style:normal;line-weight:thin;filling:none;color:black" y3="-27.1503" x1="100.803" x2="100.744" x3="100.694"/>
                                        <polygon closed="false" antialias="false" y1="-10.4964" y2="-10.6587" style="line-style:normal;line-weight:thin;filling:none;color:black" y3="-10.828" y4="-11.0058" x1="97.0295" x2="97.2539" x3="97.4726" x4="97.6843"/>
                                        <polygon y15="-14.6168" closed="false" y16="-14.9273" y17="-15.2434" y18="-15.5651" x20="100.453" y19="-15.8925" x21="100.499" x22="100.536" x23="100.563" x24="100.578" x25="100.584" x1="97.6843" x2="97.9115" x3="98.1316" x4="98.3418" x5="98.5436" x6="98.737" x7="98.9218" x8="99.0968" x9="99.2633" y20="-16.2241" y21="-16.5599" y22="-16.9014" y23="-17.2457" y24="-17.5943" style="line-style:normal;line-weight:thin;filling:none;color:black" antialias="false" y25="-17.9471" x10="99.4213" x11="99.5681" x12="99.7064" x13="99.8348" x14="99.9547" x15="100.063" x16="100.161" x17="100.25" x18="100.327" x19="100.395" y1="-11.0058" y2="-11.2104" y3="-11.4249" y4="-11.6479" y5="-11.8793" y6="-12.1178" y7="-12.3661" y8="-12.6215" y9="-12.884" y10="-13.1549" y11="-13.4343" y12="-13.7194" y13="-14.0115" y14="-14.312"/>
                                        <polygon x6="101.456" x7="101.339" x8="101.232" closed="false" x9="101.136" y10="-23.1527" y11="-22.814" x10="101.051" y12="-22.4697" x11="100.976" y13="-22.1211" x12="100.913" y14="-21.7669" x13="100.859" y15="-21.4085" x14="100.817" x15="100.785" y16="-21.0459" x16="100.765" y1="-25.9227" y2="-25.6419" y3="-25.354" y4="-25.0591" y5="-24.7571" y6="-24.4481" x1="102.194" style="line-style:normal;line-weight:thin;filling:none;color:black" y7="-24.1334" antialias="false" y8="-23.8131" x2="102.026" y9="-23.4857" x3="101.868" x4="101.72" x5="101.583"/>
                                        <polygon x43="218.872" x44="219.061" y1="-5.74519" x45="219.261" y2="-6.28141" x46="219.472" y3="-6.82046" x47="219.692" y4="-7.36091" x48="219.922" y5="-7.90278" x49="220.162" y6="-8.44606" y7="-8.99074" y8="-9.53684" y9="-10.0829" y30="-21.3831" y31="-21.8925" y32="-22.3977" y33="-22.8987" y34="-23.3954" y35="-23.8878" y36="-24.3747" y37="-24.8545" y38="-25.33" y39="-25.7985" x50="220.411" x51="220.671" x52="220.941" x10="218.581" x11="218.419" x12="218.267" x13="218.124" x14="217.993" x15="217.871" y40="-26.2613" x16="217.76" y41="-26.7185" x17="217.661" y42="-27.1673" style="line-style:normal;line-weight:thin;filling:none;color:black" x18="217.571" y43="-27.6104" x19="217.493" y44="-28.0478" y45="-28.4768" y46="-28.8987" y47="-29.3136" y48="-29.7214" y49="-30.1221" x20="217.425" x21="217.369" x22="217.324" x23="217.289" x24="217.265" x25="217.252" x26="217.252" y50="-30.5144" x27="217.261" y51="-30.8997" x28="217.28" y52="-31.2764" x29="217.311" y10="-10.6305" y11="-11.1794" y12="-11.7269" y13="-12.2758" y14="-12.8233" y15="-13.3722" y16="-13.9198" y17="-14.4673" y18="-15.0134" y19="-15.5595" x30="217.352" closed="false" x31="217.406" x32="217.469" x33="217.543" x1="220.505" x34="217.627" x2="220.252" x35="217.723" x3="220.008" x36="217.831" x4="219.774" x37="217.948" x38="218.076" x5="219.549" x6="219.336" x39="218.214" x7="219.132" x8="218.938" x9="218.755" y20="-16.1027" y21="-16.6432" y22="-17.1822" y23="-17.7171" y24="-18.2505" y25="-18.781" antialias="false" y26="-19.3088" y27="-19.8323" y28="-20.353" y29="-20.8695" x40="218.362" x41="218.522" x42="218.691"/>
                                        <polygon y15="-3.29409" closed="false" y16="-3.13604" y17="-2.98364" y18="-2.81431" x20="220.555" y19="-2.65344" x21="220.458" x22="220.352" x23="220.236" x24="220.111" x1="220.505" x2="220.586" x3="220.66" x4="220.723" x5="220.78" x6="220.829" x7="220.869" x8="220.898" x9="220.921" y20="-2.50104" y21="-2.3557" y22="-2.22023" y23="-2.09323" y24="-1.9747" style="line-style:normal;line-weight:thin;filling:none;color:black" antialias="false" x10="220.935" x11="220.941" x12="220.935" x13="220.923" x14="220.9" x15="220.869" x16="220.831" x17="220.782" x18="220.716" x19="220.641" y1="-5.74519" y2="-5.56739" y3="-5.38959" y4="-5.21038" y5="-5.03116" y6="-4.85054" y7="-4.66992" y8="-4.49071" y9="-4.31291" y10="-4.13511" y11="-3.96154" y12="-3.78939" y13="-3.62006" y14="-3.45496"/>
                                        <polygon y15="-41.5296" closed="false" y16="-41.4223" y17="-41.3221" y18="-41.2276" x20="196.236" y19="-41.1415" x21="196.358" x22="196.483" x1="195.107" x2="195.09" x3="195.082" x4="195.082" x5="195.093" x6="195.114" x7="195.144" x8="195.182" x9="195.23" y20="-41.0625" y21="-40.9919" y22="-40.9284" style="line-style:normal;line-weight:thin;filling:none;color:black" antialias="false" x10="195.287" x11="195.351" x12="195.425" x13="195.504" x14="195.591" x15="195.686" x16="195.787" x17="195.893" x18="196.003" x19="196.118" y1="-43.292" y2="-43.1707" y3="-43.0465" y4="-42.9195" y5="-42.7897" y6="-42.6599" y7="-42.5272" y8="-42.3946" y9="-42.2633" y10="-42.1335" y11="-42.0051" y12="-41.8809" y13="-41.7596" y14="-41.6424"/>
                                        <polygon y15="-56.3744" closed="false" y16="-56.2164" y17="-56.0612" y18="-55.906" x20="197.46" y19="-55.7536" x21="197.618" x1="196.226" x2="196.204" x3="196.189" x4="196.184" x5="196.19" x6="196.207" x7="196.234" x8="196.27" x9="196.317" y20="-55.6026" y21="-55.453" style="line-style:normal;line-weight:thin;filling:none;color:black" antialias="false" x10="196.373" x11="196.44" x12="196.517" x13="196.602" x14="196.698" x15="196.802" x16="196.917" x17="197.039" x18="197.171" x19="197.31" y1="-58.6111" y2="-58.4558" y3="-58.2992" y4="-58.1412" y5="-57.9831" y6="-57.8237" y7="-57.6628" y8="-57.5019" y9="-57.3396" y10="-57.1788" y11="-57.0165" y12="-56.8542" y13="-56.6934" y14="-56.5339"/>
                                        <polygon y15="-56.8331" closed="false" y16="-57.0292" y17="-57.2239" y18="-57.4187" x20="210.046" y19="-57.6106" x21="209.883" x22="209.694" x23="209.497" x24="209.288" x25="209.07" x26="208.845" x27="208.61" x28="208.368" x29="208.117" x1="211.279" x2="211.306" x3="211.323" x4="211.329" x5="211.324" x6="211.31" x7="211.285" x8="211.249" x9="211.204" y20="-57.8025" y21="-57.9916" y22="-58.2004" y23="-58.405" y24="-58.6054" style="line-style:normal;line-weight:thin;filling:none;color:black" antialias="false" y25="-58.803" y26="-58.9963" y27="-59.1854" y28="-59.3688" x30="207.858" y29="-59.548" x10="211.148" x11="211.081" x12="211.004" x13="210.918" x14="210.822" x15="210.716" x16="210.6" x17="210.475" x18="210.34" x19="210.198" y1="-54.1675" y2="-54.3453" y3="-54.5245" y4="-54.7079" y5="-54.8942" y6="-55.0819" y7="-55.271" y8="-55.4629" y9="-55.6562" y30="-59.7216" y10="-55.8509" y11="-56.0471" y12="-56.2432" y13="-56.4408" y14="-56.6369"/>
                                        <polygon x6="205.734" x7="205.423" x8="205.106" closed="false" y1="-60.1435" y2="-60.3227" y3="-60.4949" y4="-60.6586" y5="-60.8152" y6="-60.9634" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="207.212" y7="-61.1045" antialias="false" x2="206.928" y8="-61.2357" x3="206.639" x4="206.343" x5="206.042"/>
                                        <polygon x6="200.725" x7="200.763" x8="200.791" closed="false" y1="-39.9449" y2="-40.0239" y3="-40.1114" y4="-40.2045" y5="-40.3061" y6="-40.4148" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="200.402" y7="-40.5291" antialias="false" x2="200.484" y8="-40.649" x3="200.559" x4="200.623" x5="200.678"/>
                                        <polygon y1="-51.9478" y2="-51.8448" y3="-51.7516" y4="-51.667" y5="-51.5936" y6="-51.5287" y7="-51.4722" y8="-51.4271" y9="-51.3918" y30="-52.6929" y31="-52.8213" y32="-52.9539" y33="-53.0922" y34="-53.2333" y35="-53.3787" y36="-53.5297" y37="-53.6835" y38="-53.8415" y39="-54.0024" x10="205.98" x11="206.285" x12="206.587" x13="206.883" x14="207.174" x15="207.457" y40="-54.1675" x16="207.735" x17="208.008" style="line-style:normal;line-weight:thin;filling:none;color:black" x18="208.272" x19="208.527" x20="208.751" x21="208.967" x22="209.175" x23="209.375" x24="209.566" x25="209.749" x26="209.923" x27="210.089" x28="210.244" x29="210.391" y10="-51.3664" y11="-51.3509" y12="-51.3452" y13="-51.3495" y14="-51.3636" y15="-51.3876" y16="-51.4229" y17="-51.4666" y18="-51.5217" y19="-51.5852" closed="false" x30="210.515" x31="210.631" x32="210.738" x33="210.837" x1="203.144" x34="210.927" x2="203.46" x35="211.009" x3="203.777" x36="211.081" x4="204.095" x37="211.145" x5="204.412" x38="211.198" x6="204.728" x39="211.243" x7="205.044" x8="205.358" x9="205.67" y20="-51.6515" y21="-51.7249" y22="-51.8053" y23="-51.8928" y24="-51.9887" y25="-52.0918" antialias="false" y26="-52.2004" y27="-52.3175" y28="-52.4403" y29="-52.5701" x40="211.279"/>
                                        <polygon x6="199.447" x7="199.568" x8="199.688" closed="false" x9="199.804" y10="-39.6978" y11="-39.7288" x10="199.916" y12="-39.7697" x11="200.024" y13="-39.8191" x12="200.127" y14="-39.8784" x13="200.225" y15="-39.9447" x14="200.317" x15="200.402" y1="-39.8405" y2="-39.7868" y3="-39.7431" y4="-39.7078" y5="-39.6824" y6="-39.6669" x1="198.824" style="line-style:normal;line-weight:thin;filling:none;color:black" y7="-39.6598" antialias="false" y8="-39.6625" x2="198.948" y9="-39.6752" x3="199.074" x4="199.198" x5="199.322"/>
                                        <polygon x6="199.756" x7="199.88" x8="200" closed="false" x9="200.117" y10="-39.9632" y11="-39.9956" x10="200.231" y12="-40.0379" x11="200.34" y13="-40.0902" x12="200.443" x13="200.542" y1="-40.1015" y2="-40.0479" y3="-40.0041" y4="-39.9688" y5="-39.9434" y6="-39.9279" x1="199.126" style="line-style:normal;line-weight:thin;filling:none;color:black" y7="-39.9223" antialias="false" x2="199.253" y8="-39.9265" y9="-39.9392" x3="199.379" x4="199.506" x5="199.631"/>
                                        <polygon x6="200.738" x7="200.491" x8="200.244" closed="false" x9="199.997" y10="-46.1764" y11="-46.0494" x10="199.749" y12="-45.9111" x11="199.499" x12="199.25" y1="-46.8932" y2="-46.8523" y3="-46.8029" y4="-46.7422" y5="-46.6731" y6="-46.5927" x1="201.951" style="line-style:normal;line-weight:thin;filling:none;color:black" y7="-46.5038" antialias="false" x2="201.711" y8="-46.4036" y9="-46.2949" x3="201.47" x4="201.227" x5="200.983"/>
                                        <polygon y15="-48.5781" closed="false" y16="-48.6839" y17="-48.7813" y18="-48.8702" x20="196.681" y19="-48.9478" x21="196.562" x22="196.445" x1="199.25" x2="199.105" x3="198.958" x4="198.813" x5="198.668" x6="198.522" x7="198.377" x8="198.233" x9="198.089" y20="-49.0169" y21="-49.0776" y22="-49.127" style="line-style:normal;line-weight:thin;filling:none;color:black" antialias="false" x10="197.945" x11="197.803" x12="197.674" x13="197.546" x14="197.419" x15="197.293" x16="197.169" x17="197.045" x18="196.922" x19="196.801" y1="-45.9111" y2="-46.1707" y3="-46.4219" y4="-46.6618" y5="-46.8918" y6="-47.1119" y7="-47.3222" y8="-47.5225" y9="-47.7116" y10="-47.8908" y11="-48.0588" y12="-48.2027" y13="-48.3368" y14="-48.4623"/>
                                        <polygon y1="-61.2357" y2="-61.3162" y3="-61.3867" y4="-61.4474" y5="-61.501" y6="-61.5433" y7="-61.5786" y8="-61.6026" y9="-61.6181" y30="-60.0603" y31="-59.9304" y32="-59.7964" y33="-59.6595" y34="-59.5184" y35="-59.3745" y36="-59.2277" y37="-59.0767" y38="-58.9243" y39="-58.7691" x10="202.039" x11="201.704" x12="201.373" x13="201.048" x14="200.728" x15="200.415" y40="-58.6111" x16="200.108" x17="199.809" style="line-style:normal;line-weight:thin;filling:none;color:black" x18="199.517" x19="199.233" x20="198.987" x21="198.748" x22="198.518" x23="198.296" x24="198.085" x25="197.883" x26="197.691" x27="197.509" x28="197.338" x29="197.177" y10="-61.6238" y11="-61.6195" y12="-61.6068" y13="-61.5842" y14="-61.5518" y15="-61.5095" y16="-61.4587" y17="-61.3994" y18="-61.3303" y19="-61.2527" closed="false" x30="197.041" x31="196.914" x32="196.796" x33="196.689" x1="205.106" x34="196.593" x2="204.769" x35="196.506" x3="204.429" x36="196.43" x4="204.088" x37="196.363" x5="203.745" x38="196.307" x6="203.402" x39="196.262" x7="203.059" x8="202.718" x9="202.377" y20="-61.175" y21="-61.0904" y22="-60.9987" y23="-60.9013" y24="-60.7969" y25="-60.6868" antialias="false" y26="-60.5711" y27="-60.4483" y28="-60.3199" y29="-60.1859" x40="196.226"/>
                                        <polygon y15="-41.792" closed="false" y16="-41.6848" y17="-41.5832" y18="-41.49" x20="196.544" y19="-41.4026" x21="196.665" x22="196.79" x1="195.409" x2="195.392" x3="195.384" x4="195.389" x5="195.399" x6="195.42" x7="195.45" x8="195.49" x9="195.538" y20="-41.3235" y21="-41.253" y22="-41.1909" style="line-style:normal;line-weight:thin;filling:none;color:black" antialias="false" x10="195.594" x11="195.659" x12="195.731" x13="195.812" x14="195.899" x15="195.994" x16="196.094" x17="196.2" x18="196.31" x19="196.426" y1="-43.5545" y2="-43.4331" y3="-43.309" y4="-43.182" y5="-43.0521" y6="-42.9209" y7="-42.7897" y8="-42.657" y9="-42.5244" y10="-42.3946" y11="-42.2676" y12="-42.1434" y13="-42.022" y14="-41.9049"/>
                                        <polygon x6="148.15" closed="false" antialias="false" y1="-88.4659" y2="-88.1795" style="line-style:normal;line-weight:thin;filling:none;color:black" y3="-87.8831" y4="-87.5755" x1="144.856" x2="145.518" y5="-87.2594" x3="146.178" y6="-86.9321" x4="146.838" x5="147.495"/>
                                        <polygon x6="137.967" x7="137.317" x8="136.663" closed="false" x9="136.009" y1="-85.9471" y2="-86.3281" y3="-86.6992" y4="-87.0605" y5="-87.4118" y6="-87.7533" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="141.183" y7="-88.0849" antialias="false" x2="140.545" y8="-88.4067" y9="-88.7185" x3="139.905" x4="139.263" x5="138.616"/>
                                        <polygon x6="133.656" x7="133.004" x8="132.351" closed="false" x9="131.696" y1="-82.2133" y2="-82.5929" y3="-82.964" y4="-83.3253" y5="-83.6766" y6="-84.0195" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="136.871" y7="-84.3511" antialias="false" x2="136.233" y8="-84.6729" y9="-84.9847" x3="135.594" x4="134.95" x5="134.304"/>
                                        <polygon x6="192.692" x7="192.806" x8="192.926" closed="false" x9="193.05" y10="-60.6161" y11="-60.5949" x10="193.177" y12="-60.5653" x11="193.304" y13="-60.5258" x12="193.428" y14="-60.4792" x13="193.547" x14="193.661" y1="-60.4427" y2="-60.485" y3="-60.5231" y4="-60.5555" y5="-60.5824" y6="-60.6035" x1="192.335" style="line-style:normal;line-weight:thin;filling:none;color:black" y7="-60.6219" antialias="false" x2="192.391" y8="-60.6289" y9="-60.6274" x3="192.456" x4="192.528" x5="192.607"/>
                                        <polygon x6="195.107" x7="195.145" x8="195.177" closed="false" x9="195.2" y10="-59.5085" y11="-59.4563" x10="195.217" y12="-59.4055" x11="195.224" x12="195.224" y1="-59.9742" y2="-59.9291" y3="-59.8811" y4="-59.8274" y5="-59.7724" y6="-59.7131" x1="194.748" style="line-style:normal;line-weight:thin;filling:none;color:black" y7="-59.6623" antialias="false" x2="194.835" y8="-59.6115" y9="-59.5607" x3="194.915" x4="194.987" x5="195.052"/>
                                        <polygon x6="191.326" x7="191.271" x8="191.226" closed="false" x9="191.19" y10="-59.1064" y11="-59.1713" x10="191.166" y12="-59.2362" x11="191.151" y13="-59.3011" x12="191.146" x13="191.153" y1="-58.5772" y2="-58.6238" y3="-58.6746" y4="-58.7296" y5="-58.7874" y6="-58.8481" x1="191.721" style="line-style:normal;line-weight:thin;filling:none;color:black" y7="-58.9102" antialias="false" x2="191.628" y8="-58.9751" y9="-59.04" x3="191.542" x4="191.461" x5="191.39"/>
                                        <polygon closed="false" antialias="false" y1="-58.2696" y2="-58.2456" style="line-style:normal;line-weight:thin;filling:none;color:black" y3="-58.2216" x1="195.145" x2="195.145" x3="195.14"/>
                                        <polygon y15="-57.6926" closed="false" y16="-57.7038" y17="-57.7236" y18="-57.7532" x20="193.321" y19="-57.7913" x21="193.193" x1="195.14" x2="195.124" x3="195.099" x4="195.067" x5="195.024" x6="194.975" x7="194.917" x8="194.853" x9="194.781" y20="-57.8379" y21="-57.8929" style="line-style:normal;line-weight:thin;filling:none;color:black" antialias="false" x10="194.675" x11="194.559" x12="194.435" x13="194.304" x14="194.167" x15="194.024" x16="193.88" x17="193.736" x18="193.594" x19="193.456" y1="-58.2216" y2="-58.1609" y3="-58.1031" y4="-58.048" y5="-57.9944" y6="-57.9464" y7="-57.8998" y8="-57.8575" y9="-57.8194" y10="-57.7756" y11="-57.7418" y12="-57.7149" y13="-57.698" y14="-57.691"/>
                                        <polygon x6="191.306" closed="false" antialias="false" y1="-59.3011" y2="-59.3561" style="line-style:normal;line-weight:thin;filling:none;color:black" y3="-59.4084" y4="-59.4592" x1="191.153" x2="191.168" y5="-59.5071" x3="191.19" y6="-59.5523" x4="191.222" x5="191.26"/>
                                        <polygon x43="109.567" x44="108.963" y1="-81.0647" x45="108.361" y2="-81.4626" x46="107.764" y3="-81.8506" y4="-82.2288" y5="-82.5971" y6="-82.9555" y7="-83.3027" y8="-83.6399" y9="-83.9673" y30="-88.3107" y31="-88.394" y32="-88.4673" y33="-88.5308" y34="-88.5831" y35="-88.624" y36="-88.655" y37="-88.6748" y38="-88.6847" y39="-88.6831" x10="130.926" x11="130.261" x12="129.595" x13="128.928" x14="128.257" x15="127.586" y40="-88.6718" x16="126.914" y41="-88.6492" x17="126.241" y42="-88.6168" style="line-style:normal;line-weight:thin;filling:none;color:black" x18="125.566" y43="-88.573" x19="124.892" y44="-88.518" y45="-88.4531" y46="-88.3783" x20="124.216" x21="123.54" x22="122.864" x23="122.187" x24="121.539" x25="120.894" x26="120.249" x27="119.604" x28="118.962" x29="118.322" y10="-84.2848" y11="-84.591" y12="-84.8859" y13="-85.171" y14="-85.4462" y15="-85.71" y16="-85.9626" y17="-86.2053" y18="-86.4368" y19="-86.6569" closed="false" x30="117.683" x31="117.045" x32="116.408" x33="115.775" x1="136.807" x34="115.143" x2="136.165" x35="114.513" x3="135.519" x36="113.887" x4="134.87" x37="113.262" x5="134.219" x38="112.638" x6="133.565" x39="112.018" x7="132.908" x8="132.251" x9="131.589" y20="-86.8657" y21="-87.0647" y22="-87.2524" y23="-87.4274" y24="-87.5854" y25="-87.7322" antialias="false" y26="-87.869" y27="-87.996" y28="-88.1117" y29="-88.2162" x40="111.402" x41="110.786" x42="110.175"/>
                                        <polygon y15="-81.749" closed="false" y16="-81.876" y17="-82.0044" y18="-82.1343" x20="55.7391" y19="-82.2655" x21="55.7122" x1="57.6793" x2="57.5523" x3="57.4267" x4="57.2997" x5="57.1727" x6="57.0485" x7="56.9243" x8="56.803" x9="56.6661" y20="-82.3981" y21="-82.5294" style="line-style:normal;line-weight:thin;filling:none;color:black" antialias="false" x10="56.5349" x11="56.4107" x12="56.2936" x13="56.1849" x14="56.0833" x15="56.0057" x16="55.9351" x17="55.873" x18="55.8206" x19="55.7757" y1="-80.5849" y2="-80.6046" y3="-80.6328" y4="-80.6709" y5="-80.7189" y6="-80.7754" y7="-80.8403" y8="-80.9151" y9="-81.011" y10="-81.1168" y11="-81.2326" y12="-81.3567" y13="-81.488" y14="-81.6263"/>
                                        <polygon y15="-36.1419" closed="false" y16="-35.4209" y17="-34.6941" y18="-33.9632" x20="47.5052" y19="-33.228" x1="50.7098" x2="50.4473" x3="50.1961" x4="49.9548" x5="49.7234" x6="49.5019" x7="49.2916" x8="49.0912" x9="48.9022" y20="-32.4886" style="line-style:normal;line-weight:thin;filling:none;color:black" antialias="false" x10="48.7229" x11="48.5536" x12="48.3956" x13="48.2474" x14="48.1091" x15="47.9821" x16="47.8664" x17="47.7592" x18="47.6646" x19="47.5799" y1="-45.6796" y2="-45.0362" y3="-44.3871" y4="-43.7309" y5="-43.0691" y6="-42.4016" y7="-41.7285" y8="-41.0498" y9="-40.364" y10="-39.6739" y11="-38.9783" y12="-38.2769" y13="-37.57" y14="-36.8588"/>
                                        <polygon x6="60.5777" x7="60.4521" x8="60.3223" closed="false" y1="-80.7429" y2="-80.6879" y3="-80.6441" y4="-80.6117" y5="-80.5891" y6="-80.5764" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="61.1464" y7="-80.5748" antialias="false" x2="61.0434" y8="-80.5847" x3="60.9347" x4="60.8204" x5="60.7019"/>
                                        <polygon x6="136.868" closed="false" antialias="false" y1="-80.0148" y2="-80.3422" style="line-style:normal;line-weight:thin;filling:none;color:black" y3="-80.6597" y4="-80.9659" x1="140.163" x2="139.508" y5="-81.2622" x3="138.851" y6="-81.5487" x4="138.192" x5="137.531"/>
                                        <polygon x6="61.3909" x7="61.3628" x8="61.3247" closed="false" x9="61.2781" y10="-80.8459" y11="-80.7556" x10="61.2231" y12="-80.6724" x11="61.1596" y13="-80.5976" x12="61.0891" x13="61.01" y1="-81.8916" y2="-81.7617" y3="-81.6347" y4="-81.5092" y5="-81.3878" y6="-81.2693" x1="61.3961" style="line-style:normal;line-weight:thin;filling:none;color:black" y7="-81.155" antialias="false" x2="61.4131" y8="-81.0463" y9="-80.9433" x3="61.4215" x4="61.4215" x5="61.4104"/>
                                        <polygon x6="60.5622" x7="60.4592" x8="60.3533" closed="false" x9="60.2447" y10="-80.314" y11="-80.3224" x10="60.1332" x11="60.0189" y1="-80.5976" y2="-80.5355" y3="-80.4805" y4="-80.4325" y5="-80.3929" y6="-80.3605" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="61.0081" y7="-80.3365" antialias="false" x2="60.9291" y8="-80.321" y9="-80.314" x3="60.8444" x4="60.7555" x5="60.6609"/>
                                        <polygon x6="41.8593" x7="41.8535" closed="false" antialias="false" y1="-35.5747" y2="-35.5253" style="line-style:normal;line-weight:thin;filling:none;color:black" y3="-35.4674" y4="-35.4025" x1="42.0202" x2="41.971" y5="-35.3334" x3="41.9286" y6="-35.2586" x4="41.8964" y7="-35.1782" x5="41.8736"/>
                                        <polygon x6="42.6199" x7="42.5451" x8="42.4717" closed="false" x9="42.3983" y10="-35.6889" y11="-35.6818" x10="42.3264" y12="-35.6677" x11="42.2558" y13="-35.6451" x12="42.1909" y14="-35.614" x13="42.1288" y15="-35.5745" x14="42.071" x15="42.0202" y1="-35.3235" y2="-35.4053" y3="-35.4787" y4="-35.5422" y5="-35.5958" y6="-35.6311" x1="43.0122" style="line-style:normal;line-weight:thin;filling:none;color:black" y7="-35.658" antialias="false" y8="-35.6763" x2="42.9431" y9="-35.6862" x3="42.8654" x4="42.7822" x5="42.6933"/>
                                        <polygon closed="false" antialias="false" y1="-31.2553" y2="-31.3033" style="line-style:normal;line-weight:thin;filling:none;color:black" y3="-31.3555" x1="44.3993" x2="44.4699" x3="44.5362"/>
                                        <polygon y15="-32.9599" closed="false" y16="-33.0883" y17="-33.2153" y18="-33.3381" y19="-33.4566" x1="44.5362" x2="44.6152" x3="44.6858" x4="44.7478" x5="44.8002" x6="44.8425" x7="44.8748" x8="44.896" x9="44.9071" style="line-style:normal;line-weight:thin;filling:none;color:black" antialias="false" x10="44.9071" x11="44.8971" x12="44.8759" x13="44.8447" x14="44.8039" x15="44.7531" x16="44.6939" x17="44.6247" x18="44.5457" x19="44.4596" y1="-31.3554" y2="-31.4316" y3="-31.5177" y4="-31.6109" y5="-31.711" y6="-31.8183" y7="-31.9326" y8="-32.0525" y9="-32.1753" y10="-32.3023" y11="-32.4321" y12="-32.5634" y13="-32.696" y14="-32.8286"/>
                                        <polygon x43="44.1693" x44="43.9731" y1="-51.4807" x45="43.7671" y2="-51.8786" x46="43.5512" y3="-52.2822" y4="-52.6929" y5="-53.1105" y6="-53.5339" y7="-53.9629" y8="-54.3989" y9="-54.8406" y30="-65.136" y31="-65.6596" y32="-66.1845" y33="-66.7094" y34="-67.2358" y35="-67.7621" y36="-68.2899" y37="-68.8176" y38="-69.344" y39="-69.8717" x10="45.15" x11="45.2799" x12="45.3998" x13="45.5113" x14="45.6114" x15="45.7018" y40="-70.3995" x16="45.7822" y41="-70.9258" x17="45.8527" y42="-71.4522" style="line-style:normal;line-weight:thin;filling:none;color:black" x18="45.9134" y43="-71.9771" x19="45.9642" y44="-72.502" y45="-73.0241" y46="-73.5463" x20="46.0039" x21="46.0351" x22="46.0547" x23="46.0648" x24="46.0648" x25="46.0547" x26="46.0351" x27="46.0039" x28="45.9642" x29="45.9134" y10="-55.2865" y11="-55.7394" y12="-56.1966" y13="-56.6595" y14="-57.128" y15="-57.6021" y16="-58.0805" y17="-58.5631" y18="-59.0485" y19="-59.5396" closed="false" x30="45.8527" x31="45.7822" x32="45.7018" x33="45.6114" x1="43.5512" x34="45.5113" x2="43.7671" x35="45.3998" x3="43.9731" x36="45.2799" x4="44.1693" x37="45.15" x5="44.357" x38="45.0117" x6="44.5348" x39="44.8621" x7="44.7027" x8="44.8621" x9="45.0117" y20="-60.0335" y21="-60.5302" y22="-61.0311" y23="-61.5349" y24="-62.0415" y25="-62.5509" antialias="false" y26="-63.0631" y27="-63.5782" y28="-64.0946" y29="-64.6139" x40="44.7027" x41="44.5348" x42="44.357"/>
                                        <polygon y15="2.78074" closed="false" y16="2.60436" y17="2.42514" y18="2.24594" x20="212.792" y19="2.06672" x21="212.736" x22="212.671" x23="212.599" x24="212.517" x1="212.124" x2="212.25" x3="212.365" x4="212.471" x5="212.568" x6="212.655" x7="212.729" x8="212.796" x9="212.844" y20="1.8861" y21="1.70689" y22="1.52768" y23="1.34847" y24="1.17208" style="line-style:normal;line-weight:thin;filling:none;color:black" antialias="false" x10="212.882" x11="212.913" x12="212.936" x13="212.949" x14="212.954" x15="212.949" x16="212.934" x17="212.912" x18="212.88" x19="212.841" y1="4.94116" y2="4.82403" y3="4.69703" y4="4.56156" y5="4.41622" y6="4.26382" y7="4.10296" y8="3.93362" y9="3.78122" y10="3.62318" y11="3.46231" y12="3.2958" y13="3.12788" y14="2.95572"/>
                                        <polygon x6="210.867" x7="211.026" x8="211.18" closed="false" x9="211.331" y10="5.33182" y11="5.27115" x10="211.478" y12="5.20059" x11="211.617" y13="5.12298" x12="211.753" y14="5.03549" x13="211.883" y15="4.94095" x14="212.007" x15="212.124" y1="5.47596" y2="5.49713" y3="5.5084" y4="5.51105" y5="5.50401" y6="5.48851" x1="210.031" style="line-style:normal;line-weight:thin;filling:none;color:black" y7="5.46311" antialias="false" y8="5.42781" x2="210.203" y9="5.38405" x3="210.373" x4="210.541" x5="210.704"/>
                                        <polygon x43="109.765" x44="109.162" y1="-79.6987" x45="108.563" y2="-80.1023" x46="107.966" y3="-80.496" x47="107.373" y4="-80.8812" x48="106.783" y5="-81.2566" y6="-81.622" y7="-81.9776" y8="-82.3234" y9="-82.6592" y30="-87.2905" y31="-87.3907" y32="-87.4824" y33="-87.5628" y34="-87.632" y35="-87.6926" y36="-87.742" y37="-87.7815" y38="-87.8097" y39="-87.8281" x10="130.882" x11="130.23" x12="129.577" x13="128.922" x14="128.266" x15="127.607" y40="-87.8366" x16="126.948" y41="-87.8339" x17="126.286" y42="-87.8227" style="line-style:normal;line-weight:thin;filling:none;color:black" x18="125.624" y43="-87.7987" x19="124.961" y44="-87.7663" y45="-87.7225" y46="-87.6689" y47="-87.604" y48="-87.5292" x20="124.296" x21="123.632" x22="122.967" x23="122.301" x24="121.635" x25="120.996" x26="120.359" x27="119.723" x28="119.087" x29="118.453" y10="-82.9852" y11="-83.3013" y12="-83.6075" y13="-83.9024" y14="-84.1889" y15="-84.464" y16="-84.7279" y17="-84.9833" y18="-85.2274" y19="-85.4603" closed="false" x30="117.821" x31="117.189" x32="116.559" x33="115.931" x1="136.635" x34="115.305" x2="136.007" x35="114.68" x3="135.376" x36="114.057" x4="134.741" x37="113.437" x5="134.105" x38="112.818" x6="133.466" x39="112.202" x7="132.822" x8="132.179" x9="131.531" y20="-85.6832" y21="-85.8963" y22="-86.0981" y23="-86.2886" y24="-86.4692" y25="-86.6315" antialias="false" y26="-86.7839" y27="-86.9264" y28="-87.0576" y29="-87.179" x40="111.589" x41="110.978" x42="110.37"/>
                                        <polygon x43="210.593" x44="210.767" y1="-24.3592" x45="210.95" y2="-23.9824" x46="211.143" y3="-23.5986" x47="211.348" y4="-23.2049" x48="211.561" y5="-22.8055" x49="211.785" y6="-22.3977" y7="-21.9814" y8="-21.5595" y9="-21.1305" y30="-10.8012" y31="-10.265" y32="-9.72593" y33="-9.18548" y34="-8.6422" y35="-8.09751" y36="-7.55" y37="-7.00249" y38="-6.45498" y39="-5.90746" x50="212.02" x51="212.264" x52="212.516" x10="210.884" x11="210.703" x12="210.534" x13="210.374" x14="210.226" x15="210.088" y40="-5.35854" x16="209.959" y41="-4.80962" x17="209.842" y42="-4.26211" style="line-style:normal;line-weight:thin;filling:none;color:black" x18="209.735" y43="-3.7146" x19="209.639" y44="-3.16709" y45="-2.61958" y46="-2.07348" y47="-1.52879" y48="-0.985509" y49="-0.443643" x20="209.554" x21="209.48" x22="209.417" x23="209.364" x24="209.323" x25="209.292" x26="209.272" y50="0.096811" x27="209.264" y51="0.635857" x28="209.264" y52="1.17208" x29="209.277" y10="-20.6945" y11="-20.2514" y12="-19.8013" y13="-19.3441" y14="-18.8826" y15="-18.4127" y16="-17.9386" y17="-17.4574" y18="-16.9706" y19="-16.4781" x30="209.3" closed="false" x31="209.336" x32="209.381" x33="209.437" x1="212.952" x34="209.505" x2="212.683" x35="209.583" x3="212.423" x36="209.673" x4="212.173" x37="209.772" x38="209.883" x5="211.933" x6="211.703" x39="210.003" x7="211.483" x8="211.273" x9="211.073" y20="-15.9814" y21="-15.4804" y22="-14.9753" y23="-14.4659" y24="-13.9536" y25="-13.4357" antialias="false" y26="-12.915" y27="-12.3915" y28="-11.8638" y29="-11.3332" x40="210.136" x41="210.277" x42="210.431"/>
                                        <polygon x6="53.2456" x7="53.1327" x8="53.0297" closed="false" x9="52.9506" y10="-95.4989" y11="-95.5666" x10="52.8787" y12="-95.6386" x11="52.8152" y13="-95.712" x12="52.7615" y14="-95.7896" x13="52.7165" y15="-95.87" x14="52.68" x15="52.652" y16="-95.9533" x16="52.6335" y1="-95.0121" y2="-95.0487" y3="-95.0897" y4="-95.1362" y5="-95.1884" y6="-95.2449" x1="53.9652" style="line-style:normal;line-weight:thin;filling:none;color:black" y7="-95.3056" antialias="false" y8="-95.3719" x2="53.8001" y9="-95.434" x3="53.6463" x4="53.5024" x5="53.3683"/>
                                        <polygon x43="61.7542" x44="62.1268" y1="-95.9533" x45="62.4923" y2="-96.0422" x46="62.8492" y3="-96.1339" x47="63.1992" y4="-96.227" x48="63.5393" y5="-96.323" y6="-96.4218" y7="-96.522" y8="-96.625" y9="-96.7294" y30="-99.4712" y31="-99.6123" y32="-99.752" y33="-99.8875" y34="-100.055" y35="-100.216" y36="-100.369" y37="-100.513" y38="-100.647" y39="-100.772" x10="52.8812" x11="52.9546" x12="53.0378" x13="53.1295" x14="53.241" x15="53.361" y40="-100.888" x16="53.4908" y41="-100.981" x17="53.6319" y42="-101.066" style="line-style:normal;line-weight:thin;filling:none;color:black" x18="53.7814" y43="-101.141" x19="53.9395" y44="-101.207" y45="-101.265" y46="-101.313" y47="-101.352" y48="-101.383" x20="54.1074" x21="54.2852" x22="54.4701" x23="54.6648" x24="54.868" x25="55.1263" x26="55.3943" x27="55.6737" x28="55.9616" x29="56.2579" y10="-96.8366" y11="-96.9453" y12="-97.0554" y13="-97.1683" y14="-97.291" y15="-97.4166" y16="-97.5422" y17="-97.6678" y18="-97.7962" y19="-97.9232" closed="false" x30="56.5627" x31="56.876" x32="57.1964" x33="57.5237" x1="52.6331" x34="57.9513" x2="52.6231" x35="58.3859" x3="52.6231" x36="58.8248" x4="52.6316" x37="59.2678" x5="52.6501" x38="59.7123" x6="52.6781" x39="60.1583" x7="52.7146" x8="52.7612" x9="52.8162" y20="-98.0516" y21="-98.18" y22="-98.3084" y23="-98.4368" y24="-98.5653" y25="-98.7219" antialias="false" y26="-98.8757" y27="-99.0281" y28="-99.1777" y29="-99.3258" x40="60.6042" x41="60.9922" x42="61.376"/>
                                        <polygon x6="139.196" x7="138.529" x8="137.86" closed="false" x9="137.188" y10="-89.623" y11="-89.9278" x10="136.515" y12="-90.2199" x11="135.839" y13="-90.5022" x12="135.161" y14="-90.7731" x13="134.482" x14="133.8" y1="-86.4156" y2="-86.8135" y3="-87.2002" y4="-87.5783" y5="-87.9452" y6="-88.3022" x1="142.488" style="line-style:normal;line-weight:thin;filling:none;color:black" y7="-88.648" antialias="false" x2="141.835" y8="-88.9838" y9="-89.3084" x3="141.18" x4="140.521" x5="139.86"/>
                                        <polygon x43="140.624" x44="141.266" y1="-93.5967" x45="141.907" y2="-93.6729" x46="142.545" y3="-93.7364" y4="-93.7915" y5="-93.8352" y6="-93.8677" y7="-93.8903" y8="-93.903" y9="-93.9045" y30="-91.4929" y31="-91.2559" y32="-91.0089" y33="-90.7507" y34="-90.4826" y35="-90.2046" y36="-89.9153" y37="-89.6147" y38="-89.3057" y39="-88.9854" x10="119.231" x11="119.849" x12="120.469" x13="121.092" x14="121.717" x15="122.345" y40="-88.6552" x16="122.974" y41="-88.3151" x17="123.605" y42="-87.9651" style="line-style:normal;line-weight:thin;filling:none;color:black" x18="124.237" y43="-87.6053" x19="124.871" y44="-87.2342" y45="-86.8546" y46="-86.4651" x20="125.507" x21="126.144" x22="126.781" x23="127.421" x24="128.061" x25="128.73" x26="129.4" x27="130.069" x28="130.738" x29="131.407" y10="-93.8961" y11="-93.8777" y12="-93.8481" y13="-93.8086" y14="-93.7578" y15="-93.6971" y16="-93.6265" y17="-93.5447" y18="-93.453" y19="-93.3514" closed="false" x30="132.074" x31="132.741" x32="133.407" x33="134.07" x1="113.791" x34="134.733" x2="114.382" x35="135.395" x3="114.977" x36="136.055" x4="115.576" x37="136.714" x5="116.178" x38="137.372" x6="116.782" x39="138.027" x7="117.39" x8="118.001" x9="118.614" y20="-93.2385" y21="-93.1157" y22="-92.9831" y23="-92.8391" y24="-92.6853" y25="-92.5146" antialias="false" y26="-92.3311" y27="-92.1378" y28="-91.9332" y29="-91.7187" x40="138.678" x41="139.329" x42="139.978"/>
                                        <polygon x43="141.604" x44="142.247" y1="-94.4462" x45="142.888" y2="-94.521" x46="143.526" y3="-94.5859" y4="-94.6395" y5="-94.6833" y6="-94.7172" y7="-94.7398" y8="-94.751" y9="-94.7537" y30="-92.3407" y31="-92.1036" y32="-91.8567" y33="-91.5999" y34="-91.3317" y35="-91.0523" y36="-90.7631" y37="-90.4639" y38="-90.1535" y39="-89.8346" x10="120.21" x11="120.828" x12="121.449" x13="122.073" x14="122.698" x15="123.324" y40="-89.5044" x16="123.953" y41="-89.1643" x17="124.584" y42="-88.8129" style="line-style:normal;line-weight:thin;filling:none;color:black" x18="125.216" y43="-88.4531" x19="125.851" y44="-88.0834" y45="-87.7024" y46="-87.3129" x20="126.486" x21="127.124" x22="127.762" x23="128.401" x24="129.041" x25="129.711" x26="130.38" x27="131.05" x28="131.719" x29="132.386" y10="-94.7452" y11="-94.7255" y12="-94.6958" y13="-94.6563" y14="-94.6055" y15="-94.5463" y16="-94.4743" y17="-94.3939" y18="-94.3021" y19="-94.1991" closed="false" x30="133.054" x31="133.72" x32="134.386" x33="135.05" x1="114.77" x34="135.714" x2="115.363" x35="136.376" x3="115.957" x36="137.036" x4="116.556" x37="137.695" x5="117.158" x38="138.351" x6="117.763" x39="139.006" x7="118.37" x8="118.981" x9="119.595" y20="-94.0876" y21="-93.9649" y22="-93.8308" y23="-93.6883" y24="-93.5345" y25="-93.3623" antialias="false" y26="-93.1803" y27="-92.987" y28="-92.7824" y29="-92.5665" x40="139.659" x41="140.31" x42="140.957"/>
                                        <polygon closed="false" antialias="false" y1="-31.3554" y2="-30.7317" style="line-style:normal;line-weight:thin;filling:none;color:black" y3="-30.1038" y4="-29.4744" x1="47.4135" x2="47.3738" y5="-28.8423" x3="47.3415" x4="47.3161" x5="47.2992"/>
                                        <polygon y15="-82.0115" closed="false" y16="-82.1371" y17="-82.2655" y18="-82.3954" x20="56.0424" y19="-82.528" x21="56.0154" x1="57.9812" x2="57.8557" x3="57.7287" x4="57.6017" x5="57.4761" x6="57.3505" x7="57.2277" x8="57.1064" x9="56.9695" y20="-82.6592" y21="-82.7919" style="line-style:normal;line-weight:thin;filling:none;color:black" antialias="false" x10="56.8382" x11="56.7127" x12="56.5955" x13="56.4869" x14="56.3867" x15="56.3077" x16="56.2385" x17="56.1764" x18="56.1228" x19="56.0778" y1="-80.8473" y2="-80.8657" y3="-80.8953" y4="-80.9334" y5="-80.98" y6="-81.0379" y7="-81.1028" y8="-81.1762" y9="-81.2735" y10="-81.3794" y11="-81.4951" y12="-81.6178" y13="-81.7505" y14="-81.8888"/>
                                        <polygon x6="65.4742" x7="65.7028" x8="65.9216" closed="false" y1="-101.431" y2="-101.45" y3="-101.459" y4="-101.465" y5="-101.462" y6="-101.454" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="64.1873" y7="-101.437" antialias="false" x2="64.4625" y8="-101.416" x3="64.7292" x4="64.9874" x5="65.2358"/>
                                        <polygon y15="-100.132" closed="false" y16="-100.026" y17="-99.9171" y18="-99.8056" x1="65.9216" x2="66.1163" x3="66.3012" x4="66.4761" x5="66.6412" x6="66.795" x7="66.939" x8="67.0716" x9="67.193" style="line-style:normal;line-weight:thin;filling:none;color:black" antialias="false" x10="67.2932" x11="67.3821" x12="67.4625" x13="67.5345" x14="67.5951" x15="67.6475" x16="67.6914" x17="67.7237" x18="67.7475" y1="-101.416" y2="-101.344" y3="-101.268" y4="-101.189" y5="-101.104" y6="-101.015" y7="-100.922" y8="-100.824" y9="-100.724" y10="-100.631" y11="-100.537" y12="-100.439" y13="-100.339" y14="-100.236"/>
                                        <polygon x6="66.5156" x7="66.3872" x8="66.2659" closed="false" x9="66.1488" y1="-96.8084" y2="-96.8183" y3="-96.8183" y4="-96.8113" y5="-96.7971" y6="-96.7746" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="67.1464" y7="-96.7449" antialias="false" x2="67.0293" y8="-96.7096" y9="-96.6673" x3="66.9051" x4="66.7767" x5="66.6455"/>
                                        <polygon x6="68.566" x7="68.611" x8="68.6491" closed="false" x9="68.6771" y10="-96.4628" y11="-96.4247" x10="68.6967" x11="68.7078" y1="-96.6871" y2="-96.6758" y3="-96.6603" y4="-96.6419" y5="-96.6193" y6="-96.5939" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="68.233" y7="-96.5657" antialias="false" x2="68.312" y8="-96.5333" y9="-96.4994" x3="68.3854" x4="68.4517" x5="68.5124"/>
                                        <polygon x6="68.6259" x7="68.581" closed="false" antialias="false" y1="-96.4246" y2="-96.3837" style="line-style:normal;line-weight:thin;filling:none;color:black" y3="-96.3414" y4="-96.299" x1="68.7085" x2="68.7138" y5="-96.2553" x3="68.7053" y6="-96.2115" x4="68.6884" y7="-96.1692" x5="68.6614"/>
                                        <polygon x6="63.9381" x7="63.9873" x8="64.0465" closed="false" x9="64.1143" y10="-95.8602" y11="-95.9068" x10="64.189" y12="-95.9519" x11="64.2737" y13="-95.9943" x12="64.364" x13="64.4628" y1="-95.3973" y2="-95.4481" y3="-95.4989" y4="-95.5511" y5="-95.6034" y6="-95.657" x1="63.8486" style="line-style:normal;line-weight:thin;filling:none;color:black" y7="-95.7092" antialias="false" x2="63.8433" y8="-95.7614" y9="-95.8122" x3="63.8518" x4="63.8703" x5="63.8984"/>
                                        <polygon x6="64.0406" x7="63.9882" x8="63.9442" closed="false" x9="63.9088" y10="-95.3126" y11="-95.3549" x10="63.8807" y12="-95.3973" x11="63.8596" x12="63.8485" y1="-95.0459" y2="-95.0614" y3="-95.0812" y4="-95.1066" y5="-95.1362" y6="-95.1701" x1="64.4879" style="line-style:normal;line-weight:thin;filling:none;color:black" y7="-95.2025" antialias="false" x2="64.382" y8="-95.2378" y9="-95.2745" x3="64.2833" x4="64.193" x5="64.1125"/>
                                        <polygon x6="67.121" x7="66.9841" x8="66.8402" closed="false" x9="66.6906" y10="-94.8936" y11="-94.8766" x10="66.5382" y12="-94.8696" x11="66.3872" y13="-94.8712" x12="66.2377" y14="-94.8811" x13="66.0951" x14="65.9583" y1="-95.2774" y2="-95.2251" y3="-95.1743" y4="-95.1263" y5="-95.0798" y6="-95.0374" x1="67.55" style="line-style:normal;line-weight:thin;filling:none;color:black" y7="-94.9909" antialias="false" x2="67.4823" y8="-94.95" y9="-94.9175" x3="67.4046" x4="67.3186" x5="67.224"/>
                                        <polygon x6="61.0575" closed="false" antialias="false" y1="-82.5999" y2="-82.8808" style="line-style:normal;line-weight:thin;filling:none;color:black" y3="-83.1517" y4="-83.4142" x1="60.0457" x2="60.2418" y5="-83.6682" x3="60.4394" y6="-83.9123" x4="60.6426" x5="60.8486"/>
                                        <polygon y1="-99.8056" y2="-99.6927" y3="-99.577" y4="-99.4599" y5="-99.3428" y6="-99.2242" y7="-99.1057" y8="-98.9858" y9="-98.8644" y30="-96.2863" y31="-96.1833" y32="-96.0845" y33="-95.9914" y34="-95.9025" y35="-95.7995" y36="-95.7049" y37="-95.6189" y38="-95.5427" y39="-95.4749" x10="67.518" x11="67.4433" x12="67.3586" x13="67.2655" x14="67.1525" x15="67.0284" y40="-95.4171" x16="66.8943" y41="-95.3677" x17="66.749" y42="-95.3282" style="line-style:normal;line-weight:thin;filling:none;color:black" x18="66.5952" x19="66.4301" x20="66.2565" x21="66.073" x22="65.8797" x23="65.678" x24="65.4663" x25="65.225" x26="64.9752" x27="64.7156" x28="64.4489" x29="64.1737" y10="-98.7431" y11="-98.6217" y12="-98.5003" y13="-98.379" y14="-98.2463" y15="-98.1151" y16="-97.9839" y17="-97.8541" y18="-97.7256" y19="-97.5986" closed="false" x30="63.8915" x31="63.6022" x32="63.3073" x33="63.0053" x1="67.7475" x34="62.6977" x2="67.7618" x35="62.3082" x3="67.7671" x36="61.9131" x4="67.7602" x37="61.5137" x5="67.7449" x38="61.1116" x6="67.7195" x39="60.7066" x7="67.683" x8="67.638" x9="67.583" y20="-97.4731" y21="-97.3489" y22="-97.2275" y23="-97.1076" y24="-96.989" y25="-96.862" antialias="false" y26="-96.7393" y27="-96.6207" y28="-96.505" y29="-96.3936" x40="60.3016" x41="59.8952" x42="59.4902"/>
                                        <polygon y15="-83.0823" closed="false" y16="-83.0273" y17="-82.9624" y18="-82.8862" x20="58.7545" y19="-82.8001" x21="58.9479" x22="59.1454" x23="59.3472" x24="59.5518" x25="59.7607" x26="59.9737" x27="60.191" x1="56.0254" x2="56.1186" x3="56.2188" x4="56.3232" x5="56.4347" x6="56.5518" x7="56.6746" x8="56.803" x9="56.937" y20="-82.7027" y21="-82.5955" y22="-82.4784" y23="-82.3514" y24="-82.2145" style="line-style:normal;line-weight:thin;filling:none;color:black" antialias="false" y25="-82.0663" y26="-81.9097" y27="-81.7418" x10="57.0767" x11="57.2207" x12="57.3716" x13="57.5283" x14="57.6891" x15="57.8542" x16="58.0264" x17="58.2014" x18="58.382" x19="58.5654" y1="-82.7326" y2="-82.8271" y3="-82.9104" y4="-82.9824" y5="-83.0444" y6="-83.0967" y7="-83.1376" y8="-83.1686" y9="-83.1884" y10="-83.1968" y11="-83.1953" y12="-83.1826" y13="-83.16" y14="-83.1261"/>
                                        <polygon y15="-12.1646" closed="false" y16="-11.7229" y17="-11.4294" y18="-10.9892" x20="1.67075" y19="-10.5475" x21="1.00898" x22="0.215913" x23="-0.445915" x24="-0.975029" x25="-1.24035" x1="2.33258" x2="1.93608" x3="1.53814" x4="0.876313" x5="0.347147" x6="-0.18202" x7="-0.578525" x8="-0.975029" x9="-1.10769" y20="-10.254" y21="-10.1072" y22="-10.1072" y23="-10.254" y24="-10.5475" style="line-style:normal;line-weight:thin;filling:none;color:black" antialias="false" y25="-10.841" x10="-1.10769" x11="-0.975029" x12="-0.578525" x13="1.67075" x14="2.06731" x15="2.33258" x16="2.46524" x17="2.46524" x18="2.33258" x19="2.06731" y1="-15.3989" y2="-15.6924" y3="-15.8391" y4="-15.9859" y5="-15.9859" y6="-15.8391" y7="-15.6924" y8="-15.3989" y9="-14.9572" y10="-14.6637" y11="-14.222" y12="-13.9285" y13="-12.8998" y14="-12.6049"/>
                                        <polygon closed="false" antialias="false" y1="-15.9859" y2="-15.9859" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="5.90408" x2="7.75691"/>
                                        <polygon closed="false" antialias="false" y1="-15.9859" y2="-15.9859" style="line-style:normal;line-weight:thin;filling:none;color:black" y3="-10.1072" x1="4.05274" x2="5.90408" x3="5.90408"/>
                                        <polygon closed="false" antialias="false" y1="-10.1072" y2="-15.9859" style="line-style:normal;line-weight:thin;filling:none;color:black" y3="-12.753" y4="-15.9859" x1="9.34441" x2="9.34441" y5="-10.1072" x3="11.1958" x4="13.0486" x5="13.0486"/>
                                        <polygon closed="false" antialias="false" y1="-13.3401" y2="-13.3401" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="17.8111" x2="14.6361"/>
                                        <polygon closed="false" antialias="false" y1="-15.9859" y2="-15.9859" style="line-style:normal;line-weight:thin;filling:none;color:black" y3="-13.0466" y4="-10.1072" x1="18.3402" x2="14.6361" y5="-10.1072" x3="14.6361" x4="14.6361" x5="18.3402"/>
                                        <polygon y15="-10.1072" closed="false" y16="-10.1072" y17="-10.254" y18="-10.5475" x20="24.1611" y19="-10.9892" x21="24.1611" x22="24.2937" x23="24.559" x24="25.0882" x25="26.543" x1="24.1611" x2="24.2937" x3="24.559" x4="24.9555" x5="25.352" x6="26.1465" x7="26.543" x8="26.9395" x9="27.2048" y20="-11.5762" y21="-12.1646" y22="-13.3401" y23="-13.9285" y24="-14.6637" style="line-style:normal;line-weight:thin;filling:none;color:black" antialias="false" y25="-15.9859" x10="27.3374" x11="27.3374" x12="27.2048" x13="26.9395" x14="26.543" x15="26.1465" x16="25.352" x17="24.9555" x18="24.559" x19="24.2937" y1="-12.1646" y2="-12.753" y3="-13.1933" y4="-13.4882" y5="-13.635" y6="-13.635" y7="-13.4882" y8="-13.1933" y9="-12.753" y10="-12.1646" y11="-11.5762" y12="-10.9892" y13="-10.5475" y14="-10.254"/>
                                        <polygon closed="false" antialias="false" y1="-15.9859" y2="-10.1072" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="36.8624" x2="36.8624"/>
                                        <polygon closed="false" antialias="false" y1="-13.3401" y2="-13.3401" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="33.1583" x2="36.8624"/>
                                        <polygon closed="false" antialias="false" y1="-15.9859" y2="-13.0466" style="line-style:normal;line-weight:thin;filling:none;color:black" y3="-10.1072" x1="33.1583" x2="33.1583" x3="33.1583"/>
                                        <polygon closed="false" antialias="false" y1="-15.9859" y2="-10.1072" style="line-style:normal;line-weight:thin;filling:none;color:black" y3="-15.9859" x1="38.4499" x2="40.3028" x3="42.1541"/>
                                        <polygon closed="false" antialias="false" y1="-2.93935" y2="-2.93935" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="-0.578578" x2="0.523518"/>
                                        <polygon y15="-1.22485" closed="false" y16="-0.735192" y17="-0.366892" y18="-0.122767" x20="-1.24035" y19="0" x1="-1.24035" x2="0.413451" x3="0.965213" x4="1.29541" x5="1.40548" x6="1.40548" x7="1.29541" x8="1.07528" x9="0.853718" y20="0" style="line-style:normal;line-weight:thin;filling:none;color:black" antialias="false" x10="0.523518" x11="0.965213" x12="1.18535" x13="1.29541" x14="1.40548" x15="1.40548" x16="1.29541" x17="1.07528" x18="0.743651" x19="0.413451" y1="-4.89938" y2="-4.89938" y3="-4.77661" y4="-4.53249" y5="-4.16419" y6="-3.7973" y7="-3.429" y8="-3.18488" y9="-3.06211" y10="-2.93935" y11="-2.81658" y12="-2.57245" y13="-2.32692" y14="-1.83727"/>
                                        <polygon y15="-4.28695" closed="false" y16="-4.53249" y17="-4.77661" y18="-4.89938" x20="4.49296" y19="-4.89938" x21="4.82316" x22="5.04329" x23="5.26485" x24="5.37492" x25="5.37492" x1="5.37492" x2="5.26485" x3="5.04329" x4="4.82316" x5="4.49296" x6="4.16138" x7="3.94125" x8="3.61105" x9="3.27942" y20="-4.77661" y21="-4.53249" y22="-4.28695" y23="-3.7973" y24="-3.06211" style="line-style:normal;line-weight:thin;filling:none;color:black" antialias="false" y25="-1.83727" x10="3.05928" x11="2.83915" x12="2.72908" x13="2.72908" x14="2.83915" x15="3.05928" x16="3.27942" x17="3.61105" x18="3.94125" x19="4.16138" y1="-1.83727" y2="-1.10208" y3="-0.612426" y4="-0.366892" y5="-0.122767" y6="1.137e-13" y7="1.137e-13" y8="-0.122767" y9="-0.366892" y10="-0.612426" y11="-1.10208" y12="-1.83727" y13="-3.06211" y14="-3.7973"/>
                                        <polygon closed="false" antialias="false" y1="-2.93935" y2="-2.93935" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="7.35892" x2="8.46102"/>
                                        <polygon y15="-1.22485" closed="false" y16="-0.735192" y17="-0.366892" y18="-0.122767" x20="6.69715" y19="0" x1="6.69715" x2="8.35095" x3="8.90271" x4="9.23291" x5="9.34298" x6="9.34298" x7="9.23291" x8="9.01278" x9="8.79265" y20="0" style="line-style:normal;line-weight:thin;filling:none;color:black" antialias="false" x10="8.46102" x11="8.90271" x12="9.12285" x13="9.23291" x14="9.34298" x15="9.34298" x16="9.23291" x17="9.01278" x18="8.68258" x19="8.35095" y1="-4.89938" y2="-4.89938" y3="-4.77661" y4="-4.53249" y5="-4.16419" y6="-3.7973" y7="-3.429" y8="-3.18488" y9="-3.06211" y10="-2.93935" y11="-2.81658" y12="-2.57245" y13="-2.32692" y14="-1.83727"/>
                                        <polygon x6="13.2024" x7="13.3124" x8="13.3124" closed="false" x9="13.2024" y10="-0.366892" y11="-0.122767" x10="12.9822" y12="5.68e-14" x11="12.6506" y13="5.68e-14" x12="12.3204" x13="10.6666" y1="-4.89938" y2="-4.89938" y3="-2.93935" y4="-2.93935" y5="-2.81658" y6="-2.44969" x1="13.0923" style="line-style:normal;line-weight:thin;filling:none;color:black" y7="-1.96003" antialias="false" x2="10.6666" y8="-1.22485" y9="-0.735192" x3="10.6666" x4="12.3204" x5="12.8722"/>
                                        <polygon y15="1.137e-13" closed="false" y16="1.137e-13" y17="-0.122767" y18="-0.366892" x20="14.636" y19="-0.735192" x21="14.636" x22="14.7461" x23="14.9662" x24="15.4079" x25="16.6201" x1="14.636" x2="14.7461" x3="14.9662" x4="15.2964" x5="15.6281" x6="16.2899" x7="16.6201" x8="16.9503" x9="17.1718" y20="-1.22485" y21="-1.7145" y22="-2.69522" y23="-3.18488" y24="-3.7973" style="line-style:normal;line-weight:thin;filling:none;color:black" antialias="false" y25="-4.89938" x10="17.2819" x11="17.2819" x12="17.1718" x13="16.9503" x14="16.6201" x15="16.2899" x16="15.6281" x17="15.2964" x18="14.9662" x19="14.7461" y1="-1.7145" y2="-2.20415" y3="-2.57245" y4="-2.81658" y5="-2.93935" y6="-2.93935" y7="-2.81658" y8="-2.57245" y9="-2.20415" y10="-1.7145" y11="-1.22485" y12="-0.735192" y13="-0.366892" y14="-0.122767"/>
                                        <polygon y15="-4.16419" closed="false" y16="-3.67453" y17="-2.81658" y18="-2.20415" x20="20.6996" y19="-1.7145" x21="19.9277" x22="18.9357" x1="21.1399" x2="19.5961" x3="19.2659" x4="18.9357" x5="18.7142" x6="18.6041" x7="18.6041" x8="18.7142" x9="18.9357" y20="-1.22485" y21="-0.489659" y22="0" style="line-style:normal;line-weight:thin;filling:none;color:black" antialias="false" x10="19.2659" x11="19.5961" x12="20.2579" x13="20.5895" x14="20.9197" x15="21.1399" x16="21.2499" x17="21.2499" x18="21.1399" x19="21.0298" y1="-2.20415" y2="-2.20415" y3="-2.32692" y4="-2.57245" y5="-2.93935" y6="-3.429" y7="-3.67453" y8="-4.16419" y9="-4.53249" y10="-4.77661" y11="-4.89938" y12="-4.89938" y13="-4.77661" y14="-4.53249"/>
                                        <polygon closed="false" antialias="false" y1="-2.93935" y2="-2.93935" style="line-style:normal;line-weight:thin;filling:none;color:black" x1="23.2353" x2="24.3374"/>
                                        <polygon y15="-1.22485" closed="false" y16="-0.735192" y17="-0.366892" y18="-0.122767" x20="22.5735" y19="0" x1="22.5735" x2="24.2274" x3="24.7791" x4="25.1093" x5="25.2194" x6="25.2194" x7="25.1093" x8="24.8892" x9="24.6676" y20="0" style="line-style:normal;line-weight:thin;filling:none;color:black" antialias="false" x10="24.3374" x11="24.7791" x12="24.9992" x13="25.1093" x14="25.2194" x15="25.2194" x16="25.1093" x17="24.8892" x18="24.5576" x19="24.2274" y1="-4.89938" y2="-4.89938" y3="-4.77661" y4="-4.53249" y5="-4.16419" y6="-3.7973" y7="-3.429" y8="-3.18488" y9="-3.06211" y10="-2.93935" y11="-2.81658" y12="-2.57245" y13="-2.32692" y14="-1.83727"/>
                                        <circle x="281" y="-18" antialias="false" style="line-style:normal;line-weight:normal;filling:black;color:black" diameter="4"/>
                                        <circle x="250" y="-20" antialias="false" style="line-style:normal;line-weight:normal;filling:none;color:black" diameter="8"/>
                                        <line end1="none" end2="none" antialias="false" y1="-36" y2="-27" style="line-style:normal;line-weight:normal;filling:none;color:black" length1="1.5" x1="318" x2="305" length2="1.5"/>
                                        <line end1="none" end2="none" antialias="false" y1="-16" y2="-16" style="line-style:normal;line-weight:normal;filling:none;color:black" length1="1.5" x1="258" x2="270" length2="1.5"/>
                                        <line end1="none" end2="none" antialias="false" y1="-16" y2="-16" style="line-style:normal;line-weight:normal;filling:none;color:black" length1="1.5" x1="272" x2="303" length2="1.5"/>
                                        <line end1="none" end2="none" antialias="false" y1="-16" y2="-24" style="line-style:normal;line-weight:normal;filling:none;color:black" length1="1.5" x1="303" x2="303" length2="1.5"/>
                                        <line end1="none" end2="none" antialias="false" y1="-24" y2="-16" style="line-style:normal;line-weight:normal;filling:none;color:black" length1="1.5" x1="323" x2="323" length2="1.5"/>
                                        <line end1="none" end2="none" antialias="false" y1="-16" y2="-16" style="line-style:normal;line-weight:normal;filling:none;color:black" length1="1.5" x1="355" x2="367" length2="1.5"/>
                                    </description>
                                </definition>
                            </element>
                            <element name="terminal_1-pol_a_outher.elmt">
                                <definition type="element" link_type="terminal" hotspot_x="9" hotspot_y="11" width="20" height="30" version="0.90">
                                    <uuid uuid="{3a4a8bac-3a17-4dd2-929f-75d802969f35}"/>
                                    <names>
                                        <name lang="de">1-Pol  a-extern</name>
                                    </names>
                                    <kindInformations>
                                        <kindInformation name="type">generic</kindInformation>
                                        <kindInformation name="function">generic</kindInformation>
                                    </kindInformations>
                                    <elementInformations>
                                        <elementInformation name="unity" show="1"/>
                                        <elementInformation name="label" show="1"/>
                                        <elementInformation name="plant" show="1"/>
                                        <elementInformation name="supplier" show="1"/>
                                        <elementInformation name="description" show="1"/>
                                        <elementInformation name="machine_manufacturer_reference" show="1"/>
                                        <elementInformation name="comment" show="1"/>
                                        <elementInformation name="designation" show="1"/>
                                        <elementInformation name="quantity" show="1"/>
                                        <elementInformation name="manufacturer" show="1"/>
                                        <elementInformation name="manufacturer_reference" show="1"/>
                                    </elementInformations>
                                    <informations/>
                                    <description>
                                        <circle x="-2" y="-2" antialias="false" style="line-style:normal;line-weight:normal;filling:black;color:black" diameter="4"/>
                                        <line end1="none" end2="none" y1="2" antialias="false" y2="10" style="line-style:normal;line-weight:normal;filling:none;color:black" x1="0" length1="1.5" x2="0" length2="1.5"/>
                                        <dynamic_text frame="false" Halignment="AlignRight" x="-8" y="-20" z="4" rotation="0" font="Liberation Sans,9,-1,5,50,0,0,0,0,0" text_width="-1" uuid="{72429080-0aa7-40c6-86af-d95be686bd20}" keep_visual_rotation="true" text_from="ElementInfo" Valignment="AlignVCenter">
                                            <text/>
                                            <info_name>label</info_name>
                                        </dynamic_text>
                                        <dynamic_text frame="false" Halignment="AlignLeft" x="0" y="0" z="5" rotation="0" font="Liberation Sans,6,-1,5,50,0,0,0,0,0" text_width="-1" uuid="{915ce65c-8bb7-4d4f-b3cf-296e6d0dd4f6}" keep_visual_rotation="true" text_from="UserText" Valignment="AlignVCenter">
                                            <text>a</text>
                                        </dynamic_text>
                                        <terminal type="Generic" x="3" y="0" name="" uuid="{e06d9d94-b3e7-462f-b01a-5ff92f185976}" orientation="e"/>
                                        <terminal type="Generic" x="-3" y="0" name="" uuid="{90a30f9b-bd88-468b-b0eb-c23df300f06a}" orientation="w"/>
                                        <terminal type="Generic" x="0" y="-3" name="" uuid="{a2aaa095-c6f2-4681-9fd2-f9a028baf7d0}" orientation="n"/>
                                        <terminal type="Outer" x="0" y="10" name="a" uuid="{2e8bcb5d-bf91-4983-9364-dde710a2b7a4}" orientation="s"/>
                                    </description>
                                </definition>
                            </element>
                            <element name="terminal_1-pol_b_inner.elmt">
                                <definition type="element" link_type="terminal" hotspot_x="9" hotspot_y="11" width="20" height="30" version="0.90">
                                    <uuid uuid="{0d9aa0dc-2190-4ce8-bb40-9e96b54b2d5d}"/>
                                    <names>
                                        <name lang="de">1-Pol  b-intern</name>
                                    </names>
                                    <kindInformations>
                                        <kindInformation name="type">generic</kindInformation>
                                        <kindInformation name="function">generic</kindInformation>
                                    </kindInformations>
                                    <elementInformations>
                                        <elementInformation name="unity" show="1"/>
                                        <elementInformation name="label" show="1"/>
                                        <elementInformation name="plant" show="1"/>
                                        <elementInformation name="supplier" show="1"/>
                                        <elementInformation name="description" show="1"/>
                                        <elementInformation name="machine_manufacturer_reference" show="1"/>
                                        <elementInformation name="comment" show="1"/>
                                        <elementInformation name="designation" show="1"/>
                                        <elementInformation name="quantity" show="1"/>
                                        <elementInformation name="manufacturer" show="1"/>
                                        <elementInformation name="manufacturer_reference" show="1"/>
                                    </elementInformations>
                                    <informations/>
                                    <description>
                                        <circle x="-2" y="-2" antialias="false" style="line-style:normal;line-weight:normal;filling:black;color:black" diameter="4"/>
                                        <dynamic_text frame="false" Halignment="AlignRight" x="-10" y="-20" z="2" rotation="0" font="Sans Serif,9,-1,5,50,0,0,0,0,0" text_width="-1" uuid="{b78b45f1-6432-4779-83f2-8d49d95342d2}" keep_visual_rotation="true" text_from="ElementInfo" Valignment="AlignVCenter">
                                            <text/>
                                            <info_name>label</info_name>
                                        </dynamic_text>
                                        <line end1="none" end2="none" y1="1" antialias="false" y2="10" style="line-style:normal;line-weight:normal;filling:none;color:black" x1="0" length1="1.5" x2="0" length2="1.5"/>
                                        <dynamic_text frame="false" Halignment="AlignLeft" x="0" y="0" z="4" rotation="0" font="Liberation Sans,6,-1,5,50,0,0,0,0,0" text_width="-1" uuid="{a16bc41a-69d1-4e47-bf75-41026f9289d7}" keep_visual_rotation="true" text_from="UserText" Valignment="AlignVCenter">
                                            <text>b</text>
                                        </dynamic_text>
                                        <terminal type="Generic" x="0" y="-3" name="" uuid="{1d614941-f577-415c-8388-caf06e7ac165}" orientation="n"/>
                                        <terminal type="Inner" x="0" y="10" name="b" uuid="{6f181193-8b52-4137-bbbd-3ca6c8c53630}" orientation="s"/>
                                        <terminal type="Generic" x="3" y="0" name="" uuid="{2d26dfad-56dc-4c77-81d5-abbd4df8f354}" orientation="e"/>
                                        <terminal type="Generic" x="-3" y="0" name="" uuid="{ed726f6a-7912-4ca6-abed-783928acbd8d}" orientation="w"/>
                                    </description>
                                </definition>
                            </element>
                            <element name="terminal_1-pol_c_outher.elmt">
                                <definition type="element" link_type="terminal" hotspot_x="9" hotspot_y="11" width="20" height="30" version="0.90">
                                    <uuid uuid="{829b431b-543f-49c3-b1bf-9524e2244262}"/>
                                    <names>
                                        <name lang="de">1-Pol  c-extern</name>
                                    </names>
                                    <kindInformations>
                                        <kindInformation name="type">generic</kindInformation>
                                        <kindInformation name="function">generic</kindInformation>
                                    </kindInformations>
                                    <elementInformations>
                                        <elementInformation name="unity" show="1"/>
                                        <elementInformation name="label" show="1"/>
                                        <elementInformation name="plant" show="1"/>
                                        <elementInformation name="supplier" show="1"/>
                                        <elementInformation name="description" show="1"/>
                                        <elementInformation name="machine_manufacturer_reference" show="1"/>
                                        <elementInformation name="comment" show="1"/>
                                        <elementInformation name="designation" show="1"/>
                                        <elementInformation name="quantity" show="1"/>
                                        <elementInformation name="manufacturer" show="1"/>
                                        <elementInformation name="manufacturer_reference" show="1"/>
                                    </elementInformations>
                                    <informations/>
                                    <description>
                                        <circle x="-2" y="-2" antialias="false" style="line-style:normal;line-weight:normal;filling:black;color:black" diameter="4"/>
                                        <dynamic_text frame="false" Halignment="AlignRight" x="-10" y="-20" z="2" rotation="0" font="Sans Serif,9,-1,5,50,0,0,0,0,0" text_width="-1" uuid="{b78b45f1-6432-4779-83f2-8d49d95342d2}" keep_visual_rotation="true" text_from="ElementInfo" Valignment="AlignVCenter">
                                            <text/>
                                            <info_name>label</info_name>
                                        </dynamic_text>
                                        <line end1="none" end2="none" y1="0" antialias="false" y2="10" style="line-style:normal;line-weight:normal;filling:none;color:black" x1="0" length1="1.5" x2="0" length2="1.5"/>
                                        <dynamic_text frame="false" Halignment="AlignLeft" x="0" y="0" z="4" rotation="0" font="Liberation Sans,5,-1,5,50,0,0,0,0,0" text_width="-1" uuid="{faf6a463-ae8d-4ff8-a3f6-82131875de13}" keep_visual_rotation="true" text_from="UserText" Valignment="AlignVCenter">
                                            <text>c</text>
                                        </dynamic_text>
                                        <terminal type="Generic" x="-3" y="0" name="" uuid="{ef14732f-aa95-4f47-9a8a-a1612dea3289}" orientation="w"/>
                                        <terminal type="Generic" x="0" y="-3" name="" uuid="{7145c0f6-76fe-4e52-bc0d-3ce36794a8f0}" orientation="n"/>
                                        <terminal type="Outer" x="0" y="10" name="c" uuid="{68d4d782-b0ec-4190-911c-cfe8bc4e1e8f}" orientation="s"/>
                                        <terminal type="Generic" x="3" y="0" name="" uuid="{79790f6c-b6d9-48e1-816e-335af8ac6f8b}" orientation="e"/>
                                    </description>
                                </definition>
                            </element>
                            <element name="terminal_1-pol_d_inner.elmt">
                                <definition type="element" link_type="terminal" hotspot_x="9" hotspot_y="11" width="20" height="30" version="0.90">
                                    <uuid uuid="{d4ecd8a0-bdf9-4264-9e76-515573ec10d9}"/>
                                    <names>
                                        <name lang="de">1-Pol  d-intern</name>
                                    </names>
                                    <kindInformations>
                                        <kindInformation name="type">generic</kindInformation>
                                        <kindInformation name="function">generic</kindInformation>
                                    </kindInformations>
                                    <elementInformations>
                                        <elementInformation name="unity" show="1"/>
                                        <elementInformation name="label" show="1"/>
                                        <elementInformation name="plant" show="1"/>
                                        <elementInformation name="supplier" show="1"/>
                                        <elementInformation name="description" show="1"/>
                                        <elementInformation name="machine_manufacturer_reference" show="1"/>
                                        <elementInformation name="comment" show="1"/>
                                        <elementInformation name="designation" show="1"/>
                                        <elementInformation name="quantity" show="1"/>
                                        <elementInformation name="manufacturer" show="1"/>
                                        <elementInformation name="manufacturer_reference" show="1"/>
                                    </elementInformations>
                                    <informations/>
                                    <description>
                                        <circle x="-2" y="-2" antialias="false" style="line-style:normal;line-weight:normal;filling:black;color:black" diameter="4"/>
                                        <dynamic_text frame="false" Halignment="AlignRight" x="-10" y="-20" z="2" rotation="0" font="Sans Serif,9,-1,5,50,0,0,0,0,0" text_width="-1" uuid="{b78b45f1-6432-4779-83f2-8d49d95342d2}" keep_visual_rotation="true" text_from="ElementInfo" Valignment="AlignVCenter">
                                            <text/>
                                            <info_name>label</info_name>
                                        </dynamic_text>
                                        <line end1="none" end2="none" y1="2" antialias="false" y2="10" style="line-style:normal;line-weight:normal;filling:none;color:black" x1="0" length1="1.5" x2="0" length2="1.5"/>
                                        <dynamic_text frame="false" Halignment="AlignLeft" x="0" y="0" z="4" rotation="0" font="Liberation Sans,6,-1,5,50,0,0,0,0,0" text_width="-1" uuid="{11793b74-a733-4a77-9812-f699b56f9480}" keep_visual_rotation="true" text_from="UserText" Valignment="AlignVCenter">
                                            <text>d</text>
                                        </dynamic_text>
                                        <terminal type="Generic" x="3" y="0" name="" uuid="{e469c8f7-3729-4d77-beeb-73c85abaedb1}" orientation="e"/>
                                        <terminal type="Generic" x="-3" y="0" name="" uuid="{6987e802-fdc4-48d2-b555-3817777a17d2}" orientation="w"/>
                                        <terminal type="Inner" x="0" y="10" name="d" uuid="{aa1f3b97-1431-4ede-a9a5-52a6d86afaa4}" orientation="s"/>
                                        <terminal type="Generic" x="0" y="-3" name="" uuid="{4a25d5c6-53a6-4008-845a-a8ce60d491d4}" orientation="n"/>
                                    </description>
                                </definition>
                            </element>
                            <element name="terminal_2-pol-a_inner-b_outher.elmt">
                                <definition type="element" link_type="terminal" hotspot_x="9" hotspot_y="14" width="20" height="30" version="0.100.0">
                                    <uuid uuid="{db1b7c23-41c6-4836-9543-b65268337ecd}"/>
                                    <names>
                                        <name lang="de">2-Pol_a-extern_b-intern</name>
                                    </names>
                                    <kindInformations>
                                        <kindInformation name="type">generic</kindInformation>
                                        <kindInformation name="function">generic</kindInformation>
                                    </kindInformations>
                                    <elementInformations/>
                                    <description>
                                        <circle x="-2" y="-2" antialias="false" style="line-style:normal;line-weight:normal;filling:black;color:black" diameter="4"/>
                                        <dynamic_text frame="false" Halignment="AlignLeft" x="2" y="-22" z="2" rotation="0" font="Sans Serif,9,-1,5,50,0,0,0,0,0" text_width="-1" uuid="{b78b45f1-6432-4779-83f2-8d49d95342d2}" keep_visual_rotation="true" text_from="ElementInfo" Valignment="AlignTop">
                                            <text/>
                                            <info_name>label</info_name>
                                        </dynamic_text>
                                        <dynamic_text frame="false" Halignment="AlignLeft" x="0" y="0" z="4" rotation="0" font="Arial [Mono],6,-1,5,50,0,0,0,0,0,Standard" text_width="-1" uuid="{7a93baf6-5448-4b2f-a9d6-de6180bb4d1d}" keep_visual_rotation="true" text_from="UserText" Valignment="AlignTop">
                                            <text>a</text>
                                        </dynamic_text>
                                        <dynamic_text frame="false" Halignment="AlignLeft" x="0" y="-20" z="4" rotation="0" font="Arial [Mono],6,-1,5,50,0,0,0,0,0,Standard" text_width="-1" uuid="{7a93baf6-5448-4b2f-a9d6-de6180bb4d1d}" keep_visual_rotation="true" text_from="UserText" Valignment="AlignTop">
                                            <text>b</text>
                                        </dynamic_text>
                                        <line end1="none" end2="none" y1="-10" antialias="false" y2="10" style="line-style:normal;line-weight:normal;filling:none;color:black" x1="0" length1="1.5" x2="0" length2="1.5"/>
                                        <terminal type="Inner" x="0" y="-10" name="b" uuid="{60349854-34bb-4723-826b-674458de6882}" orientation="n"/>
                                        <terminal type="Generic" x="3" y="0" name="" uuid="{83682123-64ad-4252-9b4c-b73f271950e7}" orientation="e"/>
                                        <terminal type="Outer" x="0" y="10" name="a" uuid="{f5e8bd83-1662-4d60-905b-3badb7b8e5c3}" orientation="s"/>
                                        <terminal type="Generic" x="-3" y="0" name="" uuid="{c314e97d-d3c6-4aa1-9533-2a95f9821d6c}" orientation="w"/>
                                    </description>
                                </definition>
                            </element>
                            <element name="klemme.elmt">
                                <definition type="element" link_type="terminal" hotspot_x="9" hotspot_y="9" width="20" height="20" version="0.100.0">
                                    <uuid uuid="{9b027ff0-7d36-426f-afea-8d4372eae63e}"/>
                                    <names>
                                        <name lang="de">Klemme ohne Klemmpunkname nur Brücke angeschl.</name>
                                    </names>
                                    <kindInformations>
                                        <kindInformation name="type">generic</kindInformation>
                                        <kindInformation name="function">generic</kindInformation>
                                    </kindInformations>
                                    <elementInformations/>
                                    <description>
                                        <circle x="-2" y="-2" antialias="false" style="line-style:normal;line-weight:normal;filling:black;color:black" diameter="4"/>
                                        <dynamic_text frame="false" Halignment="AlignLeft" x="2" y="-22" font="Sans Serif,9,-1,5,50,0,0,0,0,0" z="2" rotation="0" text_width="-1" uuid="{b78b45f1-6432-4779-83f2-8d49d95342d2}" keep_visual_rotation="true" text_from="ElementInfo" Valignment="AlignTop">
                                            <text/>
                                            <info_name>label</info_name>
                                        </dynamic_text>
                                        <terminal type="Generic" x="0" y="3" name="" uuid="{70c2c274-8819-45ff-909e-1033fa11de12}" orientation="s"/>
                                        <terminal type="Generic" x="3" y="0" name="" uuid="{b19cb5cf-0782-400f-adc2-e742125bbaba}" orientation="e"/>
                                        <terminal type="Generic" x="-3" y="0" name="" uuid="{1be79abd-0adf-48bf-903b-dee0d156e671}" orientation="w"/>
                                        <terminal type="Generic" x="0" y="-3" name="" uuid="{949863c0-c445-4ff6-87dc-c83f4a427cda}" orientation="n"/>
                                    </description>
                                </definition>
                            </element>
                            <element name="klemme_als_verweis.elmt">
                                <definition type="element" link_type="simple" hotspot_x="9" hotspot_y="9" width="20" height="20" version="0.100.0">
                                    <uuid uuid="{723e655d-cb5f-4bd5-8e82-3e14633c1dc5}"/>
                                    <names>
                                        <name lang="de">Klemme als Element für Verweise</name>
                                    </names>
                                    <elementInformations/>
                                    <description>
                                        <circle x="-2" y="-2" antialias="false" style="line-style:normal;line-weight:normal;filling:black;color:black" diameter="4"/>
                                        <dynamic_text frame="false" Halignment="AlignLeft" x="2" y="-22" font="Sans Serif,9,-1,5,50,0,0,0,0,0" z="2" rotation="0" text_width="-1" uuid="{b78b45f1-6432-4779-83f2-8d49d95342d2}" keep_visual_rotation="true" text_from="ElementInfo" Valignment="AlignTop">
                                            <text/>
                                            <info_name>label</info_name>
                                        </dynamic_text>
                                        <terminal type="Generic" x="0" y="-3" name="" uuid="{1f822f9e-7197-4982-acad-1e2bc9d312b9}" orientation="n"/>
                                        <terminal type="Generic" x="-3" y="0" name="" uuid="{344b79c8-5f89-4562-ae86-69babeaf5d07}" orientation="w"/>
                                        <terminal type="Generic" x="0" y="3" name="" uuid="{27779d96-ef17-47d3-9f3e-847bd1ecbc26}" orientation="s"/>
                                        <terminal type="Generic" x="3" y="0" name="" uuid="{7fe8d58e-2bf1-4180-a26d-46e9b1aecbe8}" orientation="e"/>
                                    </description>
                                </definition>
                            </element>
                        </category>
                    </category>
                    """)