import terminal_table_classes as cl



def terminal_row_list(cursor):
    sql_terminal_row_list = ("""
            SELECT
            ei.ei_terminal_row_name AS terminal_name,
            d.plant,
            d.locmach
            From elementinformations ei 
            JOIN elements e on e.e_uuid = ei.e_uuid
            JOIN diagrams d on d.id = e.diagram_id
            WHERE ei_terminal_row_name LIKE "-X%" 
            GROUP BY 
            ei_terminal_row_name
            ORDER BY 
            ei_terminal_row_name
         """)
    list = cursor.execute(sql_terminal_row_list).fetchall()
    terminal_row_list = []
    for l in list:
        terminal_row_obj = cl.Terminal_Row(*l) if l else None
        terminal_row_list.append(terminal_row_obj)
    return terminal_row_list


def number_of_connectionpoints_per_terminal(cursor, terminal_row_obj):
    sql_number_of_connectionpoints_per_terminal = \
        ("""
        SELECT
            seite,
            MAX(anzahl_klemmpunkte) AS max_klemmpunkte,
            klemmpunkt
        FROM (
            SELECT
                ei.ei_terminal_row_name              AS klemme,
                eet.eet_type              AS seite,
                COUNT(DISTINCT eet.eet_name) AS anzahl_klemmpunkte,
                eet.eet_name AS klemmpunkt
            FROM elements e 
            JOIN elementinformations ei ON ei.e_uuid = e.e_uuid
            JOIN embedded_elements ee ON ee_name = e.e_type
            JOIN embedded_element_terminals eet ON eet.ee_uuid = ee.ee_uuid
            WHERE ei.ei_terminal_row_name LIKE (?) 
            AND eet.eet_type != "Generic"
            GROUP BY
                eet.eet_name
        )
        GROUP BY klemmpunkt;
        """)
    number_of_connectionpoints_per_terminal = cursor.execute(sql_number_of_connectionpoints_per_terminal, [terminal_row_obj.terminal_name]).fetchall()
    return number_of_connectionpoints_per_terminal


def data_of_the_terminal(cursor, tr):
    sql_data_of_the_terminal = \
        ("""
        SELECT
        d.folio,
        d.rows, 
        d.rowsize,
        d.cols,
        d.colsize, 
        e.x, 
        e.y, 
        ei.ei_terminal_row_name AS terminal_name,
        ei.ei_terminal_nr AS terminal_nr,
        c.function
        FROM diagrams d 
        JOIN elements e ON diagram_id = d.id 
        JOIN embedded_elements ee ON ee_name = e.e_type
        JOIN embedded_element_terminals eet on eet.ee_uuid = ee.ee_uuid
        JOIN elementinformations ei ON ei.e_uuid = e.e_uuid
        JOIN conductors c ON c.element1 = e.e_uuid OR c.element2 = e.e_uuid
        WHERE ei_terminal_row_name = (?) 
        AND ei_terminal_nr = (?)
        AND eet_name IS NOT ""
        ORDER BY c.function;
        """)
    row = cursor.execute(sql_data_of_the_terminal, tr).fetchall()
    print("terminal_obj", row)
    terminal_obj = cl.Terminal(*row[0]) if row else None
    if terminal_obj == None:
        # if there is no conductor there should be a terminal aniway
        terminal_obj = cl.Terminal("","","","","","","",tr[0],tr[1],"")

    return terminal_obj


def terminals_list(cursor, terminal_row_obj, give_feedback):
    sql_data_of_the_terminal = \
        ("""
        SELECT
        ei.ei_terminal_row_name AS terminal_name,
        ei.ei_terminal_nr
        From elementinformations ei 
        WHERE ei_terminal_row_name LIKE (?) 
        AND ei.ei_terminal_nr NOT LIKE "%sequ%"
        GROUP BY 
        ei_terminal_nr
        ORDER BY ei_terminal_nr GLOB '[0-9]*' DESC,
        CAST(ei_terminal_nr AS INTEGER),
        ei_terminal_nr;
         """)
    number = cursor.execute(sql_data_of_the_terminal, [terminal_row_obj.terminal_name]).fetchall()
    if any(n[1] == 'XXX' for n in number):

        give_feedback(_("An element was labelled with -X that is not a terminal (without a named terminal).") + terminal_row_obj.terminal_name)
    return number


