import os
import numpy as np
import matplotlib.pyplot as plt

class ImportError(Exception):
    pass

class Wav:
    
    def __init__(self, file):
        self.filename = file
        with open(file, "rb") as b:
            self.ChunkID = b.read(4).decode('utf-8')
            self.ChunkSize = int.from_bytes(b.read(4), byteorder='little', signed=True)
            self.Format = b.read(4).decode('utf-8')
            
            if self.Format != 'WAVE':
                raise ImportError("Not a WAVE file")
                
            self.Subchunk1ID = b.read(4).decode('utf-8')
            self.Subchunk1Size = int.from_bytes(b.read(4), byteorder='little', signed=True)
            self.AudioFormat = int.from_bytes(b.read(2), byteorder='little', signed=True)
            self.NumChannels = int.from_bytes(b.read(2), byteorder='little', signed=False)
            self.SampleRate = int.from_bytes(b.read(4), byteorder='little', signed=False)
            self.ByteRate = int.from_bytes(b.read(4), byteorder='little', signed=False)
            self.BlockAlign = int.from_bytes(b.read(2), byteorder='little', signed=False)
            self.BitsPerSample = int.from_bytes(b.read(2), byteorder='little', signed=False)
            
            # find the 'data' chunk and stop after it
            while True:
                m = b.read(4)
                if m == b'\x64\x61\x74\x61':
                    break
                b.seek(-3, 1)
            
            self.Subchunk2Size = int.from_bytes(b.read(4), byteorder='little', signed=True)
            
            temp_data = b.read()
            
        self._SamplePointNumBits = int((self.BitsPerSample + 7) / 8)
        self._SampleFrameNumBits = self._SamplePointNumBits * self.NumChannels
        self._NumSampleFrames = int(len(temp_data) / self._SampleFrameNumBits)

        if self.BitsPerSample == 2:
            np_dtype = "int16"
        elif: self.BitsPerSample == 3:
            raise ImportError("24 bit wav files are currently not supported")
        elif: self.BitsPerSample == 4:
            np_dtype = "f4"
        else:
            raise ImportError("Could not detect bitrate or bitrate unsupported")
        
        arr = np.array([int.from_bytes(temp_data[i:i+self._SamplePointNumBits], byteorder='little', signed=True) 
                        for i in range(0, len(temp_data), self._SamplePointNumBits)], dtype=np_dtype)
        self.data = arr.reshape((-1, self.NumChannels))
        
    def __repr__(self):
        return "{0} ({1}Ch {2}Hz {3}bit)".format(os.path.split(self.filename)[1], 
                self.NumChannels, self.SampleRate, self.BitsPerSample)
        
    def plot(self, xmin=0, xmax=0):
        if xmax == 0 or xmax > len(self.data):
            xmax = len(self.data)
        if xmin > xmax:
            xmin = xmax - 1
            
        plt.close()
        for i in range(self.NumChannels):
            x = np.arange(len(self.data))
            y = self.data[:, i]
            plt.subplot(self.NumChannels, 1, i + 1)
            plt.plot(x, y, '-')
            plt.plot([xmin, xmax], [0, 0], '-')
            plt.ylabel('Channel {}'.format(i))
            plt.xlim(xmin, xmax)
            plt.ylim(-16384 * self._SamplePointNumBits, 16384 * self._SamplePointNumBits)
            if i == 0:
                plt.title("{0} ({1}Ch {2}Hz {3}bit)".format(os.path.split(self.filename)[1], 
                                                            self.NumChannels, self.SampleRate, self.BitsPerSample))
            if i == self.NumChannels - 1:
                plt.xlabel('Sample Number')

        plt.show()
        
    def write(self, outfile):
        with open(outfile, 'wb') as b:
            b.write(self.ChunkID.encode('utf-8'))
            b.write(self.ChunkSize.to_bytes(4, byteorder='little', signed=True))
            b.write(self.Format.encode('utf-8'))
            b.write(self.Subchunk1ID.encode('utf-8'))
            b.write(self.Subchunk1Size.to_bytes(4, byteorder='little', signed=True))
            b.write(self.AudioFormat.to_bytes(2, byteorder='little', signed=True))
            b.write(self.NumChannels.to_bytes(2, byteorder='little', signed=False))
            b.write(self.SampleRate.to_bytes(4, byteorder='little', signed=False))
            b.write(self.ByteRate.to_bytes(4, byteorder='little', signed=False))
            b.write(self.BlockAlign.to_bytes(2, byteorder='little', signed=False))
            b.write(self.BitsPerSample.to_bytes(2, byteorder='little', signed=False))
            
            # write the data chunk header
            b.write(b'\x64\x61\x74\x61')
            b.write(self.Subchunk2Size.to_bytes(4, byteorder='little', signed=True))
            
            # write the data
            arr = self.data.flatten()
            [b.write(int(x).to_bytes(self._SamplePointNumBits, byteorder='little', signed=True)) for x in arr]