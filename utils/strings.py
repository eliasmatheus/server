"""Helpers para manipulação de strings."""

import re
from unidecode import unidecode
from datetime import datetime


def remove_special_chars(self, title):
    """Remove caracteres especiais do título."""
    return re.sub(r"[^a-zA-Z0-9\s]", "", unidecode(title))


def replace_spaces(self, id_string):
    """Substitui espaços em branco por hífens."""
    return re.sub(r"\s+", "-", id_string)


def add_date_prefix(self, id_string):
    """Adiciona a data no início da string."""
    date = datetime.now().strftime("%Y-%m-%d")
    return f"{date}-{id_string}"


def limit_length(self, id_string, length):
    """Limita o comprimento da string."""
    return id_string[:length]
