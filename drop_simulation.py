import multiprocessing
import random
import threading
from functools import reduce
from multiprocessing import cpu_count, Process, Value, Manager

def simulate(trials, unique_items, drop_tables, cummulative_kc, cummulative_item_kcs, cummulative_items_found, lock):
    # We want to track various values regarding all simulations.
    # To do that across all threads, it's easiest to aggregate the values later.
    # We track those values locally to this thread for now.
    local_cumulative_items_found = {}
    local_cumulative_item_kcs = {}
    local_cummulative_kc = 0
    for item_name in unique_items:
        local_cumulative_item_kcs[item_name] = 0
        local_cumulative_items_found[item_name] = 0
    # Trials is the number of simulations requested from this thread.
    for i in range(trials):
        # Collection of found items in this simulation.
        items_found = {}
        # First KC at which each item is obtained in this simulation.
        item_kcs = {}
        kc = 0
        # While we haven't found 1 of every item in the supplied drop tables.
        while len(items_found.keys()) < len(unique_items):
            # Track the total KC simulated accross all simulations.
            kc = kc + 1
            # One monster's "drop table" often consists of multiple different tables.
            # To be statistically correct, we must treat them separately if they can roll
            # simultaneously.
            for table in drop_tables:
                rand = random.random()
                cummulative_rate = 0
                for item_name in table.keys():
                    item_rate = table[item_name]
                    # At first, cummulative_rate is equal to the probability of the first item in the table.
                    # On the second iteration, it's the sum of the first and second probabilities, etc, etc.
                    # Effectively bins are created representing each item on the table using cummulative_rate.
                    # E.g for 3 items with p=0.1, the bin for the first item is 0 to 0.1,
                    # the second item is 0.1 to 0.2, and the third is 0.2 to 0.3.
                    # We check which bin (if any) the randomly generated number falls into.
                    cummulative_rate = cummulative_rate + item_rate
                    # If the number falls into the current bin being checked.
                    if rand <= cummulative_rate:
                        # We add the item to the collection of found items
                        if item_name in items_found:
                            items_found[item_name] = items_found[item_name] + 1
                        else:
                            items_found[item_name] = 1
                            item_kcs[item_name] = kc
                        break
        # Once all items on the table have been found for this simulation.
        for item_name in unique_items:
            local_cumulative_item_kcs[item_name] = local_cumulative_item_kcs[item_name] + item_kcs[item_name]
            local_cumulative_items_found[item_name] = local_cumulative_items_found[item_name] + items_found[item_name]
        local_cummulative_kc = local_cummulative_kc + kc
    # Now that all simulations are complete, we aggregate the values in variables shared between threads.
    with lock:
        cummulative_kc.value = cummulative_kc.value + local_cummulative_kc
        for name, val in local_cumulative_item_kcs.items():
            cummulative_item_kcs[name] = cummulative_item_kcs[name] + val
            cummulative_items_found[name] = cummulative_items_found[name] + local_cumulative_items_found[name]

def threaded_simulation(drop_tables, trials: int):
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
        this_thread = Process(target=simulate, args=(this_work, unique_items, drop_tables, cummulative_kc, cummulative_item_kcs, cummulative_items_found, lock))
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
        # Each table can only roll 1 of each drop
        # Hence we sum the probabilities of all the drops to get the chance of any drop
        chance_of_no_drop_per_table.append(1 - sum(table.values()))
    # Chance of no drop on a given roll for all of the rolled tables is the product of the
    # chance of no drop on every individual table.
    chance_of_no_drop_all_tables = reduce(lambda x, y: x * y, chance_of_no_drop_per_table)
    # Then we just calculate the chance of that event occuring the given amount of times.
    chance_of_no_drop_in_given_kc = chance_of_no_drop_all_tables ** trials
    return chance_of_no_drop_in_given_kc
