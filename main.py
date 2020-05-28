from contracting.client import ContractingClient
client = ContractingClient()
client.flush()

with open('./currency.py') as f:
    code = f.read()
    client.submit(code, name='currency')
with open('./con_thing_info.py') as f:
    code = f.read()
    client.submit(code, name='con_thing_info', owner="con_thing_master")
with open('./con_thing_owners.py') as f:
    code = f.read()
    client.submit(code, name='con_thing_owners', owner="con_thing_master")
with open('./con_thing_master.py') as f:
    code = f.read()
    client.submit(code, name='con_thing_master')


print ('JEFF CREATES SOME THINGS ----------------------')
client.signer = 'jeff'
things_contract = client.get_contract('con_thing_master')
currency_contract = client.get_contract('currency')

print(' ')
print ('CURRENCY BALANCES ----------------------')
print ('JEFF currency balance: ' + str(currency_contract.get_balance(who='jeff')))
print ('STU currency balance: ' + str(currency_contract.get_balance(who='stu')))
print ('ALEX currency balance: ' + str(currency_contract.get_balance(who='alex')))

print(' ')
print ('JEFF CREATES SOME THINGS ----------------------')
thing1 = things_contract.create_thing(
    thing_string="this-is-a-thing-string",
    description="a test thing"
)

thing2 = things_contract.create_thing(
    thing_string="this-is-another-thing-string",
    description="a test thing"
)
print(' ')

print ('JEFF LISTS HIS THINGS FOR SALE ----------------------')
things_contract.sell_thing(uid=thing1, amount=2)
things_contract.sell_thing(uid=thing2, amount=2)

client.signer = 'stu'
things_contract = client.get_contract('con_thing_master')
currency_contract = client.get_contract('currency')


print(' ')
print ('STU BUYS A THING ----------------------')
currency_contract.approve(amount=5, to="con_thing_master")
things_contract.buy_thing(uid=thing1)
things_contract.show_things_by_owner(owner="jeff")
things_contract.show_things_by_owner(owner="stu")
things_contract.show_owner_of_thing(uid=thing1)

print(' ')
print ('CURRENCY BALANCES ----------------------')
print ('JEFF currency balance: ' + str(currency_contract.get_balance(who='jeff')))
print ('STU currency balance: ' + str(currency_contract.get_balance(who='stu')))
print ('ALEX currency balance: ' + str(currency_contract.get_balance(who='alex')))

print(' ')
print ('STU LISTS HIS THING FOR SALE ----------------------')
things_contract.sell_thing(uid=thing1, amount=2)

client.signer = 'alex'
things_contract = client.get_contract('con_thing_master')
currency_contract = client.get_contract('currency')
print(' ')
print ('ALEX BUYS THE TWO THINGS ----------------------')
currency_contract.approve(amount=4, to="con_thing_master")
things_contract.buy_thing(uid=thing1)
things_contract.buy_thing(uid=thing2)

print(' ')
print ('CURRENCY BALANCES ----------------------')
print ('JEFF currency balance: ' + str(currency_contract.get_balance(who='jeff')))
print ('STU currency balance: ' + str(currency_contract.get_balance(who='stu')))
print ('ALEX currency balance: ' + str(currency_contract.get_balance(who='alex')))

print(' ')
print ('ALEX GIVES A THING AWAY ----------------------')
things_contract.give_thing(uid=thing2, new_owner='stu')

print(' ')
print ('ALEX LIST AN ITEM FOR JEFF TO BUY ----------------------')
things_contract.sell_thing_to(uid=thing1, amount=5, hold="jeff")


print(' ')
print ('JEFF BUYS A THING ON HOLD FOR HIM ----------------------')
client.signer = 'jeff'
things_contract = client.get_contract('con_thing_master')
currency_contract = client.get_contract('currency')
currency_contract.approve(amount=5, to="con_thing_master")
things_contract.buy_thing(uid=thing1)