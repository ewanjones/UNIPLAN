import sqlite3
from collections import namedtuple
import CONFIG

filename = 'database.sql'
conn = sqlite3.connect(filename)
c = conn.cursor()


def create_tables():
    c.execute('''CREATE TABLE IF NOT EXISTS modules
                    (code TEXT NOT NULL PRIMARY KEY, 
                     name TEXT, 
                     credits REAL, 
                     grade REAL, 
                     classification REAL)''')

    c.execute('''CREATE TABLE IF NOT EXISTS components
                    (code TEXT, 
                     name TEXT, 
                     weight REAL, 
                     category TEXT, 
                     grade REAL, 
                     classification TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS timetable
                    (date DATE, 
                     start_time TIME, 
                     end_time TIME, 
                     code TEXT, 
                     name TEXT, 
                     credits REAL)''')
    conn.commit()



def add_module(code, name, credits, grade=None, classification=None):
    try:
        c.execute('''INSERT INTO modules VALUES (?, ?, ?, ?, ?)''', (code, name, credits, grade, classification))
        conn.commit()
    except:
        print('There is already a module with that name.')



def edit_module(search, code=None, name=None, credits=None, grade=None, classification=None):
    current = c.execute('''SELECT * FROM modules WHERE code=?''', (search,)).fetchall()         # Current values
    args = [code, name, credits, grade, classification]                                         # Updated values
    params = tuple([item if item else current[0][i] for i, item in enumerate(args)])            # Create tuple of combined
    params += (search,)

    # Update module in SQL
    query = '''UPDATE modules
                SET code=?, name=?, credits=?, grade=?, classification=?
                WHERE code=?'''
    c.execute(query, params)
    conn.commit()


def del_module(code):
    c.execute('''DELETE FROM modules WHERE code=:code''', {'code': code})
    conn.commit()


def add_component(code, name, category, weight, grade=None, classification=None):
    try:
        c.execute('''INSERT INTO modules VALUES (:code, :name, :category, :grade, :classification)''',
                  {'code': code,
                   'name': name,
                   'weight': weight,
                   'category': category,
                   'grade': grade,
                   'classification': classification})
        conn.commit()
    except:
        print('There is already a component with that name.')


def check_valid():
    # Check the total credits add up to CONFIG.TOTAL_CREDITS
    total_credits = c.execute('''SELECT SUM(credits)
                    FROM modules''').fetchall()
    print(total_credits)
    if int(total_credits[0][0]) != CONFIG.TOTAL_CREDITS:
        print("The total credits do not add up to %d." % CONFIG.TOTAL_CREDITS)
        return False

    # List of modules
    modules = c.execute('''SELECT code FROM modules''').fetchall()
    module_list = [item[0] for item in modules]

    # Check the components add up to 100%
    for module in module_list:
        total_comp_weight = c.execute('''SELECT SUM(weight) FROM components WHERE code=?''', (module,))
        if total_comp_weight != 100:
            print('The component weights for %s do not add up to 100' % module)
            return False

    return True


create_tables()