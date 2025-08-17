class IntWrapperBool:
    def __init__(self, value):
        self.value = 1 if value else 0
    
    def __bool__(self):
        return self.value == 1
    
    def __repr__(self):
        return str(self.value == 1)
    
    def __and__(self, other):
        return IntWrapperBool(bool(self) and bool(other))
    
    def __or__(self, other):
        return IntWrapperBool(bool(self) or bool(other))
    
    def __xor__(self, other):
        return IntWrapperBool(bool(self) ^ bool(other))
    
    def __invert__(self):
        return IntWrapperBool(not bool(self))

TRUE = IntWrapperBool(True)
FALSE = IntWrapperBool(False)
# IntWrapperBool(True) is IntWrapperBool(True) = False

class BooleanValue:
    truthy_instance = None
    falsy_instance = None

    def __new__(cls, logical_value):
        if logical_value:
            if cls.truthy_instance is None:
                cls.truthy_instance = super().__new__(cls)
            return cls.truthy_instance
        else:
            if cls.falsy_instance is None:
                cls.falsy_instance = super().__new__(cls)
            return cls.falsy_instance

    def __repr__(self):
        return str(self is self.__class__.truthy_instance)

    def __bool__(self):
        return self is self.__class__.truthy_instance

    def __and__(self, other):
        return BooleanValue(bool(self) and bool(other))

    def __or__(self, other):
        return BooleanValue(bool(self) or bool(other))
        
    def __xor__(self, other):
        return BooleanValue(bool(self) ^ bool(other))

    def __invert__(self):
        return BooleanValue(not bool(self))

TRUE = BooleanValue(True)
FALSE = BooleanValue(False)