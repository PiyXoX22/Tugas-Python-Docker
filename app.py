import streamlit as st
import math
import periodictable as pt
#title senyawa kimias
st.title("🧪 Smart Chemical Builder (PRO)")
st.write("✔ Auto valensi • ✔ Nama senyawa • ✔ Prediksi reaksi dasar")

# =========================
# VALENSI
# =========================
valensi_default = {
    1: 1, 2: 2, 13: 3,
    15: -3, 16: -2, 17: -1
}

valensi_khusus = {
    "Fe": 3, "Cu": 2, "Zn": 2,
    "Ag": 1, "Au": 3,
    "Pb": 2, "Sn": 2,
    "U": 6
}

def get_valensi(symbol):
    try:
        el = getattr(pt, symbol)

        if symbol in valensi_khusus:
            return valensi_khusus[symbol]

        group = getattr(el, "group", None)

        if group in valensi_default:
            return valensi_default[group]

        return None
    except:
        return None


# =========================
# JENIS UNSUR
# =========================
def jenis_unsur(symbol):
    try:
        el = getattr(pt, symbol)
        if el.number <= 20:
            if symbol in ["H","C","N","O","F","Cl","Br","I"]:
                return "nonlogam"
            else:
                return "logam"
        return "logam"
    except:
        return "unknown"


# =========================
# CRISS CROSS
# =========================
def criss_cross(kation, v1, anion, v2):
    a = abs(v2)
    b = abs(v1)

    gcd = math.gcd(a, b)
    a //= gcd
    b //= gcd

    hasil = kation if a == 1 else f"{kation}{a}"

    if b == 1:
        hasil += anion
    else:
        hasil += f"{anion}{b}"

    return hasil


# =========================
# NAMA SENYAWA (INDONESIA)
# =========================
nama_unsur = {
    "Na": "natrium", "Cl": "klorida",
    "K": "kalium", "O": "oksida",
    "Ca": "kalsium", "S": "sulfida",
    "Fe": "besi", "Cu": "tembaga"
}

def angka_romawi(n):
    roman = {1:"I",2:"II",3:"III",4:"IV",5:"V",6:"VI"}
    return roman.get(n, str(n))

def nama_senyawa(kation, anion, valensi):
    nama_kat = nama_unsur.get(kation, kation.lower())
    nama_an = nama_unsur.get(anion, anion.lower())

    # untuk logam multivalensi
    if kation in valensi_khusus:
        return f"{nama_kat}({angka_romawi(valensi)}) {nama_an}"
    else:
        return f"{nama_kat} {nama_an}"


# =========================
# PREDIKSI REAKSI
# =========================
def prediksi_reaksi(u1, u2, hasil):
    jenis1 = jenis_unsur(u1)
    jenis2 = jenis_unsur(u2)

    if jenis1 == "logam" and jenis2 == "nonlogam":
        return f"Reaksi sintesis: {u1} + {u2} → {hasil}"

    elif jenis1 == "nonlogam" and jenis2 == "nonlogam":
        return "Reaksi kovalen (berbagi elektron)"

    elif jenis1 == "logam" and jenis2 == "logam":
        return "Tidak membentuk senyawa ion (alloy/logam campuran)"

    else:
        return "Reaksi tidak diketahui"


# =========================
# VALIDASI
# =========================
def valid_unsur(symbol):
    try:
        getattr(pt, symbol)
        return True
    except:
        return False


# =========================
# UI
# =========================
u1 = st.text_input("Unsur 1").capitalize()
u2 = st.text_input("Unsur 2").capitalize()

if st.button("Bentuk Senyawa"):

    if not valid_unsur(u1) or not valid_unsur(u2):
        st.error("❌ Unsur tidak valid")
    else:
        v1 = get_valensi(u1)
        v2 = get_valensi(u2)

        if v1 is None or v2 is None:
            st.warning("⚠️ Valensi tidak pasti, pakai default")
            v1 = v1 if v1 else 1
            v2 = v2 if v2 else -1

        # tentukan kation
        if v1 > 0:
            hasil = criss_cross(u1, v1, u2, v2)
            nama = nama_senyawa(u1, u2, v1)
        else:
            hasil = criss_cross(u2, v2, u1, v1)
            nama = nama_senyawa(u2, u1, v2)

        reaksi = prediksi_reaksi(u1, u2, hasil)

        st.success(f"✅ {u1} + {u2} → {hasil}")
        st.info(f"📚 Nama: {nama}")
        st.write(f"Valensi: {u1}({v1}), {u2}({v2})")
        st.write(f"🧪 {reaksi}")