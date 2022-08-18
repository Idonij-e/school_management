from datetime import datetime
from sqlite3 import OperationalError as SQLOperationalError
from django.db.utils import OperationalError as DjangoOperationalError


def generate_school_id():
    from .models import User 
    try:
        current_year = datetime.now().year
        user_count = User.objects.filter(date_joined__year=current_year).count()
        if user_count == 0:
            return "B0000000"
        return "B{}".format(str(current_year)) + str(user_count+1+100)
    except SQLOperationalError: 
        return "B0000000"
    except DjangoOperationalError:
        return "B0000000"


