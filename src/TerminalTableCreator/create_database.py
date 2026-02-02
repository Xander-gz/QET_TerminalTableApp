def create_SQLite_table(cursor, connection):

    cursor.executescript("""
    
    DROP TABLE IF EXISTS diagrams;
    DROP TABLE IF EXISTS elements;
    DROP TABLE IF EXISTS terminals;
    DROP TABLE IF EXISTS elementinformations;
    DROP TABLE IF EXISTS terminal_types;
    DROP TABLE IF EXISTS link_uuids;
    DROP TABLE IF EXISTS conductors;
    DROP TABLE IF EXISTS embedded_elements;
    DROP TABLE IF EXISTS kindInformations;
    DROP TABLE IF EXISTS embedded_element_terminals;
    
    CREATE TABLE diagrams(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        order_nr INTEGER,
        auto_page_num TEXT,
        folio TEXT,
        plant TEXT,
        locmach TEXT,
        date INTEGER,
        author TEXT,
        indexrev TEXT,
        filename TEXT,
        rows INTEGER,
        rowsize INTEGER,
        cols INTEGER,
        colsize INTEGER,
        displayrows TEXT,
        displaycols TEXT,
        titleblocktemplate TEXT,
        titleblocktemplateCollection TEXT,
        height INTEGER,
        freezeNewConductor TEXT,
        freezeNewElement TEXT,
        displayAt TEXT,
        version TEXT
    );
        
        
    CREATE TABLE elements (
        diagram_id INTEGER,
        e_uuid TEXT,
        e_type TEXT,
        x INTEGER,
        y INTEGER,
        z INTEGER,
        FOREIGN KEY(diagram_id) REFERENCES diagrams(id)
    );
                   
    CREATE TABLE terminals (
        e_uuid TEXT,
        terminal_id INTEGER,
        x INTEGER,
        y INTEGER,
        FOREIGN KEY(e_uuid) REFERENCES elements(e_uuid)
        );
        
    CREATE TABLE elementinformations (
        e_uuid TEXT,
        ei_name TEXT,
        ei_terminal_row_name TEXT,
        ei_terminal_nr TEXT,
        FOREIGN KEY(e_uuid) REFERENCES elements(e_uuid)
        );

    CREATE TABLE terminal_types (
        e_uuid TEXT,
        terminal_function TEXT,
        terminal_type TEXT,
        terminal_led TEXT,
        FOREIGN KEY(e_uuid) REFERENCES elements(e_uuid)
        );
        
    CREATE TABLE link_uuids (
        e_uuid TEXT,
        l_uuid TEXT TEXT,
        FOREIGN KEY(e_uuid) REFERENCES elements(e_uuid)
        );
        
    CREATE TABLE conductors (
        id integer PRIMARY KEY AUTOINCREMENT,
        terminal1 TEXT,
        terminalname1 TEXT,
        terminal2 TEXT,
        terminalname2 TEXT,
        element1 TEXT,
        element1_name TEXT,
        element1_linked TEXT,
        element1_label TEXT,
        element2 TEXT,
        element2_name TEXT,
        element2_linked TEXT,
        element2_label TEXT,
        formula TEXT,
        c_type TEXT,
        bus TEXT,
        num TEXT,
        conductor_section TEXT,
        conductor_color TEXT,
        cable TEXT,
        function TEXT,
        tension_protocol TEXT
        );
        
    CREATE TABLE embedded_elements (
        ee_uuid TEXT PRIMARY KEY,
        ee_name TEXT,
        ee_link_type TEXT,
        ee_type TEXT,
        ee_version TEXT
        );
        
    CREATE TABLE kindInformations (
        ee_uuid TEXT,
        ki_name TEXT,
        ki_text TEXT,
        FOREIGN KEY (ee_uuid) REFERENCES embedded_elements(ee_uuid)
        );

    CREATE TABLE embedded_element_terminals (
        eet_uuid TEXT PRIMARY KEY,
        ee_uuid TEXT,
        eet_name TEXT,
        eet_type TEXT,
        FOREIGN KEY (ee_uuid) REFERENCES embedded_elements(ee_uuid)
        );
        
    """)

    connection.commit()