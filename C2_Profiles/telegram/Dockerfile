FROM itsafeaturemythic/mythic_python_base:latest

WORKDIR /Mythic/

COPY [".", "."]

# Install required Python packages
RUN pip3 install python-telegram-bot[all]==20.7 aiofiles grpcio grpcio-tools protobuf

# Make sure the server script is executable
RUN chmod +x telegram/c2_code/server.py

CMD ["python3", "main.py"]
