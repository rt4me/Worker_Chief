'''This Class will be setup to have a common layout for participants'''
from dataclasses import dataclass, field
import string

@dataclass
class Participant:

    fname: str
    lname: str
    car_class: str
    car_num: int
    work_req: str
    member_id: int
    med_fg: bool = False
    work_assign: str = ''
    work_heat_override: int = 0
    run_heat_override: int = 0
    active: bool = True



# test1 = Participant(fname = 'Tim', lname = 'Test', car_class = 'GS' , car_num = 88, work_req = 'BOD', member_id = 12345 )
# test2 = Participant(fname = 'Jill', lname = 'James', car_class = 'XP' , car_num = 5, work_req = 'Corner', member_id = 98765 )
# test_list = [test1, test2]
# print(test1)
# print(test_list)
# for x in test_list:
#     print(x.__dict__['lname'])