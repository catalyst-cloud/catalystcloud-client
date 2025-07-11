# ========================================
# === BIOMONITOR + CCLOUD-CLIENT SETUP ===
# ========================================

# Set environment variables
$envName = "biomonitor"
$musicFolder = "E:\Music\SoundCloud\ChrisRussell"
$pyScriptPath = "$env:USERPROFILE\Documents\biosim_monitor.py"   # Safe write path
$repoUrl = "https://github.com/catalyst-cloud/ccloud-client.git"
$repoDir = "$PSScriptRoot\ccloud-client"

# Step 1: Check or Create Conda Environment
Write-Host "🔍 Checking for conda environment: $envName..."
$existingEnvs = conda env list | Out-String
if ($existingEnvs -notmatch $envName) {
    Write-Host "🛠 Creating conda environment: $envName"
    conda create -n $envName python=3.10 -y
} else {
    Write-Host "✅ Conda environment $envName exists."
}

# Step 2: Install required Python packages
Write-Host "📦 Installing Python packages..."
cmd /c "conda activate $envName && pip install pygame matplotlib numpy scipy"

# Step 3: Clone or Pull ccloud-client repo
if (-Not (Test-Path $repoDir)) {
    Write-Host "🌱 Cloning Catalyst Cloud client repo..."
    git clone $repoUrl $repoDir
} else {
    Write-Host "🔄 Updating Catalyst Cloud client repo..."
    Push-Location $repoDir
    git pull
    Pop-Location
}

# Step 4: Write Python Biosim Monitor Script with ICP spectrogram based on music frequencies
$pythonScript = @"
import os
import sys
import time
import threading
import subprocess
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pygame
from scipy.signal import spectrogram, butter, lfilter

# === Import Catalyst Cloud Client ===
REPO_DIR = os.path.join(os.path.dirname(__file__), 'ccloud-client')
sys.path.insert(0, REPO_DIR)

def update_ccloud_repo():
    try:
        print('🔄 Pulling latest ccloud-client...')
        subprocess.run(['git', 'pull'], cwd=REPO_DIR, check=True)
    except Exception as e:
        print('⚠️ Git pull failed:', e)

update_ccloud_repo()

MUSIC_DIR = r'$musicFolder'

def get_tracks(directory):
    return [f for f in os.listdir(directory) if f.lower().endswith(('.mp3', '.wav'))]

def generate_ecg():
    t = np.linspace(0, 1, 500)
    base = 1.2 * np.sin(2 * np.pi * 3 * t) * np.exp(-4 * t)
    spike = np.where((0.3 < t) & (t < 0.32), 2.5, 0)
    return base + spike

def simulate_icp():
    # Simulated ICP baseline + noise + cardiac pulse, for overlay waveform only
    return max(5, min(25, 10 + np.random.normal(0, 2) + 2.5 * np.sin(time.time() * 2)))

def butter_lowpass(cutoff, fs, order=6):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def lowpass_filter(data, cutoff=1000, fs=44100, order=6):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

