import io
from pathlib import Path
import pickle
import copy

class Zebt():
    def __init__(self, file_path = Path("ZebtList.pickle")):
        self.file_path = file_path
        self.__try_load_zebt_list(self.file_path)
        pass

    def __try_save_zebt_list(self, save_path):    
        with open(save_path, "wb+") as writer:
            pickle.dump((self.__zebt_list, self.__zebt_list_reverse), writer)

    def __try_load_zebt_list(self, load_path):
        if load_path.exists():
            with open(load_path, "rb") as reader:
                    self.__zebt_list, self.__zebt_list_reverse = pickle.load(reader)
        else:
            self.__zebt_list = {}
            self.__zebt_list_reverse = {}

    def __get_zebt_list(self):
        #if len(self.__zebt_list):
        return copy.deepcopy(self.__zebt_list), copy.deepcopy(self.__zebt_list_reverse)
        #return 1, 2
    
    def __set_zebt_list(self, zebt_list):
        print("DONT CALL THIS FUNCTION")
        self.__zebt_list = zebt_list
        #TODO: Set __zebt_list_reverse
        self.__zebt_list_reverse = {}
        self.__try_save_zebt_list(self.file_path)

    zebt_list = property(__get_zebt_list, __set_zebt_list)

    def update_zebt(self, name, name_2, change_text):
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
            if name in self.__zebt_list:
                if name_2 in self.__zebt_list[name]:
                    self.__zebt_list[name][name_2] = self.__zebt_list[name][name_2] + change_val
                    if name_2 in self.__zebt_list_reverse:
                        self.__zebt_list_reverse[name_2][name] = self.__zebt_list[name][name_2] + change_val
                    else:
                        self.__zebt_list_reverse[name_2] = {name: change_val}
                else:
                    self.__zebt_list[name][name_2] = change_val
                    if name_2 in self.__zebt_list_reverse:
                        self.__zebt_list_reverse[name_2][name] = self.__zebt_list_reverse[name_2][name] + change_val
                    else:
                        self.__zebt_list_reverse[name_2] = {name: change_val}
            else:
                self.__zebt_list[name] = {name_2: change_val}
                self.__zebt_list_reverse[name_2]= {name: change_val}
        else:
            if name in self.__zebt_list:
                if name_2 in self.__zebt_list_reverse:
                    self.__zebt_list[name][name_2] = change_val
                    self.__zebt_list_reverse[name_2][name]= change_val
                else:
                    self.__zebt_list[name][name_2] = change_val
                    self.__zebt_list_reverse[name_2] = {name: change_val}
            elif name_2 in self.__zebt_list_reverse:
                self.__zebt_list[name] = {name_2: change_val}
                self.__zebt_list_reverse[name_2][name] = change_val        
            else:
                self.__zebt_list[name] = {name_2: change_val}
                self.__zebt_list_reverse[name_2] = {name: change_val}
        if name in self.__zebt_list:
            if name_2 in self.__zebt_list[name]:
                if self.__zebt_list[name][name_2] == 0:
                    del self.__zebt_list[name][name_2]
                    if not len(self.__zebt_list[name]):
                        del self.__zebt_list[name]
        if name_2 in self.__zebt_list_reverse:
            if name in self.__zebt_list_reverse[name_2]:
                if self.__zebt_list_reverse[name_2][name] == 0:
                    del self.__zebt_list_reverse[name_2][name]
                    if not len(self.__zebt_list_reverse[name_2]):
                        del self.__zebt_list_reverse[name_2]
        self.__try_save_zebt_list(self.file_path)