# -*- coding: utf-8 -*-

import re

from enchant.tokenize import Filter


class HtmlEntitiesFilter(Filter):
    """Filter ignore HTML entities.
        Apply:
            WhatEver&SomeThing;WhatEver
    This filter skips any words matching the following regular expression:
        [\w]*&[\w]*;[\w]*
    """
    _pattern = re.compile(r"[\w]*&[\w]*[\w]*")

    def _skip(self, word):
        if self._pattern.match(word):
            return True
        return False


class sprintfParametersFilter(Filter):
    """Filter ignore php sprintf params.
        Apply:
            %NUMBER$s
    This filter skips any words matching the following regular expression:
        %[\0-9]+\$s
    """
    _pattern = re.compile(r"%[\0-9]+\$s")

    def _skip(self, word):
        if self._pattern.match(word):
            return True
        return False
