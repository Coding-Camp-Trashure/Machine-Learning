# -*- coding: utf-8 -*-
"""Trashure.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1qHQkbjG79lVoIg4lyb58Ri-nyA__VFmv

## **Import Library**
"""

import os
import zipfile
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import random
import shutil
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
from tensorflow.keras.preprocessing import image

"""## **Data Loading**"""

# Install gdown
!pip install gdown

# Unduh dan unzip
file_id = "1HYo7tF6hkZYm6s8PzCUKHwGue8zJPl9g"
!gdown --id $file_id --output Dataset.zip

with zipfile.ZipFile("Dataset.zip", 'r') as zip_ref:
    zip_ref.extractall("Dataset")

# cek isis folder
print(os.listdir("Dataset"))

"""## **Data Preparation**"""

# Cek isi folder dataset
base_dir = "Dataset/Dataset"
categories = os.listdir(base_dir)
print("Label kategori:", categories)

# Melihat jumlah data gambar
# Tentukan direktori dasar dataset
base_dir = "Dataset/Dataset"

# Dapatkan daftar semua kategori
categories = os.listdir(base_dir)

# Inisialisasi total jumlah gambar
total_images = 0

# Hitung jumlah gambar untuk setiap kategori dan total keseluruhan
for category in categories:
    category_dir = os.path.join(base_dir, category)
    # Hitung jumlah file dengan ekstensi .jpg di dalam direktori kategori
    num_images = len([f for f in os.listdir(category_dir) if f.endswith(".jpg")])
    print(f"Jumlah gambar di kategori '{category}': {num_images}")
    total_images += num_images

# Cetak total jumlah gambar keseluruhan
print(f"\nTotal keseluruhan gambar: {total_images}")

# Melihat gambar acak
# Tentukan path ke setiap folder kategori
can_dir = os.path.join(base_dir, 'can')
glass_bottle_dir = os.path.join(base_dir, 'glass_bottle')
other_dir = os.path.join(base_dir, 'other')
plastic_bottle_dir = os.path.join(base_dir, 'plastic_bottle')

# Dapatkan daftar semua gambar dalam setiap folder
can_images = os.listdir(can_dir)
glass_bottle_images = os.listdir(glass_bottle_dir)
other_images = os.listdir(other_dir)
plastic_bottle_images = os.listdir(plastic_bottle_dir)

# Pilih gambar acak dari setiap kategori
random_can_img = random.choice(can_images)
random_glass_bottle_img = random.choice(glass_bottle_images)
random_other_img = random.choice(other_images)
random_plastic_bottle_img = random.choice(plastic_bottle_images)

# Tentukan path lengkap ke gambar acak
random_can_img_path = os.path.join(can_dir, random_can_img)
random_glass_bottle_img_path = os.path.join(glass_bottle_dir, random_glass_bottle_img)
random_other_img_path = os.path.join(other_dir, random_other_img)
random_plastic_bottle_img_path = os.path.join(plastic_bottle_dir, random_plastic_bottle_img)

# Tampilkan gambar acak
img_can = mpimg.imread(random_can_img_path)
img_glass_bottle = mpimg.imread(random_glass_bottle_img_path)
img_other = mpimg.imread(random_other_img_path)
img_plastic_bottle = mpimg.imread(random_plastic_bottle_img_path)

plt.figure(figsize=(15, 5))

plt.subplot(1, 4, 1)
plt.imshow(img_can)
plt.title("Can")
plt.axis("off")

plt.subplot(1, 4, 2)
plt.imshow(img_glass_bottle)
plt.title("Glass Bottle")
plt.axis("off")

plt.subplot(1, 4, 3)
plt.imshow(img_other)
plt.title("Other")
plt.axis("off")

plt.subplot(1, 4, 4)
plt.imshow(img_plastic_bottle)
plt.title("Plastic Bottle")
plt.axis("off")

plt.show()

"""### Split data"""

# split data training, testing, dan validasi (80:10:10)
base_dir = "Dataset/Dataset"
output_base = "split_dataset"
classes = os.listdir(base_dir)

for split in ['train', 'val', 'test']:
    for class_name in classes:
        os.makedirs(os.path.join(output_base, split, class_name), exist_ok=True)

for class_name in classes:
    class_path = os.path.join(base_dir, class_name)
    images = [f for f in os.listdir(class_path) if f.endswith(".jpg")]
    train_files, testval_files = train_test_split(images, test_size=0.2, random_state=42)
    val_files, test_files = train_test_split(testval_files, test_size=0.5, random_state=42)

    for split_name, split_files in zip(['train', 'val', 'test'], [train_files, val_files, test_files]):
        for fname in split_files:
            src = os.path.join(class_path, fname)
            dst = os.path.join(output_base, split_name, class_name, fname)
            shutil.copy(src, dst)

# Augmentasi pada data training
IMG_SIZE = (224, 224)
BATCH_SIZE = 32

