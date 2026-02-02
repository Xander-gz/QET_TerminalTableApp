class Diagram():
    def __init__(self,title,
                 order,
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
                 version
                 ):
        self.freezeNewElemen = freezeNewElement
        self.plant = plant
        self.folio = folio
        self.author = author
        self.rows = rows
        self.auto_page_num = auto_page_num
        self.order = order
        self.locmach = locmach
        self.rowsize = rowsize
        self.displayAt = displayAt
        self.filename = filename
        self.colsize = colsize
        self.version = version
        self.date = date
        self.titleblocktemplateCollection = titleblocktemplateCollection
        self.freezeNewConductor = freezeNewConductor
        self.height = height
        self.indexrev = indexrev
        self.titleblocktemplate = titleblocktemplate
        self.displayrows = displayrows
        self.title = title
        self.displaycols = displaycols
        self.cols = cols
    def __repr__(self):
        return str(self.__dict__)


class Terminal_Row():
    def __init__(self,terminal_name,
                 plant,
                 locmach):
        self.terminal_name = terminal_name
        self.plant=plant
        self.locmach=locmach
    def __repr__(self):
        return str(self.__dict__)




class Terminal():
    def __init__(self,folio, rows, rowsize, cols, colsize, x, y, terminal_name=" ", terminal_nr=" ", function=" "):
        self.folio = folio
        self.rows = rows
        self.rowsize = rowsize
        self.cols = cols
        self.colsize = colsize
        self.x = x
        self.y = y
        self.terminal_name = terminal_name
        self.terminal_nr = terminal_nr
        self.function = function
    def __repr__(self):
        return str(self.__dict__)



class Terminal_Connectionpoint():
    def __init__(self,
                 folio,
                 rows,
                 rowsize,
                 cols,
                 colsize,
                 x,
                 y,
                 terminal_name,
                 terminal_nr,
                 connection_point,
                 terminal_type,
                 bus,
                 num,
                 conductor_color,
                 cable,
                 function,
                 connected_element_uuid,
                 connectet_embedded_element_uuid
    ):
        self.folio = folio
        self.rows = rows
        self.rowsize = rowsize
        self.cols = cols
        self.colsize = colsize
        self.x = x
        self.y = y
        self.terminal_name = terminal_name
        self.terminal_nr = terminal_nr
        self.connection_point = connection_point
        self.terminal_type = terminal_type
        self.bus = bus
        self.num = num
        self.conductor_color = conductor_color
        self.cable = cable
        self.function = function
        self.connected_element_uuid = connected_element_uuid
        self.connected_embedded_element_uuid = connectet_embedded_element_uuid
    def __repr__(self):
        return str(self.__dict__)


class Connected_Cable():
    def __init__(self, cable, conductor_section, tension_protocol):
        self.cable = cable
        self.conductor_section = conductor_section
        self.tension_protocol = tension_protocol
    def __repr__(self):
        return str(self.__dict__)


class Connection():
    def __init__(self,terminal_name, ei_terminal_nr, eet_name, eet_type,e_uuid, eet_uuid, folio, x, y):
        self.terminal_name = terminal_name
        self.ei_terminal_nr = ei_terminal_nr
        self.eet_name = eet_name
        self.eet_type = eet_type
        self.e_uuid = e_uuid
        self.eet_uuid = eet_uuid
        self.folio = folio
        self.x = x
        self.y = y
    def __repr__(self):
        return str(self.__dict__)


class Connected_Conductor():
    def __init__(self, terminal1, terminalname1, terminal2, terminalname2, element1, element1_name, element1_linked,
                 element1_label, element2, element2_name, element2_linked, element2_label, formula, bus, num,
                 conductor_color, cable, function, tension_protocol):
        self.terminal1 = terminal1
        self.terminalname1 = terminalname1
        self.terminal2 = terminal2
        self.terminalname2 = terminalname2
        self.element1 = element1
        self.element1_name = element1_name
        self.element1_linked = element1_linked
        self.element1_label = element1_label
        self.element2 = element2
        self.element2_name = element2_name
        self.element2_linked = element2_linked
        self.element2_label = element2_label
        self.formula = formula
        self.bus = bus
        self.num = num
        self.conductor_color = conductor_color
        self.cable = cable
        self.function = function
        self.tension_protocol = tension_protocol
    def __repr__(self):
        return str(self.__dict__)


class Connected_Link():
    def __init__(self, element, terminal):
        self.element = element
        self.terminal = terminal
    def __repr__(self):
        return str(self.__dict__)


class Connected_Element():
    def __init__(self, folio, x, y, label, connectionnpoint, location, plant, x_nr, x_plant, x_locmach,\
                 rows, rowsize, cols, colsize):
        self.folio = folio
        self.x = x
        self.y = y
        self.label = label
        self.connectionpoint = connectionnpoint
        self.location = location
        self.plant = plant
        self.x_nr = x_nr
        self.x_plant = x_plant
        self.x_locmach = x_locmach
        self.rows = rows
        self.rowsize = rowsize
        self.cols = cols
        self.colsize = colsize
    def __repr__(self):
        return str(self.__dict__)
