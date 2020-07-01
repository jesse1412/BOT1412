#import dropsims.zulrah
#import dropsims.coinFlip
#import dropsims.nightmare
#import dropsims.custom
import importlib
import dropsim
import copy

def isValidDropsimsModule(name):
    if importlib.util.find_spec("dropsims." + name) is None:
        return False
    return True

def removeTrash(dropTables, trashDrops):
    newDropTables = copy.deepcopy(dropTables)
    for trashDrop in trashDrops:
        for table in newDropTables:
            table.pop(trashDrop, None)
    return newDropTables

def simulate(name, trials, ignoreTrash):
    if isValidDropsimsModule(name):
        module = importlib.import_module("dropsims." + name)
        dropTables = module.dropTables
        if ignoreTrash:
            dropTables = removeTrash(dropTables, module.trashDrops)
        return dropsim.simulate(dropTables, trials) + (module.trashDrops,)
    raise Exception("Invalid name provided.")

def dry(name, trials, ignoreTrash):
    if isValidDropsimsModule(name):
        module = importlib.import_module("dropsims." + name)
        dropTables = module.dropTables
        if ignoreTrash:
            dropTables = removeTrash(dropTables, module.trashDrops)
        return dropsim.dry(dropTables, trials), module.trashDrops
    raise Exception("Invalid name provided.")