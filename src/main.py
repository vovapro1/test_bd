
from queries.core import Work_Table
from queries.orm import Work_Table_ORM
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], "..'"))


# Work_Table.create_table()
# Work_Table.insert_data()
# Work_Table.select_workers()
# Work_Table.update_workers()

# Work_Table_ORM.create_table()
# Work_Table_ORM.insert_data()
# Work_Table_ORM.select_workers()
# Work_Table_ORM.update_workers()
# Work_Table_ORM.insert_resum()
# Work_Table_ORM.insert_additional_resumes()
# Work_Table_ORM.join_and_sort()
# Work_Table_ORM.select_workers_with_lazy_relationship()
# Work_Table_ORM.select_workers_with_joined_relationship()
# Work_Table_ORM.select_workers_with_selectin_relationship()
# Work_Table_ORM.select_wokers_with_reletionship()
# Work_Table_ORM.select_wokers_with_reletionship_contains_eager()
# Work_Table_ORM.easy_select()
Work_Table_ORM.hard_select()
