import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import re
from sklearn.metrics import silhouette_score
import math
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime 



cred = credentials.Certificate('latsar.json') 
default_app = firebase_admin.initialize_app(cred)

db = firestore.client()

#st.set_page_config(layout="wide")
# Load research topics from CSV
def load_topics():
    return pd.read_csv('Topik_Penelitian_dengan_Pembimbing_Terpisah.csv')






# Fungsi untuk membaca data dari Firestore dan menggabungkan (append) data baru
def save_to_firestore(data, collection_name):
    try:
        # Konversi data ke format yang sesuai untuk Firestore
        data_dict = data.to_dict(orient='records')[0]
        # Tambahkan timestamp
        st.session_state.timestamp = datetime.datetime.now()    
        data_dict['timestamp'] = st.session_state.timestamp  # Gunakan timestamp dari session state


        # Simpan data ke Firestore
        db.collection(collection_name).document().set(data_dict)
        st.success(f"Data berhasil disimpan ke Firestore di koleksi '{collection_name}, tekan submit kembali untuk melanjutkan'")
    except Exception as e:
        st.error(f"Gagal menyimpan data ke Firestore: {e}")






# Step 1: Halaman Input Nama dan NIM
def input_data():
    st.title("Kuesioner Minat dan Kemampuan Mahasiswa Informatika")
    
    nama = st.text_input("Nama:")
    nim = st.text_input("NIM:")
    
    if st.button("Mulai Survey"):
        if not nama or not nim:
            st.error("Silakan masukkan Nama dan NIM Anda.")
        else:
            st.session_state.nama = nama
            st.session_state.nim = nim
            st.session_state.start_survey = True

