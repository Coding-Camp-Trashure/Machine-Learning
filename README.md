# 👩‍💻 Machine Learning

---

## 🗳️ Pelatihan Model Klasifikasi Gambar

Implementasi model machine learning bertujuan untuk mengidentifikasi beberapa kategori sampah, yang diklasifikasikan ke dalam empat kategori: sampah botol plastik, sampah botol kaleng, sampah botol kaca, dan sampah lainnya (sampah kain, tanaman, dsb). Proses pengembangan model mencakup tahap persiapan dan praproses data, termasuk pemisahan data (split), augmentasi, dan langkah-langkah lainnya. Sebelum model diintegrasikan ke dalam aplikasi berbasis web, model akan disimpan terlebih dahulu dalam format yang sesuai.


---

## 📦 Data Understanding
1. **Akses dataset** : https://drive.google.com/drive/folders/1rj3s5eVaA3yGePB2CMfXzp4ur1qtfkXt
2. **Informasi dataset** : Dataset ini diperoleh dari hasil penggabungan beberapa kumpulan data gambar yang diambil dari Kaggle. Setelah digabung, dataset dipisahkan berdasarkan kelas dan disimpan di Google Drive. Dataset ini berisi informasi tentang berbagai jenis gambar sampah, baik anorganik maupun organik, yang diklasifikasikan ke dalam empat kategori: sampah botol plastik, sampah botol kaleng, sampah botol kaca, dan sampah lainnya (sampah kain, tanaman, dsb).
3. **Jumlah data** : Terdapat 4.355 data gambar

   a. Jumlah gambar di kategori 'glass_bottle': 561

   b. Jumlah gambar di kategori 'plastic_bottle': 1508

   c. Jumlah gambar di kategori 'can': 1060

   d. Jumlah gambar di kategori 'other': 1226

---

## 🛠️ Data Preparation & Preprocessing

   1. **Cek isi folder dataset**

   2. **Melihat jumlah gambar per kelas atau kategori**

   3. **Melihat gambar acak per kelas atau kategori**

   4. **Melakukan pemisahan data (split data)**
   - 80% data training
   - 10% data testing
   - 10% data validasi

   5. **Melakukan augmentasi data**
   - Rescale
   - Horizontal flip
   - Rotation range
   - Brightness range

---

## 🧠 Model
1. **Arsitektur Model**
* **Base model**: `MobileNetV2` dengan bobot **pre-trained dari ImageNet**
* **Include top**: `False` (hanya menggunakan feature extractor)
* **Tambahan layer custom**:
  * `GlobalAveragePooling2D`
  * `Dense(128, activation='relu')`
  * `Dense(4, activation='softmax')` (output layer untuk 4 kelas)
2. **Fine-Tuning** : Semua layer dari `MobileNetV2` dibekukan (`trainable = False`) untuk melatih hanya bagian custom-nya pada tahap awal.
3. **Kompilasi Model**
* Optimizer: `Adam` dengan `learning_rate=0.0001`
* Loss function: `categorical_crossentropy` (karena klasifikasi multikelas)
* Metrics: `accuracy`
4. **Training**
* Model dilatih selama **maksimal 20 epoch**
* Menggunakan **early stopping** dengan `patience=3`
* **Model terbaik disimpan otomatis** menggunakan `ModelCheckpoint` berdasarkan akurasi validasi tertinggi (`val_accuracy`)
5. **Callback**
* `ModelCheckpoint`: Menyimpan model terbaik dengan nama `mobilenetv2_trashure.keras`
* `EarlyStopping`: Menghentikan training lebih awal jika tidak ada perbaikan pada `val_loss` selama 3 epoch dan mengembalikan bobot terbaik

---

## 📋 Evaluasi 

   1. **Setelah proses pelatihan selesai, model terbaik dimuat dari file .keras dan dievaluasi menggunakan dataset test. Berikut hasil evaluasinya:**
   - Test Accuracy: 97.03%
   - Test Loss: 0.1005
   - Train Accuracy (akhir epoch): 99.60%
   2. **Visualisasi akurasi dan loss**
   
   ![Visualisasi Akurasi dan Loss](Notebook/visualisasi_akurasiloss.png)

   - Model menunjukkan konvergensi yang stabil, tanpa overfitting yang signifikan.
   - Performa validasi dan training sangat baik, menandakan model generalisasi yang kuat.

---

## 💾 Save Model
   Model dikonversi ke berbagai format untuk deployment:
   
   1. .Keras ✅
   2. SavedModel ✅
   3. TensorFlow Lite ✅
   4. TensorFlow.js ✅

---

## 🔁 Cara Kerja Model Prediksi Sampah

1. **Input Gambar**

   Pengguna memasukkan gambar sampah melalui kamera ponsel.

2. **Preprocessing Gambar**

   Gambar yang dimasukkan akan:

   * Diubah ukurannya menjadi **224x224 piksel** (ukuran input MobileNetV2).
   * Dikonversi ke array NumPy.
   * Dinormalisasi ke rentang \[0, 1] atau \[–1, 1] sesuai standar MobileNetV2.

3. **Ekstraksi Fitur (Feature Extraction)**

   Model menggunakan arsitektur **MobileNetV2** yang telah dilatih pada ImageNet untuk mengekstrak fitur penting dari gambar (misalnya: bentuk, tekstur, dan warna objek pada gambar).

4. **Klasifikasi**

   Setelah fitur diekstraksi, fitur tersebut masuk ke:

   * Global Average Pooling (meringkas fitur).
   * Dense Layer 128 unit dengan ReLU.
   * Output Layer dengan 4 neuron dan **softmax** → memberikan probabilitas untuk setiap kelas sampah.

   Model akan memprediksi salah satu dari empat kelas (sampah botol plastik, sampah botol kaleng, sampah botol kaca, atau sampah lainnya).

5. **Output Prediksi**

   Model mengeluarkan hasil prediksi 

---