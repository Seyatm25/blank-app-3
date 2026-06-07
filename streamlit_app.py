import streamlit as st
import time

# ==============================================================================
# 1. KONFIGURASI HALAMAN
# ==============================================================================
st.set_page_config(
    page_title="OrganicChem | Edu-Lab Platform",
    page_icon="🧪",
    layout="wide"
)

# ==============================================================================
# 2. CUSTOM CSS INTERAKTIF (VERSI MODERN)
# ==============================================================================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f0f9ff, #f8fafc);
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f766e, #14b8a6);
}
[data-testid="stSidebar"] * {
    color: white !important;
}
.banner-utama {
    background: linear-gradient(135deg, #06b6d4, #3b82f6);
    padding: 35px;
    border-radius: 15px;
    color: white;
    margin-bottom: 30px;
    box-shadow: 0 6px 20px rgba(59,130,246,0.25);
}
.kotak-analisis {
    border-left: 6px solid #14b8a6;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 20px;
    background: linear-gradient(135deg, #f0fdfa, #ecfeff);
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}
.stButton > button {
    border-radius: 12px;
    border: none;
    background: linear-gradient(135deg, #14b8a6, #0ea5e9);
    color: white;
    font-weight: 600;
    transition: all 0.3s ease;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(14,165,233,0.3);
}
.tube-wrap {
    display: flex;
    justify-content: center;
    height: 350px;
    padding-top: 10px;
}
.tube-glass {
    width: 80px;
    height: 300px;
    border: 4px solid #64748b;
    border-top: none;
    border-radius: 0 0 40px 40px;
    position: relative;
    overflow: hidden;
    background: rgba(15, 23, 42, 0.16);
    box-shadow: inset 0 0 15px rgba(0,0,0,0.25);
    backdrop-filter: blur(3px);
}
.tube-liquid {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    transition: height 1.2s ease, background 1.2s ease;
}
.precipitate-layer {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 60px;
    box-shadow: inset 0 2px 5px rgba(0,0,0,0.2);
}
.cloudy-layer {
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    background: linear-gradient(to bottom, rgba(255,255,255,0.85), rgba(241,245,249,0.95));
}
.bubble-fx {
    position: absolute;
    background: rgba(0,0,0,0.15);
    border-radius: 50%;
    width: 8px;
    height: 8px;
    animation: floatUp 1.8s infinite ease-in;
}
.reagent-tag {
    text-align: center;
    font-weight: bold;
    background-color: #e2e8f0;
    color: #1e293b;
    padding: 6px 12px;
    border-radius: 8px;
    margin-bottom: 15px;
    border: 1px solid #cbd5e1;
}
@keyframes floatUp {
    0% { bottom: 0px; opacity: 1; }
    100% { bottom: 250px; opacity: 0; }
}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. FUNGSI HELPER & DATABASE (NAMA REAGEN DISESUAIKAN GAMBAR)
# ==============================================================================
def force_rerun():
    if hasattr(st, 'rerun'):
        st.rerun()
    elif hasattr(st, 'experimental_rerun'):
        st.experimental_rerun()

def render_tube(tinggi, warna_larutan, efek, warna_endapan=None):
    e_html = ""
    if efek == "precipitate":
        bg_endapan = warna_endapan if warna_endapan else warna_larutan
        e_html = f"<div class='precipitate-layer' style='background: {bg_endapan}; border-top: 3.5px solid rgba(0, 0, 0, 0.25);'></div>"
    elif efek == "cloudy":
        e_html = "<div class='cloudy-layer'></div>"
    elif efek == "bubbles":
        e_html = "<div class='bubble-fx' style='left:20px;'></div><div class='bubble-fx' style='left:50px; animation-delay:0.5s;'></div>"
    return f"<div class='tube-wrap'><div class='tube-glass'><div class='tube-liquid' style='height:{tinggi}; background:{warna_larutan};'>{e_html}</div></div></div>"

# PEMBARUAN NAMA UJI SESUAI REAGEN
reagen_colors = {
    "Uji Ceric Nitrat (CAN)": "#f97316", 
    "Uji Pereaksi Jones": "#f97316", 
    "Uji Pereaksi Lucas": "#f8fafc", 
    "Uji Natrium Bisulfit (NaHSO3)": "#f8fafc", 
    "Uji Pereaksi Fehling": "#3b82f6", 
    "Uji Pereaksi Schiff": "#f8fafc",
    "Uji Iodoform (NaOH + I2)": "#f8fafc",
    "Uji Asam Hidroksamat (NH2OH + FeCl3)": "#f8fafc",
    "Uji Lakmus & Air Barit": "#f8fafc"
}

# ALUR DIPERBARUI
flowchart_paths = {
    "Alkohol Primer": ["Uji Ceric Nitrat (CAN)", "Uji Pereaksi Jones", "Uji Pereaksi Lucas"],
    "Alkohol Sekunder": ["Uji Ceric Nitrat (CAN)", "Uji Pereaksi Jones", "Uji Pereaksi Lucas", "Uji Iodoform (NaOH + I2)"],
    "Alkohol Tersier": ["Uji Ceric Nitrat (CAN)", "Uji Pereaksi Jones", "Uji Pereaksi Lucas"],
    "Aldehida (Alkanal)": ["Uji Ceric Nitrat (CAN)", "Uji Natrium Bisulfit (NaHSO3)", "Uji Pereaksi Fehling", "Uji Pereaksi Schiff"],
    "Keton (Alkanon)": ["Uji Ceric Nitrat (CAN)", "Uji Natrium Bisulfit (NaHSO3)", "Uji Pereaksi Fehling", "Uji Iodoform (NaOH + I2)"],
    "Ester (Alkil Alkanoat)": ["Uji Ceric Nitrat (CAN)", "Uji Natrium Bisulfit (NaHSO3)", "Uji Asam Hidroksamat (NH2OH + FeCl3)"],
    "Asam Karboksilat": ["Uji Ceric Nitrat (CAN)", "Uji Natrium Bisulfit (NaHSO3)", "Uji Asam Hidroksamat (NH2OH + FeCl3)", "Uji Lakmus & Air Barit"],
    "Alkana / Hidrokarbon Jenuh": ["Uji Ceric Nitrat (CAN)", "Uji Natrium Bisulfit (NaHSO3)", "Uji Asam Hidroksamat (NH2OH + FeCl3)", "Uji Lakmus & Air Barit"]
}

# DATABASE HASIL REAKSI DIPERBARUI
database_reaksi = {
    "Alkohol Primer": {
        "Uji Ceric Nitrat (CAN)": {
            "hasil": "(+) Merah Ceri", 
            "reaksi": r"R-OH + [Ce(NO_3)_6]^{2-} \rightarrow [Ce(OR)(NO_3)_5]^{2-} + HNO_3", 
            "alasan": "Gugus -OH bebas bereaksi menggantikan ligan nitrat pada ion Cerium(IV) membentuk senyawa kompleks koordinasi berwarna merah ceri.", 
            "warna_akhir": "#ef4444", "efek": "none"
        },
        "Uji Pereaksi Jones": {
            "hasil": "(+) Hijau", 
            "reaksi": r"3\ R-CH_2OH + 2\ CrO_3 + 3\ H_2SO_4 \rightarrow 3\ R-CHO + Cr_2(SO_4)_3 + 6\ H_2O", 
            "alasan": "Memiliki atom hidrogen alfa. Gugus -OH dioksidasi menjadi aldehida, sedangkan Kromium(VI) jingga tereduksi menjadi Kromium(III) hijau.", 
            "warna_akhir": "#10b981", "efek": "none"
        },
        "Uji Pereaksi Lucas": {
            "hasil": "(-) Tetap Bening/Jingga", 
            "reaksi": r"R-CH_2OH + HCl \xrightarrow{ZnCl_2} \text{Tidak ada reaksi}", 
            "alasan": "Karbokation primer sangat tidak stabil sehingga tidak mampu bereaksi dengan pereaksi Lucas pada suhu kamar.", 
            "warna_akhir": "#f97316", "efek": "none"
        }
    },
    "Alkohol Sekunder": {
        "Uji Ceric Nitrat (CAN)": {
            "hasil": "(+) Merah Ceri", 
            "reaksi": r"R-OH + [Ce(NO_3)_6]^{2-} \rightarrow [Ce(OR)(NO_3)_5]^{2-} + HNO_3", 
            "alasan": "Ikatan koordinasi terbentuk antara atom oksigen pada gugus hidroksil sekunder dengan logam Cerium pusat.", 
            "warna_akhir": "#ef4444", "efek": "none"
        },
        "Uji Pereaksi Jones": {
            "hasil": "(+) Hijau", 
            "reaksi": r"3\ R_2CH-OH + 2\ CrO_3 + 3\ H_2SO_4 \rightarrow 3\ R_2C=O + Cr_2(SO_4)_3 + 6\ H_2O", 
            "alasan": "Alkohol sekunder dioksidasi menjadi keton, ditandai dengan perubahan warna larutan dari jingga ke hijau.", 
            "warna_akhir": "#10b981", "efek": "none"
        },
        "Uji Pereaksi Lucas": {
            "hasil": "(+) Emulsi Putih (Perlu Pemanasan)", 
            "reaksi": r"R_2CH-OH + HCl \xrightarrow{ZnCl_2} R_2CH-Cl \downarrow + H_2O", 
            "alasan": "Karbokation sekunder memiliki stabilitas menengah. Bereaksi menghasilkan alkil klorida setelah 5-10 menit dengan bantuan pemanasan.", 
            "warna_akhir": "#e2e8f0", "efek": "cloudy"
        },
        "Uji Iodoform (NaOH + I2)": {
            "hasil": "(+) Endapan Kuning", 
            "reaksi": r"R-CH(OH)-CH_3 + 4\ I_2 + 6\ NaOH \rightarrow CHI_3 \downarrow + R-COONa + 5\ NaI + 5\ H_2O", 
            "alasan": "Struktur metil karbinol dioksidasi oleh iodin menjadi metil keton, lalu membentuk kristal iodoform berwarna kuning.", 
            "warna_akhir": "#fef08a", "efek": "precipitate", "warna_endapan": "#facc15"
        }
    },
    "Alkohol Tersier": {
        "Uji Ceric Nitrat (CAN)": {
            "hasil": "(+) Merah Ceri", 
            "reaksi": r"R-OH + [Ce(NO_3)_6]^{2-} \rightarrow [Ce(OR)(NO_3)_5]^{2-} + HNO_3", 
            "alasan": "Memiliki gugus -OH bebas yang dapat membentuk kompleks koordinasi berwarna merah dengan ceric nitrat.", 
            "warna_akhir": "#ef4444", "efek": "none"
        },
        "Uji Pereaksi Jones": {
            "hasil": "(-) Tetap Jingga", 
            "reaksi": r"R_3C-OH + CrO_3 \rightarrow \text{Tidak bereaksi}", 
            "alasan": "Alkohol tersier tidak memiliki atom hidrogen alfa sehingga tidak dapat dioksidasi oleh pereaksi Jones.", 
            "warna_akhir": "#f97316", "efek": "none"
        },
        "Uji Pereaksi Lucas": {
            "hasil": "(+) Emulsi Putih (Seketika)", 
            "reaksi": r"R_3C-OH + HCl \xrightarrow{ZnCl_2} R_3C-Cl \downarrow + H_2O", 
            "alasan": "Membentuk karbokation tersier yang sangat stabil, sehingga reaksi substitusi berjalan instan membentuk kabut keruh alkil klorida.", 
            "warna_akhir": "#94a3b8", "efek": "cloudy"
        }
    },
    "Aldehida (Alkanal)": {
        "Uji Ceric Nitrat (CAN)": {
            "hasil": "(-) Tetap Jingga", 
            "reaksi": r"R-CHO + [Ce(NO_3)_6]^{2-} \rightarrow \text{Tidak bereaksi}", 
            "alasan": "Aldehida tidak memiliki gugus hidroksil (-OH) bebas sehingga warna pereaksi tetap jingga.", 
            "warna_akhir": "#f97316", "efek": "none"
        },
        "Uji Natrium Bisulfit (NaHSO3)": {
            "hasil": "(+) Endapan Putih", 
            "reaksi": r"R-CHO + NaHSO_3 \rightarrow R-CH(OH)SO_3Na \downarrow", 
            "alasan": "Nukleofil bisulfit menyerang gugus karbonil aldehida yang reaktif, menghasilkan produk adisi berupa kristal putih.", 
            "warna_akhir": "#cbd5e1", "efek": "precipitate", "warna_endapan": "#ffffff"
        },
        "Uji Pereaksi Fehling": {
            "hasil": "(+) Merah Bata", 
            "reaksi": r"R-CHO + 2\ Cu^{2+} + 5\ OH^- \rightarrow R-COO^- + Cu_2O \downarrow + 3\ H_2O", 
            "alasan": "Aldehida adalah reduktor kuat yang mereduksi kupri oksida menjadi endapan tembaga(I) oksida berwarna merah bata.", 
            "warna_akhir": "#3b82f6", "efek": "precipitate", "warna_endapan": "#b91c1c"
        },
        "Uji Pereaksi Schiff": {
            "hasil": "(+) Ungu / Magenta", 
            "reaksi": r"\text{Aldehida} + \text{Pereaksi Schiff} \rightarrow \text{Kompleks Magenta}", 
            "alasan": "Reaksi adisi spesifik yang mengembalikan struktur warna p-rosanilin menjadi ungu murni.", 
            "warna_akhir": "#d946ef", "efek": "none"
        }
    },
    "Keton (Alkanon)": {
        "Uji Ceric Nitrat (CAN)": {
            "hasil": "(-) Tetap Jingga", 
            "reaksi": r"\text{Keton} + [Ce(NO_3)_6]^{2-} \rightarrow \text{Tidak bereaksi}", 
            "alasan": "Keton tidak memiliki gugus fungsi hidroksil.", 
            "warna_akhir": "#f97316", "efek": "none"
        },
        "Uji Natrium Bisulfit (NaHSO3)": {
            "hasil": "(+) Endapan Putih", 
            "reaksi": r"CH_3-CO-CH_3 + NaHSO_3 \rightarrow (CH_3)_2C(OH)SO_3Na \downarrow", 
            "alasan": "Keton suku rendah (seperti aseton) memiliki halangan sterik kecil sehingga masih bisa diadisi oleh bisulfit membentuk endapan putih.", 
            "warna_akhir": "#cbd5e1", "efek": "precipitate", "warna_endapan": "#ffffff"
        },
        "Uji Pereaksi Fehling": {
            "hasil": "(-) Tetap Biru", 
            "reaksi": r"\text{Keton} + Cu^{2+} \rightarrow \text{Tidak bereaksi}", 
            "alasan": "Keton tidak memiliki atom hidrogen pada gugus karbonil sehingga tidak bersifat reduktor.", 
            "warna_akhir": "#3b82f6", "efek": "none"
        },
        "Uji Iodoform (NaOH + I2)": {
            "hasil": "(+) Endapan Kuning", 
            "reaksi": r"R-CO-CH_3 + 3\ I_2 + 4\ NaOH \rightarrow CHI_3 \downarrow + R-COONa + 3\ NaI + 3\ H_2O", 
            "alasan": "Memiliki gugus metil yang terikat langsung pada karbonil, sehingga bereaksi positif membentuk endapan kuning iodoform.", 
            "warna_akhir": "#fef08a", "efek": "precipitate", "warna_endapan": "#facc15"
        }
    },
    "Ester (Alkil Alkanoat)": {
        "Uji Ceric Nitrat (CAN)": {
            "hasil": "(-) Tetap Jingga", "reaksi": r"\text{Ester} + [Ce(NO_3)_6]^{2-} \rightarrow \text{Tidak bereaksi}", "alasan": "Tidak memiliki gugus hidroksil bebas.", "warna_akhir": "#f97316", "efek": "none"
        },
        "Uji Natrium Bisulfit (NaHSO3)": {
            "hasil": "(-) Bening", "reaksi": r"\text{Ester} + NaHSO_3 \rightarrow \text{Tidak bereaksi}", "alasan": "Gugus ester stabil akibat efek resonansi elektron sehingga tidak reaktif terhadap nukleofil lemah.", "warna_akhir": "#f8fafc", "efek": "none"
        },
        "Uji Asam Hidroksamat (NH2OH + FeCl3)": {
            "hasil": "(+) Merah Violet", 
            "reaksi": r"3\ R-CONHOH + FeCl_3 \rightarrow Fe(R-CONHO)_3 + 3\ HCl", 
            "alasan": "Ester bereaksi dengan hidroksilamin membentuk asam hidroksamat yang mengikat besi(III) menjadi kompleks berwarna violet.", 
            "warna_akhir": "#c026d3", "efek": "none"
        }
    },
    "Asam Karboksilat": {
        "Uji Ceric Nitrat (CAN)": {
            "hasil": "(-) Tetap Jingga", "reaksi": r"R-COOH + [Ce(NO_3)_6]^{2-} \rightarrow \text{Tidak bereaksi}", "alasan": "Oksigen hidroksil ditarik oleh efek resonansi karbonil sehingga sifat nukleofilnya hilang.", "warna_akhir": "#f97316", "efek": "none"
        },
        "Uji Natrium Bisulfit (NaHSO3)": {
            "hasil": "(-) Bening", "reaksi": r"R-COOH + NaHSO_3 \rightarrow \text{Tidak bereaksi}", "alasan": "Senyawa ini tidak mengandung gugus fungsi aldehida atau keton.", "warna_akhir": "#f8fafc", "efek": "none"
        },
        "Uji Asam Hidroksamat (NH2OH + FeCl3)": {
            "hasil": "(-) Bening", "reaksi": r"R-COOH + NH_2OH + FeCl_3 \rightarrow \text{Tidak bereaksi}", "alasan": "Asam karboksilat bebas tidak membentuk hidroksamat pada kondisi uji ini.", "warna_akhir": "#f8fafc", "efek": "none"
        },
        "Uji Lakmus & Air Barit": {
            "hasil": "(+) Lakmus Merah & Gelembung", 
            "reaksi": r"CO_2 + Ba(OH)_2 \rightarrow BaCO_3 \downarrow + H_2O", 
            "alasan": "Sifat asamnya memerahkan kertas lakmus biru, dan kemampuannya mendonasikan proton dapat mengurai bikarbonat menjadi gas CO2. Gas tersebut mengeruhkan air barit.", 
            "warna_akhir": "#f8fafc", "efek": "bubbles"
        }
    },
    "Alkana / Hidrokarbon Jenuh": {
        "Uji Ceric Nitrat (CAN)": {
            "hasil": "(-) Tetap Jingga", "reaksi": r"\text{Alkana} + [Ce(NO_3)_6]^{2-} \rightarrow \text{Tidak bereaksi}", "alasan": "Senyawa nonpolar inert, tidak memiliki gugus hidroksil.", "warna_akhir": "#f97316", "efek": "none"
        },
        "Uji Natrium Bisulfit (NaHSO3)": {
            "hasil": "(-) Bening", "reaksi": r"\text{Alkana} + NaHSO_3 \rightarrow \text{Tidak bereaksi}", "alasan": "Tidak memiliki gugus fungsi karbonil.", "warna_akhir": "#f8fafc", "efek": "none"
        },
        "Uji Asam Hidroksamat (NH2OH + FeCl3)": {
            "hasil": "(-) Bening", "reaksi": r"\text{Alkana} + NH_2OH \rightarrow \text{Tidak bereaksi}", "alasan": "Tidak memiliki gugus fungsi ester.", "warna_akhir": "#f8fafc", "efek": "none"
        },
        "Uji Lakmus & Air Barit": {
            "hasil": "(-) Bening / Netral", "reaksi": r"\text{Alkana} + NaNaHCO_3 \rightarrow \text{Tidak bereaksi}", 
            "alasan": "Hidrokarbon jenuh bersifat inert. Kegagalan di seluruh uji membuktikan sampel ini kemungkinan adalah golongan alkana (mis. Heksana).", 
            "warna_akhir": "#f8fafc", "efek": "none"
        }
    }
}

# Inisialisasi session state jika belum ada
if "test_started" not in st.session_state:
    st.session_state.test_started = False
if "current_step" not in st.session_state:
    st.session_state.current_step = 0
if "log_history" not in st.session_state:
    st.session_state.log_history = []
if "trigger_animation" not in st.session_state:
    st.session_state.trigger_animation = False

# Inisialisasi State Sub-Bab agar bisa diganti lewat tombol
if "sub_bab_i" not in st.session_state:
    st.session_state.sub_bab_i = "A. Sifat Fisika Hidrokarbon"
if "sub_bab_ii" not in st.session_state:
    st.session_state.sub_bab_ii = "A. Sifat Fisika & Klasifikasi"
if "sub_bab_iii" not in st.session_state:
    st.session_state.sub_bab_iii = "A. Sifat Fisika"
if "sub_bab_iv" not in st.session_state:
    st.session_state.sub_bab_iv = "A. Sifat Fisika"

# ==============================================================================
# 4. SIDEBAR NAVIGASI
# ==============================================================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3022/3022607.png", width=75)
    st.title("OrganicChem v1.0")
    st.write("🔬 *E-Learning & Lab Simulator*")
    st.markdown("---")
    
    pilihan_halaman = st.sidebar.radio(
        "Navigasi Menu:",
        [
            "🏠 HALAMAN UTAMA", 
            "📘 BAB I. HIDROKARBON", 
            "📙 BAB II. ALKOHOL, ETER, DAN FENOL", 
            "📗 BAB III. ALDEHID DAN KETON", 
            "📕 BAB IV. ASAM KARBOKSILAT DAN DERIVATNYA", 
            "🔬 POST TEST"
        ]
    )
    st.markdown("---")
    st.caption("E-Learning Kimia Organik | © 2026")

# ==============================================================================
# 5. LOGIKA KONTEN TIAP HALAMAN
# ==============================================================================

if pilihan_halaman == "🏠 HALAMAN UTAMA":
    st.markdown("""
        <div class="banner-utama">
            <h1 style='color: white; margin-bottom: 5px; font-weight: 700;'>Eksplorasi Dunia Kimia Organik Tanpa Batas! 👋</h1>
            <p style='font-size: 1.2em; opacity: 0.95;'>Solusi cerdas belajar mandiri dan simulasi identifikasi gugus fungsi dalam satu platform.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.subheader("💡 Tentang Platform Ini")
    st.write(
         "Kami hadir untuk menjembatani teori dan praktik. Platform ini dirancang khusus untuk "
        "membantu Anda memahami materi teoretis sekaligus memvisualisasikan reaksi uji kualitatif "
        "senyawa organik secara interaktif—kapan saja dan di mana saja, layaknya memiliki laboratorium pribadi."
    )
    st.markdown("---")
    
    st.markdown("### 📜 Petunjuk Penggunaan")
    st.write("Ikuti langkah-langkah berikut untuk memulai petualangan laboratorium virtualmu:")
    
    p1, p2, p3 = st.columns(3)
    
    with p1:
        st.markdown("""
        <div style="background: white; padding: 20px; border-radius: 12px; border-top: 5px solid #0f766e; box-shadow: 0 4px 6px rgba(0,0,0,0.05); min-height: 180px;">
            <h4 style="margin-top:0; color:#0f766e;">📖 Langkah 1: Pelajari</h4>
            <p style="font-size: 0.95em; color: #475569;">Buka <b>Menu Navigasi</b> di samping kiri. Pilih materi dari <b>BAB I hingga BAB IV</b> untuk membaca teori dasar, sifat fisik/kimia, dan persamaan reaksi kimia senyawa organik.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with p2:
        st.markdown("""
        <div style="background: white; padding: 20px; border-radius: 12px; border-top: 5px solid #14b8a6; box-shadow: 0 4px 6px rgba(0,0,0,0.05); min-height: 180px;">
            <h4 style="margin-top:0; color:#14b8a6;">🧪 Langkah 2: Simulasi</h4>
            <p style="font-size: 0.95em; color: #475569;">Masuk ke menu <b>🔬 POST TEST</b>. Di sana, kamu bisa memilih sampel misterius (<i>Blind Sample</i>) untuk menguji pemahaman analisismu secara langsung.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with p3:
        st.markdown("""
        <div style="background: white; padding: 20px; border-radius: 12px; border-top: 5px solid #0ea5e9; box-shadow: 0 4px 6px rgba(0,0,0,0.05); min-height: 180px;">
            <h4 style="margin-top:0; color:#0ea5e9;">📊 Langkah 3: Amati</h4>
            <p style="font-size: 0.95em; color: #475569;">Klik tombol reaksi, amati perubahan visual pada <b>Visual Lab</b> (warna/endapan/gas), serta baca hasil evaluasi otomatis pada tab <b>Logbook & Analisis</b>.</p>
        </div>
        """, unsafe_allow_html=True)

    st.info("💡 **Tips:** Pastikan koneksi internet stabil agar transisi animasi tabung reaksi berjalan dengan mulus!")

elif pilihan_halaman == "📘 BAB I. HIDROKARBON":
    st.title("📘 BAB I. HIDROKARBON")
    st.write("---")
    
    st.write("**Pilih Sub-Bab Materi:**")
    btn_col1, btn_col2, btn_col3, _ = st.columns([1, 1, 1.2, 1])
    with btn_col1:
        if st.button("A. Sifat Fisika Hidrokarbon", use_container_width=True):
            st.session_state.sub_bab_i = "A. Sifat Fisika Hidrokarbon"
    with btn_col2:
        if st.button("B. Sifat Kimia & Identifikasi", use_container_width=True):
            st.session_state.sub_bab_i = "B. Sifat Kimia & Reaksi Identifikasi"
    with btn_col3:
        if st.button("🧪 Mini-Lab: Hidrokarbon", use_container_width=True):
            st.session_state.sub_bab_i = "🧪 Mini-Lab: Hidrokarbon"
    st.write("---")
    
    if st.session_state.sub_bab_i == "A. Sifat Fisika Hidrokarbon":
        st.markdown("""
        #### **A. Sifat Fisika Hidrokarbon**
        Hidrokarbon adalah senyawa organik yang seluruh strukturnya hanya tersusun atas unsur karbon (C) dan hidrogen (H). Berdasarkan jenis ikatannya, hidrokarbon alifatik dibagi menjadi hidrokarbon jenuh (alkana) dan tidak jenuh (alkena dan alkuna). Sementara itu, hidrokarbon aromatik memiliki rantai siklik konjugasi yang sangat stabil.

        * **Wujud Zat (pada suhu kamar):**
          * Suhu rendah ($C_1 - C_4$) berwujud gas (contoh: metana, etana, etena, etuna).
          * Suhu sedang ($C_5 - C_{17}$) berwujud cair (contoh: pentana, heksana, benzena).
          * Suhu tinggi ($\ge C_{18}$) berwujud padat (contoh: parafin padat).
        * **Kelarutan:** Bersifat nonpolar, sehingga tidak larut dalam air (pelarut polar). Hidrokarbon larut dengan baik dalam sesama pelarut organik nonpolar seperti kloroform ($CHCl_3$), karbon tetraklorida ($CCl_4$), atau eter.
        * **Titik Didih dan Titik Leleh:** Meningkat seiring bertambahnya massa molekul (panjang rantai karbon). Untuk isomer dengan jumlah atom karbon sama, senyawa dengan rantai lurus memiliki titik didih lebih tinggi dibandingkan rantai bercabang karena luas permukaan kontak antarmolekul yang lebih besar.
        * **Densitas:** Memiliki massa jenis (densitas) yang lebih kecil daripada air. Jika dicampur dengan air, lapisan hidrokarbon akan selalu berada di bagian atas.
        """)
        
    elif st.session_state.sub_bab_i == "B. Sifat Kimia & Reaksi Identifikasi":
        st.markdown("""
        #### **B. Sifat Kimia & Reaksi Identifikasi Hidrokarbon**
        
        **1. Alkana (Hidrokarbon Jenuh)**
        * Disebut juga parafin (afinitas kecil) karena sangat tidak reaktif terhadap sebagian besar pereaksi seperti asam kuat, basa kuat, dan oksidator pada suhu kamar.
        * **Uji Iodo (Substitusi Halogen):** Alkana dapat bereaksi dengan halogen ($I_2$) melalui reaksi substitusi radikal bebas dengan bantuan paparan sinar ultraviolet (UV) atau pemanasan tinggi. Reaksi berjalan lambat dan ditandai dengan memudarnya warna ungu dari iodium.
        """)
        st.latex(r"\text{CH}_4 + \text{I}_2 \xrightarrow{\text{Sinar UV} / \Delta} \text{CH}_3\text{I} + \text{HI}")
        
        st.markdown("""
        **2. Alkena dan Alkuna (Hidrokarbon Tidak Jenuh)**
        * Sangat reaktif karena memiliki ikatan rangkap 2 atau rangkap 3 yang kaya akan elektron, sehingga mudah mengalami pemutusan ikatan rangkap (adisi).
        * **Uji Adisi Iodium:** Mengadisi halogen pada ikatan rangkap tanpa memerlukan bantuan sinar UV. Ditandai dengan warna ungu iodium yang memudar/hilang seketika.
        """)
        st.latex(r"\text{R-CH}=\text{CH-R} + \text{I}_2 \rightarrow \text{R-CH(I)-CH(I)-R}")
        
        st.markdown("""
        * **Uji Baeyer (Oksidasi dengan $KMnO_4$):** Alkena atau alkuna dioksidasi oleh larutan kalium permanganat encer dalam suasana netral/basa menghasilkan senyawa glikol. Uji positif ditandai dengan hilangnya warna ungu $KMnO_4$ dan terbentuknya endapan cokelat $MnO_2$.
        """)
        st.latex(r"3\text{CH}_2=\text{CH}_2 + 2\text{KMnO}_4 + 4\text{H}_2\text{O} \rightarrow 3\text{HO-CH}_2\text{-CH}_2\text{-OH} + 2\text{MnO}_2\downarrow + 2\text{KOH}")
        
        st.markdown("""
        **3. Benzena (Hidrokarbon Aromatik)**
        * Memiliki struktur siklik dengan elektron pi yang terdelokalisasi (resonansi) yang memenuhi aturan Hückel ($4n + 2$), membuat intinya sangat stabil.
        * **Uji Bakar:** Ketika dibakar dengan api langsung pada cawan porselin, benzena menghasilkan nyala api berminyak disertai jelaga hitam yang sangat tebal. Jelaga ini terbentuk akibat tingginya persentase kadar karbon dalam benzena dibandingkan kadar hidrogennya.
        """)
        st.latex(r"\text{Benzena} + \text{O}_2 \rightarrow \text{C}_{(s)} \text{ [Jelaga hitam]} + \text{CO} + \text{H}_2\text{O}")
        
    elif st.session_state.sub_bab_i == "🧪 Mini-Lab: Hidrokarbon":
        st.markdown("#### 🧪 Laboratorium Mini: Identifikasi Hidrokarbon")
        st
