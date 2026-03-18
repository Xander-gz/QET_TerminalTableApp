"""
Copyright (C) 2026 xanderhopp; xanderhopp@gmail.com

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, version 3.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
"""


import TerminalTableApp.sort.sql_queries as sq


def reference(terminal_obj, report):
    print("terminal_obj: ", terminal_obj)
    print("report: ", report)
    alpha = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'] # posible row-names
    reference_x = (int(terminal_obj.x) -25 ) // int(terminal_obj.colsize)+1 # number and size of cols
    reference_y = alpha[(int(terminal_obj.y) -25 ) // int(terminal_obj.rowsize)] # number and size of rows

    foliorev = ""
    placeholder = ""
    for i in report:
        print("Reverence: ", foliorev, "<", i, ">")
        if placeholder == "":
            if i == "%":
                placeholder += i
                continue
            foliorev += i
        else:
            if i == "f":
                foliorev += str(terminal_obj.order_nr)
            if i == "F":
                foliorev += terminal_obj.folio
            if i == "M":
                foliorev += terminal_obj.plant
            if i == "LM":
                foliorev += terminal_obj.location
            if i == "l":
                foliorev += str(reference_y)
            if i == "c":
                foliorev += str(reference_x)

            placeholder = ""


    # reference = "/" + terminal_obj.folio + " ." + str(reference_y) + str(reference_x) # where the element is

    return str(foliorev)


def rows_per_terminal(rows_per_terminal):
# the rows would be used to draw the number of lines that would be neede per Terminal
# inner- and outerlist is needed to select the position of the connectionpoint in the lines of the terminal
    innerlist = []
    outerlist = []
    inner = 0
    outer = 0

    for row in rows_per_terminal:
        if row[0] == "Outer":
            outer += 1
            outerlist.append(row[2])
        if row[0] == "Inner":
            inner += 1
            innerlist.append(row[2])

    if inner > outer:
        rows = inner
    else:
        rows = outer

    return rows, outerlist, innerlist


def search_conductor(cursor, connection_obj):
    conductor_obj = sq.connected_conductor_side1(cursor, connection_obj.eet_uuid, connection_obj.e_uuid,)
    if conductor_obj == None:
        conductor_obj = sq.connected_conductor_side2(cursor, connection_obj.eet_uuid, connection_obj.e_uuid,)
    return conductor_obj


def search_element(cursor, connection_tuple_list, conductor_obj, cl,terminal_obj, give_feedback):
    print("connection_obj: ", connection_tuple_list)
    print("conductor_obj: ", conductor_obj)

    if conductor_obj == None:
        give_feedback(_("No element is connected to a linked page reference? ")
                        + getattr(connection_tuple_list, 'terminal_name') + ":"
                        + getattr(connection_tuple_list, 'ei_terminal_nr')
                        + getattr(connection_tuple_list, 'eet_name') )

    if connection_tuple_list.eet_uuid == conductor_obj.terminal1:
        target_terminal = conductor_obj.terminal2
        target_element = conductor_obj.element2
    else:
        target_terminal = conductor_obj.terminal1
        target_element = conductor_obj.element1
    print("target_terminal: ", target_terminal)
    print("target_element: ", target_element)




    element_type = sq.select_element_type_simple_terminal(cursor, target_element,)
    if element_type != None:
        print("Element Type1: ", element_type)
    if element_type == None or element_type == "master" or element_type == "slave":
        print(target_element)
        element_type = sq.select_element_type_master_slave(cursor, target_terminal,)
    print("element_type2: ", element_type)
    if element_type == "simple" or element_type == "terminal" or element_type == "master":
        connected_element = sq.select_simple_element(cursor, target_element, terminal_obj, give_feedback)
        connected_terminal = sq.select_terminal(cursor, target_terminal)
        connected_element.connectionpoint = connected_terminal[0]



    if element_type == "slave":
        slave_element_list = sq.select_slave_element(cursor, target_element, terminal_obj, give_feedback)
        print("slave_element: ", slave_element_list)
        slave_terminal_list = sq.select_terminal(cursor, target_terminal)
        print("slave_terminal: ", slave_terminal_list)
        slave_master_element_list = sq.select_master_element(cursor, slave_element_list[3],terminal_obj, give_feedback)
        print("master_element: ", slave_master_element_list)
        connected_element = cl.Connected_Element(slave_element_list[0], slave_element_list[1], slave_element_list[2],
                                                 slave_master_element_list[1], slave_terminal_list[0], slave_master_element_list[3],
                                                 slave_master_element_list[5], "", "", "", slave_element_list[5],
                                                 slave_element_list[6], slave_element_list[7], slave_element_list[8], slave_element_list[9],)


    if element_type == "next_report" or element_type == "previous_report":
        # if element is next-, preview-report, it comes with an element_type to recursion
        linked_terminal = sq.next_previous_report_element(cursor, target_element)
        connection_tuple_list.eet_uuid = linked_terminal.terminal
        connection_tuple_list.e_uuid = linked_terminal.element
        linked_conductor = search_conductor(cursor, connection_tuple_list)
        connected_element = search_element(cursor, connection_tuple_list, linked_conductor, cl, terminal_obj,
                                           give_feedback)


    return connected_element


def linked_conductor(cursor, target_element):
    try:
        link = sq.next_previous_report_element(cursor, target_element)
    except:
        return target_element

    if link != None:
        print("oooooooooooooooooooooooooops!")
        # if element is next-, preview-report, it comes with an element_type to recursion
        # if element is next-, preview-report, it comes with an element_type to recursion
        print("Link:", link.terminal, link.element)

        conductor = sq.connected_conductor_side1(cursor, link.terminal, link.element,)
        if conductor != None:
            print("conductor1: ", conductor)
        if conductor == None:
            conductor = sq.connected_conductor_side2(cursor, link.terminal, link.element,)
            print("conductor2: ", conductor)
            target_element = conductor.element1

        else:
            target_element = conductor.element2

        linked_element = linked_conductor(cursor, target_element,)
        return linked_element


def bridge_at_terminal(cursor, terminal_obj, give_feedback):
    connection_list = sq.connections_per_terminal(cursor,terminal_obj, ["", "Generic"])
    list_of_bridge_at_terminal = []
    for connection_obj in connection_list:
        conductor_obj = search_conductor(cursor, connection_obj)
        if conductor_obj == None:
            continue
        else:

            print("conductor_obj für Brücke: ", conductor_obj)
            if conductor_obj.num.startswith("Brücke "):
                print("Treffer Brücke ", conductor_obj.num)
                if connection_obj.eet_uuid == conductor_obj.terminal1:
                    target_element0 = conductor_obj.element2
                    target_terminal0 = conductor_obj.terminal2
                else:
                    target_element0 = conductor_obj.element1
                    target_terminal0 = conductor_obj.terminal1

                # ist ein link vorhanden, muss dieser zuerst aufgelöst werden, wenn nicht pass
                # is there a link, it must be served at first, if not, pass

                print(target_element0)
                target_element = linked_conductor(cursor, target_element0,)
                print(target_element)


                connected_element = sq.select_simple_element(cursor, target_element, terminal_obj, give_feedback)
                where_the_bridge_belongs_to = conductor_obj.num.split(" ")[1]
                print("Brücke von ", terminal_obj.terminal_name, terminal_obj.terminal_nr, "nach ",connected_element.label, connected_element.x_nr)
                list_of_bridge_at_terminal.append([terminal_obj.terminal_name, terminal_obj.terminal_nr, "to",
                                                   connected_element.label, connected_element.x_nr,
                                                   where_the_bridge_belongs_to[0], where_the_bridge_belongs_to[1]])

                if terminal_obj.terminal_nr == connected_element.x_nr:
                    give_feedback(_("Attention! \nAll conductors carrying potential are likely to be marked as bridges!\n") \
                                  + terminal_obj.terminal_name + ":" + terminal_obj.terminal_nr)

            else:
                continue
    return list_of_bridge_at_terminal


def search_bridges(bridges_at_terminalrow_list, list_of_created_terminals):
    draw_brige_list = []

    bridges_unique = list(map(list, dict.fromkeys(map(tuple, bridges_at_terminalrow_list))))

    terminal_map = {t[1]: t[2] for t in list_of_created_terminals}

    print("Klemmen: ", list_of_created_terminals, ", Brücken: ", bridges_unique)

    for bridge in bridges_unique:
        start = terminal_map.get(bridge[1])
        end = terminal_map.get(bridge[4])

        if start is None:
            continue

        if end is None:
            if bridge[1] < bridge[4]:
                end = 9999
            else:
                end = 0

        draw_brige_list.append([
            start,
            end,
            bridge[5],
            bridge[6],
            bridge[0] + ":" + bridge[1]
        ])

    return draw_brige_list
