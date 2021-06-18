
from typing import Any, Dict, List

from .constants import TRACKED_OBJECT_NAMES

class DataService():
    def __init__(self, config: Dict[str, Any]) -> List:
        self.config = config
        
        # validate
        assert "added" in config

        pass
    
    def to_nested_list(self) -> List[List]:
        added = self.config["added"]

        data = []
        for goal in added:
            # order should match GoalTableModel headers
            row = [goal["slug"], TRACKED_OBJECT_NAMES[goal["type"]], goal["enabled"]]
            data.append(row)

        return data
        
    def to_dict(self) -> Dict[str, Any]:
        raise NotImplementedError