def connected_cables(cursor, terminal_row_obj):
    sql_connected_cables = \
        ("""
         SELECT
         DISTINCT c.cable,
		 c.tension_protocol,
		 c.conductor_section
         FROM elements e
         JOIN elementinformations ei ON ei.e_uuid = e.e_uuid
         JOIN embedded_elements ee ON ee_name = e.e_type
         JOIN embedded_element_terminals eet ON eet.ee_uuid = ee.ee_uuid
         JOIN conductors c ON element1 = e.e_uuid OR element2 = e.e_uuid
         WHERE ei_terminal_row_name = (?)
         AND eet_type != "Generic"
         AND c.cable != ""
         GROUP BY c.cable
         ORDER BY c.cable
         """)
    cablelist = cursor.execute(sql_connected_cables, [terminal_row_obj.terminal_name]).fetchall()
    return cablelist


def list_of_connectionpoints(cursor, terminal_row_obj):
    sql_list_of_connectionpoints = \
        ("""
        SELECT
        DISTINCT eet.eet_name,
        eet.eet_type
        FROM elements e
        JOIN elementinformations ei ON ei.e_uuid = e.e_uuid
        JOIN embedded_elements ee ON ee_name = e.e_type
        JOIN embedded_element_terminals eet ON eet.ee_uuid = ee.ee_uuid
        WHERE ei_terminal_row_name = (?)
        AND eet_type != "Generic"
        ORDER BY
        eet_type,
        eet_name;
        """)
    connectionpoints = cursor.execute(sql_list_of_connectionpoints, [terminal_row_obj.terminal_name]).fetchall()
    return connectionpoints


def connected_conductor_side1(cursor, connection_obj):
    sql_connected_conductor = ("""
    SELECT
    c.terminal1,
    c.terminalname1,
    c.terminal2,
    c.terminalname2,
    c.element1,
    c.element1_name,
    c.element1_linked,
    c.element1_label,
    c.element2,
    c.element2_name,
    c.element2_linked,
    c.element2_label,
    c.formula,
    c.bus,
    c.num,
    c.conductor_color,
    c.cable,
    c.function,
    c.tension_protocol
    FROM conductors c 
    WHERE terminal1 = (?)
    AND element1 = (?)
    """)
    sql_values = (connection_obj.eet_uuid, connection_obj.e_uuid,)
    row = cursor.execute(sql_connected_conductor, sql_values).fetchone()
    return cl.Connected_Conductor(*row) if row else None


def connected_conductor_side2(cursor, connection_obj):
    sql_connected_conductor = ("""
    SELECT 
    c.terminal1,
    c.terminalname1,
    c.terminal2,
    c.terminalname2,
    c.element1,
    c.element1_name,
    c.element1_linked,
    c.element1_label,
    c.element2,
    c.element2_name,
    c.element2_linked,
    c.element2_label,
    c.formula,
    c.bus,
    c.num,
    c.conductor_color,
    c.cable,
    c.function,
    c.tension_protocol
    FROM conductors c
    WHERE terminal2 = (?)
    AND element2 = (?) 
    """)
    sql_values = (connection_obj.eet_uuid, connection_obj.e_uuid,)
    row = cursor.execute(sql_connected_conductor, sql_values).fetchone()
    return cl.Connected_Conductor(*row) if row else None


def connections_per_terminal(cursor, terminal_obj, text1):
    sql_connections = ("""
        SELECT
        ei.ei_terminal_row_name AS terminal_name,
        ei.ei_terminal_nr,
        eet.eet_name,
        eet.eet_type,
        e.e_uuid,
        eet.eet_uuid,
        d.folio,
        e.x,
        e.y
        FROM elementinformations ei
        JOIN elements e on e.e_uuid = ei.e_uuid
        JOIN embedded_elements ee on ee.ee_name = e.e_type
        JOIN embedded_element_terminals eet on eet.ee_uuid = ee.ee_uuid
        JOIN diagrams d on d.id = e.diagram_id
        WHERE ei_terminal_row_name = (?)
        AND ei_terminal_nr = (?)
        AND eet_name LIKE (?)
        AND eet_type LIKE (?)
                       """)
    sql_values = (terminal_obj.terminal_name, terminal_obj.terminal_nr, text1[0], text1[1])
    list = cursor.execute(sql_connections, sql_values).fetchall()
    connections_list = []
    for l in list:
        connection_obj = cl.Connection(*l) if l else None
        connections_list.append(connection_obj)
    return connections_list

def select_element_type_master_slave(cursor, target_terminal,):
    sql_select_element_type = ("""
    SELECT ee.ee_link_type
    FROM embedded_element_terminals eet
    LEFT JOIN embedded_elements ee on ee.ee_uuid = eet.ee_uuid
    WHERE eet.eet_uuid = (?)
        """)
    sql_values = (target_terminal,)
    typ = cursor.execute(sql_select_element_type, sql_values).fetchone()
    type = typ[0]
    return type


