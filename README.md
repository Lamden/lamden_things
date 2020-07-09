# con_thing_master
Main thing contract which owns con_thing_info

## create_thing(thing_string: str, description: str)
### Arguments
- thing_string: as string representation of the thing that is to be unique
- name: A name for this thing, which will be unique to the contract (max 25chars). 
Names are formatted to lowercase and all spaces removed. This is done to enforce uniqueness.
- description: a description of the unique thing (max 128chars)
- meta: A dictionary object for passing in meta info about the thing which is outside of the required
thing data.

### Purpose
Creates a unique thing in the smart contract

### Asserts
- uid already exists in state
- description exists and has a length <= 128
- name exits, is unique, and has a length <= 25
- thing_string exists

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

## prove_ownership(uid: str, code: str):
### Arguments
- uid: unique id of the thing you want to prove you own
- code: a code you will store as the proof

### Purpose
Allows a user to prove they own an item by storing a code associated with that thing.

### Asserts
- owner == tx sender, "thing not owned by sender"