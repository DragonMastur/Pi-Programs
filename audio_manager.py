# Audio Manager
# Made by Preston Hager

import audioop
import pyaudio
import sys
import wave

class AudioRecord:
    def __init__(self, file, paramaters=[2, 2, 44100]):
        self.data = b""
        self.filename = file
        self.params = paramaters

    def writeto(self, write_data):
        self.data = self.data + bytes(write_data)
    def write(self, write_data):
        self.data = bytes(write_data)

    def writefile(self):
        writef = wave.open(self.filename, 'wb')
        writef.setnchannels(self.params[0])
        writef.setsampwidth(self.params[1])
        writef.setframerate(self.params[2])
        writef.writeframes(self.data)
        writef.close()
    def readfile(self, doread=True, keepopen=False):
        self.readf = wave.open(self.filename, 'rb')
        self.params = []
        self.params.append(self.readf.getnchannels())
        self.params.append(self.readf.getsampwidth())
        self.params.append(self.readf.getframerate())
        if doread:
            self.data = b""
            fdata = self.readfileline()
            while fdata != "":
                fdata = self.readfileline()
        if not keepopen:
            self.readf.close()
    def readfileline(self):
        data = self.readf.readframes(1024)
        self.writeto(data)
        return data
    def closeall(self):
        try: self.writef.close()
        except: pass
        try: self.readf.close()
        except: pass

    def getcur(self):
        return (self.data, self.filename)
    def setparams(self, paramaters):
        self.params = paramaters

class Recorder:
    def __init__(self, file, seconds, pyaudio_inst):
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.rate = 44100
        self.channels = 2
        self.record_seconds = seconds

        self.pyaudio_inst = pyaudio_inst
        self.data = AudioRecord(file)

    def record(self):
        self.stream = self.pyaudio_inst.open(format=self.format,
                                             channels=self.channels,
                                             rate=self.rate,
                                             input=True,
                                             frames_per_buffer=self.chunk
        )
        frames = []
        frameamount = int(self.rate / self.chunk * self.record_seconds)
        for i in range(0, frameamount):
            data = self.stream.read(self.chunk)
            frames.append(data)
        self.stream.stop_stream()
        self.stream.close()

        self.data.write(b''.join(frames))
        self.data.setparams([self.channels, self.pyaudio_inst.get_sample_size(self.format), self.rate])
        self.data.writefile()

class Player:
    def __init__(self, file, pyaudio_inst):
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.rate = 44100
        self.channels = 2

        self.pyaudio_inst = pyaudio_inst
        self.data = AudioRecord(file)
        self.data.readfile(doread=False, keepopen=True)

    def play(self):
        self.stream = self.pyaudio_inst.open(format=self.format,
                                             channels=self.channels,
                                             rate=self.rate,
                                             output=True,
        )
        play_data = self.data.readfileline()
        while play_data != "":
            self.stream.write(play_data)
            play_data = self.data.readfileline()
        self.data.closeall()
        self.stream.stop_stream()
        self.stream.close()

class Manager:
    def __init__(self):
        self.pyaudio_inst = pyaudio.PyAudio()