class BioMonitor:
    def __init__(self):
        plt.style.use('dark_background')
        self.fig, self.axs = plt.subplots(3, 1, figsize=(12, 10), gridspec_kw={'height_ratios': [1, 1, 1]})
        self.ax_ecg = self.axs[0]
        self.ax_icp_wave = self.axs[1]
        self.ax_spec = self.axs[2]

        # ECG plot
        self.ax_ecg.set_title("❤️ ECG Waveform", color='white')
        self.ax_ecg.set_ylim(-1, 3)
        self.ax_ecg.set_xlim(0, 2)
        self.line_ecg, = self.ax_ecg.plot([], [], color='lime', lw=2, label='ECG')
        self.ax_ecg.legend(loc='upper right')

        # ICP waveform (simulated overlay, for comparison)
        self.ax_icp_wave.set_title("🧠 ICP Pressure Waveform (Simulated)", color='deepskyblue')
        self.ax_icp_wave.set_ylim(0, 30)
        self.ax_icp_wave.set_xlim(0, 2)
        self.line_icp, = self.ax_icp_wave.plot([], [], color='deepskyblue', lw=2, label='ICP')
        self.ax_icp_wave.legend(loc='upper right')

        # Spectrogram of audio from music playback
        self.ax_spec.set_title("🎵 ICP Spectrogram from Music Audio Frequencies", color='magenta')
        self.ax_spec.set_ylabel('Frequency [Hz]', color='white')
        self.ax_spec.set_xlabel('Time [s]', color='white')
        self.ax_spec.tick_params(axis='x', colors='white')
        self.ax_spec.tick_params(axis='y', colors='white')
        self.ax_spec.set_ylim(0, 1000)  # focus below 1kHz for detail
        self.ax_spec.grid(True, linestyle='--', alpha=0.3)

        self.x = np.linspace(0, 2, 1000)
        self.y_ecg = np.zeros(1000)
        self.y_icp = np.zeros(1000)
        self.ecg_wave = generate_ecg()
        self.index = 0

        self.audio_buffer = np.zeros(44100 * 2)  # 2 seconds audio buffer at 44.1 kHz

        self.im_spec = None
        self.ani = animation.FuncAnimation(self.fig, self.update, interval=50, blit=False)

    def update(self, _):
        # Update ECG waveform
        self.y_ecg = np.roll(self.y_ecg, -1)
        self.y_ecg[-1] = self.ecg_wave[self.index % len(self.ecg_wave)]

        # Update ICP waveform (simulated)
        self.y_icp = np.roll(self.y_icp, -1)
        self.y_icp[-1] = simulate_icp()

        self.index += 1

        # Update ECG and ICP plots
        self.line_ecg.set_data(self.x, self.y_ecg)
        self.line_icp.set_data(self.x, self.y_icp)

        self.ax_ecg.set_xlim(0, 2)
        self.ax_ecg.set_ylim(-1, 3)

        self.ax_icp_wave.set_xlim(0, 2)
        self.ax_icp_wave.set_ylim(0, 30)

        # Compute spectrogram from current audio buffer
        f, t_spec, Sxx = spectrogram(self.audio_buffer, fs=44100, nperseg=1024, noverlap=768)
        Sxx_log = 10 * np.log10(Sxx + 1e-10)

        # Limit freq range to 0-1000Hz for clearer visualization
        freq_mask = f <= 1000
        f = f[freq_mask]
        Sxx_log = Sxx_log[freq_mask, :]

        # Clear and redraw spectrogram axis (efficient redraw)
        if self.im_spec is None:
            self.im_spec = self.ax_spec.pcolormesh(t_spec, f, Sxx_log, shading='gouraud', cmap='magma')
            self.fig.colorbar(self.im_spec, ax=self.ax_spec, label='Power/Frequency (dB/Hz)')
        else:
            self.im_spec.set_array(Sxx_log.ravel())
            self.im_spec.set_offsets(np.c_[t_spec.repeat(len(f)), np.tile(f, len(t_spec))])
            self.im_spec.autoscale()

        return self.line_ecg, self.line_icp, self.im_spec

    def run(self):
        plt.tight_layout()
        plt.show()

    def add_audio_data(self, data):
        filtered = lowpass_filter(data, cutoff=1000, fs=44100, order=6)
        n = len(filtered)
        self.audio_buffer = np.roll(self.audio_buffer, -n)
        self.audio_buffer[-n:] = filtered

def play_music(tracks, monitor):
    pygame.mixer.init(frequency=44100, size=-16, channels=1)

    def player():
        for t in tracks:
            full_path = os.path.join(MUSIC_DIR, t)
            print(f"🎶 Playing {t}")
            try:
                pygame.mixer.music.load(full_path)
                pygame.mixer.music.play()
            except Exception as e:
                print(f"⚠️ Failed to play {t}: {e}")
                continue

            while pygame.mixer.music.get_busy():
                t_audio = np.linspace(0, 0.05, int(44100 * 0.05), False)
                sim_audio = 0.5 * np.sin(2 * np.pi * 440 * t_audio) + 0.05 * np.random.randn(len(t_audio))
                # Instead of sim_audio, you might extract real audio samples here for better accuracy
                monitor.add_audio_data(sim_audio)
                time.sleep(0.05)

    threading.Thread(target=player).start()
    monitor.run()

def main():
    tracks = get_tracks(MUSIC_DIR)
    if not tracks:
        print("❌ No music found in directory.")
        return
    monitor = BioMonitor()
    play_music(tracks, monitor)

if __name__ == '__main__':
    main()
"@

# Step 5: Save Python script
Set-Content -Path $pyScriptPath -Value $pythonScript -Encoding UTF8
Write-Host "📝 Python biosim script written to $pyScriptPath"

# Step 6: Run the biosim monitor
Write-Host "🚀 Launching biosim monitor..."
cmd /c "conda activate $envName && python `"$pyScriptPath`""

Write-Host "`n✅ All done. Press any key to close..."
[void][System.Console]::ReadKey($true)
Footer
© 2025 GitHub, Inc.
Footer navigation
Terms
Privacy
Security
Status
Docs
Contact
