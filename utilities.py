import decimal
from decimal import Decimal

class GeneralMethods:
    @staticmethod
    def is_number(x):
        try:
            Decimal(x)
            return True
        except ValueError:
            return False
        except decimal.InvalidOperation:
            return False
    @staticmethod
    def it_exists(var: str, index: int) -> bool:
        if  not var:
            raise Exception(f'{var} does not exist')
        else:
            if (index > 0 and index > len(var) - 1) or (index < 0 and index < len(var) * -1):
                return False
            else:
                return True

class ManagerMethods:
    def __init__(self, manager_instance, evaluator_instance):
        self.manager = manager_instance
        self.evaluator = evaluator_instance

    def pop_input(self, pop: int = -1) -> str:
        if not self.manager.expr:
            return self.manager.expr
        else:
            try:
                expr_list: list[str] = list(self.manager.expr)
                expr_list.pop(pop)
                self.manager.expr = ''.join(expr_list)
            except IndexError:
                raise IndexError
            return self.manager.expr

    def get_expr(self):
        return self.manager.get_expr()

    def all_clear(self):
        self.manager.expr = ''

    def add_expr(self, value: str):
        self.manager.expr += value

    def request_update_display(self, value: str):
        self.manager.widget.update_display(value=value)

    def evaluate(self, stage: int):
        try:
            result = self.evaluator.run(expr=self.manager.get_expr(), stage=stage)
            return result
        except ValueError:
            return f'Mismatched Parentheses'
        except IndexError:
            return f'Invalid Input'
        except ZeroDivisionError:
            return f'Division by Zero'
        except Exception as e:
            print(repr(e))
            return None
