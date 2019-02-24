from abc import ABC, abstractmethod


class VariableNotFoundError(LookupError):
    def __init__(self, variable):
        super().__init__(f"{variable}: variable not found")


class IEnvironment(ABC):
    @abstractmethod
    def add(self, variable: str, value: str) -> None:
        """
        Add variable in environment
        :param variable: str
        :param value: str
        """
        pass

    @abstractmethod
    def contains(self, variable: str) -> bool:
        """
        Return True if variable exist otherwise return False
        :param variable: str
        """
        pass

    @abstractmethod
    def remove(self, variable: str) -> bool:
        """
        Return True if variable was removed otherwise False
        :param variable: str
        """
        pass

    @abstractmethod
    def get(self, variable: str) -> str:
        """
        Retrieve value of variable
        :param variable: str
        """
        pass


def create_environment() -> IEnvironment:
    return EnvironmentImpl()


##################
# Implementation #
##################


class EnvironmentImpl(IEnvironment):
    def __init__(self):
        self.env = dict()

    def add(self, variable: str, value: str) -> None:
        self.env[variable] = value

    def contains(self, variable: str) -> bool:
        return self.env.__contains__(variable)

    def remove(self, variable: str) -> bool:
        if self.contains(variable):
            self.env.__delitem__(variable)
            return True
        return False

    def get(self, variable: str) -> str:
        if self.contains(variable):
            return self.env[variable]
        raise VariableNotFoundError(variable)
