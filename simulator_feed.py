import os
import django
import pandas as pd
import time
import sys

# 1. Setup Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartgrid.settings')
django.setup()

from monitoring.models import GridData
from django.utils import timezone

def run_simulation():
    print("🚀 Starting Real-Time HMM Data Replay...")
    print("Press Ctrl+C to stop.")

    # 2. Read the CSV
    try:
        # Read the file you uploaded
        df = pd.read_csv('fusion_hmm_output.csv')
    except FileNotFoundError:
        print("❌ Error: 'fusion_hmm_output.csv' not found. Please put it in this folder.")
        return

    # 3. Loop through rows to simulate real-time feed
    for index, row in df.iterrows():
        try:
            # We map the CSV columns to our Django Model fields:
            # - 'chi2_n' (Physical Deviation) -> mapped to 'voltage' for the graph
            # - 'cyber_score' (Cyber Deviation) -> mapped to 'current' for the graph
            
            # Using get() with default 0 to avoid crashes if columns are missing
            physical_val = float(row.get('chi2_n', 0))
            cyber_val = float(row.get('cyber_score', 0))
            
            # Check if attack is detected (1 = Attack, 0 = Normal)
            is_attack = int(row.get('hmm_detect', 0)) == 1
            
            # Determine Attack Name
            attack_name = "HMM Detected Attack" if is_attack else None

            # Create the record in the database
            GridData.objects.create(
                timestamp=timezone.now(),
                voltage=physical_val,   # Storing Physical Score here
                current=cyber_val,      # Storing Cyber Score here
                anomaly=is_attack,
                attack_type=attack_name
            )

            status = "⚠️ ATTACK" if is_attack else "✅ Normal"
            print(f"[{index}] Time: {timezone.now().strftime('%H:%M:%S')} | Phys: {physical_val:.4f} | Cyber: {cyber_val:.4f} | {status}")

            # Wait 2 seconds before next reading to simulate real-time
            time.sleep(2)

        except KeyboardInterrupt:
            print("\n🛑 Simulation stopped.")
            sys.exit()
        except Exception as e:
            print(f"Error on row {index}: {e}")

if __name__ == '__main__':
    # Optional: Clear old data before starting?
    # GridData.objects.all().delete() 
    run_simulation()
