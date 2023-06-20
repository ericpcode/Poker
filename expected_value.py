from abc import ABC, abstractmethod

class TreeNode(ABC):
    def __init__(self, action=None):
        self.action = action
    
    @abstractmethod
    def get_expected_value(self):
        pass

class FoldNode(TreeNode):
    def __init__(self, outcome):
        super().__init__(action="Fold")
        self.outcome = outcome
    
    def get_expected_value(self):
        return self.outcome

class RaiseNode(TreeNode):
    def __init__(self, outcome):
        super().__init__(action="Raise")
        self.outcome = outcome
    
    def get_expected_value(self):
        return self.outcome
    
# Check node
# Call node
# conditions to prevent certain children nodes ex: check node, cant be followed by fold node
# add probabilies to each node
# add leaf nodes
