import streamlit as st
import pandas as pd
from datetime import datetime, date

st.set_page_config(page_title="Sistem Manajemen Distribusi Linen RS", page_icon="🏥", layout="wide")

if "orders" not in st.session_state:
    st.session_state["orders"] = [
        {
            "id": "ORD-001",
            "date": str(date.today()),
            "unit": "ICU",
            "unit_code": "123",
            "linen_type": "Bed Sheet",
            "qty": 50,
            "status_step": 6,
            "admin_name": "Budi (Admin Utama)",
            "unit_nurse": "Siti Nurhaliza",
            "runner_name": "Ahmad (Runner)",
            "checker_name": "Dewi (Checker)",
            "delivery_schedule": "14:30 WIB",
            "receiver_nurse": "Siti Nurhaliza",
        },
        {
            "id": "ORD-002",
            "date": str(date.today()),
            "unit": "IGD",
            "unit_code": "124",
            "linen_type": "Selimut Pasien",
            "qty": 30,
            "status_step": 6,
            "admin_name": "Budi (Admin Utama)",
            "unit_nurse": "Joko Susilo",
            "runner_name": "Ahmad (Runner)",
            "checker_name": "Dewi (Checker)",
            "delivery_schedule": "15:00 WIB",
            "receiver_nurse": "Joko Susilo",
        }
    ]

if "units" not in st.session_state:
    st.session_state["units"] = {
        "123": {"name": "ICU", "nurse": "Siti Nurhaliza"},
        "124": {"name": "IGD", "nurse": "Joko Susilo"},
        "125": {"name": "Melati", "nurse": "Siti Rahma"}
    }

st.sidebar.title("🏥 Login Sistem Linen RS")
role = st.sidebar.selectbox("Pilih Peran", ["Pilih Peran...", "Unit Rumah Sakit", "Runner / Kurir", "Checker", "Admin Pusat"])

user_logged_in = False
current_role_data = {}

if role == "Unit Rumah Sakit":
    code_input = st.sidebar.text_input("Kode Unit (Contoh: 123)", type="password")
    if code_input in st.session_state["units"]:
        u = st.session_state["units"][code_input]
        st.sidebar.success(f"Login Sukses: Unit {u['name']}")
        user_logged_in = True
        current_role_data = {"type": "unit", "code": code_input, "name": u["name"], "nurse": u["nurse"]}
    elif code_input != "":
        st.sidebar.error("Kode Salah!")

elif role == "Runner / Kurir":
    r_name = st.sidebar.text_input("Nama Runner", value="Ahmad")
    if r_name:
        user_logged_in = True
        current_role_data = {"type": "runner", "name": r_name}

elif role == "Checker":
    c_name = st.sidebar.text_input("Nama Checker", value="Dewi")
    if c_name:
        user_logged_in = True
        current_role_data = {"type": "checker", "name": c_name}

elif role == "Admin Pusat":
    a_name = st.sidebar.text_input("Nama Admin", value="Budi")
    if a_name:
        user_logged_in = True
        current_role_data = {"type": "admin", "name": a_name}

st.title("Sistem Pelacakan & Distribusi Linen Rumah Sakit")

