#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from difflib import SequenceMatcher

def similar(a, b):
        return SequenceMatcher(None, a, b).ratio()

def custom_sort(sub_li):
    # reverse = None (Sorts in Ascending order)
    # key is set to sort using second element of 
    # sublist lambda has been used
    sub_li.sort(key = lambda x: x[1], reverse=True)
    return sub_li

class ManageSearch:
    

    def search(self,sorted_list,param_type,param_word,param_version,param_limit):
        desired_cpe = f"cpe:2.3:{param_type}:{" ".join(param_word)}:{param_version}"
        best_matching_version = []
        if param_version != "" :
            for match in sorted_list:
                for version in match[1]:
                    current_cpe = f"{match[0]}:{version}"
                    ranking = [current_cpe,similar(desired_cpe,current_cpe)]
                    best_matching_version.append(ranking)            
            best_matching_version=custom_sort(best_matching_version)
            length = len(best_matching_version)
            # print("Len",length,"param_limit",type(param_limit),param_limit)
            if length > param_limit:
                best_matching_version=best_matching_version[:param_limit]
            best_matching_version=[c[0] for c in best_matching_version]
        else:
            best_matching_version = sorted_list
        return best_matching_version