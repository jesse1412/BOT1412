import importlib
import copy

import drop_simulation

DROP_SIMULATIONS = "drop_simulations"

def isValidDropsimsModule(name):
    if importlib.util.find_spec(DROP_SIMULATIONS + "." + name) is None:
        return False
    return True

def removeTrash(drop_tables, trash_drops):
    newdrop_tables = copy.deepcopy(drop_tables)
    for trashDrop in trash_drops:
        for table in newdrop_tables:
            table.pop(trashDrop, None)
    return newdrop_tables

def simulate(name, trials, ignoreTrash):
    if isValidDropsimsModule(name):
        module = importlib.import_module(DROP_SIMULATIONS + "." + name)
        drop_tables = module.drop_tables
        if ignoreTrash:
            drop_tables = removeTrash(drop_tables, module.trash_drops)
        return drop_simulation.threaded_simulation(drop_tables, trials) + (module.trash_drops,)
    raise Exception("Invalid name provided.")

def dry(name, trials, ignoreTrash):
    if isValidDropsimsModule(name):
        module = importlib.import_module(DROP_SIMULATIONS + "." + name)
        drop_tables = module.drop_tables
        if ignoreTrash:
            drop_tables = removeTrash(drop_tables, module.trash_drops)
        return drop_simulation.dry(drop_tables, trials), module.trash_drops
    raise Exception("Invalid name provided.")
