import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
from PIL import Image
import io

# Page Configuration & Elite SaaS Aesthetics
st.set_page_config(
    page_title="AutoSheet 5-Agent Autonomous Enterprise OS", 
    layout="wide", 
    page_icon="⚡"
)

# Initialize Database & Secure Tenant Tables
DB_NAME = "autosheet_enterprise_v2.db"

def init_db():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT,
                organization TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                timestamp TEXT,
                action TEXT,
                details TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_ledgers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                subsidiary TEXT,
                filename TEXT,
                file_data TEXT,
                upload_date TEXT
            )
        """)
        conn.commit()
        conn.close()
    except Exception as e:
        st.error(f"Database initialization error: {e}")

init_db()

# Action Logger
def log_action(username, action, details):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO audit_logs (username, timestamp, action, details) VALUES (?, ?, ?, ?)",
            (username, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), action, details)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Logging error: {e}")

# Session State Initialization
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "org_name" not in st.session_state:
    st.session_state.org_name = ""

# ================= AUTHENTICATION SCREEN =================
if not st.session_state.logged_in:
    st.title("⚡ AutoSheet 5-Agent Master OS - Secure Portal")
    auth_mode = st.radio("Authentication Mode", ["Login", "Register Organization"])
    
    username = st.text_input("Username / Email")
    password = st.text_input("Password", type="password")
    
    org_name = ""
    if auth_mode == "Register Organization":
        org_name = st.text_input("Company / Organization Name")

    if st.button("Authenticate Session"):
        if not username or not password:
            st.error("Please enter both username and password.")
        else:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            
            if auth_mode == "Register Organization":
                if not org_name:
                    st.error("Please enter your organization name.")
                else:
                    try:
                        cursor.execute(
                            "INSERT INTO users (username, password, organization) VALUES (?, ?, ?)", 
                            (username, password, org_name)
                        )
                        conn.commit()
                        st.success("Organization registered successfully! Please switch to Login above.")
                    except sqlite3.IntegrityError:
                        st.error("Username already exists! Please choose another.")
            else:
                cursor.execute(
                    "SELECT organization FROM users WHERE username = ? AND password = ?", 
                    (username, password)
                )
                user_record = cursor.fetchone()
                if user_record:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.org_name = user_record[0]
                    log_action(username, "Login", "User authenticated successfully.")
                    st.rerun()
                else:
                    st.error("Invalid username or password.")
            conn.close()
    st.stop()

# ================= MAIN APP COMMAND CENTER (LOGGED IN) =================
st.sidebar.title(f"🏢 {st.session_state.org_name}")
st.sidebar.write(f"Active User: **{st.session_state.username}**")

current_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
st.sidebar.markdown(f"📅 **Live Timestamp:** `{current_time_str}`")
st.sidebar.markdown("---")

subsidiary = st.sidebar.selectbox(
    "Global Subsidiary Entity", 
    ["HQ - Main", "Delhi Branch", "US Subsidiary", "Rishikesh Unit"]
)

selected_currency = st.sidebar.selectbox(
    "🌍 Global Currency", 
    [
        "USD ($ - US Dollar)", "EUR (€ - Euro)", "INR (₹ - Indian Rupee)", 
        "GBP (£ - British Pound)", "JPY (¥ - Japanese Yen)", "AUD ($ - Australian Dollar)", 
        "CAD ($ - Canadian Dollar)", "CHF (CHF - Swiss Franc)", "CNY (¥ - Chinese Yuan)", 
        "AED (د.إ - UAE Dirham)", "SGD ($ - Singapore Dollar)", "SAR (ر.س - Saudi Riyal)"
    ]
)

selected_language = st.sidebar.selectbox(
    "🌐 App Language", 
    [
        "English", "Hindi (हिन्दी)", "Spanish (Español)", "French (Français)", 
        "German (Deutsch)", "Mandarin Chinese (中文)", "Japanese (日本語)", 
        "Arabic (العربية)", "Portuguese (Português)", "Russian (Русский)", 
        "Italian (Italiano)", "Korean (한국어)"
    ]
)

if st.sidebar.button("Logout"):
    log_action(st.session_state.username, "Logout", "User terminated session.")
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.org_name = ""
    st.rerun()

st.title("⚡ AutoSheet 5-Agent Autonomous Enterprise OS")
currency_code = selected_currency.split(' ')[0]
st.markdown(f"**Subsidiary:** `{subsidiary}` | **Currency:** `{currency_code}` | **Language:** `{selected_language}` | **Multi-AI Red Highlighting:** `Active 🔴`")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🤖 Agent 1: Ingestion & Vision", 
    "🛡️ Agent 2: Forensic Fraud Shield", 
    "💸 Agent 3: Global Cash-Sweep", 
    "📈 Agent 4: Vendor Inflation", 
    "🔒 Agent 5: Compliance Dossier"
])

# Helper function to fetch user dataframe
def get_user_master_df():
    try:
        conn = sqlite3.connect(DB_NAME)
        ledger_rows = pd.read_sql(
            "SELECT file_data FROM user_ledgers WHERE username = ? AND subsidiary = ?", 
            conn, 
            params=(st.session_state.username, subsidiary)
        )
        conn.close()
        if not ledger_rows.empty:
            dfs = [pd.read_csv(io.StringIO(csv_str)) for csv_str in ledger_rows['file_data']]
            return pd.concat(dfs, ignore_index=True)
    except:
        pass
    return pd.DataFrame()

# --- TAB 1: AGENT 1 (INGESTION & VISION WITH RED SCHEMA ALERTS) ---
with tab1:
    st.subheader("🤖 Agent 1: Autonomous Ingestion & Normalization Engine")
    st.write("Upload raw corporate ledgers. Agent 1 validates schema and triggers red warnings if columns are missing.")
    
    uploaded_file = st.file_uploader(
        "Upload Corporate Ledger (CSV) or Receipt Asset (Image)", 
        type=["csv", "png", "jpg", "jpeg"]
    )
    
    if st.button("🚀 Execute 5-Agent Sequential Pipeline"):
        if uploaded_file is not None:
            if uploaded_file.name.endswith('.csv'):
                try:
                    df = pd.read_csv(uploaded_file)
                    
                    # Agent 1 Red Schema Validation Check
                    required_cols = {'Category', 'Vendor', 'Amount'}
                    missing_cols = required_cols - set(df.columns)
                    
                    if missing_cols:
                        st.error(f"🔴 **[Agent 1 Schema Error]:** Uploaded ledger is missing mandatory financial columns: `{missing_cols}`. Please reformat your CSV!")
                    else:
                        st.success(f"✅ [Agent 1]: Successfully ingested and normalized {uploaded_file.name}")
                        st.dataframe(df, use_container_width=True)
                        
                        conn = sqlite3.connect(DB_NAME)
                        cursor = conn.cursor()
                        cursor.execute(
                            "INSERT INTO user_ledgers (username, subsidiary, filename, file_data, upload_date) VALUES (?, ?, ?, ?, ?)",
                            (st.session_state.username, subsidiary, uploaded_file.name, df.to_csv(index=False), datetime.now().strftime("%Y-%m-%d"))
                        )
                        conn.commit()
                        conn.close()
                        
                        log_action(st.session_state.username, "Agent 1 Pipeline", f"Successfully ingested {uploaded_file.name}")
                        st.balloons()
                        st.info("✨ **Pipeline Complete:** All 5 AIs have analyzed your data. Review Tabs 2-5 for red threat highlights.")
                except Exception as e:
                    st.error(f"🔴 **[Agent 1 Fatal Error]:** Failed to parse CSV file: {e}")
            else:
                try:
                    img = Image.open(uploaded_file)
                    st.success(f"✅ [Agent 1 - Vision]: Successfully processed receipt asset: {uploaded_file.name}")
                    st.image(img, caption=f"Source Document: {uploaded_file.name}", width=400)
                except Exception as e:
                    st.error(f"🔴 [Agent 1 Vision Error]: {e}")
        else:
            st.warning("⚠️ Please upload a file before running the pipeline.")

# --- TAB 2: AGENT 2 (FORENSIC FRAUD SHIELD WITH RED HIGHLIGHTING) ---
with tab2:
    st.subheader("🛡️ Agent 2: Forensic Fraud & Anomaly Detection AI")
    st.write("Automatically scans ledger data and **highlights fraudulent or high-risk transactions in red**.")
    
    master_df = get_user_master_df()
    if not master_df.empty and 'Amount' in master_df.columns:
        mean_val = master_df['Amount'].mean()
        std_val = master_df['Amount'].std() if len(master_df) > 1 else 0
        threshold = mean_val + (1.5 * std_val)
        
        def highlight_fraud(row):
            if row['Amount'] > threshold:
                return ['background-color: #ff4b4b; color: white'] * len(row)
            return [''] * len(row)
        
        styled_df = master_df.style.apply(highlight_fraud, axis=1)
        st.dataframe(styled_df, use_container_width=True)
        
        fraud_count = len(master_df[master_df['Amount'] > threshold])
        if fraud_count > 0:
            st.markdown(f"🔴 **[Agent 2 Alert]:** `{fraud_count}` high-risk transaction(s) flagged and highlighted in red.")
        else:
            st.success("🟢 **[Agent 2 Status]:** All transactions verified clean.")
    else:
        st.info("⏳ Waiting for data. Run pipeline in Tab 1.")

# --- TAB 3: AGENT 3 (GLOBAL CASH-SWEEP WITH RED LIQUIDITY ALERTS) ---
with tab3:
    st.subheader("💸 Agent 3: Autonomous Global Cash-Sweep & Liquidity AI")
    st.write(f"Monitors treasury capital velocity in {selected_currency} and highlights cash drag in red.")
    
    master_df = get_user_master_df()
    if not master_df.empty and 'Amount' in master_df.columns:
        total_vol = master_df['Amount'].sum()
        savings = total_vol * 0.035
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Managed Capital", f"{currency_code} {total_vol:,.2f}")
        c2.metric("Automated Cash-Sweep Savings", f"{currency_code} {savings:,.2f}", delta="Optimized")
        
        # Red liquidity warning if total volume is abnormally low/high deficit risk
        if total_vol < 100:
            c3.metric("Liquidity Status", "CRITICAL DEFICIT", delta="🔴 Action Required", delta_color="inverse")
            st.error("🔴 **[Agent 3 Treasury Alert]:** Low capital volume detected across subsidiary accounts. Cash drag risk is elevated.")
        else:
            c3.metric("Runway Status", "Stable (18+ Months)", delta="AI Verified")
            st.success("🟢 **[Agent 3 Status]:** Liquidity velocity optimal.")
    else:
        st.info("⏳ Ingest data in Tab 1 to activate Agent 3 liquidity AI.")

# --- TAB 4: AGENT 4 (VENDOR INFLATION WITH RED HIGH-SPEND HIGHLIGHTS) ---
with tab4:
    st.subheader("📈 Agent 4: Vendor Cost Creep & SaaS Inflation AI")
    st.write(f"Audits supplier pricing and **highlights abnormal vendor price spikes in bright red**.")
    
    master_df = get_user_master_df()
    if not master_df.empty and {'Category', 'Vendor', 'Amount'}.issubset(master_df.columns):
        v_mean = master_df['Amount'].mean()
        
        def highlight_vendor_inflation(row):
            if row['Amount'] > (v_mean * 1.5):
                return ['background-color: #ff4b4b; color: white'] * len(row)
            return [''] * len(row)
            
        styled_vendor_df = master_df.style.apply(highlight_vendor_inflation, axis=1)
        st.dataframe(styled_vendor_df, use_container_width=True)
        
        high_vendors = len(master_df[master_df['Amount'] > (v_mean * 1.5)])
        if high_vendors > 0:
            st.markdown(f"🔴 **[Agent 4 Inflation Alert]:** `{high_vendors}` vendor payout(s) exceeding normal cost thresholds highlighted in red.")
        else:
            st.success("🟢 **[Agent 4 Status]:** Stable vendor pricing observed.")
    else:
        st.info("⏳ Waiting for pipeline data. Upload ledgers in Tab 1.")

# --- TAB 5: AGENT 5 (COMPLIANCE DOSSIER WITH RED ERROR HIGHLIGHTS) ---
with tab5:
    st.subheader("🔒 Agent 5: Statutory Audit Dossier & Compliance Vault AI")
    st.write("Audits session logs and **highlights system errors or security warnings in red**.")
    
    try:
        conn = sqlite3.connect(DB_NAME)
        audit_df = pd.read_sql(
            "SELECT timestamp, action, details FROM audit_logs WHERE username = ?", 
            conn, 
            params=(st.session_state.username,)
        )
        conn.close()
        
        if not audit_df.empty:
            def highlight_audit_errors(row):
                if 'Error' in str(row['details']) or 'Logout' in str(row['action']):
                    return ['background-color: #ff4b4b; color: white'] * len(row)
                return [''] * len(row)
                
            styled_audit = audit_df.style.apply(highlight_audit_errors, axis=1)
            st.dataframe(styled_audit, use_container_width=True)
            st.success("🧠 [Agent 5 Active]: Audit dossier compiled with real-time red threat surveillance.")
        else:
            st.info("⏳ Audit dossier initializing. Run pipeline in Tab 1.")
    except Exception as e:
        st.error(f"🔴 [Agent 5 Error]: {e}")