# from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor  #FIXME It's a bull shit
# import soundfile as sf
# import torch
# import subprocess
#
# def resample_audio(input_file, output_file, new_sample_rate=16000):
#     command = ['ffmpeg', '-i', input_file, '-ar', str(new_sample_rate), output_file]
#     subprocess.run(command, check=True)
#
#
# # Загрузка предварительно обученной модели и токенизатора
# processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-large-960h")
# model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-960h")
#
# # Функция для распознавания речи из аудиофайла
# def recognize_speech(speech, sample_rate, processor, model):
#     # Преобразование речи во входные значения
#     input_values = processor(speech, sampling_rate=sample_rate, return_tensors="pt").input_values
#
#     # Получение логитов модели
#     logits = model(input_values).logits
#
#     # Декодирование логитов в текст
#     predicted_ids = torch.argmax(logits, dim=-1)
#     transcription = processor.batch_decode(predicted_ids)
#     return transcription[0]
#
# # Функция для разделения аудио на сегменты
# def split_audio(audio_input, segment_length=15):
#     # Чтение аудиофайла
#     speech, sample_rate = sf.read(audio_input)
#     total_seconds = len(speech) / sample_rate
#     segments = []
#
#     # Разделение аудио на сегменты
#     for start_time in range(0, int(total_seconds), segment_length):
#         end_time = start_time + segment_length
#         if end_time > total_seconds:
#             end_time = total_seconds
#         segment = speech[int(start_time * sample_rate):int(end_time * sample_rate)]
#         segments.append(segment)
#     return segments, sample_rate
#
# # Обработка аудиофайла и получение сегментов
# audio_segments, sample_rate = split_audio("../../../../files/input/output_audio.mp3")
#
# # Распознавание текста для каждого сегмента
# for segment in audio_segments:
#     transcription = recognize_speech(segment, sample_rate, processor, model)
#     # Здесь должна быть логика для проверки, что слова не обрезаны
#     print(transcription)
