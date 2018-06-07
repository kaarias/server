import socket
import pyaudio
import wave
import audioop
import struct
from threading import Thread


frames = []
HOST = ''
PORT = 9090
BUFFER = 30

#recieves audio packets
def udpStream(CHUNK):
	#create and bind socket
	udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	udp.bind((HOST, PORT))
	print("socket binding successful")
	
	#recieve packets of audio
	while True:
		soundData, addr = udp.recvfrom((CHUNK) * CHANNELS * 2)
		frames.append(soundData)
	udp.close()

#plays the packets when enough are in the buffer			
def play(stream, CHUNK):
	while True:
		if len(frames) == BUFFER:
			while True:
				try:
					stream.write(frames.pop(0), CHUNK)
				except:
					pass

if __name__ == "__main__":
	FORMAT = pyaudio.paInt16
	CHUNK = 1024
	CHANNELS = 2
	RATE = 44100
	
	p = pyaudio.PyAudio()

	stream = p.open(format = FORMAT,
			channels = CHANNELS,
			rate = RATE,
			output = True,
			input = True,
			frames_per_buffer = CHUNK,
			)
	#makes and starts 2 threads one for recieving and one for playing
	Ts = Thread(target = udpStream, args=(CHUNK,))
	Tp = Thread(target = play, args = (stream, CHUNK,))
	Ts.setDaemon(True)
	Tp.setDaemon(True)
	Ts.start()
	Tp.start()
	Ts.join()
	Tp.join()


