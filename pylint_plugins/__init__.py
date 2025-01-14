from pylint_plugins.import_checker import ImportChecker
from pylint_plugins.assign_checker import AssignChecker


def register(linter):
    linter.register_checker(ImportChecker(linter))
    linter.register_checker(AssignChecker(linter))
