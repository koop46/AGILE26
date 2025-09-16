from typing import Any, Dict, List
import requests


class ResourceClient:
    def __init__(self, base_url: str, endpoint_path: str):
        # """
        # Initialize API client
        # :param base_url: Base API URL (e.g., "http://localhost:8000")
        # :param endpoint_path: Resource endpoint path (e.g., "users")
        # """

        self.base_url = f"{base_url.rstrip('/')}/{endpoint_path.strip('/')}"
    
    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # """Create new resource item"""
        response = requests.post(
            f"{self.base_url}/",
            json=data,
            
        )
        response.raise_for_status()
        return response.json()
    
    def get_all(self) -> List[Dict[str, Any]]:
        # """Get all resource items"""
        response = requests.get(
            f"{self.base_url}/",
            
        )
        response.raise_for_status()
        return response.json()
    
    def get_one(self, item_id: int) -> Dict[str, Any]:
        # """Get single resource item by ID"""
        response = requests.get(
            f"{self.base_url}/{item_id}",
            
        )
        response.raise_for_status()
        return response.json()
    
    def update(self, item_id: int, update_data: Dict[str, Any]) -> Dict[str, Any]:
    #    """Update resource item"""
        response = requests.put(
            f"{self.base_url}/{item_id}",
            json=update_data,
            
        )
        response.raise_for_status()
        return response.json()
    
    def delete(self, item_id: int) -> Dict[str, Any]:
    #    """Delete resource item"""
        response = requests.delete(
            f"{self.base_url}/{item_id}",
            
        )
        response.raise_for_status()
        return response.json()
    
    def __repr__(self):
        return f"<ResourceClient for {self.base_url}>"


# client.get_all()

# client.create(
#     {
#         "username":"the_admin_man",
#         "email": "admin@power.sv",
#         "password":"123123123",
#         "is_admin": 1
#     }
# )

# client.update(
#     1,
#     {
#     "username": "dev_papi"
# })

# client.delete(4)