import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "valence.settings")

import django

django.setup()

from agent.services import manage_internal_tools

def main():
    manage_internal_tools()

if __name__ == "__main__":
    main()
