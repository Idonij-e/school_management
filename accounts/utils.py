from datetime import datetime


def generate_school_id():
    from .models import User 
    try:
        current_year = datetime.now().year
        user_count = User.objects.filter(created_at__year__gte=current_year).count() + 100
        print("B{}".format(str(current_year)) + str(user_count))
        return "B{}".format(str(current_year)) + str(user_count)
    except: 
        return "B{}100".format(str(datetime.now().year))
