# con_thing_master
Main thing contract which owns con_thing_info

## create_thing(thing_string: str, description: str)
### Arguments
- thing_string: as string representation of the thing that is to be unique
- description: a description of the unique thing

### Purpose
Creates a unique thing in the smart contract

### Asserts
- uid already exists in state

## buy_thing(uid: str):
### Arguments
- uid: unique id of the thing you want to buy

### Purpose
Transfers ownership of the thing after transferring the "price" in TAU from tx sender to owner.
This requires a previous tx to currency.approve to give "con_thing_master" permission to transfer on the sender's behalf

### Asserts
- price > 0, "thing is not for sale"
- if price_hold: price_hold == tx sender, "thing is being held for someone else"
- (in currency contract) TAU balance of tx sender == allowance provided for con_thing_master


## sell_thing(uid: str, amount: int)
### Arguments
- uid: unique id of the thing you want to sell (must be owner of thing)
- amount: the amount, in TAU, to list thing for

### Purpose
Allows the owner of a thing to set a price, in TAU, that the thing can be bought for.

### Asserts
- owner == tx sender, "thing not owned by sender"

## sell_thing_to(uid: str, amount: int, hold: str)
### Arguments
- uid: unique id of the thing you want to sell (must be owner of thing)
- amount: the amount, in TAU, to list thing for
- hold: supply a vk to make the sale exclusive to this person

### Purpose
Allows the owner of a thing to set a price, in TAU, that the thing can be bought for.
This thing can only be bought by the person who matches the "hold" value.

### Asserts
- owner == tx sender, "thing not owned by sender"

## give_thing_to(uid: str, new_owner: str):
### Arguments
- uid: unique id of the thing you want to sell (must be owner of thing)
- new_owner: the vk to transfer ownership to

### Purpose
Allows the transfer of a thing without a TAU transaction

### Asserts
- owner == tx sender, "thing not owned by sender"
- owner != new_owner, "thing already owned by new_owner"

## like_thing_to(uid: str):
### Arguments
- uid: unique id of the thing you want to sell (must be owner of thing)

### Purpose
Allows any lamden user to like a thing.
One vk can only like a think once

### Asserts
- ['likes'][uid]['tx sender'] == None, "can only like a thing once"