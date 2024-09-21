import requests
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from job_extractor_app.models import Postulation


def get_keycloak_users(token):
    # URL to fetch users from Keycloak (replace with your Keycloak URL and realm)
    keycloak_url = "http://localhost:8080/admin/realms/master/users"

    headers = {
        "Authorization": f"Bearer {token}",  # Pass the token in the Authorization header
        "Content-Type": "application/json"
    }

    response = requests.get(keycloak_url, headers=headers)
    print(response)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching users from Keycloak: {response.status_code}")

def get_user_tasks(user_id):
    # Query the database for tasks associated with the given Keycloak user ID
    tasks = ['task1', 'task2']
    return tasks

@api_view(['POST'])
def get_users_with_tasks(request):
    # Extract the Authorization header
    auth_header = request.headers.get('Authorization')

    # Ensure that the Authorization header is present and starts with "Bearer "
    if not auth_header or not auth_header.startswith('Bearer '):
        return Response({"error": "Authorization token not provided or invalid"}, status=401)

    # Extract the token (remove "Bearer " from the header)
    token = auth_header.split(' ')[1]

    try:
        # Use the token to fetch users from Keycloak
        users = get_keycloak_users(token)

        result = []

        # Loop through the Keycloak users and fetch tasks for each user
        for user in users:
            user_id = user['id']  # Keycloak user ID
            tasks = get_user_tasks(user_id)  # Fetch tasks for this user

            user_info = {
                "user_id": user_id,
                "username": user['username'],
                "email": user.get('email', 'No email provided'),
                "tasks": []  # Convert tasks queryset to a list of dictionaries
            }
            result.append(user_info)

        return Response(result)  # Return the combined result as JSON

    except Exception as e:
        # Handle any errors that occur while fetching users or tasks
        return Response({"error": str(e)}, status=500)


@api_view(['GET'])
def find_postulation_by_id(id_postulation):
    return get_object_or_404(Postulation, id=id_postulation)
