from datetime import datetime
from ntpath import join
from sqlite3 import OperationalError as SQLOperationalError
from types import NoneType
from django.db.utils import OperationalError as DjangoOperationalError
import os

from main.settings import BASE_DIR

def generate_school_id():
    from .models import User 
    try:
        current_year = datetime.now().year
        last_user_id = User.objects.last().id
        return "B{}".format(str(current_year)[-2:]) + str(last_user_id+1+1000)
    except AttributeError:
        return "B0000000"
    except SQLOperationalError: 
        return "B0000000"
    except DjangoOperationalError:
        return "B0000000"


def save_user_photo(instance, filename):
    images_path = os.path.join(BASE_DIR, "media", "images")
    for folder, subfolder, files in os.walk(images_path):
        if instance.school_id in files:
            os.remove(os.path.join(images_path, instance.school_id))
    # file_extension = filename.split('.')[-1]
    return "images/" + instance.school_id

