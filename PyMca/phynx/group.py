"""
"""

from __future__ import absolute_import, with_statement

import posixpath

import h5py
import numpy as np

from .base import _PhynxProperties
from .dataset import Axis, Dataset, Signal
from .exceptions import H5Error
from .registry import registry
from .utils import sorting, sync


class Group(h5py.Group, _PhynxProperties):

    """
    """

    @property
    @sync
    def entry(self):
        try:
            target = self['/'.join(self.name.split('/')[:2])]
            assert isinstance(target, registry['Entry'])
            return target
        except AssertionError:
            return None

    @property
    @sync
    def measurement(self):
        try:
            return self.entry.measurement
        except AttributeError:
            return None

    @property
    def parent(self):
        return self[posixpath.split(self.name)[0]]

    @property
    @sync
    def signals(self):
        return dict(
            [(posixpath.split(s.name)[-1], s) for s in self.iterobjects()
                if isinstance(s, Signal)]
        )

    @property
    @sync
    def axes(self):
        return dict(
            [(posixpath.split(a.name)[-1], a) for a in self.iterobjects()
                if isinstance(a, Axis)]
        )

    def __init__(self, parent_object, name, create=False, **attrs):
        """
        Open an existing group or create a new one.

        attrs is a python dictionary of strings and numbers to be saved as hdf5
        attributes of the group.

        """
        with parent_object.plock:
            h5py.Group.__init__(self, parent_object, name, create=create)
            if create:
                self.attrs['class'] = self.__class__.__name__
                try:
                    self.attrs['NX_class'] = self.nx_class
                except AttributeError:
                    pass

            _PhynxProperties.__init__(self, parent_object)

            if attrs:
                for attr, val in attrs.iteritems():
                    if not np.isscalar(val):
                        val = str(val)
                    self.attrs[attr] = val

    @sync
    def __repr__(self):
        try:
            return '<%s group "%s" (%d members, %d attrs)>' % (
                self.__class__.__name__,
                self.name,
                len(self),
                len(self.attrs)
            )
        except Exception:
            return "<Closed %s group>" % self.__class__.__name__

    @sync
    def __getitem__(self, name):
        # TODO: would be better to check the attribute without having to
        # create create the group twice. This might be possible with the
        # 1.8 API.
        item = super(Group, self).__getitem__(name)
        if 'class' in item.attrs:
            return registry[item.attrs['class']](self, name)
        elif 'NX_class' in item.attrs:
            return registry[item.attrs['NX_class']](self, name)
        elif isinstance(item, h5py.Dataset):
            return Dataset(self, name)
        else:
            return Group(self, name)

    @sync
    def __setitem__(self, name, value):
        super(Group, self).__setitem__(name, value)

    @sync
    def get_sorted_axes_list(self, direction=1):
        return sorted([a for a in self.axes.values() if a.axis==direction])

    @sync
    def get_sorted_signals_list(self, direction=1):
        return sorted([s for s in self.signals.values()])

    def create_dataset(self, name, *args, **kwargs):
        type = kwargs.pop('type', 'Dataset')
        return registry[type](self, name, *args, **kwargs)

    @sync
    def require_dataset(self, name, *args, **kwargs):
        type = kwargs.setdefault('type', 'Dataset')
        if not name in self:
            return self.create_dataset(name, *args, **kwargs)
        else:
            item = self[name]
            if not isinstance(item, registry[type]):
                raise NameError(
                    "Incompatible object (%s) already exists" % \
                    item.__class__.__name__
                )
            return item

    def create_group(self, name, type='Group', **data):
        return registry[type](self, name, create=True, **data)

    @sync
    def require_group(self, name, type='Group', **data):
        if not name in self:
            return self.create_group(name, type, **data)
        else:
            item = self[name]
            if not isinstance(item, registry[type]):
                raise NameError(
                    "Incompatible object (%s) already exists" % \
                    item.__class__.__name__
                )
            return item

    @sync
    def listobjects(self):
        print "listobjects is deprecated, use values"
        return self.values()

    @sync
    def values(self):
        try:
            values = super(Group, self).values()
        except AttributeError:
            print "Please update to h5py-1.2"
            values = super(Group, self).listobjects()
        try:
            return self.file._sorted(values)
        except TypeError:
            return values

    @sync
    def listnames(self):
        print "listnames is deprecated, use keys"
        return self.keys()

    @sync
    def keys(self):
        return [posixpath.split(i.name)[-1] for i in self.values()]

    @sync
    def listitems(self):
        print "listitems is deprecated, use items"
        return self.items()

    @sync
    def items(self):
        return [(posixpath.split(i.name)[-1], i) for i in self.values()]


registry.register(Group)
