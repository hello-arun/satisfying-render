import librosa
import matplotlib.pyplot as plt
import numpy as np
musicFile="../data/harry-potter-marble-music.mp3"
y, sr = librosa.load(path=musicFile,mono=True,sr=None)
y_max=np.max(y)
duration=len(y)/sr
time = np.linspace(0,duration,len(y))

print(f"Date Points: {len(y)}\n\
Sample Rate: {sr}\n\
Duration: {duration:0.3f}(sec)\n\
Y_MAX: {y_max}")

# Detect note onsets
onset_env = librosa.onset.onset_strength(y=y, sr=sr)
onset_frames = librosa.onset.onset_detect(
    onset_envelope=onset_env, 
    sr=sr,
    units="frames",
    hop_length=1000,
    )
print(onset_frames)
# onset_frames=np.array([fr for fr in onset_frames if np.max(np.abs(y[fr-3:fr+3]))>0.0*y_max])

# Convert onset frames to timestamps
onset_times = librosa.frames_to_time(onset_frames, sr=sr)
# filtered_onset_times = [onset_time for onset_time in onset_times if onset_env[onset_frames[onset_time]] >= amplitude_threshold]


# time = np.arange(0,duration,1.0/sr) #time vector
plt.plot(time,y)
plt.vlines(onset_times, -1, 1, color='r', linestyle='--', label='Beats')
# plt.specgram(y)
# plt.xlim([0,10])
np.savetxt("../data/harry-potter-marble-music.txt",onset_times*1000)
plt.show()