# -*- coding: utf-8 -*-

from . import controllers
from . import models

def pre_init_hook(cr):
    """
    With this pre-init-hook we want to add new language sensitive column to fix problem with different from latin letters words
    """
    cr.execute("""
            SELECT * FROM pg_available_extensions WHERE name = 'pg_trgm';
            """)
    if not cr.fetchone():
        cr.execute(
            """
            CREATE EXTENSION pg_trgm;
            """)

