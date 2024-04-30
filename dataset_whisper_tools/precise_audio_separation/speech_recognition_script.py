# import speech_recognition as sr #FIXME it's a big shit
# from pydub import AudioSegment
# import math
# import os
#
# # Функция для распознавания речи из аудиофайла
# def recognize_speech(audio_file):
#     r = sr.Recognizer()
#     with sr.AudioFile(audio_file) as source:
#         audio = r.record(source)
#     try:
#         text = r.recognize_google(audio, language="ru-RU")
#         return text
#     except sr.UnknownValueError:
#         print("Не удалось распознать речь")
#     except sr.RequestError as e:
#         print(f"Ошибка при запросе к сервису распознавания речи: {e}")
#
# # Функция для разбиения речи на сегменты
# def split_speech(audio_file, max_duration=14):
#     audio = AudioSegment.from_file(audio_file)
#     total_duration = len(audio)
#     segments = []
#     start = 0
#     end = 0
#     segment_index = 1
#
#     while start < total_duration and start + max_duration * 1000 <= total_duration:
#         # Находим ближайшую границу слова к max_duration
#         end = min(start + max_duration * 1000, len(audio))
#         word_end = find_word_end(audio[start:end])
#         segment = audio[start:start + word_end]
#         segments.append(segment)
#
#         # Сохранение сегмента в файл
#         base_name, ext = os.path.splitext(audio_file)
#         segment_file = f"{base_name}_segment_{segment_index}{ext}"
#         segment.export(segment_file, format=ext[1:])
#
#         # Распознавание речи и вывод тайм-кодов и текста
#         start_time = start / 1000
#         end_time = (start + word_end) / 1000
#         print(f"Segment {segment_index}: Start: {start_time:.2f}s, End: {end_time:.2f}s")
#         segment_text = recognize_speech(segment_file)
#         if segment_text:
#             print(f"Text: {segment_text}")
#         else:
#             print("No text recognized")
#         print()
#
#         start += word_end
#         segment_index += 1
#
#     return segments
#
# # Функция для поиска ближайшей границы слова
# def find_word_end(audio_segment):
#     silence_threshold = -40  # Порог тишины в дБ
#     chunk_size = 10  # Размер чанка в мс
#     word_end = len(audio_segment)
#
#     for i in range(len(audio_segment), 0, -chunk_size):
#         chunk = audio_segment[i - chunk_size:i]
#         if chunk.dBFS < silence_threshold:
#             word_end = i
#         else:
#             break
#
#     return word_end
#
# # Пример использования
# audio_file = "../../../../files/input/audio.wav"
# split_speech(audio_file)