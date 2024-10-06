import numpy as np
import onnxruntime as rt
import pandas as pd

session = rt.InferenceSession("./model/rf.onnx")

input_name = session.get_inputs()[0].name

COLS = ['type_dress', 'type_jacket', 'type_pants', 'type_shirt', 'type_shoes',
 'brand_adidas', 'brand_armani', 'brand_dior', 'brand_forever21', 'brand_gap',
 'brand_gucci', 'brand_h&m', 'brand_lacoste', 'brand_levis', 'brand_nike',
 'brand_pull&bear', 'brand_zara', 'material_cotton', 'material_denim',
 'material_leather', 'material_polyester', 'style_athletic', 'style_casual',
 'style_formal', 'color_black', 'color_blue', 'color_brown', 'color_green',
 'color_purple', 'color_red', 'color_white', 'color_yellow', 'state_new',
 'state_used']

CAT = ['type', 'brand', 'material', 'style', 'color', 'state']

def predict(texts: list) -> float:

    print(f'val: {texts}')

    preData = [f"{CAT[i]}_{texts[i].lower()}" for i in range(len(texts))]

    data = {}

    for col in COLS:
        data[col] = [False]

    for i in preData:
        
        if i in COLS:
            data[i] = [True]

    df = pd.DataFrame(data)

    processed = df.values.astype(np.float32)

    return session.run(None, input_feed={input_name: processed})[0][0][0]


if __name__ == "__main__":
    clothe = ["shirt", "zara", "cotton", "casual", "white", "new"]

    print(predict(clothe))