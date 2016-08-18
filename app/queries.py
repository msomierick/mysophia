from ..models import Student


for s in Student.query.all():
    print s
