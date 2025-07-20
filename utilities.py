

class GeneralMethods:
    @staticmethod
    def is_number(x):
        try:
            float(x)
            return True
        except ValueError:
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
