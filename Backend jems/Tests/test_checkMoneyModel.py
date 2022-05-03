from pytest import fixture, main
import sys

sys.path.insert(1, 'C:/Users/dvir tayeb/PycharmProjects/jemsProject/Backend jems')
import Models


class TestMoneyModel:

    @fixture
    def input_val(self):
        input_v = 5
        return input_v

    def test_calculate_cash_per_hour(self, input_val):
        moneyTest = Models.Money
        print("Hello")
        assert input_val == 4


main(plugins=[TestMoneyModel()])
