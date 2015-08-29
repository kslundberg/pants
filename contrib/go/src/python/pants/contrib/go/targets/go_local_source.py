# coding=utf-8
# Copyright 2015 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (absolute_import, division, generators, nested_scopes, print_function,
                        unicode_literals, with_statement)

import os
from glob import glob

from pants.base.payload import Payload

from pants.contrib.go.targets.go_target import GoTarget


class GoLocalSource(GoTarget):

  @classmethod
  def is_go_source(cls, path):
    """Returns `True` if the file at the given `path` is a go source file."""
    return path.endswith('.go') and os.path.isfile(path)

  @classmethod
  def local_import_path(cls, source_root, address):
    """Returns the Go import path for the given address housed under the given source root.

    :param string source_root: The path of the source root the address is found within.
    :param address: The target address of a GoLocalSource target.
    :type: :class:`pants.base.address.Address`
    :raises: `ValueError` if the address does not reside within the source root.
    """
    return cls.package_path(source_root, address.spec_path)

  def __init__(self, address=None, payload=None, **kwargs):
    sources = glob(os.path.join(address.spec_path, '*.go'))
    payload = payload or Payload()
    payload.add_fields({
      'sources': self.create_sources_field(sources=sources,
                                           sources_rel_path='',
                                           key_arg='sources'),
    })
    super(GoLocalSource, self).__init__(address=address, payload=payload, **kwargs)

  @property
  def import_path(self):
    """The import path as used in import statements in `.go` source files."""
    return self.local_import_path(self.target_base, self.address)