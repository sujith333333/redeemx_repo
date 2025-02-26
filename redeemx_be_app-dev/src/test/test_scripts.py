# from unittest.mock import MagicMock, patch, ANY
# import pytest
# from src.scripts import fun

# @patch("src.scripts.pymysql.connect")
# def test_fun_success(mock_connect):
#     # Mock the cursor and connection
#     mock_cursor = MagicMock()
#     mock_connection = MagicMock()
#     mock_connection.__enter__.return_value = mock_connection
#     mock_connection.cursor.return_value = mock_cursor
#     mock_connect.return_value = mock_connection

#     # Mock database connection parameters
#     mock_host = "mock_host"
#     mock_user = "mock_user"
#     mock_password = "mock_password"
#     mock_database = "mock_database"

#     # Call the function
#     fun(mock_host, mock_user, mock_password, mock_database)

#     # Assert the SQL query and parameters
#     mock_cursor.execute.assert_called_once_with(
#         "INSERT INTO user (id, created_at, name, username, password, emp_id, email, mobile_number, is_admin, is_vendor, is_user) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
#         (ANY, ANY, "admin", "admin", ANY, "admin", "john.doe@example.com", 987078907, True, False, False),
#     )

#     # Assert the connection was committed
#     mock_connection.commit.assert_called_once()



# @patch("src.scripts.pymysql.connect")
# def test_fun_failure(mock_connect):
#     mock_connect.side_effect = Exception("Database connection failed")

#     # Define mock parameters
#     mock_host = "mock_host"
#     mock_user = "mock_user"
#     mock_password = "mock_password"
#     mock_database = "mock_database"

#     with pytest.raises(Exception, match="Database connection failed"):
#         fun(mock_host, mock_user, mock_password, mock_database)
#     mock_connect.assert_called_once()
