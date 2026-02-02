import xml.etree.ElementTree as etree


def read_xml_file(origin_file, cursor, connection, give_feedback):

    def parsetree(origin_file):
        try:
            xmltree = etree.parse(origin_file)
            fback = "Auslesen der Datei"
            feedback = (fback)
            return xmltree
        except:
            fback = "Datei konnt nicht ausgelesen werden!"
            feedback = (fback)


    def collect_diagram_data(root):
        diagram_id_map = {}

        for diagram in xmlroot.findall("diagram"):
            cursor.execute("""
                           INSERT INTO diagrams 
                           (title,
                            order_nr,
                            auto_page_num,
                            folio,
                            plant,
                            locmach,
                            date,
                            author,
                            indexrev,
                            filename,
                            rows,
                            rowsize,
                            cols,
                            colsize,
                            displayrows,
                            displaycols,
                            titleblocktemplate,
                            titleblocktemplateCollection,
                            height,
                            freezeNewConductor,
                            freezeNewElement,
                            displayAt,
                            version)
                            values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
                                   ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                                    ?, ?, ?)""",(
                                diagram.get("title"),
                                diagram.get("order"),
                                diagram.get("auto_page_num"),
                                diagram.get("folio"),
                                diagram.get("plant"),
                                diagram.get("locmach"),
                                diagram.get("date"),
                                diagram.get("autor"),
                                diagram.get("indexrev"),
                                diagram.get("filename"),
                                diagram.get("rows"),
                                diagram.get("rowsize"),
                                diagram.get("cols"),
                                diagram.get("colsize"),
                                diagram.get("displayrows"),
                                diagram.get("displaycols"),
                                diagram.get("titleblocktemplate"),
                                diagram.get("titleblocktemplateCollection"),
                                diagram.get("height"),
                                diagram.get("freezeNewConductor"),
                                diagram.get("freezeNewElement"),
                                diagram.get("displayAt"),
                                diagram.get("version"),
                                ))

            diagram_id = cursor.lastrowid
            diagram_id_map[diagram] = diagram_id

        for diagram in root.findall("diagram"):
            d_id = diagram_id_map[diagram]

            for el in diagram.findall(".//element"):
                el_type = el.get("type").split("/")
                cursor.execute("""
                            INSERT INTO elements (
                            diagram_id, 
                            e_uuid, 
                            e_type, 
                            x, 
                            y, 
                            z)
                            VALUES (?, ?, ?, ?, ?, ?)
                            """, (
                                d_id,
                                el.get("uuid"),
                                el_type[-1],
                                el.get("x"),
                                el.get("y"),
                                el.get("z"),
                            ))


                for t in el.findall(".//terminal"):
                    cursor.execute("""
                                INSERT INTO terminals (
                                    e_uuid, 
                                    terminal_id, 
                                    x, 
                                    y)
                                VALUES (?, ?, ?, ?)
                                """, (
                                    el.get("uuid"),
                                    t.get("id"),
                                    t.get("x"),
                                    t.get("y"),
                                ))


                for info in el.findall(".//elementInformation"):
                # The terminal name and the number wuld be seperatet, the if is because other elements than
                # terminals have only a name an no number. The emty place has to be filled.
                    ei_text2 = "XXX"
                    if info.text:
                        ei_text = (info.text.strip().split(":"))
                        if len(ei_text) < 2:
                            ei_text.append("xxx")
                        else:
                            ei_text2 = ei_text[1]
                        ei_text1 = ei_text[0]
                        cursor.execute("""
                                    INSERT INTO elementinformations (
                                        e_uuid, 
                                        ei_name, 
                                        ei_terminal_row_name,
                                        ei_terminal_nr
                                        )
                                    VALUES (?, ?, ?, ?)
                                    """, (
                                        el.get("uuid"),
                                        info.get("name"),
                                        ei_text1,
                                        ei_text2,
                                    ))


                for p in el.findall(".//element_type"):
                    cursor.execute("""
                                INSERT INTO terminal_types (
                                    e_uuid, 
                                    terminal_function, 
                                    terminal_type, 
                                    terminal_led)
                                VALUES (?, ?, ?, ?)
                                """, (
                                    el.get("uuid"),
                                    p.get("terminal_function"),
                                    p.get("terminal_type"),
                                    p.get("terminal_led"),
                                ))



                for uu in el.findall(".//link_uuid"):
                    cursor.execute("""
                                   INSERT INTO link_uuids (
                                       e_uuid,
                                       l_uuid)
                                   VALUES (?, ?)
                                   """, (
                                       el.get("uuid"),
                                       uu.get("uuid"),
                                   ))


        for co in root.findall(".//conductor"):
            cursor.execute("""
                           INSERT INTO conductors (
                               terminal1,
                               terminalname1,
                               terminal2,
                               terminalname2,
                               element1,
                               element1_name,
                               element1_linked,
                               element1_label,
                               element2,
                               element2_name,
                               element2_linked,
                               element2_label,
                               formula,
                               c_type,
                               bus,
                               num,
                               conductor_section,
                               conductor_color,
                               cable,
                               function,
                               tension_protocol)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                               ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                           """, (
                               co.get("terminal1"),
                               co.get("terminalname1"),
                               co.get("terminal2"),
                               co.get("terminalname2"),
                               co.get("element1"),
                               co.get("element1_name"),
                               co.get("element1_linked"),
                               co.get("element1_label"),
                               co.get("element2"),
                               co.get("element2_name"),
                               co.get("element2_linked"),
                               co.get("element2_label"),
                               co.get("formula"),
                               co.get("type"),
                               co.get("bus"),
                               co.get("num"),
                               co.get("conductor_section"),
                               co.get("conductor_color"),
                               co.get("cable"),
                               co.get("function"),
                               co.get("tension_protocol"),
            ))

        for collection in root.findall("collection"):
            for eel in collection.findall(".//element"):
                eel_name = eel.get("name")

                definition = eel.find("definition")
                if definition is None:
                    continue

                link_type = ""
                link_type = definition.get("link_type")
                definition_type = definition.get("type")
                version = definition.get("version")

                uuid_eelem = definition.find("uuid")
                uuid_eel = uuid_eelem.get("uuid")



                cursor.execute("""
                               INSERT OR IGNORE INTO embedded_elements (
                                       ee_uuid,
                                       ee_name,
                                       ee_link_type,
                                       ee_type,
                                       ee_version
                                   )
                                   VALUES (?, ?, ?, ?, ?)
                                       """,(
                                        uuid_eel,
                                        eel_name,
                                        link_type,
                                        definition_type,
                                        version,
                                    ))


                for ki in eel.findall(".//kindInformation"):

                    cursor.execute("""
                                   INSERT INTO kindInformations (
                                       ee_uuid,
                                       ki_name,
                                       ki_text
                                   )
                                   VALUES (?, ?, ?)
                                   """, (
                                       uuid_eel,
                                       ki.get("name"),
                                       ki.text.strip(),
                                   ))

                for et in eel.findall(".//terminal"):
                    try:
                        cursor.execute("""
                                       INSERT INTO embedded_element_terminals (
                                           eet_uuid,
                                           ee_uuid,
                                           eet_name,
                                           eet_type
                                           )
                                       VALUES (?, ?, ?, ?)
                                       """, (
                                           et.get("uuid"),
                                           uuid_eel,
                                           et.get("name"),
                                           et.get("type"),
                                       ))
                    except:
                        validate = cursor.execute("""SELECT ee_uuid
                                          FROM embedded_element_terminals 
                                          WHERE eet_uuid = (?)""",
                                       (et.get("uuid"),)).fetchone()
                        if validate != uuid_eel:
                            give_feedback(_("Terminal with the same uuid available again?") + " " +
                                          eel_name + " : " + et.get("name"))


        connection.commit()


    def feedback(feedback):
        print(feedback)


    xmltree = parsetree(origin_file)
    xmlroot = xmltree.getroot()
    collect_diagram_data(xmlroot)


