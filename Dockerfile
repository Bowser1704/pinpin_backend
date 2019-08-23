FROM python:3.6
COPY . /app
WORKDIR /app
EXPOSE 5000
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirement.txt
CMD ["python3", "manage.py"]