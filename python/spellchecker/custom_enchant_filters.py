# -*- coding: utf-8 -*-

import re

from enchant.tokenize import Filter

class HtmlEntitiesFilter(Filter):
    """Filter skipping some HTML entities.
        Apply:
            &SOMETHING;
    This filter skips any words matching the following regular expression:
        &[\w]*;
    """
    _pattern = re.compile(r"&[\w]*")

    def _skip(self, word):
        if self._pattern.match(word):
            return True
        return False
