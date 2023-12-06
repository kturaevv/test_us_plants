from typing import List, Dict

def self_mapping(arr: List[str]) -> Dict[str, str]:
    return {key: key for key in arr}