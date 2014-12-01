#
# This file is part of pySMT.
#
#   Copyright 2014 Andrea Micheli and Marco Gario
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
from functools import wraps
import warnings

import pysmt.shortcuts

class deprecated(object):
    """This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emmitted
    when the function is used."""

    def __init__(self, alternative=None):
        self.alternative = alternative

    def __call__(self, func):
        def newFunc(*args, **kwargs):
            alt = ""
            if self.alternative is not None:
                alt = " You should call %s() instead!" % self.alternative
            warnings.warn("Call to deprecated function %s().%s" % \
                          (func.__name__, alt),
                          category=DeprecationWarning,
                          stacklevel=2)
            return func(*args, **kwargs)
        newFunc.__name__ = func.__name__
        newFunc.__doc__ = func.__doc__
        newFunc.__dict__.update(func.__dict__)
        return newFunc


def clear_pending_pop(f):
    """Pop the solver stack (if necessary) before calling the function.

    Some functions (e.g., get_value) required the state of the solver
    to stay unchanged after a call to solve. Therefore, we can leave
    th solver in an intermediate state in which there is a formula
    asserted in the stack that is not needed (e.g., when solving under
    assumptions). In order to guarantee that methods operate on the
    correct set of formulae, all methods of the solver that rely on
    the assertion stack, need to be marked with this decorator.
    """

    @wraps(f)
    def wrapper(self, *args, **kwargs):
        if self.pending_pop:
            self.pending_pop = False
            self.pop()
        return f(self, *args, **kwargs)
    return wrapper


def typecheck_result(f):
    """Performs type checking on the return value using the global environment"""

    @wraps(f)
    def wrapper(*args, **kwargs):
        res = f(*args, **kwargs)
        pysmt.shortcuts.get_type(res)
    return wrapper
