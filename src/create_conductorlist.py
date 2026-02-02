# import sqlite3
#
# import sql_queries as sq
# import sorting_functions as sf
# import terminal_table_classes as cl
#
# connection = sqlite3.connect('QET.db')
# cursor = connection.cursor()
#
# def select_conductors():
#     sql_select_conductors = ("""
#     SELECT
#     c.terminal1,
#     c.terminal2,
#     c.element1,
#     c.element2,
#     c.formula,
#     c.bus,
#     c.num,
#     c.conductor_color,
#     c.cable,
#     c.function,
#     c.tension_protocol,
#     c.conductor_section,
#     c.id
#     FROM conductors c
#     ORDER BY
#     c.conductor_section,
#     c.conductor_color
#             """)
#     conductors = cursor.execute(sql_select_conductors)
#     return conductors
#
#
# def give_feedback(feedback):
#     print (feedback)
# for cond in select_conductors():
#     if "Brücke%" in cond:
#         continue
#     dummy_connection = cl.Connection(" ", " ", " ",
#                                      " ", "", cond[3], " ", " ", " " )
#     dummy_terminal= cl.Terminal(" "," "," "," "," "," "," "," "," "," ")
#     conductor_obj = cl.Connected_Conductor(cond[0], cond[1], cond[2], cond[3], " ", " ", " ", cond[7]," ", " ", " ")
#     element_I = sf.search_element(cursor, dummy_connection, conductor_obj, cl, dummy_terminal, give_feedback)
#
#     print(element_I)
#
