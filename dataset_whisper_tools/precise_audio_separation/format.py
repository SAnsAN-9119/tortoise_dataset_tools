import ffmpeg

input_file = "../../../../files/input/audio.mp3"
output_file = "../../../../files/input/audio.wav"

stream = ffmpeg.input(input_file)
stream = ffmpeg.output(stream, output_file)
ffmpeg.run(stream)