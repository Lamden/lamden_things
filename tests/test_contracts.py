import unittest
import base64
from contracting.db.driver import ContractDriver, Driver
from contracting.client import ContractingClient
client = ContractingClient()

icon_svg_base64 = ""

with open('../logo.svg') as f:
    icon_svg = f.read()
    icon_svg_base64 = base64.b64encode(bytes(icon_svg, encoding='utf-8'))
    print(icon_svg_base64)

with open('./currency.py') as f:
    code = f.read()
    client.submit(code, name='currency')
with open('../con_thing_info.py') as f:
    code = f.read()
    client.submit(code, name='con_thing_info', owner="con_thing_master")
with open('../con_thing_master.py') as f:
    code = f.read()
    client.submit(
        code,
        name='con_thing_master',
        constructor_args={
            'name': 'My Thing',
            'description': 'a bunch of my things',
            'icon_svg_base64': icon_svg_base64.decode("utf-8")
        }
    )

thing1_uid = '27079f6e416094112f0a8b694424089dfe15c7927bedb22bdaafa5e6df56fe3d'
thing2_uid = '4ca9fada87f469f252658c5810c283d48b6ca826baf216fb2c4d23578df97c75'
desc_too_long = ("Too long, Too long, Too long, Too long, Too long, Too long, Too long, Too long, Too long, Too long," +
                 " Too long, Too long, Too long,")
meta = {}
meta['foo'] = 'foo'
meta['bar'] = 'bar'




