import abc


class UnavailableError(Exception):
    pass


class NominalError(Exception):
    pass


class CurrencyError(Exception):
    pass


class ATMBase(abc.ABC):
    @abc.abstractmethod
    def put(self, currency, nominal, count):
        pass

    @abc.abstractmethod
    def get(self, currency, amount):
        pass


class ATM(ATMBase):
    CURRENCIES = ['RUB', 'USD', 'EUR']
    NOMINALS = [1, 5, 10, 50, 100, 500, 1000, 5000]

    def __init__(self):
        self._state = {
            currency: {
                nominal: 0 for nominal in ATM.NOMINALS
            } for currency in ATM.CURRENCIES
        }

    def _check_currency(self, currency):
        if currency not in self.CURRENCIES:
            raise CurrencyError(
                f"Currency {currency} doesn't exist for this ATM",
            )

    def _check_nominal(self, nominal):
        if nominal not in self.NOMINALS:
            raise NominalError(
                f"Denomination (nominal) {nominal} doesn't exist for this ATM",
            )

    def put(self, currency, nominal, count):
        self._check_currency(currency)
        self._check_nominal(nominal)
        self._state[currency][nominal] += count

    def get(self, currency, amount):
        self._check_currency(currency)
        money = {}
        sm = 0
        for nominal in self.NOMINALS[::-1]:
            count = (amount - sm) // nominal
            if not count or not self._state[currency][nominal]:
                continue
            if count >= self._state[currency][nominal]:
                money[nominal] = self._state[currency][nominal]
            else:
                money[nominal] = count
            sm += money[nominal] * nominal
            if sm == amount:
                break
        if sm != amount:
            raise UnavailableError()
        result = []
        for nominal, count in money.items():
            self._state[currency][nominal] -= count
            result.append((nominal, count))
        return result


