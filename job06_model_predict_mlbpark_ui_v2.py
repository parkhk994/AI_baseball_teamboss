import pickle  # 타입변환 없이 binary 코드로 저장
import pandas as pd  # dataFrame 문자열을 맞는 데이터타입으로 변환
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from keras.utils import to_categorical
from konlpy.tag import Okt  # open korean tokenizer, java 기반
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from keras.models import load_model
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QMovie  # QMovie를 사용하여 GIF 애니메이션을 표시합니다.

form_window = uic.loadUiType('./mainWidget.ui')[0]

class Exam(QWidget, form_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.model = load_model(
            './models/MP_KBO_category_classification_model_0.6137456893920898.h5')
        self.btn_save.clicked.connect(self.save_and_predict)  # CSV 저장 및 예측 버튼 연결

    def save_and_predict(self):
        text = self.textEdit_repl.toPlainText()  # QTextEdit에서 텍스트 가져오기
        if text:  # 텍스트가 비어있지 않은 경우
            # CSV 파일로 저장
            with open('./crawling_data/output.csv', 'w', encoding='utf-8') as file:  # CSV 파일 열기
                file.write('titles,category\n')
                file.write(text + ',KBO')  # 텍스트를 파일에 쓰기
            print("CSV 파일로 저장되었습니다.")
            self.lbl_predict.setText("댓글 분석 중...")

            # 데이터 로드 및 전처리
            self.lbl_predict.setText("댓글 분석 중...")
            df = pd.read_csv('./crawling_data/output.csv')
            df.drop_duplicates(inplace=True)
            df.reset_index(drop=True, inplace=True)

            print(df.head())
            df.info()
            print(df['category'].value_counts())

            # 공백 제거
            df['category'] = df['category'].str.strip()
            X = df['titles']
            Y = df['category']

            # 레이블 인코더 재생성
            encoder = LabelEncoder()
            encoder.fit(Y)  # 현재 데이터셋에 맞게 인코더 적합

            # 레이블 변환
            label = encoder.classes_
            print("Labels:", label)

            # 레이블을 숫자로 인코딩
            labeled_y = encoder.transform(Y)

            # 원-핫 인코딩 (10개 클래스에 맞게)
            onehot_Y = to_categorical(labeled_y, num_classes=10)
            print("One-hot encoded labels shape:", onehot_Y.shape)

            # x 문장데이터 처리, 불용어 제거
            okt = Okt()
            X_morphs = []
            for title in X:
                X_morphs.append(okt.morphs(title, stem=True))

            # stopwords 불용어 다운로드
            stopwords = pd.read_csv('./crawling_data/stopwords.csv', index_col=0)

            # 불용어 제거
            X_cleaned = []
            for sentence in X_morphs:
                words = [word for word in sentence if len(word) > 1 and word not in list(stopwords['stopword'])]
                X_cleaned.append(' '.join(words))

            # 토큰나이징
            with open('models/MP_KBO_token_max_37.pickle', 'rb') as f:
                token = pickle.load(f)
            tokened_X = token.texts_to_sequences(X_cleaned)

            # 토큰 길이 제한
            for i in range(len(tokened_X)):
                if len(tokened_X[i]) > 37:
                    tokened_X[i] = tokened_X[i][:37]

            # 패딩
            X_pad = pad_sequences(tokened_X, maxlen=37)

            # 예측
            preds = self.model.predict(X_pad)

            # 모든 클래스를 포함하도록 레이블 설정
            all_labels = ['DOOSAN', 'HANWHA', 'KIA', 'KIWOOM', 'KT', 'LG', 'LOTTE', 'NC', 'SAMSUNG', 'SSG']

            # 예측 코드 수정
            predicts = []
            for pred in preds:
                most_index = np.argmax(pred)
                most = all_labels[most_index]
                pred[most_index] = 0
                second_index = np.argmax(pred)
                second = all_labels[second_index]
                predicts.append([most, second])

            df['predict'] = predicts

            print(df.head(30))

            # 모델 평가
            score = self.model.evaluate(X_pad, onehot_Y)
            print("Model Evaluation Score:", score[1])

            # 예측 정확도 계산
            df['OX'] = 0
            for i in range(len(df)):
                if df.loc[i, 'category'] in df.loc[i, 'predict']:
                    df.loc[i, 'OX'] = 1

            print("Prediction Accuracy:", df['OX'].mean())

            # 예측 결과를 GUI에 표시
            if predicts:
                most_predicted = predicts[0][0]  # 첫 번째 예측 결과의 가장 높은 확률 클래스
                self.lbl_predict.setText(f"예측 결과: {most_predicted}")
            #all_labels = ['DOOSAN', 'HANWHA', 'KIA', 'KIWOOM', 'KT', 'LG', 'LOTTE', 'NC', 'SAMSUNG', 'SSG']
                # 예측 팀에 따라 GIF 표시
                if most_predicted == 'DOOSAN':
                    movie = QMovie('image/doosan.gif')  # 한화 GIF 경로
                    self.lbl_image.setMovie(movie)  # lbl_image에 GIF 설정
                    movie.start()  # GIF 애니메이션 시작
                elif most_predicted == 'HANWHA':
                    movie = QMovie('image/hanwha.gif')  # 한화 GIF 경로
                    self.lbl_image.setMovie(movie)  # lbl_image에 GIF 설정
                    movie.start()  # GIF 애니메이션 시작
                elif most_predicted == 'KIA':
                    movie = QMovie('image/kia.gif')  # 한화 GIF 경로
                    self.lbl_image.setMovie(movie)  # lbl_image에 GIF 설정
                    movie.start()  # GIF 애니메이션 시작
                elif most_predicted == 'KIWOOM':
                    movie = QMovie('image/kiwoom.gif')  # 한화 GIF 경로
                    self.lbl_image.setMovie(movie)  # lbl_image에 GIF 설정
                    movie.start()  # GIF 애니메이션 시작
                elif most_predicted == 'KT':
                    movie = QMovie('image/kt.gif')  # 키움 GIF 경로
                    self.lbl_image.setMovie(movie)  # lbl_image에 GIF 설정
                    movie.start()  # GIF 애니메이션 시작
                elif most_predicted == 'LG':
                    movie = QMovie('image/lg.gif')  # 키움 GIF 경로
                    self.lbl_image.setMovie(movie)  # lbl_image에 GIF 설정
                    movie.start()  # GIF 애니메이션 시작
                elif most_predicted == 'LOTTE':
                    movie = QMovie('image/lotte.gif')  # 키움 GIF 경로
                    self.lbl_image.setMovie(movie)  # lbl_image에 GIF 설정
                    movie.start()  # GIF 애니메이션 시작
                elif most_predicted == 'NC':
                    movie = QMovie('image/nc.gif')  # 키움 GIF 경로
                    self.lbl_image.setMovie(movie)  # lbl_image에 GIF 설정
                    movie.start()  # GIF 애니메이션 시작
                elif most_predicted == 'SAMSUNG':
                    movie = QMovie('image/samsung.gif')  # 키움 GIF 경로
                    self.lbl_image.setMovie(movie)  # lbl_image에 GIF 설정
                    movie.start()  # GIF 애니메이션 시작
                elif most_predicted == 'SSG':
                    movie = QMovie('image/ssg.gif')  # 키움 GIF 경로
                    self.lbl_image.setMovie(movie)  # lbl_image에 GIF 설정
                    movie.start()  # GIF 애니메이션 시작
                else:
                    self.lbl_image.clear()  # 다른 팀일 경우 이미지 지우기

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Exam()
    window.show()
    sys.exit(app.exec_())