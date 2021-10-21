import requests

def check_calculate_page():
    response = requests.get('http://localhost:3000/CalculateTips')
    print("Status: ", response)
    print("Content: ", response.content)
    r = response.json()
    print("JSON: ", r)

check_calculate_page()
