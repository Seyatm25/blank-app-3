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
# 2. CUSTOM CSS INTERAKTIF (VERSI MODERN + ANIMASI API JELAGA)
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

/* === CSS TABUNG REAKSI === */
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

/* === CSS ANIMASI NYALA API & JELAGA === */
.flame-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-end;
    height: 350px;
    padding-top: 20px;
}
.flame-area {
    position: relative;
    width: 120px;
    height: 150px;
}
.flame-core {
    position: absolute;
    bottom: 0;
    left: 50%;
    transform-origin: center bottom;
    border-radius: 50% 0 50% 50%;
    animation: flicker 0.3s infinite alternate;
    z-index: 2;
}
.flame-core.clean {
    width: 45px; height: 45px; background: linear-gradient(to top right, #1d4ed8, #60a5fa); transform: translateX(-50%) rotate(-45deg); box-shadow: 0 0 15px #60a5fa;
}
.flame-core.medium {
    width: 60px; height: 60px; background: linear-gradient(to top right, #d97706, #fbbf24); transform: translateX(-50%) rotate(-45deg); box-shadow: 0 0 25px #f59e0b;
}
.flame-core.heavy {
    width: 80px; height: 80px; background: linear-gradient(to top right, #b91c1c, #f97316); transform: translateX(-50%) rotate(-45deg); box-shadow: 0 0 35px #ea580c;
}
.cawan {
    width: 100px; height: 35px; background: #cbd5e1; border-radius: 5px 5px 40px 40px; border: 3px solid #94a3b8; z-index: 3; position: relative; margin-top: -15px; box-shadow: inset 0 -5px 10px rgba(0,0,0,0.2);
}
.smoke-particle {
    position: absolute; border-radius: 50%; opacity: 0; z-index: 1; bottom: 20px;
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
@keyframes flicker {
    0% { transform: translateX(-50%) rotate(-45deg) scale(0.95); }
    100% { transform: translateX(-50%) rotate(-45deg) scale(1.05); }
}
@keyframes flySoot {
    0% { transform: translateY(0) scale(1); opacity: 0.8; }
    100% { transform: translateY(-160px) scale(3); opacity: 0; }
}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. FUNGSI HELPER & DATABASE (TERMASUK RENDER NYALA API)
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

def render_flame(tipe):
    html = "<div class='flame-wrapper'><div class='flame-area'>"
    
    if tipe == "bersih":
        html += "<div class='smoke-particle' style='width:10px;height:10px;left:45%;background:#e2e8f0;animation:flySoot 2.5s infinite'></div>"
        html += "<div class='flame-core clean'></div>"
        desc = "<div style='text-align:center; color:#2563eb; font-weight:bold; margin-top:20px; background:white; padding:10px; border-radius:10px; border:1px solid #bfdbfe;'>🔥 Nyala Api Biru (Bersih)<br><span style='font-size:0.85em;color:#64748b;'>Hampir tidak ada jelaga terbentuk.</span></div>"
    
    elif tipe == "sedang":
        html += "<div class='smoke-particle' style='width:15px;height:15px;left:35%;background:#94a3b8;animation:flySoot 2s infinite'></div>"
        html += "<div class='smoke-particle' style='width:12px;height:12px;left:55%;background:#64748b;animation:flySoot 2.2s infinite 0.5s'></div>"
        html += "<div class='flame-core medium'></div>"
        desc = "<div style='text-align:center; color:#d97706; font-weight:bold; margin-top:20px; background:white; padding:10px; border-radius:10px; border:1px solid #fde68a;'>🔥 Nyala Api Kuning<br><span style='font-size:0.85em;color:#64748b;'>Menghasilkan sedikit asap jelaga tipis.</span></div>"
    
    elif tipe == "kotor":
        html += "<div class='smoke-particle' style='width:25px;height:25px;left:30%;background:#0f172a;animation:flySoot 1.5s infinite'></div>"
        html += "<div class='smoke-particle' style='width:30px;height:30px;left:50%;background:#000000;animation:flySoot 1.8s infinite 0.3s'></div>"
        html += "<div class='smoke-particle' style='width:22px;height:22px;left:65%;background:#1e293b;animation:flySoot 1.6s infinite 0.7s'></div>"
        html += "<div class='flame-core heavy'></div>"
        desc = "<div style='text-align:center; color:#b91c1c; font-weight:bold; margin-top:20px; background:white; padding:10px; border-radius:10px; border:1px solid #fca5a5;'>⚫ 🔥 Nyala Api Merah/Berminyak<br><span style='font-size:0.85em;color:#64748b;'>Kadar karbon sangat tinggi, jelaga hitam pekat!</span></div>"
    
    html += "</div><div class='cawan'></div>" + desc + "</div>"
    return html

reagen_colors = {
    "Uji Ceric Nitrat (CAN)": "#fef08a", 
    "Uji Pereaksi Jones": "#f97316", 
    "Uji Pereaksi Lucas": "#f8fafc", 
    "Uji Natrium Bisulfit (NaHSO3)": "#f8fafc", 
    "Uji Pereaksi Fehling": "#3b82f6", 
    "Uji Pereaksi Schiff": "#f8fafc",
    "Uji Iodoform (NaOH + I2)": "#f8fafc",
    "Uji Asam Hidroksamat (NH2OH + FeCl3)": "#f8fafc",
    "Uji Lakmus & Air Barit": "#f8fafc"
}

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

# DATABASE HASIL REAKSI YANG SUDAH DIPERBAIKI (VALID)
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
            "reaksi": r"3\ R-CH_2OH + 4\ CrO_3 + 6\ H_2SO_4 \rightarrow 3\ R-COOH + 2\ Cr_2(SO_4)_3 + 9\ H_2O", 
            "alasan": "Memiliki atom hidrogen alfa. Gugus -OH dioksidasi lanjut langsung menjadi asam karboksilat, sedangkan Kromium(VI) yang berwarna jingga tereduksi menjadi Kromium(III) yang berwarna hijau.", 
            "warna_akhir": "#10b981", "efek": "none"
        },
        "Uji Pereaksi Lucas": {
            "hasil": "(-) Tetap Bening", 
            "reaksi": r"R-CH_2OH + HCl \xrightarrow{ZnCl_2} \text{Tidak ada reaksi}", 
            "alasan": "Karbokation primer sangat tidak stabil sehingga tidak mampu bereaksi dengan pereaksi Lucas pada suhu kamar (larutan tetap bening).", 
            "warna_akhir": "#f8fafc", "efek": "none"
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
            "alasan": "Alkohol sekunder dioksidasi menjadi keton, ditandai dengan perubahan warna larutan dari jingga ke hijau akibat terbentuknya ion kromium(III).", 
            "warna_akhir": "#10b981", "efek": "none"
        },
        "Uji Pereaksi Lucas": {
            "hasil": "(+) Emulsi Putih (Perlu Pemanasan)", 
            "reaksi": r"R_2CH-OH + HCl \xrightarrow{ZnCl_2} R_2CH-Cl \downarrow + H_2O", 
            "alasan": "Karbokation sekunder memiliki stabilitas menengah. Bereaksi menghasilkan alkil klorida yang tidak larut setelah 5-10 menit dengan bantuan pemanasan.", 
            "warna_akhir": "#e2e8f0", "efek": "cloudy"
        },
        "Uji Iodoform (NaOH + I2)": {
            "hasil": "(+) Endapan Kuning", 
            "reaksi": r"R-CH(OH)-CH_3 + 4\ I_2 + 6\ NaOH \rightarrow CHI_3 \downarrow + R-COONa + 5\ NaI + 5\ H_2O", 
            "alasan": "Struktur metil karbinol dioksidasi oleh iodin menjadi metil keton, lalu membentuk kristal iodoform (CHI3) berwarna kuning yang sukar larut.", 
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
            "alasan": "Alkohol tersier tidak memiliki atom hidrogen alfa pada karbon karbinolnya sehingga resisten terhadap oksidasi oleh pereaksi Jones (warna tetap jingga).", 
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
            "hasil": "(-) Tetap Kuning", 
            "reaksi": r"R-CHO + [Ce(NO_3)_6]^{2-} \rightarrow \text{Tidak bereaksi}", 
            "alasan": "Aldehida tidak memiliki gugus hidroksil (-OH) bebas sehingga tidak membentuk kompleks dan pereaksi tetap berwarna kuning asli.", 
            "warna_akhir": "#fef08a", "efek": "none"
        },
        "Uji Natrium Bisulfit (NaHSO3)": {
            "hasil": "(+) Endapan Putih", 
            "reaksi": r"R-CHO + NaHSO_3 \rightarrow R-CH(OH)SO_3Na \downarrow", 
            "alasan": "Nukleofil bisulfit menyerang gugus karbonil aldehida yang reaktif dan tidak terhalang sterik, menghasilkan produk adisi berupa kristal putih.", 
            "warna_akhir": "#f8fafc", "efek": "precipitate", "warna_endapan": "#ffffff"
        },
        "Uji Pereaksi Fehling": {
            "hasil": "(+) Merah Bata", 
            "reaksi": r"R-CHO + 2\ Cu^{2+} + 5\ OH^- \rightarrow R-COO^- + Cu_2O \downarrow + 3\ H_2O", 
            "alasan": "Aldehida adalah reduktor kuat yang mereduksi kompleks Cu(II) yang berwarna biru menjadi endapan tembaga(I) oksida (Cu2O) berwarna merah bata.", 
            "warna_akhir": "#1e3a8a", "efek": "precipitate", "warna_endapan": "#b91c1c"
        },
        "Uji Pereaksi Schiff": {
            "hasil": "(+) Ungu / Magenta", 
            "reaksi": r"\text{Aldehida} + \text{Pereaksi Schiff} \rightarrow \text{Kompleks Magenta}", 
            "alasan": "Reaksi adisi spesifik antara aldehida dengan pereaksi Schiff yang mengembalikan struktur kromofor p-rosanilin hidroklorida menjadi ungu murni.", 
            "warna_akhir": "#d946ef", "efek": "none"
        }
    },
    "Keton (Alkanon)": {
        "Uji Ceric Nitrat (CAN)": {
            "hasil": "(-) Tetap Kuning", 
            "reaksi": r"\text{Keton} + [Ce(NO_3)_6]^{2-} \rightarrow \text{Tidak bereaksi}", 
            "alasan": "Keton tidak memiliki gugus fungsi hidroksil sehingga warna asal pereaksi CAN (kuning) tidak berubah.", 
            "warna_akhir": "#fef08a", "efek": "none"
        },
        "Uji Natrium Bisulfit (NaHSO3)": {
            "hasil": "(+) Endapan Putih", 
            "reaksi": r"CH_3-CO-CH_3 + NaHSO_3 \rightarrow (CH_3)_2C(OH)SO_3Na \downarrow", 
            "alasan": "Keton suku rendah (seperti aseton) memiliki halangan sterik kecil sehingga masih bisa diadisi oleh bisulfit membentuk endapan kristal putih.", 
            "warna_akhir": "#f8fafc", "efek": "precipitate", "warna_endapan": "#ffffff"
        },
        "Uji Pereaksi Fehling": {
            "hasil": "(-) Tetap Biru", 
            "reaksi": r"\text{Keton} + Cu^{2+} \rightarrow \text{Tidak bereaksi}", 
            "alasan": "Keton tidak memiliki atom hidrogen yang terikat pada gugus karbonil sehingga tidak bersifat reduktor; warna larutan fehling tetap biru.", 
            "warna_akhir": "#3b82f6", "efek": "none"
        },
        "Uji Iodoform (NaOH + I2)": {
            "hasil": "(+) Endapan Kuning", 
            "reaksi": r"R-CO-CH_3 + 3\ I_2 + 4\ NaOH \rightarrow CHI_3 \downarrow + R-COONa + 3\ NaI + 3\ H_2O", 
            "alasan": "Memiliki gugus metil yang terikat langsung pada karbonil (metil keton), bereaksi positif membentuk endapan iodoform kuning.", 
            "warna_akhir": "#fef08a", "efek": "precipitate", "warna_endapan": "#facc15"
        }
    },
    "Ester (Alkil Alkanoat)": {
        "Uji Ceric Nitrat (CAN)": {
            "hasil": "(-) Tetap Kuning", "reaksi": r"\text{Ester} + [Ce(NO_3)_6]^{2-} \rightarrow \text{Tidak bereaksi}", "alasan": "Tidak memiliki gugus hidroksil bebas untuk berkoordinasi.", "warna_akhir": "#fef08a", "efek": "none"
        },
        "Uji Natrium Bisulfit (NaHSO3)": {
            "hasil": "(-) Bening", "reaksi": r"\text{Ester} + NaHSO_3 \rightarrow \text{Tidak bereaksi}", "alasan": "Gugus ester stabil akibat efek resonansi elektron sehingga tidak reaktif terhadap nukleofil lemah seperti bisulfit.", "warna_akhir": "#f8fafc", "efek": "none"
        },
        "Uji Asam Hidroksamat (NH2OH + FeCl3)": {
            "hasil": "(+) Merah Violet", 
            "reaksi": r"3\ R-CONHOH + FeCl_3 \rightarrow Fe(R-CONHO)_3 + 3\ HCl", 
            "alasan": "Ester bereaksi dengan hidroksilamin membentuk asam hidroksamat, yang kemudian mengkelat besi(III) menjadi kompleks berwarna violet.", 
            "warna_akhir": "#c026d3", "efek": "none"
        }
    },
    "Asam Karboksilat": {
        "Uji Ceric Nitrat (CAN)": {
            "hasil": "(-) Tetap Kuning", "reaksi": r"R-COOH + [Ce(NO_3)_6]^{2-} \rightarrow \text{Tidak bereaksi}", "alasan": "Oksigen hidroksil ditarik oleh efek resonansi karbonil kuat sehingga kehilangan sifat nukleofilnya terhadap ion Cerium.", "warna_akhir": "#fef08a", "efek": "none"
        },
        "Uji Natrium Bisulfit (NaHSO3)": {
            "hasil": "(-) Bening", "reaksi": r"R-COOH + NaHSO_3 \rightarrow \text{Tidak bereaksi}", "alasan": "Senyawa ini tidak mengandung gugus fungsi aldehida atau metil keton.", "warna_akhir": "#f8fafc", "efek": "none"
        },
        "Uji Asam Hidroksamat (NH2OH + FeCl3)": {
            "hasil": "(-) Bening", "reaksi": r"R-COOH + NH_2OH + FeCl_3 \rightarrow \text{Tidak bereaksi}", "alasan": "Asam karboksilat bebas tidak membentuk asam hidroksamat pada kondisi uji ini karena gugus pergi (-OH) kurang reaktif dibanding ester.", "warna_akhir": "#f8fafc", "efek": "none"
        },
        "Uji Lakmus & Air Barit": {
            "hasil": "(+) Lakmus Merah & Gelembung", 
            "reaksi": r"CO_2 + Ba(OH)_2 \rightarrow BaCO_3 \downarrow + H_2O", 
            "alasan": "Sifat asamnya memicu gas CO2 keluar saat bereaksi dengan bikarbonat. Gas CO2 tersebut bereaksi dengan air barit menghasilkan endapan BaCO3 (larutan menjadi keruh/bergelembung).", 
            "warna_akhir": "#f8fafc", "efek": "bubbles"
        }
    },
    "Alkana / Hidrokarbon Jenuh": {
        "Uji Ceric Nitrat (CAN)": {
            "hasil": "(-) Tetap Kuning", "reaksi": r"\text{Alkana} + [Ce(NO_3)_6]^{2-} \rightarrow \text{Tidak bereaksi}", "alasan": "Senyawa nonpolar inert, tidak memiliki gugus hidroksil.", "warna_akhir": "#fef08a", "efek": "none"
        },
        "Uji Natrium Bisulfit (NaHSO3)": {
            "hasil": "(-) Bening", "reaksi": r"\text{Alkana} + NaHSO_3 \rightarrow \text{Tidak bereaksi}", "alasan": "Tidak memiliki gugus fungsi karbonil aktif.", "warna_akhir": "#f8fafc", "efek": "none"
        },
        "Uji Asam Hidroksamat (NH2OH + FeCl3)": {
            "hasil": "(-) Bening", "reaksi": r"\text{Alkana} + NH_2OH \rightarrow \text{Tidak bereaksi}", "alasan": "Tidak memiliki gugus fungsi ester yang dapat diubah menjadi hidroksamat.", "warna_akhir": "#f8fafc", "efek": "none"
        },
        "Uji Lakmus & Air Barit": {
            "hasil": "(-) Bening / Netral", "reaksi": r"\text{Alkana} + NaHCO_3 \rightarrow \text{Tidak bereaksi}", 
            "alasan": "Hidrokarbon jenuh bersifat inert. Kegagalan di seluruh uji membuktikan sampel ini kemungkinan besar adalah golongan alkana.", 
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
        st.write("Silakan pilih sampel hidrokarbon dan jenis uji untuk melihat hasil analisanya secara visual.")
        
        c1, c2 = st.columns(2)
        with c1:
            sampel_h = st.selectbox("Pilih Sampel Hidrokarbon:", ["Alkana (Heksana)", "Alkena (Sikloheksena)", "Aromatik (Benzena)"])
            uji_h = st.selectbox("Pilih Jenis Uji Reaksi:", ["Uji Adisi Iodium (Gelap/Tanpa UV)", "Uji Oksidasi Baeyer (KMnO4)", "Uji Bakar Kualitatif"])
        
        with c2:
            st.write("**Visualisasi Hasil Uji:**")
            if sampel_h == "Alkana (Heksana)":
                if uji_h == "Uji Adisi Iodium (Gelap/Tanpa UV)":
                    st.markdown(render_tube("65%", "#9333ea", "none"), unsafe_allow_html=True)
                    st.warning("⚠️ **Hasil:** (-) Negatif. Warna ungu iodium tetap bertahan karena alkana jenuh tidak dapat diadisi tanpa bantuan radiasi sinar UV.")
                elif uji_h == "Uji Oksidasi Baeyer (KMnO4)":
                    st.markdown(render_tube("65%", "#a855f7", "none"), unsafe_allow_html=True)
                    st.warning("⚠️ **Hasil:** (-) Negatif. Larutan tetap berwarna ungu murni. Alkana bersifat parafin (inert) terhadap oksidator.")
                else:
                    # ANIMASI API BERSIH UNTUK ALKANA
                    st.markdown(render_flame("bersih"), unsafe_allow_html=True)
            
            elif sampel_h == "Alkena (Sikloheksena)":
                if uji_h == "Uji Adisi Iodium (Gelap/Tanpa UV)":
                    st.markdown(render_tube("65%", "#f8fafc", "none"), unsafe_allow_html=True)
                    st.success("✅ **Hasil:** (+) Positif. Warna ungu larutan iodium hilang seketika menjadi bening karena terjadi adisi spontan pada ikatan rangkap.")
                elif uji_h == "Uji Oksidasi Baeyer (KMnO4)":
                    st.markdown(render_tube("65%", "#78350f", "precipitate", warna_endapan="#451a03"), unsafe_allow_html=True)
                    st.success("✅ **Hasil:** (+) Positif. Warna ungu KMnO4 menghilang dan terbentuk endapan cokelat tua dari MnO2 hasil reduksi.")
                else:
                    # ANIMASI API KUNING UNTUK ALKENA
                    st.markdown(render_flame("sedang"), unsafe_allow_html=True)
            
            elif sampel_h == "Aromatik (Benzena)":
                if uji_h == "Uji Adisi Iodium (Gelap/Tanpa UV)":
                    st.markdown(render_tube("65%", "#9333ea", "none"), unsafe_allow_html=True)
                    st.warning("⚠️ **Hasil:** (-) Negatif. Cincin aromatik terkonjugasi sangat stabil, menolak pemutusan rantai melalui reaksi adisi halogen biasa.")
                elif uji_h == "Uji Oksidasi Baeyer (KMnO4)":
                    st.markdown(render_tube("65%", "#a855f7", "none"), unsafe_allow_html=True)
                    st.warning("⚠️ **Hasil:** (-) Negatif. Larutan tetap berwarna ungu. Resonansi benzena melindunginya dari serangan oksidator biasa.")
                else:
                    # ANIMASI API MERAH & JELAGA UNTUK AROMATIK
                    st.markdown(render_flame("kotor"), unsafe_allow_html=True)

elif pilihan_halaman == "📙 BAB II. ALKOHOL, ETER, DAN FENOL":
    st.title("📙 BAB II. ALKOHOL, ETER, DAN FENOL")
    st.write("---")
    
    st.write("**Pilih Sub-Bab Materi:**")
    btn_col1, btn_col2, btn_col3, btn_col4, _ = st.columns([1.2, 1.2, 1.2, 1.2, 1])
    with btn_col1:
        if st.button("A. Sifat Fisika & Klasifikasi", use_container_width=True):
            st.session_state.sub_bab_ii = "A. Sifat Fisika & Klasifikasi"
    with btn_col2:
        if st.button("B. Reaksi Alkohol & Eter", use_container_width=True):
            st.session_state.sub_bab_ii = "B. Reaksi Alkohol & Eter"
    with btn_col3:
        if st.button("C. Reaksi Kimia Fenol", use_container_width=True):
            st.session_state.sub_bab_ii = "C. Reaksi Kimia Fenol"
    with btn_col4:
        if st.button("🧪 Mini-Lab: Alkohol-Fenol", use_container_width=True):
            st.session_state.sub_bab_ii = "🧪 Mini-Lab: Alkohol-Fenol"
    st.write("---")
    
    if st.session_state.sub_bab_ii == "A. Sifat Fisika & Klasifikasi":
        st.markdown("""
        #### **A. Sifat Fisika & Klasifikasi**
        * **Alkohol ($R - OH$):** Turunan alkana di mana satu atau lebih atom H digantikan oleh gugus hidroksil ($-OH$). Alkohol diklasifikasikan menjadi alkohol primer ($1^\circ$), sekunder ($2^\circ$), dan tersier ($3^\circ$) berdasarkan jenis atom C yang mengikat gugus $-OH$. Alkohol suhu rendah mudah larut dalam air karena sanggup membentuk ikatan hidrogen dengan molekul air. Kelarutan berkurang seiring bertambah panjangnya rantai karbon, namun meningkat pada struktur yang bercabang banyak.
        * **Eter ($R^1 - O - R^2$):** Isomer fungsional dari alkohol. Titik didih eter jauh lebih rendah dibandingkan alkohol isomernya karena tidak memiliki ikatan hidrogen antar-sesama molekul eter. Kelarutannya dalam air mirip dengan alkohol karena oksigen pada eter masih bisa menerima ikatan hidrogen dari air.
        * **Fenol ($C_6H_5OH$):** Senyawa hidrokarbon aromatik yang mengikat gugus fungsi $-OH$ langsung pada cincin benzena. Berupa padatan/hablur pada suhu kamar, sedikit larut dalam air, dan larutannya bersifat asam lemah karena ion fenoksida yang terbentuk distabilkan oleh resonansi.
        """)
        
    elif st.session_state.sub_bab_ii == "B. Reaksi Alkohol & Eter":
        st.markdown("""
        #### **B. Persamaan Reaksi Kimia Alkohol & Eter**
        
        **1. Pereaksi Lucas (Substitusi Gugus $-OH$ oleh Cl)**
        * Menggunakan campuran $HCl$ pekat dan katalis $ZnCl_2$ untuk membedakan jenis alkohol berdasarkan kecepatan reaksinya.
        * Alkohol $3^\circ$: Bereaksi seketika (larutan langsung keruh/terbentuk dua lapisan terpisah).
        * Alkohol $2^\circ$: Bereaksi dalam waktu 5–10 menit dengan sedikit pemanasan.
        * Alkohol $1^\circ$: Tidak bereaksi pada suhu kamar.
        """)
        st.latex(r"\text{R}_3\text{C-OH} + \text{HCl} \xrightarrow{\text{ZnCl}_2} \text{R}_3\text{C-Cl}\downarrow \text{ (Keruh)} + \text{H}_2\text{O}")
        
        st.markdown("""
        **2. Pereaksi Jones (Oksidasi Alkohol)**
        * Menggunakan kromium trioksida ($CrO_3$) dalam asam sulfat pekat. Uji positif ditandai dengan perubahan warna pereaksi dari jingga menjadi hijau.
        * Alkohol $1^\circ$ dioksidasi menjadi Aldehida, lalu berlanjut menjadi Asam Karboksilat.
        * Alkohol $2^\circ$ dioksidasi menjadi Keton.
        * Alkohol $3^\circ$ tidak dapat dioksidasi (warna tetap jingga).
        """)
        st.latex(r"\text{R-CH}_2\text{-OH} \xrightarrow{\text{CrO}_3/\text{H}_2\text{SO}_4} \text{R-COOH [Jingga } \rightarrow \text{ Hijau]}")
        
        st.markdown("""
        **3. Uji Iodoform**
        * Khusus untuk alkohol yang memiliki gugus metil alfa $(CH_3CH(OH))$, seperti etanol atau 2-propanol. Bereaksi dengan $I_2$ dalam suasana basa ($NaOH$) membentuk endapan kuning kristal iodoform ($CHI_3$) yang berbau khas.
        """)
        st.latex(r"\text{R-CH(OH)-CH}_3 + 4\text{I}_2 + 6\text{NaOH} \rightarrow \text{R-COONa} + \text{CHI}_3\downarrow + 5\text{NaI} + 5\text{H}_2\text{O}")
        
    elif st.session_state.sub_bab_ii == "C. Reaksi Kimia Fenol":
        st.markdown("""
        #### **C. Persamaan Reaksi Kimia Fenol**
        
        **1. Reaksi dengan Basa Kuat ($NaOH$)**
        * Membentuk garam natrium fenoksida yang larut dalam air (menunjukkan sifat asam lemah fenol).
        """)
        st.latex(r"\text{C}_6\text{H}_5\text{OH} + \text{NaOH} \rightarrow \text{C}_6\text{H}_5\text{ONa} + \text{H}_2\text{O}")
        
        st.markdown("""
        **2. Uji Besi(III) Klorida ($FeCl_3$)**
        * Ion fenoksida membentuk senyawa kompleks koordinasi dengan besi(III) yang menghasilkan warna ungu tua/kehitaman yang khas.
        """)
        st.latex(r"6\text{C}_6\text{H}_5\text{OH} + \text{FeCl}_3 \rightarrow [\text{Fe(OC}_6\text{H}_5)_6]^{3-} + 3\text{H}^+ + 3\text{Cl}^-")

    elif st.session_state.sub_bab_ii == "🧪 Mini-Lab: Alkohol-Fenol":
        st.markdown("#### 🧪 Laboratorium Mini: Alkohol & Fenol")
        c1, c2 = st.columns(2)
        with c1:
            sampel_a = st.selectbox("Pilih Sampel Gugus Fungsi:", ["Alkohol Primer", "Alkohol Sekunder", "Alkohol Tersier", "Fenol"])
            uji_a = st.selectbox("Pilih Jenis Uji Reaksi:", ["Uji Ceric Nitrat (CAN)", "Pereaksi Lucas", "Uji FeCl3"])
            
        with c2:
            st.write("**Visualisasi Hasil Uji:**")
            if sampel_a == "Fenol":
                if uji_a == "Uji FeCl3":
                    st.markdown(render_tube("65%", "#4c1d95", "none"), unsafe_allow_html=True)
                    st.success("✅ **Hasil:** (+) Positif Ungu Kompleks. Ion Besi(III) mengikat gugus fenoksida membentuk kompleks ungu pekat.")
                else:
                    st.markdown(render_tube("65%", "#f97316", "none"), unsafe_allow_html=True)
                    st.warning("⚠️ **Hasil:** Tidak menghasilkan reaksi khas/Negatif.")
            else:
                if uji_a == "Uji Ceric Nitrat (CAN)":
                    st.markdown(render_tube("65%", "#ef4444", "none"), unsafe_allow_html=True)
                    st.success("✅ **Hasil:** (+) Positif Kompleks Merah Ceri untuk seluruh jenis alkohol bebas.")
                elif uji_a == "Pereaksi Lucas":
                    if sampel_a == "Alkohol Tersier":
                        st.markdown(render_tube("65%", "#cbd5e1", "cloudy"), unsafe_allow_html=True)
                        st.success("✅ **Hasil:** (+) Keruh Seketika. Karbokation tersier stabil memicu pembentukan emulsi alkil klorida secara instan.")
                    elif sampel_a == "Alkohol Sekunder":
                        st.markdown(render_tube("65%", "#e2e8f0", "cloudy"), unsafe_allow_html=True)
                        st.info("ℹ️ **Hasil:** (+) Keruh lambat (5-10 menit), membutuhkan proses pemanasan.")
                    else:
                        st.markdown(render_tube("65%", "#f8fafc", "none"), unsafe_allow_html=True)
                        st.warning("⚠️ **Hasil:** (-) Tetap Bening. Alkohol primer sangat tidak reaktif terhadap uji Lucas pada suhu kamar.")
                else:
                    st.markdown(render_tube("65%", "#fecdd3", "none"), unsafe_allow_html=True)
                    st.warning("⚠️ **Hasil:** (-) Negatif. Alkohol biasa tidak memicu warna ungu dengan FeCl3.")

elif pilihan_halaman == "📗 BAB III. ALDEHID DAN KETON":
    st.title("📗 BAB III. ALDEHID DAN KETON")
    st.write("---")
    
    st.write("**Pilih Sub-Bab Materi:**")
    btn_col1, btn_col2, btn_col3, btn_col4, _ = st.columns([1, 1.2, 1.5, 1.2, 1])
    with btn_col1:
        if st.button("A. Sifat Fisika", use_container_width=True):
            st.session_state.sub_bab_iii = "A. Sifat Fisika"
    with btn_col2:
        if st.button("B. Reaksi Adisi Karbonil", use_container_width=True):
            st.session_state.sub_bab_iii = "B. Reaksi Adisi Karbonil"
    with btn_col3:
        if st.button("C. Reaksi Diferensiasi (Uji Reduksi)", use_container_width=True):
            st.session_state.sub_bab_iii = "C. Reaksi Diferensiasi (Uji Reduksi)"
    with btn_col4:
        if st.button("🧪 Mini-Lab: Karbonil", use_container_width=True):
            st.session_state.sub_bab_iii = "🧪 Mini-Lab: Karbonil"
    st.write("---")
    
    if st.session_state.sub_bab_iii == "A. Sifat Fisika":
        st.markdown("""
        #### **A. Sifat Fisika**
        Aldehida (${R-CHO}$) dan keton (${R-CO-R}'$) adalah senyawa organik isomer fungsional yang sama-sama memiliki gugus fungsi karbonil (${C}={O}$). Perbedaan utamanya terletak pada atom C karbonil aldehida yang mengikat minimal satu atom hidrogen, sedangkan pada keton terikat pada dua gugus alkil/aril.

        Metanal (formaldehida) merupakan suku paling rendah yang berwujud gas pada suhu kamar dengan bau menyengat. Suku-suku aldehida rendah lainnya berupa cairan dengan bau yang semakin harum (seperti aroma buah-buahan) seiring bertambah panjangnya rantai C. Keton suku rendah (seperti aseton atau propanon) berupa cairan encer, mudah larut dalam air, mudah menguap, dan memiliki aroma yang segar.
        """)
        
    elif st.session_state.sub_bab_iii == "B. Reaksi Adisi Karbonil":
        st.markdown("""
        #### **B. Reaksi Adisi Karbonil**
        
        **1. Adisi Natrium Bisulit (${NaHSO}_3$):**
        * Reaksi adisi nukleofilik pada gugus karbonil aldehida atau metil keton menghasilkan senyawa aduk berupa kristal padat berwarna putih yang sukar larut.
        """)
        st.latex(r"\text{R-CHO} + \text{NaHSO}_3 \rightarrow \text{R-CH(OH)-SO}_3\text{Na}")
        
        st.markdown("""
        **2. Pembentukan Hemiasetal dan Asetal:**
        * Reaksi reversibel gugus karbonil dengan alkohol dalam suasana asam gas $HCl$.
        """)
        st.latex(r"\text{R-CHO} + \text{R'OH} \xrightarrow{\text{HCl}} \text{R-CH(OH)(OR')}")
        
    elif st.session_state.sub_bab_iii == "C. Reaksi Diferensiasi (Uji Reduksi)":
        st.markdown("""
        #### **C. Reaksi Diferensiasi (Uji Daya Reduksi Aldehida)**
        Aldehida bertindak sebagai reduktor kuat karena keberadaan atom hidrogen pada karbon karbonilnya, sedangkan keton tidak memiliki daya pereduksi dan memberikan hasil negatif pada uji-uji berikut:
        
        **1. Uji Tollens (Cermin Perak):**
        * Aldehida mereduksi ion kompleks perak beramoniak $[\text{Ag(NH}_3)_2]^+$ menjadi logam perak murni yang menempel di dinding tabung reaksi membentuk cermin perak.
        """)
        st.latex(r"\text{R-CHO} + 2[\text{Ag(NH}_3)_2]^+ + 3\text{OH}^- \rightarrow \text{R-COO}^- + 2\text{Ag}\downarrow + 4\text{NH}_3 + 2\text{H}_2\text{O}")
        
        st.markdown("""
        **2. Uji Fehling:**
        * Aldehida mereduksi ion ${Cu}^{2+}$ yang berada dalam bentuk kompleks tartrat basa, menghasilkan endapan merah bata kupro oksida (${Cu}_2{O}$).
        """)
        st.latex(r"\text{R-CHO} + 2\text{Cu}^{2+} + 5\text{OH}^- \rightarrow \text{R-COO}^- + \text{Cu}_2\text{O}\downarrow + 3\text{H}_2\text{O}")

    elif st.session_state.sub_bab_iii == "🧪 Mini-Lab: Karbonil":
        st.markdown("#### 🧪 Laboratorium Mini: Identifikasi Gugus Karbonil")
        c1, c2 = st.columns(2)
        with c1:
            sampel_k = st.selectbox("Pilih Senyawa Karbonil:", ["Aldehida (Alkanal)", "Keton (Alkanon)"])
            uji_k = st.selectbox("Pilih Reaksi Diferensiasi:", ["Uji Reduksi Fehling", "Uji Spesifik Schiff", "Uji Bisulfit"])
            
        with c2:
            st.write("**Visualisasi Hasil Uji:**")
            if sampel_k == "Aldehida (Alkanal)":
                if uji_k == "Uji Reduksi Fehling":
                    st.markdown(render_tube("65%", "#1e3a8a", "precipitate", warna_endapan="#b91c1c"), unsafe_allow_html=True)
                    st.success("✅ **Hasil:** (+) Terbentuk Endapan Merah Bata ($Cu_2O$) akibat daya reduksi gugus aldehida.")
                elif uji_k == "Uji Spesifik Schiff":
                    st.markdown(render_tube("65%", "#d946ef", "none"), unsafe_allow_html=True)
                    st.success("✅ **Hasil:** (+) Terbentuk Kompleks Warna Magenta/Ungu pekat khas kualitatif alkanal.")
                else:
                    st.markdown(render_tube("65%", "#f8fafc", "precipitate", warna_endapan="#ffffff"), unsafe_allow_html=True)
                    st.success("✅ **Hasil:** (+) Terbentuk endapan kristal putih adisi bisulfit.")
            else:
                if uji_k == "Uji Reduksi Fehling":
                    st.markdown(render_tube("65%", "#3b82f6", "none"), unsafe_allow_html=True)
                    st.error("❌ **Hasil:** (-) Tetap Biru. Keton tidak memilki atom hidrogen bebas pada C karbonil sehingga tidak dapat dioksidasi.")
                elif uji_k == "Uji Spesifik Schiff":
                    st.markdown(render_tube("65%", "#f8fafc", "none"), unsafe_allow_html=True)
                    st.warning("⚠️ **Hasil:** (-) Hasil negatif (Bening), larutan tidak berubah warna.")
                else:
                    st.markdown(render_tube("65%", "#f8fafc", "precipitate", warna_endapan="#ffffff"), unsafe_allow_html=True)
                    st.success("✅ **Hasil:** (+) Terbentuk endapan kristal putih (Khusus untuk metil keton / keton suku rendah seperti aseton).")

elif pilihan_halaman == "📕 BAB IV. ASAM KARBOKSILAT DAN DERIVATNYA":
    st.title("📕 BAB IV. ASAM KARBOKSILAT DAN DERIVATNYA")
    st.write("---")
    
    st.write("**Pilih Sub-Bab Materi:**")
    btn_col1, btn_col2, btn_col3, btn_col4, _ = st.columns([1, 1.5, 1.5, 1.2, 1])
    with btn_col1:
        if st.button("A. Sifat Fisika", use_container_width=True):
            st.session_state.sub_bab_iv = "A. Sifat Fisika"
    with btn_col2:
        if st.button("B. Reaksi Kimia Asam Karboksilat", use_container_width=True):
            st.session_state.sub_bab_iv = "B. Reaksi Kimia Asam Karboksilat"
    with btn_col3:
        if st.button("C. Identifikasi Derivat (Ester)", use_container_width=True):
            st.session_state.sub_bab_iv = "C. Identifikasi Derivat (Ester)"
    with btn_col4:
        if st.button("🧪 Mini-Lab: Karboksilat", use_container_width=True):
            st.session_state.sub_bab_iv = "🧪 Mini-Lab: Karboksilat"
    st.write("---")
    
    if st.session_state.sub_bab_iv == "A. Sifat Fisika":
        st.markdown("""
        #### **A. Sifat Fisika**
        Asam karboksilat memiliki gugus fungsi karboksil ($-{COOH}$), senyawa gabungan dari gugus karbonil dan hidroksil. Derivat atau turunan asam karboksilat (seperti ester, halida asam/asil halida, anhidrida asam, dan amida) terbentuk ketika gugus $-{OH}$ pada karboksilat digantikan oleh nukleofil lain.

        Asam karboksilat rantai pendek ($C_1 - C_4$) memiliki kelarutan yang sangat baik di dalam air karena kemampuan gugus $-{COOH}$ membentuk ikatan hidrogen antarmolekul yang kuat membentuk dimer. Kelarutan senyawa akan semakin menurun seiring dengan bertambah tingginya bobot molekul (rantai alkil nonpolar semakin panjang). Titik didih asam karboksilat relatif tinggi dibandingkan senyawa organik lain dengan berat molekul setara.
        """)
        
    elif st.session_state.sub_bab_iv == "B. Reaksi Kimia Asam Karboksilat":
        st.markdown("""
        #### **B. Persamaan Reaksi Kimia Asam Karboksilat**
        
        **1. Reaksi dengan Basa Kuat (${NaOH}$):**
        * Menghasilkan garam karboksilat yang larut dalam air.
        """)
        st.latex(r"\text{R-COOH} + \text{NaOH} \rightarrow \text{R-COONa} + \text{H}_2\text{O}")
        
        st.markdown("""
        **2. Reaksi dengan Basa Lemah (${NaHCO}_3$):**
        * Asam karboksilat tergolong cukup asam untuk mendeprotonasi natrium bikarbonat, menghasilkan garam, air, dan pelepasan gas karbon dioksida secara cepat (effervescence). Reaksi ini membedakan asam karboksilat dengan fenol.
        """)
        st.latex(r"\text{R-COOH} + \text{NaHCO}_3 \rightarrow \text{R-COONa} + \text{H}_2\text{O} + \text{CO}_2\uparrow")
        
    elif st.session_state.sub_bab_iv == "C. Identifikasi Derivat (Ester)":
        st.markdown("""
        #### **C. Persamaan Reaksi Identifikasi Derivat Asam Karboksilat (Uji Asam Hidroksamat)**
        Derivat asam karboksilat (contohnya ester) terlebih dahulu dikondensasikan dengan hidroksilamin (${NH}_2{OH}$) menghasilkan senyawa asam hidroksamat. Sifat kimia khas dari asam hidroksamat adalah kemampuannya mengkelat logam besi membentuk senyawa kompleks besi(III) hidroksamat yang menghasilkan warna ungu intens saat ditambahkan larutan ${FeCl}_3$.
        """)
        st.latex(r"\text{R-COOR'} + \text{NH}_2\text{OH} \rightarrow \text{R-CONH-OH} + \text{R'-OH}")

    elif st.session_state.sub_bab_iv == "🧪 Mini-Lab: Karboksilat":
        st.markdown("#### 🧪 Laboratorium Mini: Asam Karboksilat & Ester")
        c1, c2 = st.columns(2)
        with c1:
            sampel_ak = st.selectbox("Pilih Senyawa Sampel:", ["Asam Karboksilat", "Ester (Alkil Alkanoat)"])
            uji_ak = st.selectbox("Pilih Reaksi Identifikasi Khas:", ["Uji Lakmus & Air Barit", "Uji Asam Hidroksamat (NH2OH + FeCl3)"])
            
        with c2:
            st.write("**Visualisasi Hasil Uji:**")
            if sampel_ak == "Asam Karboksilat":
                if uji_ak == "Uji Lakmus & Air Barit":
                    st.markdown(render_tube("65%", "#f8fafc", "bubbles"), unsafe_allow_html=True)
                    st.success("✅ **Hasil:** (+) Terbentuk gelembung gas $CO_2$ secara cepat yang mengeruhkan larutan indikator air barit.")
                else:
                    st.markdown(render_tube("65%", "#f8fafc", "none"), unsafe_allow_html=True)
                    st.warning("⚠️ **Hasil:** (-) Negatif. Asam karboksilat bebas tidak bereaksi membentuk kompleks warna hidroksamat.")
            else:
                if uji_ak == "Uji Lakmus & Air Barit":
                    st.markdown(render_tube("65%", "#f8fafc", "none"), unsafe_allow_html=True)
                    st.error("❌ **Hasil:** (-) Negatif. Ester tidak memiliki hidrogen asam karboksil sehingga gagal mengurai bikarbonat.")
                else:
                    st.markdown(render_tube("65%", "#c026d3", "none"), unsafe_allow_html=True)
                    st.success("✅ **Hasil:** (+) Positif Merah Violet/Ungu. Ester berhasil diubah menjadi asam hidroksamat yang mengkelat ion $Fe^{3+}$.")

# ==============================================================================
# 6. POST TEST CERDAS
# ==============================================================================
elif pilihan_halaman == "🔬 POST TEST":
    st.title("🔀 Asisten Identifikasi Cerdas (Step-by-Step)")
    st.write("Sistem ini mensimulasikan penelusuran Identifikasi Kualitatif langkah demi langkah. Tekan tombol Lanjut untuk melanjutkan ke tahap reaksi berikutnya berdasarkan spesifikasi pereaksi.")

    if not st.session_state.test_started:
        st.divider()
        senyawa = st.selectbox("Pilih Golongan Senyawa yang Akan Diuji (Sebagai *Blind Sample*):", ["-- Pilih Senyawa --"] + list(flowchart_paths.keys()))
        if st.button("Mulai Identifikasi 🚀", type="primary"):
            if senyawa == "-- Pilih Senyawa --":
                st.warning("⚠️ Harap pilih komponen senyawa terlebih dahulu!")
            else:
                st.session_state.test_started = True
                st.session_state.senyawa_uji = senyawa
                st.session_state.current_step = 0
                st.session_state.log_history = []
                st.session_state.trigger_animation = True
                force_rerun()

    else:
        st.write("---")
        senyawa = st.session_state.senyawa_uji
        urutan = flowchart_paths[senyawa]

        col_visual, col_log = st.columns([1, 2.5])
        
        with col_visual:
            st.markdown("<h4 style='text-align: center;'>Visual Lab</h4>", unsafe_allow_html=True)
            
            reagent_tag_placeholder = st.empty()
            tube_placeholder = st.empty() 
            status_placeholder = st.empty()
            
            st.write("")
            if st.button("⏹️ Stop & Pilih Reagen/Sampel Ulang", use_container_width=True, type="secondary"):
                st.session_state.test_started = False
                st.session_state.current_step = 0
                st.session_state.log_history = []
                st.session_state.trigger_animation = False
                force_rerun()
            
        with col_log:
            st.markdown("#### 📑 Logbook & Analisis Teoritis")
            log_container = st.container()

        with log_container:
            for log in st.session_state.log_history:
                if "(+)" in log["hasil"]:
                    st.success(f"**Tahap {log['step']}: {log['pereaksi']}** ➔ **{log['hasil']}**")
                    st.latex(log['reaksi'])
                    st.write(f"**Pembahasan:** {log['alasan']}")
                else:
                    st.error(f"**Tahap {log['step']}: {log['pereaksi']}** ➔ **{log['hasil']}**")
                    st.latex(log['reaksi'])
                    st.write(f"**Pembahasan:** {log['alasan']}")

        if st.session_state.trigger_animation and st.session_state.current_step < len(urutan):
            pereaksi = urutan[st.session_state.current_step]
            
            reagent_tag_placeholder.markdown(f"<div class='reagent-tag'>🧪 Pereaksi: {pereaksi}</div>", unsafe_allow_html=True)
            tube_placeholder.markdown(render_tube("30%", "#f1f5f9", "none"), unsafe_allow_html=True)
            status_placeholder.markdown(f"<div style='text-align:center;'><em>Menyiapkan sampel untuk analisis...</em></div>", unsafe_allow_html=True)
            time.sleep(1.0)
            
            warna_reagen = reagen_colors[pereaksi]
            tube_placeholder.markdown(render_tube("65%", warna_reagen, "none"), unsafe_allow_html=True)
            status_placeholder.markdown(f"<div style='text-align:center;'><em>Mereaksikan komponen senyawa...</em></div>", unsafe_allow_html=True)
            time.sleep(1.5)
            
            res = database_reaksi[senyawa][pereaksi]
            w_endapan = res.get("warna_endapan", None)
            tube_placeholder.markdown(render_tube("65%", res["warna_akhir"], res["efek"], warna_endapan=w_endapan), unsafe_allow_html=True)
            status_placeholder.markdown("<div style='text-align:center; font-weight:bold;'>Mengamati pengendapan & perubahan warna...</div>", unsafe_allow_html=True)
            time.sleep(1.2)
            
            st.session_state.log_history.append({
                "step": st.session_state.current_step + 1,
                "pereaksi": pereaksi,
                "hasil": res["hasil"],
                "reaksi": res["reaksi"],
                "alasan": res["alasan"]
            })
            
            st.session_state.current_step += 1
            st.session_state.trigger_animation = False
            force_rerun()

        elif not st.session_state.trigger_animation:
            if st.session_state.current_step > 0:
                last_pereaksi = urutan[st.session_state.current_step - 1]
                reagent_tag_placeholder.markdown(f"<div class='reagent-tag'>🧪 Pereaksi: {last_pereaksi}</div>", unsafe_allow_html=True)
                res = database_reaksi[senyawa][last_pereaksi]
                w_endapan = res.get("warna_endapan", None)
                tube_placeholder.markdown(render_tube("65%", res["warna_akhir"], res["efek"], warna_endapan=w_endapan), unsafe_allow_html=True)
            
            if st.session_state.current_step < len(urutan):
                next_pereaksi = urutan[st.session_state.current_step]
                status_placeholder.markdown("<div style='text-align:center; color:#475569;'>Menunggu konfirmasi data...</div>", unsafe_allow_html=True)
                
                with col_visual:
                    if st.button(f"Lanjutkan ke {next_pereaksi} ⏭️", use_container_width=True, type="primary"):
                        st.session_state.trigger_animation = True
                        force_rerun()
                        
            else:
                reagent_tag_placeholder.markdown("<div class='reagent-tag' style='background-color:#d1fae5; color:#065f46;'>🏁 Identifikasi Selesai</div>", unsafe_allow_html=True)
                status_placeholder.markdown("<div style='text-align:center; font-weight:bold; color:#10b981;'>Rangkaian uji selesai!</div>", unsafe_allow_html=True)
                with log_container:
                    st.info(f"🎉 **KESIMPULAN AKHIR:** Sampel ini terbukti sah merupakan senyawa **{senyawa.upper()}**.")
                
                with col_visual:
                    if st.button("🔄 Uji Golongan Senyawa Lain", use_container_width=True):
                        st.session_state.test_started = False
                        force_rerun()
