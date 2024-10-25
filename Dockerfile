FROM pytorch/pytorch:2.3.1-cuda12.1-cudnn8-runtime

# 작업 디렉토리 설정
WORKDIR /app

# requirements.txt 파일 복사 및 패키지 설치
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 현재 디렉토리의 모든 파일을 /app 디렉토리로 복사
COPY . /app

# Streamlit 앱 실행 시 포트 번호 지정
CMD ["streamlit", "run", "app.py", "--server.port=8507"]
