import copy
import io
import math
import pickle
from pathlib import Path
from utils import resolve_suffix

MAX_DEBT = 2**64

class Debt():
    def __init__(self, file_path = Path("debt_list.pickle")):
        self.file_path = file_path
        self.__try_load_debt_list(self.file_path)

    def __try_save_debt_list(self, save_path):    
        with open(save_path, "wb+") as writer:
            pickle.dump((self.__debt_list, self.__debt_list_reverse), writer)

    def __try_load_debt_list(self, load_path):
        if load_path.exists():
            with open(load_path, "rb") as reader:
                    self.__debt_list, self.__debt_list_reverse = pickle.load(reader)
        else:
            self.__debt_list = {}
            self.__debt_list_reverse = {}

    def __get_debt_list(self):
        return copy.deepcopy(self.__debt_list), copy.deepcopy(self.__debt_list_reverse)
    
    def __set_debt_list(self, debt_list):
        self.__debt_list = debt_list
        self.__debt_list_reverse = {}
        self.__try_save_debt_list(self.file_path)

    debt_list = property(__get_debt_list, __set_debt_list)

    def update_debt(self, name, name_2, change_text):
        is_additive = False
        if len(change_text) == 1:
            is_additive = False
        else:
            is_additive = change_text[0] == "+" or change_text[0] == "-"
        change_val = resolve_suffix(change_text)
        new_debt_value = 0
        if not name_2 in self.__debt_list_reverse:
            self.__debt_list_reverse[name_2] = {}
        if not name in self.__debt_list:
            self.__debt_list[name] = {}
        if not is_additive:
            new_debt_value = change_val
        else:
            if name_2 in self.__debt_list[name]:
                new_debt_value = self.__debt_list[name][name_2] + change_val
            else:
                new_debt_value = change_val
                self.__debt_list[name][name_2] = {}
                self.__debt_list_reverse[name_2][name] = {}
        if abs(new_debt_value) > MAX_DEBT:
            raise Exception("Debt too high.")
        self.__debt_list[name][name_2] = new_debt_value
        self.__debt_list_reverse[name_2][name] = new_debt_value
        if new_debt_value == 0:
            del self.__debt_list[name][name_2]
            del self.__debt_list_reverse[name_2][name]
        if len(self.__debt_list[name]) == 0:
            del self.__debt_list[name]
        if len(self.__debt_list_reverse[name_2]) == 0:
            del self.__debt_list_reverse[name_2]
        self.__try_save_debt_list(self.file_path)
        