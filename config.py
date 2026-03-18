#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# config.py
#
# This script configures any changes to the pyproject.toml file.
# This could be, for example, version changes to the package.
#

import sys
import re
import os
import tomlkit as tk


class EditPyProject:
    """
    https://realpython.com/python-toml/
    """
    FILENAME = 'pyproject.toml'
    CHG_FIELDS = {'project': ('version', 'classifiers')}

    def start(self):
        # Get vesion info
        data = self.version()
        return self.edit_pyproject(data)

    def version(self):
        data = {}
        regex0 = r'(?m)(^{}[\s]*=[\s]*(?P<ver>\d*)$)'
        regex1 = r'''(?m)(^{}[\s]*=[\s]*['"](?P<status>\d - .*)['"]$)'''

        with open(os.path.join(os.path.dirname(__file__), 'include.mk')) as f:
            ver = f.read()

        major = re.search(regex0.format('MAJORVERSION'), ver).group('ver')
        minor = re.search(regex0.format('MINORVERSION'), ver).group('ver')
        patch = re.search(regex0.format('PATCHLEVEL'), ver).group('ver')
        status = re.search(regex1.format('STATUS'), ver).group('status')
        # Look for a tag indicating a pre-release candidate. ex. rc1
        env_value = os.environ.get('PR_TAG', '')
        data['version'] = "{}.{}.{}{}".format(major, minor, patch, env_value)
        data['classifiers'] = status
        return data

    def update_version(self, config, table, field, items, version):
        old_ver = config[table][field]

        if old_ver != version:
            config[table][field] = version
            items.append((f"Old version: {old_ver}"))
            items.append((f"New version: {version}"))

    def update_classifier_status(self, config, table, field, items, status):
        ser_str = 'Development Status :: '

        for idx, classifier in enumerate(config[table][field]):
            if classifier.startswith(ser_str):
                old_classifier = classifier
                new_classifier = f"{ser_str}{status}"

                if old_classifier != new_classifier:
                    items.append(f"Old classifier: {old_classifier}")
                    items.append(f"New classifier: {new_classifier}")
                    config[table][field][idx] = new_classifier

                break

    __UPDATE_METHODS = {
        'version': update_version,
        'classifiers': update_classifier_status,
        }

    def edit_pyproject(self, new_data):
        data = {}

        with open(self.FILENAME, mode="rt", encoding="utf-8") as fp:
            config = tk.load(fp)

            for table, fields in self.CHG_FIELDS.items():
                items = data.setdefault(table, [])

                for field in fields:
                    value = new_data[field]
                    self.__UPDATE_METHODS[field](self, config, table, field,
                                                 items, value)

        with open(self.FILENAME, mode="wt", encoding="utf-8") as fp:
            tk.dump(config, fp)

        return data


if __name__ == "__main__":
    epp = EditPyProject()
    ret = 0
    changes = epp.start()
    chg_flag = [items for table, items in changes.items() if items] != []

    if chg_flag:
        print(f"Changes made to {EditPyProject.FILENAME}:")

        for table, items in changes.items():
            if items:
                print(f"{table}:")

                for idx, item in enumerate(items):
                    print(f"{items[idx]}")
    else:
        print(f"There were no changes to {EditPyProject.FILENAME}")

    sys.exit(ret)
