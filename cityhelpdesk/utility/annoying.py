# coding=utf-8
"""
Annoying sets of helpers that are used with Django and other Python projects.
"""

from __future__ import unicode_literals
import string
from django.core.exceptions import ObjectDoesNotExist
from django.utils.crypto import get_random_string
from django.utils.deconstruct import deconstructible
from django.http import Http404
import uuid
import os


# pylint: disable-msg=R0903
class AllIps (object):
    """Hack class to pretend every IP is an internal one."""
    def __init__(self):
        pass

    def __contains__(self, ip):
        return True


def get_env(k, default=None):
    """Simplified environment fetch."""
    v = os.environ.get(k, None)
    if v is None:
        return default
    return v


def get_int(k, default=0):
    """Simplified environment fetch passing into a `int` cast."""
    v = get_env(k, default)
    try:
        return int(v)
    except (TypeError, ValueError):
        return default


def get_str(k, default=""):
    """Simplified environment fetch returning a utf-8 decoded string."""
    v = get_env(k)
    if v is not None:
        return v
    return default


def get_bool(k, default=False):
    """Simplified environment fetch returning a boolean value. Normalizes
    integers according to built-in logic (i.e. ``0`` returns False``). Strings
    ``"true"`` and ``"t"`` normalize to ``True``, everything else is
    ``False``."""

    v = get_str(k).lower().strip()
    if v == "":
        return default
    try:
        return not not int(v)
    except ValueError:
        if v == "true" or v == "t":
            return True
        return False


def fetch_env(name=".env"):
    env = {}
    contents = []
    try:
        with open(name, "r") as env_file:
            contents = env_file.readlines()
    except IOError:
        print("Unable to read {0}".format(name))
        return env

    clean_lines = [line.strip() for line in contents if line.strip()]
    if not clean_lines:
        print("No lines read from {0}".format(name))

    for line in clean_lines:
        if "=" not in line:
            print("Skipping malformed line: {0}".format(line))
            continue

        # Split out the variable name from the contents
        name, contents = line.split("=", 1)

        # Clean the name and contents slightly
        name = name.strip().upper()
        contents = contents.strip()
        if contents[0] == contents[-1] and contents[0] in {"'", '"'}:
            contents = contents[1:-1]

        # Push that into the environment
        env[name] = contents

    return env


def make_uuid():
    """Returns a ``uuid.uuid4().hex``."""
    return str(uuid.uuid4().hex)


def get_or_none(Model, *args, **kw):
    """Suppress that annoying ObjectDoesNotExist shit."""
    obj = None

    # While you can force this check by specifying ``use_objects`` this
    # is a catch for being lazy.
    use_objects = kw.pop("use_objects", None)
    if use_objects is None:
        # Do some reflection to figure out if we should use Model.objects.get
        # or just Model.get
        if hasattr(Model, "objects"):
            use_objects = True
        else:
            use_objects = False

    if use_objects:
        get = Model.objects.get
    else:
        get = Model.get

    try:
        obj = get(**kw)
    except ObjectDoesNotExist:
        pass
    except ValueError:
        pass
    return obj
# Shortcut function
gon = get_or_none


def get_or_gone(*args, **kwargs):
    """Raises Http404 if the object doesn't exist."""
    obj = get_or_none(*args, **kwargs)
    if not obj:
        raise Http404
    return obj
# Shortcut function
gog = get_or_gone


def default_if_none(obj, default):
    """Allows you to set a default value to something if it is None."""
    if obj is None:
        return default
    return obj
# Shortcut function
din = default_if_none


def tree_get(obj, *args):
    """Love this function."""
    val = obj
    for arg in args:
        if val is None:
            return None
        if callable(arg):
            val = arg(val)
        elif isinstance(val, dict):
            val = val.get(arg)
        elif isinstance(val, (list, tuple)):
            try:
                val = val[arg]
            except IndexError:
                return None
        elif isinstance(val, object):
            val = getattr(val, arg, None)
        else:
            # ``val`` is something we can't operate on
            return None
        if val is None:
            return None
    return val


@deconstructible
class UploadAndRename(object):
    """ Helper function for upload model-fields."""

    def __init__(self, dest):
        """ Set destination app"""
        self.dest = dest

    def __call__(self, instance, filename):
        """ Rename file path."""
        args = [instance._meta.app_label, self.dest]
        rand = get_random_string(10, string.ascii_lowercase)
        args.append("{0}_{1}".format(rand, filename))
        return "/".join(args)
