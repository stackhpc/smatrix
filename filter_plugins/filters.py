from ansible.errors import AnsibleError, AnsibleFilterError
from ansible.utils.display import Display
from collections import defaultdict, MutableMapping
import jinja2
from ansible.module_utils.six import string_types
import os.path
import re
import itertools
import json

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

def map_loop_results(results, attr, default=None):
    """ Take a results attribute from a looped registered task, and convert it into a dict of item->attr
        If the loop item is a dict, it is converted into a json string to make it usable as a dict key.
        If 'attr' is not presnet in the task (e.g. because it's been skipped in a loop) then use 'default' if provided else error.
    """
    output = {}
    for res in results:
        if isinstance(res['item'], dict):
            key = json.dumps(res['item'])
        else:
            key = res['item']
        output[key] = res.get(attr, default)
    return output

class FilterModule(object):
    
    def filters(self):
        return {
            'dict2product': dict2product,
            'is_subset_in': is_subset_in,
            'map_loop_results': map_loop_results,
        }