class MyTestCase(unittest.TestCase):
    things_contract = None
    currency_contract = None

    def change_signer(self, name):
        client.signer = name
        self.things_contract = client.get_contract('con_thing_master')
        self.thing_info = client.get_contract('con_thing_info')
        self.currency_contract = client.get_contract('currency')

    def test_01a_create_thing(self):
        print("TEST CREATE A THING")
        self.change_signer('jeff')
        new_thing = self.things_contract.create_thing(
            thing_string="this-is-a-thing-string",
            name="A new thing!_1",
            description="a test thing",
            meta=meta
        )
        reqList = ['thing', 'type', 'name', 'description', 'owner', 'creator', 'likes', 'price:amount', 'price:hold', 'meta_items']
        self.assertEqual(self.thing_info.quick_read('S', new_thing), reqList)
        self.assertEqual(self.thing_info.quick_read('S', new_thing + ':thing'), "this-is-a-thing-string")
        self.assertEqual(self.thing_info.quick_read('S', new_thing + ':type'), "text/plain")
        self.assertEqual(self.thing_info.quick_read('S', new_thing + ':name'), "A new thing!_1")
        self.assertEqual(self.thing_info.quick_read('S', new_thing + ':description'), "a test thing")
        self.assertEqual(self.thing_info.quick_read('S', new_thing + ':owner'), "jeff")
        self.assertEqual(self.thing_info.quick_read('S', new_thing + ':creator'), "jeff")
        self.assertEqual(self.thing_info.quick_read('S', new_thing + ':likes'), 0)
        self.assertEqual(self.thing_info.quick_read('S', new_thing + ':price:amount'), 0)
        self.assertEqual(self.thing_info.quick_read('S', new_thing + ':price:hold'), None)

        self.assertEqual(self.thing_info.quick_read('S', new_thing + ':meta_items'), ['attrib_1', 'attrib_2'])
        self.assertEqual(self.thing_info.quick_read('S', new_thing + ':meta' + ':attrib_1'), 'foo')
        self.assertEqual(self.thing_info.quick_read('S', new_thing + ':meta' + ':attrib_2'), 'bar')


    def test_01b_assert_create_thing_arg_name(self):
        print("TEST - ASSERT CREATE THING ARGUEMENTS - NAME EXISTS")
        self.change_signer('jeff')
        self.assertRaises(
            AssertionError,
            lambda: self.things_contract.create_thing(
                thing_string="this is a thing string",
                description="This is a what my thing is like",
                name="",
                meta=meta
            )
        )

    def test_01c_assert_create_thing_arg_name_len(self):
        print("TEST - ASSERT CREATE THING ARGUEMENTS - NAME TOO LONG")
        self.change_signer('jeff')
        self.assertRaises(
            AssertionError,
            lambda: self.things_contract.create_thing(
                thing_string="this is a thing string",
                description="This is a what my thing is like",
                name="This name is way too long and will fail",
                meta=meta
            )
        )

    def test_01d_assert_create_thing_arg_dup_name(self):
        print("TEST - ASSERT CREATE THING ARGUEMENTS - DUP NAME")
        self.change_signer('jeff')
        self.assertRaises(
            AssertionError,
            lambda: self.things_contract.create_thing(
                thing_string="this is a thing string",
                description="This is a what my thing is like",
                name="A new thing!_1",
                meta=meta
            )
        )

    def test_01e_assert_create_thing_arg_desc(self):
        print("TEST - ASSERT CREATE THING ARGUEMENTS - DESCRIPTION EXISTS")
        self.change_signer('jeff')
        self.assertRaises(
            AssertionError,
            lambda: self.things_contract.create_thing(
                thing_string="this is a thing string",
                description="",
                name="My thing",
                meta=meta
            )
        )

    def test_01f_assert_create_thing_arg_desc_len(self):
        print("TEST - ASSERT CREATE THING ARGUEMENTS - DESCRIPTION LENGTH")
        self.change_signer('jeff')
        self.assertRaises(
            AssertionError,
            lambda: self.things_contract.create_thing(
                thing_string="this is a thing string",
                description=desc_too_long,
                name="My thing",
                meta=meta
            )
        )



    def test_02_create_thing_reject_dup(self):
        print("TEST CREATE A THING - NEG - DUPLICATE")
        self.change_signer('jeff')
        self.assertRaises(
            AssertionError,
            lambda: self.things_contract.create_thing(
                thing_string="this-is-a-thing-string",
                name="A new thing!_2",
                description="this thing won't work",
                meta=meta
            )
        )

    def test_03_create_another_thing(self):
        print("TEST CREATE ANOTHER THING")
        self.change_signer('jeff')
        new_thing = self.things_contract.create_thing(
            thing_string="test_03_create_another_thing",
            name="A new thing!_3a",
            description="test_03_create_another_thing",
            meta=meta
        )

        self.assertEqual(self.thing_info.quick_read('S', new_thing + ':thing'), "test_03_create_another_thing")
        self.assertEqual(self.thing_info.quick_read('S', new_thing + ':type'), "text/plain")
        self.assertEqual(self.thing_info.quick_read('S', new_thing + ':description'), "test_03_create_another_thing")
        self.assertEqual(self.thing_info.quick_read('S', new_thing + ':owner'), "jeff")
        self.assertEqual(self.thing_info.quick_read('S', new_thing + ':creator'), "jeff")
        self.assertEqual(self.thing_info.quick_read('S', new_thing + ':likes'), 0)
        self.assertEqual(self.thing_info.quick_read('S', new_thing + ':price:amount'), 0)

    def test_04_sell_thing(self):
        print("TEST - SELL THING")
        self.change_signer('jeff')
        new_thing = self.things_contract.create_thing(
            thing_string="test_04_sell_thing",
            name="A new thing!_3b",
            description="test_04_sell_thing",
            meta=meta
        )

        self.things_contract.sell_thing(
            uid=new_thing,
            amount=2
        )

        self.assertEqual(self.thing_info.quick_read('S', new_thing + ':price:amount'), 2)
        self.assertEqual(self.thing_info.quick_read('S', new_thing + ':price:hold'), '')

    def test_05_sell_thing_reject_not_owner(self):
        print("TEST - SELL THING - NEG - NOT OWNER")
        self.change_signer('jeff')
        new_thing = self.things_contract.create_thing(
            thing_string="test_05_sell_thing_reject_not_owner",
            name="A new thing!_4",
            description="test_05_sell_thing_reject_not_owner",
            meta=meta
        )

        self.change_signer('stu')
        self.assertRaises(
            AssertionError,
            lambda: self.things_contract.sell_thing(
                uid=new_thing,
                amount=2
            )
        )
        self.assertEqual(self.thing_info.quick_read('S', new_thing + ':price:amount'), 0)

    def test_06_sell_thing_with_hold(self):
        print("TEST - SELL THING WITH HOLD")
        self.change_signer('jeff')
        new_thing = self.things_contract.create_thing(
            thing_string="test_06_sell_thing_with_hold",
            name="A new thing!_5",
            description="test_06_sell_thing_with_hold",
            meta=meta
        )
        self.things_contract.sell_thing_to(
            uid=new_thing,
            amount=2,
            hold='alex'
        )

        self.assertEqual(self.thing_info.quick_read('S', new_thing + ':price:amount'), 2)
        self.assertEqual(self.thing_info.quick_read('S', new_thing + ':price:hold'), 'alex')

    def test_07_sell_thing_with_hold_reject_not_owner(self):
        print("TEST - SELL THING WITH HOLD - NEG - NOT OWNER")
        self.change_signer('jeff')
        new_thing = self.things_contract.create_thing(
            thing_string="test_07_sell_thing_with_hold_reject_not_owner",
            name="A new thing!_6",
            description="test_07_sell_thing_with_hold_reject_not_owner",
            meta=meta
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

        self.assertEqual(self.thing_info.quick_read('S', new_thing + ':price:amount'), 0)

    def test_08_buy_thing(self):
        print("TEST - BUY THING")
        self.change_signer('jeff')
        new_thing = self.things_contract.create_thing(
            thing_string="test_08_buy_thing",
            name="A new thing!_7",
            description="test_08_buy_thing",
            meta=meta
        )
        self.things_contract.sell_thing(
            uid=new_thing,
            amount=2
        )

        jeff_balance_before = self.currency_contract.quick_read('balances', 'jeff')
        stu_balance_before = self.currency_contract.quick_read('balances', 'stu')

        self.change_signer('stu')
        self.currency_contract.approve(amount=2, to="con_thing_master")
        self.things_contract.buy_thing(
            uid=new_thing
        )

        jeff_balance_after = self.currency_contract.quick_read('balances', 'jeff')
        stu_balance_after = self.currency_contract.quick_read('balances', 'stu')

        self.assertEqual(jeff_balance_before + 2, jeff_balance_after)
        self.assertEqual(stu_balance_before - 2, stu_balance_after)

        self.assertEqual(self.thing_info.quick_read('S', new_thing + ':owner'), 'stu')
        self.assertEqual(self.thing_info.quick_read('S', new_thing + ':creator'), 'jeff')
        self.assertEqual(self.thing_info.quick_read('S', new_thing + ':price:amount'), 0)
        self.assertEqual(self.thing_info.quick_read('S', new_thing + ':price:hold'), '')

    def test_085_buy_thing_for_you(self):
        print("TEST - BUY THING FOR YOU")
        self.change_signer('jeff')
        new_thing = self.things_contract.create_thing(
            thing_string="test_085_buy_thing_for_you",
            name="A new thing!_8",
            description="test_085_buy_thing_for_you",
            meta=meta
        )
        self.things_contract.sell_thing_to(
            uid=new_thing,
            amount=2,
            hold="stu"
        )

        jeff_balance_before = self.currency_contract.quick_read('balances', 'jeff')
        stu_balance_before = self.currency_contract.quick_read('balances', 'stu')

        self.change_signer('stu')
        self.currency_contract.approve(amount=2, to="con_thing_master")
        self.things_contract.buy_thing(
            uid=new_thing
        )

        jeff_balance_after = self.currency_contract.quick_read('balances', 'jeff')
        stu_balance_after = self.currency_contract.quick_read('balances', 'stu')

        self.assertEqual(jeff_balance_before + 2, jeff_balance_after)
        self.assertEqual(stu_balance_before - 2, stu_balance_after)

        self.assertEqual(self.thing_info.quick_read('S', new_thing + ':owner'), 'stu')
        self.assertEqual(self.thing_info.quick_read('S', new_thing + ':creator'), 'jeff')
        self.assertEqual(self.thing_info.quick_read('S', new_thing + ':price:amount'), 0)
        self.assertEqual(self.thing_info.quick_read('S', new_thing + ':price:hold'), '')

    def test_09_buy_thing_reject_not_for_sale(self):
        print("TEST - BUY THING - NEG - THING NOT FOR SALE")
        self.change_signer('jeff')
        new_thing = self.things_contract.create_thing(
            thing_string="test_9_buy_thing_reject_not_for_sale",
            name="A new thing!_9",
            description="test_9_buy_thing_reject_not_for_sale",
            meta=meta
        )

        jeff_balance_before = self.currency_contract.quick_read('balances', 'jeff')
        stu_balance_before = self.currency_contract.quick_read('balances', 'stu')

        self.change_signer('stu')
        self.currency_contract.approve(amount=2, to="con_thing_master")
        self.assertRaises(
            AssertionError,
            lambda: self.things_contract.buy_thing(
                uid=new_thing
            )
        )
        jeff_balance_after = self.currency_contract.quick_read('balances', 'jeff')
        stu_balance_after = self.currency_contract.quick_read('balances', 'stu')

        self.assertEqual(jeff_balance_before, jeff_balance_after)
        self.assertEqual(stu_balance_before, stu_balance_after)

        self.assertEqual(self.thing_info.quick_read('S', new_thing + ':owner'), 'jeff')
        self.assertEqual(self.thing_info.quick_read('S', new_thing + ':price:amount'), 0)

    def test_10_buy_thing_reject_on_hold(self):
        print("TEST - BUY THING - NEG - THING ON HOLD FOR SOMEONE ELSE")
        self.change_signer('jeff')
        new_thing = self.things_contract.create_thing(
            thing_string="test_10_buy_thing_reject_on_hold",
            name="A new thing!_10",
            description="test_10_buy_thing_reject_on_hold",
            meta=meta
        )

        jeff_balance_before = self.currency_contract.quick_read('balances', 'jeff')
        stu_balance_before = self.currency_contract.quick_read('balances', 'stu')

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

        jeff_balance_after = self.currency_contract.quick_read('balances', 'jeff')
        stu_balance_after = self.currency_contract.quick_read('balances', 'stu')

        self.assertEqual(jeff_balance_before, jeff_balance_after)
        self.assertEqual(stu_balance_before, stu_balance_after)

        self.assertEqual(self.thing_info.quick_read('S', new_thing + ':owner'), 'jeff')
        self.assertEqual(self.thing_info.quick_read('S', new_thing + ':price:amount'), 2)
        self.assertEqual(self.thing_info.quick_read('S', new_thing + ':price:hold'), 'alex')

    def test_11_buy_thing_reject_already_owned(self):
        print("TEST - BUY THING - NEG - ALREADY OWNED")
        self.change_signer('jeff')
        new_thing = self.things_contract.create_thing(
            thing_string="test_11_buy_thing_reject_already_owned",
            name="A new thing!_11",
            description="test_11_buy_thing_reject_already_owned",
            meta=meta
        )
        self.things_contract.sell_thing_to(
            uid=new_thing,
            amount=2
        )

        jeff_balance_before = self.currency_contract.quick_read('balances', 'jeff')
        stu_balance_before = self.currency_contract.quick_read('balances', 'stu')

        self.currency_contract.approve(amount=2, to="con_thing_master")
        self.assertRaises(
            AssertionError,
            lambda: self.things_contract.buy_thing(
                uid=new_thing
            )
        )

        jeff_balance_after = self.currency_contract.quick_read('balances', 'jeff')
        stu_balance_after = self.currency_contract.quick_read('balances', 'stu')

        self.assertEqual(jeff_balance_before, jeff_balance_after)
        self.assertEqual(stu_balance_before, stu_balance_after)

        self.assertEqual(self.thing_info.quick_read('S', new_thing + ':owner'), 'jeff')
        self.assertEqual(self.thing_info.quick_read('S', new_thing + ':price:amount'), 2)

    def test_12_give_thing(self):
        print("TEST - GIVE THING")
        self.change_signer('jeff')
        new_thing = self.things_contract.create_thing(
            thing_string="test_12_give_thing",
            name="A new thing!_12",
            description="test_12_give_thing",
            meta=meta
        )

        jeff_balance_before = self.currency_contract.quick_read('balances', 'jeff')
        stu_balance_before = self.currency_contract.quick_read('balances', 'stu')

        self.things_contract.give_thing(
            uid=new_thing,
            new_owner='stu'
        )

        jeff_balance_after = self.currency_contract.quick_read('balances', 'jeff')
        stu_balance_after = self.currency_contract.quick_read('balances', 'stu')

        self.assertEqual(jeff_balance_before, jeff_balance_after)
        self.assertEqual(stu_balance_before, stu_balance_after)

        self.assertEqual(self.thing_info.quick_read('S', new_thing + ':owner'), 'stu')
        self.assertEqual(self.thing_info.quick_read('S', new_thing + ':creator'), 'jeff')
        self.assertEqual(self.thing_info.quick_read('S', new_thing + ':price:amount'), 0)

    def test_13_give_thing_reject_not_owner(self):
        print("TEST - GIVE THING - NEG - NOT OWNER")
        self.change_signer('jeff')
        new_thing = self.things_contract.create_thing(
            thing_string="test_13_give_thing_reject_not_owner",
            name="A new thing!_13",
            description="test_13_give_thing_reject_not_owner",
            meta=meta
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

        self.assertEqual(self.thing_info.quick_read('S', new_thing + ':owner'), 'jeff')
        self.assertEqual(self.thing_info.quick_read('S', new_thing + ':creator'), 'jeff')
        self.assertEqual(self.thing_info.quick_read('S', new_thing + ':price:amount'), 0)

    def test_14_like_thing(self):
        print("TEST - LIKE THING")
        self.change_signer('jeff')
        new_thing = self.things_contract.create_thing(
            thing_string="test_14_like_thing",
            name="A new thing!_14",
            description="test_14_like_thing",
            meta=meta
        )
        self.assertEqual(self.thing_info.quick_read('S', new_thing + ':likes'), 0)
        self.things_contract.like_thing(uid=new_thing)
        self.assertEqual(self.thing_info.quick_read('S', new_thing + ':likes'), 1)
        self.assertEqual(self.thing_info.quick_read('S', new_thing + ':owner'), 'jeff')

    def test_15_like_thing_only_once(self):
        print("TEST - LIKE THING - NEG - CAN ONLY ONCE")
        self.change_signer('jeff')
        new_thing = self.things_contract.create_thing(
            thing_string="test_15_like_thing_only_once",
            name="A new thing!_15",
            description="test_15_like_thing_only_once",
            meta=meta
        )
        self.assertEqual(self.thing_info.quick_read('S', new_thing + ':likes'), 0)

        self.things_contract.like_thing(uid=new_thing)
        self.assertEqual(self.thing_info.quick_read('S', new_thing + ':likes'), 1)

        self.change_signer('stu')
        self.things_contract.like_thing(uid=new_thing)
        self.assertEqual(self.thing_info.quick_read('S', new_thing + ':likes'), 2)
        self.assertRaises(
            AssertionError,
            lambda: self.things_contract.like_thing(uid=new_thing)
        )
        self.assertEqual(self.thing_info.quick_read('S', new_thing + ':likes'), 2)

        self.assertEqual(self.thing_info.quick_read('S', new_thing + ':owner'), 'jeff')

    def test_16_prove_ownership(self):
        print("TEST - PROVE OWNERSHIP")
        self.change_signer('jeff')
        new_thing = self.things_contract.create_thing(
            thing_string="test_16_prove_ownership",
            name="A new thing!_16",
            description="test_16_prove_ownership",
            meta=meta
        )

        self.assertEqual(self.thing_info.quick_read('S', new_thing + ':owner'), 'jeff')

        self.things_contract.prove_ownership(uid=new_thing, code='12345')

        self.assertEqual(self.thing_info.quick_read('S', new_thing + ':proof'), '12345')

    def test_17_prove_ownership_(self):
        print("TEST - PROVE OWNERSHIP - NOT OWNER")
        self.change_signer('jeff')
        new_thing = self.things_contract.create_thing(
            thing_string="test_17_prove_ownership_neg",
            name="A new thing!_17",
            description="test_17_prove_ownership_neg",
            meta=meta
        )

        self.assertEqual(self.thing_info.quick_read('S', new_thing + ':owner'), 'jeff')

        self.change_signer('stu')
        self.assertRaises(
            AssertionError,
            lambda: self.things_contract.prove_ownership(uid=new_thing, code='12345')
        )


if __name__ == '__main__':
    unittest.main()
