from service import EmotionService


def main():
    input_text = "I hnestly feal she'd be a beter leadr than the current lot."
    print("Input text: ", input_text)
    emotion_service = EmotionService()

    clean_text = emotion_service.get_autocorrected_text(input_text)
    print("Cleaned text: ", clean_text)

    emotion_result = emotion_service.get_text2emotion(clean_text)
    print("Emotion result: ", emotion_result)

if __name__ == '__main__':
    main()
