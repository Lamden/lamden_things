import unittest
from contracting.client import ContractingClient
client = ContractingClient()
with open('../currency.py') as f:
    code = f.read()
    client.submit(code, name='currency')
with open('../con_thing_info.py') as f:
    code = f.read()
    client.submit(code, name='con_thing_info', owner="con_thing_master")
with open('../con_thing_owners.py') as f:
    code = f.read()
    client.submit(code, name='con_thing_owners', owner="con_thing_master")
with open('../con_thing_master.py') as f:
    code = f.read()
    client.submit(code, name='con_thing_master')

thing1_uid = '27079f6e416094112f0a8b694424089dfe15c7927bedb22bdaafa5e6df56fe3d'
thing2_uid = '4ca9fada87f469f252658c5810c283d48b6ca826baf216fb2c4d23578df97c75'


class MyTestCase(unittest.TestCase):
    things_contract = None
    currency_contract = None

    def change_signer(self, name):
        client.signer = name
        self.things_contract = client.get_contract('con_thing_master')
        self.currency_contract = client.get_contract('currency')

    def test_01_create_thing(self):
        print("TEST CREATE A THING")
        self.change_signer('jeff')
        self.things_contract.create_thing(
            thing_string="this-is-a-thing-string",
            description="a test thing"
        )

    def test_02_create_thing_reject_dup(self):
        print("TEST CREATE A THING - NEG - DUPLICATE")
        self.change_signer('jeff')
        self.assertRaises(
            AssertionError,
            lambda: self.things_contract.create_thing(
                thing_string="this-is-a-thing-string",
                description="this thing won't work"
            )
        )

    def test_03_create_another_thing(self):
        print("TEST CREATE ANOTHER THING")
        self.change_signer('jeff')
        self.things_contract.create_thing(
            thing_string="test_03_create_another_thing",
            description="test_03_create_another_thing"
        )


    def test_04_sell_thing(self):
        print("TEST - SELL THING")
        self.change_signer('jeff')
        new_thing = self.things_contract.create_thing(
            thing_string="test_04_sell_thing",
            description="test_04_sell_thing"
        )
        self.things_contract.sell_thing(
            uid=new_thing,
            amount=2
        )

    def test_05_sell_thing_reject_not_owner(self):
        print("TEST - SELL THING - NEG - NOT OWNER")
        self.change_signer('jeff')
        new_thing = self.things_contract.create_thing(
            thing_string="test_05_sell_thing_reject_not_owner",
            description="test_05_sell_thing_reject_not_owner"
        )

        self.change_signer('stu')
        self.assertRaises(
            AssertionError,
            lambda: self.things_contract.sell_thing(
                uid=new_thing,
                amount=2
            )
        )

    def test_06_sell_thing_with_hold(self):
        print("TEST - SELL THING WITH HOLD")
        self.change_signer('jeff')
        new_thing = self.things_contract.create_thing(
            thing_string="test_06_sell_thing_with_hold",
            description="test_06_sell_thing_with_hold"
        )
        self.things_contract.sell_thing_to(
            uid=new_thing,
            amount=2,
            hold='alex'
        )

    def test_07_sell_thing_with_hold_reject_not_owner(self):
        print("TEST - SELL THING WITH HOLD - NEG - NOT OWNER")
        self.change_signer('jeff')
        new_thing = self.things_contract.create_thing(
            thing_string="test_07_sell_thing_with_hold_reject_not_owner",
            description="test_07_sell_thing_with_hold_reject_not_owner"
        )

        self.change_signer('stu')
        self.assertRaises(
            AssertionError,
            lambda: self.things_contract.sell_thing_to(
                uid=new_thing,
                amount=2,
                hold='alex'
            )
        )

    def test_08_buy_thing(self):
        print("TEST - BUY THING")
        self.change_signer('jeff')
        new_thing = self.things_contract.create_thing(
            thing_string="test_08_buy_thing",
            description="test_08_buy_thing"
        )
        self.things_contract.sell_thing(
            uid=new_thing,
            amount=2
        )

        self.change_signer('stu')
        self.currency_contract.approve(amount=2, to="con_thing_master")
        self.things_contract.buy_thing(
            uid=new_thing
        )

    def test_09_buy_thing_reject_not_for_sale(self):
        print("TEST - BUY THING - NEG - THING NOT FOR SALE")
        self.change_signer('jeff')
        new_thing = self.things_contract.create_thing(
            thing_string="test_9_buy_thing_reject_not_for_sale",
            description="test_9_buy_thing_reject_not_for_sale"
        )

        self.change_signer('stu')
        self.currency_contract.approve(amount=2, to="con_thing_master")
        self.assertRaises(
            AssertionError,
            lambda: self.things_contract.buy_thing(
                uid=new_thing
            )
        )

    def test_10_buy_thing_reject_on_hold(self):
        print("TEST - BUY THING - NEG - THING ON HOLD FOR SOMEONE ELSE")
        self.change_signer('jeff')
        new_thing = self.things_contract.create_thing(
            thing_string="test_10_buy_thing_reject_on_hold",
            description="test_10_buy_thing_reject_on_hold"
        )

        self.things_contract.sell_thing_to(
            uid=new_thing,
            amount=2,
            hold='alex'
        )
        self.change_signer('stu')
        self.currency_contract.approve(amount=2, to="con_thing_master")
        self.assertRaises(
            AssertionError,
            lambda: self.things_contract.buy_thing(
                uid=new_thing
            )
        )

    def test_11_buy_thing_reject_already_owned(self):
        print("TEST - BUY THING - NEG - ALREADY OWNED")
        self.change_signer('jeff')
        new_thing = self.things_contract.create_thing(
            thing_string="test_11_buy_thing_reject_already_owned",
            description="test_11_buy_thing_reject_already_owned"
        )
        self.things_contract.sell_thing_to(
            uid=new_thing,
            amount=2
        )
        self.currency_contract.approve(amount=2, to="con_thing_master")
        self.assertRaises(
            AssertionError,
            lambda: self.things_contract.buy_thing(
                uid=new_thing
            )
        )

    def test_12_give_thing(self):
        print("TEST - GIVE THING")
        self.change_signer('jeff')
        new_thing = self.things_contract.create_thing(
            thing_string="test_12_give_thing",
            description="test_12_give_thing"
        )
        self.things_contract.give_thing(
            uid=new_thing,
            new_owner='stu'
        )

    def test_13_give_thing_reject_not_owner(self):
        print("TEST - BUY THING - NEG - ALREADY OWNED")
        self.change_signer('jeff')
        new_thing = self.things_contract.create_thing(
            thing_string="test_13_give_thing_reject_not_owner",
            description="test_13_give_thing_reject_not_owner"
        )
        self.change_signer('stu')
        self.currency_contract.approve(amount=2, to="con_thing_master")
        self.assertRaises(
            AssertionError,
            lambda: self.things_contract.give_thing(
                uid=new_thing,
                new_owner='alex'
            )
        )

if __name__ == '__main__':
    unittest.main()
