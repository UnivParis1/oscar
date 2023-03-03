from app.data.entity_factory import EntityFactory
from app.output.output_handler import OutputHandler


class TestOutputHandler:

    def test_error_entity_detection(self):
        entity = EntityFactory.entity_class("error")()
        assert OutputHandler._error_entity(entity)
