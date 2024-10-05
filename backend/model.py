import numpy as np
import onnxruntime as rt

sess = rt.InferenceSession("./model/rf.onnx")

