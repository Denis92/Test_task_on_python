from work_gtiff import CalculationNDWI, SaveGTiif

if __name__ == '__main__':
    input_file = 'IM4-KV4-20190606-07444052972-L2.tif'
    calc_ndwi = CalculationNDWI(input_file=input_file)
    binary_ndwi = calc_ndwi.get_binary_ndwi(binarization_threshold=0.7)
    save_param = SaveGTiif(bands=1, raster=[binary_ndwi])
    calc_ndwi.save_gtiff(save_param)
