#!/usr/bin/env python
# -*- coding: utf-8 -*-
# <Lettuce - Behaviour Driven Development for python>
# Copyright (C) <2010-2011>  Gabriel Falcão <gabriel@nacaolivre.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import os
import sys
import optparse

import lettuce


def main(args=sys.argv[1:]):
    base_path = os.path.join(os.path.dirname(os.curdir), 'features')
    parser = optparse.OptionParser(
        usage="%prog or type %prog -h (--help) for help",
        version=lettuce.version)

    parser.add_option("-v", "--verbosity",
                      dest="verbosity",
                      default=4,
                      help='The verbosity level')

    parser.add_option("-s", "--scenarios",
                      dest="scenarios",
                      default=None,
                      help='Comma separated list of scenarios to run')

    parser.add_option("-t", "--tags",
                      dest="tags",
                      default=None,
                      help='Comma separated list of tags to run')

    parser.add_option("--disable-overlap",
                      dest="disable_overlap",
                      action="store_true",
                      default=False,
                      help="Disable overlapping in colored shell output. "
                        "Use it with colored output in places, where ANSI escape sequences not supported")

    parser.add_option("--with-xunit",
                      dest="enable_xunit",
                      action="store_true",
                      default=False,
                      help='Output JUnit XML test results to a file')

    parser.add_option("--xunit-file",
                      dest="xunit_file",
                      default=None,
                      type="string",
                      help='Write JUnit XML to this file. Defaults to '
                      'lettucetests.xml')

    parser.add_option("--with-html",
        dest="enable_html",
        action="store_true",
        default=False,
        help='Output test results to a html-file')

    parser.add_option("--html-file",
        dest="html_file",
        default=None,
        type="string",
        help='Write html to this file. Defaults to '
             'lettucetests.html')

    options, args = parser.parse_args()
    if args:
        base_path = os.path.abspath(args[0])

    try:
        options.verbosity = int(options.verbosity)
    except ValueError:
        pass

    with_tags = None
    without_tags = None
    if options.tags:
        with_tags = []
        without_tags = []
        tags = options.tags.split(',')
        for tag in tags:
            if tag:
                if tag.find('~') is 0:
                    without_tags.append(tag[1:])
                else:
                    with_tags.append(tag)

        if len(with_tags) is 0: with_tags = None
        if len(without_tags) is 0: without_tags = None


    runner = lettuce.Runner(
        base_path,
        scenarios=options.scenarios,
        verbosity=options.verbosity,
        enable_xunit=options.enable_xunit,
        xunit_filename=options.xunit_file,
        enable_html=options.enable_html,
        html_filename=options.html_file,
        disable_overlap=options.disable_overlap,
        with_tags = with_tags,
        without_tags = without_tags
    )

    result = runner.run()
    if not result or result.steps != result.steps_passed:
        raise SystemExit(1)

if __name__ == '__main__':
    main()
