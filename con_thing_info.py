S = Hash(default_value='')

@export
def add_thing(thing_string: str, name: str, description: str, meta: dict, creator: str ):

    #Enforce the thing requirements on the standard arguments
    enforce_thing_standards(thing_string, name, description)

    # Create unique hash of the thing_string
    # Append any meta items required to make the string more unique, if necessary.
    uid = hashlib.sha256(thing_string + meta['foo'])

    # Validate the string is unique
    assert not S[uid],  thing_string + ' already exists'

    # Create unique hash of the name,
    # to weed out similar names first convert to lowercase, then remove spaces
    names_uid = hashlib.sha256(name.lower().replace(" ", ""))

    # Validate the name is unique
    assert not S['names', names_uid],  'A form of this name provided already belongs to ' + S['names', names_uid]

    # Store the uid of the name
    S['names', names_uid] = uid

    # Run Custom formatting validations on your thing_string (length, content, etc.)
    custom_string_validations(thing_string)

    # Required Values for Thing Compatibility
    S[uid] = ['thing', 'type', 'name', 'description', 'owner', 'creator', 'likes', 'price:amount', 'price:hold', 'meta_items']
    S[uid, 'thing'] = thing_string
    S[uid, 'type'] = 'text/plain'  # A mime/type or custom value that helps a 3rd party decode the thing_string.
    S[uid, 'name'] = name
    S[uid, 'description'] = description
    S[uid, 'owner'] = creator
    S[uid, 'creator'] = creator
    S[uid, 'likes'] = 0
    S[uid, 'price', 'amount'] = 0

    # Store some meta information about your Thing.
    # Meta Items defined here will be attached to your thing when returned from the block explorer.
    # Meta Items can also be appended to your thing_string before hashing, if they add to it's uniqueness.
    # Then they can be stored separately here for easy lookup later

    # Run Custom formatting validations on your thing_string (length, content, etc.)
    custom_meta_validations(meta)

    # metaitems should equal [] if no meta items are to be set
    S[uid, 'meta_items'] = ['attrib_1', 'attrib_2']
    S[uid, 'meta', 'attrib_1'] = meta['foo']
    S[uid, 'meta', 'attrib_2'] = meta['bar']

    return uid

def enforce_thing_standards(thing_string, name, description):
    assert len(thing_string) > 0, "Thing string cannot be empty."

    assert len(name) > 0, "No Name provided."
    assert len(name) <= 25, "Name too long (25 chars max)."

    assert len(description) > 0, "No description provided."
    assert len(description) <= 128, "Description too long (128 chars max)."


def custom_string_validations(thing_string):
    assert thing_string, "Thing string does not exist."

def custom_meta_validations(meta):
    assert meta['foo'], "foo meta value should exist."
    assert meta['bar'], "bar meta value should exist."

@export
def thing_exists(thing_string: str):
    uid = hashlib.sha256(thing_string)
    return S[uid]

@export
def get_owner(uid: str):
    return S[uid, 'owner']

@export
def set_price(uid: str, amount: int, hold: str):
    assert amount >= 0, 'Cannot set a negative price'
    S[uid, 'price', 'amount'] = amount

    if not hold == None:
        S[uid, 'price', 'hold'] = hold

@export
def get_price_amount(uid: str):
    return S[uid, 'price', 'amount']

@export
def get_price_hold(uid: str):
    return S[uid, 'price', 'hold']

@export
def set_owner(uid: str, owner: str):
    S[uid, 'owner'] = owner

@export
def like_thing(uid: str):
    likes = S[uid, 'likes']
    S[uid, 'likes'] = likes + 1

@export
def set_proof(uid: str, code: str):
    S[uid, 'proof'] = code