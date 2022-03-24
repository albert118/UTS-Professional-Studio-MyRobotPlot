import json
import logging
from types import SimpleNamespace

LOG_LVL = logging.NOTSET
logging.basicConfig(level=LOG_LVL)
_logger = logging.getLogger(__name__)


class Deserializer:
    def Deserialize(self, data):
        try:
            return json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        except json.JSONDecodeError as e:
            _logger.error(f"{e} raised by JSONDecoder while attempting to decode '{data}' to SimpleNamespace")
            if(LOG_LVL is logging.DEBUG or LOG_LVL is logging.NOTSET):
                input('=== CHECK THE ERROR AND POTENTIALLY UPDATE THE PRE-CLEANING METHOD(S) ===')
                raise
            else:
                return None
        except Exception as e:
            _logger.debug(f"when json loading '{str(e)}'")
            input()
            _logger.error(f"Decoding serial data failed to parse with error '{e}'")
            return None
