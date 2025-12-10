import onnxruntime as ort

model_path = 'hair_classifier_v1.onnx'
session = ort.InferenceSession(model_path)

print("Input names:")
for i in session.get_inputs():
    print(i.name)

print("\nOutput names:")
for o in session.get_outputs():
    print(o.name)
