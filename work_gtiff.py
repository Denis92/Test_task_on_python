from typing import NamedTuple, Union

import gdal
import numpy
import uuid


class InputDataError(Exception):
    """
    Exception for fail data
    """
    def __init__(self, message: str = ''):
        self.message = message
        super().__init__(self.message)


class SaveGTiif(NamedTuple):
    """
    Create param for save GTiff
    """
    bands: int
    raster: list
    output_file: str = ''
    projection: str = ''
    transform: tuple = tuple()
    xsize: int = 0
    ysize: int = 0


class BaseGTiffWork:
    """
    Base class for GTiff
    """
    def __init__(self, input_file: str) -> None:
        """

        :param input_file:
        """
        self.gdalData = gdal.Open(input_file)
        if self.gdalData is None:
            raise InputDataError(message=f'File {input_file} not found')

    def get_raster(self, number_channel: int) -> Union[numpy.ndarray, None]:
        """

        :param number_channel:
        :return:
        """
        gdal_band = self.gdalData.GetRasterBand(number_channel)
        raster = gdal_band.ReadAsArray()
        return raster

    def save_gtiff(self, save_param: SaveGTiif) -> None:
        """

        :param save_param:
        """
        try:
            update_save_param = {}
            default_param = {'xsize': self.gdalData.RasterXSize,
                             'ysize': self.gdalData.RasterYSize,
                             'projection': self.gdalData.GetProjection(),
                             'transform': self.gdalData.GetGeoTransform(),
                             'output_file': f'output_{uuid.uuid4().hex}.tiff'}
            for key, value in save_param._asdict().items():
                if not value:
                    update_save_param[key] = default_param.get(key)
                else:
                    update_save_param[key] = value
            save_param_new = SaveGTiif(**update_save_param)
            format_file = "GTiff"
            driver = gdal.GetDriverByName(format_file)
            dt = gdal.GDT_Byte
            output_data = driver.Create(save_param_new.output_file,
                                        save_param_new.xsize,
                                        save_param_new.ysize,
                                        save_param_new.bands,
                                        dt)
            output_data.SetProjection(save_param_new.projection)
            output_data.SetGeoTransform(save_param_new.transform)
            for item_array in range(save_param_new.bands):
                output_data.GetRasterBand(item_array + 1).WriteArray(save_param_new.raster[item_array])
            print(f'File {save_param_new.output_file} created')
        except Exception as e:
            print(f'Error save: {e}')


class CalculationNDWI(BaseGTiffWork):
    """
    Class for calculation NDWI
    """

    def __init__(self, input_file: str) -> None:
        """

        :param input_file:
        """
        super().__init__(input_file)

    def get_ndwi(self) -> Union[numpy.ndarray, None]:
        """

        :return:
        """
        try:
            green_channel = self.get_raster(2)
            infrared_channel = self.get_raster(4)
            sum_channel = numpy.add(green_channel, infrared_channel)
            subtract_channel = numpy.subtract(green_channel, infrared_channel)
            with numpy.errstate(divide='ignore', invalid='ignore'):
                ndwi = numpy.true_divide(subtract_channel, sum_channel)
                ndwi[~ numpy.isfinite(ndwi)] = 0
            return ndwi
        except Exception as e:
            print(f'Error get ndwi: {e}')

    def get_binary_ndwi(self, binarization_threshold: float = 0.0) -> Union[numpy.ndarray, None]:
        """

        :return:
        """
        ndwi = self.get_ndwi()
        if ndwi is None:
            raise InputDataError('NDWI is none')
        ndwi_binary = numpy.where(ndwi <= binarization_threshold, 0, 255)
        return ndwi_binary
