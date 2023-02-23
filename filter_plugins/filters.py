from ansible.errors import AnsibleError, AnsibleFilterError
from ansible.utils.display import Display
from collections import defaultdict
import jinja2
from ansible.module_utils.six import string_types
import os.path
import re
import itertools

def dict2product(d):
    """
    given
        d = {
            'a': [1, 2],
            'b': ['x', 'y'],
        }
    returns:
        [{a: 1, b: 'x'}, {a: 2, b: 'x'},  {a: 1, b: 'y'}, {a: 2, b: 'x'}]
    """
    output = []
    values = itertools.product(*d.values())
    for v in values:
        output.append(dict(zip(d.keys(), v)))
    return output

def is_subset_in(d, lst):
    """ Return True if dict d is a subset of any dict in list lst """
    d_items = d.items()
    for t in lst:
        if t.items() <= d_items:
            return True
    return False

class FilterModule(object):
    
    def filters(self):
        return {
            'dict2product': dict2product,
            'is_subset_in': is_subset_in,
        }
