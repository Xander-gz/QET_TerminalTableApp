

import sql_queries as sq


def reference(terminal_obj):
    alpha = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    reference_x = (int(terminal_obj.x) -25 ) // int(terminal_obj.colsize)+1
    reference_y = alpha[(int(terminal_obj.y) -25 ) // int(terminal_obj.rowsize)]
    reference = "/" + terminal_obj.folio + " ." + str(reference_y) + str(reference_x)

    return reference


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
    conductor_obj = sq.connected_conductor_side1(cursor, connection_obj)
    if conductor_obj == None:
        conductor_obj = sq.connected_conductor_side2(cursor, connection_obj)
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
                                                 slave_element_list[6], slave_element_list[7], slave_element_list[8])


    if element_type == "next_report" or element_type == "previous_report":
        # if element is next-, preview-report, it comes with an element_type to recursion
        linked_terminal = sq.next_previous_report_element(cursor, target_element)
        connection_tuple_list.eet_uuid = linked_terminal.terminal
        connection_tuple_list.e_uuid = linked_terminal.element
        linked_conductor = search_conductor(cursor, connection_tuple_list)
        connected_element = search_element(cursor, connection_tuple_list, linked_conductor, cl, terminal_obj,
                                           give_feedback)


    return connected_element


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
                    target_element = conductor_obj.element2
                else:
                    target_element = conductor_obj.element1
                connected_element = sq.select_simple_element(cursor, target_element, terminal_obj, give_feedback)
                where_the_bridge_belogs_to = conductor_obj.num.split(" ")[1]
                print("Brücke von ", terminal_obj.terminal_name, terminal_obj.terminal_nr, "nach ",connected_element.label, connected_element.x_nr)
                list_of_bridge_at_terminal.append([terminal_obj.terminal_name, terminal_obj.terminal_nr, "to",
                                                   connected_element.label, connected_element.x_nr,
                                                   where_the_bridge_belogs_to[0], where_the_bridge_belogs_to[1]])

                if terminal_obj.terminal_nr == connected_element.x_nr:
                    give_feedback(_("Attention! \nAll conductors carrying potential are likely to be marked as bridges!\n") \
                                  + terminal_obj.terminal_name + ":" + terminal_obj.terminal_nr)

            else:
                continue
    return list_of_bridge_at_terminal


def search_bridges(bridges_at_terminalrow_list, list_of_created_terminals):
    # bridges_at_terminalrow_list = [['-X313', '1', 'to', '-X313', '2', '3', 'e'], ['-X313', '11', 'to', '-X313', '12', '3', 'e'], ['-X313', '11', 'to', '-X313', '12', '3', 'e'], ['-X313', '11', 'to', '-X313', '12', '3', 'e']]
    # list_of_created_terminals = [('-X313', '1', 270), ('-X313', '2', 310), ('-X313', '11', 350), ('-X313', '12', 390), ('-X313', '21', 430), ('-X313', '29', 470), ('-X313', '73', 510), ('-X313', '75', 550), ('-X313', '77', 590), ('-X313', '500', 630), ('-X313', '501', 670)]
    draw_brige_list = []
    bridges_unique = list(map(list, dict.fromkeys(map(tuple, bridges_at_terminalrow_list))))
    print("Klemmen: ", list_of_created_terminals, ", Brücken: ", bridges_unique)
    for bridge_at_terminalrow in bridges_unique:

        if(btl[1] == bridge_at_terminalrow[1] for brl in list_of_created_terminals):
            result = next((e for e in list_of_created_terminals if e[1] == bridge_at_terminalrow[1]), None)
            if result != None:
                start = result[2]
        if(btl[1] == bridge_at_terminalrow[4] for brl in list_of_created_terminals):
            result = next((e for e in list_of_created_terminals if e[1] == bridge_at_terminalrow[4]), None)
            if result != None:
                end = result[2]
            else:
                if bridge_at_terminalrow[1] < bridge_at_terminalrow[4]:
                    end = 9999
                else:
                    end = 0

        draw_brige_list.append([start, end, bridge_at_terminalrow[5], bridge_at_terminalrow[6],
                                    (bridge_at_terminalrow[0] + ":" + bridge_at_terminalrow[1])])


    return draw_brige_list


