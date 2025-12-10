import onnxruntime as ort

model_path = 'hair_classifier_v1.onnx'
session = ort.InferenceSession(model_path)

print("Input shape:")
for i in session.get_inputs():
    print(i.name, i.shape)
