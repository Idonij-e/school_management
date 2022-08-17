from datetime import datetime
from sqlite3 import OperationalError as SQLOperationalError
from django.db.utils import OperationalError as DjangoOperationalError


def generate_school_id():
    from .models import User 
    try:
        current_year = datetime.now().year
        user_count = User.objects.filter(date_joined__year=current_year).count() + 101
        return "B{}".format(str(current_year)) + str(user_count)
    except SQLOperationalError: 
        return "B{}100".format(str(datetime.now().year))
    except DjangoOperationalError:
        return "B{}100".format(str(datetime.now().year))


