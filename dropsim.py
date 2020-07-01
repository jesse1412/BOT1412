import random
from functools import reduce
import threading
from multiprocessing import cpu_count
from multiprocessing import Process, Value, Manager
import multiprocessing

def thread_thing(trials, uniqueItems, dropTables, cummulativeKC, cummulativeItemKCs, cummulativeItemsFound, lock):
    local_cumulative_items_found = {}
    local_cumulative_item_KCs = {}
    local_cummulative_KC = 0
    for itemName in uniqueItems:
        local_cumulative_item_KCs[itemName] = 0
        local_cumulative_items_found[itemName] = 0
    for i in range(trials):
            itemsFound = {}
            itemKCs = {}
            KC = 0
            while len(itemsFound.keys()) < len(uniqueItems):
                KC = KC + 1
                for table in dropTables:
                    rand = random.random()
                    cummulativeRate = 0
                    for itemName in table.keys():
                        itemRate = table[itemName]
                        cummulativeRate = cummulativeRate + itemRate
                        if rand <= cummulativeRate:
                            if itemName in itemsFound:
                                itemsFound[itemName] = itemsFound[itemName] + 1
                            else:
                                itemsFound[itemName] = 1
                                itemKCs[itemName] = KC
                            break
            for itemName in uniqueItems:
                local_cumulative_item_KCs[itemName] = local_cumulative_item_KCs[itemName] + itemKCs[itemName]
                local_cumulative_items_found[itemName] = local_cumulative_items_found[itemName] + itemsFound[itemName]
            local_cummulative_KC = local_cummulative_KC + KC
    with lock:
        print(local_cummulative_KC)
        cummulativeKC.value = cummulativeKC.value + local_cummulative_KC
        print(cummulativeKC)
        for name, val in local_cumulative_item_KCs.items():
            cummulativeItemKCs[name] = cummulativeItemKCs[name] + val
            cummulativeItemsFound[name] = cummulativeItemsFound[name] + local_cumulative_items_found[name]

def simulate(dropTables, trials: int):
    uniqueItems = set()
    for table in dropTables:
        for itemName in table.keys():
            uniqueItems.add(itemName)

    manager = Manager()

    cummulativeItemKCs = manager.dict()
    cummulativeItemsFound = manager.dict()

    for itemName in uniqueItems:
        cummulativeItemKCs[itemName] = 0
        cummulativeItemsFound[itemName] = 0
    cummulativeKC = Value("i", 0)
    work_per_thread = int(trials / cpu_count())
    spare_work = trials % cpu_count()
    threads = []
    lock = multiprocessing.Lock()
    for i in range(cpu_count()):
        this_work = work_per_thread
        if i == 0:
            this_work += spare_work
        this_thread = Process(target=thread_thing, args=(this_work, uniqueItems, dropTables, cummulativeKC, cummulativeItemKCs, cummulativeItemsFound, lock))
        threads.append(this_thread)
        threads[-1].start()
        if work_per_thread == 0:
            break
    for thread in threads:
        thread.join()
    averageKC = cummulativeKC.value / trials
    averageItemKCs = {}
    averageItemsFound = {}
    for itemName in uniqueItems:
        averageItemKCs[itemName] = cummulativeItemKCs[itemName] / trials
        averageItemsFound[itemName] = cummulativeItemsFound[itemName] / trials

    return averageKC, averageItemKCs, averageItemsFound

def dry(dropTables, trials):
    noDropChancePerTable = []
    for table in dropTables:
        noDropChancePerTable.append(1 - sum(table.values()))
    chanceOfNoDropAllTables = reduce(lambda x, y: x * y, noDropChancePerTable)
    print(chanceOfNoDropAllTables)
    print(trials)
    chanceOfDropInGivenKC = chanceOfNoDropAllTables ** trials
    return chanceOfDropInGivenKC