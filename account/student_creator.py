from account.models import User
from booth.models import Booth
import pandas as pd
# for user in User.objects.all():
#     if user.id>75:
#         user.delete()
# df = pd.read_excel("account/students.xlsx", sheet_name='student')
# for i, r in df.iterrows():
# for i in range(1,10):
#     # booth = Booth.objects.get(id=r['Debriefing room'])
#     user_template = User.objects.get(id=72)
#     new_user = user_template
#     new_user.id = None
#     new_user.username = f"demo_student_{i}"
#     new_user.first_name = "Demo"
#     new_user.last_name = f"Student {i}"
#     new_password = User.objects.make_random_password(length=6)
#     new_user.set_password(new_password)
#     new_user.save()
#     print(new_user.username, ",", new_password)
    # df.loc[i, 'password'] = new_password
# df.to_csv('account/students_created.csv')
# new_user.save()
# print(new_user, new_password)
user_template = User.objects.get(id=465)
new_user = user_template
# new_user.id = None
# new_user.username = f"s181094416@ych2ss.edu.hk"
# new_user.first_name = "嘉駿"
# new_user.last_name = f"黃"
new_password = User.objects.make_random_password(length=6)
new_user.set_password(new_password)
new_user.save()
print(new_user.username, ",", new_password)