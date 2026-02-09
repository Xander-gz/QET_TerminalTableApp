"""
Copyright (C) 2026 xanderhopp; xanderhopp@gmail.com

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, version 3.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
"""


import datetime
import xml.etree.ElementTree as etree


def parsetree(origin_file, give_feedback):
    xmltree = etree.parse(origin_file)
    # give_feedback(_("Reading the file."))

    return xmltree



from TerminalTableApp.sort import sorting_functions as sf
from TerminalTableApp.sort import sql_queries as sq
from TerminalTableApp.sort import terminal_table_classes as cl
from TerminalTableApp.write import table_functions as tf


def create_table(origin_file, cursor, connection, give_feedback):
    xmltree = parsetree(origin_file, give_feedback)

    # funktions
    # -------------------------------------------------------------------------------
    # Take the data to write it into the new file
    # -------------------------------------------------------------------------------


    # category wird nur einmal gebraucht, unabhängig von der Anzahl der Klemmleisten
    # category would be used only once
    eTable = tf.create_category()
    diagram_template = tf.diagram_template(xmltree)
    new_diagram_data = tf.new_diagram(xmltree)


    origin_number_of_pages = cursor.execute("SELECT MAX(order_nr) FROM diagrams").fetchone()[0]
    pagenumber = origin_number_of_pages
    ePage = None
    eTablePart = None

    date = datetime.datetime.now().strftime("%Y%m%d")

    terminal_row_list = sq.terminal_row_list(cursor)

    # ----------------------------------------------------------------------------------------------------------------------
    # set the terminalrow
    # ----------------------------------------------------------------------------------------------------------------------
    for terminal_row_obj in terminal_row_list:

        # Reihenanzahl für die Tabelle ermitteln und klemmenaufbaubezeichnung ermitteln
        # get the number of rows per terminal and the terminal-connectionpoints
        terminals_list = sq.terminals_list(cursor, terminal_row_obj, give_feedback)
        print("terminal_row_obj = ",terminal_row_obj)
        print("terminals_list", terminals_list)
        number_of_connectionpoints_per_terminal = sq.number_of_connectionpoints_per_terminal(cursor, terminal_row_obj)
        print("number_of_connectionpoints_per_terminal: ", number_of_connectionpoints_per_terminal)
        rows_per_terminal = sf.rows_per_terminal(number_of_connectionpoints_per_terminal)
        try:
            max_terminals_per_page = int(40/rows_per_terminal[0])
        except:
            give_feedback(_("\nThe lines per terminal could not be calculated!\n") + str(terminal_row_obj[terminal_name]) + _("All connection points (a, b, c, d,...) must be shown once in the plan for each terminal strip.\nIf desired, they can be covered with a white rectangle."))

        connected_cables = sq.connected_cables(cursor, terminal_row_obj)

        terminal_counter = 1
        p = 0
        partcounter = 0
        versatz = 20

    # ----------------------------------------------------------------------------------------------------------------------
    # insert the terminals in the row
    # ----------------------------------------------------------------------------------------------------------------------

        for listed_terminal in terminals_list:
            print("gelistete Klemme: ", listed_terminal)

            # Seiten und Teilabschnitte erstellen
            # create Pages and partial terminalrows
            if terminal_counter == 1:

                pagenumber += 1
                partcounter += 1
                list_of_created_terminals = []
                bridges_at_terminalrow_list = []

                parts = len(terminals_list) // max_terminals_per_page
                if len(terminals_list) % max_terminals_per_page > 0:
                    parts += 1

                # erstellen einer neuen UUID, damit das Klemmenplan-Teilstück als Element später in QET eingeügt werden kann
                # create a new UUID so can the Terminaltable part culd be insertet into QET as an Element
                identstr = tf.create_ident()

                if ePage == None:
                    ePage = tf.create_page(terminal_row_obj, pagenumber, origin_number_of_pages, diagram_template, new_diagram_data, date,
                                           partcounter, identstr)
                else:
                    ePage.append(
                        tf.create_page(terminal_row_obj, pagenumber, origin_number_of_pages, diagram_template, new_diagram_data, date,
                                       partcounter, identstr))
                eTablePart = tf.create_table(terminal_row_obj, partcounter, parts, identstr)


            # Teilabschnitte mit Daten füllen
            # fill the partial terminalstrips with data
            pos = eTablePart.find("definition/description")
            line = tf.create_lines(terminal_counter, rows_per_terminal[0])
            for i in line.iter("line"):
                pos.append(i)


            terminal_obj = sq.data_of_the_terminal(cursor, listed_terminal)
            print("Terminal_obj: ", terminal_obj)
            list_of_connectionpoints =sq.list_of_connectionpoints(cursor, terminal_row_obj)
            terminalnumber = tf.create_terminal(terminal_obj, terminal_counter, rows_per_terminal[0],
                                                list_of_connectionpoints)


            for i in terminalnumber[0].iter("text"):
                pos.append(i)
            list_of_created_terminals.append(terminalnumber[1])

    # ----------------------------------------------------------------------------------------------------------------------
    # set the connectionspoints into the terminals
    # ----------------------------------------------------------------------------------------------------------------------
            conductor_obj = None
            connection_list = sq.connections_per_terminal(cursor, terminal_obj, ["%", "%er"])
            for connection_obj in connection_list:
                print("Klemmpunkt:", connection_obj)
                conductor_obj = sf.search_conductor(cursor, connection_obj)
                if conductor_obj == None:
                    continue


                element_obj = sf.search_element(cursor, connection_obj, conductor_obj, cl, terminal_obj, give_feedback)
                print("Ziehlelement: ", element_obj)







                pos = eTablePart.find("definition/description")
                if connection_obj.eet_type == 'Outer':
                    row = tf.create_row_outer(connection_obj, conductor_obj, element_obj, connected_cables, terminal_counter, rows_per_terminal, sf, give_feedback)
                    for i in row.iter("text"):
                        pos.append(i)
                    row = None
                if connection_obj.eet_type == 'Inner':
                    row = tf.create_row_inner(connection_obj, conductor_obj, element_obj, connected_cables, terminal_counter, rows_per_terminal, sf, give_feedback)
                    for i in row.iter("text"):
                        pos.append(i)
                    row = None
                del (conductor_obj)


            bridge_at_terminal = sf.bridge_at_terminal(cursor, terminal_obj, give_feedback)
            for b in bridge_at_terminal:
                # for t in list_of_created_terminals:
                if b[1] < b[4]:
                    bridges_at_terminalrow_list.append(b,)
                if b[1] > b[4] and b[4] not in list_of_created_terminals:
                    bridges_at_terminalrow_list.append(b,)
            print(bridges_at_terminalrow_list)





                # Mit jeder neuen Klemmenzeile wird x um 40 erhöht, die neue Zeile
                # 40 punkte tiefer gezeichnet. Bei 40 Zeilen ist das Ende der Seite erreicht
                # und eine neue kann beginnen mit neuer Abschnitts-Nummer

                # with every terminal 40 would be addet to the the x
                # the next row would be 40 points deeper than the one befor. If the number of
                # arrives 40, a new page would be createt

            terminal_counter += rows_per_terminal[0]
            if terminal_counter > 38:
                cableListPart = tf.create_cablelist_part(connected_cables)  # Liste mit den verwendeten Kabeln für den Teilabschnitt einfügen
                for i in cableListPart.iter("text"):
                    pos.append(i)
                eTable.insert(2, eTablePart)  # Einfügen der Tabelle in die Datei, neue Tabelle bei

                bridges = sf.search_bridges(bridges_at_terminalrow_list, list_of_created_terminals)
                create_briges = tf.create_terminal_bridge(bridges, len(list_of_created_terminals), terminal_counter, give_feedback)
                for i in create_briges.iter("line"):
                    pos.append(i)
                    del(i)
                # the bridges have to be createt for every page separatly, to start anew, the values must be deleted
                # del bridges_at_terminalrow_list
                # del list_of_created_terminals
                # if create_briges != None:
                #     del create_bridges

                terminal_counter = 1  # überlauf des Blattes


                print("Lister der eingebauten Klemmen: ", list_of_created_terminals)

            # Einfügen der Tabelle, nur wenn der Abschnitt auch Klemmen enthält
            # Insert Table only if there are terminals in the table
        if terminal_counter > 1:
            cableListPart = tf.create_cablelist_part(connected_cables)
            for i in cableListPart.iter("text"):
                pos.append(i)
            bridges = sf.search_bridges(bridges_at_terminalrow_list, list_of_created_terminals)
            create_briges = tf.create_terminal_bridge(bridges, len(list_of_created_terminals), terminal_counter, give_feedback)
            for i in create_briges.iter("line"):
                pos.append(i)
            print("Lister der eingebauten Klemmen: ", list_of_created_terminals)

            eTable.insert(2, eTablePart)
# instert the accessories
    eTable.insert(2, etree.fromstring(tf.eTableaccessories))
    ec = xmltree.find("collection/category")
    ed = xmltree.getroot()

    ec.insert(4, eTable)
    ed.insert(origin_number_of_pages + 3, ePage)

    # --------------------------------------------------------------------------------
    # Übergabe zur Datei ... put fata to file
    # --------------------------------------------------------------------------------
    save_file = origin_file.replace(".qet", "_terminals.qet")
    # save_file = "Test_Terminals.qet"

    etree.indent(xmltree, space='    ', level=0)
    xmltree.write(save_file, encoding='UTF-8', xml_declaration=None, default_namespace=None, method='xml',
                  short_empty_elements=False)

    print("Finished!")

    give_feedback(_("\nFinisch!"))
    give_feedback(_("The file") +" " + save_file + " " + _("is successfully created."))





