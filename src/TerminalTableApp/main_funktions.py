"""
Copyright (C) 2026 xanderhopp; xanderhopp@gmail.com

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, version 3.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
"""


import sqlite3


from TerminalTableApp.read import create_database as cdb
from TerminalTableApp.read import read_xml_file as read_xml
from TerminalTableApp.write import create_table as create_table



def work_out_the_terminal_diagram(origin_file, give_feedback):

# open SQLite to store and sort the infos of the diagram-file
# the out commented line is for test-cases
    connection = sqlite3.connect(':memory:')
    # connection = sqlite3.connect('QET.db')
    cursor = connection.cursor()

    cdb.create_SQLite_table (cursor, connection)
    read_xml.read_xml_file(origin_file, cursor, connection, give_feedback)
    create_table.create_table(origin_file, cursor, connection, give_feedback)


# todo: Brücke im Moment nicht über seitenverweis möglich






# todo: Darstellung der Seitenverweise aus der Datei importieren (?)









