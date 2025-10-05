from rel.crud_operations import ResourceClient
from app import API_BASE

quiz_table = ResourceClient(base_url=API_BASE, endpoint_path="/quizzes/")

#quiz_table.create(json_payload)
# quiz_table.get_one(id)
# quiz_table.get_all()
# quiz_table.update(id, json_payload)