# Step 2: Halaman Survey
def survey():
    st.title("Survey Minat dan Kemampuan Mahasiswa Informatika")

    st.header("Minat Mahasiswa")
    q1 = st.slider("1. Seberapa tertarik Anda dalam mengembangkan algoritma dan pemrograman?", 1, 5)
    q2 = st.slider("2. Seberapa tertarik Anda pada keamanan jaringan dan siber?", 1, 5)
    q3 = st.slider("3. Apakah Anda tertarik dalam bidang kecerdasan buatan dan pembelajaran mesin?", 1, 5)
    q4 = st.slider("4. Apakah Anda tertarik untuk bekerja di bidang pengembangan perangkat lunak?", 1, 5)
    q5 = st.slider("5. Apakah Anda lebih suka bekerja di bidang grafika komputer dan multimedia?", 1, 5)
    q6 = st.slider("6. Seberapa tertarik Anda dalam bidang komputasi berbasis awan?", 1, 5)
    q7 = st.slider("7. Seberapa tertarik Anda untuk bekerja di bidang analisis data besar (big data)?", 1, 5)
    q8 = st.slider("8. Apakah Anda tertarik pada sistem komputasi terdistribusi?", 1, 5)
    q9 = st.slider("9. Seberapa besar minat Anda dalam penelitian di bidang sistem cerdas dan robotika?", 1, 5)
    q10 = st.slider("10. Apakah Anda tertarik pada bidang sistem informasi?", 1, 5)

    st.header("Kemampuan Teknis")
    q11 = st.slider("11. Apakah Anda merasa nyaman menggunakan bahasa pemrograman seperti Python atau Java?", 1, 5)
    q12 = st.slider("12. Seberapa mahir Anda dalam menggunakan SQL dan manajemen basis data?", 1, 5)
    q13 = st.slider("13. Seberapa baik kemampuan Anda dalam pemrograman web?", 1, 5)
    q14 = st.slider("14. Apakah Anda memiliki pengalaman dalam mengembangkan aplikasi berbasis cloud?", 1, 5)
    q15 = st.slider("15. Seberapa mahir Anda dalam memahami arsitektur jaringan?", 1, 5)
    q16 = st.slider("16. Seberapa baik kemampuan Anda dalam desain perangkat lunak dan rekayasa perangkat lunak?", 1, 5)
    q17 = st.slider("17. Seberapa baik Anda memahami prinsip algoritma dan optimasi?", 1, 5)
    q18 = st.slider("18. Apakah Anda memiliki pengalaman dalam pemrosesan gambar dan grafika komputer?", 1, 5)
    q19 = st.slider("19. Seberapa mahir Anda dalam menggunakan teknologi big data seperti Hadoop atau Spark?", 1, 5)
    q20 = st.slider("20. Apakah Anda memiliki pengalaman dalam menggunakan framework AI seperti TensorFlow atau PyTorch?", 1, 5)

    st.header("Preferensi Gaya Belajar")
    q21 = st.slider("21. Apakah Anda lebih suka belajar melalui pemecahan masalah praktis atau proyek?", 1, 5)
    q22 = st.slider("22. Apakah Anda lebih suka belajar melalui pembelajaran berbasis teori?", 1, 5)
    q23 = st.slider("23. Seberapa sering Anda menggunakan platform pembelajaran online untuk belajar?", 1, 5)
    q24 = st.slider("24. Apakah Anda lebih suka bekerja sendiri atau dalam tim?", 1, 5)
    q25 = st.slider("25. Apakah Anda merasa nyaman belajar dengan cara eksploratif dan mandiri?", 1, 5)
    q26 = st.slider("26. Apakah Anda lebih menyukai metode pembelajaran yang melibatkan banyak diskusi kelompok?", 1, 5)
    q27 = st.slider("27. Seberapa nyaman Anda belajar dengan kode dan debugging langsung?", 1, 5)
    q28 = st.slider("28. Apakah Anda lebih suka materi yang terstruktur secara sistematis dalam belajar?", 1, 5)
    q29 = st.slider("29. Apakah Anda lebih suka belajar dengan materi multimedia (video, simulasi, animasi)?", 1, 5)
    q30 = st.slider("30. Seberapa sering Anda mengikuti workshop atau seminar untuk menambah pengetahuan teknis?", 1, 5)

    st.header("Tujuan Karir")
    q31 = st.slider("31. Apakah Anda bercita-cita menjadi pengembang perangkat lunak?", 1, 5)
    q32 = st.slider("32. Apakah Anda tertarik untuk bekerja di bidang keamanan siber?", 1, 5)
    q33 = st.slider("33. Apakah Anda ingin menjadi peneliti di bidang kecerdasan buatan?", 1, 5)
    q34 = st.slider("34. Apakah Anda ingin bekerja di perusahaan teknologi besar?", 1, 5)
    q35 = st.slider("35. Apakah Anda tertarik menjadi data scientist atau data engineer?", 1, 5)
    q36 = st.slider("36. Apakah Anda berencana untuk melanjutkan studi di bidang sistem informasi?", 1, 5)
    q37 = st.slider("37. Apakah Anda bercita-cita untuk bekerja di startup teknologi?", 1, 5)
    q38 = st.slider("38. Apakah Anda ingin bekerja sebagai arsitek jaringan?", 1, 5)
    q39 = st.slider("39. Apakah Anda tertarik menjadi pengembang game atau multimedia?", 1, 5)
    q40 = st.slider("40. Apakah Anda ingin berkarir di bidang komputasi awan dan cloud computing?", 1, 5)

    # Button untuk Submit
    if st.button("Submit"):
        
        st.session_state.survey_submitted = True
        data_new = {
            'Nama': st.session_state.nama,
            'NIM': st.session_state.nim,
            'Feature_1': q1,  'Feature_2': q2,  'Feature_3': q3,  'Feature_4': q4,  'Feature_5': q5,
            'Feature_6': q6,  'Feature_7': q7,  'Feature_8': q8,  'Feature_9': q9,  'Feature_10': q10,
            'Feature_11': q11, 'Feature_12': q12, 'Feature_13': q13, 'Feature_14': q14, 'Feature_15': q15,
            'Feature_16': q16, 'Feature_17': q17, 'Feature_18': q18, 'Feature_19': q19, 'Feature_20': q20,
            'Feature_21': q21, 'Feature_22': q22, 'Feature_23': q23, 'Feature_24': q24, 'Feature_25': q25,
            'Feature_26': q26, 'Feature_27': q27, 'Feature_28': q28, 'Feature_29': q29, 'Feature_30': q30,
            'Feature_31': q31, 'Feature_32': q32, 'Feature_33': q33, 'Feature_34': q34, 'Feature_35': q35,
            'Feature_36': q36, 'Feature_37': q37, 'Feature_38': q38, 'Feature_39': q39, 'Feature_40': q40
        }

        

        
        df_new = pd.DataFrame([data_new])

        # Simpan data responden baru ke dalam file CSV
        df_new.to_csv('hasil_kuesioner.csv', mode='a', header=False, index=False)

        df_training = pd.read_csv('synthetic_training_data_with_nama_nim.csv')

        features = df_training.drop(columns=['Nama', 'NIM'])

        # K-means cluster 4
        kmeans = KMeans(n_clusters=4, random_state=42)
        df_training['Cluster'] = kmeans.fit_predict(features)

        features_new = df_new.drop(columns=['Nama', 'NIM'])
        clusters = kmeans.predict(features_new)

        df_new['Cluster'] = clusters

        # Menghubungkan cluster ke keahlian
        cluster_labels = {
            0: "Computational dan Artificial Intelligence",
            1: "Networking dan Security",
            2: "Software Engineering dan Mobile Computing",
            3: "Information System dan Data Spasial"
        }

        # Menentukan cluster pengguna baru
        cluster_user = clusters[-1]
        keahlian = cluster_labels[cluster_user]
        st.session_state.keahlian = keahlian

        #st.success(f"Terima kasih atas partisipasi Anda! Anda diklasifikasikan ke dalam kelompok: {keahlian}")

        # Tampilkan hasil klasifikasi untuk pengguna
        #st.write(f"Nama: {st.session_state.nama}, NIM: {st.session_state.nim}, Keahlian: {keahlian}")

        # Simpan hasil klasifikasi ke file CSV lain
        hasil_klasifikasi = {
            'Nama': st.session_state.nama,
            'NIM': st.session_state.nim,
            'Keahlian': keahlian
        }
        
        df_klasifikasi = pd.DataFrame([hasil_klasifikasi])
        df_klasifikasi.to_csv('hasil_klasifikasi_dan_nama.csv', mode='a', header=False, index=False)
        save_to_firestore(df_klasifikasi, "hasil_klasifikasi")
        #store_in_google_drive(df_klasifikasi, 'hasil_klasifikasi_dan_nama.csv')


        st.session_state.start_survey = False

