import multiprocessing
import random
import threading
from functools import reduce
from multiprocessing import cpu_count, Process, Value, Manager

def thread_thing(trials, unique_items, drop_tables, cummulative_kc, cummulative_item_kcs, cummulative_items_found, lock):
    local_cumulative_items_found = {}
    local_cumulative_item_kcs = {}
    local_cummulative_kc = 0
    for item_name in unique_items:
        local_cumulative_item_kcs[item_name] = 0
        local_cumulative_items_found[item_name] = 0
    for i in range(trials):
            items_found = {}
            item_kcs = {}
            kc = 0
            while len(items_found.keys()) < len(unique_items):
                kc = kc + 1
                for table in drop_tables:
                    rand = random.random()
                    cummulative_rate = 0
                    for item_name in table.keys():
                        item_rate = table[item_name]
                        cummulative_rate = cummulative_rate + item_rate
                        if rand <= cummulative_rate:
                            if item_name in items_found:
                                items_found[item_name] = items_found[item_name] + 1
                            else:
                                items_found[item_name] = 1
                                item_kcs[item_name] = kc
                            break
            for item_name in unique_items:
                local_cumulative_item_kcs[item_name] = local_cumulative_item_kcs[item_name] + item_kcs[item_name]
                local_cumulative_items_found[item_name] = local_cumulative_items_found[item_name] + items_found[item_name]
            local_cummulative_kc = local_cummulative_kc + kc
    with lock:
        print(local_cummulative_kc)
        cummulative_kc.value = cummulative_kc.value + local_cummulative_kc
        print(cummulative_kc)
        for name, val in local_cumulative_item_kcs.items():
            cummulative_item_kcs[name] = cummulative_item_kcs[name] + val
            cummulative_items_found[name] = cummulative_items_found[name] + local_cumulative_items_found[name]

def simulate(drop_tables, trials: int):
    unique_items = set()
    for table in drop_tables:
        for item_name in table.keys():
            unique_items.add(item_name)

    manager = Manager()

    cummulative_item_kcs = manager.dict()
    cummulative_items_found = manager.dict()

    for item_name in unique_items:
        cummulative_item_kcs[item_name] = 0
        cummulative_items_found[item_name] = 0
    cummulative_kc = Value("i", 0)
    work_per_thread = int(trials / cpu_count())
    spare_work = trials % cpu_count()
    threads = []
    lock = multiprocessing.Lock()
    for i in range(cpu_count()):
        this_work = work_per_thread
        if i == 0:
            this_work += spare_work
        this_thread = Process(target=thread_thing, args=(this_work, unique_items, drop_tables, cummulative_kc, cummulative_item_kcs, cummulative_items_found, lock))
        threads.append(this_thread)
        threads[-1].start()
        if work_per_thread == 0:
            break
    for thread in threads:
        thread.join()
    average_kc = cummulative_kc.value / trials
    average_item_kcs = {}
    average_items_found = {}
    for item_name in unique_items:
        average_item_kcs[item_name] = cummulative_item_kcs[item_name] / trials
        average_items_found[item_name] = cummulative_items_found[item_name] / trials

    return average_kc, average_item_kcs, average_items_found

def dry(drop_tables, trials):
    chance_of_no_drop_per_table = []
    for table in drop_tables:
        chance_of_no_drop_per_table.append(1 - sum(table.values()))
    chance_of_no_drop_all_tables = reduce(lambda x, y: x * y, chance_of_no_drop_per_table)
    chance_of_drop_in_given_kc = chance_of_no_drop_all_tables ** trials
    return chance_of_drop_in_given_kc