def render_timeline_and_receipt(o):
    st.markdown("### 📋 Struk / Status Pelacakan Pengiriman")
    steps = [
        "1. Linen diambil dari unit",
        "2. Linen di cek oleh checker",
        "3. Pesanan disiapkan",
        f"4. Dijadwalkan untuk pengiriman jam {o['delivery_schedule']}",
        f"5. Pesanan dikirimkan oleh {o['runner_name']}",
        f"6. Pesanan diterima oleh perawat {o['receiver_nurse'] if o['receiver_nurse'] else '...(Menunggu)...'}"
    ]
    for idx, s in enumerate(steps, 1):
        if o['status_step'] >= idx:
            st.markdown(f"✅ **{s}**")
        else:
            st.markdown(f"⏳ *{s} (Menunggu)*")
            
    st.markdown("---")
    st.markdown("### 🏷️ Informasi Petugas & Metadata Struk")
    c1, c2 = st.columns(2)
    with c1:
        st.write(f"- **ID Pesanan:** `{o['id']}`")
        st.write(f"- **Tanggal:** `{o['date']}`")
        st.write(f"- **Unit Rumah Sakit:** `{o['unit']}`")
        st.write(f"- **Jenis Linen:** `{o['linen_type']} ({o['qty']} pcs)`")
        st.write(f"- **Nama Admin:** `{o['admin_name']}`")
    with c2:
        st.write(f"- **Nama Perawat Unit:** `{o['unit_nurse']}`")
        st.write(f"- **Nama Runner:** `{o['runner_name']}`")
        st.write(f"- **Nama Checker:** `{o['checker_name']}`")
        st.write(f"- **Perawat Penerima:** `{o['receiver_nurse'] if o['receiver_nurse'] else '-'}`")

if not user_logged_in:
    st.info("👈 Silakan login di sidebar sebelah kiri.")
    st.markdown("### Fitur Aplikasi:")
    st.markdown("1. **Login per Unit** (misal ICU kode `123`, IGD kode `124`)")
    st.markdown("2. **Login Admin, Runner, Checker**")
    st.markdown("3. **Pelacakan 6 Langkah** dari pengambilan sampai diterima.")
    st.markdown("4. **Akumulasi Rekap Data Bulanan (Ekspor ke Excel)** per unit dari tanggal 1 sampai 31.")
