import pytest
from httpx import AsyncClient

special_key=None
reftoken=None

@pytest.mark.asyncio
async def test_login_user_admin_login_post(testing_client):
            """Test case for login_user_admin_login_post

            Login User
            """
            async with AsyncClient(app=testing_client, base_url="http://test") as client:
                login_user_model = {"password":"password","grant_type":"authorization_code","username":"Bushu","token":"none"}
                
                headers = {
                    'accept': 'application/json',
                    'Content-Type': 'application/json'
                }
                response = await client.post(
                    "/admin/login",
                    headers={},
                    json=login_user_model,
                )
               
            assert response.status_code == 500
                # uncomment below to assert the status code of the HTTP response
                # ##############################################################################
            async with AsyncClient(app=testing_client, base_url="http://test") as client:
                login_user_model = {
                        "grant_type": "authorization_code",
                        "username": "superspecial",
                        "password": "password",
                        "token": "none"
                                }
                
                headers = {
                    'accept': 'application/json',
                    'Content-Type': 'application/json'
                }
                response2 = await client.post(
                    "/admin/login",
                    headers=headers,
                    json=dict(login_user_model),
                )
            global reftoken
            global special_key
            
            reftoken=response2.json()["refresh_token"]
            special_key=response2.json()["access_token"]
                
            assert response2.status_code == 200
           
            # ####################################################################################
            async with AsyncClient(app=testing_client, base_url="http://test") as client:
                login_user_model = {
                        "grant_type": "authorization_code",
                        "username": "superspecial",
                        "password": "password3",
                        "token": "none"
                                }
                
                headers = {
                    'accept': 'application/json',
                    'Content-Type': 'application/json'
                }
                response3 = await client.post(
                    "/admin/login",
                    headers=headers,
                    json=dict(login_user_model),
                )     
            assert response3.json() == {"Message":"Invalid Password"}
            assert response3.status_code == 200
                # ####################################################################################
            async with AsyncClient(app=testing_client, base_url="http://test") as client:  
                login_user_model = {"password":"password","grant_type":"refresh_token","username":"superspecial","token":reftoken}
                
                headers = {
                    'accept': 'application/json',
                    'Content-Type': 'application/json'
                }
                response4 = await client.post(
                    "/admin/login",
                    headers=headers,
                    json=login_user_model,
                )

                # uncomment below to assert the status code of the HTTP response
            assert response4.status_code == 200
            # #################################################################################### 
            # ####################################################################################
            async with AsyncClient(app=testing_client, base_url="http://test") as client:  
                login_user_model = {"password":"password","grant_type":"refresh_token","username":"superspecial","token":'assdfasd'}
                
                headers = {
                    'accept': 'application/json',
                    'Content-Type': 'application/json'
                }
                response5 = await client.post(
                    "/admin/login",
                    headers=headers,
                    json=login_user_model,
                )

                # uncomment below to assert the status code of the HTTP response
            assert response5.status_code == 500
            # #################################################################################### 
            # ####################################################################################
            async with AsyncClient(app=testing_client, base_url="http://test") as client: 
                login_user_model = {"password":"password","grant_type":"token_decode","username":"Bushu","token":special_key}
                
                headers = {
                    'accept': 'application/json',
                    'Content-Type': 'application/json'
                }
                response6 = await client.post(
                    "/admin/login",
                    headers=headers,
                    json=login_user_model,
                )
                # # uncomment below to assert the status code of the HTTP response
            
            assert response6.status_code == 200
                # #################################################################################### 
            async with AsyncClient(app=testing_client, base_url="http://test") as client: 
                login_user_model = {"password":"password","grant_type":"token_decode","username":"Bushu","token":special_key+'asdfasdf'}
                
                headers = {
                    'accept': 'application/json',
                    'Content-Type': 'application/json'
                }
                response7 = await client.post(
                    "/admin/login",
                    headers=headers,
                    json=login_user_model,
                )
                # # uncomment below to assert the status code of the HTTP response
            
            assert response7.status_code == 500
                # #################################################################################### 
@pytest.mark.asyncio
async def test_get_all_users_admin_users_all_get(testing_client):
    """Test case for get_all_users_admin_users_all_get

    Get All Users
    """
    async with AsyncClient(app=testing_client, base_url="http://test") as client:
        
        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {special_key}',
                       
        }
        response = await client.get(
            "/admin/users/all",
            headers=headers,
        )
    
    print(response.json())
    assert response.status_code == 200
