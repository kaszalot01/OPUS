from opus.lang.exceptions import IdentityDict


def test_identity_dict():

    d = IdentityDict({"a": "b", "b": "c"})
    assert d['a'] == 'b'
    assert d['b'] == 'c'
    assert d['c'] == 'c'
    assert d['ziemniaki'] == 'ziemniaki'
    assert d[42] == 42