else:
    st.write(f"Peran Aktif: **{role}**")
    st.markdown("---")

    if current_role_data["type"] == "unit":
        st.subheader(f"Dashboard Unit: {current_role_data['name']}")
        with st.form("req_form"):
            l_type = st.selectbox("Jenis Linen", ["Bed Sheet", "Selimut Pasien", "Sarung Bantal", "Handuk", "Linen OK"])
            qty = st.number_input("Jumlah (pcs)", 1, 500, 25)
            if st.form_submit_button("Ajukan Permintaan"):
                new_id = f"ORD-{len(st.session_state['orders'])+1:03d}"
                st.session_state['orders'].append({
                    "id": new_id,
                    "date": str(date.today()),
                    "unit": current_role_data["name"],
                    "unit_code": current_role_data["code"],
                    "linen_type": l_type,
                    "qty": qty,
                    "status_step": 1,
                    "admin_name": "Belum Ditugaskan",
                    "unit_nurse": current_role_data["nurse"],
                    "runner_name": "Belum Ditugaskan",
                    "checker_name": "Belum Ditugaskan",
                    "delivery_schedule": "Belum Dijadwalkan",
                    "receiver_nurse": "",
                })
                st.success(f"Permintaan {new_id} berhasil dibuat!")

        st.markdown("---")
        st.subheader("📊 Akumulasi Rekap Data Bulanan Unit Anda (Tgl 1 s.d. 31)")
        
        # Filter orders for current unit
        unit_orders = [o for o in st.session_state['orders'] if o['unit_code'] == current_role_data['code']]
        if unit_orders:
            df_unit = pd.DataFrame(unit_orders)[['id', 'date', 'linen_type', 'qty', 'status_step', 'admin_name', 'runner_name', 'checker_name']]
            st.dataframe(df_unit, use_container_width=True)
            
            # Total accumulation summary
            total_qty = sum([o['qty'] for o in unit_orders])
            st.info(f"📈 **Total Keseluruhan Permintaan Linen Unit {current_role_data['name']} Bulan Ini:** `{total_qty} pcs`")
            
            # CSV Download button for Excel compatibility
            csv_data = df_unit.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Rekap Bulanan (Format Excel / CSV)",
                data=csv_data,
                file_name=f"rekap_linen_{current_role_data['name']}.csv",
                mime="text/csv"
            )
        else:
            st.info("Belum ada data rekap untuk unit ini.")

        st.markdown("---")
        st.subheader("Riwayat & Pelacakan Pesanan Aktif")
        for o in unit_orders:
            with st.expander(f"📦 {o['id']} - {o['linen_type']} ({o['qty']} pcs) - Status Step: {o['status_step']}/6"):
                render_timeline_and_receipt(o)
                if o['status_step'] == 5:
                    if st.button(f"Konfirmasi Diterima ({o['id']})", key=f"rcv_{o['id']}"):
                        o['status_step'] = 6
                        o['receiver_nurse'] = current_role_data['nurse']
                        st.success("Terkonfirmasi diterima!")
                        st.rerun()

    elif current_role_data["type"] == "runner":
        st.subheader(f"Dashboard Runner: {current_role_data['name']}")
        for o in st.session_state['orders']:
            with st.expander(f"🚚 {o['id']} - Unit: {o['unit']} (Step {o['status_step']}/6)"):
                render_timeline_and_receipt(o)
                col1, col2 = st.columns(2)
                with col1:
                    if o['status_step'] == 1:
                        if st.button(f"Tandai Diambil oleh {current_role_data['name']}", key=f"r1_{o['id']}"):
                            o['runner_name'] = current_role_data['name']
                            o['status_step'] = 2
                            st.success("Diperbarui!")
                            st.rerun()
                with col2:
                    if o['status_step'] == 4:
                        if st.button(f"Kirimkan Pesanan ({o['id']})", key=f"r5_{o['id']}"):
                            o['runner_name'] = current_role_data['name']
                            o['status_step'] = 5
                            st.success("Pesanan dikirim!")
                            st.rerun()

    elif current_role_data["type"] == "checker":
        st.subheader(f"Dashboard Checker: {current_role_data['name']}")
        for o in st.session_state['orders']:
            with st.expander(f"🔍 {o['id']} - Unit: {o['unit']} (Step {o['status_step']}/6)"):
                render_timeline_and_receipt(o)
                if o['status_step'] in [1, 2]:
                    if st.button(f"Verifikasi & Cek Fisik Linen ({o['id']})", key=f"c_{o['id']}"):
                        o['checker_name'] = current_role_data['name']
                        o['status_step'] = 2
                        st.success("Linen telah dicek!")
                        st.rerun()

    elif current_role_data["type"] == "admin":
        st.subheader(f"Dashboard Admin: {current_role_data['name']}")
        
        st.markdown("### 📈 Akumulasi Seluruh Unit (Laporan Bulanan Global)")
        if st.session_state['orders']:
            df_all = pd.DataFrame(st.session_state['orders'])[['id', 'date', 'unit', 'linen_type', 'qty', 'status_step', 'admin_name', 'runner_name', 'checker_name']]
            st.dataframe(df_all, use_container_width=True)
            
            csv_all = df_all.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Seluruh Rekap Rumah Sakit (Format Excel / CSV)",
                data=csv_all,
                file_name="rekap_seluruh_unit_linen.csv",
                mime="text/csv"
            )
        
        st.markdown("---")
        st.markdown("### Kelola Status & Penugasan Pesanan")
        for o in st.session_state['orders']:
            with st.expander(f"⚙️ {o['id']} - Unit: {o['unit']} (Step {o['status_step']}/6)"):
                render_timeline_and_receipt(o)
                with st.form(f"adm_{o['id']}"):
                    ad_n = st.text_input("Nama Admin", value=current_role_data['name'])
                    rn_n = st.text_input("Nama Runner", value=o['runner_name'])
                    ch_n = st.text_input("Nama Checker", value=o['checker_name'])
                    sch = st.text_input("Jadwal Pengiriman Jam", value=o['delivery_schedule'])
                    if st.form_submit_button("Simpan & Setujui / Siapkan Pesanan"):
                        o['admin_name'] = ad_n
                        o['runner_name'] = rn_n
                        o['checker_name'] = ch_n
                        o['delivery_schedule'] = sch
                        o['status_step'] = 4
                        st.success("Pesanan disiapkan & dijadwalkan!")
                        st.rerun()
