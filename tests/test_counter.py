import pytest
import uuid

# we need to import the unit under test - counter
from src.counter import app 

# we need to import the file that contains the status codes
from src import status 

@pytest.fixture()
def client():
    return app.test_client()

@pytest.fixture()
def unique_counter_name():
    """Generate a unique counter name for testing."""
    return f"counter-{uuid.uuid4()}"

@pytest.mark.usefixtures("client")
class TestCounterEndPoints:
    """Test cases for Counter-related endpoints"""

    def test_create_a_counter(self, client, unique_counter_name):
        """It should create a counter"""
        result = client.post(f'/counters/{unique_counter_name}')
        assert result.status_code == status.HTTP_201_CREATED     

    def test_duplicate_a_counter(self, client, unique_counter_name):
        """It should return an error for duplicates"""
        result = client.post(f'/counters/{unique_counter_name}')
        assert result.status_code == status.HTTP_201_CREATED
        result = client.post(f'/counters/{unique_counter_name}')
        assert result.status_code == status.HTTP_409_CONFLICT
    
    def test_update_a_counter(self, client, unique_counter_name):
        result = client.post(f'/counters/{unique_counter_name}')
        assert result.status_code == status.HTTP_201_CREATED
        original_count = result.json[unique_counter_name]
        result = client.put(f'/counters/{unique_counter_name}')
        assert result.status_code == status.HTTP_200_OK
        new_count = result.json[unique_counter_name]
        assert original_count + 1 == new_count

    def test_get_counter(self, client, unique_counter_name):
        result = client.post(f'/counters/{unique_counter_name}')
        assert result.status_code == status.HTTP_201_CREATED
        original_count = result.json[unique_counter_name]
        result = client.get(f'/counters/{unique_counter_name}')
        assert result.status_code == status.HTTP_200_OK
        returned_count = result.json[unique_counter_name]
        assert original_count == returned_count

    def test_del_counter(self, client, unique_counter_name):
        result = client.post(f'/counters/{unique_counter_name}')
        assert result.status_code == status.HTTP_201_CREATED
        result = client.delete(f'/counters/{unique_counter_name}')
        assert result.status_code == status.HTTP_204_NO_CONTENT
        result = client.get(f'/counters/{unique_counter_name}')
        assert result.status_code == status.HTTP_404_NOT_FOUND

    def test_del_counter_not_present(self, client):
        counter_name = f'/counters/counter-{uuid.uuid4()}'
        result = client.delete(counter_name)
        assert result.status_code == status.HTTP_404_NOT_FOUND
