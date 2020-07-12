import copy
import io
import pickle
from pathlib import Path

class Debt():
    def __init__(self, file_path = Path("debt_list.pickle")):
        self.file_path = file_path
        self.__try_load_debt_list(self.file_path)
        pass

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
        change_text = change_text.replace(",", "")
        is_additive = False
        suffix = ""
        if len(change_text) == 1:
            is_additive = False
        else:
            is_additive = change_text[0] == "+" or change_text[0] == "-"
            suffix = change_text[-1].lower()
        if suffix == "k":
            change_val = int(change_text[:-1]) * 10 ** 3
        elif suffix == "m":
            change_val = int(change_text[:-1]) *  10 ** 6
        elif suffix == "b":
            change_val = int(change_text[:-1]) *  10 ** 9
        else:
            change_val = int(change_text)
        if is_additive:
            if name in self.__debt_list:
                if name_2 in self.__debt_list[name]:
                    self.__debt_list[name][name_2] = self.__debt_list[name][name_2] + change_val
                    if name_2 in self.__debt_list_reverse:
                        self.__debt_list_reverse[name_2][name] = self.__debt_list[name][name_2] + change_val
                    else:
                        self.__debt_list_reverse[name_2] = {name: change_val}
                else:
                    self.__debt_list[name][name_2] = change_val
                    if name_2 in self.__debt_list_reverse:
                        self.__debt_list_reverse[name_2][name] = self.__debt_list_reverse[name_2][name] + change_val
                    else:
                        self.__debt_list_reverse[name_2] = {name: change_val}
            else:
                self.__debt_list[name] = {name_2: change_val}
                self.__debt_list_reverse[name_2]= {name: change_val}
        else:
            if name in self.__debt_list:
                if name_2 in self.__debt_list_reverse:
                    self.__debt_list[name][name_2] = change_val
                    self.__debt_list_reverse[name_2][name]= change_val
                else:
                    self.__debt_list[name][name_2] = change_val
                    self.__debt_list_reverse[name_2] = {name: change_val}
            elif name_2 in self.__debt_list_reverse:
                self.__debt_list[name] = {name_2: change_val}
                self.__debt_list_reverse[name_2][name] = change_val        
            else:
                self.__debt_list[name] = {name_2: change_val}
                self.__debt_list_reverse[name_2] = {name: change_val}
        if name in self.__debt_list:
            if name_2 in self.__debt_list[name]:
                if self.__debt_list[name][name_2] == 0:
                    del self.__debt_list[name][name_2]
                    if not len(self.__debt_list[name]):
                        del self.__debt_list[name]
        if name_2 in self.__debt_list_reverse:
            if name in self.__debt_list_reverse[name_2]:
                if self.__debt_list_reverse[name_2][name] == 0:
                    del self.__debt_list_reverse[name_2][name]
                    if not len(self.__debt_list_reverse[name_2]):
                        del self.__debt_list_reverse[name_2]
        self.__try_save_debt_list(self.file_path)
