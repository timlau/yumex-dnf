# -*- coding: utf-8 -*-
#    Yum Exteder (yumex) - A graphic package management tool
#    Copyright (C) 2013 -2021 Tim Lauridsen < timlau<AT>fedoraproject<DOT>org >
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to
#    the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

import logging

from gi.repository import Gtk
import yumex.common.const as const
from yumex.common import _, CONFIG, pkg_id_to_full_name

logger = logging.getLogger("yumex.gui.views")


class HistoryPackageView(Gtk.TreeView):
    """History Package View Class"""

    def __init__(self, base):
        Gtk.TreeView.__init__(self)
        self.model = self.setup_view()
        self.base = base

    def setup_view(self):
        """Create Notebook list for single page"""
        model = Gtk.TreeStore(str)
        self.set_model(model)
        cell = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn(_("History Packages"), cell, markup=0)
        column.set_resizable(True)
        # column1.set_fixed_width(200)
        self.append_column(column)
        # model.set_sort_column_id(0, Gtk.SortType.ASCENDING)
        return model

    def reset(self):
        self.model.clear()

    def populate(self, data):
        self.model.clear()
        # Order by package name.arch
        names = {}
        names_pair = {}
        for elem in data:
            pkg_id, state, is_inst = elem
            (name, _, _, _, arch, _) = str(pkg_id).split(",")
            name_arch = f"{name}.{arch}"
            if state in const.HISTORY_UPDATE_STATES:  # part of a pair
                if name_arch in names_pair:
                    # this is the updating pkg
                    if state in const.HISTORY_NEW_STATES:
                        names_pair[name_arch].insert(0, elem)  # add first in list
                    else:
                        names_pair[name_arch].append(elem)
                else:
                    names_pair[name_arch] = [elem]
            else:
                names[name_arch] = [elem]

        # order by primary state
        states = {}
        # pkgs without relatives
        for name_arch in sorted(list(names)):
            pkg_list = names[name_arch]
            pkg_id, state, is_inst = pkg_list[
                0
            ]  # Get first element (the primary (new) one )
            if state in states:
                states[state].append(pkg_list)
            else:
                states[state] = [pkg_list]
        # pkgs with releatives
        for name_arch in sorted(list(names_pair)):
            pkg_list = names_pair[name_arch]
            pkg_id, state, is_inst = pkg_list[
                0
            ]  # Get first element (the primary (new) one )
            if state in states:
                states[state].append(pkg_list)
            else:
                states[state] = [pkg_list]
        # apply packages to model in right order
        for state in const.HISTORY_SORT_ORDER:
            if state in states:
                num = len(states[state])
                cat = self.model.append(
                    None, [f"<b>{const.HISTORY_STATE_LABLES[state]} ({num})</b>"]
                )
                for pkg_list in states[state]:
                    pkg_id, _, is_inst = pkg_list[0]
                    if is_inst:
                        color = CONFIG.conf.color_install
                        fullname = pkg_id_to_full_name(pkg_id)
                        name = f'<span foreground="{color}">{fullname}</span>'
                    else:
                        name = pkg_id_to_full_name(pkg_id)
                    pkg_cat = self.model.append(cat, [name])
                    if len(pkg_list) == 2:
                        pkg_id, _, is_inst = pkg_list[1]
                        name = pkg_id_to_full_name(pkg_id)
                        self.model.append(pkg_cat, [name])
        self.expand_all()