def select_element_type_simple_terminal(cursor, target_element,):
    sql_select_element_type = ("""
           SELECT ee.ee_link_type
           FROM embedded_elements ee
           LEFT JOIN elements e ON e.e_type = ee.ee_name
           WHERE e.e_uuid = (?)
           """)
    sql_values = (target_element,)
    typ = cursor.execute(sql_select_element_type, sql_values).fetchone()
    type = typ[0]
    return type


def select_simple_element(cursor, target_element, terminal_obj, give_feedback):
    sql_select_simple_element = ("""
    SELECT
    	d.folio,
    	e.x,
    	e.y,
    	ei.ei_name,
    	ei.ei_terminal_row_name,
    	ei.ei_terminal_nr,
        d.plant,
        d.locmach,
        d.rows,
        d.rowsize,
        d.cols,
        d.colsize
    FROM elements e 
    JOIN elementinformations ei on ei.e_uuid = e.e_uuid
    LEFT JOIN diagrams d on d.id = e.diagram_id
    WHERE e.e_uuid = (?)
    """)
    sql_values = (target_element,)
    list = cursor.execute(sql_select_simple_element, sql_values).fetchall()
    print(list)
    label = ""
    location = ""
    plant = ""
    x_plant = ""
    x_locmach = ""
    for l in list:
        folio = l[0]
        x = l[1]
        y = l[2]
        if l[3] == "label":
            label = l[4]
        if l[3] == "location":
            location = l[4]
        if l[3] == "plant":
            plant = l[4]
        x_nr = l[5]
        x_plant = l[6]
        x_locmach = l[7]
        rows = l[8]
        rowsize = l[9]
        cols = l[10]
        colsize = l[11]

    connectionpoint = " "
    if not list:
        give_feedback(_("Error! \nAt terminal  ") + terminal_obj.terminal_name + ":" + terminal_obj.terminal_nr +
        _("\na connected element is not fully populated with data."))

    element = cl.Connected_Element(folio, x, y, label, connectionpoint, location, plant, x_nr, x_plant, x_locmach, rows,
                                   rowsize, cols, colsize)
    return element


def select_slave_element(cursor, target_element, terminal_obj, give_feedback):
    sql_select_element = ("""
    SELECT
        d.folio,
        e.x,
        e.y,
        l.l_uuid,
        e.e_type,
        d.rows,
        d.rowsize,
        d.cols,
        d.colsize
    FROM elements e
    JOIN diagrams d on d.id = e.diagram_id
    JOIN link_uuids l on l.e_uuid = e.e_uuid
    WHERE e.e_uuid = (?)
    """)
    sql_values = (target_element,)
    list = cursor.execute(sql_select_element, sql_values).fetchone()
    if not list:
        give_feedback(_("Error!\nAt terminal ") + terminal_obj.terminal_name + ":" + terminal_obj.terminal_nr +
        _("\na slave element is not linked."))
    return list

def select_terminal(cursor, target_terminal):
    sql_select_slave_terminal = ("""
    SELECT
        eet.eet_name,
        eet.eet_type
    FROM embedded_element_terminals eet 
    where eet.eet_uuid = (?)
        """)
    sql_values = (target_terminal,)
    list = cursor.execute(sql_select_slave_terminal, sql_values).fetchone()
    return list

def select_master_element(cursor, target_element, terminal_obj, give_feedback):
    sql_select_master_element = ("""
    SELECT
        ei.ei_name,
        ei.ei_terminal_row_name,
        ei.ei_terminal_nr
    FROM elementinformations ei
    where ei.e_uuid = (?)
        """)
    sql_values = (target_element,)
    list = cursor.execute(sql_select_master_element, sql_values).fetchall()
    for l in list:
        if l[0] == "label":
            label = l[1]
        if l[0] == "plant":
            plant = l[1]
        if l[0] == "location":
            location = l[1]

    if not list:
        give_feedback(_("Error! \nAt terminal  ") + terminal_obj.terminal_name + ":" + terminal_obj.terminal_nr +
                      _("\na connected element is not fully populated with data."))
    element_list = "label", label, "location", location, "plant", plant
    return element_list


def next_previous_report_element(cursor, target_element):
    sql_next_previous_report_element = ("""
    SELECT
    e.e_uuid,
    eet.eet_uuid
    FROM link_uuids l
    JOIN elements e on e.e_uuid = l.e_uuid
    JOIN embedded_elements ee on ee.ee_name = e.e_type
    JOIN embedded_element_terminals eet on ee.ee_uuid = eet.ee_uuid
    WHERE e.e_uuid =
    (SELECT 
    l.l_uuid 
    FROM link_uuids l
    WHERE l.e_uuid = (?))
    """)
    sql_values = (target_element,)
    list = cursor.execute(sql_next_previous_report_element, sql_values).fetchone()
    linked_terminal = cl.Connected_Link(list[0], list[1])
    return linked_terminal