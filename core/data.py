import pandas as pd
import base64
from pickle import loads


class DataPD:

    _data_frame = None
    _src_data = None

    def __init__(self, data=None):
        self._src_data = data
        # self._data_frame = pd.read_pickle(filepath_or_buffer=data, compression='xz')
        self._data_frame = loads(base64.b64decode(data.encode()))

    @property
    def src_data(self):
        return self._src_data

    @property
    def data_frame(self):
        return self._data_frame

    def get_indexes(self):
        return self._data_frame.index
