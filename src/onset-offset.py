import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
# Load the audio file
audio_file = '../data/mario-marble-music.wav'
y, sr = librosa.load(
    path=audio_file,
    mono=True,
    offset=0,
    duration=3)

duration=len(y)/sr
time = np.linspace(0,duration,len(y))
print(time)
onset_env = librosa.onset.onset_strength(y=y, sr=sr)

# Find the onset times
onset_frames = librosa.onset.onset_detect(
    onset_envelope=onset_env, 
    sr=sr,
    hop_length=512)


D = librosa.stft(y)
S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
S_db_filtered = np.where(S_db > -20, S_db, np.min(S_db))


max_freq_indices = np.argmax(S_db, axis=0)

# Convert frame indices to time (in seconds)
times = librosa.frames_to_time(np.arange(len(max_freq_indices)), sr=sr)

# Get the corresponding frequencies for the maximum amplitude
max_freqs = librosa.fft_frequencies(sr=sr)[max_freq_indices]
# Print the times and corresponding maximum frequencies
for t, freq in zip(times, max_freqs):
    print(f"Time: {t:.2f} s, Max Frequency: {freq:.2f} Hz")
onset_times = librosa.frames_to_time(onset_frames, sr=sr)
# Plot the audio waveform and onset/offset times
fig, [[ax,ax2]]=plt.subplots(1,2,squeeze=False)
img = librosa.display.specshow(S_db_filtered, x_axis='time', y_axis='log', ax=ax)
ax.set(title='Now with labeled axes!')
fig.colorbar(img, ax=ax, format="%+2.f dB")
ax2.plot(time, y, alpha=0.5)

print(onset_times)
for val in onset_times:
    ax.axvline(val,color='g', linestyle='--')
    ax2.axvline(val,color='g', linestyle='--')
# plt.vlines(offset_times, -1, 1, color='g', linestyle='--', label='Offset Times')
plt.legend()
plt.show()