train_dir = os.path.join(output_base, 'train')
val_dir = os.path.join(output_base, 'val')
test_dir = os.path.join(output_base, 'test')

train_datagen = ImageDataGenerator(
    rescale=1./255,
    horizontal_flip=True,
    rotation_range=15,
    brightness_range=[0.8, 1.2]
)

val_test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    train_dir, target_size=IMG_SIZE, batch_size=BATCH_SIZE, class_mode='categorical')

val_generator = val_test_datagen.flow_from_directory(
    val_dir, target_size=IMG_SIZE, batch_size=BATCH_SIZE, class_mode='categorical')

test_generator = val_test_datagen.flow_from_directory(
    test_dir, target_size=IMG_SIZE, batch_size=BATCH_SIZE, class_mode='categorical', shuffle=False)

"""## **Modelling**"""

# Melakukan modelling dengan MobilenetV2
base_model = MobileNetV2(input_shape=(224, 224, 3), include_top=False, weights='imagenet')
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(128, activation='relu')(x)
predictions = Dense(4, activation='softmax')(x)
model = Model(inputs=base_model.input, outputs=predictions)

for layer in base_model.layers:
    layer.trainable = False

model.compile(optimizer=Adam(learning_rate=0.0001),
              loss='categorical_crossentropy',
              metrics=['accuracy'])
model.summary()

# Callback
checkpoint = ModelCheckpoint("mobilenetv2_trashure.keras", monitor='val_accuracy', save_best_only=True, mode='max')
early_stop = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)

history = model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=20,
    callbacks=[checkpoint, early_stop]
)

"""## **Evaluasi**"""

# setelah training selesai, dan load model terbaik dari .keras
model = tf.keras.models.load_model('mobilenetv2_trashure.keras')
loss, acc = model.evaluate(test_generator)
print(f"Test Loss: {loss:.4f}")
print(f"Test Accuracy: {acc * 100:.2f}%")

# Mengambil riwayat akurasi train dari objek history
train_accuracy = history.history['accuracy']

# Menampilkan akurasi train
print(f"Train Accuracy: {train_accuracy[-1] * 100:.2f}%")

# membuat dan melihat plot akurasi dan loss
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Train')
plt.plot(history.history['val_accuracy'], label='Val')
plt.title("Accuracy")
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Train')
plt.plot(history.history['val_loss'], label='Val')
plt.title("Loss")
plt.legend()
plt.show()

"""## **Simpan Model dan interferensi**"""

# simpan dengan format savemodel
model.export("saved_model_trashure")

# Konversi ke TFLite
converter = tf.lite.TFLiteConverter.from_saved_model("saved_model_trashure")
tflite_model = converter.convert()

# Simpan ke file .tflite
with open("mobilenetv2_trashure.tflite", "wb") as f:
    f.write(tflite_model)

# simpan dengan format tensorflowjs
!pip install tensorflowjs
# Konversi SavedModel ke format TFJS
!tensorflowjs_converter --input_format=tf_saved_model --output_format=tfjs_graph_model \
    saved_model_trashure tfjs_model_trashure

# Load model TFLite
interpreter = tf.lite.Interpreter(model_path="mobilenetv2_trashure.tflite")
interpreter.allocate_tensors()

# Dapatkan input dan output details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Fungsi untuk preprocessing 1 gambar
def preprocess_tflite(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0).astype(np.float32)
    return img_array

# Contoh inference
img_path = "/content/Dataset/Dataset/plastic_bottle/PET1,001.jpg"
input_data = preprocess_tflite(img_path)
interpreter.set_tensor(input_details[0]['index'], input_data)
interpreter.invoke()
output_data = interpreter.get_tensor(output_details[0]['index'])

# Ambil label prediksi
predicted_class = np.argmax(output_data)
confidence = np.max(output_data)
print(f"Prediksi kelas: {predicted_class}, Confidence: {confidence:.2f}")

# Load model TFLite
interpreter = tf.lite.Interpreter(model_path="mobilenetv2_trashure.tflite")
interpreter.allocate_tensors()

# Dapatkan detail input dan output
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Mapping kelas (ganti sesuai urutan aslinya)
class_labels = ['can', 'glass_bottle','other', 'plastic_bottle']

# Fungsi untuk prediksi dan tampilkan gambar
def predict_and_show(img_path):
    # Preprocess
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0).astype(np.float32)

    # Inference
    interpreter.set_tensor(input_details[0]['index'], img_array)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])

    # Ambil prediksi
    pred_idx = np.argmax(output_data)
    confidence = np.max(output_data)
    label = f"{class_labels[pred_idx]} ({confidence*100:.2f}%)"

    # Visualisasi
    plt.imshow(img)
    plt.axis('off')
    plt.title(f"Prediction: {label}", fontsize=14)
    plt.show()

predict_and_show("/content/Dataset/Dataset/glass_bottle/Glass1,016.JPG")