# Halaman hasil setelah survey
def hasil_survey():
    # Load research topics
    topics_df = load_topics()
    
    st.title("Hasil Klasifikasi")
    st.success(f"Terima kasih atas partisipasi Anda! Anda diklasifikasikan ke dalam kelompok: **{st.session_state.keahlian}** ")

    # Cocokkan keahlian dengan kolom "Kelompok" di CSV dan tampilkan topik serta pembimbing terkait
    filtered_topics = topics_df[topics_df['Kelompok'].str.lower() == st.session_state.keahlian.lower()]
    narasi_topics=filtered_topics['narasi'].unique()
    st.success(f"{narasi_topics[0]}")
    

    if not filtered_topics.empty:
        st.write("**Pembimbing yang Direkomendasikan**:")
        pembimbing_columns = [f'Pembimbing {i}' for i in range(1, 9)]

        # Create a list of unique names for each pembimbing
        pembimbing_list = {col: filtered_topics[col].unique().tolist() for col in pembimbing_columns}
        #st.write(pembimbing_list)
        # Display the result
        nama_pembimbing = [nama[0] for nama in pembimbing_list.values() if not (isinstance(nama[0], float) and math.isnan(nama[0]))]
        # Construct the email link
       
        for topic in nama_pembimbing:
            #email_address = "email@example.com"  # Replace with the actual email address
            #subject = f"Meeting with {topic}"  # Example subject
            #body = f"Dear {topic},\n\nI would like to schedule a meeting with you...\n\nSincerely,\nYour Name"  # Example body
            
            #mail_to_link = f"mailto:{email_address}?subject={subject}&body={body}"
            #st.write(f"- {topic}")
            name = re.sub(r'(Dr\.|Prof\.|Ir\.|S\.T\.|M\.T\.|Ph\.D\. | M\.Eng\. | M\.Cs\.|ST|M\.Cs| S.Kom |M.Kom||S\.Kom\.|M\.Kom\.|M\.Eng|)', '', topic)
            name = re.sub(r' {2,}', ' ', name)  # Remove extra spaces
            name = name.strip()
            st.page_link(f"https://sinta.kemdikbud.go.id/authors?q= {name}", label=f"-  {topic}", icon="🔗")
            #st.markdown(
            #"<a href='mailto:nama_dosen@informatika.untan.ac.id?subject=Email Subject&body=Email Body'> Kirim email perkenalan diri</a>",
            #unsafe_allow_html=True,
            #)


            #st.markdown(f"<div style='display: flex; align-items: center;'>{topic} <a href='#'><img src='https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png' width='24' height='24'></a></div>", unsafe_allow_html=True)

            #st.markdown(f"[{topic}]({mail_to_link})")
            #text = f":green-background[{topic}]"  # Create the formatted string
            #st.markdown(text)
          
                 
        #st.table(filtered_topics[['Topik Penelitian', 'Pembimbing 1', 'Pembimbing 2', 'Pembimbing 3', 'Pembimbing 4', 'Pembimbing 5', 'Pembimbing 6', 'Pembimbing 7', 'Pembimbing 8']])
        research_topics=filtered_topics[['Topik Penelitian','minat']]
        #st.write(research_topics)
        #research_topics=filtered_topics['minat'].tolist()
        st.write("**Topik yang Direkomendasikan:**")
        for index, row  in research_topics.iterrows():
            topic = row['Topik Penelitian']
            minat = row['minat']
            #st.write(minat)
            #st.write(f"- {topic}")
            if minat <= 5:
                text = f":green-background[{topic}]"  
                st.markdown(text)
            elif 6 <= minat < 16:
                text = f":orange-background[{topic}]"  
                st.markdown(text)
            else:
                text = f":red-background[{topic}]"  
                st.markdown(text)


    else:
        st.write("Tidak ada topik yang sesuai dengan keahlian Anda.")
    
    
    





    st.write(f"Nama: {st.session_state.nama}, NIM: {st.session_state.nim}, Keahlian: {st.session_state.keahlian}")

# Cek apakah survey sudah dimulai
if 'start_survey' not in st.session_state:
    st.session_state.start_survey = False

# Cek apakah survey sudah di-submit
if 'survey_submitted' not in st.session_state:
    st.session_state.survey_submitted = False

# Jika sudah submit, tampilkan halaman hasil
if st.session_state.survey_submitted:
    hasil_survey()
# Jika belum mulai survey, tampilkan halaman input nama dan NIM
elif not st.session_state.start_survey:
    input_data()
# Jika survey belum di-submit, tampilkan halaman survey
else:
    survey()
